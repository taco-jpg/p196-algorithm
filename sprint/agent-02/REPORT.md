# Sprint agent 02 — generalizing `Agent124ForwardInvariant`

Branch `sprint/agent-02-forward-invariant`. Everything is under `sprint/agent-02/` and
`lean/P196/Sprint/Agent02/`. Machine used: 2-core x86 VM, 7.8 GB RAM, Lean 4.19.0, gcc, Python 3.13.

## 1. Answer

`Agent124ForwardInvariant` uses the forward closure `F_k` (k = 3) of the folded column sums
`(q_0, q_1, q_2)` of `orbit(196, 100)` under the prefix map `forwardPrefix w e` with both values
of the one unknown inner carry `e`; a 3-digit word outside `F_3` (and with no possible final
overflow) cannot be the start of a palindrome in the orbit, because the last predecessor of a
non-overflow palindrome has column sums equal to the palindrome's digits. I reproduced the 19 Lean
files byte for byte from Agent 124's archived generator and the module builds. Scaling the same
invariant to k = 4 … 9 gives exactly the counts of the backward batch (5,045 / 5,657 / 5,791 /
5,823 / 5,839 four-digit prefixes at k ≤ 4 … 8, and 5,846 at k ≤ 9), and the reason is
structural: for k = 3 … 7 the forward closure of 196 **equals the recurrent part of the whole
positive abstraction graph** (every word that lies on or downstream of some cycle), and for
k = 3 … 6 that recurrent part is **one strongly connected component**. So the forward invariant is
not specific to 196 (other seeds and later times give the identical set), and at any fixed width
it excludes exactly the prefixes that the backward rank method certifies (all finite ranks at
k ≤ 7 are ≤ 62 < 99, so the backward bound never binds). Scaling it cannot produce exclusions that
a complete backward census at the same width would miss. Its value is computational: one closure
decides every prefix at width k exactly, with no node cap (k = 8 in 66 s / 4.3 GB; k = 9 by a
lifting trick in 1,164 s CPU (20 min wall) / 4.31 GB peak RSS). In Lean I proved the width-3 version of this limit
(the 277 list is optimal for both methods at width 3, from any start time ≥ 100), and I add three new
Lean-verified four-digit exclusions found by the k = 8 census, **2342, 9149, 6676** (not in `main`'s
combined prefix table, not under a `Core` two-digit prefix, and not certifiable at width ≤ 7, so not
in the width-4…7 packages either). To make width 8 buildable I proved a 196-specific endpoint that
needs only the long rows of a rank certificate (`no_196_of_entry_long`): the short-source check at
width 7, which the all-seeds endpoint requires, ran out of memory on this machine (one of its 19
chunk files alone was killed at 5.9 GB peak RSS).

## 2. Claims

### LEAN-VERIFIED

All print exactly the allowed axioms (`propext`, `Classical.choice`, `Quot.sound`, or a subset).

| Module | Theorem | Statement (informal) | Axioms |
|---|---|---|---|
| `P196.Sprint.Agent02.Core` | `reach_from`, `reach_to`, `no_rank_of_from` | generic: breadth-first parent/next trees checked by kernel give forward reachability inside any carry-closed predicate; if every listed word has a listed forward predecessor, every `RowsClosed k` rank function is `none` on all listed words | propext, Quot.sound / + Classical.choice |
| `P196.Sprint.Agent02.W3Final` | `fset_connected` | `Agent124.FwdW3.fset` (4,194 words) is strongly connected under both carries | propext, Quot.sound |
| | `forward_optimal` | every code-keyed set closed under `fwdOK _ 3` that contains the 3-column projection of the 196 orbit at **any** time `100 + s` contains all of `fset` | propext, Classical.choice, Quot.sound |
| | `no_rank_on_fset` | `∀ R, RowsClosed 3 R → R w = none` for every word of `fset` | propext, Classical.choice, Quot.sound |
| | `entryOK_false`, `limit_words`, `limitWords_length` | for the 620 three-digit digit words in `fset`, every width-3 batch entry check `entryOK 3 R (w, b)` fails (any `R` with `RowsClosed 3 R`, any bound `b`), and every forward-closed set as above contains them | propext, Classical.choice, Quot.sound (`limitWords_length`: none) |
| `P196.Sprint.Agent02.Long196` | `rank_long` | along an actual trajectory whose width is ≥ k from the start, a `RowsClosed k` rank after t steps is ≥ t (no `ShortClosed` premise) | propext, Classical.choice, Quot.sound |
| | `orbit196_50`, `canonical50` | `orbit 196 50 = 925153265399993573340628` (24 digits) and its canonical digits | none / propext, Quot.sound |
| | `no_196_of_entry_long` | `1 ≤ k ≤ 24`, `RowsClosed k R`, `entryOK k R (pre, b) = true`, `b ≤ 49` ⇒ `∀ T, ¬ PalStartsL pre (orbit 196 T)` | propext, Classical.choice, Quot.sound |
| `P196.Sprint.Agent02.P2342` | `no_196_2342` | `∀ t, ¬ PalStartsL [2,3,4,2] (orbit 196 t)` (width-8 rank tree `CertK8.ranks`, 17,317 words, ranks ≤ 8, `allRows : RowsClosed 8`) | propext, Classical.choice, Quot.sound |
| `P196.Sprint.Agent02.P9149P6676` | `no_196_9149`, `no_196_6676` | `∀ t, ¬ PalStartsL [9,1,4,9] (orbit 196 t)` and the same for 6676 (width-8 rank tree `CertK8B.ranks`, 102,852 words, ranks ≤ 26) | propext, Classical.choice, Quot.sound |

Together with `Agent124.FwdW3.no_196_excluded` this says: at width 3 the forward method and the
backward rank method exclude exactly the same 277 three-digit words (plus 100, 101, 102, which are
absent from `fset` but fail `noOverflowPre`), and neither can do better at width 3.

### COMPUTED (exact commands in §3; all numbers measured)

1. **Reproduction.** `repro/gen_fwd_agent124.py 3 OUT --leaf 512` (Agent 124's `gen_fwd.py` from tag
   `archive/2026-10-17/research/agent-124/s20261015T1600`) regenerates all 19 files of
   `lean/P196/Agent124ForwardInvariant/A124W3*.lean` byte-identically (after the import-path rewrite).
   `lake build P196.Agent124ForwardInvariant.A124W3Summary` succeeds (118 s wall with dependencies).
   An independent C reimplementation (`src/fwdclosure.c`) gives |F_3| = 4,194, 620 digit words, 277
   excluded — identical.
2. **Forward closures of 196 at time 100** (`src/fwdclosure.c`, k ≤ 8 direct bitset; k = 9
   `src/liftclosure.c` inside the lift of F_8):

   | k | \|F_k\| | positive space 18·19^(k-1) | digit words in F_k | CPU | memory |
   |---|---:|---:|---:|---:|---:|
   | 3 | 4,194 | 6,498 | 620 | <0.01 s | — |
   | 4 | 47,980 | 123,462 | 3,940 | <0.01 s | — |
   | 5 | 497,471 | 2,345,778 | 23,360 | 0.05 s | — |
   | 6 | 4,985,132 | 44,569,782 | 137,214 | 0.39 s | — |
   | 7 | 48,820,141 | 846,825,858 | 785,927 | 4.96 s | 0.22 GB allocated |
   | 8 | 470,163,112 | 16,089,691,302 | 4,452,206 | 65.9 s | 4.25 GB allocated (two bitsets) |
   | 9 | 4,466,505,279 | 305,704,134,738 | 24,965,162 | 1,164 s CPU (20 min wall) | 4.31 GB peak RSS |

   Cross-check: the lifted computation of F_8 from F_7 reproduces the direct F_8 exactly
   (470,163,112 words, 4,452,206 digit words, identical 4-digit exclusion list). F_9 needed 52 passes.
3. **Prefix census** (`src/prefixes.c`; a prefix P is excluded at width k iff `noOverflowPre(P)` and
   no word `P ++ tail`, tail ∈ {0..9}^(k−n), lies in F_k). Cumulative counts:

   | k | 3-digit | 4-digit | 5-digit |
   |---|---:|---:|---:|
   | 3 | 277 | — | — |
   | 4 | 353 | 5,045 | — |
   | 5 | 379 | 5,657 | 66,585 |
   | 6 | 389 | 5,791 | 69,753 |
   | 7 | 390 | 5,823 | 70,415 |
   | 8 | 391 | 5,839 | 70,658 |
   | 9 | 391 | 5,846 | 70,759 |

   The 4-digit column equals the brief's backward batch (5,045@k4, +612, +134, +32, +16@k8). New at
   k = 7: 1660 2386 2429 2518 2589 2641 3121 3181 3185 3585 3898 3916 4254 4937 5492 5493 5523 5524
   5774 5974 5997 6698 7382 7385 7389 7399 8416 8417 8722 9118 9366 9538. New at k = 8: 2342 3749 3958
   3986 4258 4347 4673 5967 6676 7383 7386 7699 7700 9137 9149 9523. New at k = 9: 3537 3899 3984 4307 5838 6311 9123 (seven; the brief reports six found by the capped backward search at k = 9, so one of these was left undetermined there or counted at k = 10 — worth reconciling against the batch lists). Backward closures at k = 9 (`src/backclosure.c`, long words): 4307 1,112,733 nodes / rank 16, 5838 2,082,586 / 26, 6311 3,100,147 / 18, 9123 3,231,156 / 24; 3537, 3899, 3984 exceed the 6,000,000-node cap. The forward exclusion of these three does not depend on conjecture C1 (it is a valid argument by itself), but a Lean certificate for it would have to contain all of F_9, which is out of reach; a backward certificate needs > 6M nodes.
   New three-digit prefixes: 739 at k = 7, 769 at k = 8 (769 is already excluded on `main` through the
   two-digit prefix 76 of `Core`).
   Lists: `data/excl_k{K}_n{N}.txt`, `data/open4_k8.txt` (3,161 four-digit prefixes not excluded at
   k ≤ 8), `data/W3-limit-words.txt` (the 620 width-3 limit words).
4. **The forward closure is the recurrent part of the abstraction** (`src/peel.c`): on all words with
   entries < 19 and q_0 ≥ 1 (the positivity constraint of `SevenColumn.prefixPredecessors`), repeatedly
   deleting words of in-degree 0 leaves the set R_k of words with an infinite backward path. For
   k = 3, 4, 5, 6, 7: **R_k = F_k exactly** (e.g. k = 7: |R_7| = |F_7| = 48,820,141, symmetric
   difference 0; digit words equal). Peeling rounds (= 1 + largest finite rank anywhere):
   10, 21, 49, 56, 63. Without the q_0 ≥ 1 restriction R_k is much larger (k = 6: 17,747,583) because
   of spurious cycles through q_0 = 0 words; with it the equality is exact.
5. **R_k is one strongly connected component** for k = 3, 4, 5, 6 (`src/scc.c`, Kosaraju; e.g. k = 6:
   1 SCC of 4,985,132 words). (k = 3 is also LEAN-VERIFIED above.) Not checked at k ≥ 7 (memory).
6. **Not 196-specific.** The closure from the projection of 196 at t = 1000 and t = 10000, of 89 at
   t = 20, 10911 at t = 40, 1186060307891929990 at t = 100 and of
   123456789012345678901234567890123456789 at t = 0 is bit-identical to F_k(196, 100) for k = 6 and 7.
   A transient start (100000000000000000000000000001, w0 = (2,0,0,…)) gives F_k plus 15 (k = 6) /
   54 (k = 7) transient words.
7. **Backward closures of the 16 new k = 8 prefixes** (`src/backclosure.c`, exact mirror of
   `prefixPredecessors`, self-tested against the forward map; long words only): all acyclic; node
   counts / largest initial rank: 2342 17,315/8, 3749 420,076/43, 3958 482,565/34, 3986 957,377/17,
   4258 662,464/28, 4347 550,690/20, 4673 628,396/32, 5967 990,422/33, 6676 60,089/26,
   7383 182,107/35, 7386 775,840/35, 7699 44,969/15, 7700 352,326/24, 9137 116,759/8,
   9149 42,762/11, 9523 173,828/11. Sanity: 2641 at k = 7 gives 25,624 nodes and rank 5, matching
   `Agent117P2641` (bound 6). Agent 124's `gen_code4.py` (with short words) gives 17,317 nodes for
   2342, 42,762 for 9149, 60,090 for 6676.
8. **Interaction with `Core`.** Of the 3,161 four-digit prefixes not excluded by the census at k ≤ 8,
   11 lie under a `Core` two-digit prefix: 1000 1001 1002 1010 1011 1012 1020 1021 1022 (overflow
   class, outside `noOverflowPre`), 1099, 6599. With `Core`, 5,850 of 9,000 four-digit prefixes are
   excluded by results proved or certifiable at width ≤ 8. 1,289 of the 5,839 census exclusions are
   already implied by `Core`.
9. None of the 14 `Agent117RemainingCycles` prefixes is excluded at k ≤ 9 (consistent).
10. **Real-orbit witness for 4456.** The last predecessor (119 digits) of the palindrome reached by
    1186060307891929990 after 261 steps has its k-column projection in F_k for every k = 3 … 8, so
    4456 is not excludable at any width ≤ 8 by either method (and, by the 261-step backward path, its
    projection has infinite rank whenever the largest finite rank at width k is below 260).
11. Open four-digit prefixes after the k = 9 census: 3,154 (`data/open4_k9.txt`); 11 of them lie under a
    `Core` two-digit prefix (the nine overflow-class words 1000 … 1022, 1099, 6599).

### CONJECTURE

- C1. R_k = F_k(196) and R_k is strongly connected for every k ≥ 3 (checked k ≤ 7 resp. k ≤ 6).
  If true, the forward invariant at width k and a complete backward census at width k exclude the
  same prefixes for every k (as long as the largest finite rank stays ≤ 99).
- C2. The largest finite rank grows slowly with k (9, 20, 48, 55, 62 for k = 3…7). If it stays below
  260 for all relevant k, then 4456 (reached after 261 steps by 1186060307891929990) is never
  excludable by either method at any width ≤ 19 (the seed's width): its last predecessor's projection
  has a backward path of length ≥ 260 and must therefore lie in R_k.

### IDEA

- Any finite abstraction whose recurrent part is a single SCC gives forward ≡ backward. A
  196-specific gain needs an enriched state whose recurrent part splits into several closed classes,
  with 196 provably in a proper one (relevant for assignments 1 and 3).

## 3. Reproduce

```bash
git fetch origin 'refs/tags/archive/2026-10-17/research/agent-124/*:refs/tags/archive/2026-10-17/research/agent-124/*'
bash sprint/agent-02/run.sh              # all COMPUTED items; DATA=/path BUILD=/path to relocate
cd lean
lake build P196.Sprint.Agent02.W3Final P196.Sprint.Agent02.P2342 P196.Sprint.Agent02.P9149P6676
python3 ../sprint/agent-02/src/leantime.py P196/Sprint/Agent02/*.lean   # per-file time / peak RSS
python3 -I ../sprint/agent-02/src/gen_limit.py P196/Sprint/Agent02  # regenerates W3Data.lean
```

The width-8 certificates are regenerated and installed with Agent 124's archived `gen_code4.py`
(copied to `repro/`, with its `scope.py`):

```bash
bash sprint/agent-02/src/install_cert.sh 8 2342 S2K8 CertK8
bash sprint/agent-02/src/install_cert.sh 8 9149,6676 S2K8B CertK8B
cd lean && lake build P196.Sprint.Agent02.P2342 P196.Sprint.Agent02.P9149P6676
```

(the script reproduces the committed files byte for byte; it drops gen_code4's `Short`/`Final`
modules, which `no_196_of_entry_long` does not need).

Lean build measurements, per file, `src/leantime.py` (`lake env lean`, one process per file, imports prebuilt):

| File | wall | peak RSS |
|---|---:|---:|
| `Core.lean` | 0.6 s | 447 MB |
| `W3Data.lean` (two 4,194-node trees) | 110.5 s | 573 MB |
| `W3Check.lean` (all kernel checks) | 69.5 s | 3,695 MB |
| `W3Final.lean` | 2.6 s | 654 MB |
| `Long196.lean` | 0.7 s | 455 MB |
| `A124S2K8Rows000.lean` (one of 32 rows files, 2342) | 4.0 s | 683 MB |
| `A124S2K8BRows000.lean` / `A124S2K8BRows127.lean` (of 128, 9149+6676) | 7.9 s / 11.6 s | 1,007 / 1,209 MB |
| `A124S2K8BEntries1.lean` (one width-8 entry check) | 44.6 s | 5,280 MB |
| `A124S2K8Entries.lean` (2342) | 45.1 s | 4,972 MB |
| `P2342.lean`, `P9149P6676.lean` | 0.5 s, 0.8 s | 433, 520 MB |

Whole builds with `lake build` (2 parallel jobs): 351 s for the first 2342 build (dependencies,
data, 32 rows files and the short-word module that failed), 1,339 s for the 128 rows files of
9149+6676. Every file is within the repository budget (8 GB, 20 min). What did **not**
fit: gen_code4's width-7 short-word check (`ShortClosed 8`) — one of its 19 chunk files alone was
killed at 5,926 MB peak RSS, and an entries module with two width-8 entries was killed at 5,925 MB;
hence `no_196_of_entry_long` and one entry per module.

## 4. What the next agent should do

1. **Stop scaling the forward invariant for new exclusions at a fixed width**; use it as an exact,
   cap-free census instead. Run k = 10 on the Mac: lift over F_9 (bitset of |F_9| · 19 bits ≈
   4,466,505,279 · 19 bits = 10.6 GB each, ≈ 25 GB in total for visited + done, plus a rank directory over F_9); expect ~10× the k = 9 time.
   This settles the brief's 2,091 "undetermined at k = 10" exactly.
2. **Lean-certify the remaining k = 8 (and k = 9) prefixes** with `src/install_cert.sh` +
   `no_196_of_entry_long` (one entry per module, ~5 GB each). By the backward closure sizes in
   COMPUTED 7 the next cheapest are 9137 (117K nodes), 9523 (174K), 7383 (182K), 7700 (352K); the
   rest are 420K–990K; 7699 is already implied by `Core` (prefix 76). The k = 9 ones need 1.1M–>6M
   nodes; 3537, 3899, 3984 probably need a better certificate format.
3. **Assignments 1 and 3**: by COMPUTED 4–6, whenever the backward method fails for a prefix at
   width k ≤ 7, its backward closure contains a cycle, every cycle lies in R_k = F_k, so "forward set ∩
   infinite-rank part of the backward closure" is never empty; assignment 1's candidate list is
   empty at k ≤ 7. An enrichment only helps if it breaks the strong connectivity of the recurrent part.
4. **Prove C1 symbolically** (a "reset" carry sequence from every word to a fixed word) — this would
   turn the width-3 Lean limit into an all-width statement.
5. Coordination note: `AGENTS.md` forbids branches and pull requests; the sprint brief requires them.
   I followed the brief. The new Lean files are not in `lean/registry.json` (the brief forbids editing
   files outside my folders), so `tools/verify.py` will reject them as unregistered until the owner
   registers or moves them.
