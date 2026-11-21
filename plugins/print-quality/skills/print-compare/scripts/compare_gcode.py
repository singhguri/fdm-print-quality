#!/usr/bin/env python3
"""Compare sliced G-code files to explain why one print finished better than another.

For each file it reports:
  1. settings that differ (from the slicer's settings block at the end of the file)
  2. the share of extruded plastic that went into each line type (outer wall, inner wall,
     solid infill, sparse infill, bridges ...)
  3. retractions per layer, and per part per layer
  4. optional (--stl): extruded plastic vs the part's volume, to check for over-extrusion

Works with OrcaSlicer and Bambu Studio G-code (';TYPE:' comments, '; key = value' settings
block). PrusaSlicer G-code works for the settings diff; its line types use the same ;TYPE: tags.
Plain Python 3, no packages.

  python compare_gcode.py good.gcode bad.gcode
  python compare_gcode.py good.gcode bad.gcode --parts 5 4 --stl good.stl bad.stl
"""
import argparse
import math
import re
import struct
import sys
from collections import Counter

# Keys that always differ between files and say nothing about print quality.
NOISE = ("thumbnail", "compatible", "inherits", "_settings_id", "gcode", "notes", "post_process",
         "template", "time_lapse", "wipe_tower", "printer_model", "printer_variant", "host_type",
         "print_host", "printhost", "upload", "filament_vendor", "filament_ids", "plate_name")
E_RE = re.compile(r"E(-?[\d.]+)")
# Settings worth seeing even when they match, so nobody has to grep for them.
KEY_SETTINGS = ("layer_height", "wall_loops", "sparse_infill_density", "sparse_infill_pattern",
                "wall_generator", "seam_position", "seam_slope_type", "outer_wall_speed",
                "nozzle_temperature", "fan_max_speed", "retraction_length", "z_hop",
                "reduce_infill_retraction", "enable_pressure_advance", "pressure_advance",
                "ironing_type")


def read_config(path):
    """Return the '; key = value' settings block written at the end of the G-code."""
    cfg, inside = {}, False
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "CONFIG_BLOCK_START" in line or "prusaslicer_config = begin" in line:
                inside = True
                continue
            if "CONFIG_BLOCK_END" in line or "prusaslicer_config = end" in line:
                break
            if inside:
                m = re.match(r";\s*([\w\-]+)\s*=\s*(.*)", line.rstrip("\n"))
                if m:
                    cfg[m.group(1)] = m.group(2).strip()
    return cfg


def scan(path):
    """Extrusion per line type, layers, retractions, labelled objects, M900 (pressure advance) lines."""
    ext, kind = Counter(), "unknown"
    layers = retracts = m900 = 0
    objects = set()
    relative, last_e = True, 0.0
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith(";TYPE:"):
                kind = line[6:].strip()
            elif line.startswith(";LAYER_CHANGE"):
                layers += 1
            elif line.startswith("M486 A") or line.startswith("EXCLUDE_OBJECT_DEFINE"):
                objects.add(line.split()[1])
            elif line.startswith("M900"):
                m900 += 1
            elif line.startswith("M82"):
                relative = False
            elif line.startswith("M83"):
                relative = True
            elif line.startswith("G92") and " E" in line:
                last_e = float(E_RE.search(line).group(1))
            elif line.startswith(("G1 ", "G0 ", "G2 ", "G3 ")):
                m = E_RE.search(line)
                if not m:
                    continue
                e = float(m.group(1))
                if relative:
                    d = e
                else:
                    d, last_e = e - last_e, e
                if d < 0:
                    retracts += 1
                elif d > 0 and ("X" in line or "Y" in line):
                    ext[kind] += d
    return ext, max(layers, 1), retracts, len(objects), m900


def stl_volume_cm3(path):
    """Signed-tetrahedron volume of a binary or ASCII STL."""
    data = open(path, "rb").read()
    if data[:5].lower() == b"solid" and b"facet" in data[:1000]:
        v = [tuple(map(float, x)) for x in re.findall(rb"vertex\s+(\S+)\s+(\S+)\s+(\S+)", data)]
        tris = [v[i:i + 3] for i in range(0, len(v) - 2, 3)]
    else:
        n = struct.unpack_from("<I", data, 80)[0]
        tris = []
        for i in range(n):
            f = struct.unpack_from("<9f", data, 84 + i * 50 + 12)
            tris.append((f[0:3], f[3:6], f[6:9]))
    vol = 0.0
    for a, b, c in tris:
        vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    return abs(vol) / 1000.0


def filament_cm3(path, cfg):
    """Total extruded volume from the slicer's summary lines."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        f.seek(max(0, f.tell() - 400_000))
        text = f.read().decode("utf-8", "ignore")
    m = re.search(r"; (?:total )?filament used \[mm3\] = ([\d.]+)", text)
    if m:
        return float(m.group(1)) / 1000.0
    m = re.search(r"; (?:total )?filament used \[mm\] = ([\d.]+)", text)
    if m:
        dia = float(cfg.get("filament_diameter", "1.75").split(",")[0])
        return float(m.group(1)) * math.pi * (dia / 2) ** 2 / 1000.0
    return None


def pct(counter, key_filter=None):
    total = max(sum(counter.values()), 1e-9)
    if key_filter is None:
        return {k: v / total * 100 for k, v in counter.items()}
    return sum(v for k, v in counter.items() if key_filter(k)) / total * 100


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("gcode", nargs="+", help="two or more G-code files, best print first")
    ap.add_argument("--parts", nargs="+", type=int,
                    help="separate parts on each plate (default: object labels in the G-code; "
                         "several bodies merged into one STL count as 1, so pass this then)")
    ap.add_argument("--stl", nargs="+", help="the STL that was sliced for each G-code, same order")
    a = ap.parse_args()
    if len(a.gcode) < 2:
        ap.error("give at least two G-code files")
    names = [p.replace("\\", "/").split("/")[-1] for p in a.gcode]
    cfgs = [read_config(p) for p in a.gcode]

    print("== Settings that differ")
    shown = 0
    for k in sorted(set().union(*cfgs)):
        if any(s in k for s in NOISE):
            continue
        vals = [c.get(k, "<none>") for c in cfgs]
        if len(set(vals)) > 1:
            shown += 1
            print(f"  {k}: " + " | ".join(v[:40] for v in vals))
    if not shown:
        print("  none")

    scans = [scan(p) for p in a.gcode]
    print("\n== Key settings (shown even when they match)")
    for k in KEY_SETTINGS:
        vals = [c.get(k, "<none>") for c in cfgs]
        if any(v != "<none>" for v in vals):
            tag = "same" if len(set(vals)) == 1 else "DIFF"
            print(f"  [{tag}] {k}: " + " | ".join(v[:30] for v in vals))
    print("  M900 pressure-advance commands in the G-code: " + " | ".join(str(s[4]) for s in scans)
          + "  (0 means pressure advance was not set by the slicer)")
    shares = [pct(s[0]) for s in scans]
    kinds = sorted(set().union(*shares), key=lambda k: -max(s.get(k, 0) for s in shares))
    print("\n== Where the plastic goes (% of extrusion by line type)")
    print("  " + f"{'line type':24s}" + "".join(f"{n[:18]:>20s}" for n in names))
    for k in kinds:
        row = [s.get(k, 0) for s in shares]
        if max(row) >= 0.5:
            print("  " + f"{k:24s}" + "".join(f"{v:19.1f}%" for v in row))
    is_wall = lambda k: "wall" in k.lower() or "perimeter" in k.lower()
    print("  " + f"{'ALL WALLS':24s}" + "".join(f"{pct(s[0], is_wall):19.1f}%" for s in scans))

    print("\n== Retractions")
    for i, (n, s) in enumerate(zip(names, scans)):
        parts = a.parts[i] if a.parts and i < len(a.parts) else max(s[3], 1)
        print(f"  {n}: {s[2]} retractions over {s[1]} layers = {s[2] / s[1]:.1f}/layer, "
              f"{s[2] / s[1] / parts:.1f} per part per layer ({parts} part{'s' if parts != 1 else ''})")
    if not a.parts:
        print("  (part counts come from object labels; pass --parts if bodies were merged into one STL)")

    if a.stl:
        print("\n== Extruded plastic vs part volume")
        for n, g, c, stl in zip(names, a.gcode, cfgs, a.stl):
            vol, used = stl_volume_cm3(stl), filament_cm3(g, c)
            if used is None:
                print(f"  {n}: no 'filament used' line found")
            else:
                print(f"  {n}: part {vol:.1f} cm3, extruded {used:.1f} cm3 = {used / vol * 100:.0f}% of solid")
        print("  (a 100%-infill part well over 100% points at over-extrusion; brims and supports add a little)")


if __name__ == "__main__":
    sys.exit(main())
