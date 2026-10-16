# Checked sharp obstruction to four seven-step returns

Integration parent: `8a42fe14262fee12ce1c8b40bf25e97b94044742`, branch
`main`. This checkpoint's containing commit publishes the complete
reviewed sources and certificates announced by the preceding
[obstruction checkpoint](2026-10-14-seven-step-obstruction.md).
All previous contributions and concurrent seam-safety work are preserved.

**Every admissible canonical symmetric pair word of finite width at least
six with prefix (4,4,0) has at most three consecutive seven-step returns
to that prefix.** Returns at all four times 7,14,21,28 are impossible,
without any palindrome-safety hypothesis. The stronger clock bound is
also sharp: at most 26 consecutive transitions of its forced seven-phase
prefix/overflow schedule can occur from phase zero.

The actual starting word `(4,4,0) W (0,4,4)` with
`W=(1,1,14,16,14,1,1)` makes three safe returns and follows the phase
clock for 26 transitions, first deviating at transition 27. The independent
audit retains all actual states through time 28 and their safety checks.
Losing the clock does not imply a palindrome; this example remains safe
through all 28 positive successors.

The [complete proof](../contributions/2026-10-14-seven-step-extension/SEVEN_STEP_BOUND.md)
projects every actual transition to a graph with 48,013 phase vertices,
61,731 edges and both possible deeper carry inputs. Its strictly
decreasing sink rank has maxima `(26,25,24,26,25,28,27)` by phase. Four
returns require 28 edges from phase zero, contradicting its maximum 26.
The local projection works even when observed low and high columns
overlap, including whole width six; it never assumes arbitrary graph
paths are globally realizable.

## What has been independently checked

- All 96,026 labeled controls were reconstructed by literal ordinary
  integer normalization without importing the producer. Every accepted
  edge, rejected control and all 48,013 rank values agree. The full graph,
  rank certificate and complete independent control outcomes are retained
  as lossless gzip artifacts, with documented byte schemas.
- The exploratory macro graph and correlated spatial lifts are also
  preserved. Separate audits retain 1,064 macro controls and 1,078 lift
  controls, full graph comparisons, and the earlier six-column acyclicity
  argument. The direct graph proves the stronger sharp finite bound.
- Eight fresh Lean theorems establish the actual all-length prefix
  extension formula, exhaustive carry alternatives, coefficient bounds,
  iterative necessity and ordinary-integer interpretation. Their condition
  is `1 <= k < L`; no disjointness condition is needed.

The current theorem is a written all-width proof using a complete
independently checked finite certificate and a formal local bridge.
The complete rank calculation has not yet been integrated into the Lean
kernel. That is a separate active contribution, not a claim of this
bundle. The [formal scope and audit](../contributions/2026-10-14-prefix-extension-formal/README.md)
and [root review](../contributions/2026-10-14-seven-step-bound-root-review.json)
state the exact division of proof obligations.

## Reproduction from repository root

```sh
python3 -B proofs/contributions/2026-10-14-seven-step-extension/independent_extension_audit.py
python3 -B proofs/contributions/2026-10-14-seven-step-extension/independent_lift_audit.py
python3 -B proofs/contributions/2026-10-14-seven-step-extension/independent_direct_audit.py
python3 proofs/contributions/2026-10-14-prefix-extension-formal/check.py /absolute/path/to/lean-4.19.0/bin/lean
python3 proofs/verify_release.py
```

Every completed producer, proof, compiler log, graph checkpoint, failed
branch, sharp witness and independent audit in this contribution is
retained. `INVENTORY.json` gives compressed and decoded identities and
recovery commands for all five new gzip artifacts.

## Consequence for the shared research

The preceding seven-step handoff posed preservation of this fixed clock
as an open route. The all-width obstruction now closes that route. The
concurrent generalized-seam/language work should consider different
clocks, variable return times, or different reset languages instead of
attempting an invariant class with this precise seven-step return forever.
This theorem supplies no all-time safe seed and neither proves nor
disproves the assertion for 196 or decimal Lychrel existence. Research
continues; the historical checkpoints remain unchanged.
