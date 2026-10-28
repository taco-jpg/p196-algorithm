# FORMATS.md -- W3 "formats": generalized self-similar templates for reverse-and-add

All labels: COMPUTED / PAPER PROOF / LEAN-VERIFIED / UNDECIDED with exact scope.  Nothing here is LEAN-VERIFIED.
Code: `code/` (all paths below relative to /home/claude/research/w3_formats).

## 1. Definition (format G)
Base b.  Pair word of N = coefficients P_i = d_i + d_{n-1-i} (LSB first, 0..2b-2); N + rev N = sum P_i b^i, and the pair word of the
next number is pairs(digits(N + rev N)).  A *template* is a palindromic pair word  P = Hs ++ core ++ mirror(Hs)  where Hs is a list of
items: literal blocks and *bands* w^g (block w of any length m>=1, exponent g_pid symbolic and large; a band and its mirror share g_pid).
core = palindromic literal.  Agent120's format is the special case Hs = (B, (b-1)^g), core = C.  `gt.py`: Template, step(T) -> (T', gmap, info),
gmap[new pid] = (old pid, mult, offset), info = {gam (overflow), differs (O is not a palindrome)}.

## 2. Exact dynamics (PAPER PROOF of the mechanism, COMPUTED validation)
* Carry map of a block w: f_w(c) = carry out of norm(w, c).  f_w = id iff w = (b-1)^m (NEUTRAL band: transmits carry; needs flip e1 != e2).
  Otherwise f_w is constant: ABSORBING band, first copy sees the carry in, all later copies see the fixed point c*; the digit output is steady.
* A neutral band with e1 = e2 becomes an absorbing uniform band 0 or 2(b-1) (the only way single-band templates die; W4 confirms 100% of deaths).
* Mirror pairing O_x + O_{n'-1-x}, n' = n + gam, shifts the partner by gam positions; lattice update w'[i] = dl[i] + du[m-1-i] (gam=0) or du[(m-i)%m] (gam=1).
* gap maps: n' = n + gam <= n + 1, hence every gap map has multiplier 1 (a multiplier >= 2 doubles a band); only offsets matter (item (c) of the plan: PAPER).
* Reflection equivariance (PAPER, numerically verified): the pair-word step commutes with reflection about the number's centre; a lattice
  symmetric about R_t maps to one symmetric about R_t + gam_t/2.  Hence (see 5) a self-mirror absorbing lattice needs NO centre structure.

## 3. Validation status (COMPUTED)
* test_gt.py: 15,454 random steps (bases 2..26, 0-3 bands, block lengths 1-3, adjacent bands, empty cores) vs big-integer RAA: 0 mismatches, 0 unsupported, palindrome flag exact.
* test_regress.py: equals the Lean-mirror nextB/nextC/trim on 7,316 random single-band cases; re-derives all 8 known certificates
  (bases 2,4,8,16,32,26,11,17), each returning to itself with net gap +1 per cycle.
* test_pad.py (17,235), test_band.py (5,547): padded absorbing-band and band-successor formulas vs engine, 0 mismatches.
* kink.py: window one-step map vs big-int RAA, 20,000 random cases incl. both parities and gam, 0 bad.  kink_check.py: p=8 lattices are bulk solutions for all offsets, 0 bad.
* Validity threshold: the engine assumes all gaps "large" (symbolic comparisons decided by pid coefficients); no rigorous g_min is proven.  Tested g in 25..70 (engine) and l0 = 1..199 (merged lattices below).

## 4. Soundness statement for a cycle (PAPER PROOF, conditional on step-exactness for g >= g_min)
Let T_0, ..., T_{q-1}, T_q = T_0 (up to pid relabelling) with gmap multipliers 1, all per-orbit offsets >= 0 over the cycle (net > 0 gives growth),
each step with info.differs = true, and lead coefficient >= 1.  Then for every integer N_0 with template T_0 and gaps >= g_min, N_i never is a palindrome
(induction on cycles; gaps never shrink below g_min).  The single-band certificate is the case q = number of edges.  Lean effort (ESTIMATE, not a prediction):
the existing A120* files give norm/val/step; the new work is (i) a general theorem "carry through w^g" (absorbing/neutral), (ii) the pumping lemma for pairs(O) on lattices,
(iii) a decidable checker for a cycle; I would guess several thousand lines.  Alternative: Lean-check each concrete certificate by `decide`-style finite replay for gaps in [g_min, g_min+m)
plus the pumping lemma once.

## 5. NEW: merged symmetric lattice certificates (bases 9 and 13)  -- COMPUTED, symbolic engine cycle, plain-integer replay; NOT Lean-verified
Exterior census (bauto3 = reachable-state graph of the position automaton, ANY periodic lattice): an SCC cycle of length m (spatial period) for stream g (period p, S = sum gam)
is a periodic band.  If the lattice words w_t are palindromic necklaces and m | S, the centre closes automatically (section 2, equivariance): no core, no centre search.
Template at time t:  P_t = B_t ++ (w_t^inf)[:l_t] ++ rev(B_t),  l_{t+1} = l_t + gam_t,  l_0 = a+1 (mod m) for a symmetry axis a of w_0.
Found (base, p, gam, |B|, m, S):
* base 13, p=10, gam=1010010000, S=3, uniform lattice m=1, schedule w_t in {16,8,...} (absorbing loop {8,16}); two B-cycles: |B|=75 and |B|=55.
* base 9,  p=10, gam=1100011000, S=4, lattice m=4 (palindromic necklaces), two B-cycles |B|=61 (axes 1 and 3).
* (base 4 p=6 gam=101100 also, base 4 is a power of 2: known.)
Checks (all COMPUTED): (a) engine_sym3.py: symbolic template cycle with mult 1, differs=true at every step: template returns after 20 steps (2 periods), gap +3 (b13) / +1 (b9) per cycle;
(b) replay_int.py: explicit integer N_0 (base b digits), plain digit-list N + rev N, 600 steps (60 periods), no palindrome, pair word equals the template at EVERY step;
(c) verify_int.py (independent: Python big ints, base conversion by divmod, no templates): 3000 steps, no palindrome (n grows from ~110-150 to ~1000-1300 digits);
(d) replay_scan.py: starting gaps l0 = 1..199 (all axis-compatible) each 3 periods: 0 failures.
Saved: out/cert_b13_rec0.json, cert_b13_rec1.json, cert_b9_rec0.json, cert_b9_rec1.json (B_t, w_t, gam stream, N_0 digits).  Reproduce:
`bauto3 13 10 10 -g 1010010000` / `bauto3 9 10 10 -g 1100011000`, then `python3 code/replay_int.py 13 out/b13_p10.txt 1 1 60`, `python3 code/engine_sym3.py 13 out/b13_p10.txt 1`.

## 6. Base 10 search results (COMPUTED, bauto3; scope = streams listed)
* All gam necklaces p=1..24, cap 3,000,000 states, ANY periodic lattice (neutral, uniform absorbing incl. time-varying schedules, non-uniform): cycles exist only for
  p=8 (g=10101010: SCCs with lattice periods 20, 20, 48), p=11 (neutral, known), p=12 ((1000)^3: neutral, known, plus a lattice with m=9).  p=9,10,13,14,15,17,19,20: none.
  UNDECIDED (state cap reached): p=16 (10)^8, p=18 101010100101010100, p=21 101010100101010100100, p=22 x3, p=23 x1, p=24 x5; 2 p=24 streams skipped (key too long).
* No decimal merged-symmetric lattice (needs m | S and self-mirror) exists in the covered range: the p=8 lattices have m=20 or 48 with S=4; p=12 m=9 with S=3.
* The real decimal period-8 lock (W4: bottom cells (8,17), (12,5,13,6,14,8,16,13), (9,0,5,11,8,17,16,14)...) coincides with the first columns of the p=8 exterior found here
  (doubling counter 1,2,4,8,16,14,10 in column 3) but real orbits agree with it only for the lowest 3-5 positions (orbit_match.py, 196 for 3000 steps: max prefix match 5).
* Centre ("kink") for the p=8 / p=12-m9 / neutral p=11,12 exteriors: exhaustive pruned DFS (kinkdfs.cpp, all centre phases, any time period) finds NO time-periodic centre of lower-half width <= 5
  (p=8, p=12 m=9) and <= 7 (neutral p=11, p=12 |B|=53).  Control (same program): base 26 neutral exterior returns the known centres at width 3-5; base 11 control reaches width 6 only.
  Random-seed forward simulations and engine runs: core grows 4 digits per period (generic wall speed 0).  Wider centres UNDECIDED.
* Uniform absorbing outer bands (loops {0},{18},{6,12},{2,4,8,16,14,10}): no B-cycle for p <= 11/12.

## 7. Open items / next steps
1. Extend the symmetric-lattice census to all bases (census4 for bases 17..40 is queued: out/census4_b17_40.txt) and to larger p / capped streams; every hit must be replayed (replay_int.py).
2. Lean-check the base 9 / 13 certificates (needs the pumping lemma for absorbing lattices).
3. Base 10: wider centre kinks (CP-SAT was too slow; kinkdfs scales x10 per width unit), capped streams p=16..24, self-mirror lattices from non-shortest SCC cycles.

## 8. Second task: decimal merged-lattice exterior search beyond p=24 (DRAFT; final numbers in NOTES.md 3.6-3.8)
Scope words: COMPUTED = exhaustive/exact program run with the stated caps; PAPER = hand argument; UNDECIDED = cap reached.  Nothing here is Lean-verified.

8.1 Position-automaton view (PAPER, validated by 3,420 big-int tests and differential tests of the predecessor enumerator)
* A periodic exterior lattice for overflow stream g (period p) is a cycle in the automaton on states (L,H,Y) over the time ring Z/p.  A cycle of length m is a lattice of
  spatial period m.  m=1 (uniform band) lattices are the self-loops of the base-b map k -> 2*((k+[k>=b]) % b); in base 10 the loops are {0},{18},{6,12},{2,4,8,16,14,10}.
  The self-loop exists for EVERY stream (Y_i = band digit), so for uniform bands the whole question is REACHABILITY from the start state (L=0,H=g,Y=1).
* The uniform {6,12} band feeds a FIXED carry schedule (0 / 1 alternating) to the outer part; the outer part is then an autonomous one-way automaton (this is the
  coordinator's observation).  Operationally: backward co-reachability cone from the band state + forward closure (bwdcensus / bwdwords, code/bwd_common.h, solve.h).
* Self-mirror (palindromic necklace) lattices of spatial period m | S_p are exactly the periodic orbits of the cyclic row map (code/latenum.cpp enumerates them for
  given (b, g, m)); they need no centre.  Base 10 has MANY of them (p=10: 194; p=16 (10)^8: 4 uniform + 48 with m=4) -- existence is not the obstruction.

8.2 Results, base 10 (COMPUTED)
* Uniform-band reachability, all overflow necklaces (G >= ceil(p/5), p <= 4G), loops {0},{18},{6,12},{2,4,8,16,14,10}: NO hit for p = 2..29 on every stream that the
  engine decides.  Streams the engine could not decide (both forward closure and backward cone exceed the cap) are listed in NOTES.md 3.8 / out/und_*.txt and are all
  DENSE words (many gam=1; e.g. (10)^8, (1000)^6, (10)^12, 101010100101010100).
* Control (same engine): base 13 p=10 g=1010010000 -- finds the hit at depth 55 (cone 53k states vs forward 250k); base 9 g=1100011000 -- m=4 lattice, depth 61; base 4 known hit.
