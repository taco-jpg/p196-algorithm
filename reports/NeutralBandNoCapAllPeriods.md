# NeutralBandNoCapAllPeriods: details

Labels: COMPUTED = exact finite computation, no state caps; PAPER PROOF = argument below. Base 10 throughout.

## 1. The wire as a lattice
In the neutral-band format B ++ 9^g ++ ... the run of pair coefficients 9 stays 9 iff exactly one carry crosses each cell per step
(c + d = 1). The ascending carry therefore passes unchanged through the wire, and the stream s_t delivered by the exterior is the
ascending carry at the top of the wire. The structure sitting on the wire must return d_t = 1 - s_t. Equivalently, the wire is a
spatial-period-1 "lattice" of 9s whose steady upward carry is s_t and whose steady downward carry is 1 - s_t. The edge relaxation of
`results/EdgeRelaxW9NoCentre.md` (code `calculation/decimal_frontier/lattice_kinks/edge_relaxation/kink6.cpp`) applies with this table.
In this table the "lattice intact" test is exactly the wire condition, and the r-digit of the wire cell below is 9 s_t.

## 2. Exteriors and streams (COMPUTED, re-derived)
`up4.cpp` builds all periodic left pieces upward from the least significant end and stops when the set of interfaces repeats.
- p11, g=00001110001: unique stream `00111010011` at height 29, interface set repeats at 60/59 (complete).
- p12, g=(0001)^3: streams `101101010010`, `001010110101`, `010100101011` (4-step rotations of each other) at height 53, repeats 74/71.
These equal the census in `calculation/decimal_frontier/exterior_census/EXTERIOR.md`. p22 is p11 twice, with the same stream repeated
(Agent732P22BHistoryUniqueness), so its wire is the p11 wire.

## 3. Centres (frame = centre)
Reduction (PAPER PROOF, as in EdgeRelaxW9NoCentre):
- Let b(t) be the first non-9 cell above the wire's base and w0 = max over a period of (h - b).
- If w0 >= K, the K cells starting at the frame h - w0 form an infinite run of R_K that has a non-9 bottom cell infinitely often.
- If w0 <= K, the centre is a periodic orbit of the exact top window inside Cyc(K).
- Bounded-width centres are eventually periodic (finite window state), so periodicity is no restriction.

Counts of cyclic states / accepting (non-9 bottom) cyclic states, K = 3, 4, 5, 6:

| wire | K=3 | K=4 | K=5 | K=6 | exact centre cycles in Cyc(K) |
|---|---|---|---|---|---|
| p11 | 273/85 | 627/151 | 1026/131 | 1026/0 | 0 for K=3..6 |
| p12, each stream | 303/63 | 556/103 | 803/69 | 803/0 | 0 for K=3..6 |
| control (clock 0001, loop stream) | 720/286 | 1670/612 | 3214/834 | n/a | 1 (the known 16-step loop) at K=4, 5 |

`wirelat.py` (Python reference rule from klib, its own SCC and exact check) reproduces every number in this table.

## 4. Converters and centres of any drift (shift-budget frame)
A cap with period T and drift s cells per T (0 <= s/T <= v_c, the centre speed) is followed by the balanced frame
c(t) = floor((s t + phi)/T) - w0. A balanced 0/1 schedule of rate v has at most ceil(L v) shifts in any L consecutive steps.
So every such frame obeys the budget "at most 2 shifts in any 11 steps" (p11, v_c = 2/11) or "at most 1 in any 8" (p12, v_c = 1/8).
Adding the ages of the last shifts to the state keeps R_K finite and exact (`wirebudget.cpp`). Shifts may now occur on non-overflow
steps; the new top cell is then left completely free (0..18), which is an over-approximation.

| wire | K=3 | K=4 | K=5 | K=6 | K=7 |
|---|---|---|---|---|---|
| p11, budget 2/11 | 18021/9617 | 38938/17848 | 58352/14814 | 68168/7782 | 68168/0 |
| p12, each stream, budget 1/8 | 1474/346 | 2617/513 | 4136/437 | 4530/43 | 4530/0 |
| control (loop stream, budget 1/8) | 4640/2676 | 10836/5436 | 20006/6882 | 32536/10016 | (not needed) |

A converter sits far below the centre, so the 7-cell window always fits inside the number; centres of depth <= 6 are excluded in §3.

## 5. Fixed-period cross-check (separate SAT encoding, `edgesatg.py`)
The cap pattern must return shifted by `shift` cells after T steps.
- p11, T=11, K=8: SAT exactly for shift >= 3. With K=12, SAT for shift >= 4.
- p11, T=22, K=12: SAT exactly for shift >= 7. T=33 (shifts 0..7) and T=44 (shifts 0..9), K=12: all UNSAT.
- p12 (earlier session): SAT only for shift >= T/6, T = 12..48.

The centre needs 2 per 11 steps (p11) and T/8 (p12). Control: the known loop stream is SAT at its drift (2 per 16) in all phases.

## 6. Consequence
Every neutral-band template on a census exterior is excluded, whatever sits between the exterior and the centre: wire segments,
converters, and the centre itself. The neutral-band route to a decimal certificate therefore needs a new exterior, i.e. an overflow
word beyond the census (period > 32).
