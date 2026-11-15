# Supports: settings that make them easy to remove

Setting names are OrcaSlicer's. Start here, then adjust one value at a time.

## Starting values (PLA, 0.2 mm layers)

| What | OrcaSlicer setting | Start with | Why |
|---|---|---|---|
| Type | `support_type`, `support_style` | Tree for figures and organic shapes; normal for flat undersides and functional parts | Trees touch less and come off cleaner; normal supports give a flatter underside |
| Top gap | `support_top_z_distance` | 0.2 mm (one layer) | Smaller welds PLA to the support; larger leaves a droopy underside |
| Bottom gap | `support_bottom_z_distance` | 0.2 mm | Same idea where supports stand on the part |
| Interface layers | `support_interface_top_layers` | 2-3 | A denser roof under the part gives a smoother underside |
| Interface spacing | `support_interface_spacing` | 0.2-0.5 mm | Tighter = smoother underside, harder removal |
| Base density | `support_base_pattern_spacing` | about 2.5 mm | OrcaSlicer sets density by line spacing, not a percentage: a larger gap means less support |
| Gap to walls | `support_object_xy_distance` | 0.35 mm | Keeps supports from fusing to vertical walls |
| Speed | `support_speed`, `support_interface_speed` | 60 / 30 mm/s | The interface is what you see; print it slowly |
| Where | `support_on_build_plate_only` | on for most parts | Avoids supports standing on the part's own surfaces and scarring them |

## Overhang threshold: watch which way the angle is measured

Most hobby printers handle overhangs up to about 45° from vertical without support, and many
manage 50-60° with good cooling.

In OrcaSlicer, `support_threshold_angle` is measured **from the horizontal**: supports are added
under surfaces flatter than that angle. The default 30 means "support anything within 30° of flat".
That is the same as about 60° from vertical. Tutorials often quote the angle from vertical, so check
which convention a guide uses before copying a number. Raising the threshold adds more supports.

## Tips

- Orient the part first. A different orientation often removes the need for supports altogether.
- Use support blockers or painted supports to keep supports off visible faces.
- With PETG, raise the top gap a little (0.25-0.3 mm) or use a PLA interface: PETG welds to its
  own supports.
- Remove supports once the part has cooled. Pliers and a flush cutter beat fingers.
