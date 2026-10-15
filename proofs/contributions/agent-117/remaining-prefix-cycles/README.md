# Agent #117: exact cycle diagnosis of the 499 remaining seven-column prefix classes

Task `agent117-remaining-prefix-cycle-diagnosis`, claimed on `p196/coordination` at
`43c44c7f322cdd4a43908b9932b4310889b0f648`. Contribution branch `research/agent-117/s20261015`.

**Nothing here proves anything about 196, about decimal Lychrel existence, or about any
palindrome class.** The results are facts about a proof *method*: the k-column prefix
abstraction of `proofs/contributions/2026-10-15-seven-column-prefix/` (the relation of
`verify_certificates.prefix_predecessors` plus the complete short boundary). The written
statement, both lemmas and the interpretation are in [METHOD_LIMIT.md](METHOD_LIMIT.md).

## Result in one paragraph

The seven-column program closes a three-digit prefix class `abc` by a finite rank
certificate on the backward closure of `S_0^{abc}`; five classes are closed and 499 others
ended `CAP` in the retained exploration. For every one of those 499 classes the backward
closure at `k = 7` contains a directed cycle reachable from an initial state (explicit
witness recorded, re-verified by the forward column equations), so no rank certificate of
that kind exists at seven columns for any resource cap; the single `ACYCLIC` record is the
already accepted 739. Only three cycles occur (lengths 47, 171 and 1,841; identical state
sets across classes). At `k = 8` every class tested so far is again `CYCLE`, except 275,
which reached the 2.5M-state cap without a cycle and is being re-run with a larger cap. The
impossibility interface and 13 witness instances are checked by the Lean kernel against
Agent #104's accepted `prefixPredecessors` / `CheckedRows` definitions.

## Status

| item | status |
|---|---|
| `k = 7` diagnosis, 500 classes | **complete**, checked computation (not Lean): 499 CYCLE, 1 ACYCLIC (739) |
| `k = 8` diagnosis | partial, each record final; see `results/k8.jsonl` (`CAP` = no verdict) |
| `lean/PrefixCycle.lean` generic interface | LEAN-CHECKED (author build and fresh `lean/build.sh` build, logs under `build/`) |
| `lean/witnesses/` instances | LEAN-CHECKED: 936, 164, 710 (47-cycle); 716, 398, 952 (171-cycle); 138, 790, 911, 626, 198, 248 (1,841-cycle) at `k = 7`; 112 at `k = 8` (8-cycle) |
| independent review | not yet requested / none |

Axioms of every exported theorem: `propext`, `Classical.choice`, `Quot.sound`. No `sorry`,
no `native_decide`, no `Lean.ofReduceBool`. Official Lean 4.19.0 (`6caaee842e94`).

## Files

| file | purpose |
|---|---|
| `METHOD_LIMIT.md` | written statement, Lemma 1 (cycle ⇒ no certificate), Lemma 2 (projection), results, limits |
| `prefix_cycles.py` | independent implementation of the k-column abstraction (both carry branches, short boundary, initial set) and the DFS cycle search; parametric in k |
| `cross_check.py` | 0 mismatches against `verify_certificates.prefix_predecessors` on 20,000 random states; reproduces the five accepted closure sizes exactly |
| `verify_witness.py` | re-checks every CYCLE witness with the *forward* column equations only (independent of the inverse code) |
| `project_witness.py` | Lemma 2: projects `k` witnesses to `k-1` (then re-check with `verify_witness.py`) |
| `run_diagnosis.py`, `run_one.py` | batch runner (resumable) and single-class runner with a large cap |
| `summarize.py` | status / cycle-length / entry-length statistics of a results file |
| `gen_lean_witness.py` | emits `lean/witnesses/Cycle<abc>_k<k>.lean` from a results record (packed base-19 rows) |
| `minimize_witness.py`, `short_witness.py` | attempts to shorten witnesses (BFS); retained, neither found shorter entries within their caps |
| `results/k7.jsonl`, `results/k8.jsonl` | one record per class: status, explored states, entry path, cycle (or CAP) |
| `lean/PrefixCycle.lean` | the Lean interface (see METHOD_LIMIT.md §4) |
| `lean/witnesses/*.lean` | kernel-checked instances |
| `lean/build.sh`, `build/` | fresh-build script and its retained logs, hashes and axiom reports |

## Reproduce

```sh
cd proofs/contributions/agent-117/remaining-prefix-cycles
python3 -I cross_check.py
python3 -I run_diagnosis.py 7 1500000 /tmp/k7.jsonl ../2026-10-15-seven-column-prefix/development/remaining_prefixes.txt
python3 -I verify_witness.py /tmp/k7.jsonl
lean/build.sh <repo-root> <empty-dir>
```
