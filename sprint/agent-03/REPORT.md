# Sprint agent 03 — enriching the forward state

Assignment 3: add 196-specific information (mod-99 phase, mod 11, width parity, carry into the
outer block, width mod m) to the k-column forward abstraction and measure how much the
forward-reachable set shrinks per added component.

## 1. Answer

**None of the suggested components shrinks the forward-reachable set by a single word.** Every one of them (n mod 99, n mod 11, n mod 9, width mod m, time mod 6, the inner carry used
on the previous step) is updated from the previous value, the word and the carry without ever
forbidding a carry; for any such update the least enriched invariant projects *exactly* onto the
plain forward closure (LEAN-VERIFIED, `EnrichedNoGain.lean`). The measurements agree: in 63 enriched
runs at k = 3..6 the projection is bit-identical to the plain closure, and for every global
quantity the enriched set is even the full product |F_k| × |E| (no joint information either). The
underlying reason is structural (COMPUTED): at k = 3..7 the forward closure F_k of 196's state at
t = 100 is *exactly* the set of words with infinite backward rank, and that set is one strongly
connected component which the 196 orbit enters at t = 2, 2, 4, 7, 8 (k = 3..7) — so starting later
gives no shrink either. The forward route's four-digit exclusions at width k have exactly the
batch generator's cumulative backward counts (5,045 / 5,657 / 5,791 / 5,823 / 5,839 at k = 4..8,
and every backward-certified entry published in the repo is among them), and conversely no backward
certificate can ever certify a word of this forward closure (LEAN-VERIFIED for k = 3..7,
`CycleRank.lean`). The Lean theorem covers enrichments without a guard; that no *guard* on the free
carry can come from residues, width or outer digits is only COMPUTED: every combination (word,
carry, residue mod 99 compatible with 196, width mod 12) was realized by an actual integer,
exhaustively at k = 3 and for 2,000 sampled words at each k = 4..7. The only
component that shrinks the set is **the next column**: π_k(F_{k+1}) is 11.4–16.7 % smaller than F_k
(k = 3..8). Lifting through F_8, the width-9 closure (4,466,505,279 words) excludes **5,846**
four-digit prefixes — one more than the 5,845 the brief lists for backward search at widths ≤ 9
(COMPUTED, not Lean-verified). Nothing here proves anything about palindromes of 196 beyond what is
listed below.

## 2. Results

### LEAN-VERIFIED

Both files build with the repo lakefile (`lake build P196.Sprint.Agent03.CycleRank`), no `sorry`,
no `native_decide`, no custom axioms. Measured with `lake env lean <file>` on this sandbox:
`EnrichedNoGain.lean` 2.0 s / 430 MB, `CycleRank.lean` 2.5 s / 562 MB. They are **not** in
`lean/registry.json` (I must not edit it), so `tools/verify.py --changed` currently fails only with
"unregistered Lean file" for these two modules. With the ready entry `registry_entry.json` merged
into `lean/registry.json` locally (not committed), `python3 tools/verify.py --changed` printed
`[axioms] 17 endpoints checked` and `ALL CHECKS PASSED (changed files only, against origin/main)`.

`lean/P196/Sprint/Agent03/EnrichedNoGain.lean` — all endpoints depend on **no axioms**:

| theorem | statement |
| --- | --- |
| `Sprint.Agent03.proj_iff` | for any `X`, any `δ : X → List Nat → Nat → X`, `(∃ x, EReach δ w0 x0 w x) ↔ Reach w0 w` (`Reach` = closure under `forwardPrefix · e`, `e ≤ 1`) |
| `enriched_invariant_covers` | any `S : List Nat → X → Prop` closed under `(w,x) ↦ (forwardPrefix w e, δ x w e)` and containing `(w0,x0)` contains some `(w,x)` for every `Reach w0 w` |
| `no_new_exclusion` | hence `(∀ x, ¬ S w x) → ¬ Reach w0 w`: an enriched invariant excludes nothing the plain closure keeps |
| `overflow_driven_no_new_exclusion` | the same for updates `upd x (highDigits w e).1` (residues, width mod m) |
| `reach_sub_invariant` | `Reach w0` is contained in every plain forward-closed set containing `w0` |

`lean/P196/Sprint/Agent03/CycleRank.lean` — endpoints depend on `[propext, Classical.choice, Quot.sound]`
(`fp_head_pos`, `wordPrefix_q100`: `[propext, Quot.sound]`):

| theorem | statement |
| --- | --- |
| `rank_descent` | along a forward walk of `n` steps (good words: length k, entries < 19, head > 0) any `R` with `Agent124.PrefixR.RowsClosed k R` drops by ≥ n |
| `rank_none_of_cycle`, `no_rank_of_cycleOK` | if `w0` returns to itself under `forwardPrefix` (positive length), then `R w = none` for every `w` with `Reach w0 w` |
| `entryOK_false_of_cycleOK` | for such `w0` and a `k`-digit `pre` with `Reach w0 pre`: `Agent124.PrefixL.entryOK k R (pre, bound) = false` for every bound |
| `wordPrefix_q100` | `wordPrefix Agent124.Forward.q100 k = [8,8,13,9,14,14,14].take k` (k ≤ 7) — the projection of `orbit 196 100` |
| `no_rank_3` … `no_rank_7` | every word of `Reach (wordPrefix q100 k)` has no rank under any `RowsClosed k` function (cycle witnesses of 17, 22, 28, 28, 42 steps, checked by `decide +kernel`) |
| `entryOK_false_3` … `entryOK_false_7` | no batch entry for a `k`-digit prefix in that forward closure can pass `entryOK k` (prefixes of length exactly k only; e.g. four-digit prefixes at width 5..7 follow the same way but are not formalised) |

Together with the existing `Agent124.Forward.no_196_outside` (which excludes everything *outside* a
forward-closed set containing the time-100 projection): at k = 3..7, every k-digit prefix the
backward batch method can certify at width k is also excluded by the forward closure. The
converse inclusion is only COMPUTED (below).

### COMPUTED

All runs on this sandbox (2 cores, 8 GB RAM, Linux, gcc -O3). Reference model `fwdref.py` mirrors
the Lean definitions literally; its self-test shows the forward relation equals the converse of
`prefixPredecessors` exhaustively at k = 2, 3 (513 and 9,747 edges) and matches 221,277 random
(integer, k) pairs of actual reverse-and-add. `orbit196.c` agrees with Python big integers for
t ≤ 3,000; the orbit to t = 200,000 (82,927 digits) has no palindrome.

**C1. Plain forward closure F_k from w(196,100) = [8,8,13,9,14,14,14,3,11,…]** (`fwdbfs`, `fwdlift`)

| k | \|F_k\| | all words 18·19^(k−1) | fraction | words with 2 distinct successors | 4-digit prefixes excluded |
| --- | --- | --- | --- | --- | --- |
| 3 | 4,194 | 6,498 | 64.5 % | 2,035 | — (277 three-digit = `Agent124ForwardInvariant`) |
| 4 | 47,980 | 123,462 | 38.9 % | 23,152 | 5,045 |
| 5 | 497,471 | 2,345,778 | 21.2 % | 238,457 | 5,657 |
| 6 | 4,985,132 | 44,569,782 | 11.2 % | 2,376,057 | 5,791 |
| 7 | 48,820,141 | 846,825,858 | 5.77 % | 23,148,265 | 5,823 |
| 8 | 470,163,112 | 16,089,691,302 | 2.92 % | 222,036,860 | 5,839 |
| 9 | 4,466,505,279 | 305,704,134,738 | 1.46 % | — | 5,846 |

Checks: k = 3,4,5 bitsets equal a pure-Python BFS (`chk_bfs.py`); the k = 3 three-digit exclusion
count is 277, equal to the repo's `Agent124.FwdW3.excluded_length`; all 757 + 6 entries of branch
`prefix-k45-certificates` are forward-excluded at their certificate width, and all 1,730 four-digit
entries of `Agent124FourDigit` are forward-excluded at k = 5 (1,267 of them already at k = 4). Newly excluded four-digit prefixes per width: 612 (k=5),
134 (k=6), 32 (k=7), 16 (k=8) — identical to the brief's backward per-width counts — and **7 at
k = 9: 3537, 3899, 3984, 4307, 5838, 6311, 9123** (the brief lists 6 at k = 9; I do not have the
batch lists, so I cannot say which one is the extra prefix or whether the backward search reached
its node cap on it). k = 8 run: 230 s, 4.1 GB; k = 9 lift: 1,027 s, 4.5 GB.

**C2. Enrichments** (`gen_tables.py` builds each automaton and checks it is sound along the actual
orbit for t = 100..200,000; `fwdbfs K table`), k = 3..6, full output in `results/enrich_k3-6.txt`:

| component E | update | \|E reachable\| | \|Reach(W×E)\| | projection vs F_k |
| --- | --- | --- | --- | --- |
| width mod m, m ∈ {2,3,4,5,6,7,8,10,12} | (E + b) mod m | m | m·\|F_k\| exactly | identical |
| (n mod 99, width mod 2) | rev ≡ n (9), rev ≡ (−1)^(L−1) n (11) | 12 | 12·\|F_k\| | identical |
| (n mod 11, width mod 2) | same, mod 11 | 2 (n ≡ 0 mod 11) | 2·\|F_k\| | identical |
| n mod 9 | 2E mod 9 | 6 | 6·\|F_k\| | identical |
| t mod 6 (196's mod-99 phase is a clock) | E + 1 | 6 | 6·\|F_k\| | identical |
| previous inner carry e | e | 2 | 5,261 / 58,076 / 595,281 / 5,905,802 | identical |
| previous (b, e) | (b, e) | 4 | 5,769 / 61,395 / 614,069 / 6,010,260 | identical |
| (n mod 99, width mod 12, prev e) | combined | — | 72 × (prev-e count), k ≤ 5 | identical |

(b = overflow bit `(highDigits w e).1`.) Shrink of the forward set per added component: **0 words** in
all 63 runs. The full-product sizes mean these quantities are also jointly uninformative: every
reachable word occurs with every reachable residue/phase/width class. Only "previous carry" is not
a full product (some words are entered only through e = 0 or only through e = 1), but it still
projects onto all of F_k.

**C3. Why: F_k is the whole recurrent core** (`peel`, `scc`, `results/peel_scc.txt`)

| k | \|F_k\| = \|R_k\| (infinite backward rank, Kahn peeling of all 18·19^(k−1) words) | max finite rank (any word) | \|SCC(w100)\| | max BFS distance from w100 | orbit enters SCC at t | shortest cycle through w100 |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 4,194 | 9 | 4,194 | 31 | 2 | 17 |
| 4 | 47,980 | 20 | 47,980 | 52 | 2 | 22 |
| 5 | 497,471 | 48 | 497,471 | 83 | 4 | 28 |
| 6 | 4,985,132 | 55 | 4,985,132 | 93 | 7 | 28 |
| 7 | 48,820,141 | 62 | 48,820,141 | 121 | 8 | 42 |

An independent uncapped k = 7 run on the Mac Studio (`~/p196-forward-check`, global graph of
846,836,325 nodes = the 846,825,858 long words plus the 10,467 admissible short words of widths 1..6)
found the same single nontrivial component of 48,820,141 nodes and the same entry time t = 8.
So F_k = R_k = one SCC at k = 3..7, and F_k(t0) = F_k for every start time t0 ≥ the entry time —
a later start is not an enrichment that helps. At k = 8: w(196,100) lies on a forward cycle
(it is in the closure of w(196,101), and |F_8(101)| = |F_8(100)| = 470,163,112), hence F_8 ⊆ R_8;
R_8 ⊆ F_8 was not checked (the in-degree array needs 32 GB). Same at k = 9: w(196,100) is in the
closure of w(196,101) and |F_9(101)| = |F_9(100)| = 4,466,505,279, hence F_9 ⊆ R_9
(`results/cycle_check_k8_k9.txt`; 1,024 s, 4.5 GB).

**C4. Middle information does shrink the set** (`settool proj/diff`, `fwdlift`): |π_k F_{k+1}| / |F_k| =
3,716 / 4,194 (−11.40 %), 40,907 / 47,980 (−14.74 %), 421,312 / 497,471 (−15.31 %),
4,206,465 / 4,985,132 (−15.62 %), 40,936,006 / 48,820,141 (−16.15 %),
391,459,503 / 470,163,112 (−16.74 %) for k = 3..8; π_k F_{k+1} ⊆ F_k in every case.

**C5. No guard is possible from these features** (`realize.py`, `results/realize.txt`): for every
word of F_3 (exhaustive) and 2,000 sampled words of F_k, k = 4..7, every carry e ∈ {0,1}, every
residue r ∈ {0, 11, …, 88} mod 99 and every width class l mod 12, an explicit integer with exactly
that projection, actual inner carry c_{L−k}, residue and width class was built and checked with
exact arithmetic (905,904 + 4 × 432,000 realizations). So no statement "(word, residue, width class)
⇒ carry ∈ G" with G ≠ {0,1} holds for integers; a sound guard has to know middle digits.

### CONJECTURE

- F_k = R_k (forward closure of 196 = infinite-rank region) and R_k is a single SCC for every k ≥ 3.
  Checked k = 3..7; at k = 8 and 9 only F_k ⊆ R_k (196's state is on a cycle), plus at k = 8 the
  agreement of the four-digit counts with the backward batch (5,839).
- If so, at every width the forward route and the backward rank route exclude the same prefixes
  (up to the rank ≤ 99 requirement of the backward route, which the forward route does not need).
  Computing F_10, F_11, … forward then settles, *within the abstraction*, which of the brief's
  2,091 "undetermined" prefixes are excludable at each width. A prefix that stays inside F_k is
  not shown to occur in 196's orbit, and forward exclusions at k ≥ 8 have no Lean certificate.

### IDEA

- The only way an enrichment can help is a *guard* on the free inner carry, i.e. orbit-specific
  information about the middle digits that is preserved by the step. Global residues, width, time
  and outer digits are ruled out (C2, C5, Lean). Width is the cheap honest version of "more
  middle information".
- Lean-verifying forward exclusions at k ≥ 8 cannot go through an explicit closed set (10^8–10^9
  words). A scalable route: a Boolean checker over a *compressed* closed set (e.g. a DFA over the
  column word recognising a superset of F_k that is still forward closed), proved correct once.

### Independent review

A separate review agent (no access to my reasoning) recompiled both Lean files, used `no_rank_4` with
the repo's real width-4 certificate (`Agent124.CertF4.allRows`) to confirm `RowsClosed` is not vacuous,
re-implemented `forwardPrefix` from the Lean definition, and reproduced |F_3|..|F_7|, the 2-successor
counts, π_3 F_4 = 3,716, the L-mod-2 product (8,388 states), R_k = F_k at k = 3, 4, the SCC sizes and
BFS radii at k = 3..7, the entry times at k = 3..6, the exclusion counts 277 / 5,045 / 5,657 / 5,791 /
5,823, the enrichment counts, the orbit value at t = 100 and the absence of palindromes to t = 200,000.
It could not check k = 8, 9 (memory), the brief's counts or the `verify.py` run. Its corrections
(a reversed sentence in the `CycleRank.lean` docstring, and wording in sections 1 and 2 that
overstated the sampled realizations and the reach of the forward classification) are applied above.

## 3. Reproduce

```bash
git checkout sprint/agent-03-enrich-state
# Every COMPUTED number above (k ≤ 8 direct, k = 9 lifted, plus all checks: fwdref self-test,
# orbit vs big integers, C vs Python BFS, SCC/cycles, k = 8, 9 cycle test). Here: ~50 min, ~4.6 GB peak.
bash sprint/agent-03/run_all.sh /tmp/a3work 8 9
# k = 10 on the 32-core / 512 GB Mac: direct k = 9 (two 40 GB bitsets), then lift to 10 (~2 × 11 GB)
bash sprint/agent-03/run_all.sh /tmp/a3work 9 10
# Lean (from the repo's lean/ directory)
cd lean && lake build P196.Sprint.Agent03.EnrichedNoGain P196.Sprint.Agent03.CycleRank
```

Programs: `fwdbfs.c` (closure, optional enrichment automaton), `fwdlift.c` (width k+1 indexed through
F_k; `QUERY=` membership), `peel.c` (infinite-rank region), `scc.c` (SCC + BFS distances),
`settool.c` (projection, difference, excluded prefixes), `orbit196.c`, `gen_tables.py`,
`realize.py`, `cycle_bidir.py` (bidirectional cycle search; too shallow for k ≥ 7, use `scc` +
`entry_and_cycle.py`), `memtime.py` (wall time + peak RSS). All single-threaded.

## 4. What the next agent should do

1. **Width, not enrichment.** Run `run_all.sh WORK 9 10` on the Mac (direct k = 9 needs ~80 GB, the
   k = 10 lift ~25 GB) and continue lifting (k = 11 needs F_10 as a full bitset, 766 GB — instead
   generalise `fwdlift` to index through a compressed F_k). Each width gives a complete classification
   of all four-digit prefixes *within the abstraction* (excluded at width k or not), with no node cap;
   compare with the 2,091 undetermined. These are computed exclusions, not Lean certificates.
2. **Identify the extra k = 9 prefix** among 3537, 3899, 3984, 4307, 5838, 6311, 9123 against the
   batch lists, and run the backward search on it without a node cap (or check whether its rank
   exceeds 99, which the forward route does not need).
3. **Agent 1 / agent 18 interface:** C3 says the forward abstraction from 196 adds nothing over the
   backward cycle analysis at k ≤ 7, and C2/C5 say residue × prefix cannot be won inside this
   abstraction. Effort there should target information about the middle digits.
4. Register the two Lean files (`registry_entry.json`) if the integrator wants them on `main`.
