# W6 -- hybrid centres: pair word  B ++ N^g ++ C ++ c^h ++ rev C ++ N^g ++ rev B   (base 10, N = 9)

Labels: COMPUTED (exact finite computation, scope stated) / PAPER PROOF (hand argument, no Lean) / LEAN-VERIFIED (none here) / UNDECIDED.
All code in this folder; everything below was re-run from the files named.

## 0. Bottom line

* The hybrid format is SOUND and its exact step function is validated on thousands of big-int instances (Section 2, 3).
* An independent positive control exists: base 4 has a genuine hybrid cycle (odd sum gam = 3, impossible for a neutral centre) that was
  replayed 30 000 steps with plain big-int reverse-and-add, template checked at EVERY step, never a palindrome (Section 5).
* DECIMAL: no hybrid cycle exists over the known neutral exteriors p11 and p12 in the scope of Section 6 (COMPUTED, exact decision procedures,
  not sampling), and the stationary-wall case (A = 0) is excluded for EVERY period multiple of p and EVERY width (COMPUTED, finite automaton).
  The same A = 0 automaton kills ordinary neutral centres of that kind. What is NOT excluded: moving wall A > 0 for large periods / large A
  (UNDECIDED), and every exterior that is not a neutral-N band (p = 8 lattices, two cores, period-m cores) (UNDECIDED, Section 8).

## 1. Format and notation

Pair word = LSB first, P_i = d_i + d_{n-1-i} in 0..2b-2; it is always palindromic; the next pair word is pairs(digits(val(P))).
Blocks: B (exterior word, carry-in 0 at the bottom), N^g (neutral gap, N = b-1), C (centre word), c^h (absorbing core), then mirrored.
c is absorbing: c != N and c <= 2b-2, so the carry out of c^h is the constant k = [c >= b] whatever the carry-in is (c + 1 <= b-1 < b if c < b-1).
Core value map: y = (c+k) mod b, c' = 2y.  In base 10 only four loops exist (c' never 9): {0}, {18}, {6,12}, {2,4,8,16,14,10}.
Carry flow: B -> e1 ; N^g passes e1 ; C (carry-in e1) -> e2 ; core -> k ; rev C (carry-in k) -> e3 ; N^g passes e3 ; rev B (carry-in e3) -> gam.
Neutral gaps reproduce iff the two gap digits x = (N+e1) mod b, w = (N+e3) mod b satisfy x + w = N, i.e. e1 + e3 = 1 (the flip).
The exterior B is autonomous (it never sees C); it emits the stream (e1_t, gam_t).  Decimal exteriors with a flip stream: p11 (|B| = 25..29,
sum gam = 4 per 11 steps, g = 11100010000, e = 10100110011) and p12 (|B| ~ 51..53, sum gam = 3 per 12, g = (1000)^3, three rotations of one class);
W1 census files: w1_bases/out/ext4/b10_p11.txt, b10_p12.txt (no ACCEPT line for p13..p21).

## 2. Exact one-step dynamics (PAPER PROOF + COMPUTED validation)

Digits of the sum: DB,e1 = norm(B,0); x gap digit; DC,e2 = norm(C,e1); core digits z = (c+e2) mod b then y^(h-1); DRC,e3 = norm(rev C,k);
w gap digit; DR,gam = norm(rev B,e3).  Then (pairing digit i with digit n'-1-i):
* gam = 0:  B' = DB + rev(DR) (entrywise), gap x+w = N, C' = DC + rev(DRC) then one extra entry z+y on top,
            core (2y)^(h-2).        g' = g,   h' = h-2.
* gam = 1:  B' = (DB ++ [x]) + ([1] ++ rev DR)  (one longer), gap g-1, C' = (DC ++ [z]) + ([w] ++ rev DRC), core (2y)^(h-1).   g' = g-1, h' = h-1.
New core value c' = 2y.  Canonical trims (state is only defined up to merging into the bands):
u = number of N at the top of B' (join the gap), v = number of N at the bottom of C' (join the gap), p = number of c' at the top of C' (join the core):
    g'' = g - gam + u + v,      h'' = h - 2 + gam + 2p.
Closed cycle of length T (B, C, c return to themselves): sum u = sum gam (B closes), sum (v + p) = T (C closes), hence with A := sum v
    dg = sum u + sum v - sum gam = A >= 0 (automatic),    dh = sum gam - 2 T + 2 (T - A) = sum gam - 2A.
So the ONLY extra condition on a cycle is dh >= 0:   2A <= sum gam, i.e. A <= floor(sum gam / 2).  The parity of sum gam is free
(a neutral centre needs sum gam even; the hybrid does not), which is why base 4 admits a hybrid with sum gam = 3.
Code: hyb.py (hstep_raw, trim, hstep).

## 3. Validation and soundness

COMPUTED (hyb.py, `python3 hyb.py`): random instances (random B, C, c, g, h in 3..14, gap/core as templates), plain big-int
`n + rev n`, compare pairs(digits(val(P))) with the predicted template (pre-trim): b = 10: 3027 flip-ok instances, 0 mismatches;
b = 13, 11, 7, 3: 1245, 1220, 1228, 1267 flip-ok instances, 0 mismatches; flip-fail instances skipped; the next integer was never a palindrome.

THEOREM (soundness; PAPER PROOF).  Let (B_t, C_t, c_t)_{t in Z/T}, with canonical step as above, satisfy e1+e3=1 at every t, return to themselves
after T steps, and have dg >= 0, dh >= 0 per period.  Let g_0 >= T + 3 and h_0 >= 2T + 3.  Then every iterate X_s (s >= 0) of reverse-and-add started at
X_0 = val(P_0) with P_0 the template has pair word equal to the template with (B_s, C_s, c_s, g_s, h_s), g_s >= 3, h_s >= 3, and no X_s is a palindrome.
Proof: induction on s using Section 2 (the validated formulas hold for any g >= 1... h >= 2); g_s,h_s change by dg,dh >= 0 per period and drop by at most T and 2T
inside a period.  Non-palindrome witness: the digit string of X_{s+1} has the gap digit x (value 0 or N) at a position whose mirror position carries w, and x + w = N
with N != 0 forces x != w, so the digit string is not a palindrome (needs g_s >= 2).  Hence the orbit never reaches a palindrome: every such X_0 is a Lychrel
number in base 10 (and X_0 is not itself needed to be non-palindromic: val(P_0) is just the first sum).  Soundness with the closed-form consequences is
exercised by replay.py (`replay`) and replay_fast.py (Section 5).

## 4. Engines (all differentially tested against each other)

| engine | what it decides | files |
|---|---|---|
| hbf (C++) | brute force: every C of width <= W, every c, every phase; follow the exact dynamics to death / repeat / leaving width W | code/hbf.cpp |
| hsat (CP-SAT, 1 worker) | existence of a cycle in the register model Q_T = N^A Q_0 c^(T-A) (the C word of width W0, N-padded below, core-padded above); monotone in W0 | hsat.py, test_hsat.py (500 cases vs direct simulation, 0 bad) |
| htrans (C++) | EXACT decision for ALL widths for given (stream, k, loop, phase, A): BFS over spatial link states (Aup, G, ddprev, mem); EXHAUSTED means the start state never reaches the vacuum (core) link state | code/htrans.cpp, htrans.py, test_trans*.py |
| cells2 | stationary wall A = 0 for all periods at once: time automaton on the two lowest cells above the gap | cells2.py |

Cell picture used by htrans/cells2: register cell i (0 = lowest cell of C) holds v_i in 0..2b-2, one step maps v_i -> (v_i+a_i) mod b + (v_i+delta_i) mod b
(a = carry from below, delta = carry from above, with the descending-digit shift of the neighbour at gam = 1).  The register is N below (padding, "pops") and c(t)
above (core vacuum).  A cell with v = 9 stays 9 forever (a pop); sum v of the trims is A, the number of cells that pop below per period, i.e. the wall moves A cells per T steps.

## 5. Positive control: base 4 (COMPUTED + integer replay)

Base 4, B-cycle with g = 101100 (T = 6, e1 = 101010; sum gam = 3, ODD), C = [1], c = 4 (loop {2,4}), A = 0, dg = 0, dh = 3 per cycle.
replay_fast.py (numpy digit arrays, plain big-int sum): 30 000 steps, template compared at every step, `min g = 15, min h = 30`, never a palindrome; final length 15 093 digits.
Certificate: out/b4_ctrl_cert.json.  (The earlier replay.py ran 2000 steps with the generic code.)  hsat and htrans find the same cycle and its mirror; so the
engines are not vacuous.  In other bases (2..39, census exteriors, k = 1, T <= 12..24) the exact transfer returns SUCCESS only in base 4 (b = 11: 4 CAP instances, b = 20: 6 CAP, b = 22..39: 24 CAP are UNDECIDED).

## 6. Decimal search scope and results

All results below are COMPUTED unless noted.  "ALL widths" = exact transfer decision, not a width bound.

(a) Stationary wall, A = 0, p11 and p12, every period multiple of p, ALL widths, all four loops, all phases: NO solution.
    cells2.py: every cyclic SCC of the 2-cell time automaton has lowest cell == 9 (a pop), so no cell above the neutral gap can carry a periodic non-9 orbit.
    The unique lowest-cell orbit for p11 is v0 = 5,15,5,15,11,2,5,15,10,0,2 and it cannot host a second cell.  This kills hybrid AND ordinary neutral centres with A = 0
    on these exteriors (the base-4 control has a non-trivial SCC, so the test is not blind).
(b) Moving wall, A = 1..floor(sum gam/2): exact transfer EXHAUSTED (no cycle of any width):
    p11: T = 11 and 22 (k = 1, 2) with loops {0}, {18}, {6,12}, all phases, all A; T = 33 (k = 3) loops {0}, {18}, A <= 2.
    p12: T = 12 (k = 1), all four loops, all phases, all A.
(c) CP-SAT register model, INFEASIBLE for all A <= floor(sum gam/2):
    p11 k = 1: W0 <= 250 (loop {0}); k = 3: W0 <= 40 (loops {0},{18});  loop {0}: k = 1..7 (T = 11..77), W0 = 60 (out/sat_p11_loop0.txt).
(d) Brute force hbf, C width <= 5, all c and phases: 0 cycles for p11 (258 M states visited) and p12 (281 M).
(e) Controls in other bases (k = 1): SUCCESS in base 4 only.

Reason (heuristic + the exact facts above): the reachable set of link states from the N-padded start is tiny and independent of the loop; the lowest register
cell must be on the unique orbit above, a second cell never fits; larger A only lets cells pop (v = 9) and A >= 1 starts with mem = N padding that must eventually
turn into core values, and the transfer never reaches the core vacuum.

## 7. Non-palindrome witness / certificate protocol

A decimal hit would be (B-cycle, C, c, phase) plus g_0, h_0; run replay.py `replay(b=10, ..., steps >= 20000)` (template checked at every step against plain
`n + rev n`), store JSON with the integer digits of X_0, the B-cycle and exponent sequences.  No decimal hit exists, so no decimal JSON was produced.
The base-4 JSON (out/b4_ctrl_cert.json) shows the format.

## 7b. Variant: absorbing core on the decimal lattice exteriors (p = 8: W3 lattices lat0, lat1 (m = 20), lat2 (m = 48); p = 12, m = 9) -- NEW
Cell CA validated on the lattices (lat/latcheck.py): v_i' = (v_i+a_i)%b + (v_i+delta_i)%b (gam=0) or + (v_{i-1}+delta_{i-1})%b (gam=1), a = ascending carry,
delta = descending carry; reproduces W3's lattice evolution and cup arrays exactly on all 3 p=8 lattices (0 bad).  htrans3 (compact) is the transfer BFS started at the lattice
link state (control: lattice continuation found as SUCCESS; base-4 SUCCESS re-found; counts identical to the older engine on p11).
COMPUTED:
* Transfer, T = 8 (k = 1), cores {0}, {18}, {6,12} (all loops whose period divides 8), ALL widths, every departure phase j0, A = 0, 1, 2 (= floor(S/2) for S=4):
  lat0 and lat1 EXHAUSTED (max 1 133 290 states), lat2 EXHAUSTED (max 1 709 039 states).  p=12 m=9: T=12, A=0,1 EXHAUSTED.  T = 16, 24 : CAP (UNDECIDED).
* Stationary wall (A = 0), ANY period multiple of p, any width above, any content above (core OR kink): lat0, lat1 and the p=12 m=9 lattice have NO off-lattice cyclic SCC
  already for two cells (latcell2.py).  lat2: 44 of 48 positions die at 2 cells, j0 = 22, 46 die at width 4; j0 = 9, 33 stay alive (24 705 nodes at width 6) but the
  forced-core-top automaton (latcore.py, control: base 4 finds the known width-4 hybrid, decimal N-pad p11/p12: nothing) has NO hit for widths <= 5 (width 8 run was killed at wrap-up: UNDECIDED beyond 5).
* So no decimal hybrid (absorbing core) exists on the p=8 lattices for T = 8, A <= 2, nor stationary with defect width <= 5 (lat2) / any width (lat0, lat1, p12m9).

## 8. What is left (UNDECIDED) and the best next variants

1. Moving wall for larger T, large A: no finite reduction proved.  N-pad p11: the BFS dies within <= 7 cells for T = 11, 22, 33 (state count explodes with T and A, not the depth);
   a lowest cell lives <= 23 steps (life.py), which gives only A >= T/24 - 1 (no contradiction with A <= 2T/11).  p11 T=33 A>=3, T>=44, p12 T>=24: not exhausted.
2. lat2 (m = 48) stationary at j0 = 9, 33 for width > 5 (latcore.py, Python; port to C++), lattice T = 16, 24 moving walls (CAP), p=12 m=9 T = 24.
3. Two absorbing bands: B a^g M c^h rev M a^g rev B decouples into independent layers (carries are constants); big-int test (var/abs1.py, B width <= 2, 200 steps) shows B grows
   (no survivor beyond ~35 steps); NOT a proof.   4. Core bands of period > 1 (spatial period 2 cores): not implemented.
5. Queue leftovers that did NOT run (daemon killed at wrap-up): scan_cpp base 10 k <= 3, SAT batch for p11 loops 18/6/2 and p12 all loops, ctrl_bf bases 2..9, scan_cpp bases 11..15.
