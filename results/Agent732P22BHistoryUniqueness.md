# Agent732P22BHistoryUniqueness

**COMPUTED (exact exhaustive, uncapped).** The base-10 neutral-band position automaton with period-22 overflow word `g=0000111000100001110001 = (00001110001)^2` has exactly zero accepting B-position histories at widths `d<29`, and exactly one at every width `d>=29`.
The sole accepted lower-carry stream is `e=0011101001100111010011 = (00111010011)^2`: the already-known period-11 exterior repeated, **not** a new primitive period-22 B-cycle.
Proof by exact multiplicity-weighted cut-state dynamic programming: the entire 257-state weighted vector is identical at widths 88 and 89, so all subsequent vectors (and accepted counts) coincide.
The largest frontier has 651,921 states (width 37); no state, depth, candidate, or integer-multiplicity cap was reached. All state keys are exact 128-bit words with checked 64-bit history multiplicities.
An independently written Python tuple-state enumerator and the C++ counter agree on all 29,760 states and weights at width 3; p11 and p12 known exterior controls pass.
Separate independent digit-vector and big-integer positive controls check 201 complete pairwords for each of the established base-9 `g=1100011000` (`|B|=61, m=4`) and base-13 `g=1010010000` (`|B|=75`) lattice certificates.
Reproduce: `bash calculation/decimal_frontier/exterior_census/Agent732P22Reproduce.sh`.
Code: `calculation/decimal_frontier/exterior_census/src/Agent732P22History.cpp`, `calculation/decimal_frontier/exterior_census/py/Agent732P22Oracle.py`, `calculation/decimal_frontier/exterior_census/py/Agent732P22PositiveControls.py`.
Full recurrence, proof of completeness, exact scope and limitations: `reports/Agent732P22BHistoryUniqueness.md`.
No assertion about decimal absorbing lattices, periodic centres, nonpalindromic infinite trajectories, 196, or a decimal Lychrel certificate.
