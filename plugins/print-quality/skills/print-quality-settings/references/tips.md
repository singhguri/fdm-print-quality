# More print-quality tips

Vetted against the OrcaSlicer wiki, Prusa Knowledge Base, Ellis' Print Tuning Guide, CNC Kitchen
and Teaching Tech. Setting names are OrcaSlicer 2.4 keys. Short link prefixes:

- `OW/` = https://github.com/OrcaSlicer/OrcaSlicer/wiki/
- `EL/` = https://ellis3dp.com/Print-Tuning-Guide/articles/

## First layer

**Set Z offset by looking at first-layer squish.** Paper is only a starting point. The squish
decides both adhesion and how the bottom looks. Settings: `initial_layer_print_height = 0.2`,
`initial_layer_line_width` about 0.5, `initial_layer_speed` 30 mm/s or lower.
Prusa: First layer height / width / speed. Cura: Initial Layer settings.
Source: EL/first_layer_squish.html

**Clean the plate with dish soap and warm water, not just alcohol.** Skin oil is the most common
cause of a first layer that suddenly stops sticking. Rinse well and avoid touching the surface.

**Make the first layer slightly wider and slower.** A first-layer line width around 120-125 % of
the nozzle (0.5 mm on a 0.4 mm nozzle) at 20-30 mm/s presses more plastic into the bed.
`initial_layer_line_width = 0.5`, `initial_layer_speed = 30`.

**Use elephant-foot compensation of 0.1 to 0.2 mm on parts that must fit.** It shrinks the first
layer to cancel the squish. Too much and small parts or brims let go. It does not fix a wrong Z
offset. `elefant_foot_compensation = 0.15`, `elefant_foot_compensation_layers = 1`.
Prusa: `elefant_foot_compensation`. Cura: Initial Layer Horizontal Expansion (negative).
Source: OW/quality_settings_precision, help.prusa3d.com/article/elephant-foot-compensation_114487

## Walls and seams

**Use inner-outer-inner wall order (3 or more walls) for looks and accuracy.** The outer wall is
printed between two inner walls, so it is not pushed outward. Skip it on parts with steep
overhangs: the outer wall has nothing to lean on. `wall_sequence = inner-outer-inner wall`.
Prusa: External perimeters first. Cura: Wall Ordering.
Source: OW/quality_settings_wall_and_surfaces

**Turn on precise outer wall.** Removes the overlap between outer and inner wall for better size
accuracy. `precise_outer_wall = 1`. No Prusa or Cura equivalent.
Source: OW/quality_settings_precision

**Put the seam where nobody looks.** Aligned, back, or painted. Random spreads blobs over the
whole surface. `seam_position = aligned` or `back`, `seam_gap`, `wipe_on_loops = 1`.
Prusa: Seam position Aligned / Rear. Cura: Z Seam Alignment.
Source: OW/quality_settings_seam

## Top surfaces

**Use monotonic top surfaces and about 1 mm of top shell.** Monotonic lines all go down in one
direction, so the sheen is even. A thick shell stops pillowing over sparse infill.
`top_surface_pattern = monotonicline`, `top_shell_thickness = 1`.
Prusa: Top fill pattern Monotonic. Cura: Monotonic Top/Bottom Order, Top Thickness.
Source: OW/quality_settings_wall_and_surfaces

**Iron flat tops that face up.** A second low-flow pass smooths the top. Not for curved or
organic tops; it slows the print. `ironing_type = top`, `ironing_flow = 10%`,
`ironing_spacing = 0.15`. Prusa: Ironing. Cura: Enable Ironing.
Source: OW/quality_settings_ironing, help.prusa3d.com/article/ironing_177488

**Use one wall on top surfaces for small embossed detail.** Leaves room for the top pattern.
`only_one_wall_top = 1`.
Source: OW/quality_settings_wall_and_surfaces

## Overhangs, bridges, cooling, supports

**PLA: full part fan after the first layer, minimum layer time about 4 to 8 s.** Small layers
otherwise land on soft plastic. More cooling means weaker layer bonds, so turn it down for
strength parts. `fan_max_speed = 100`, `close_fan_the_first_x_layers = 1`,
`slow_down_layer_time = 4` to `8`, `overhang_fan_speed = 100`.
Prusa: Cooling, Slow down if layer print time is below. Cura: Minimum Layer Time.
Source: EL/cooling_and_layer_times.html

**Slow overhangs and bridges, bridge flow at or below 1.** Slower, thinner strands sag less.
`enable_overhang_speed = 1`, `bridge_speed`, `bridge_flow`, `thick_bridges`.
Prusa: Dynamic overhang speed, Bridge flow ratio. Cura: Bridge Settings.
Source: OW/quality_settings_bridging, OW/quality_settings_overhangs

**Use "make overhang printable" on functional parts.** Reshapes steep undersides to about 55
degrees so they print without supports. It changes the shape, so not for cosmetic or
dimension-critical faces. `make_overhang_printable = 1`, `make_overhang_printable_angle = 55`.
Cura: Make Overhang Printable.
Source: OW/quality_settings_overhangs

**Use tree or organic supports with 2 to 3 interface layers and a top gap of one layer
height.** Fewer marks, easier removal. Below about 0.2 mm, PLA welds to the support.
`support_type = tree(auto)`, `support_style = organic`, `support_top_z_distance = 0.2`,
`support_interface_top_layers = 3`.
Prusa: Organic supports, Contact Z distance. Cura: Tree support, Support Z Distance.
Source: OW/support_settings_tree

## Strength

**Add walls before infill.** Walls carry most of the load. In CNC Kitchen's tests, wall count
and line width beat infill percentage. `wall_loops = 3` or `4`.
Source: cnckitchen.com/blog/how-designs-the-strongest-hook-polymaker-competition

**Orient so the load runs along the layers, not across them.** Layer bonds are the weakest
direction. Looks and strength can want different orientations; choose per part.
Source: as above

## Travel and cosmetics

**Avoid crossing walls; use Z-hop only if the nozzle catches.** Detours keep travel marks off
visible faces. Z-hop adds time and can add stringing. `reduce_crossing_wall = 1`,
`max_travel_detour_distance`, `z_hop`, `z_hop_types`, `retract_lift_above`.
Prusa: Avoid crossing perimeters, Lift Z. Cura: Combing, Z Hop When Retracted.
Source: OW/quality_settings_wall_and_surfaces

**Fuzzy skin hides layer lines and seams on cosmetic parts.** Gives a matte, textured outer
wall. Not for mating or gripping faces. `fuzzy_skin = external`, `fuzzy_skin_thickness = 0.3`,
`fuzzy_skin_point_distance = 0.8`. Orca 2.4 gotcha: `fuzzy_skin = none` means "painted only";
fully off is `disabled_fuzzy`.
Prusa / Cura: Fuzzy skin.
Source: OW/others_settings_fuzzy_skin

## Common advice that is wrong or situational

- **"Gyroid is the strongest infill."** Situational. It is equally strong in all directions and
  never crosses itself, which is gentle on bed-slingers. Load-specific patterns can match or beat
  it. Source: OW/strength_settings_patterns
- **"Arc fitting improves quality."** It only changes how moves are written to the G-code.
  Source: OW/quality_settings_precision
- **"Always dry PLA."** Mostly a PETG, TPU and nylon problem. Dry PLA when it pops, strings badly
  or snaps.
- **"Calibrate flow with a single-wall cube and calipers."** Caliper readings include layer
  wobble and read high. Judge flow by top-surface smoothness instead. Source: EL/misconceptions.html
