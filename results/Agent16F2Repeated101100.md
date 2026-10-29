# Agent16F2Repeated101100

**PAPER PROOF.** For every integer `k>=1`, every integer base `b>=2`, and
all six cyclic phases of the overflow word `g=(101100)^k`, a temporally
closed *canonical-root first-spatial-column* history exists **iff**
`b∈{4,5,6}`; in each of these three bases there are **exactly `4^k`**
distinct admissible carry histories. Every coefficient word repeats the
same six-step block. No higher temporal multiplier yields a new base class.

**COMPUTED** controls: an independent weighted six-step transfer graph
checks all rotations, bases 2..100, `k=1..8`; a separate constructive
checker replays cases through `k=1000` and all rotations.
Proof and reproducibility: `reports/Agent16F2Repeated101100.md` and
`calculation/decimal_frontier/lattice_formats/code/agent16_repeat_run.sh`.
This is not a full spatial SCC, a base-10 Lychrel certificate, or 196.
