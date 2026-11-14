---
name: print-quality-settings
description: Slicer settings that make FDM 3D prints look better and fit better - brim ears instead of full brims, scarf seams, Arachne walls for small text, variable layer height, colour order on multi-colour prints, plus a vetted list of further tips and common myths. Use when the user asks how to improve print quality, wants their slicer profile reviewed or tuned, asks about seams, brims, layer lines, small text, stringing or surface finish, or wants these settings applied to OrcaSlicer presets.
---

# Print quality settings

Five settings changes that most hobby profiles get wrong, how to apply them, and how to check
they actually took effect. Setting names are OrcaSlicer's (tested on 2.4). PrusaSlicer and Cura
names are listed where they exist.

## The five core rules

| # | Don't | Do | OrcaSlicer setting | PrusaSlicer / Cura |
|---|---|---|---|---|
| 1 | Use a full outer brim by default. It leaves a rough edge all the way round. | Use **brim ears** (mouse ears). Small brim pads only at sharp corners, where parts lift. | `brim_type = brim_ears`, `brim_ears_max_angle = 125` (corners sharper than this get an ear), `brim_width` sets ear size | Prusa / Cura: no ears option that we could verify. Paint a brim on the corners or add small disc modifiers. |
| 2 | Let the Z seam leave a zipper of blobs on round parts. | Use a **scarf seam**: the outer wall ramps up and overlaps itself so there is no start/stop blob. | `seam_slope_type = external`, `seam_slope_conditional = 1`, `seam_slope_min_length = 20` | Prusa: Scarf seam in recent versions. Cura: none (place the seam instead). |
| 3 | Let a dark colour bleed into a light one on first layers. | On multi-colour prints, **start with the lighter colour**. When a light colour is printed on top of a dark one, give it enough layers to cover the dark. | (print order / colour change placement) | same |
| 4 | Use Classic walls for small text and fine detail. Thin strokes come out as gaps. | Use **Arachne**: it varies line width to fill thin features. | `wall_generator = arachne` | Prusa: Perimeter generator Arachne. Cura: on by default since 5.0. |
| 5 | Leave the same layer height on curved tops, so layer lines show as steps. | Use **variable layer height**: thin layers on curves, thick on vertical walls. | GUI only (see below) | Prusa: Variable layer height tool. Cura: Adaptive Layers. |

### Gotchas found while testing

- **Scarf length 0 does nothing.** Some vendor profiles ship with `seam_slope_type` set but
  `seam_slope_min_length = 0`. The header says scarf is on and the G-code has no scarf at all.
  Set the length to about 20 mm.
- **Conditional scarf** (`seam_slope_conditional = 1`) only applies where the seam cannot hide in
  a sharp corner. On a box the seam goes in a corner as usual; on round parts it scarfs. That is
  usually what you want.
- **Variable layer height cannot be set from the OrcaSlicer command line.** There is no setting
  for it, and in testing a layer-height profile or height-range modifiers written into a 3MF
  were ignored by command-line slicing. Do it in the GUI:
  1. Select the object, click the **Variable layer height** button in the top toolbar.
  2. Click **Adaptive** (lower the quality slider for thinner layers), then **Smooth**.
  3. Slice. The profile is saved with the object in the project 3MF.
  It adds print time. Use it on curved, domed or organic tops, not on boxy parts.
- **Brim ears and large flat parts.** Ears go only on corners. Large flat parts with good bed
  adhesion need neither ears nor a brim; switch the brim off for them.

## Applying the settings to OrcaSlicer presets

`scripts/apply_orca_quality.py` in this skill's folder patches process presets (JSON). It needs
only Python 3, no packages.

```
python scripts/apply_orca_quality.py "<preset>.json" --dry-run    # show what would change
python scripts/apply_orca_quality.py "<preset>.json"              # apply (writes a .bak first)
python scripts/apply_orca_quality.py "<preset>.json" --brim keep  # leave brim settings alone
python scripts/apply_orca_quality.py "<preset>.json" --extras     # also the safe extras below
```

- Run it on **user presets**, not system presets. System presets get overwritten on update. In
  OrcaSlicer, save a copy of the process preset first (it then appears under "User presets").
- User preset folders (close OrcaSlicer first, it rewrites presets on exit):
  - Windows: `%APPDATA%\OrcaSlicer\user\<id>\process\`
  - macOS: `~/Library/Application Support/OrcaSlicer/user/<id>/process/`
  - Linux: `~/.config/OrcaSlicer/user/<id>/process/`
- Presets with `brim_type = no_brim` keep their brim off.
- It skips files that are not process presets (printer and filament presets).
- `--extras` adds: monotonic top surface, 1 mm top shell, 0.15 mm elephant-foot compensation,
  avoid crossing walls, precise outer wall. These need no calibration. Ask the user before using
  it; elephant-foot compensation slightly shrinks the first layer, which matters for parts that
  were already sized to fit.

Bambu Studio and other Orca forks use many of the same keys but are untested. Check the keys
exist in the preset (or in a sliced G-code's config block) before patching.

## Verify it worked

Slice a part and read the settings block at the end of the G-code:

```
grep -E "^; (wall_generator|seam_slope_type|seam_slope_min_length|brim_type) =" part.gcode
```

The header only shows what was requested. To confirm the toolpaths changed:
- Scarf seam: outer-wall moves (`;TYPE:Outer wall`) should include `G1` lines that change Z while
  extruding. With the scarf off there are none.
- Brim ears: the first layer's `;TYPE:Brim` moves should be short pads at corners, not a full loop.

## Going further

`references/tips.md` has about 20 more vetted tips (calibration order, first layer, walls and
seams, top surfaces and ironing, overhangs, supports, strength, travel, fuzzy skin) with setting
names, when not to use each, and sources, plus common advice that is wrong or only true in some
cases. Read it when the user wants more than the five rules or asks about a specific problem.
For calibration steps, use the `print-calibration` skill.
