# Agent #117: exact cycle diagnosis of the 500 remaining seven-column prefix classes

Task `agent117-remaining-prefix-cycle-diagnosis` (claimed on `p196/coordination` at
`43c44c7f322cdd4a43908b9932b4310889b0f648`). Status: **WIP** (diagnosis running; nothing accepted).

**Nothing here proves anything about 196, about decimal Lychrel existence, or about any
palindrome class.** The results are facts about a proof *method*: the k-column prefix
abstraction of `proofs/contributions/2026-10-15-seven-column-prefix/` (the relation of
`verify_certificates.prefix_predecessors` plus the complete short boundary).

## Question

The seven-column program closes a three-digit prefix class `abc` by a finite rank
certificate on the backward closure of `S_0^{abc}` under the k=7 predecessor relation.
Five classes (217, 218, 620, 739, 777) are closed; 500 others ended `CAP` (resource
limit) in the retained exploration records, which leaves open whether a larger cap
would close them. This contribution replaces `CAP` by an exact answer:

* `CYCLE`: the backward closure of `S_0^{abc}` contains a directed cycle reachable from
  an initial state. An explicit witness (initial state, entry path, cycle) is recorded.
  Then **no** rank certificate with strict descent along backward edges exists at this k,
  for any cap. This says nothing about the class itself (the abstraction is an
  over-approximation); it only says the k-column method cannot close it.
* `ACYCLIC`: the closure is finite and acyclic, i.e. a new certificate exists (none found
  so far).

## Files

| file | purpose |
|---|---|
| `prefix_cycles.py` | independent implementation of the k-column abstraction (both branches, short boundary, initial set) and the DFS cycle search; parametric in k |
| `cross_check.py` | compares the predecessor relation against `verify_certificates.prefix_predecessors` on 20,000 random states (0 mismatches) and reproduces the five accepted closure sizes exactly |
| `verify_witness.py` | re-checks every CYCLE witness with the *forward* column equations only |
| `run_diagnosis.py` | batch runner (`K CAP OUT.jsonl PREFIX_LIST`) |
| `results/` | JSONL results per k (added when complete) |

Reproduce: `python3 -I cross_check.py`, then
`python3 -I run_diagnosis.py 7 1500000 results/k7.jsonl ../../2026-10-15-seven-column-prefix/development/remaining_prefixes.txt`
and `python3 -I verify_witness.py results/k7.jsonl`.
