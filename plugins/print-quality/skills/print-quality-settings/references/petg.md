# PETG: starting points and troubleshooting

PETG is tougher and more heat- and water-resistant than PLA, and good for functional parts
(brackets, clips, outdoor parts, springs). It strings more, is sticky when molten, and wants
different settings. Treat everything below as starting points; brands vary. Change one setting
at a time so you can tell what helped.

## Starting points

| Setting | PETG start | Compared with PLA |
|---|---|---|
| Nozzle | 230-250 °C | 20-30 °C hotter |
| Bed | 70-85 °C | hotter |
| Part cooling fan | 0-30 % for strength, up to 40-50 % for overhangs and bridges | much less |
| Max volumetric flow | 8-12 mm³/s on typical hotends (run the max-flow test) | similar or a bit lower |
| Retraction (direct drive) | 0.8-1.2 mm, 30-45 mm/s | a little longer |
| Travel speed | high (around 200 mm/s if the printer allows) | same idea |
| First layer | 20-30 mm/s, 0.20-0.24 mm high, **less squish than PLA** | slower, higher |
| Top layers | 4-6 (about 0.8-1.2 mm) | similar |
| Drying | 65 °C for 4-6 h | PLA: 45-55 °C |

## Problems and fixes

**Stringing.** The most common PETG complaint. In order: dry the filament (wet PETG strings
badly whatever the settings), lower the nozzle 5 °C at a time, raise travel speed, then tune
retraction in small steps (0.8, 1.0, 1.2 mm). Turning on avoid-crossing-walls / combing helps.
A few wisps that pull off are normal for PETG.

**Blobs and zits.** Usually flow too high, pressure advance not tuned, or the seam in a visible
place. Calibrate flow (0.95-1.00 is typical), tune pressure advance if your firmware supports it,
put the seam at the back or use a scarf seam, slow the outer wall to 40-60 mm/s, and avoid
running much above 245 °C.

**First layer not sticking.** Clean the plate (isopropyl alcohol or dish soap and water), bed at
75-85 °C, first layer slower, and set the nozzle **slightly higher than for PLA**: PETG dislikes
being squashed. Too much squish gives poor adhesion *and* drags plastic onto the nozzle.

**Sticking too well.** The opposite problem: on smooth PEI or glass, PETG can bond so hard it
pulls chunks out of the surface. Textured PEI is the safe choice; on smooth surfaces use a thin
layer of glue stick as a release. Let the bed cool before removing parts.

**Weak layers / parts split along layers.** Hotter nozzle (240-250 °C), less fan (0-30 %),
slower printing (40-80 mm/s), dry filament, and correct flow. Thicker layers (0.2-0.28 mm) and
orienting the part so the load runs along the layers make the biggest difference.

**Plastic building up on the nozzle.** Usually the first layer is squished too much or the
nozzle is too hot or over-extruding. Raise the Z offset slightly, check flow and temperature, dry
the filament, and clean the nozzle while hot (soft brass brush, carefully). A silicone sock on
the heater block helps a lot.

**Warping and lifting corners.** Less than ABS but it happens on large flat parts. Bed 75-85 °C,
low fan, brim ears or a 3-8 mm brim on sharp corners, no drafts, and an enclosure for big parts.

**Rough or dull top surface.** 4-6 top layers, top layer at 20-40 mm/s, calibrated flow, moderate
fan (20-40 %) on the top layers, and ironing (about 10-15 % flow, 20-30 mm/s) for flat tops.

## Calibration order for a new PETG

Same order as the `print-calibration` skill, with drying first:

1. Dry the spool (65 °C, 4-6 h).
2. Temperature tower (roughly 230-250 °C).
3. Max volumetric flow.
4. Flow ratio.
5. Retraction, and pressure advance if supported.
6. Cooling and top layers.

Save the result as its own filament profile.

## Material notes

- PETG is a good choice for parts under constant load (clips, springs, brackets): it creeps less
  than PLA and cracks less at flex points.
- It is food-contact-friendly as a plastic, but printed parts have layer gaps that trap bacteria,
  and brass nozzles can contain lead. Do not treat a printed part as food-safe.
