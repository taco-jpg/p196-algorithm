# X20 running notes

## Coordination / route selection

- Read `AGENTS.md`, `OPEN_PROBLEMS.md`, `docs/FOCUS_SWARM.md`, `reports/audit_2026-10-28/AUDIT_N.md`, `AUDIT_Nseries.md`, `AUDIT_X11-X20.md`, `calculation/decimal_frontier/lattice_formats/FORMATS.md`, the rooted p12/m9 data, the R30 wrapper/implementation, and current #475 coordination. Issue #474 is full; new coordination belongs on #475.
- The initially assigned phase-0 U3 `|J|=3-4`, `C=2..13` cell is already claimed by W09/V01 and X12. The proposed U3 high-centre extension `U=(9,0,18)`, even `C=14..24`, is subsumed by the T12/V39 centre-independence result and W21's fixed-U scan. Posted a `BREAK` explaining the reduction; did not issue `RELEASE`.
- Pivoted to the adjacent U6 route: `U=(3,3,9,15,15,9)`, `|J|=3-4`, 240-step macro. The distinct U6 lane is not covered by R30's U3-only CLI, so this work uses its own exact carry recurrence and independent integer/digit-array oracle.

## All-width 240-step U6 cut/insertion theorem

- Exact cyclic carry map: `T_x(c)=floor((x+c)/10)`; a coefficient `x != 9` resets the one-bit carry. The rooted clock is `gamma_t = [t mod 4 = 0]`, so 240 steps contain 60 overflows.
- Under the actual two-ended carry map, `U0` returns after 48 phases, is half-rotated at phase 120, and returns at phase 240. All 240 rows have coefficient sum 54 and no adjacent 9s.
- Exact U6 boundary-cone losses over 240 phases, by six spatial rotations, are `(299,240)`, `(300,240)`, `(300,239)`, `(299,240)`, `(300,240)`, `(300,239)`. Thus uniform maxima are 300 on the junction side and 240 on the centre side.
- Put the U6 insertion cut 330 coefficients into the band (after 55 U6 copies). For `k>=100`, the cut has at least 330−300=30 protected coefficients from the junction side and 600−330−240=30 from the centre side. A full six-column reset guard remains on both sides; the prefix through the cut is independent of every admissible centre `C` for all 240 phases.
- The rooted W9 row returns after 12 phases. The exact 240-step rooted-prefix loss is 181 (not `2*91`, because the shifted cut enters a different W9 phase in epoch two). For `q=24`, the root prefix starts at 250 and ends with 69 protected coefficients; the W insertion cut at 52 leaves 17 coefficients, more than one full W9 period plus a reset guard. For every `q>=24`, the same cut remains protected.
- Therefore, for each fixed `J,C`, the 240-step return predicate is invariant under `q -> q+1` and `k -> k+1`; `Return(q,k)` iff `Return(24,100)` for all independent `q>=24,k>=100`. Every phase retains an odd coefficient in the rooted B prefix, so any hypothetical return would also have a phasewise non-palindrome guard.

## Exact finite cell

- The finite decision uses `q=24`, `k=100`, and the prefix `B0 W0^24 J U0^55`, plus a six-coefficient U6 lookahead. At each of 240 phases, low carries are propagated forward from coefficient 0; high carries are propagated backward from the first non-9 in the lookahead. The lookahead reset makes every computed prefix coefficient exact; the tail is asserted to remain the corresponding U6 bulk row.
- Exhaustive junction domain: all `19^3 + 19^4 = 6,859 + 130,321 = 137,180` ordered J words, no modular or MDD pruning. The assertion-enabled scan checks the rooted overflow clock and odd-coefficient guard at every phase, then compares the complete computed prefix at phase 240 against `B0 W0^24 J U0^55`.
- Result: zero W9-prefix restorations and zero full-prefix returns; every J has first mismatch at indices 202..213, i.e. 37–48 coefficients before the W9 endpoint at index250. The histogram is recorded in `CELL_REPORT.md`.
- Independent controls in `u6_240.py`: full arbitrary-precision `n + reverse(n)` and a separate LSD digit-array oracle agree at all 240 phases for q=20,24,40,80,160 with scaled k; paired W/U6 insertions are independently checked at q=24,40,80,160 and both centre parities. All controls pass.
