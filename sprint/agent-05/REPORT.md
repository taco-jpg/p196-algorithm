# [sprint 05] Delay witnesses — REPORT

Agent 05 · assignment A5 "DELAY WITNESSES" · branch `sprint/agent-05-delay-witnesses` · base commit `c6902ac6` (main, 2026-10-21)

## 1. Answer in one paragraph

A realized delay is a hard lower bound for the prefix method: if a positive seed `A` has `orbit A t` = a palindrome
beginning with `pre`, then **every** Agent124 certificate entry `(pre, b)` has `t ≤ b + 1`, for every width `k` and
every closed rank function (LEAN-VERIFIED, `Sprint.Agent05.entry_bound_ge_of_witness`). I searched **every seed below
10^14** (1,364,330,547 column-sum classes), 32 million random classes of 15–22 digits, the 1,301 numbers in published delayed-palindrome
record lists and 367 predecessor extensions, recording **every** palindrome hit, not only first hits (2,018 of the 9,000 per-prefix
maxima come from a later palindrome). Every one of the 9,000 four-digit prefixes is reached by some seed.
**449 four-digit prefixes have a witness with delay > 100, so no certificate can ever pass `no_196_of_entries`
(base check t ≤ 100) for them, nor for their three- and two-digit parents** — LEAN-VERIFIED for all 449 at once
(`Sprint.Agent05.Over100.not_mem_entries`, `not_mem_entries_take`) and separately, as requested, for 4456
(seed 1186060307891929990, first palindrome at t = 261; `Sprint.Agent05.W4456`). 447 of the 449 lie under open
three-digit prefixes, 2 (1129, 1386) under the cycle prefixes 112 and 138; the brief's 81-step example 1337 now has a
112-step witness. Nothing contradicts the existing certificates: 0 of the 1,731 Lean-certified four-digit bounds and 0
of the 168 C/K/S three-digit exclusions is exceeded, and **1,514 of the 1,731 certified bounds are attained exactly**
by a real seed (lower bounds LEAN-VERIFIED in `Sprint.Agent05.Sharp`), so those certificates are optimal. The flip
side, for assignment 8: the largest delay found anywhere is 289 (prefix 6634), so a base check to N = 1,000 would
remove the delay obstruction for every prefix found so far; the remaining obstruction is the cycles. Witnesses are
lower bounds only: a prefix without a large witness is not thereby certifiable, and the counts above grow with more
search (62 → 247 → 326 → 444 → 449 prefixes over 100 as the search went from ≤12 to ≤13 to ≤14 digits, then
sampling, then extension; record seeds included throughout).

## 2. Claims, labelled

### LEAN-VERIFIED

All modules are in `lean/P196/Sprint/Agent05/`, import only `P196.Agent117P2641.Agent124PrefixL` (plus each other),
and build with the repository lakefile on Lean 4.19.0. `#print axioms` output is in the files' build log; every
endpoint uses a subset of {propext, Classical.choice, Quot.sound}. No `sorry`, `native_decide`, custom axiom.

**`DelayWitness`** — the lemma shape (1.2 s, 456 MB):

| theorem | statement | axioms |
| --- | --- | --- |
| `Sprint.Agent05.AncestryBound pre B` (def) | `∀ A P t, 0 < A → PalStartsL pre P → orbit A t = P → t ≤ B` — the conclusion `ancestry_of_entries` gives with `B = b + 1` | — |
| `le_of_witness` | `AncestryBound pre B → 0 < A → PalStartsL pre (orbit A t) → t ≤ B` | none |
| `entry_bound_ge_of_witness` | `RowsClosed k R → ShortClosed k R → entryOK k R (pre, b) = true → 0 < A → PalStartsL pre (orbit A t) → t ≤ b + 1` (any `k`, `R`) | propext, Classical.choice, Quot.sound |
| `not_mem_entries_of_witness` | if `entries.all (entryOK k R) = true` and `entries.all (fun e => Nat.ble (e.2+1) N) = true` (the two premises of `no_196_of_entries`, which has `N = 100`) and a witness has `N < t`, then `∀ b, (pre, b) ∉ entries` | propext, Classical.choice, Quot.sound |
| `palStartsL_of_append`, `palStartsL_take` | a palindrome beginning with `pre ++ more` begins with `pre`; with `pre` it begins with `pre.take j` | propext, Quot.sound |
| `witnessOK`, `witnessOK_sound` | Boolean check of data `(pre, seed, t, P, W)`: `0 < seed`, `orbit seed t = P`, `reverse10 P = P`, `value (digitAt P) W = P` with nonzero lead digit, leading digits `= pre`; `witnessOK w = true → 0 < w.seed ∧ PalStartsL w.pre (orbit w.seed w.t)` | propext, Quot.sound |
| `entry_bound_ge_of_witnessOK`, `not_mem_entries_of_witnessOK`, `not_mem_entries_take_of_witnessOK` | the lemmas above for a checked witness (the last one also for every shorter prefix `pre.take j`) | propext, Classical.choice, Quot.sound |

`N` is a parameter, so the lemmas apply unchanged when assignment 8 generalizes `no_196_of_entries` to
`bound + 1 ≤ N`.

**`Witness4456`** — the requested instance (19.4 s, 1,506 MB):

* `Sprint.Agent05.W4456.first_hit : Palindrome (orbit seed 261) ∧ ∀ t, t < 261 → ¬ Palindrome (orbit seed t)` with
  `seed = 1186060307891929990`; the 119-digit palindrome is a literal in the file.
* `reaches : 0 < seed ∧ PalStartsL [4,4,5,6] (orbit seed 261)`.
* `ancestry_bound_ge : AncestryBound [4,4,5,6] B → 261 ≤ B`.
* `entry_bound_ge`: every accepted entry for `[4,4,5,6]`, `[4,4,5]` or `[4,4]` has rank bound `b ≥ 260`.
* `not_mem_entries`: for every base check `N ≤ 260`, no entry list passing both premises of `no_196_of_entries`
  contains `[4,4,5,6]`, `[4,4,5]` or `[4,4]`, with any bound.

**`Over100`** — all 449 four-digit prefixes with a witness delay above 100 (23 chunk files of ≤ 20 witnesses + one
aggregator; heaviest file `Over100C00` 72.0 s and 2,014 MB, the aggregator 6.1 s and 580 MB). Endpoints `Sprint.Agent05.Over100.`:
`witnesses_ok`, `prefixes` (the 449 prefixes as an explicit list), `length_witnesses` (= 449), `delays_gt`
(every `t > 100`), `realized`, `ancestry_bound_ge`, `entry_bound_ge`, `not_mem_entries`
(`∀ w ∈ witnesses, N < w.t → ∀ b, (w.pre, b) ∉ entries` for every entries list passing the two premises with base
check `N`; take `N = 100`), `not_mem_entries_take` (the same for `w.pre.take j`, i.e. the 177 three-digit and 44
two-digit parents).

**`Sharp`** — 1,514 witnesses (6 chunk files of ≤ 300 + aggregator; heaviest file `SharpC00` 19.2 s and 1,394 MB): for 1,514 of the 1,731 certified
four-digit entries `(pre, b)` (the 1,730 entries of `Agent124FourDigit` plus 2641 with `b = 5` from
`Agent117P2641`), a positive seed whose orbit at time `b + 1` is a palindrome beginning with `pre`
(`Sprint.Agent05.Sharp.realized`, `ancestry_bound_ge`). Together with the existing `Agent124.CertF4.ancestry_NN`
(`t ≤ b + 1`) the maximal delay to these 1,514 prefixes is exactly `b + 1`. The equality is the conjunction of two
verified theorems read side by side; I did not state it as a single Lean theorem.

### COMPUTED

All numbers below are printed by the commands in section 3 (outputs saved in `data/analysis_output.txt` and
`data/run_summaries.txt`). Machine: Linux VM, 2 cores, 7.8 GB RAM. Every row of every result table was recomputed
independently with Python big integers (`tools/verify_tables.py data` → `P3: 900`, `P4: 9000`, `P5: 90000 rows
re-verified`, `ALL ROWS VERIFIED`); the search code only proposes witnesses.

1. **Search engine** (`tools/delays.cpp`, C++17/OpenMP). Seeds are enumerated by column-sum class (pair sums
   `q_i = d_i + d_{l-1-i}` and the middle digit): all members of a class share `step(A)`, so each class is iterated
   once and the smallest member is reported. Every palindrome hit is recorded while the iterate has ≤ D digits.
   An exact memo stores "distinguished" iterates (hash low bits zero) with the list of their later hits; a later
   orbit that reaches a stored iterate copies the list and stops. Validation:
   * class search == brute force over every seed `< 10^5` (`tools/pycheck.py 100000 120` vs `delays exhaust 1 5
     --D 120`): identical per-prefix maxima and witness seeds, 1,487 rows;
   * memo == no memo for every seed with ≤ 9 digits, `--D 200`: identical P3/P4/P5 tables (71,342 rows), 59.6 s
     without memo vs 6.3 s with memo;
   * the step cap never bound before the digit cap in any run (`# mcap 0` in every table header).
2. **Coverage and cost** (wall time on 2 cores, peak RSS):

   | run | classes | steps | time | RSS |
   | --- | ---: | ---: | ---: | ---: |
   | all seeds with 1–12 digits, D = 200 | 71,806,869 | 2,800,393,530 | 152.0 s | 1,560 MB |
   | all 13-digit seeds, D = 200 | 445,697,820 | 18,500,807,946 | 1,141.2 s | 3,116 MB |
   | all 14-digit seeds, D = 160 | 846,825,858 | 77,095,478,109 | 6,084.1 s | 3,106 MB |
   | random classes, lengths 15–22, 4,000,000 each, D = 200 | 32,000,000 | — (per run in `run_summaries.txt`) | 202.5–209.7 s each | 789–792 MB |
   | 1,301 numbers from record lists, D = 400 | 1,301 | 1,183,137 | 0.4 s | — |
   | predecessor extensions (`tools/extend.py`), re-run forward | 28 + 339 | — | < 3 s | — |

   The 13- and 14-digit memo tables filled (93,952,405 entries = 70 % of 2^27); after that the memo stops
   inserting, which costs speed, not correctness. Known record seeds: OEIS b-files A023109, A065198, A281390,
   A281506, A281507, A281508, A281509, A326414, A340397, A353185, A065320–A065327, A033665, and the 285 numbers on
   jasondoucette.com/worldrecords.html (`data/known_seeds.txt`; any integer is a valid seed, so a mistyped record
   only changes which witness it is, never its validity).
3. **Per-prefix tables**: `data/max_delay_P3.tsv` (900 rows), `data/max_delay_P4.tsv` (9,000), `data/max_delay_P5.tsv.gz`
   (90,000): prefix, largest delay found, smallest witness seed at that delay, palindrome width, source run.
   Every 2-, 3-, 4- and 5-digit prefix is reached by some seed.
4. **Four-digit prefixes by largest witness delay** (repo status: certified = the 1,731 Lean-certified four-digit
   entries; parent-excluded = three-digit parent marked C/K/S/F in RESULTS.md; parent-cycle = parent among the 14
   Agent117RemainingCycles prefixes; repo-open = the other 3,993):

   | witness delay | count | repo-open | parent-cycle |
   | --- | ---: | ---: | ---: |
   | > 48 (no rank bound ≤ 47 possible) | 2,259 | | |
   | > 50 | 2,191 | 2,165 | 26 |
   | > 80 | 1,050 | 1,040 | 10 |
   | > 100 | **449** | 447 | 2 |
   | > 120 | 135 | 134 | 1 |
   | > 150 | 31 | 31 | 0 |
   | > 200 | 16 | 16 | 0 |
   | > 250 | 2 | 2 | 0 |

   The largest: 6634 (289, seed 10036069400174999499950, OEIS A353185), 4456 (261), 9945 (250), 8922 (244), 6633 (243),
   1486 (241), 4967 (238), 5799 (236), 4577 (233), 1596 (222); full list `data/P4_delay_over_100.tsv`.
   Three-digit: 177 of the 579 open/cycle three-digit prefixes have a witness > 100 (447 > 48). Two-digit: 44 of 90.
   By first digit, the 449 split 1: 141, 4: 91, 8: 64, 3: 48, 6: 40, 2: 33, 5: 23, 9: 7, 7: 2.
5. **Consistency with the existing certificates** (red-team value): 0 of the 1,731 certified four-digit entries has a
   witness delay above `b + 1`; 0 of the 168 three-digit cells marked C/K/S has a witness above 100; 620: largest
   witness 12 = proved bound 12; 739: largest witness 15 vs proved bound 39. Slack `b + 1 − delay` histogram:
   0: 1,514 · 1: 18 · 2: 34 · 3: 45 · 4: 17 · 5: 18 · 6: 31 · 7–32: 54. The largest delay to a certified prefix is 26
   (5987, rank bound 28); 111 certified prefixes are reached in more than 11 steps (the brief's "never more than 11"
   came from seeds < 10^6 only and is not a property of the prefixes).
6. **Later hits matter.** 2,018 of the 9,000 four-digit maxima are not the seed's first palindrome
   (`tools/later_hits.py`). Extreme case: seed 100000037873410 is a palindrome after 1 step and reaches a palindrome
   beginning 4973 after 174 steps. A witness search that stops at the first palindrome under-reports the bound a
   certificate needs.
7. **The 14 cycle prefixes** (largest witness for the three-digit prefix, then for its children x0…x9):
   112: 113 [1,1,83,93,87,78,97,80,68,113] · 138: 122 [1,1,1,1,1,1,122,89,97,83] · **164: 1 [all ten children 1]** ·
   198: 63 · 248: 85 · **275: 16** · 398: 56 · 626: 45 · 710: 49 · 716: 62 · 790: 73 · **911: 22** · 936: 68 · 952: 46
   (children in `data/analysis_output.txt`). For 164 no seed below 10^14 (nor any sampled or record seed) reaches a
   164-palindrome in more than one step, although its k-column graph has a cycle.
8. **Open prefixes with tiny witnesses.** Three-digit open/cycle prefixes whose largest witness is 1: 120, 131, 142,
   153, 164, 175, 186, 197, 560, 780 (68 have largest witness ≤ 8). Four-digit repo-open prefixes with largest witness
   1: 105; ≤ 8: 868.
9. The brief's batch numbers could not be checked here: the batch lists (5,852 certified, 1,030 cycle, 2,091
   undetermined, 27 lead-one) are not in the repository, and this session had no shell or folder access on the Mac
   Studio, so I did not read them.
   `tools/check_list.py data/max_delay_P4.tsv LIST` does the join in one command (lines `PREFIX` or `PREFIX BOUND`);
   any certified line with witness delay > `BOUND + 1` is a contradiction. Since the largest batch bound is 47, none
   of the 2,259 prefixes with witness > 48 may appear among the 5,852 batch-certified ones. (Also: 1,030 + 2,091 + 27
   = 3,148 open in §1 of the brief vs 3,134 in assignment 6 — 14 apart; I could not resolve which is right.)

### CONJECTURE

* **C1.** The prefixes 1a(a−2) — 120, 131, 142, 153, 164, 175, 186, 197 — and 560, 780 have true maximal delay 1:
  every palindrome beginning with them is reached only as `step(A)` of its seed, never later. In particular the
  k-column cycle of 164 (Agent117RemainingCycles) is not realized by any integer orbit. Evidence: item 7–8 above.
  (Their F-list neighbours 130, 140–141, 150–152, … are excluded by the forward-invariant list.)
* **C2.** For every N there are four-digit prefixes whose largest delay exceeds N (record delays have grown roughly
  linearly with seed length: 24 at 2 digits, 261 at 19, 289 at 23), so a fixed base check N always leaves some
  prefixes outside the Agent124 route. Evidence: the over-100 count kept growing with every extension of the search.

### IDEA

* **I1.** Feed `data/max_delay_P4.tsv` to the batch generator: skip prefixes whose witness exceeds the base check,
  and start each certificate search at width/bound ≥ witness − 1 (the 1,514 sharp entries show the bound found is
  usually exactly the witness).
* **I2.** For C1 a direct argument may be short. By `palindromePredecessor_iff` a predecessor `x` of a palindrome
  either has all pair sums ≤ 9 (then, for prefix 1a(a−2), pair sums 1, a, a−2, … and `x` = 1…0) or overflows (pair
  sums in {0, 11}, first one 11). Show that no such `x` is itself `step(y)`, using the necessary image condition
  `y_i − y_{l−1−i} ∈ {0, ±1, ±9}` for same-length predecessors and its shifted form for shorter ones (the filter in
  `tools/extend.py`, validated by brute force below 10^5). That would be a depth-1 certificate exactly where the
  k-column abstraction of 164 sees a cycle.
* **I3.** Backward extension (`tools/extend.py`, predecessor classes) extends long witnesses by a few steps: it lifted
  6633 from 242 to 243 and 1129 from 112 to 113, and moved 1331, 1452, 1468, 1487, 4608 above 100. Run it on every
  new sampled witness (it cannot help inside the exhaustive range: a predecessor never has more digits).

## 3. Reproduce

From `sprint/agent-05/` on a checkout of this branch (Python 3.13, g++ with OpenMP; on macOS use `CXX=g++-14` from
Homebrew, or build without `-fopenmp` for one thread):

```bash
./run_all.sh            # everything below in order: about 2.5 h of search on 2 cores (14 digits alone: 1.7 h), then the Lean build
```

or step by step:

```bash
g++ -O3 -fopenmp -o delays tools/delays.cpp
# self-tests
python3 tools/pycheck.py 100000 120 > runs/py5.txt
./delays exhaust 1 5 runs/cpp5.txt --D 120 --memo 2 --table 20
diff runs/py5.txt <(awk '$1=="P4"{print $2, $3, $4}' runs/cpp5.txt) && echo "class search == brute force"
./delays exhaust 1 9 runs/v_nm.txt --D 200
./delays exhaust 1 9 runs/v_m.txt --D 200 --memo 4 --table 24
diff <(grep ^P runs/v_nm.txt) <(grep ^P runs/v_m.txt) && echo "memo == no memo"
python3 tools/extend.py --selftest       # pred_classes mismatches below 200000: 0; filter dropped ...: 0
# search
./delays exhaust 1 12 runs/ex1_12.txt --D 200 --memo 5 --table 26
./delays exhaust 13 13 runs/ex13.txt --D 200 --memo 5 --table 27
./delays exhaust 14 14 runs/ex14.txt --D 160 --memo 5 --table 27
./delays seeds data/known_seeds.txt runs/known.txt --D 400
for L in 15 16 17 18 19 20 21 22; do ./delays sample $L 4000000 $L runs/s$L.txt --D 200 --memo 5 --table 25; done
# extension of the best witnesses, forward re-run of the extended seeds, final tables
python3 tools/analyze.py runs/tmp runs/ex*.txt runs/known.txt runs/s*.txt > /dev/null
python3 tools/extend.py runs/tmp/max_delay_P4.tsv 50 1000 runs/ext.tsv --budget 5
cut -f4 runs/ext.tsv | tail -n +2 > runs/ext_seeds.txt && ./delays seeds runs/ext_seeds.txt runs/ext_fwd.txt --D 400
python3 tools/analyze.py data runs/ex1_12.txt runs/ex13.txt runs/ex14.txt runs/known.txt runs/s*.txt runs/ext_fwd.txt
python3 tools/verify_tables.py data      # ALL ROWS VERIFIED
python3 tools/later_hits.py data/max_delay_P4.tsv
# Lean
python3 tools/gen_lean.py data/max_delay_P4.tsv 100 ../../lean/P196/Sprint/Agent05 Over100 --chunk-size 20
python3 tools/sharp_table.py data/max_delay_P4.tsv data/repo_bounds.json data/sharp_P4.tsv
python3 tools/gen_lean.py data/sharp_P4.tsv -1 ../../lean/P196/Sprint/Agent05 Sharp --chunk-size 300
cd ../../lean && lake build P196.Sprint.Agent05.Witness4456 P196.Sprint.Agent05.Over100 P196.Sprint.Agent05.Sharp
```

In this session the extension ran in two passes (28 seeds from the record list, then 339 from the merged table);
`run_all.sh` does it once on the merged table, which extends the same best witnesses. `data/repo_bounds.json` comes from
`tools/extract_entries.py ../../lean/P196` and `data/three_digit_marks.json` from `tools/parse_marks.py
../../RESULTS.md`. The Lean files are not registered in `lean/registry.json` (the sprint rules forbid editing it), so
`tools/verify.py` reports them as unregistered; `sprint/agent-05/registry_entry.json` is the entry to add on merge.
With that entry added temporarily, `python3 tools/verify.py --changed` printed `[build] OK`, `[axioms] 32 endpoints
checked`, `ALL CHECKS PASSED (changed files only, against origin/main)`; the registry change was then reverted. The whole
sprint build (`lake build` of the three roots, 2 jobs) took 351.7 s wall with at most 2,012 MB per Lean process.

## 4. What the next agent should do

1. **Run the join** on the Mac Studio: `python3 tools/check_list.py data/max_delay_P4.tsv <batch certified list with
   bounds>` and `<open list>`. A certified prefix with a larger witness would mean a bug in the batch certificates.
2. **Scale the search on the 32-core Mac**: `./delays exhaust 15 15 … --table 31` (8.47·10^9 classes) and 16
   digits, plus `sample` at 10^8–10^9 classes per length. On this machine 14 digits took 11,840 CPU-seconds with a full
   memo table; with 16× the cores and a table that does not fill, 15 digits should take very roughly an hour (an
   estimate, not a measurement). Then regenerate `Over100` (the generator chunks automatically).
3. **Assignment 8 (base check N)**: the lemmas here take `N` as a parameter; with N = 1,000 none of the witnesses
   found blocks the route (max 289). Prefixes in `P4_delay_over_100.tsv` are exactly where a certificate needs a rank
   bound above 99 — check that the batch generator's search does not cap the rank there.
4. **Agents 4 / 7 / anyone with a new abstraction**: start with the prefixes of C1 (164 above all): the integer data
   say depth 1, the k-column abstraction says cycle. Item 7 lists which children of each cycle prefix have small
   witnesses (e.g. 1380–1385, 1640–1649, 2480–2484, 6260–6267, 7106–7109, 7900–7907, 9110–9116 have largest witness
   ≤ 4); these are the natural first targets for a refined certificate.
