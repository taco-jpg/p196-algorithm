# W5 — decimal exterior frontier (base 10 B-cycles)

Scope: exterior B-cycles of the autonomous B-system of the Agent120 neutral-band format (Lean `A120Template`: `nextB` with
`e2 = 1 - e1`), base 10, for a fixed cyclic overflow word `g` (period p, G = number of ones), ALL B-widths, ALL carry streams e.
A "B-cycle of length p" means B_p = B_0 (minimal period dividing p), so repetitions of shorter cycles are included.
Labels: COMPUTED = exact program output reproduced here; PAPER PROOF = argument written out below (checkable by hand/script);
UNDECIDED = capped, nothing claimed.  Everything below is for base 10 unless a base is named.

Files: `src/bx.cpp` (engine), `src/fc_enum.cpp` (first-coordinate NFA enumerator), `py/*` (validation, census driver, proofs-as-scripts),
`out/db_b10.jsonl` (one record per word: status, states, depth, cap, wdone, accepted e), `lists/` (survivor words), `studio/` (Mac Studio runner),
`STUDIO_JOBS.md`, `NOTES.md`.

---------------------------------------------------------------------------------------------------------------------------------

## 1. The exact engine `bx` (src/bx.cpp)  — COMPUTED / validated

Same mathematical object as `structure/bauto.cpp` (re-derived from the mirror `Bstep`, not trusted): scan the B coefficients by position
k = 0,1,2,...; the cut state between positions k-1 and k is (L, H, Y), each indexed by the p times t:
  * L[t] = carry into position k at time t (determined by the lower positions),
  * H[t] = carry that position k must "pass down" (demand; guessed from above),
  * Y[t] (only at overflow times g_t = 1) = (x_t[k-1] + H_t[k]) mod b  (partner digit shifted by the overflow; Y at k=0 is the leading 1).
A position is a choice of x_0[k] in 0..2b-2 (x_t[0] != 0) and carry guesses c_t in {0,1}; the p-step recursion
x_{t+1} = (x_t + L_t) mod b + (g_t ? Y_t : (x_t + c_t) mod b)  must close (x_p = x_0) and satisfy floor((x_t + c_t)/b) = H_t.
New cut state: L'_t = [x_t + L_t >= b], H'_t = c_t, Y'_t = (x_t + c_t) mod b.   Start (L,H,Y) = (0, g, 1).
Accept (neutral band above): L_t + H_t = 1 and Y_t = (b-1) L_t for all overflow t  (then the carry stream is e = L).
BFS over all cut states, de-duplicated over ALL depths, until saturation: the reachable set is finite, so
`EXHAUSTED` = no B-cycle with overflow word g for ANY width and ANY e;  `ACCEPT` lists every accepted e (`e=...@d`: d = position at which the accepting cut state first appears = width of the cycle; the `depth=` field is the saturation depth of the BFS);
`CAPPED_states|time|mem` = nothing claimed except `wdone` = number of B-widths (positions) completely processed.

Differences from bauto: (1) NO key truncation: key = bit-packed (L,H,Y) in KW 64-bit words (KW=2: p<=32, G*4<=64 bits, or mixed-radix Y; KW=3: p<=59) and the
open-addressing table compares the full key (exact set); (2) backward viability DP over the p-step ring makes successor enumeration output-sensitive
(measured: ~1.2 emitted successors per expansion, ~2.4 us per expansion; ~10x faster than bauto2); (3) quotient by the cyclic time shift for
imprimitive g = u^m (canonical minimum over the m rotations of (L,H,Y); reachable ORBITS, same ACCEPT/EXHAUSTED answer, states/m);
(4) caps (states, seconds), depth cap, word-list mode; (5) a table of 2^k entries of 16 B (24 B for KW=3), load factor <= 0.6.

### Validation (all COMPUTED, scripts in `py/`)
* `cmp_bauto.py`: bx vs W1's `bauto2` — identical #states and identical accepted-e sets on EVERY necklace word p=2..14 (base 10), p=2..8 for 15 bases (2..32),
  p=9,10 for bases 2,3,4,8,11,16,17,26, and p=15,16,17,19 (base 10, ALL necklaces incl. dead ones: 7712 words at p=17, 27596 at p=19; 0 mismatches; capped words skipped).
  `cmp_sample.py` (bauto2 `-g WORD` vs bx on random F1 survivors, identical #states for m=1 words and same accept/no-accept): p=19 200 words, p=20 300, p=21 30, p=22 25, p=23 40, p=24 40 — all identical
  (bx is 10x faster at p=20 and ~70x at p=24).
  bx (KW=2), bx3 (KW=3) and a clang++ build give identical output on 400 random p=31 survivors (resp. 200 random p=36 survivors).
* Re-found known streams: base 10 p11 (g=00001110001, e=00111010011: accepted at position/width 29, BFS saturates at depth 59 with 18,061 states), p12 (g=(0001)^3, e=101101010010 and its two 4-step rotations: accepted at width 53, saturation depth 71, 45,571 quotient states),
  base 11 (g=001, e=001/011), 17 (g=100001, e=100000), 26 (g=01, e=01), 20 (g=00010001), and 2,4,8,16,32 (g=10,100,1000,10000,100000).
* `verify_ext.py`: every witness of `bx -w` is replayed (i) with the Lean-mirror `Bstep` (B_{t+1}=Bstep(B_t), e1/gam streams equal e/g, B_p=B_0) and
  (ii) in real integers (one reverse-and-add per step with a one-digit centre, pair word of N_{t+1} starts with B_{t+1} + neutral band).
* `brute_model.py` (independent check of the MODEL, completeness direction): all trimmed coefficient lists of length <= L, iterate the mirror map F, take the
  periodic orbits that stay in the box, and require bx to ACCEPT their (g,e): base 3 (L=9): 1 orbit (p=5 g=11100) OK; base 4 (L=6): 2 orbits (p=3) OK; base 2 (L=12): OK;
  bases 5, 10, 11 (small L): no orbits, bx agrees. `missing: 0` in every run.

---------------------------------------------------------------------------------------------------------------------------------

## 2. Necessary filters on g — PAPER PROOF (scripts re-check every edge)

### 2.1 The first-coordinate automaton (position k = 0)
At k = 0 the cut state is (L,H,Y) = (0,g,1).  Write q_t = x_t[0] = B_t[0] (the leading coefficient; B is trimmed so q_t in 1..2b-2) and r_t = c_t = H_t[1] in {0,1}
(the carry arriving from the unseen higher positions: FREE).  The engine recursion at position 0 reads
  floor((q_t + r_t)/b) = g_t,        q_{t+1} = (q_t mod b) + ( g_t ? 1 : (q_t + r_t) mod b ).
* g_t = 0: q_t + r_t <= b-1, so q_{t+1} = 2 q_t + r_t.
* g_t = 1: q_t + r_t >= b,     so q_{t+1} = (q_t mod b) + 1.
This is a nondeterministic automaton on the 2b-2 = 18 states 1..18 with 36 edges (q,r) (`py/fc_graph.py`; targets stay in 1..18: for g=0, 2q+r <= 2(b-1)).
**Filter F1** (sound, any width): if a B-cycle with overflow word g exists, (q_t) is a closed walk of length p labelled g, i.e. g (cyclically) is accepted by the NFA.
F1 does not depend on the width, nor on e, nor on any other position.  `fc_enum` enumerates the cyclic (necklace) words accepted: counts in `out/fc_counts_b10.txt`
(they reproduce every count quoted by the other agents: p16 95, p18 207, p20 449, p23 1502, p24 2268, p25 3428 with G=7:13, 8:303, 9:1314, 10:1455, ...).

### 2.2 Consequences (each is a statement about all closed walks, hence about all B-cycles)
* (a) **runs**: no 00000 (zero-runs <= 4): after j consecutive g=0 steps q >= 2^j, and the (j+1)-th needs q <= b-1 = 9, so j <= 4 (q = 1,2,4,8 then 16 forces g=1).
  One-runs have length <= 3 (the only 1-run of length 3 is q = 18,9,10; computed by `py` on the edge list).  Hence g is a necklace over blocks 1,01,001,0001,00001 etc.
* (b) **p <= 4G** (at least one 1 in every 4 steps on average): potential f(q) = floor(log2 q) satisfies f(2q+r) = f(q)+1 on g=0 edges, and f decreases by at most 3 on g=1
  edges (q in 9..15 has f <= 3 and q' >= 1; q in 16..18 goes to q' in 7..9 with f(q') >= 2).  Summing along a closed walk: (p-G)*1 <= G*3.
  Explicit integer potential used by `verify_potentials.py` (phi(q2)-phi(q) <= 4g-1 on all 36 edges, so 0 <= 4G-p):
  phi = [q=1:4, 2:3, 3-5:2, 6-10:1, 11-18:0].
* (c) **2G <= p** (no more than half the steps overflow): psi(q2)-psi(q) >= 2g-1 on all 36 edges, so 0 >= 2G-p, with
  psi = [q=1:3, 2:2, 3:2, 4-9:1, 10:2, 11-18:0].  (Hand check: g=0 edges drop psi by at most 1; g=1 edges raise it by at least 1.)
* (d) **equality cases** (`critical.py`): the edges lying on cycles of mean exactly 1/2 are (8,17,0),(17,8,1),(9,18,0),(18,9,1): so 2G = p forces g = (01)^{p/2};
  the edges on cycles of mean exactly 1/4 are 1->2->5->10->1 (labels 0,0,0,1): so p = 4G forces g = (0001)^{p/4}.  Karp min/max cycle means: 1/4 and 1/2.
These agree with the Lean-verified 2G <= P <= 4G (#364) — here re-derived independently from the engine's own recursion — and add the run bounds.

### 2.3 Soundness check on known exteriors (COMPUTED, `py/known_check.py`)
The F1 automaton (built for base b with 2b-2 states) accepts the known streams: base 10 p11, p12; base 11 g=001, 001001; 17 g=100001; 26 g=01; 20 g=00010001, 0001;
2, 4, 8, 16, 32 (g=10,100,1000,10000,100000); base 3 g=11100, 10.  All 15 pass.

### 2.4 What was tried and NOT used as a proven filter
* "Top lemma" (observation only): in all nine known exterior witnesses the B-length at every overflow time is strictly below the maximal width (`toplemma.py`).
  No proof, not used as a filter.
* Second-coordinate (K=2) prefilter: the first two layers of `bx` ARE the exact pair automaton; measured on 300 random p=36 survivors of F1:
  289/300 words are EXHAUSTED already after depth 2 (`-maxdepth 2`), 297/300 after depth 3; layers 1-2 take 5.2 of 9.8 s.  So a pair-automaton prefilter would remove 96% of F1
  survivors at p=36 but the engine does this work itself in ~17 ms/word; a stand-alone version was NOT implemented (it would need the width < 2 cases handled separately to stay sound).
* Forbidden-factor idea (relax the p-step ring closure to a finite window of g: `bx -seg`, lists `lists/seg_m*.txt`): implemented, NOT evaluated at scale (abandoned after a first trial, nothing is claimed).
* Last-coefficient (top of B) automaton: built and found useless.  At the top position H = 1-e is forced and L (carry from below) and the partner digit Y are free, so the
  g=1 edges are almost unconstrained and the g=0 edges only give x -> 2x+1 style growth plus a fixed point x=9=b-1 (position inside the neutral band, i.e. B shorter than the max width),
  which allows arbitrarily long zero-runs: no run or density bound beyond F1.
* Cycle-mean bound from the pair automaton (K=2,3 heads): the (01)^4 cycle (p=8) survives the first three layers and BFS needs depth 88 to kill it, so the K=2,3 graphs still have max mean 1/2
  and the known p12 stream keeps min mean 1/4: no improvement over 1/4 <= G/p <= 1/2 from small K.  Observation (COMPUTED, k <= 15): the BFS for (01)^k dies at depth 3 unless 4 | k
  (k=4: dies at depth 88 with 61,249 states; k=8 and k=12: UNDECIDED at 40M states; k=16 (p=32): UNDECIDED), i.e. the only live words with 2G = p seem to be (01)^{4j}, p = 8j.

### 2.5 Pair/triple-coordinate automata and the critical families (COMPUTED finite-graph statements, `py/khead.py`, `py/khead_family.py`)
The first K layers of `bx` are the exact K-head time-domain graph: nodes (x_t[0..K-1]), edge label g_t, one free bit h = H_t[K] (carry from the unseen positions >= K).
It is a necessary condition for every B-cycle of width >= K (K=1 gives the 36-edge F1 automaton above; checked: 36 edges).  `khead_family.py PATTERN` grows the graph restricted to a periodic label pattern.
* **Theorem (finite-graph check, all k): 2G = p implies 8 | p.**  For K=3 and the label pattern 01 the pattern graph has exactly ONE cyclic strongly connected component: a single 8-cycle, so closed walks labelled (01)^k exist iff 4 | k.
  On it the three lowest coefficients are forced (columns B_t[0..2], t = 0..7, g = 0,1,0,1,...): (8,12,9) (17,5,0) (8,13,5) (17,6,11) (8,14,8) (17,8,17) (8,16,16) (17,13,14); the (9,18) branch of F1 dies.
  Widths 1 and 2 are covered separately (accepting-top graphs with 9 and 171 edges, deterministic h = 1-L, Y condition at overflow times): neither contains a closed walk labelled (01)^* (nor (0001)^*).
  Consistent with the engine (BFS of (01)^k dies at depth 3 for every k <= 15 with 4 not dividing k).
* Growth of the family graphs (number of nodes on cycles, K = 3..9): pattern 01: 8, 65, 388, 2191, 7556, 36479, 175057 (a giant SCC of period 8 survives: x5 per extra coordinate);
  pattern 0001: 62, 161, 332, 795, 2011, 7879, 23243 (giant SCC of period 4 plus small SCCs of periods 8, 12, 16: x3 per coordinate).  So no small K-head filter can decide these families:
  the position BFS must go on until the p-step closure x_p = x_0 kills the branches, which is why (01)^{4j} and (0001)^m words have 10^8+ states.

---------------------------------------------------------------------------------------------------------------------------------

## 3. Cost model (COMPUTED on this 2-core box, nice 10, `bin/bx`/`bin/bx3`, cap 300k states)
Mean time per F1 survivor (uniform random sample of 300 words): p=33 6.9 ms, 34 12.9, 35 13.0, 36 19.3, 38 33.1, 40 47.5 ms; capped fraction at 300k states 0.3-0.7%.
Pass 1 (cap 300k) over ALL F1 survivors: p25 6 s, p26 18 s, p27 23 s, p28 44 s, p29 81 s, p30 ~150 s, p31 245 s, p32 371 s (single core).
Frontier growth is the only hard part: the residue words (a few per mille) are NEAR-CRITICAL (G/p close to 1/2: long (10)^m runs separated by 00/000/111, or (1000)^m blocks),
where the live frontier does not die quickly: e.g. p18 g=001010101001010101 keeps 5e4-2.3e5 live cut states per layer through depth 38 and beyond (`bx -v`: 3.0M visited states at depth 38),
so the total visited set is (frontier) x (number of layers until the last live state dies, ~60-100 positions for these words), i.e. tens of millions - hence cap 3M is not enough but 40M may be.

---------------------------------------------------------------------------------------------------------------------------------

## 3b. B-level uniqueness of accepted streams, and the other engine modes  (COMPUTED)
* `bx -count D -nosym`: layered DP counting position-choice histories (x_0[k], carries) that end in an accepting cut state; a history = one complete B-cycle (the carries are determined by B).
  p11 (g=00001110001): exactly ONE history for e=00111010011 at every depth >= 29 (so exactly one B-cycle); p12 ((0001)^3): exactly ONE history for each of the three accepted e's
  (101101010010, 010100101011, 001010110101: the three 4-step rotations), first at width 53.  So for the known streams B is determined by (g,e).
  p22 = (p11 word)^2: the quotient BFS reports the single accepted stream e11e11; its B-level count (`run_count.sh`) was NOT run (session ended): the B-level uniqueness of the p22 repetition is UNDECIDED; B-uniqueness is shown only for p11 and p12.
* `bx -layered D`: layer-by-layer BFS WITHOUT global de-duplication (memory O(layer)); exact EXHAUSTED when a layer becomes empty, otherwise only "no cycle of width < D".
  It does NOT help on the hard words: the layers keep growing (p21 word 0.8M states at layer 30, (01)^8 0.37M at layer 30), and for (01)^4 the layers never empty (recurrent states).
* `bx1/bx/bx3` = KW 1/2/3 builds; `bx1` (8-byte keys) fits only keys <= 63 bits, e.g. (01)^8.
* **Symbolic (BDD) cross-check and why it does not decide the hard words** (COMPUTED; `py/symacc.py`, which drives a verbatim copy of W3's CUDD/`dd` encoding `py/symfwd_w3.py`
  of the same position automaton; ACC set built from `bx.cpp accepting()`; run with W3's venv).  Forward symbolic BFS vs the explicit engine (`bx -nosym`):
  states 9, 57, 2193 for g = 0001001001, 000100010011, 0010101010010101 are EXACTLY equal (EXHAUSTED at depth 2, 3, 5 in both); p11 hits ACC at level 29 (= bx `e=...@29`);
  p18 SQ1 `001010101001010101` EXHAUSTED at depth 57 with 7,599,801 visited states = 2 x 3,800,689 (bx quotient states) - 1,577 (fixed points of the order-2 time shift) - an independent exact
  re-derivation of the SQ1 verdict by a second engine (1.0M BDD nodes, 30 s).  Backward cone from ACC for p11: 1.04M states in 4.0e5 nodes (2.6x), ACCEPT at depth 28.
  Compression of the forward visited set as an ordered MDD over time levels (`bx -mdd`, `MDDV` lines; symbol = (L_t,H_t,Y_t)): p21 word 1.7M states -> 30.7k MDD nodes (56x),
  SQ1 (no quotient) 1.76M -> 63.6k (28x); node count grows linearly with the state count.  One MDD node = ~5 BDD nodes, so this agrees with the ~6x BDD compression measured by W3:
  a 1e9-state visited set (the order of magnitude of the open words) would need 1e8 BDD nodes (> 2.5 GB), so symbolic reachability is NOT a way to decide (01)^8, p21, (0001)^6, (01)^12 here.

---------------------------------------------------------------------------------------------------------------------------------

## 4. Results (base 10; generated from the census DB by `py/make_results.py`, i.e. every number below is a program output)

**Statement (COMPUTED + PAPER PROOF F1).**  A cyclic overflow word g of length p with a B-cycle must be accepted by the first-coordinate NFA (section 2, PAPER PROOF).
For EVERY p <= 32 all F1 survivors were run through the exact engine with the caps shown; every survivor is EXHAUSTED (no B-cycle of any width, any e) EXCEPT
  * ACCEPT: p11 (g=00001110001), p12 (g=(0001)^3) and p22 (g = the p11 word twice; the ONLY accepted stream is e11e11, i.e. the repetition) — nothing else accepted;
  * the UNDECIDED words in the last table (CAPPED: nothing is claimed for them, they may or may not carry an exterior).
Hence: **no new primitive decimal exterior stream (B-cycle) exists with p <= 32 except possibly for the listed undecided words; every p in 2..15, 17..20, 22, 23 is completely decided (the open words with p <= 24 are p16 (01)^8, p21 001001010101001010101, p24 (0001)^6 and (01)^12).**
Not claimed: anything about centres, anything for p >= 33 (first-pass numbers for p = 33 may be appended below), the B-level uniqueness for imprimitive accepted words beyond the counts quoted in section 3b.

| p | all necklaces | with 2G<=p<=4G | F1 survivors (NFA) | EXHAUSTED | ACCEPT | CAPPED = UNDECIDED |
|--:|--:|--:|--:|--:|--:|--:|
| 2 | 3 | 1 | 1 | 1 | 0 | 0 |
| 3 | 4 | 1 | 1 | 1 | 0 | 0 |
| 4 | 6 | 3 | 2 | 2 | 0 | 0 |
| 5 | 8 | 2 | 2 | 2 | 0 | 0 |
| 6 | 14 | 7 | 3 | 3 | 0 | 0 |
| 7 | 20 | 8 | 4 | 4 | 0 | 0 |
| 8 | 36 | 21 | 5 | 5 | 0 | 0 |
| 9 | 60 | 24 | 9 | 9 | 0 | 0 |
| 10 | 108 | 60 | 10 | 10 | 0 | 0 |
| 11 | 188 | 87 | 14 | 13 | 1 | 0 |
| 12 | 352 | 208 | 22 | 21 | 1 | 0 |
| 13 | 632 | 286 | 28 | 28 | 0 | 0 |
| 14 | 1,182 | 679 | 45 | 45 | 0 | 0 |
| 15 | 2,192 | 1,056 | 61 | 61 | 0 | 0 |
| 16 | 4,116 | 2,418 | 95 | 94 | 0 | 1 |
| 17 | 7,712 | 3,666 | 130 | 130 | 0 | 0 |
| 18 | 14,602 | 8,424 | 207 | 207 | 0 | 0 |
| 19 | 27,596 | 13,532 | 292 | 292 | 0 | 0 |
| 20 | 52,488 | 30,556 | 449 | 449 | 0 | 0 |
| 21 | 99,880 | 48,610 | 665 | 664 | 0 | 1 |
| 22 | 190,746 | 109,791 | 1,000 | 999 | 1 | 0 |
| 23 | 364,724 | 180,424 | 1,502 | 1,502 | 0 | 0 |
| 24 | 699,252 | 403,670 | 2,268 | 2,266 | 0 | 2 |
| 25 | 1,342,184 | 661,270 | 3,428 | 3,428 | 0 | 0 |
| 26 | 2,581,428 | 1,478,637 | 5,181 | 5,181 | 0 | 0 |
| 27 | 4,971,068 | 2,470,804 | 7,865 | 7,863 | 0 | 2 |
| 28 | 9,587,580 | 5,492,374 | 11,939 | 11,936 | 0 | 3 |
| 29 | 18,512,792 | 9,181,140 | 18,130 | 18,128 | 0 | 2 |
| 30 | 35,792,568 | 20,388,094 | 27,641 | 27,632 | 0 | 9 |
| 31 | 69,273,668 | 34,521,600 | 42,052 | 42,040 | 0 | 12 |
| 32 | 134,219,796 | 76,360,870 | 64,249 | 64,227 | 0 | 22 |

By (p,G): decided/F1-survivors, [c] = capped words

* p=16: G4: 1/1; G5: 14/14; G6: 54/54; G7: 25/25; G8: 0/1 [1c]
* p=17: G5: 8/8; G6: 58/58; G7: 60/60; G8: 4/4
* p=18: G5: 3/3; G6: 57/57; G7: 111/111; G8: 35/35; G9: 1/1
* p=19: G5: 1/1; G6: 38/38; G7: 148/148; G8: 101/101; G9: 4/4
* p=20: G5: 1/1; G6: 23/23; G7: 164/164; G8: 219/219; G9: 41/41; G10: 1/1
* p=21: G6: 11/11; G7: 145/145; G8: 343/343; G9: 161/162 [1c]; G10: 4/4
* p=22: G6: 4/4; G7: 107/107; G8: 445/445; G9: 392/392; G10: 51/51; G11: 1/1
* p=23: G6: 1/1; G7: 64/64; G8: 463/463; G9: 731/731; G10: 239/239; G11: 4/4
* p=24: G6: 0/1 [1c]; G7: 32/32; G8: 415/415; G9: 1077/1077; G10: 685/685; G11: 57/57; G12: 0/1 [1c]
* p=25: G7: 13/13; G8: 303/303; G9: 1314/1314; G10: 1455/1455; G11: 339/339; G12: 4/4
* p=26: G7: 4/4; G8: 194/194; G9: 1348/1348; G10: 2442/2442; G11: 1125/1125; G12: 67/67; G13: 1/1
* p=27: G7: 1/1; G8: 100/100; G9: 1184/1184; G10: 3385/3385; G11: 2728/2728; G12: 461/463 [2c]; G13: 4/4
* p=28: G7: 1/1; G8: 46/46; G9: 885/886 [1c]; G10: 3972/3972; G11: 5166/5166; G12: 1792/1794 [2c]; G13: 73/73; G14: 1/1
* p=29: G8: 16/16; G9: 570/570; G10: 3987/3989 [2c]; G11: 8071/8071; G12: 4877/4877; G13: 603/603; G14: 4/4
* p=30: G8: 5/5; G9: 316/317 [1c]; G10: 3479/3479; G11: 10641/10643 [2c]; G12: 10397/10397; G13: 2711/2716 [5c]; G14: 82/83 [1c]; G15: 1/1
* p=31: G8: 1/1; G9: 148/148; G10: 2624/2625 [1c]; G11: 12091/12094 [3c]; G12: 18055/18056 [1c]; G13: 8353/8357 [4c]; G14: 764/767 [3c]; G15: 4/4
* p=32: G8: 1/1; G9: 59/59; G10: 1736/1736; G11: 11942/11943 [1c]; G12: 26574/26581 [7c]; G13: 19839/19842 [3c]; G14: 3990/3997 [7c]; G15: 86/89 [3c]; G16: 0/1 [1c]

Accepted streams (all are repetitions of the known p11 / p12 streams, see py/check_accepts.py):

* p=11 g=00001110001 status=ACCEPT e=['00111010011'] states=18061 depth=59
* p=12 g=000100010001 status=ACCEPT e=['101101010010'] states=45571 depth=71
* p=22 g=0000111000100001110001 status=ACCEPT e=['0011101001100111010011'] states=13191834 depth=88

UNDECIDED (CAPPED) words; `wdone` = B-positions completely processed (no cycle of width <= wdone); cap in visited states (quotient states if m>1):

| p | G | word g | m | cap | states | depth reached | wdone |
|--:|--:|---|--:|--:|--:|--:|--:|
| 16 | 8 | `0101010101010101` | 8 | 40,000,000 | 40,003,127 | 70 | 69 |
| 21 | 9 | `001001010101001010101` | 1 | 40,000,000 | 40,000,043 | 82 | 81 |
| 24 | 6 | `000100010001000100010001` | 6 | 40,000,000 | 40,000,154 | 47 | 46 |
| 24 | 12 | `010101010101010101010101` | 12 | 40,000,000 | 40,001,669 | 16 | 15 |
| 27 | 12 | `000100010101010101010100111` | 1 | 40,000,000 | 40,037,665 | 16 | 15 |
| 27 | 12 | `001010101001010101001010101` | 3 | 40,000,000 | 40,033,969 | 13 | 12 |
| 28 | 9 | `0000111000100010001100010001` | 1 | 40,000,000 | 40,000,713 | 34 | 33 |
| 28 | 12 | `0000101010101001010100100111` | 1 | 40,000,000 | 40,018,449 | 13 | 12 |
| 28 | 12 | `0000111000011100001110000111` | 4 | 40,000,000 | 40,026,827 | 33 | 32 |
| 29 | 10 | `00001110001000110001000110001` | 1 | 40,000,000 | 40,000,897 | 21 | 20 |
| 29 | 10 | `00010001100010010001010100101` | 1 | 40,000,000 | 40,045,305 | 15 | 14 |
| 30 | 9 | `000100010001000110001000100011` | 1 | 40,000,000 | 40,003,745 | 11 | 10 |
| 30 | 11 | `000010101001010001000011100011` | 1 | 40,000,000 | 40,004,817 | 20 | 19 |
| 30 | 11 | `000100100011000110001100010011` | 1 | 40,000,000 | 40,022,817 | 10 | 9 |
| 30 | 13 | `000011100001110000111000100111` | 1 | 40,000,000 | 40,021,057 | 21 | 20 |
| 30 | 13 | `000100010101010101001010100111` | 1 | 12,000,000 | 12,022,881 | 9 | 8 |
| 30 | 13 | `001001010100100101010101010101` | 1 | 12,000,000 | 12,200,193 | 5 | 4 |
| 30 | 13 | `001001010100101010101001010101` | 1 | 12,000,000 | 12,066,305 | 4 | 3 |
| 30 | 13 | `001001010101001001010101010101` | 1 | 12,000,000 | 12,036,481 | 6 | 5 |
| 30 | 14 | `001010101010101001010101010101` | 2 | 12,000,000 | 12,094,291 | 8 | 7 |
| 31 | 10 | `0001000100011000100010001100011` | 1 | 12,000,000 | 12,036,289 | 6 | 5 |
| 31 | 11 | `0000111000011100010001000110001` | 1 | 12,000,000 | 12,030,529 | 9 | 8 |
| 31 | 11 | `0000111000011100010001100010001` | 1 | 12,000,000 | 12,097,281 | 11 | 10 |
| 31 | 11 | `0001000101010010100011000100011` | 1 | 12,000,000 | 12,049,249 | 6 | 5 |
| 31 | 12 | `0001000101010010101001010100101` | 1 | 12,000,000 | 12,042,849 | 7 | 6 |
| 31 | 13 | `0000101010010011100010011100011` | 1 | 12,000,000 | 12,072,961 | 5 | 4 |
| 31 | 13 | `0000101010100100101010100100111` | 1 | 12,000,000 | 12,090,881 | 5 | 4 |
| 31 | 13 | `0000111000110001000101010100111` | 1 | 12,000,000 | 12,012,865 | 5 | 4 |
| 31 | 13 | `0001000101010010011100010010111` | 1 | 12,000,000 | 12,327,809 | 8 | 7 |
| 31 | 14 | `0000101010101010100111000100111` | 1 | 12,000,000 | 12,014,593 | 7 | 6 |
| 31 | 14 | `0010010101010101010101010010101` | 1 | 12,000,000 | 12,018,049 | 3 | 2 |
| 31 | 14 | `0010101001010100101010101010101` | 1 | 12,000,000 | 12,014,721 | 6 | 5 |
| 32 | 11 | `00010001000110001000110001100011` | 1 | 12,000,000 | 12,061,057 | 6 | 5 |
| 32 | 12 | `00001010100101000100010101001011` | 1 | 12,000,000 | 12,004,225 | 6 | 5 |
| 32 | 12 | `00001010100101010010100010000111` | 1 | 12,000,000 | 12,000,801 | 5 | 4 |
| 32 | 12 | `00001011100010100010101001010001` | 1 | 12,000,000 | 12,085,825 | 4 | 3 |
| 32 | 12 | `00001110000111000101001000110001` | 1 | 12,000,000 | 12,006,513 | 12 | 11 |
| 32 | 12 | `00001110001100010000111000110001` | 2 | 12,000,000 | 12,006,761 | 6 | 5 |
| 32 | 12 | `00010001000110001000101010100111` | 1 | 12,000,000 | 12,028,033 | 4 | 3 |
| 32 | 12 | `00010001001001010101001010100101` | 1 | 12,000,000 | 12,023,233 | 3 | 2 |
| 32 | 13 | `00001010101001010100101000100111` | 1 | 12,000,000 | 12,050,145 | 8 | 7 |
| 32 | 13 | `00010001010101010101001010100101` | 1 | 12,000,000 | 12,070,785 | 5 | 4 |
| 32 | 13 | `00010101010010101001001010100101` | 1 | 12,000,000 | 12,057,729 | 5 | 4 |
| 32 | 14 | `00001010100101010101010011100011` | 1 | 12,000,000 | 12,103,425 | 8 | 7 |
| 32 | 14 | `00001010101010011100001110000111` | 1 | 12,000,000 | 12,026,881 | 9 | 8 |
| 32 | 14 | `00001010101010101001001110000111` | 1 | 12,000,000 | 12,012,033 | 6 | 5 |
| 32 | 14 | `00001110001001110000111000100111` | 2 | 12,000,000 | 12,032,161 | 7 | 6 |
| 32 | 14 | `00100101010101001001010101010101` | 1 | 12,000,000 | 12,002,305 | 4 | 3 |
| 32 | 14 | `00100101010101010010010101010101` | 2 | 12,000,000 | 12,032,021 | 5 | 4 |
| 32 | 14 | `00100101010101010100101010010101` | 1 | 3,000,000 | 3,006,977 | 2 | 1 |
| 32 | 15 | `00001010101010101010101010100111` | 1 | 3,000,000 | 3,019,777 | 2 | 1 |
| 32 | 15 | `00100101010101010101010101010101` | 1 | 3,000,000 | 3,440,641 | 1 | 0 |
| 32 | 15 | `00101010010101010101010101010101` | 1 | 3,000,000 | 3,014,849 | 3 | 2 |
| 32 | 16 | `01010101010101010101010101010101` | 16 | 3,000,000 | 6,816,545 | 3 | 2 |

(total 54 undecided words)

<!-- END RESULTS -->

---------------------------------------------------------------------------------------------------------------------------------

## 5. Reproduction
```
studio/build.sh                      # bin/bx1 bin/bx bin/bx3 bin/fc_enum
bin/fc_enum 10 2 40 -list lists      # survivor lists lists/fc_b10_p{p}_G{G}.txt  (counts: out/fc_counts_b10.txt)
python3 py/census.py 10 25 --cap 3000000 --sec 40          # resumable census of all F1 survivors of p=25 (DB out/db_b10.jsonl)
python3 py/summarize.py 10 --g | less                      # funnel by p and G, capped words
python3 py/make_results.py                                 # markdown tables (this section)
python3 py/check_accepts.py out/db_b10.jsonl               # classify accepted streams: KNOWN p11/p12 repetition or NEW
python3 py/cmp_bauto.py 10 17 ; python3 py/cmp_sample.py 22 25 3 ; python3 py/brute_model.py 3 9 20 ; python3 py/known_check.py
python3 py/verify_potentials.py ; python3 py/critical.py 10 1 2 ; python3 py/critical.py 10 1 4     # section 2
```
Single-word runs: `bin/bx 10 -g WORD [-cap N] [-sec S] [-v] [-w] [-first] [-nosym]`; `-count D` counts B-histories per accepted e (layered, use with `-nosym`), `-layered D` runs without global de-duplication.

