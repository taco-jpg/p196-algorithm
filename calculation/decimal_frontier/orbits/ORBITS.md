# ORBITS.md -- W4 "orbits": what real reverse-and-add orbits look like, per base (Lychrel / neutral-band question)

Labels: COMPUTED = reproduced by the scripts named (exact integer arithmetic or exact C++ mirror); PAPER PROOF / LEAN-VERIFIED are not
claimed for anything new here.  "Regular" = from some step on, the pair word of the integer orbit is exactly a single-band template
B (b-1)^g C (b-1)^g rev(B) that follows the mirror prediction (nextB/nextC, g' = g - gam + u + v) with growing g, and the mirror's
canonical run from it returns a closed (B,C) cycle with cycleOK (= certificate).  All code in this folder; data in data/.

## 0. Bottom line (all COMPUTED, scope stated)
1. Natural orbits regularize ONLY in power-of-2 bases (2,4,8,16,32, and also 64,128,256,512,1024 -- see 2.2).  Not one natural seed of any other base
   (3,5-7,9,10,12-15,18,19,21-40) regularized in any run (exhaustive short seeds b^D <= 1.5e6 per base, random 6-30 digit seeds, smallest natural
   candidates for 20001 steps).  This includes the proven bases 11, 17, 20, 26 (no natural seed found there either).
2. Reason: a power-of-2 certificate is tiny (|B|=1-2, |C|=2-4, p=2k+2) so it has a large basin and short seeds fall in; the certificates of 11,17,20,26 have
   |B| = 7, 29, 90, 8 and |C| = 42, 21, 26, 4 (p = 6,6,8,4) and are isolated knife-edge cycles (one changed digit of the cert seed leaves the basin
   at once in 83-100% of trials).  => "base-10 orbits do not regularize" carries NO information about whether a base-10 certificate exists.
3. Base-10 orbits (196, 879, 1997, 7059, 10553, 10911 + 50 random 10-30 digit seeds, up to 3e4 steps, 250k-step overflow streams) show NO static
   hidden structure beyond a first-order Markov surrogate of their own pair word (no growing 9-runs, no periodic stretches, LRS/compression like null,
   no spectral lines).  The only non-random object is DYNAMICAL: the orbit repeatedly shadows quasi-cycles of the exterior (bottom/top frame +
   overflow stream): alternating overflow 0101.. for up to 85-105 steps, bottom cells with a doubling counter 1->2->4->8->16->14->10, period 8, locked
   3-5 cells for 25-70 steps.  Same phenomenon in every base >= 10 (base 11: 233-step alternation, 3 cells period 2 for 167 steps); it never closes.
4. Only open base with run structure beyond Markov-1: base 3 (constant runs z=+2.8 vs the surrogate, 36% of snapshots above surrogate maximum).
5. Template lifetimes (mirror-exact, 3e6 random single-band templates per base, bases 2..40): geometric death, 100% of deaths are e1=e2 (flip failure);
   nested family lifetime = s(b)*m with s(b) ~ 2.1*log2(b) (base 10: 7.05, 11: 7.2, 20: 9.2, 26: 11.0).  No cycle from random/hill-climb in any
   non-power-of-2 base.

## 1. Instruments (validated)
* rar.py numpy reverse-and-add (selfcheck vs Python ints, bases 2,3,7,10,11,20), nbs.py exact copy of the repo mirror (selftest PASS), cpp/tpl.cpp mirror-exact
  template evaluator (validated against nbs on 1500 random templates), cpp/enumscan.cpp exhaustive seed scan, cpp/lock.cpp exterior-lock statistics.
* Pair word P_i = d_i + d_{n-1-i} (LSB first), normalization = carry chain, gam = overflow.  Detectors on the half word: longest run of b-1 / 0 /
  2(b-1) / any constant; periodic stretches p=2..6; longest repeated substring (rolling hash, verified vs brute force); zlib ratio; frozen bottom/centre
  frame (prefix equal to the element q<=24 steps earlier); single-band template fit (rar.bands/template_of) + mirror prediction check.
* Nulls: random digit strings of the same length (24 lengths 20..20000), permutation and first-order Markov surrogates of the actual half pair word,
  shuffled step order for temporal statistics.

## 2. Regularization, base by base
### 2.1 Proven bases: certificate seeds (certseed.py replay; data from nbs/Lean files)
| base | cycle p | |B| | |C| | sumgam | gain | seed replay (g0=4,6,40; 600 steps) |
| 2,4,8,16,32 | 4,6,8,10,12 | 1-2 | 2-4 | 2 | 3 | pair word == predicted template at every step, no palindrome |
| 11 | 6 | 7 | 42-43 | 2 | 3 | same |
| 17 | 6 | 29 | 20-21 | 2 | 3 | same |
| 20 (PR#356) | 8 | 90-91 | 25-27 | 2 | 3 | same |
| 26 | 4 | 8 | 4-5 | 2 | 3 | same |
Regularity begins at step 0 (the seed is the template).  The gap grows by 1 per cycle (final g = g0 + 600/p).  COMPUTED.
One-digit perturbation of a cert seed (certseed.py perturb) leaves the cert basin (observed best template -> mirror cycle with cert) immediately in 83-100%
of trials in every zone (B, lower band, C, upper band, top) -- the cycles are isolated.

### 2.2 Natural seeds
* Base 2: random 6-30-digit seeds: 75/75 non-palindromic orbits regularize, entry step min 1 / median 20 / max 301, always the (p=4, sumgam 2, gain 3) cycle.
  Seed 22 = 10110_2: entry step 10 (n=11 digits, |B|=2, |C|=3, g=2); 26 and 28 same.
* Natural seed family  1 0 (b-1)^k (b-2)  (k>=2; base 2: 10110=22):  regularizes onto the certificate cycle in EVERY power of 2 tried:
  b=2,4,8,16,32 (entry 5-14), b=64 (entry 9-16, p=14), b=128 (10-18, p=16), b=256 (11-20, p=18), b=512 (12-22, p=20), b=1024 (13-24, p=22): cycleOK True, sumgam 2, gain 3, B sizes 1-2, C sizes 2-4,
  integer orbit of val(template) replayed 6p+5 steps for g0=4,6,40: pair word == template every step, no palindrome (verify_pow2.py,
  data/pow2_beyond32.json holds the edges).  Powers of 2 are known in the literature, so this is NOT a new base; Lean certificates exist only to 32.
  The same family in bases 3..40 (k=2,3,4): dead or non-regular, never regular.
* Exhaustive short seeds (cpp/enumscan; all seeds with D digits; T=300; flagged = neutral run >=20% of the half word at T/2 and T and growing; data/enum_all.log):
  fraction of ALL D-digit seeds that regularize: base 2 D=19 44%, base 4 D=10 2.6%, base 8 D=6 1.8%, base 16 D=5 0.18%, base 32 D=4 0 (of 1.0e6);
  all other bases 0 flagged: base 3 D<=12 (354k), 5 D<=8, 6 D<=7, 7 D<=7 (706k), 9 D<=6, 10 D<=6 (900k), 11 D<=5, 12-15 D<=5, 17 D<=5 (1.3M), 18-34 D<=4,
  35-40 D=3.  Flagged seeds in 4/8/16 re-run with the mirror: entry 1-12, cycle p=6/8/10, is_cert True.
  Probability of regularizing decays with the base even among powers of 2 (the cycle is larger relative to the seed space).
* Random long (6-30 digit) seeds, 150 per base, T=4000: regular only in base 2 (75); 0 in the other 38 bases (data/census_proven.jsonl, census_open.jsonl).
* Smallest natural candidates (no palindrome in 300 steps; 6 per base 2..20; 20001 steps): regular only base 2 (all 6) and base 4 (n=318, entry 8).

### 2.3 Open bases (prime targets for W1)
No non-power-of-2 base has an orbit that regularizes (2.2).  No base other than 2^k showed any mirror cycle from random or hill-climbed templates (3.2).
=> no orbit-derived certificate in any open base; nothing to Lean-check.  Orbit evidence cannot discriminate bases (2.1: proven bases look like open ones).
Base 3 is the one open base with real run structure (4.3) and the smallest base; worth a dedicated multi-band look (W3).

## 3. Template lifetime study (cpp/tpl, life_study.py; data/life_study.json, data/nested.json)
3.1 Random single-band templates (|B|<=10, |C|<=16, cells = sum of two uniform digits; 3e6 per base): 53% die at step 0 (Hyp fails), tail geometric with slope
   -0.16 (b=2), -0.135 (b=3), -0.24 (b=10), -0.25 (b=11), -0.27 (b=20), -0.30 (b=40).  Deaths: e1=e2=0 and e1=e2=1 in equal halves, no other reason ever.
   Longest random lifetimes 43-157; cycles only in 2,4,8,16,32 (all certificates).
3.2 Hill climbing (800 restarts x 600 evals, |B|<=12, |C|<=20): max lifetimes b=10: 155, 11: 149, 20: 169, 26: 369, 34: 365, 35: 328, 3: 101; no cycle in any non-power-of-2 base.
   Base 10 champions are nested bands: B=[12,9], C=[6,9^18,6] (t=155), B=[14], C=[4,9^12,4] (t=137): an inner neutral band inside C is eroded and never sustained.
3.3 Nested family B=[B1], C=[x,(b-1)^m,x]: best lifetime ~ s(b)*m: s = 2.4 (b=3), 4.6 (5), 6.7 (9), 7.05 (10), 7.2 (11), 9.2 (20), 11.0 (26,32); s ~ 2.1 log2 b.
3.4 Real orbits: a neutral run of initial length L (runtrack.py, 30000 steps, bases 10/11/20) lives 1.7/3.8/5.4/7.2/8.9/11.4 steps for L=4..9, max 14-17; identical in the
   three bases (L=5: 3.78, 3.78, 3.89) = the same erosion law as the template study.

## 4. Base 10 vs null
4.1 Static detectors (b10_orbits.jsonl.gz: 6 named + 50 random seeds, T=3e4, n up to 12.5k, 6380 windows) vs random-digit-string null (960 samples):
   longest 9-run orbit 3.2 vs null 2.9 (exceeds null 99th pct in 4-7% of windows, max 8 vs null max 5); periodic stretches p=2..6, LRS, zlib: identical to null;
   zero/18 runs: orbit mean 2.3 vs null 1.15 (38% above null q99) -- explained by the orbit's own cell marginal (P(0)=P(18)=0.032 vs 0.01 for two uniform digits).
   Frozen bottom / centre frame (prefix equal to the element q<=24 steps earlier): mean 1.0 / 0.9 cells, max 5.  The single-band template follows the mirror prediction
   in 8 of 3300 windows (n>=500), never a cycle.  196, 879, 1997, 7059, 10553 are not different from random seeds; 10911 dies at step 55 (known).
4.2 Surrogates of the actual half pair word (surrogate.py; 12 random seeds per base + named; permutation / Markov-1; 12 checkpoints up to T=8000):
   bases 5,6,7,10,11,20: |mean z| <= 0.8 vs Markov-1 for run, periodic and LRS statistics, fraction above surrogate max <= 0.07 -> no structure beyond nearest-neighbour correlation.
4.3 Base 3 is the ONE anomalous base (surrogate.py to T=1e5, 3 random + 2 named seeds, 12 checkpoints, 60 snapshots, n up to 60k; cpp/runs.cpp single orbits):
   constant-run statistics exceed the Markov-1 surrogate: any-constant z=+3.9, 0-run z=+4.0, 2(b-1)-run z=+4.4, 9-run (digit 2) z=+3.5, LRS z=+3.3, 55-60% of snapshots above the
   surrogate maximum (T<=8000: z~+2.5).  cpp/runs.cpp (natural seed 103, n=15k-36k): longest 0-run 25 vs Markov-1 expectation 7.2, 4-run 29 vs 7.2, 2-run 17-24 vs 12-14 (2.5-3.5x for the
   absorbing values); bounded around 20-30, NOT growing with n.  Bases 4-11, 20 (same tool, n=10-28k): ratio real/expected 0.7-1.4 (base 10: 4/4.3; 11: 4/3.9; 20: 3/3.6).
   Mechanism seen in a space-time diagram (seed 103, t=4502-4564): a neutral run of 2s (length ~30) forms from converging neighbours, at t=4528 it flips to a run of 0s in ONE step (e1=e2
   event) and then erodes ~1 cell/step on one side, ~0.5 on the other for 34 steps.  So: sticky absorbing runs of a small alphabet, no regularization; but base 3 is the base where
   the single-band Hyp (e1!=e2) fails most visibly by 'collapse into an absorbing band' (relevant for a generalized format, W3).
4.4 Overflow stream gam_t, 250k steps (gamstream.py, gam_analysis.py, gam_markov.py): density 0.41; zero-runs 1-4 only (nmax(10)=4 as theory); conditional entropy h_8 = 0.445 bit
   (shuffled 0.978); longest 0101.. stretch 105 (Markov-8 surrogate fitted to the stream: max 73-75; counts >=60: real 8 vs 1.5 mean/4 max, >=70: 4 vs 0.2/1, >=100: 1 vs 0).
   Short stretches (30-40) are FEWER than in the surrogate: the stream is bimodal (locked / free).  Base 11 stream: longest 233.
4.5 Exterior lock (cpp/lock.cpp; one orbit per base, 20-digit random seed, 1e5 steps; data/lock_100k.txt, lock_table.py): longest run of steps for which the lowest K cells of the pair word are
   exactly p-periodic in time, vs shuffled baseline (<=17):
   base 10 : K=1 79 (p even), K=2 69 (p=8), K=3 69 (p=8), K=4 33-44 (p=8,9), K=5 25 (p=8), gam alternation 85
   base 11 : K=1 183, K=2 177, K=3 167 (all p=2), K=4 25, gam alternation 189
   base 17 : K=1 81 (p=4), K=2 46 (p=6), K=3 27; base 20: K=2 77 (p=4), K=3 69 (p=4); base 26: K=1 307, K=2 67, K=3 45, K=4 35 (p=2); base 32: K=1 257.
   All bases >= 10 show the effect with dwell 25-350 steps and widths 1-4 cells; base 10 is neither special nor weaker (period 8 lock is its signature).  Locked cells carry the doubling counter
   (column of 3rd cell in seed 196, t=2743: 14,10,1,2,4,8,16,14,10 ... = the F-cycle {2,4,8,16,14,10} of constant runs).
4.6 Flip condition (cpp/lock.cpp, 2e4 steps): e1 != e2 for the lowest K cells (carry out of cells 0..K-1 vs carry into the top K cells = the certificate's autonomy condition) holds in 46-53% of
   steps (b10, b11, all K=1..8), longest consecutive run 11-18 (K>=3) -- random-like.  Hence the time-periodic locks of 4.5 are NOT autonomous exterior cycles: in the lock of seed 196
   (t=2743-2800, K=3, p=8) e1(3), e2(3) are equal in 11 of 16 rows and the e2 stream differs between periods; the bottom cells are periodic because the top-zone carry only matters when the
   ripple reaches the top digit.
4.7 Multi-seed spread (data/lock_multi.txt: 8 random 20-digit seeds per base, 1e5 steps, lock3/lock4):
   base 10: overflow alternation (p=2 stretch) median 90 (61-115); bottom K=2,3 cells lock ALWAYS with p=8 (8/8 seeds), median 74 / 73 steps (43-97), K=4 median 41 (p=8,12,16), K=1 median 84.
   base 11: alternation median 135 (72-223); K=1,2,3 lock with p=2, median 129/123/113 (max 217/211/201); K=4 median 37.
   base 20: alternation median 136 (107-227); K=2 median 61 (p=4,14,16), K=3 43 (p=4,16), K=4 22.
   => every base shadows a G/p = 1/2 exterior quasi-cycle (overflow every other step) for ~100 steps; the frame period differs: 8 in base 10 (Sigma gam = 4 per 8 steps = exactly the base-10
   counter bound P/G <= 4 / Sigma gam >= 4 of W1/W2), 2 in base 11, 4/16 in base 20.  Certificate cycles have G/p = Sigma gam / p = 1/3 (bases 11, 17), 1/4 (20), 1/2 (26), 2/(2k+2) (base 2^k).
   Named base-10 seeds (data/lock_b10_named.txt, 5e4 steps): 196: alternation 77, K=2,3 p=8 59/55; 879: 165, p=8 155/147 (K=5 45, K=6 25); 1997: 67, p=8 51/51; 7059: 83, p=8 67/63;
   10553: 83, p=8 67/65 -- same distribution as random seeds.
   COMPUTED observation only; no claim that these near-cycles are related to any exact cycle (W2: no exact exterior cycle with p<=10 in base 10).

## 5. What this says about base 10 (honest reading)
* The absence of regularization in base-10 orbits is expected under the isolated-cycle picture: proven bases 11/17/20/26 look identical to base 10 under every natural-seed test.
* Nothing in the static statistics suggests hidden extra regularity (multi-band, periodic end blocks, growing 9/0 runs) in base 10.
* The dynamical near-cycles (exterior locks) are the one non-random feature: the real orbit visits neighbourhoods of exterior cycles with a doubling counter, for tens of steps, in all bases.
  In base 10 the lock periods are 8 (frame) and 2 (overflow alternation) although exact exterior cycles exist only at p=11,12 (W1/W2): the orbit's frame is NOT closed; the middle perturbs the
  frame upward each period.  A closing mechanism would need a centre that returns the right carry stream; this is the (undecided) centre problem of W2.

## 6. Prime targets, implications, next steps
1. No orbit-derived certificate in any open base (nothing for the coordinator to Lean-check from W4).  Orbits cannot find certificates with |B|>~3 (basin ~ 0), so the orbit method is only a
   detector for tiny cycles; tiny cycles in open bases are W1's exhaustive domain.
2. By-product (literature-known family, therefore not a ranked hit; rule-4 replay done anyway): mirror-checked cycleOK certificates in bases 64,128,256,512,1024 (p=2k+2, sumgam 2, gain 3), reached from
   the natural seed 1 0 (b-1)^k (b-2) in 9-24 steps; edges in data/pow2_beyond32.json.  Lean currently stops at 32; this family could be added with a generator for 2^k.
3. W3 (generalized formats): real orbits show the neutral band dying by a single-step flip to an ABSORBING band of 0 (or 2(b-1)) (base 3 space-time, e1=e2 event; 100% of template deaths in all
   40 bases are e1=e2).  A format with absorbing 0/2(b-1) bands should be tried first in base 3 (smallest alphabet, longest-lived absorbing runs, 2.5-3.5x Markov expectation).
4. W2 (why base 10 fails): the real base-10 orbit's dominant exterior near-cycle is p=8, bottom K=2-3 cells locked 50-150 steps, overflow 0101..., Sigma gam = 4 per 8 steps = the
   counter bound; frames printed by cpp/lock3 (e.g. 196 at t=2743: cells (8,12,9),(17,5,0),(8,13,5),(17,6,11),(8,14,8),(17,8,17),(8,16,16),(17,13,14)).  Question to test exactly: is there a
   B-cycle of period 8 with |B|=4..6 and gam stream (01)^4?  (W2 reports none for p<=10, i.e. the orbit's lock must be driven, not autonomous: see 4.6.)
5. Not done / undecided: lock statistics for more bases with many seeds (only 3 bases x 8 seeds + one orbit for the rest); mirror-consistency streaks of real-orbit templates (dense) per base;
   base-2^k anatomy of the basin boundary (why P(regular|D) decays with k); multi-band detector on base-3 orbits.

## 7. Reproduce
python3 certseed.py replay;  python3 census_list.py ...;  ./cpp/enumscan BASE D T FRAC;  ./enum_all.sh 300 0.2 1500000;  python3 verify_pow2.py 64 128;
cpp/tpl rand|climb|eval; python3 life_study.py data/life_study.json BASES; python3 nested_only.py data/nested.json BASES; python3 surrogate.py BASE T NORB NSUR OUT [seeds];
python3 gamstream.py BASE SEED STEPS OUT.npz; python3 gam_analysis.py OUT.npz; python3 gam_markov.py OUT.npz 8; cpp/lock3 BASE SEEDLEN|n<decimal> SEED T KM PM; python3 lock_table.py FILE;
python3 analyze_b10.py data/b10_orbits.jsonl.gz data/null_b10.jsonl.gz;  python3 runtrack.py BASE SEED T L0.
All long runs went through /home/claude/research/bin/heavy.
