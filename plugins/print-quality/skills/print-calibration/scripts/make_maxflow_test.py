#!/usr/bin/env python3
"""Turn a vase-mode cylinder G-code into a max volumetric flow test.

The flow steps up with height: START mm3/s from Z_START, +STEP every BAND mm.
Each step is announced on the printer screen (M117) and listed at the end so
you can read the result with a ruler.

How to make the input (any slicer):
  * a cylinder about 36 mm wide and 66 mm tall
  * spiral vase mode on, 3 bottom layers, layer height 0.28 (0.2 also works)
  * outer wall line width about 0.5 mm
  * arc fitting OFF (G2/G3 moves are refused, not guessed)
  * slow-down-for-cooling off if your slicer has it (this script resets speeds anyway)

    python make_maxflow_test.py vase.gcode maxflow_test.gcode
    python make_maxflow_test.py vase.gcode out.gcode --start 4 --step 1 --band 4.5

Only standard Python 3, no packages.
"""
import argparse
import math
import re
import sys

MOVE = re.compile(r"([XYZEF])(-?\d*\.?\d+)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--start", type=float, default=6.0, help="first flow, mm3/s (default 6)")
    ap.add_argument("--step", type=float, default=1.0, help="flow added per band, mm3/s (default 1)")
    ap.add_argument("--band", type=float, default=4.5, help="band height, mm (default 4.5)")
    ap.add_argument("--z-start", type=float, default=2.0, help="height where the ramp starts, mm (default 2)")
    ap.add_argument("--filament", type=float, default=1.75, help="filament diameter, mm (default 1.75)")
    ap.add_argument("--max-speed", type=float, default=300.0, help="refuse feedrates above this, mm/s (default 300)")
    a = ap.parse_args()

    area = math.pi * (a.filament / 2) ** 2
    x = y = z = e_last = 0.0
    e_abs = False
    out, bands, last_band, top_speed, ref = [], [], None, 0.0, 0.0

    for n, line in enumerate(open(a.src, encoding="utf-8", errors="replace"), 1):
        s = line.rstrip("\n")
        code = s.split(";", 1)[0].strip()
        if code.startswith(("G2 ", "G3 ")) or code in ("G2", "G3"):
            print(f"line {n}: arc move found. Turn arc fitting off in the slicer and slice again.", file=sys.stderr)
            return 1
        if code.startswith("M82"):
            e_abs = True
        elif code.startswith("M83"):
            e_abs = False
        elif code.startswith("G92") and "E" in code:
            e_last = float(dict(MOVE.findall(code)).get("E", 0))
        if code.startswith(("G1 ", "G0 ")):
            m = dict(MOVE.findall(code))
            nx, ny, nz = float(m.get("X", x)), float(m.get("Y", y)), float(m.get("Z", z))
            de = None
            if "E" in m:
                ev = float(m["E"])
                de = ev - e_last if e_abs else ev
                if e_abs:
                    e_last = ev
            d = math.hypot(nx - x, ny - y)
            per_mm = de * area / d if (de is not None and de > 0 and d > 0.05) else 0.0
            if nz >= a.z_start:
                ref = max(ref, per_mm)
            # Vase mode tapers extrusion to zero on the last loop; leave those moves alone.
            if per_mm > 0 and per_mm >= 0.85 * ref and nz >= a.z_start:
                band = int((nz - a.z_start) // a.band)
                flow = a.start + a.step * band
                if band != last_band:
                    out.append(f"; ===== FLOW {flow:g} mm3/s from Z {a.z_start + band * a.band:.1f} =====")
                    out.append(f"M117 Flow {flow:g} mm3/s")
                    bands.append((a.z_start + band * a.band, flow))
                    last_band = band
                feed = flow / per_mm  # mm/s
                top_speed = max(top_speed, feed)
                s = re.sub(r"\s*F\d*\.?\d+", "", code) + f" F{feed * 60:.0f}"
            x, y, z = nx, ny, nz
        out.append(s)

    if not bands:
        print("No extrusion found above --z-start. Is this a vase-mode cylinder?", file=sys.stderr)
        return 1
    if top_speed > a.max_speed:
        print(f"Top band needs {top_speed:.0f} mm/s, above --max-speed {a.max_speed:g}. "
              "Lower --start/--step or raise --max-speed if your printer allows it.", file=sys.stderr)
        return 1

    table = ["; ===== READING THE TEST =====",
             "; Measure from the bed. Find the lowest height where the wall turns rough, matte,",
             "; thin or gappy ALL the way round. Set max volumetric speed 10-20% below that band.",
             "; height_mm  flow_mm3s"]
    table += [f"; {zb:5.1f} - {zb + a.band:5.1f}  {fl:g}" for zb, fl in bands]
    open(a.dst, "w", encoding="utf-8").write("\n".join(out + table) + "\n")
    print(f"wrote {a.dst}: {len(bands)} bands, {bands[0][1]:g} to {bands[-1][1]:g} mm3/s, top speed {top_speed:.0f} mm/s")
    for zb, fl in bands:
        print(f"  {zb:5.1f} - {zb + a.band:5.1f} mm  ->  {fl:g} mm3/s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
