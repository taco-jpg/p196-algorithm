# Round 14, tails: every periodic left part on the p11 and (1000)^3 clocks ends in a 9-wire or W0, and carries no periodic centre

Labels: COMPUTED (exhaustive program runs, no caps) + PAPER PROOF (the reduction below). Not LEAN-VERIFIED.
Nothing here is a statement about 196, and no Lychrel number is claimed. It excludes one class of mechanisms for all time;
it is not a certificate.

## What is new and what is already on main

Already on main (not restated): no centre of any width or time period sits on the 9-wire of the census exteriors p11 and p12
(`results/NeutralBandNoCapAllPeriods.md`), and none on the lattice B0/W9 of p12 (`results/EdgeRelaxW9NoCentre.md`; that lattice
is W0 below: `data/mchk13b/lat/p12m9.txt` is a rotation of `lattice_kinks/data/lat_p12m9.txt`).
New here: **completeness of the tails.** Not only the census exteriors but every d-periodic rooted infinite closed history (ICH,
r13c section 1) on these two clocks ends, above a finite head, in one of these objects. So no left part of time period d of any
kind (exterior with any band, lattice, anything) carries an eventually time-periodic centre. The same interface graph at d = 8
on clock 10 gives the complete list of period-8 tails used by `../r14a_lattices/`.

## Statement

Base 10. Let (g, d) be (00001110001, 11) or ((1000)^3, 12). Let (N_t) be a reverse-and-add orbit, P_t its pair word (folded
columns x < h_t = ceil(n_t/2)), with overflow gamma_t = g_(t+tau mod d) for all t >= t0, for some tau. Suppose that some d-periodic
rooted history X (columns X_x(t), infinite closed d-history in the sense of r13c, H_0(t) = g_t and X_0(t) >= 1) and some D >= 0
satisfy P_t(x) = X_x(t + tau mod d) for all t >= t0 and all x < h_t - D. Then the window (P_t(x))_(h_t - D <= x < h_t) is NOT
eventually periodic in t.

So on these two clocks a left part of time period d admits no time-periodic centre: of any period, any width, any number of laps.
With r13c Theorem B (round 13: every ICH of period L = 22, 33, 44 on the p11 clock is 11-periodic, and of period L = 24, 36 on
clock 1000 is 12-periodic) the same holds for left parts of those time periods L.

Not covered: other clocks (clock 10 stays open: task K1, see `../r14a_lattices/`), left parts of other time periods, centres that
are not eventually time-periodic in the frame of the fold (growing or quasi-periodic centres).

## Proof

Notation as in r12g sections 1-3, r13b sections 1-2, r13c section 2 (round 13).

**Step 1 (finite list of tails; COMPUTED).** By r13c Lemmas I1, I2 the interfaces of the d-periodic rooted heads form a finite
graph IF(d), and X is an infinite path from the root (edge = one column). `ifscc.py` builds IF(d) explicitly (`logs/if_*.txt`):
- p11, d = 11: 1,612 interfaces (saturation height 58), one non-trivial SCC: a loop labelled by the all-9 column, first reached
  at height 29.
- clock 1000, d = 12: 22,657 interfaces (height 70), four non-trivial SCCs: the 9-cycle of the lattice W0 (first height 34), and
  three loops labelled by the all-9 column (first height 53; the three are the time rotations by 4 of one object).
- clock 10, d = 8 (used by r14a): 22,601 interfaces (height 87), three non-trivial SCCs: the 20-cycles of rec0 and rec1 (first
  height 39) and one SCC of 1,056 nodes and 1,104 edges (cycle rank 49, growth 1.0534 per column, first height 11) that contains
  rec2 (shortest cycle 48) and closed walks of lengths 61, 64, 69, 92, 96, 97, ... .
- clock 1000, d = 4 and clock 10, d = 4: no non-trivial SCC (no 4-periodic ICH at all).
The interface counts and heights equal those of r13c's two implementations; the heights equal |B| = 29, 52-53 of the neutral
exteriors and nB = 34 of p12m9. An infinite path in a finite graph ends in one non-trivial SCC; at d = 11, 12 all of them are
single cycles. So above some height a0 the columns of X are those of one of these cycles: the wire (every cell 9) or W0.
By-product (same runs): none of the census bands of spatial period <= 8 with time period T | d (2 at d = 11, 19 at d = 12, 16 at
d = 8; band lists `data/mchk13a/logs/bc_*`) has a rooted d-periodic left end.

**Step 2 (window walks; PAPER PROOF).** Assume the window is eventually periodic and pass to the periodic regime (t >= t1, with
h_t - D >= a0 + 3m + 3). h_t grows without bound because g has at least one overflow per period. Let D now be the least integer
such that the left part agrees with X below h_t - D for all t >= t1 (D may have decreased).
If D = 0 and the tail is the wire: at a time with n_t odd the middle column is P = 2 d_mid, even, but the wire value is 9.
Contradiction (n_t changes parity at an overflow step). If D = 0 and the tail is W0: `depth0.py` (plain addition at every phase)
finds no such orbit (`logs/depth0_tails.out`; it also confirms the wire case).
If D >= 1: put c_t = h_t - D. For 1 <= K <= D the bottom K cells of the window, w_t = (P_t(c_t), ..., P_t(c_t + K - 1)), with
phase (t mod d, (c_t - nB) mod m, n_t mod 2), form a walk of the relaxation R_K, which is exact below the window and has a free
descending carry at the top of the window and a free low digit at frame shifts (r12g Lemma 3).
Lattice tail W0: exactly r12g/r13b. Wire tail: the wire has forward carry stream s(t) (the carry out of the head; it passes through
the 9-cells unchanged); the cell directly below the window is 9 at time t and at time t+1 iff the descending carry b leaving the
window satisfies (9 + s) mod 10 + (9 + b) mod 10 = 9, that is b = 1 - s(t) (the same relation holds at g_t = 1, where the digit
from the cell below is (9 + b) mod 10; it is the neutral condition e2 = 1 - e1 of the Agent120 format). At a frame shift the
leaving cell must be 9. Every step is therefore an R_K edge. Since the window is periodic, this is a closed walk. Since D is least,
at some time the bottom cell is off the tail: the walk passes through an accepting state. So its states lie in Cyc_acc(K), the
union of the strongly connected components of R_K containing an accepting state.

**Step 3 (computation; COMPUTED).** Cyc_acc(K) is contained in the children of Cyc_acc(K-1) (projection to the bottom K-1 cells,
r13b Lemma R2). Computed for every phase orbit (`logs/tails_cpp_py.out`, `logs/pyscc_wires.out`, `logs/w9_*.log`):

| tail | phase orbits | \|Cyc_acc(K)\|, K = 1, 2, ... | exact fold orbits inside, K <= 5 |
|---|---|---|---|
| p11 wire | 2 | 37, 62, 143, 346, 391, 0 and 30, 55, 130, 281, 635, 0 | 0 |
| clock 1000 wire (each of the 3 loops) | 1 | 78, 178, 303, 253, 247, 0 | 0 |
| W0 (m = 9) | 3 | 185, 504, 997, 2029, 3546, 0 (all three) | 0 |

So Cyc_acc(6) is empty: D >= 6 is impossible (Step 2 with K = 6). For 1 <= D <= 5 the window is a periodic orbit of the exact fold
map F_D inside Cyc_acc(D), and there is none. QED

## Verification

- Two independent programs give every count of the table: C++ `mc14w runscc` (carry tables; rule self-tested against genuine
  big-integer reverse-and-add, 300,000 random cases per tail file, `logs/selftest_tails.out`) and plain Python `pyscc.py` (every step by explicit carries along the whole
  word from column 0, overflow compared with the clock, plain Tarjan, exact orbits by big-number addition).
- Positive controls for the wire rule: all eight Lean-verified neutral certificates (bases 2, 4, 8, 16, 32, 11, 17, 26): the same
  program, on the wire loop whose first height equals the certificate's |B|, finds exact periodic orbits of the certificate's
  period at depth ceil(max|C|/2) = 2, 2, 2, 2, 2, 22, 11, 3 (`logs/posctrl2.out`, K <= 12; base 11 needs K = 22 and is in
  `logs/posctrl_b11_K24.out`). In those bases the closure does not die.
- Interface graph cross-check: at d = 8 every cycle word of length <= 128 of IF(8) is a cycle of the independent position
  automaton `bauto3 -dump` (`data/mchk13b/sccdump.txt`), and the 8 words found only in the bauto list (length 125) are closed
  (non-simple) walks of IF(8) (`logs/cmp_bauto_128.out`).

## Reproduction (from this directory; Python 3, clang++)

    P196_H=data python3 ifscc.py 00001110001 11 160 ; P196_H=data python3 ifscc.py 1000 12 160 ; P196_H=data python3 ifscc.py 10 8 160
    python3 mklat14.py 00001110001 11 lat 40 ; python3 mklat14.py 1000 12 lat 40      # writes the tail lattice files lat/*.txt
    clang++ -O2 -std=c++17 -o mc14w mc14w.cpp -lpthread
    ./mc14w selftest lat/1000_d12_scc0_len9_0.txt 7 300000
    ./mc14w runscc lat/FILE ORBIT 8 4 1          # every file of lat/, every orbit (FATAL orbit index = no such orbit)
    python3 pyscc.py lat/FILE 6
    python3 depth0.py lat/1000_d12_scc0_len9_0.txt lat/1000_d12_scc1_len1_0.txt lat/p00001110001_d11_scc0_len1_0.txt
    P196_H=data python3 cmp_bauto.py 128
    bash posctrl2.sh     # positive controls; reads logs/certs.txt (made by posctrl.sh from calculation/neutral_band_search.py)

Each IF(d) run takes a few seconds, every closure here less than a minute. `ifscc.py` reads the band census lists and the known
lattices from `$P196_H/mchk13a/logs/bc_*.txt` and `$P196_H/mchk13b/lat/` (copies in `data/`); `posctrl*.sh` and the original run
used the run directory `~/p196_run/mchk14` (adjust the `cd` line).
