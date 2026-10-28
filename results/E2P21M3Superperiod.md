# E2P21M3Superperiod

**COMPUTED.** Complete exact finite row-map census of **spatial period 3**, base 10, overflow word `g=001001010101001010101` (period 21), allowing **any multiple of 21 as the lattice temporal period**.

All `19^3=6,859` coefficient rows were enumerated (no state cap). The 21-step row-return map is defined on 6,858, and its functional graph has 52 cycles with lengths in overflow blocks `{1:2, 2:37, 5:6, 6:4, 8:3}`.

Exactly **18** recurrent cycles have primitive spatial period 3 and a compatible moving reflection axis: **15** have minimal temporal period 42, **3** have minimal temporal period 168. They give 54 axis/phase-labelled starts, or **6 families** modulo spatial rotation and temporal phase.

In particular, **no primitive reflective m=3 lattice closes after only one 21-step block**, but a one-block-only census misses all 18 longer cycles. Representative row starts of six families: `(2,6,6)`, `(4,4,8)`, `(8,8,10)`, `(8,9,9)`, `(8,12,12)`, `(0,9,9)`.

The anchored carry algorithm was checked against independently constructed cyclic-carry fixed points for **13,718** row/overflow cases; all 54 reflected starts were replayed for their exact 42/168-step temporal cycles. Prior to this census the base-9 `g=1100011000` control returned m=4, depth 61 and the base-13 `g=1010010000` control returned depths 55/75 using the exact position automaton.

**Scope limitation:** these are *bulk row-map cycles*, NOT reachable exterior `B`-cycles, not genuine integer reverse-and-add certificates, and not a Lychrel result. Root reachability and spatial period 9 remain **UNDECIDED**. No big-integer replay of a seed is claimed.

Reproduce: `python3 calculation/decimal_frontier/lattice_formats/code/census_p21_m3_superperiod.py`.
