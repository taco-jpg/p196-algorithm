# EQUIV_R8 — reach graph vs the Agent120 exterior system

Goal: check that "reach reaches a 9-wire stream at height h" matches "the Agent120 B-system has a B-cycle with that overflow word g and carry stream e of width h".
Sources (read-only clone `~/p196_repo` on studio): `calculation/neutral_band_search.py` (exact Python mirror of the Lean `nextB`, `e2 = 1 - e1`, trimming of 9s),
`calculation/decimal_frontier/exterior_census/EXTERIOR.md` and `py/verify_ext.py` (the `Bstep` mirror with `e2 = 1 - e1`, mirror replay and real-integer replay), `py/brute_model.py`.
Everything below is a computed consistency check. **The equivalence itself is not proven**; no inconsistency was found.

## A. reach witness -> Agent120 mirror (every stream that reach finds, replayed)
Tool: `reach_w` (the single-thread `reach` with left-end reconstruction switched on for WIRE streams), then `equiv.py`: B_t[k] = value of cell k at time t, trailing 9s removed (neutral band),
then `verify_ext.verify`: (1) B_{t+1} = Bstep(B_t) for all t, e1 and gam equal the stream and the clock, B_p = B_0; (2) one genuine reverse-and-add step per t in integers (pair word of N_{t+1} starts with B_{t+1} and the shrunk neutral band).

| clock | T | stream reach reports | height = number of cells | rebuilt left end | mirror + integer replay |
|---|---|---|---|---|---|
| 00001110001 | 11 | 00111010011 | 29 | ok | **True** |
| 000100010001 | 12 | 010100101011 (a 4-step rotation of N12 101101010010) | 53 | ok | **True** |
| (00001110001)^2 | 22 | 0011101001100111010011 (p11 stream twice) | 29 | ok | **True** |
| (0001)^6 | 24 | 010100101011010100101011 (N12 stream twice, rotated) | 53 | ok | **True** |

B-lengths over t are 25..29 (p11, p22) and 51..53 (p12, T=24), i.e. the width is the height.

## B. Agent120 mirror -> reach (every periodic orbit of the B-map up to a width bound, compared with reach)
`brute_r8.py b L pmax`: all trimmed B lists with at most L coefficients (each coefficient 0..2b-2, B[0] != 0, B[-1] != b-1), the map Bstep, every periodic orbit inside the box; for each orbit (g, e) reach (WIRE, ALLFITS=1) is run with clock g.

| base | L | lists | periodic orbits | (g, e), widths | reach |
|---|---|---|---|---|---|
| 2 | 10 | 39,366 | 1 | p=2, g=10, e=10, widths 1..2 | stream 10 at height 2: AGREE |
| 3 | 8 | 312,500 | 1 | p=5, g=11100, e=01011, widths 4..7 | stream 01011 at height 7 (also 01010 at height 11, outside the box): AGREE |
| 4 | 6 | 100,842 | 2 | p=3, g=100, e=100 (widths 1..2) and e=010 (widths 5..6) | streams 100 at height 2 and 010 at height 6: AGREE |
| 10 | 5 | 2,345,778 | **0** | none | (nothing to compare; reach has no stream below height 29 for any clock with T <= 24) |
In every case the height at which reach first reports the stream equals the maximal width of the B-cycle (2, 7, 2, 6). Base 10 has no B-cycle of width <= 5 at all, so the
decimal exterior cannot be tested at small width; that is why section A (large width, replayed) and section D (the repository's exhaustive census) carry the decimal evidence.

## C. Count identities with the repository's engine `bx` (position automaton of the Agent120 B-system)
`bx` counts the start state (L,H,Y) = (0, g, 1); reach does not.
* p11 (g = 00001110001): bx 18,061 states, accepted at width 29, saturation depth 59. reach: 18,060 interfaces, stream at height 29, frontier empty after height 59. Equal up to the start state.
* p12 ((0001)^3, quotient by the 4-step shift): bx 45,571, accepted at width 53, saturation depth 71. reach ROT=1: 45,570 orbits, stream at height 53, empty after height 71. Equal up to the start state.
* p22 (p11 word twice): bx 13,191,834 quotient states, depth 88. reach (ROT=0) 26,365,606 interfaces for T=22. Burnside for the 11-step shift: orbits = (26,365,606 + 18,060)/2 = 13,191,833; the 18,060 fixed points are exactly the T=11 interfaces. 13,191,833 + 1 (start state) = 13,191,834. Equal.

## D. Repository census (EXTERIOR.md, section 4) vs reach/reachdisk
EXTERIOR: every F1-surviving overflow word of length p <= 32 was run; the only ACCEPTs are p11, p12 and p22 (the p11 word twice, only the repetition stream). reach finds exactly the same streams (p11 at 29, p12 at 53, p22 at 29), and no stream for any other clock with T <= 24 (round-5 sweep of 1,465,899 tasks) or for any of the round-6 tasks except the repetition e12e12 at T=24 clock (0001)^6.
EXTERIOR lists 54 words as UNDECIDED (capped at 12-40 million states). reach decides 51 of them:
* 50 COMPLETE with no 9-wire stream (T=16, 21 from round 5; T=27..32 from round 6; nine words of T=29/30 from the round-5 heavy runs, log files `r5_heavy_T29_*`, `r5_heavy_T30_*`);
* 1 COMPLETE with only the repetition stream: p24 (0001)^6 (EXTERIOR: capped at 40M states, depth 47; reach: 6,625,354,893 orbits, depth 1346);
* 3 left UNDECIDED by reach as well: p24 (01)^12 (TOO_BIG at height 184), p32 `00001110001100010000111000110001` (TOO_BIG at height 220), p32 (01)^16 (TOO_BIG at height 21).
No disagreement in either direction: no word that EXTERIOR exhausted has a reach stream, no stream reach finds is missing from EXTERIOR's ACCEPT list.
The full list is in `results/exterior_vs_reach.json`.

## E. What is NOT established
* No proof that the position automaton (bx / reach) equals the Lean system `Agent120.Neutral.cycleOK`. The checks are: identical recursion up to bookkeeping, replay of all four decimal streams through the Lean mirror and through integers (A), orbit enumeration in bases 2, 3, 4 (B), identical state counts (C), identical census (D).
* The converse direction at large decimal widths (every Agent120 B-cycle of width up to about 50 is a reach stream) is only supported by the census and the structural identity, not by an independent enumeration (a brute enumeration of 19^50 lists is impossible).
* A reach stream gives a B-cycle (exterior). A decimal Lychrel number needs a centre as well (`Agent6NineRailCentreRenewal`); that is not done here.
