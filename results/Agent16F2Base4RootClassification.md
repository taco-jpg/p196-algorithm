# Agent16F2Base4RootClassification

**PAPER PROOF.** For the canonical root of the `bauto3` position automaton,
fixed overflow word `g=101100` (or any of its six cyclic rotations),
a time-closed first-spatial-column transition exists **iff** the integer base
is `b=4,5,6`; in each such base exactly four carry assignments work.

The corresponding coefficient trajectories for `g=101100` are respectively
`(4,1,3,4,1,2)`, `(6,2,4,5,1,3)`, `(7,2,5,6,1,3)`.
This is a necessary first-column filter, not a full reachable SCC criterion,
not a complete band certificate, and not a result for other overflow words,
other formats, base 10 Lychrel existence, or 196.

Proof: `reports/Agent16F2Base4RootClassification.md`.
Reproduce independent checks: `python3 calculation/decimal_frontier/lattice_formats/code/agent16_base4_f1.py`.
