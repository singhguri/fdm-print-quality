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

## Notes that trip people up

- **Pressure advance on Marlin printers** only works if the firmware was built with
  `LIN_ADVANCE`. Send `M900` and check `M503` for a K value. If it is missing, skip step 3. On
  Marlin, linear advance can also conflict with stealthChop on the extruder driver.
- **Two flow multipliers.** OrcaSlicer has `filament_flow_ratio` (per filament) and
  `print_flow_ratio` (per process). They multiply. Tune one and leave the other at 1.
- **Don't calibrate flow with calipers on a single-wall cube.** Layer wobble makes walls measure
  thick. Judge by top surfaces.
- **Repeat steps 1 to 5 for each new filament type or brand**, not for a re-buy of the same spool.
- Step 0 and step 6 are per printer; redo step 0 after any nozzle or bed change.

Sources: https://github.com/OrcaSlicer/OrcaSlicer/wiki/calibration_guide,
https://ellis3dp.com/Print-Tuning-Guide/, https://teachingtechyt.github.io/calibration.html

For appearance settings (seams, brims, walls, layer height), use the `print-quality-settings`
skill.
