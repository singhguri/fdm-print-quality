#!/usr/bin/env python3
"""Apply print-quality defaults to OrcaSlicer process presets (JSON).

Works on any Orca-family process preset file: user presets in the Orca
config folder, or flattened profiles you pass to the command line.

    python apply_orca_quality.py PRESET.json [PRESET.json ...] [--dry-run]
    python apply_orca_quality.py PRESET.json --brim keep      # leave brim settings alone
    python apply_orca_quality.py PRESET.json --extras         # also apply the safe extras

Each changed file gets a .bak copy next to it first (once; an existing .bak is kept).
Presets whose brim is switched off (brim_type = no_brim) keep it off.
"""
import argparse
import json
import pathlib
import shutil
import sys

# The five core rules.
CORE = {
    # Arachne varies line width to fit thin features, so small text and
    # fine detail print as solid strokes instead of gaps.
    "wall_generator": "arachne",
    # Scarf seam: the outer wall ramps up and overlaps itself instead of
    # starting and stopping in one spot. Only applied where the seam
    # cannot hide in a sharp corner (conditional).
    "seam_slope_type": "external",
    "seam_slope_conditional": "1",
    # A scarf length of 0 silently disables the scarf. Some vendor
    # profiles ship with 0, so set a real length.
    "seam_slope_min_length": "20",
}

# Mouse ears instead of a full outer brim.
EARS = {"brim_type": "brim_ears", "brim_ears_max_angle": "125"}

# Safe extras: no calibration needed, low risk on most printers.
EXTRAS = {
    "top_surface_pattern": "monotonicline",
    "top_shell_thickness": "1",
    "elefant_foot_compensation": "0.15",
    "reduce_crossing_wall": "1",
    "precise_outer_wall": "1",
}


def patch(path: pathlib.Path, brim: str, extras: bool, dry_run: bool) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("type", "process") != "process":
        print(f"skip {path.name}: type is {data.get('type')!r}, not a process preset")
        return
    wanted = dict(CORE)
    if brim == "ears" and data.get("brim_type") != "no_brim":
        wanted.update(EARS)
    if extras:
        wanted.update(EXTRAS)
    changes = {k: (data.get(k), v) for k, v in wanted.items() if str(data.get(k)) != v}
    if not changes:
        print(f"ok   {path.name}: already applied")
        return
    for k, (old, new) in changes.items():
        print(f"     {path.name}: {k} {old!r} -> {new!r}")
    if dry_run:
        return
    bak = path.with_suffix(path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(path, bak)
    data.update({k: v for k, (_, v) in changes.items()})
    path.write_text(json.dumps(data, indent=4), encoding="utf-8")
    print(f"done {path.name} ({len(changes)} changes, backup {bak.name})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("presets", nargs="+", type=pathlib.Path)
    ap.add_argument("--brim", choices=["ears", "keep"], default="ears")
    ap.add_argument("--extras", action="store_true", help="also apply the safe extras")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for p in a.presets:
        if not p.is_file():
            print(f"missing {p}", file=sys.stderr)
            return 1
        patch(p, a.brim, a.extras, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
