# Y41 primitive-family survey

**Status: PARTIAL (3/5 families have a nontrivial exact phase/charge screen; no broad family is FOUND).**

- p8/m20: same-phase band return requires at least 5 clock laps (40 steps).
- p12/m9: same-phase band return requires at least 3 clock laps (36 steps).
- p16/m4: the phase gate is immediate, but the existing U32 charge excludes the selected 48- and 96-step three-cycle cases; 144 steps is the first multiple not excluded by that charge. Longer cases remain open.
- p20: the existing census exhausts only its neutral-band candidates; the broader W-band family remains undecided.
- p24: broader family remains undecided; the exterior census has capped candidates.
- p31/G10: not surveyed here; owned by agent-407.

Reproduce the arithmetic with python3 phase_gate.py. It does not simulate decimal orbits and makes no seam-return claim.

**Missing all-time lemma:** a complete physical epoch-map recurrence/emptiness result for an unowned rooted family, including carries, overflow, canonical realization, and a phasewise non-palindrome guard. No finite-horizon survival claim is made.
