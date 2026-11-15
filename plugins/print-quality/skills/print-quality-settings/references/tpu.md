# TPU (flexible filament): starting points

TPU makes soft, rubbery parts: grips, phone cases, feet, gaskets, straps, toys. It needs slow,
gentle feeding and dry filament.

## Pick a hardness

Shore A hardness: lower is softer.

| Hardness | Feel | Prints |
|---|---|---|
| 85A | very soft | hardest to print; direct drive and very slow only |
| 90A | soft | grips, straps |
| 95A | medium | **the usual first TPU**; prints on most direct-drive printers |
| 98A | firm | functional parts, easier to print |
| "high-speed" TPU | usually 95A | formulated to tolerate faster feeding |

**Bowden printers** (long tube to the hotend) struggle with anything softer than 95A; the filament
buckles in the tube. Direct-drive printers handle TPU far better.

## Starting settings

| Setting | Start |
|---|---|
| Nozzle | 210-240 °C (try 220 °C first) |
| Bed | 40-60 °C |
| Print speed | 15-40 mm/s; start at 15-30 and work up |
| Max volumetric flow | 2-6 mm³/s (start low) |
| Retraction (direct drive) | 0.5-1.0 mm at 10-25 mm/s, or off |
| Part fan | 20-50 % (more for bridges and overhangs) |
| Layer height | 0.12-0.28 mm (0.2 is a good default) |
| Flow | 95-105 %, adjust for surface |

## Five common mistakes

1. **Printing too fast:** under-extrusion, weak layers and jams. Slow down first.
2. **Too much retraction:** pulling soft filament back and forth tangles and jams it in the
   extruder. Keep it short and slow, or turn it off.
3. **Wet filament:** TPU soaks up moisture quickly and then strings, bubbles and prints weak.
   Dry at 50-60 °C for 6-8 hours, store sealed with desiccant, and dry again after it sits out.
4. **Too much cooling:** weak layer bonds. Use moderate fan, not 100 %.
5. **Poor or too-strong adhesion:** textured PEI or glue stick works. On smooth PEI, TPU can bond so
   hard it tears the surface, so use glue stick as a release.

## Other notes

- **Multi-spool feeders** (AMS-style automatic material systems) often jam on soft TPU. Use only
  grades the manufacturer lists as compatible, usually 95A/98A or high-speed TPU, and test with one
  spool first.
- Let the spool turn freely; TPU should not have to drag a stiff spool holder.
- Infill percentage controls squishiness: low infill with few walls gives soft parts, high infill
  gives firm ones.
