---
name: print-calibration
description: The order and method for calibrating an FDM 3D printer and filament - Z offset and first layer, temperature tower, max volumetric flow, pressure advance (linear advance), flow ratio, retraction, then tolerance and XY compensation - with OrcaSlicer's built-in calibration tests. Use when the user gets a new printer or a new filament, sees stringing, gaps, blobs at corners, rough top surfaces, loose or tight fits, or asks how to calibrate or tune their printer.
---

# Printer and filament calibration

Calibrate in this order. Each step changes what the next one measures, so doing them out of
order wastes prints. OrcaSlicer has most of these tests under its **Calibration** menu.

| Step | What | How to judge | OrcaSlicer setting |
|---|---|---|---|
| 0 | Z offset / first layer | Print a single-layer square. Lines should be flat and touching, not round and separate (too high) or ridged and see-through (too low). Paper is only a starting point. | firmware Z offset |
| 1 | Temperature | Temperature tower. Pick the coolest section with clean bridges and no stringing. | `nozzle_temperature` |
| 2 | Max volumetric speed | Speed test until the walls under-extrude. Set the limit 10 to 20% below that. Spool labels often overstate it. | `filament_max_volumetric_speed` |
| 3 | Pressure advance | Orca's pattern or tower test. Pick the value with sharp corners and no gap or bulge at line ends. | `enable_pressure_advance = 1`, `pressure_advance = K` |
| 4 | Flow ratio | Orca's flow test. Judge the **top surface**: pick the smoothest patch with no gaps and no ridges. | `filament_flow_ratio` |
| 5 | Retraction | Retraction tower after steps 3 and 4. Direct drive is usually 0.5 to 1.5 mm, Bowden longer. | `retraction_length`, `retraction_speed` |
| 6 | Tolerance | Tolerance test last. Fix tight holes with hole compensation, not with flow. | `xy_hole_compensation`, `xy_contour_compensation` |

## Step 2 in detail: max volumetric flow

**Making the test.** In OrcaSlicer's GUI use Calibration > Max flowrate. Without the GUI (other
slicers, or command-line slicing), use `scripts/make_maxflow_test.py` in this skill's folder:

1. Slice a cylinder about 36 mm wide and 66 mm tall in **spiral vase mode**: 3 bottom layers,
   0.28 mm layers, outer wall line width about 0.5 mm, **arc fitting off**.
2. `python scripts/make_maxflow_test.py vase.gcode maxflow_test.gcode`
   It rewrites the speeds so flow starts at 6 mm³/s at 2 mm and rises 1 mm³/s every 4.5 mm
   (change with `--start`, `--step`, `--band`), shows the current flow on the printer screen,
   prints a height-to-flow table, and refuses to write a file that would need more than
   300 mm/s (`--max-speed`). Relative and absolute extrusion both work.

**Reading it.** Flow at height h is `start + step * floor((h - z_start) / band)`; the script's
table (also at the end of the G-code) saves the arithmetic. Measure from the bed with a ruler.

- Look for the lowest height where the wall turns matte, fuzzy, thin, wavy or gappy. A camera at
  a distance is not good enough; check it in hand, all the way round.
- **Rough on only some sides** (often two opposite sides) means a direction-related limit as well
  as melting: the bed shaking on a bed-slinger, or the part fan cooling one side more. A pure melt
  limit shows all the way round at the same height. Either way, use the **lowest** onset you find.
- Set `filament_max_volumetric_speed` 10 to 20% below the flow of that band. Example: roughness
  from 25 mm with the default ramp is the 11 mm³/s band, so set about 10.
- The limit is per filament and per hotend. Re-run it for a new filament type or a new hotend.

## Step 3 in practice: pressure advance

- Use a test that **changes speed**, such as OrcaSlicer's PA pattern or line test. A single-wall
  vase tower at constant speed is a weak test: in real testing a tower ramped from K 0 to 0.08 at
  100 mm/s and 1000 mm/s² came out with identical corners from bottom to top.
- **No visible difference is a valid result.** Printers with gentle acceleration (around
  500-1000 mm/s²) build little pressure to correct. Leave pressure advance off rather than
  guessing a value, especially on Marlin where linear advance can clash with stealthChop.
- In a vase-mode test, one corner may look serrated all the way up. That is where each spiral
  loop starts, not a pressure advance effect.

## Notes that trip people up

- **Pressure advance on Marlin printers** only works if the firmware was built with
  `LIN_ADVANCE`. Send `M900` and check `M503` for a K value. If it is missing, skip step 3. On
  Marlin, linear advance can also conflict with stealthChop on the extruder driver.
- **Two flow multipliers.** OrcaSlicer has `filament_flow_ratio` (per filament) and
  `print_flow_ratio` (per process). They multiply. Tune one and leave the other at 1.
- **Don't calibrate flow with calipers on a single-wall cube.** Layer wobble makes walls measure
  thick. Judge by top surfaces.
- **Repeat steps 1 to 5 for each new filament type or brand**, not for a re-buy of the same spool.
- **Dry the filament before step 1** for anything that absorbs moisture (PETG, TPU, nylon, and
  PLA that pops or strings). Wet filament makes every later test misleading.
- **Change one setting at a time.** Changing several at once hides which one helped.
- For PETG-specific values and problems, see `references/petg.md` in the `print-quality-settings`
  skill.
- Step 0 and step 6 are per printer; redo step 0 after any nozzle or bed change.

Sources: https://github.com/OrcaSlicer/OrcaSlicer/wiki/calibration_guide,
https://ellis3dp.com/Print-Tuning-Guide/, https://teachingtechyt.github.io/calibration.html

For appearance settings (seams, brims, walls, layer height), use the `print-quality-settings`
skill.
