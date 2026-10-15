# The seven-column prefix method cannot close the 499 remaining three-digit classes

Agent #117, 15 October 2026. Task `agent117-remaining-prefix-cycle-diagnosis`.

**This is a result about a proof method, not about numbers.** It proves nothing about
196, nothing about decimal Lychrel existence, and nothing about any class of palindromes.
It replaces the resource-limited `CAP` outcomes of the retained exploration records by an
exact answer: for every one of the 499 three-digit prefix classes that the seven-column
program left open, the backward closure of the standard initial set contains a directed
cycle, so no finite rank certificate of the kind used for 217, 218, 620, 739 and 777 exists
at seven columns, for any resource cap. The same holds at eight columns for every class
tested so far. Each verdict carries an explicit witness checked by the forward column
equations, and a representative subset of the witnesses is checked by the Lean kernel
against Agent #104's accepted executable inverse and certificate interface.

## 1. The abstraction (as in the seven-column proof)

Let a realizable pair word be a symmetric word `s = (s_0, …, s_{n-1})`, `0 ≤ s_i ≤ 18`,
`s_0 > 0`, even centre when `n` is odd, and `F(s)` the pair word of the ordinary
reverse-add output (normalize `s` with decimal carries, then fold the digits). For `k ≥ 1`
the `k`-column state of `s` is its first `k` pair sums when `n ≥ k` (a *long* state) and
the whole word when `n < k` (a *short* state).

The forward relation on long states supplies the single unobserved inner carry
`e ∈ {0,1}` freely (`forward_prefixes` in `verify_certificates.py`, `forwardPrefix` in
Agent #104's `ActualPrefix.lean`). The backward relation `Pred_k(p)` is the set of all
long states `s` with `p ∈ forward_prefixes(s)` together with all short words `s` with
`F(s) = p`. For a three-digit prefix `abc`, the initial set `S_0^{abc}` consists of the
long rows `(a,b,c,d_3,…,d_{k-1})`, `0 ≤ d_i ≤ 9`, and the complete short palindrome
words of width `3..k-1` beginning `abc` with even centre. This is exactly the relation and
initial set of `proofs/contributions/2026-10-15-seven-column-prefix/` at `k = 7` (the
implementation here, `prefix_cycles.py`, is independent; `cross_check.py` shows 0
mismatches against `verify_certificates.prefix_predecessors` on 20,000 random states and
reproduces the five accepted closure sizes 58,501 / 59,189 / 186,686 / 38,587 / 151,754).

A **certificate** for `abc` at `k` columns is a finite set `V ⊇ S_0^{abc}` closed under
`Pred_k` with a rank `ρ : V → ℕ` that strictly decreases along every backward edge.
By the coverage lemma of the seven-column proof (and, in Lean, Agent #104's
`actual_mem_prefixPredecessors` and `PrefixCertificate.backPath_length_le`) such a
certificate bounds the ancestry height of every palindrome beginning `abc` by
`1 + max ρ(S_0)`. The leading digit `a ≥ 2` is required for the last-step bridge; for
`a = 1` the initial set must additionally contain the predecessors of overflow
palindromes. Adding initial states can only enlarge a backward closure, so every
`CYCLE` verdict below is unaffected by that caveat; an `ACYCLIC` verdict for a class
with `a = 1` would require the enlarged initial set before it could become a theorem.

## 2. Two elementary lemmas

**Lemma 1 (no certificate with a cycle).** If the backward closure of `S_0^{abc}` under
`Pred_k` contains a directed cycle reachable from an initial state, then no certificate
exists at `k` columns. *Proof.* A rank strictly decreasing along backward edges would
strictly decrease around the cycle. ∎

In Lean this is `Agent117.lookup_none_of_cycle` (file `lean/PrefixCycle.lean`): for
every `tree : RankTree` with `CheckedRows tree prefixPredecessors` (Agent #104's
certificate hypothesis, which every accepted certificate satisfies via
`checkedRows_of_complete_enumeration`), a word with a reachable backward cycle has
`lookup tree p = none`, hence `checkInitial tree bound p = false` for every bound
(`checkInitial_false_of_cycle`). The witness edges are checked by kernel evaluation of
`forwardPrefix`; the new generic bridge `forwardPrefix_mem_prefixPredecessors` (every
`forwardPrefix` edge with boundary carry `< 2` and a positive, `< 19` source is a
`prefixPredecessors` edge, i.e. `ForwardAdmitted ⊆ prefixPredecessors`) turns them into
edges of the executable inverse.

**Lemma 2 (projection).** Dropping the last pair sum maps every `(k+1)`-column backward
walk to a `k`-column backward walk, initial states to initial states, and cycles to
cycles. Hence `CYCLE` at `k+1` implies `CYCLE` at `k`, and a class that is `ACYCLIC`
(closed) at `k` is closed at every larger `k`. *Proof.* Let `s = (s_0,…,s_k)` be long and
`p ∈ forward_prefixes_{k+1}(s)` with inner carry `e`. The low scan of `(s_0,…,s_{k-1})`
is identical. The high scan of `s` from `e` enters column `k-1` with the carry
`e' = ⌊(s_k + e)/10⌋ ∈ {0,1}`, and the `k`-column high scan of `(s_0,…,s_{k-1})` from
`e'` produces the same high digits and the same outer carry. In both the no-overflow and
the overflow pairing, the first `k` output coefficients use only low digits `0..k-1` and
high digits `0..k-1`, so `(p_0,…,p_{k-1}) ∈ forward_prefixes_k(s_0,…,s_{k-1})`. A short
source of width `≤ k-1` is short at both levels with the same exact map `F`; a short
source of width exactly `k` is a long `k`-column state, and `F(s)` is one of its two
forward images since the abstraction admits the actual inner carry. The long initial
rows `(a,b,c,d_3,…,d_k)` project to long initial rows, short initial palindromes of
width `< k` stay short, and a short initial palindrome of width exactly `k` is a long
initial row (its digits are `≤ 9`). ∎

`project_witness.py` applies Lemma 2 to every `k = 8` witness and `verify_witness.py`
re-checks the result at `k = 7` (100 projected witnesses, 0 failures).

## 3. Results (checked computation)

`results/k7.jsonl` has one record per class of
`development/remaining_prefixes.txt` (500 classes: the 499 never closed plus 739).

| k | classes | CYCLE | ACYCLIC | witnesses re-verified by `verify_witness.py` |
|---|---:|---:|---:|---:|
| 7 | 500 | 499 | 1 (739, closure 58,501 = the accepted certificate) | 499 / 499, 0 failures |
| 8 | see `results/k8.jsonl` (partial run, each record final) | all | 0 | all, 0 failures |

Every `CYCLE` record contains an initial state, an entry walk and the cycle. The DFS
stops at its first back edge, so the recorded closure sizes (22,698 to 723,270 states at
`k = 7`) are lower bounds on the closure, not its size.

At `k = 7` the search reached, across all 499 classes, **only three cycles**: one of
length 47, one of length 171 and one of length 1,841 (identical state sets wherever the
same length occurs: 118, 37 and 344 classes respectively). At `k = 8` the first cycles
found are an 8-cycle (one state set), a 5,161-cycle, an 848-cycle and a 307-cycle. The
leading columns of all of them follow the doubling dynamics of the outer pair sum with
alternating overflow, for instance the `k = 8` cycle visits the leading quadruples
`(1,5,10,11) → (2,11,1,3) → (5,2,3,7) → (10,4,6,14) → (1,5,10,11)` twice, with the
unobserved inner carry chosen differently on the two rounds. Nothing is claimed about
the realizability of these cycles by actual integers; the free inner carry is exactly the
information the prefix abstraction discards.

## 4. Results (Lean, kernel checked)

`lean/PrefixCycle.lean` (imports Agent #104's `PrefixInverse`, `FastInverse`,
`PrefixCertificate`, `ActualPrefix`, hence the pinned `LychrelDigitSums`):

| declaration | statement |
|---|---|
| `Agent117.noOverflow_of_scans`, `overflowTail_of_scans` | both deterministic scans satisfy Agent #104's `NoOverflow` / `OverflowTail` column equations for any boundary carry `< 2` |
| `Agent117.forwardPrefix_longCompatible`, `forwardPrefix_mem_prefixPredecessors`, `forwardAdmitted_mem_prefixPredecessors` | every `forwardPrefix s e = p` with `e < 2`, entries `< 19`, positive head gives `s ∈ prefixPredecessors p`; i.e. `ForwardAdmitted s p → s ∈ prefixPredecessors p` |
| `Agent117.walkOK`, `walkOK_sound` | executable checker of a backward walk given with its forward carries; soundness as a `BackPath` |
| `Agent117.backPath_trans`, `backPath_cycle_pow` | concatenation and pumping of `BackPath` |
| `Agent117.lookup_none_of_cycle`, `checkInitial_false_of_cycle`, `lookup_none_of_walks` | Lemma 1 against `CheckedRows tree prefixPredecessors` |

`lean/witnesses/Cycle<abc>_k<k>.lean` (generated by `gen_lean_witness.py`; rows are packed
base-19 naturals decoded by `Agent117.unpack`): for the listed class and `k`,
`no_checked_tree_contains_p0 : ∀ tree, CheckedRows tree prefixPredecessors → lookup tree p0 = none`
and `checkInitial_fails`, where `p0` is a long initial row of the class. Instances are
listed in `README.md` with their build status. Axioms of every exported theorem:
`propext`, `Classical.choice`, `Quot.sound`; no `sorry`, no `native_decide`,
no `Lean.ofReduceBool`. Toolchain: official Lean 4.19.0 (`6caaee842e94`), `lean/build.sh`.

The instances cover all three `k = 7` cycles and the `k = 8` 8-cycle. The other classes
have the same witness format and the generator is mechanical; they are not kernel
checked here only because each instance costs about a minute of kernel time per
thousand edges and the recorded entry walks are up to 3,431 edges long.

## 5. What this does and does not mean

* For the 499 classes, the seven-column rank-certificate method is exhausted at `k = 7`,
  and (Lemma 2 contrapositive does not apply upward, but the data do) at `k = 8` for
  every class tested. Larger `k` can in principle break a cycle, because the
  `(k+1)`-column relation is finer; the only witnesses that survive refinement are those
  the actual dynamics can follow, and whether the three cycles are realizable by actual
  integers for arbitrarily many rounds is not decided here.
* A class with a reachable cycle may still have bounded ancestry height; the abstraction
  over-approximates. Conversely, proving that such a class has unbounded ancestry height
  would require actual integer families with arbitrarily deep ancestries, which is not
  known for any prefix class and is not attempted.
* The five closed classes and 739 are unaffected; so are the concurrent kernel
  formalizations of the 396-class baseline by Agents #104, #113, #118, #119 and #124.
* Nothing about the orbit of 196 follows.

## 6. Reproduce

```sh
cd proofs/contributions/agent-117/remaining-prefix-cycles
python3 -I cross_check.py                      # relation agreement and the five closures
python3 -I run_diagnosis.py 7 1500000 /tmp/k7.jsonl ../2026-10-15-seven-column-prefix/development/remaining_prefixes.txt
python3 -I verify_witness.py /tmp/k7.jsonl     # forward-equation re-check of every witness
python3 -I project_witness.py results/k8.jsonl /tmp/k8to7.jsonl && python3 -I verify_witness.py /tmp/k8to7.jsonl
python3 -I gen_lean_witness.py results/k7.jsonl 936 /tmp/wit   # emit a Lean instance
lean/build.sh <repo-root> <empty-dir>          # fresh Lean build with logs and hashes
```
`run_diagnosis.py` resumes from an existing output file; the `k = 7` run takes about an
hour on one core, `k = 8` about a minute per class.
