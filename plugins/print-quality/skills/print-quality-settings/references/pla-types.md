# Starting points by PLA type

PLA comes in many blends, and the setting that changes most between them is **max volumetric
flow** (how many mm³ of plastic per second the hotend can melt for that filament). Temperatures
move much less. Use these as first guesses, then run a max-flow test and a temperature tower for
your own printer and brand (see the `print-calibration` skill). The vendor's datasheet wins
over this table.

| Type | Nozzle °C | Max flow, mm³/s | Hardened nozzle? | What to watch |
|---|---|---|---|---|
| Basic PLA | 205-220 | 8-12 | no | Most rough walls on fast prints come from going over the flow limit. |
| High-speed PLA | 210-230 | 12-18 | no | Only fast if the hotend can melt it; needs strong cooling. |
| Matte PLA | 205-220 | 5-8 | no | Low flow limit. Too hot turns it shiny; thinner layers hide lines well. |
| Silk PLA | 215-230 | 6-8 | no | Slow, steady outer walls keep the shine; too hot or too fast goes dull. |
| PLA+ / Tough PLA | 210-230 | 8-14 | no | A bit hotter and a bit less fan for stronger layers. |
| Marble / stone-fill PLA | 205-220 | 6-10 | recommended | Filler particles wear brass. |
| Wood-fill PLA | 190-210 | 4-8 | recommended | Clogs small nozzles; 0.6 mm nozzle helps. Too hot darkens and burns. |
| Carbon-fibre PLA (PLA-CF) | 210-240 | 6-10 | **yes** | Abrasive; wears a brass nozzle out quickly. |
| Glow-in-the-dark PLA | 200-220 | 6-10 | **yes** | Often forgotten: the glow powder is very abrasive. |
| Dual / multi-colour (coextruded) PLA | 210-230 | 6-10 | no | The colour you see depends on the face angle; orient the part on purpose. |

## Notes

- **Brass vs hardened.** A brass nozzle can be worn oversize by a single spool of abrasive
  filament: lines get wider, detail softens and flow calibration drifts. Hardened steel or
  ruby-tipped nozzles last; they conduct heat a little worse, so you may need +5 to 10 °C.
- **Setting the limit.** In OrcaSlicer the limit is `filament_max_volumetric_speed`. The slicer
  slows any move that would exceed it, so a correct value prevents under-extrusion on fast
  infill without slowing everything else.
- **Stock hotends.** Many stock hotends on budget bed-slingers top out around 10-15 mm³/s with
  plain PLA. A filament profile that allows more than the hotend can melt causes rough walls and
  gaps on fast moves; test before raising it.
- **Dry filament.** PLA absorbs some moisture; if a spool starts popping, stringing or snapping,
  dry it (around 45-50 °C for several hours) before blaming settings.
