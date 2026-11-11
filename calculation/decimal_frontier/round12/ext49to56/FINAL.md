# Round 12, agent r12e: r12b's UNDECIDED clock words and the F1 census T = 49..56 with the exact K-head filter

Run on the Studio in ~/p196_run/r12e; paths below are relative to this directory. r12b (Theorem K, khx, kh2): `../ext41to48/`.
Labels: **COMPUTED** (exact program output, reproducible with the files
listed), **PAPER PROOF** (argument written out, here or in r12b `FINAL.md` §2/§6), **UNDECIDED** (capped; nothing claimed).
Nothing here is LEAN-VERIFIED. **Nothing is claimed about 196.**
Tables: `out/final_table_r12e3.md`, `out/final_open_r12e3.txt`, `out/final_surv5556_r12e3.md` (earlier drafts not shipped).

**STATUS (2026-11-08T09:56Z, FINAL; finished by the main session after r12e3 was stopped at 08:25Z; every job has ended).** All counts and
tables below are regenerated from the final outputs. Census T = 49..56 complete (counts = CSV for every T), 12 census words UNDECIDED,
p47, (p21)^2 and the T = 52 word decided by long runs with independent confirmations (section 4).

## 0. Results

1. **Census T = 49..54 (COMPUTED + Theorem K).** All 2,184,221,864 F1 necklaces of lengths 49..54 were run (primitive and
   imprimitive; every total and primitive count equals `data/f1_b10_p33_60.csv`). 2,184,221,857 words DIE (pass 1, deep pass 1,
   deep pass 2 or the long run): for each of them there is **no 9-wire exterior and no uniform-band template** with that clock
   (any width, any left-end height, any band value cycle, any phase). **7 words are UNDECIDED** (section 6); T = 49, 50 and 52
   are complete with 0 UNDECIDED. No word of T = 49..54 carries a known stream (no repetition of p11 or N12 has these lengths).
1b. **Decisive run: T = 52 0001000100010001000100011000100011000100011000100011 DIES at K = 1744** (COMPUTED, khxt -exactset
   -top -inv, 5,139 s, widest level 109.6M). By Theorem K: no 9-wire exterior and no uniform-band template with this clock.
   Exact set 1.1M at K = 1600, 51K at 1700, 445 at 1743, 0 at 1744; TOP99/TOPUU never hit. Confirmed (section 4.3): khxt_b
   rerun identical at every level 1..1710, kh2s (independent code) from level 1710 reproduces every count and dies at K = 1744.
2. **Census T = 55, 56 (COMPUTED + Theorem K):** T = 55: 1,286,235,064 words (= CSV; primitive 1,286,235,048 = CSV), 42 pass-1
   survivors: 38 DIE in deep pass 1, 1 in deep pass 2 (K = 759), p11^5 is the known p11 stream (TOP99 hit at K = 31, kept 22 per level; extraction
   `out/hits/` VERIFIED by exact integers: widths 25..29), 2 UNDECIDED. T = 56: 1,989,587,605 words (= CSV; primitive 1,989,575,663 = CSV), 74 pass-1
   survivors: 69 DIE in deep pass 1, 2 in deep pass 2, 3 UNDECIDED (incl. (01)^28).
3. **p47 = 00010001000110001100010010001010100101000100011 DIES at K = 763** (COMPUTED, three runs, two independent codes).
   By Theorem K: no 9-wire exterior and no uniform-band template with this clock (r12b had it UNDECIDED at K = 588).
4. **(p21)^2 = (001001010101001010101)^2 DIES at K = 2787** (COMPUTED, khxt run on the root pattern p21 with L = 42, Lemma K6).
   By Theorem K: no 9-wire exterior and no uniform-band template with clock (p21)^2 (r12b: UNDECIDED at K = 671).
   Confirmed (section 4.2): khxt_b rerun identical to the original at every level 1..2750, kh2s (independent code) from level 2750
   reproduces every count and dies at K = 2787.
5. **p34 = 0001010101001001010101001010100101: UNDECIDED.** khxt -exactset survives to K = 2412 (time cap 15,000 s), exact set
   6.56M nodes and growing. No TOP99/TOPUU hit up to K = 2412.
6. **No TOP99 or TOPUU hit on any open word** in any run of this round (0 new exteriors, 0 new streams). The hit-extraction path
   (`py/extract_hit.py` -> r12b `verify_ext.verify`, exact integers) is validated on p11 and N12 (both VERIFIED).
7. **Independent checks (COMPUTED):** kh2 -exact (r12b's independent code) reproduces the death level of 2,153 pass-1 deaths
   of T = 49..54 (about 25 sampled per shard + every pass-1 death with K >= 40): 2,153 SAME, 0 DIFF, 0 NOVERDICT. T = 55: 501 SAME, T = 56: 746 SAME (samples + all deaths with K >= 40); deep deaths: T = 49..54 73 + 8 SAME (5 more without verdict inside the time limit), T = 55/56 42 SAME; 0 DIFF anywhere (`ctrl/kh2_*.out`). The WL hash
   (khxt -inv) never repeats within the p34, p47, (p21)^2 and decisive runs, so no Theorem-U stabilisation was seen.
8. Not decided by this round: (01)^20, (01)^24 (G_K(01) keeps 8-periodic closed walks at every K, so Theorem K can never
   apply), N12^4 = (0001)^12 (carries N12, so khx can never die; P(12) stays open). These stay UNDECIDED as in r12b.

**What this round changes.** r12b left 6 words of period 34..48 UNDECIDED (p34, (01)^20, (p21)^2, p47, N12^4, (01)^24); two of
them, p47 and (p21)^2, are now decided by Theorem K. The F1 census, complete for T <= 48 after r12b, is extended to T = 49..54
(complete except 7 UNDECIDED words; the hardest T = 52 word died at K = 1744 in the decisive run) and T = 55/56 (section 3). No exterior, stream or certificate was found; this is exclusion
work, not a Lychrel certificate.

## 1. What a DIES means (PAPER PROOF, r12b FINAL.md section 2) and what it does not

- **Theorem K (r12b).** If the K-head filter (khx, khxc, khxt, any options) prints DIES at level K for pattern g and length L,
  there is no 9-wire exterior and no uniform-band template (any band of Sigma_U, any phase, any left-end height) with clock
  g^{L/|g|}, of any width. Proof: Lemmas K1-K5 (reach paths are closed L-walks of G_K; the kept set contains every node on a
  closed L-walk), on top of Theorem B, Theorem B' and Lemma X (`round11/premiseB/PROOF.md`) and Lemmas A1-A3
  (`three_divides_r/PROOF.md`). **Lemma K6:** for g = h^m, running the root pattern h with L = m|h| is a valid test for g.
- khxt `-exactset` keeps EXACTLY the nodes of the candidate graph that lie on a closed L-walk (per-source forward/backward
  bitsets); this set contains every node of G_K on a closed L-walk (Lemma K5 induction), so Theorem K applies unchanged.
  Code review (r12e2): matches the definition; no defect found. Node counts equal kh2 -exact at every level
  K = 1..46 on p34 (COMPUTED).
- **TOP99/TOPUU (khxt -top; r12e).** A closed L-walk inside TOP99_K (top two digits 9,9) is a wire-accepting reach
  history of height K; inside TOPUU_K a strict band acceptance at height K-1. So "c99 = 0 at every level <= K" means no 9-wire
  exterior of width <= K-2, "cUU = 0" no uniform band of left-end height <= K-3. These finite bounds are scope statements for
  the UNDECIDED words only, not results (AGENTS.md: horizon measurements are not progress).
- **SURVIVES** (kmax / nodecap / time) claims nothing. Non-uniform bands, centres and anything about 196 are not claimed.

## 2. Tools and validation (COMPUTED)

| tool | what | validation |
|---|---|---|
| `bin/fc_enum2` (`src/fc_enum2.cpp`) | r12b fc_enum generator streamed to stdout, sharded by index mod N, counts all words on stderr | p41 list == fc_enum list; union of shards == list; totals/primitive == CSV for p = 33, 34, 36, 40, 41, 42, 48 and every T = 49..54 |
| `bin/khxc` (`src/khxc.cpp`) | r12b khx.cpp lines 1-307 byte-identical + streaming main (-summary/-krep/-samp); pass 1 | identical verdicts and death levels vs r12b khx on 298,660 p41 words (`ctrl/khxc_val.out`) |
| `bin/khxt` (`src/khxt.cpp`) | r12b khx + `-exactset`, `-top` (TOP99/TOPUU closed-part test at every level), `-inv`, `-anc`, `-dump`, `-stophit` | controls: p11 TOP99 first hit K = 31, N12 K = 55, base 13 band {8,16} TOPUU K = 56, base 4 011001 K = 11 / 14 (all as expected); exact set == kh2 -exact at every level 1..46 on p34 |
| `bin/kh2`, `bin/kh2s` | r12b independent checker (string windows, full-window trans per edge, Kosaraju, exact closed-walk set); kh2s = kh2 seeded with a dumped level | kh2s seeded with the khxt p34 level 40 reproduces kh2's full-run counts at K = 41..46 |
| `py/extract_hit.py` | TOP99 hit block -> closed walk -> trim 9s -> r12b `verify_ext.verify` (exact integers) | p11 hit K = 31 -> e = 00111010011 VERIFIED; N12 hit K = 55 -> e = 010100101011 VERIFIED (`out/confirm/{p11,n12}_*`) |

md5 of the binaries and sources used: `logs/md5_r12e2.txt`.

## 3. Census T = 49..56 (COMPUTED; exclusions by Theorem K)

Pass 1: `khxc -kmax 400 -nodecap 2e7 -sec 4` (= r12b pass-1 options) on every F1 necklace (`run_census*.sh`, sharded).
Deep pass 1: `khxt -batch 4096 -exactset -top`, nodecap 1.2e8, 900 s, root pattern for imprimitive words (Lemma K6).
Deep pass 2: same with nodecap 2e8 and 3600 s (T = 49..52) or 2400 s (T = 53..56).

<!-- TABLE3 -->
| T | F1 words | primitive | counts = CSV | pass-1 DIES | pass-1 survivors | deep-1 DIES | deep-2 DIES | long-run DIES | known stream only | UNDECIDED | decided (Thm K/U) | max pass-1 K |
|--:|--:|--:|:-:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 49 | 94,598,340 | 94,598,336 | yes | 94,598,323 | 17 | 17 | 0 | 0 | 0 | 0 | 94,598,340 | 64 |
| 50 | 146,010,697 | 146,007,261 | yes | 146,010,679 | 18 | 18 | 0 | 0 | 0 | 0 | 146,010,697 | 62 |
| 51 | 225,446,789 | 225,446,658 | yes | 225,446,763 | 26 | 25 | 0 | 0 | 0 | 1 | 225,446,788 | 61 |
| 52 | 348,243,213 | 348,238,031 | yes | 348,243,187 | 26 | 24 | 1 | 1 | 0 | 0 | 348,243,213 | 78 |
| 53 | 538,112,178 | 538,112,178 | yes | 538,112,141 | 37 | 34 | 0 | 0 | 0 | 3 | 538,112,175 | 116 |
| 54 | 831,810,647 | 831,802,584 | yes | 831,810,611 | 36 | 33 | 0 | 0 | 0 | 3 | 831,810,644 | 73 |
| 55 | 1,286,235,064 | 1,286,235,048 | yes | 1,286,235,022 | 42 | 38 | 1 | 0 | 1 | 2 | 1,286,235,061 | 99 |
| 56 | 1,989,587,605 | 1,989,575,663 | yes | 1,989,587,531 | 74 | 69 | 2 | 0 | 0 | 3 | 1,989,587,602 | 90 |
| all | 5,460,044,533 | 5,460,015,759 | | 5,460,044,257 | 276 | 258 | 4 | 1 | 1 | 12 | 5,460,044,520 | |
<!-- /TABLE3 -->

- Per-word deep verdicts: `out/deep_verdicts.tsv` (from `py/deep_tsv.py`); survivors per T: `out/census/surv_T*.txt`;
  pass-1 histograms: `out/census/summary_T*.json`, `logs/census_sum_*.txt`.
- Deep deaths reach K = 661 in deep pass 1 (T = 53), K = 769 in deep pass 2
  (T = 52 0000111000100010101001010101001001110000111000110001, 1,225 s, widest level 48.6M nodes) and K = 1744 in the long run
  (T = 52 0001000100010001000100011000100011000100011000100011, 5,139 s, widest level 109.6M nodes).
- Odd T: no uniform band has odd combined period (r12b §4), so for odd T the band part is vacuous; Theorem K covers it anyway.

## 4. Death results and their confirmations

| word | T | verdict | runs | label |
|---|--:|---|---|---|
| p47 00010001000110001100010010001010100101000100011 | 47 | DIES K = 763 | (a) khxt -exactset -top, 1,718 s, widest 50.3M (`out/taskA/p47.out`); (b) r12b khx -batch 4096 (one-lap refinement, other pruning), 3,361 s, widest 157.2M, same K (`out/confirm/p47_khx3.out`); (c) kh2s (independent code) seeded with khxt's level 730 (50,677 windows, all kept): candidate and kept counts equal at every level 731..762, DIES K = 763 (`out/confirm/p47_kh2s.out`) | COMPUTED x3 + Theorem K |
| (p21)^2, root p21 = 001001010101001010101, L = 42 | 42 | DIES K = 2787 | (a) khxt -exactset -top -inv, 10,573 s, widest 58.75M (`out/taskA/p21sq.out`); (b) khxt_b rerun, identical per-level counts at every level 1..2750; (c) kh2s (independent code) seeded with level 2750 (69,291 windows, all kept): candidate and kept counts equal at every level 2751..2786, DIES K = 2787 (section 4.2) | COMPUTED x3 + Theorem K |
| T = 52 0001000100010001000100011000100011000100011000100011 (decisive run) | 52 | DIES K = 1744 | (a) khxt -exactset -top -inv, nodecap 2.5e8, 5,139 s, widest 109.6M (`out/decisive/T52w.*`); deep pass 1 (K = 550) and deep pass 2 (K = 1227) had been stopped by time; (b) khxt_b rerun, identical per-level counts at every level 1..1710; (c) kh2s (independent code) seeded with level 1710 (9,822 windows, all kept): candidate and kept counts equal at every level 1711..1743, DIES K = 1744 (section 4.3) | COMPUTED x3 + Theorem K |
| T = 52 0000111000100010101001010101001001110000111000110001 | 52 | DIES K = 769 | deep pass 2 khxt, 1,225 s, widest 48.6M (`out/deep2/52_*.out`); single run | COMPUTED + Theorem K |
| 151 census deep-1 deaths, T = 49..54 | 49-54 | DIES K <= 661 | khxt deep pass 1 (`out/deep1`, `out/deep53`, `out/deep54`); kh2 V5-style check of the ones with widest level <= 6M queued (chain15) | COMPUTED + Theorem K |
| 2,184,221,704 census pass-1 deaths | 49-54 | DIES K <= 116 | khxc (r12b khx code); kh2 -exact on 2,153 of them (samples + all with K >= 40): 2,153 SAME (`ctrl/kh2_T*.out`) | COMPUTED + Theorem K |

### 4.1 Shape of the three long deaths (COMPUTED)
- p47: exact set 2.0M at K ~ 520, 20K at K = 740, 165 at K = 762, 0 at K = 763. TOP99/TOPUU never hit.
- (p21)^2: exact set 0.3M-2.8M up to K ~ 2400, dip to 21K at K = 2500, 318K at 2700, 69K (2750), 15K (2770), 228 (2784),
  0 at 2787. TOP99/TOPUU never hit.
- T = 52 0001000100010001000100011000100011000100011000100011: exact set fluctuating between 0.36M (K = 850) and 4.4M (K = 600,
  1253) for 1,600 levels, then 1.10M (1600), 0.41M (1650), 51K (1700), 9.8K (1710), 22.6K (1720), 8.7K (1740), 445 (1743), 0 at
  K = 1744. TOP99/TOPUU never hit. In all three cases the final fall from ~1M to 0 took 100-250 levels after a long fluctuating
  phase; the WL hash never repeated, so there was no stabilisation before the death.

### 4.2 (p21)^2 confirmation (PASSED 08:00Z; `run_p21conf.sh`)
khxt_b (= `src/khxt.cpp`, separate binary) reruns p21, L = 42 to level 2750 and dumps the exact set of level 2750 with full windows
(`out/confirm/p21sq_K2750.seed`); then kh2s (r12b kh2 rules) continues from that seed. Pass criteria: per-level lines of the
rerun equal `out/taskA/p21sq.err` at every level 1..2750, and kh2s keeps all seed windows and prints DIES K = 2787.
Result: the rerun reached level 2750 (10,154 s); its per-level lines are IDENTICAL to Task A at every level 1..2750; the seed has 69,291 windows; kh2s keeps all of them, its candidate and kept counts equal Task A's (nodes, exactset) at every level 2751..2787 (0 mismatches over 37 levels) and it prints DIES K = 2787 (`out/confirm/p21sq_kh2s.out`).

### 4.3 T = 52 death confirmation (PASSED 07:59Z; `run_t52conf.sh`)
khxt_b rerun of the word to level 1710 with `-anc 0` (5,350 s; seed = the 9,822 windows of level 1710,
`out/confirm/T52w_K1710.seed`): per-level lines (nodes, scc, kept, exactset, exact, smallest) IDENTICAL to `out/decisive/T52w.err`
at every level 1..1710. kh2s (r12b's independent kh2: string windows, full-window trans for every edge, Kosaraju, its own exact
closed-walk set) seeded with that level keeps all 9,822 windows; its candidate and kept counts equal the decisive run's (nodes,
exactset) at every level 1711..1744 (0 mismatches) and it prints DIES K = 1744 (`out/confirm/T52w_kh2s.out`).

## 5. The "spine" observations: what they show and what they do not

- p34 ancestry (K = 2000, D = 1000, `out/anc/p34_K2000.anc`, COMPUTED): the level-k ancestors of the level-2000 exact set are ONE
  window per phase (34 nodes) for every k <= ~537, then 68, 102, 136, ... At level 1000 the 102 ancestors form 3 disjoint closed
  34-walks sharing digits 0..537; along each, the reach interfaces at cuts 1..959 are all distinct (no position period <= 958).
  **Shown (COMPUTED):** every 9-wire exterior of p34 of width >= 2000 has, at every time t, its lowest 537 digits equal to the
  unique trunk window at phase t (widths <= 2410 are excluded by TOP99 anyway). **Not shown:** that an infinite spine exists,
  that it is periodic, or anything that points toward an exterior.
- **SPINE CAVEAT (COMPUTED, r12e2):** at K = 800 the (p21)^2 exact set had the same shape (one window per phase for k = 1..70,
  then 42, 84, 126, ...), and (p21)^2 then DIED at K = 2787. A unique trunk at finite K is therefore no evidence of an infinite
  spine, and the earlier p34 K = 800 "two spines" turned out to be one trunk plus a long-lived transient (gone by K = 2000).
  Transient lifetimes are heavy-tailed (one branch lived > 750 levels).
- PAPER PROOF (elementary, r12e): in a finite graph, if only finitely many infinite paths start at a vertex, each is eventually
  periodic; so bounded ancestor counts of the inverse limit would force eventually periodic spines (possibly with a huge period).
- PAPER PROOF (r12e, "Theorem U with lookahead"): with S_k = the level-k ancestors of C_{k+D}, S_{k+1} is a function of S_k;
  an isomorphism S_k0 ~= S_k0+d with empty closed parts of TOP99/TOPUU on k0+1..k0+d would exclude every 9-wire exterior and
  band. For p34 the trunk digits are aperiodic over 959 cuts, so this does not close p34.

## 6. UNDECIDED words (nothing claimed)

Census words (T = 49..56; generated by `py/final_r12e3.py`; "exact set" = khxt -exactset node count at the last level reached in the best
run; a TOP hit would be marked in the last column):

<!-- OPEN -->
| T | word | type | best run | K reached | exact set at stop | widest level | TOP99/TOPUU |
|--:|---|---|---|--:|--:|--:|---|
| 51 | 000101010101010101001001010101001010101001010100101 | prim | deep2 (time, 3602 s) | 980 | 3,812,319 | 82,470,450 | none |
| 53 | 00001110000111000110001000101010101010101010100100111 | prim | deep2 (time, 2412 s) | 1308 | 5,797,433 | 115,431,308 | none |
| 53 | 00010101001010101010101010101001001010101001010100101 | prim | deep2 (time, 2401 s) | 595 | 3,518,588 | 76,333,488 | none |
| 53 | 00001010100101010010100010001010100100111000011100011 | prim | deep2 (time, 2404 s) | 652 | 2,838,786 | 93,981,391 | none |
| 54 | 001010101001010101001010101001010101001010101001010101 | imprim(root 9) | deep2 (time, 2482 s) | 69 | 2,844,821 | 61,568,569 | none |
| 54 | 000100010101010101010100111000100010101010101010100111 | imprim(root 27) | deep2 (time, 2429 s) | 156 | 5,262,215 | 111,830,485 | none |
| 54 | 000010111000100100001110000111000100001110001100010001 | prim | deep2 (time, 2404 s) | 752 | 4,148,201 | 94,661,230 | none |
| 55 | 0000101110001001000011100010000111000100010101001010001 | prim | deep2 (time, 2402 s) | 820 | 4,735,909 | 89,841,899 | none |
| 55 | 0001001011100010010111000100101110001001011100010010111 | imprim(root 11) | deep2 (time, 2443 s) | 217 | 2,840,156 | 54,847,813 | none |
| 56 | 00100101010101001001010101010010010101010100100101010101 | imprim(root 14) | deep2 (time, 2455 s) | 158 | 3,601,159 | 69,463,772 | none |
| 56 | 01010101010101010101010101010101010101010101010101010101 | imprim(root 2) | deep1 (time, 1150 s) | 20 | 1,021,527 | 17,582,999 | none |
| 56 | 00001110000111000100100010101001010001100010001000110001 | prim | deep2 (time, 2403 s) | 485 | 2,857,012 | 103,716,763 | none |
<!-- /OPEN -->

Words from r12b's list (not census words of this round):

| T | word (root, L) | last run | stopped at | exact set at stop | widest level | source / why open |
|--:|---|---|--:|--:|--:|---|
| 34 | 0001010101001001010101001010100101 | khxt, 15,018 s (time) | K = 2412 | 6,564,518 (growing: 1.9M at 1800, 4.7M at 2000) | 123.7M | `out/taskA/p34.out`; no TOP99/TOPUU hit |
| 40 | (01)^20 | r12b only (K = 60 at L = 40) | | | | can never die (8-periodic closed walks of G_K(01) at every K) |
| 48 | (01)^24 | r12b only (K = 26 at L = 48) | | | | as (01)^20 |
| 48 | N12^4 = (0001)^12 | r12e pattern 0001, L = 48, 3,771 s | K = 53 | 3.2M kept | | carries N12 (cannot die); P(12) open; `out/fam/n12x4_L48.out` |

For p <= 32 r12b's remaining open words ((01)^8, (01)^12, (01)^16; N12^2 settled by ReachDisk) were not run here.

## 7. Which open words look most worth a longer run

(T = 53 word 00001110000111000110001000101010101010101010100100111: a long run with -sec 6922 reached K = 1737 and was stopped by time, exact set 4.86M, widest level 147.2M, no TOP hit, `out/long/T53a.out`; its section 6 row shows the shorter deep-2 run.)
1. Evidence from the three long deaths (p47 K = 763, (p21)^2 K = 2787, T = 52 K = 1744): each exact set fluctuated for hundreds
   to thousands of levels without trend and without stabilisation, then fell to 0 within 100-250 levels. Survival to K ~ 1000-2400
   is therefore no sign of a surviving inverse limit, and capped words whose exact set fluctuates (rather than grows steadily)
   are the best candidates for a death. Deep pass 1 / deep pass 2 gave the T = 52 word only K = 550 / 1227; it died at 1744.
2. Best candidates (fast per level, so a 4-8 h khxt -exactset run reaches K ~ 3000-5000): T = 53
   00001110000111000110001000101010101010101010100100111 (K = 1308 in 2,412 s) and T = 51
   000101010101010101001001010101001010101001010100101 (K = 980 in 3,602 s; exact set 2.7M at 598 -> 3.8M at 980), then the
   primitive T = 53/54 words with K = 595-752 after 40 min. Their trajectories are not known (deep pass 2 kept no per-level log),
   so "fluctuating vs growing" cannot be told apart yet; a rerun with -v gives it.
3. Not worth more K-head time: p34 (exact set growing for 600 levels, 31 s per level at K = 2412, no checkpoint), the two
   imprimitive T = 54 words (roots of length 9 and 27: K = 69 and 156 after 40 min, i.e. 36 and 16 s per level, with 2.8M and
   5.3M kept nodes at that depth), and the families (01)^{4j}, N12^m (Theorem K can never apply; they need a top-boundary
   argument, r12b §9).

## 8. Where each result is (all jobs had ended when this was written)

| result | files |
|---|---|
| census T = 49..56 pass 1 | `logs/census_*.log`, `logs/census_sum_*.txt`, `out/census/summary_T*.json`, `out/census/surv*_T*.txt`; per-shard `out/census/T*_s*.out` in `logs.tar.gz` |
| deep passes | `out/deep_verdicts.tsv`; per-word `out/deep1`, `out/deep53`, `out/deep54`, `out/deep2`, `out/deep5556/*.out` in `logs.tar.gz`, per-level `out/deep5556/*.err` in `logs_deep5556.tar.gz` |
| p34, p47, (p21)^2 (Task A) | `out/taskA/*.out`; per-level `out/taskA/*.err` in `logs_taskA.tar.gz` |
| decisive T = 52 run | `out/decisive/T52w.out`; per level `out/decisive/T52w.err` (`logs.tar.gz`) |
| confirmations | `out/confirm/*.out`, `out/confirm/done_*.log`; per-level reruns `out/confirm/*_K*.err` (`logs.tar.gz`) |
| long T = 53 run | `out/long/T53a.out`; `out/long/T53a.err` (`logs.tar.gz`) |
| kh2 checks | `ctrl/kh2_deep_*.out`; `ctrl/kh2_T*.out` (`logs.tar.gz`) |
| TOP hit (p11^5) | `out/hits/` |
| main-session check | `logs/main_check/` (`tally.py`, `tally.out`: shard sums = CSV for every T, reruns identical per level, verdict lines) |

## 9. Reproduction (commands as run; all on the Studio, nice 10)

- Census pass 1, per shard: `bin/fc_enum2 10 T -shard i N | bin/khxc 10 -f /dev/stdin -kmax 400 -nodecap 20000000 -sec 4 -summary
  -krep 40 -samp S` (`run_census.sh`, `run_census2.sh`, `run_census3.sh "55:18 56:27" 9`); summary + CSV check:
  `python3 py/census_sum.py T ...`.
- Deep passes: `bin/khxt 10 -g W [-L n] -batch 4096 -exactset -top -v -kmax 100000 -nodecap NC -sec SEC` (root pattern + `-L |W|`
  for imprimitive W) via `run_deep.sh` / `run_deep2.sh` / `run_deep3.sh LIST OUTDIR NWORK NC SEC [START_BY END_BY]`.
- Task A: `run_taskA.sh NAME WORD [L] 15000` (= khxt `-batch 4096 -exactset -top -inv -v -kmax 100000 -nodecap 4e8`), launched by
  `launch_taskA.sh` for p34, p47 and p21 with L = 42.
- p47 confirmations: r12b khx `-batch 4096` (`out/confirm/p47_khx3.*`); `bin/khxt_b ... -kmax 730 -anc 0 out/confirm/p47_K730.seed`
  then `bin/kh2s 10 p47 47 -exact 800 400000000 out/confirm/p47_K730.seed` (`run_anc2.sh`).
- (p21)^2 confirmation: `run_p21conf.sh` (same pattern with level 2750 and `kh2s 10 p21 42 -exact 2800 ...`).
- kh2 checks: `ctrl/kh2_sample.sh T` (pass-1 deaths), `ctrl/kh2_deep.sh TAG MAXW TLIM BUDGET DIRS` (deep deaths).
- Hit path: `khxt ... -top -stophit -dump F`, `python3 py/extract_hit.py F ROOT L` (r12b verify_ext.verify), and the independent
  `python3 py/replay_plain.py F ROOT L [G]` (plain Python ints; controls p11, N12 OK; corrupted dumps FAIL).
- Tables: `python3 py/deep_tsv.py > out/deep_verdicts.tsv`; `python3 py/final_r12e3.py` (-> `out/final_table_r12e3.md`,
  `out/final_open_r12e3.txt`, `out/final_surv5556_r12e3.md`).

## 10. Files (this directory; binaries not included)

- Sources: `src/khxc.cpp`, `src/khxt.cpp` (khxt_b is a second build of the same file), `src/fc_enum2.cpp`, `src/kh2s.cpp`; `py/*.py`.
  khx.cpp, kh2.cpp, kstruct.py, verify_ext.py, wire_unique.py, census_summary.py are r12b's (`../ext41to48/src`, `../ext41to48/py`);
  bx.cpp, bxb.cpp, fc_enum.cpp are `../../round11/periods33to48/src`. Build: `c++ -O3 -std=c++17 -o bin/khxt src/khxt.cpp` (same for the others).
- Drivers: `run_census*.sh`, `run_deep*.sh`, `run_taskA.sh`, `launch_taskA.sh`, `run_p21conf.sh`, `run_t52conf.sh`, `run_decisive.sh`,
  `run_anc*.sh`, `run_fam.sh`, `chain*.sh`, `ctrl/*.sh`, `watchdog*.sh` (written for ~/p196_run/r12e on the Studio).
- Logs: plain files as in section 8; packed in `logs.tar.gz`, `logs_taskA.tar.gz`, `logs_deep5556.tar.gz` (each under 1 MB).
- Not copied (large or regenerable): the khxt level dumps `out/confirm/*.seed`, the ancestry files `out/anc/*.anc` (section 5,
  `run_anc.sh`), `out/explore/`, the stale drafts `out/final_table.md`, `out/final_open*.txt`, `out/final_table_r12e2.md`, and the
  working notes.

## Appendix A. All pass-1 survivors of T = 55 and 56 and their fates (generated by `py/final_r12e3.py`)

<!-- APP -->
| T | word | pass 1 (reason K) | type | deep runs |
|--:|---|---|---|---|
| 55 | 0000101110001001000011100001110001000110001000100010001 | time 42 | prim | deep1 DIES K=76, widest 1,923,959, 2 s |
| 55 | 0001000100011000110001000101010101001010101001010100101 | nodecap 23 | prim | deep1 DIES K=64, widest 2,665,244, 3 s |
| 55 | 0001000100101000101010010101001010001010101001010100101 | nodecap 34 | prim | deep1 DIES K=338, widest 39,125,769, 323 s |
| 55 | 0001000101010101010101001010100101000100100011000100011 | nodecap 24 | prim | deep1 DIES K=101, widest 8,107,813, 11 s |
| 55 | 0010010101010100100101010101010100101010010010101010101 | nodecap 12 | prim | deep1 DIES K=34, widest 1,603,011, 0 s |
| 55 | 0000101010010100010101010101010100100101010101010101011 | time 37 | prim | deep1 DIES K=43, widest 2,993,944, 2 s |
| 55 | 0000101110001001000011100001110001100010001000100010001 | time 41 | prim | deep1 DIES K=95, widest 2,928,546, 5 s |
| 55 | 0000101110001001000011100010000111000100010101001010001 | time 36 | prim | deep1 SURVIVES K=486 (time, kept 2,534,580), widest 51,934,885, 903 s; deep2 SURVIVES K=820 (time, kept 4,735,909), widest 89,841,899, 2402 s |
| 55 | 0000111000100010101001010001100010001000110001100010001 | nodecap 32 | prim | deep1 DIES K=163, widest 20,681,329, 64 s |
| 55 | 0000111000011100001110000111000011100010011000100010001 | time 61 | prim | deep1 DIES K=121, widest 1,966,557, 4 s |
| 55 | 0000111000100001110001000011100010000111000100001110001 | nodecap 14 | imprim(root 11) | deep1 SURVIVES K=100000 (kmax, kept 22), widest 5,047,369, 25 s, TOP99 first 31 |
| 55 | 0000111000011100010001000011100010001000100011000110001 | time 30 | prim | deep1 DIES K=71, widest 3,805,719, 4 s |
| 55 | 0000101010010100010001001010001000011100010001010101011 | nodecap 53 | prim | deep1 DIES K=106, widest 2,805,293, 5 s |
| 55 | 0000101010100101010101010100101010010101001001110000111 | nodecap 19 | prim | deep1 DIES K=55, widest 6,222,120, 5 s |
| 55 | 0000101010101010010101001001010101010101001001110000111 | nodecap 24 | prim | deep1 DIES K=51, widest 3,709,617, 2 s |
| 55 | 0000101110001001000011100010001000100010001000100010001 | time 27 | prim | deep1 DIES K=63, widest 3,337,274, 3 s |
| 55 | 0000111000011100011000100010001000100011000100110001001 | nodecap 16 | prim | deep1 DIES K=172, widest 9,213,043, 36 s |
| 55 | 0000101010010011100001010101010010101001010001000100011 | nodecap 28 | prim | deep1 DIES K=78, widest 3,040,380, 3 s |
| 55 | 0000101010101001010100101010010010101010101001110000111 | nodecap 39 | prim | deep1 DIES K=77, widest 6,721,459, 5 s |
| 55 | 0000111000011100001110001100010001010101010011100010001 | nodecap 31 | prim | deep1 DIES K=177, widest 4,478,034, 14 s |
| 55 | 0000111000011100011000100001110001000101010010100010001 | nodecap 39 | prim | deep1 DIES K=118, widest 2,913,004, 4 s |
| 55 | 0001001011100010010111000100101110001001011100010010111 | nodecap 22 | imprim(root 11) | deep1 SURVIVES K=149 (time, kept 1,452,858), widest 32,056,439, 913 s; deep2 SURVIVES K=217 (time, kept 2,840,156), widest 54,847,813, 2443 s |
| 55 | 0010010101010101010010101010010101001010100101010010101 | nodecap 14 | prim | deep1 DIES K=64, widest 1,389,185, 2 s |
| 55 | 0000101010010011100001010101010100101010011100010000111 | nodecap 45 | prim | deep1 DIES K=144, widest 6,777,699, 12 s |
| 55 | 0000111000011100010000111000110001000100011000110001001 | time 61 | prim | deep1 DIES K=85, widest 2,896,683, 2 s |
| 55 | 0000101010100101010010100010001000110001001000100100111 | nodecap 22 | prim | deep1 DIES K=235, widest 10,702,681, 39 s |
| 55 | 0000101010101010101010010101010101010101001010100100111 | nodecap 31 | prim | deep1 DIES K=48, widest 2,597,851, 2 s |
| 55 | 0000111000011100010011100010000111000100010001100010001 | nodecap 38 | prim | deep1 DIES K=164, widest 10,548,420, 28 s |
| 55 | 0001000101010100101010101010100100111000100111000100011 | nodecap 32 | prim | deep1 DIES K=69, widest 5,250,289, 6 s |
| 55 | 0000111000011100010001000100101000100010101001001110001 | nodecap 25 | prim | deep1 DIES K=288, widest 38,579,994, 242 s |
| 55 | 0000111000011100010011000100100011000100010001100010001 | nodecap 70 | prim | deep1 DIES K=243, widest 11,148,516, 38 s |
| 55 | 0000111000100010001000100010001100010001010101001110001 | time 19 | prim | deep1 DIES K=36, widest 3,291,047, 2 s |
| 55 | 0000111000100010001100011000100010101001010001000110001 | nodecap 26 | prim | deep1 SURVIVES K=433 (time, kept 3,051,005), widest 64,944,147, 900 s; deep2 DIES K=759, widest 64,944,147, 1245 s |
| 55 | 0000111000100011000100010101010011100001110001100010001 | time 48 | prim | deep1 DIES K=67, widest 1,877,751, 2 s |
| 55 | 0001000100010001000100101000100010001100010001000100011 | nodecap 32 | prim | deep1 DIES K=55, widest 2,422,101, 2 s |
| 55 | 0000101010010100010000101110001001100010001000011100011 | nodecap 27 | prim | deep1 DIES K=61, widest 5,314,889, 4 s |
| 55 | 0001000100100101010100101010010010101010101001010100101 | nodecap 20 | prim | deep1 DIES K=296, widest 16,679,454, 51 s |
| 55 | 0000101110001001000011100001110001000100010001100010001 | nodecap 19 | prim | deep1 DIES K=199, widest 9,897,214, 30 s |
| 55 | 0000101010010101001010001000100011000100010001000100011 | nodecap 23 | prim | deep1 DIES K=113, widest 12,887,757, 26 s |
| 55 | 0001000101010010011100010011000100011000100011000100011 | nodecap 32 | prim | deep1 DIES K=149, widest 12,455,754, 26 s |
| 55 | 0001010101010101001010101001001010101010101001010100101 | nodecap 24 | prim | deep1 DIES K=207, widest 28,774,189, 102 s |
| 55 | 0000111000011100011000100100011000100011000100110001001 | nodecap 19 | prim | deep1 DIES K=81, widest 3,742,715, 4 s |
| 56 | 00001010101010010101001001010101001010101001010100100111 | time 51 | prim | deep1 DIES K=77, widest 1,584,505, 2 s |
| 56 | 00001010101010101001010100101000101010101010011100010001 | time 30 | prim | deep1 DIES K=58, widest 3,407,726, 3 s |
| 56 | 00001010101010101010010010101010101010101001010100100111 | nodecap 13 | prim | deep1 DIES K=22, widest 1,899,639, 0 s |
| 56 | 00001011100010011100001110001000011100001110001001110001 | time 78 | prim | deep1 DIES K=230, widest 4,380,469, 16 s |
| 56 | 00001110001000101010011100010011000100010001000100010001 | time 40 | prim | deep1 DIES K=144, widest 5,821,638, 10 s |
| 56 | 00001110001100011000110001000101010011100010011100010001 | nodecap 23 | prim | deep1 DIES K=58, widest 3,179,897, 2 s |
| 56 | 00010001001010010010101001001010101001010101001010100101 | nodecap 45 | prim | deep1 DIES K=94, widest 6,101,337, 8 s |
| 56 | 00100101010010010101010010010101010101010010010101010101 | nodecap 21 | prim | deep1 DIES K=129, widest 3,412,514, 7 s |
| 56 | 00001010101010010101001001110000101010101001010100100111 | nodecap 10 | imprim(root 28) | deep1 DIES K=70, widest 1,960,401, 2 s |
| 56 | 00001110000111000100010101010101001010100101000100110001 | nodecap 24 | prim | deep1 DIES K=105, widest 6,475,124, 9 s |
| 56 | 00001110000111000100001110001000100001110001000110001001 | time 61 | prim | deep1 DIES K=88, widest 3,060,349, 3 s |
| 56 | 00001010100101010010011100010000111000100010001000100011 | time 24 | prim | deep1 DIES K=66, widest 4,112,702, 5 s |
| 56 | 00001010101010011100010001100011000110001100010010000111 | nodecap 62 | prim | deep1 DIES K=157, widest 4,867,496, 8 s |
| 56 | 00001110001001000101010010101010101010010101001010001001 | time 62 | prim | deep1 DIES K=114, widest 2,760,510, 4 s |
| 56 | 00010001010101010101010010101001010001001000110001100011 | nodecap 14 | prim | deep1 DIES K=50, widest 5,981,941, 4 s |
| 56 | 00001110001000011100011000100011000100010000111000110001 | time 27 | prim | deep1 DIES K=207, widest 13,434,197, 54 s |
| 56 | 00001110001000100010001100010010001100010001000110001001 | time 43 | prim | deep1 DIES K=76, widest 2,271,051, 3 s |
| 56 | 00010001001010001010100101010010010101010101001010100101 | nodecap 18 | prim | deep1 DIES K=83, widest 5,908,886, 6 s |
| 56 | 00001010100101010010100010011000100010001000100010000111 | nodecap 21 | prim | deep1 DIES K=64, widest 6,457,169, 7 s |
| 56 | 00001011100010011100010001100011000100001110001100010001 | time 40 | prim | deep1 DIES K=62, widest 2,488,316, 3 s |
| 56 | 00001110001000110001000110001000110001000110001100010001 | nodecap 13 | prim | deep1 DIES K=129, widest 4,410,964, 10 s |
| 56 | 00001110001001100010000111000110001000100011000100010001 | nodecap 33 | prim | deep1 SURVIVES K=780 (time, kept 578,677), widest 50,630,630, 901 s; deep2 DIES K=911, widest 50,630,630, 875 s |
| 56 | 00001110001010001010100101000100010001100011000100010001 | nodecap 28 | prim | deep1 DIES K=124, widest 8,178,892, 17 s |
| 56 | 00010100100101010100101010101010100101010101010100100111 | nodecap 15 | prim | deep1 DIES K=37, widest 1,611,466, 1 s |
| 56 | 00001110000111000100011000110001000100010001000110001001 | nodecap 34 | prim | deep1 DIES K=107, widest 3,921,315, 7 s |
| 56 | 00001011100010001010100101010010101001010100101000110001 | nodecap 23 | prim | deep1 DIES K=41, widest 2,537,222, 1 s |
| 56 | 00001011100010010000111000100010001000100010001100010001 | nodecap 27 | prim | deep1 DIES K=133, widest 9,624,754, 21 s |
| 56 | 00001011100010100010101001010001000100001110001100010001 | nodecap 30 | prim | deep1 DIES K=73, widest 3,882,232, 3 s |
| 56 | 00001110001000101010100101010101010100101010010100010001 | nodecap 33 | prim | deep1 DIES K=77, widest 7,403,692, 10 s |
| 56 | 00001110001000101010101001110001000011100010001100010001 | time 39 | prim | deep1 DIES K=87, widest 4,688,345, 6 s |
| 56 | 00001010100101000101010100101010010101001001010100100111 | time 48 | prim | deep1 SURVIVES K=343 (time, kept 2,686,788), widest 73,417,254, 901 s; deep2 DIES K=773, widest 81,927,962, 2012 s |
| 56 | 00001010100101010010101001001010101001010100101000100011 | nodecap 18 | prim | deep1 DIES K=179, widest 11,378,055, 38 s |
| 56 | 00001110001100011000100010001100010001000110001100010001 | nodecap 25 | prim | deep1 DIES K=45, widest 3,273,757, 2 s |
| 56 | 00001010100101000100010010100011000100010001000011100011 | nodecap 13 | prim | deep1 DIES K=83, widest 3,534,342, 3 s |
| 56 | 00001011100010011000100001110000111000100010101001010001 | time 79 | prim | deep1 DIES K=162, widest 7,659,223, 17 s |
| 56 | 00001010100101000100010000111000110001000100001110000111 | nodecap 24 | prim | deep1 DIES K=472, widest 24,164,979, 263 s |
| 56 | 00001010100101010010100010001001001010101001010100100111 | time 40 | prim | deep1 DIES K=69, widest 2,274,338, 3 s |
| 56 | 00001010101010100101010010100010001010101001010100100111 | nodecap 26 | prim | deep1 DIES K=53, widest 2,711,281, 2 s |
| 56 | 00001010101010101010101010101001010100101000100010000111 | time 24 | prim | deep1 DIES K=33, widest 2,635,775, 1 s |
| 56 | 00001011100010010000111000100010001100010010001001010001 | nodecap 36 | prim | deep1 DIES K=149, widest 5,299,214, 7 s |
| 56 | 00001110001000110001000110001000110001000110001000110001 | nodecap 26 | prim | deep1 DIES K=38, widest 2,880,514, 1 s |
| 56 | 00010001001001010101010100100101010101010101001010100101 | nodecap 28 | prim | deep1 DIES K=104, widest 6,582,341, 10 s |
| 56 | 00100101010101001001010101010010010101010100100101010101 | nodecap 14 | imprim(root 14) | deep1 SURVIVES K=119 (time, kept 2,111,570), widest 39,555,682, 912 s; deep2 SURVIVES K=158 (time, kept 3,601,159), widest 69,463,772, 2455 s |
| 56 | 00001010100111000100110001000100011000100100011000100011 | nodecap 17 | prim | deep1 DIES K=107, widest 6,205,780, 16 s |
| 56 | 00001010101010100100111000100101110001010001010100100111 | nodecap 16 | prim | deep1 DIES K=68, widest 3,629,912, 3 s |
| 56 | 00001011100010010111000100111000100010101001001110000111 | time 69 | prim | deep1 DIES K=133, widest 3,046,061, 6 s |
| 56 | 00001110001000011100010001010100101000100010101001010001 | nodecap 43 | prim | deep1 DIES K=328, widest 9,063,722, 47 s |
| 56 | 00001110001000011100011000100001110001100010001000110001 | time 67 | prim | deep1 DIES K=81, widest 1,755,068, 2 s |
| 56 | 00010101010101010101010010101001010101010101001010100101 | nodecap 30 | prim | deep1 DIES K=50, widest 2,194,823, 1 s |
| 56 | 00001010100010101001010001000101010010011100001110000111 | time 72 | prim | deep1 DIES K=177, widest 3,267,943, 9 s |
| 56 | 00010001000100010001100010001000110001000100011000100011 | nodecap 18 | prim | deep1 DIES K=69, widest 4,300,194, 7 s |
| 56 | 00001110001000100011000100010000111000100010001100010001 | nodecap 28 | imprim(root 28) | deep1 DIES K=120, widest 9,028,990, 20 s |
| 56 | 00010001000100010001100010001000110001000101010010100011 | nodecap 14 | prim | deep1 DIES K=627, widest 62,312,058, 887 s |
| 56 | 00001010100101010010100010001010100101000100011000100011 | nodecap 23 | prim | deep1 DIES K=57, widest 2,690,932, 2 s |
| 56 | 00001110001100010001000100011000100010101001010100100111 | nodecap 15 | prim | deep1 DIES K=78, widest 6,034,438, 9 s |
| 56 | 00001011100010010000111000100011000100010001000100010001 | nodecap 16 | prim | deep1 DIES K=288, widest 17,124,548, 120 s |
| 56 | 00001010100101000110001000100011000100010001000011100011 | nodecap 52 | prim | deep1 DIES K=106, widest 8,816,152, 13 s |
| 56 | 00001110000111000100010001000110001000101010010100010001 | time 29 | prim | deep1 DIES K=208, widest 11,517,021, 42 s |
| 56 | 00001110001000100010001000100011000100010101001001110001 | nodecap 16 | prim | deep1 DIES K=114, widest 7,231,970, 17 s |
| 56 | 00001110001000110001000100011000100010101010011100010001 | time 68 | prim | deep1 DIES K=166, widest 10,392,107, 17 s |
| 56 | 01010101010101010101010101010101010101010101010101010101 | nodecap 9 | imprim(root 2) | deep1 SURVIVES K=20 (time, kept 1,021,527), widest 17,582,999, 1150 s |
| 56 | 00001010100100101010101010100111000100010001000011100011 | nodecap 22 | prim | deep1 DIES K=136, widest 7,850,078, 16 s |
| 56 | 00001110001000011100011000100100010101001010001100010001 | nodecap 23 | prim | deep1 DIES K=303, widest 34,101,751, 207 s |
| 56 | 00100101010100100101010101010101001001010101010101010101 | nodecap 12 | prim | deep1 DIES K=54, widest 2,295,409, 1 s |
| 56 | 00001010101010011100010001000100010001000010111000100111 | time 38 | prim | deep1 DIES K=186, widest 6,249,309, 14 s |
| 56 | 00001010101010100100101010100101010100101010010100010001 | nodecap 10 | prim | deep1 DIES K=47, widest 3,563,127, 4 s |
| 56 | 00001011100010010001100010001010101001110001000100010001 | nodecap 28 | prim | deep1 DIES K=52, widest 4,641,605, 3 s |
| 56 | 00001110000111000100100010101001010001100010001000110001 | nodecap 20 | prim | deep1 SURVIVES K=235 (time, kept 4,038,241), widest 103,716,763, 902 s; deep2 SURVIVES K=485 (time, kept 2,857,012), widest 103,716,763, 2403 s |
| 56 | 00010001000110001100010001010100101010100101010010100011 | nodecap 12 | prim | deep1 DIES K=40, widest 2,638,378, 2 s |
| 56 | 00001011100010100010101001010001000100001110001001110001 | nodecap 52 | prim | deep1 DIES K=88, widest 3,015,072, 3 s |
| 56 | 00001010100100111000100110001000100001110001000011100011 | time 37 | prim | deep1 DIES K=126, widest 8,466,001, 15 s |
| 56 | 00001110000111000011100001110000111000011100001110000111 | nodecap 31 | imprim(root 7) | deep1 DIES K=726, widest 9,819,200, 526 s |
| 56 | 00001110001000101010101001110001000100010001000100010001 | time 25 | prim | deep1 DIES K=131, widest 8,496,496, 25 s |
| 56 | 00010001001001010101010101010010010101010101001010100101 | nodecap 15 | prim | deep1 DIES K=109, widest 4,447,216, 12 s |
<!-- /APP -->
