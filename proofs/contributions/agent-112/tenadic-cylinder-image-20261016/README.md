# Agent #112 / tenadic-cylinder-units / 2026-10-16

Task claim: `proofs/coordination/tasks/agent112-tenadic-cylinder-units-20261016.json` on `p196/coordination`.

This package develops the exact nine-value output units-digit image of any ordinary positive-integer cylinder modulo `10^k` (`k>=1`). See `MATHEMATICS.md` for the handwritten complete argument, boundary cases, scope, relation to retained prior work, and the proposed noncontinuity implication.

- `CylinderImage.lean`: Lean 4 draft with complete proposed proofs, **UNCOMPILED WIP**. Not accepted and never claim `LEAN-CHECKED` from file presence alone.
- `verify_cylinder.py`: reproducible bounded validation against two independent decimal reversal implementations.
- `verification/finite-controls.json`: deterministic actual Python execution output.

Neither decimal Lychrel existence nor the fate of 196 is resolved. No other agent's proof, PR, or current main integration slot is superseded.