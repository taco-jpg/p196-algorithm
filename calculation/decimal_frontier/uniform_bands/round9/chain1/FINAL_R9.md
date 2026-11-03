# Round 9 — final report (chain 1 at P = 72, 88, 96; chain 8)

Labels: COMPUTED / UNDECIDED only. A finite replay is not a certificate. "Height" = number of reach edges = width of the Agent120 B-cycle.
Studio run dir `~/p196_run/r9/` (sources, logs, window bitsets `win/`); copies of sources and logs in `results/r9/` here.
Repo `~/p196_repo` was only pulled (now 4a490bab); nothing tracked was changed, nothing pushed.

## 0. Inputs and anomalies
* `claude/swarm_digest_2026-11-02.md` does **not exist**: not on main after `git pull` (4a490bab), not in any remote ref name, not on either machine.
  So the port-language definition (S = 100, L = 1000) and "chain 8 root [9,17,5]" could not be read from their source. The repo has no other
  text that defines either (grep for `9,17,5`, `chain 8`, `port language`).
* Checked from the given facts: `khead_family.py 0001 7` gives 4, 11, 62, 161, 332, 795, 2011 (matches). The arithmetic r = P/4 with cyclic
  words over S = 100, L = 1000 and >= 5 S between L's gives exactly the stated residues (r = 1 mod 3 needs r >= 19, r = 2 mod 3 needs r >= 38,
  3 | r < 57 only pure S), and hence the open cells P = 72, 88, 96, 112, 120.
* Consequence for the method: the bottom of every cone below is the unrestricted root interface (c = 0, d = overflow mask, r = 1, root rule
  x >= 1) of r6-r8. A port-language restriction of the bottom could only remove paths, so an UNREACHABLE here would also hold with it;
  a REACHABLE would have had to be checked against the language by hand. Neither happened.

## 1. Tools (new, round 9)
* `backdisk9.cpp`: backdisk (r8) with 128-bit c/d streams (T <= 128, keys up to 5 words) and window sets read from bitsets (env WINFILE).
  Otherwise identical (same predecessor DFS, root rule, ROT quotient, manifest, guards).
* `winbits.cpp`: the same window abstraction (same abstract step, bottom pattern, closure) stored as an exact bitset per clock phase.
  w = 10 counts equal round 7 exactly (28,699,436 / 25,467,296 / 114,741,888 / 97,404,348). New w = 12 (clock 0001): 1,691,146,196 /
  1,410,547,788 / 1,173,961,472 / 1,034,174,112 states (2.1 GB per phase, 7 min on 16 threads).
* `wintest.cpp`: tests every alignment of a periodic 9-wire stream against the window sets (T-independent exclusion).
* `ktail.cpp` (new idea): the reach graph read column by column (time direction) from the 9-wire end outward. Node = (x_0..x_{K-1}, phase),
  label = outer interface letter; with fixed labels the step is deterministic. S_K = nodes on bi-infinite walks (trimming), S_K inside
  S_{K-1} x [0..18]. Root cycles in S_K (labels = bottom interface, d_K = clock bit, x_{K-1} >= 1) are exactly the reach paths of height K,
  for EVERY period at once.

## 2. Validation
| check | result |
|---|---|
| self test backdisk9 (random forward edge in predecessor set + random predecessor steps forward), clock 0001 | T=24: 200,000 edges 0 mismatches; T=48: 100,000, 0; T=72: 2,000, 0; T=88, T=96, clock 01 T=40, w=12 T=88: still running at hand-off (studio `r9/selftest2.sh`, log `r9/logs/selftest.log`) |
| **N12 positive control (required)**, same binary, ROT=1 | T=24 w=10: **height 53**; T=24 w=12: **53**; T=48 w=12: **53** (21 s) |
| N12 at T=72, w=12 | cone 135,082 / 3.4M / 23.1M / 240.9M / 569.2M / 636.7M new states in layers 2-7 (1.47e9 total), stopped: height 53 needs 52 layers. The cone method cannot reproduce the known positive at T=72 |
| regression vs round 7 (w=10) | M1 P=24: 7,142 states (= r7); P=40: 11,320,224 states, 88 layers (= r7) |
| w=12 vs w=10 | P=40: 6,668,190 states (88 layers); P=48: 141,349,987 (119 layers; r7 w=10: 271,954,230, 120 layers): UNREACHABLE again, cone only about 2x smaller |
| ktail vs Agent120 orbits (EQUIV_R8 B) | base 2 g=10 e=10: first root cycle K=2; base 3 g=11100 e=01011: K=7 (len 5); base 4 g=100 e=100: K=2; e=010: K=6. All equal the first reach heights 2, 7, 2, 6 |
| ktail decimal p11 (g=00001110001, e=00111010011) | no root cycle for K <= 23 (S_23 = 28,093,832), consistent with first height 29; K=29 not reachable with this tool |

## 3. Chain 1, P = 88, clock (0001)^22, Agent6 period-8 ports — **UNDECIDED**
backdisk9, WIN=12, ROT=1, targets: 01000101 and 10111010 repeated, offsets 0..3 (16 keys, 8 survive the windows).
Layers (new states): 4; 5,170,243; 31,585,555; 68,157,175; 142,880,722; 559,082,140; 2,068,715,037 -> TOO_BIG at layer 7 (2,875,590,876 states, cap 2e9), 11.6 min.
Growth about x3.7 per layer at layer 7; with round-7/8 cones needing 88-545 layers, a complete cone is out of reach (also by disk: 1.2 TB free, 40 B/key).
Stuck at: cone size (no pruning that grows with T); the N12 control shows the same explosion at T=72.

## 4. Chain 1, P = 72, clock (0001)^18 (pure S) — **UNDECIDED**
Same setup (8 of 16 keys survive). Layers: 4; 410,528; 1,723,121; 2,767,916; 4,691,505; 14,565,881; 41,585,142; 117,762,673; 318,921,335;
747,889,146; 1,800,810,110 -> TOO_BIG at layer 11 (3,051,127,361 states), 11.7 min. Growth x2.4-2.7 per layer.

## 5. P = 96 (period-8 and period-16 ports) — **UNDECIDED**
32 keys, 12 survive. Layers: 5; 19,389,882; 153,424,192; 609,430,547; 6,573,952,408 -> TOO_BIG at layer 5 (7,356,197,034 states), 18.6 min.

## 6. All-period lower bound on the height (ktail) — **COMPUTED** (premise: reach = Agent120 system, as in r8)
Clock 0001, e = port word at each clock alignment (alignments o and o+4 are the same up to a time shift):
| port class | alignment(s) | windows (w=10 and w=12) | ktail |
|---|---|---|---|
| 01000101 | o=0 (01000101), o=3 (00101010) | excluded (window at slot 0) for every T | S_K = 14 nodes = the bare 9-rail for K = 1..24, no root cycle |
| 01000101 | o=1 (10001010) | survives | no root cycle for K <= 18 (S_18 = 38,610,309); K=19: 7.3e8 candidates, stopped |
| 01000101 | o=2 (00010101) | survives | no root cycle for K <= 17 (S_17 = 41,244,886) |
| 10111010 | o=0, o=3 | excluded | 14-node 9-rail only, K <= 24, no root cycle |
| 10111010 | o=1 (01110101) | survives | no root cycle for K <= 18 (same counts as 10001010) |
| 10111010 | o=2 (11101010) | survives | no root cycle for K <= 17 |
| 1000100001110111 | o = 1 mod 4 (0001000011101111) | survives (o=1,5,9,13) | no root cycle for K <= 15 (S_15 = 45,685,084) |

So: **for every period P (72, 88, 96, 112, ... included) any chain-1 outer end that emits an Agent6 period-8 port has height >= 18**
(>= 19 at alignment 1), and one emitting the period-16 port has height >= 16. This is a bound only, not a decision; N12 has height 53.
S_K grows by x2.2-2.6 per K, so K ~ 50 is not reachable this way. (The 9-rail alignments: the inner 9s are transparent, so the K-tail graphs
for K >= 3 are isomorphic; the computed K <= 24 agrees with the window exclusion.)

## 7. Chain 8, root [9,17,5], P = 72 — **UNDECIDED (blocked)**
No definition of chain 8 or of the root [9,17,5] exists in the repo or in any local file (the digest is missing). Not run.

## 8. Not done / open
* Exact cones at P >= 72: the window filter (w=10 or 12) is the only forward pruning; it is T-independent and does not stop the per-T
  growth. Ideas not finished: a head/tail product (khead from the root x ktail from the 9-wire) with matching interface letters, which is
  deterministic and covers all periods; a port-language bottom once its definition is available.
* Self tests at T=88/96 (2,000 / 1,000 edges) were still running in the background at hand-off; result in studio `~/p196_run/r9/logs/selftest.log`.

## 9. Label table
| cell | label |
|---|---|
| N12 positive control (T=24, 48; height 53) | COMPUTED (passes) |
| chain 1 P=88 | UNDECIDED (TOO_BIG at layer 7, 2.88e9) |
| chain 1 P=72 | UNDECIDED (TOO_BIG at layer 11, 3.05e9) |
| chain 1 P=96 (period 8 and 16) | UNDECIDED (TOO_BIG at layer 5, 7.36e9) |
| chain 8 [9,17,5] P=72 | UNDECIDED (definition missing) |
| height >= 18 / 19 / 16 for all P (section 6) | COMPUTED (premise: reach = Agent120) |
