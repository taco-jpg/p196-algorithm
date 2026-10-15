# The complete well-founded part of the pure k-column prefix abstraction, k = 4..7

Agent #117, 15 October 2026, task `agent117-remaining-prefix-cycle-diagnosis`.
**Checked computation, not Lean.** No statement about 196 or about any palindrome class is
made; this catalogue says exactly which prefix classes the *pure* k-column rank-certificate
method (the relation of `verify_certificates.prefix_predecessors` with the standard initial
set, Section 1 of METHOD_LIMIT.md) can close, and with which bound, for every prefix length
3..k and every k from 4 to 7.

## 1. One computation per k instead of one search per class

The per-class searches of the seven-column program explore the backward closure of a
class's initial set; the whole-space computation (`wellfounded7.cpp`) instead computes, by
Kahn's algorithm over *all* long states (`18·19^(k-1)` of them) plus the 10,467 complete
short words, the set of states whose backward closure is finite and acyclic together with
their ranks (`rank p = 0` if `p` has no predecessor, else `1 + max` over predecessors).
A state is unbounded iff some predecessor never receives a rank. Forward images are
computed once per state (two inner carries), so no predecessor enumeration is needed.
A class of `D` leading digits is closed at `k` columns iff every long initial row with that
prefix and every complete short palindrome word (width 3..k-1, even centre) with that prefix
is bounded; its bound is `1 + max rank` (the extra step is the final carry-free addition).

| k | long states | bounded long states | max rank | closed classes, D = 3 | D = 4 | D = 5 | D = 6 | D = 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 123,462 | 75,482 | 20 | 357 / 900 | 5,060 / 9,000 | – | – | – |
| 5 | 2,345,778 | 1,848,307 | 48 | 383 | 5,673 | 66,640 / 90,000 | – | – |
| 6 | 44,569,782 | 39,584,650 | 55 | 393 | 5,807 | 69,808 | 762,786 / 900,000 | – |
| 7 | 846,207,882 | 798,005,717 | 62 | 394 | 5,839 | 70,470 | 782,063 | 8,214,073 / 9,000,000 |

Classes whose three leading digits are 110, 111, 121 or 122 (the only prefixes a palindrome
produced by an overflow last step can have; none of the four is closed at any k) would need
the overflow predecessors in their initial sets; the four-digit refinements 1120 and 1121 are
the only "closed" entries affected and are excluded from every count that follows.

## 2. Validation

* The `k = 4` graph statistics reproduce the baseline four-column report exactly: 75,482
  long states of finite rank, maximum rank 20 (`p196_four_column_obstruction.md`, Section 4).
* The five accepted seven-column certificates are reproduced exactly: 217 → 23, 218 → 34,
  620 → 12, 739 → 39, 777 → 25.
* An independent per-class Python computation (`rank_certificate.py`: backward closure plus
  Kahn ranks with the `prefix_cycles.py` relation) agrees with the catalogue on every closed
  three-digit class and on the tested open ones: 357/357 at `k = 4`, 383/383 at `k = 5`,
  393/393 at `k = 6`, 394/394 at `k = 7` (logs in `results/cross_k*.txt`).
* The compact outputs (`results/rows_rank<k>.bin.gz`, `results/short_rank<k>.tsv`) rebuild
  every class table through `class_table.py`; the rebuilt tables agree with the C++ tables.
* Agent #124's exploratory counts of four-digit refinements of the 499 open three-digit
  classes (1,267 at width 4, 463 at width 5, 100 at width 6, excluding 1120/1121) are
  reproduced exactly: 1,269 − 2, 463, 100.

## 3. Relation to the 396-class baseline (relevant to Agents #113, #119, #124)

The baseline four-column method is not the pure abstraction: for a *descending* prefix
(`b < a`) it restricts the first backward edge to the no-growth branch by a whole-word
argument (`p196_four_column_obstruction.md`: "若 b<a，第一条逆向图边还可限定为 N"). In the pure
abstraction

* **109, 659 and 769 are not closed at any k ≤ 7** (each has one unbounded initial row; at
  `k = 7` the row `(1,0,9,9,9,9,9)` reaches the 1,841-cycle through `(10,9,9,9,9,9,9)`). Their
  kernel certificates need that descending-prefix lemma, or an equivalent whole-word fact,
  and cannot come from `prefixPredecessors` rows alone.
* The other 393 baseline classes close purely: 357 at `k = 4`, 26 at `k = 5`, 10 at `k = 6`.
  Agent #124's 24 five-column and 9 six-column classes close purely at exactly those widths.
* Three pure bounds at the minimal closing width exceed the baseline bound (which used the
  lemma): 217 → 34 at `k = 5` (23 at `k = 7`), 329 → 5 at `k = 4` (baseline 2), 429 → 24 at
  `k = 5` (baseline 22). Eighteen pure `k = 7` bounds are smaller than the baseline bound.

## 4. What is new relative to the record

* The complete list of closed classes at every prefix length 3..7 and k ≤ 7, with bounds,
  is in `results/` (rebuild with `class_table.py K results D --list-closed`).
* Four-digit refinements of the 499 open three-digit classes that close purely at `k = 7` but
  not at `k ≤ 6`: see Section 5. Each such class, once kernel-checked (the width-generic
  infrastructure of Agents #118/#124 applies), would be a new statement of the 739 kind:
  no palindrome beginning with those four digits lies in the orbit of 196 after the bound.
  No such Lean instance is built here, and no claim is made before one is.
* The seven-digit level is the finest the pure `k = 7` method can see: 8,214,073 of the
  9,000,000 rows are bounded, 785,927 are not. Every open class at every coarser level is
  open because it contains at least one of those rows.

## 5. Four-digit classes newly closed at k = 7

Excluding the 739 refinements and 1120/1121, the four-digit refinements of the 499 open
three-digit classes close purely as follows: 1,269 at `k = 4`, 463 more at `k = 5`, 100 more
at `k = 6` (these 1,832 are Agent #124's 1,830 plus 1120 and 1121), and **31 more at
`k = 7`**, with their `k = 7` bounds:

```
1660:23 2386:17 2429:11 2518:9 2589:48 2641:6 3121:13 3181:11 3185:11 3585:25 3898:16
3916:8 4254:29 4937:10 5492:14 5493:14 5523:7 5524:7 5774:22 5974:8 5997:26 6698:42
7382:44 7385:20 7389:44 8416:15 8417:15 8722:40 9118:25 9366:12 9538:9
```

Nine of the ten refinements of each rule-only class also close purely at `k = 7`
(1090..1098 with bound 1, 6590..6598 with bound 6, 7690..7698 with bound 3; the x9 refinement
contains the cyclic row in each case). All of these are checked computations with the
written coverage argument of the seven-column proof; none is a Lean theorem here.

The compact data for all of this are `results/catalogue/rows_rank<k>.bin.gz` and
`results/catalogue/short_rank<k>.tsv` (rebuild any level with
`python3 -I class_table.py K results/catalogue D --list-closed`), the `D ≤ 4` tables
`classes<k>_D34.tsv`, the C++ stderr summaries, the cross-check logs and
`summary.txt` (from `summarize_catalogue.py`).
