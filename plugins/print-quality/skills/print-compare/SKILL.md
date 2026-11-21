---
name: print-compare
description: Use when one FDM print came out noticeably better or worse than another (smoother walls, cleaner threads, fewer lines, blobs or rough spots) and the user asks why, what was different, or what to change, and the sliced G-code files of both prints are available. Also use when asked to explain a surface-finish difference between two profiles, plates or slicers.
---

# Compare two prints

Find out from the G-code, not from memory, why print A looks better than print B. The slicer's
settings block shows what was asked for; the toolpaths show what the printer actually did.
Most finish differences between two prints from the same printer and spool come down to how
the part is built (walls vs solid fill) and how often the nozzle stops and restarts, not to
speed or temperature.

## Steps

1. **Get the right files.** The G-code that was actually printed (from the printer, OctoPrint
   or the SD card), not a re-slice. If the model was sliced as one merged STL, note how many
   separate parts were on the plate.
2. **Run the comparison** with `scripts/compare_gcode.py` from this skill's folder (plain
   Python 3, no packages; use the full path to the script), best print first:

   ```
   python <skill folder>/scripts/compare_gcode.py good.gcode bad.gcode --parts 5 4 --stl good.stl bad.stl
   ```

   `--parts` and `--stl` are optional. It prints the settings that differ, key settings even
   when they match (pressure advance with its `M900` count, infill retraction, seam, speed,
   temperature, fan), the share of plastic per line type, retractions per part per layer, and
   extruded volume vs part volume. You should not need to grep the files yourself.
3. **Read it with the table below.** Name the one or two differences that explain the finish,
   each with the number that shows it.
4. **Propose one change at a time** and a small test print (one part, same plate position) to
   compare in hand against the old part. Several changes at once leave you unable to tell
   which one helped.
5. **Say what the files cannot show.** G-code proves what was printed, not how it looks.
   Cooling, wet filament, a worn nozzle or a dirty bed never appear in it.

## Reading the output

| Output | What it means | Usual fix |
|---|---|---|
| ALL WALLS high (60%+) on the good print, low (under 35%) on the bad one; "Internal solid infill" dominates the bad one | The good part is built from continuous concentric loops. The bad one is mostly short zig-zag solid fill pressing against thin walls; on parts with cut-outs it is chopped into many islands. | More walls (6-8 on small parts) with 30-50% gyroid instead of 100% infill, so small parts end up nearly all wall. |
| Retractions per part per layer much higher on the bad print | Every retract/unretract can leave a blob or zit and a string. Cut-outs and islands multiply them. | Fewer islands (more walls), `reduce_infill_retraction = 1` (OrcaSlicer: no retract on travel inside infill), then retraction tuning. |
| Extruded volume well over 100% of the part on a 100%-infill print | Over-extrusion: ridges, rough tops, nozzle dragging. | Flow calibration (see the `print-calibration` skill). |
| Extruded volume 90-100% on a 100%-infill print | Normal. Over-extrusion is ruled out. | Look elsewhere. |
| Extruded volume under 100% on a partial-infill print | Expected; the infill is hollow. The check only means something at 100% infill. | None. |
| Speed, temperature, fan, acceleration differ | Real candidates, but only if they differ. | Test them one at a time. |
| No settings differ | Same profile, so the difference is the model's shape, the plate position or the physical setup. | Compare part geometry (cut-outs, thin features, overhangs) and bed position. |
| A setting is `[same]` in both | It cannot explain a difference between these two prints, even if it is a common culprit (Arachne, seam type, pressure advance). | Don't propose it as the cause. |
| No STL given | The volume check is skipped, so over-extrusion is not ruled out. | Say so, or get the STLs. |

Parts of different heights are fine to compare: retractions are per part per layer and line
types are shares of each file's own plastic.

## Gotchas

- **Arc moves count.** OrcaSlicer and Bambu Studio turn curves (gyroid infill, round walls)
  into `G2`/`G3` arcs. A parser that reads only `G1` undercounts them; gyroid infill came out
  at half its real share in testing. The script reads G1, G2 and G3.
- **Check the enable flag, not only the value.** `pressure_advance = 0.02` does nothing when
  `enable_pressure_advance = 0`, and no `M900` then appears in the G-code. The script counts
  `M900` lines for you. A count of 0 only means the slicer didn't set it: firmware or the
  printer's start G-code can still apply a value (on Marlin, `M503` reports it). Either way it
  is the same for both prints from the same printer, so it can't explain a difference.
- **Raw retraction totals mislead.** A taller plate with more parts has more retractions in
  total. Compare per part per layer.
- **Merged plates count as one object.** If several bodies were merged into one STL, the
  object labels show 1 part. Pass `--parts`.
- **Wipe moves extract as retractions.** OrcaSlicer's wipe retracts while moving. That is
  fine for comparing two prints from the same slicer, but don't compare retraction counts
  across slicers.
- **The settings block shows the whole-plate profile.** Per-object overrides set in a 3MF
  project don't show there separately. If the good print came from a designer's project file,
  read its `Metadata/model_settings.config` (per-object `wall_loops`, infill and shell overrides) to see what each part really got.
