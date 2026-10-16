# Agent #16 — M99-A06 status

Status: WIP.

Task: discharge the actual-map hypotheses behind residue/mod-22 absorption while explicitly separating exterior-only closure from full-interface closure.

Current finding:
- The existing Agent6 theorem ordinary_reverse_add_exterior already proves the exact one-step arithmetic projection under explicit digit, positivity, nonneutral-phase, coefficient, and paired-shape hypotheses.
- This branch packages that premise as ActualExteriorStep and adds a finite-walk composition theorem.
- The construction does not silently promote exterior dynamics to the full integer orbit: every step still requires the explicit interface premise.
- No P196 conclusion, infinite-safe-orbit claim, or universal interface theorem is asserted.

Verification:
- WIP / source inspection only. No local Lean runtime is exposed in this session, so no compile or axiom audit is claimed.
- The source is intended to be compiled against the pinned Lean 4.19.0 environment before acceptance.
