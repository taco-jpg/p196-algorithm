# U32 target: base-10 p16 / spatial period 4

## Route adjustment

The initially registered broad route, a cross-base zero-drift-band census, overlaps U30's route. U32 narrowed to the adjacent unresolved subcase: the primitive reflection-symmetric spatial-period-4 three-cycles of the exact base-10 overflow clock `g=(01)^8` (the phase rotation of `(10)^8`).

## Exact statement under test

Let `Phi_g` be the exact cyclic coefficient-row map for base 10 on four-cell rows, with one 16-step epoch driven by `g=(01)^8`. Exhaust the `19^4` row space and determine whether any of the primitive reflection-symmetric 3-cycles of `Phi_g` (temporal period 48) can be attached to a finite canonical-root exterior in a fully 48-periodic template.

The target is the missing lemma: **no such 48-periodic rooted template exists for any of the 16 primitive reflection-symmetric three-cycles**. The exact one-lap fixed-point family is separate and already has an exhaustive reachability exclusion in `results/Agent11E2P16M4OneLap.md`.

## Scope guard

This does not prove the decimal Lychrel conjecture, does not exclude all band periods up to 40, and does not exclude every longer template period. The new mod-9 charge excludes the 48-step three-cycles for a 48-periodic template, and also full template periods `48*k` with `3` not dividing `k`. Periods divisible by 144 remain open under this charge. The fixed-row components in longer-period templates are also not excluded by the new charge (their 48-phase charge is 0).
