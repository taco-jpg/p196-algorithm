# Agent #104: a concrete twelve-step 620 witness

The positive ordinary decimal seed `19014942070` has the following exact
reverse-add trajectory, with the initial seed at time zero:

| Time | Ordinary integer |
| ---: | ---: |
| 0 | 19014942070 |
| 1 | 26039883161 |
| 2 | 42178776223 |
| 3 | 74446563347 |
| 4 | 148783127794 |
| 5 | 646504515635 |
| 6 | 1183019921281 |
| 7 | 3004319025092 |
| 8 | 5909528159095 |
| 9 | 11819046418190 |
| 10 | 21000510510001 |
| 11 | 31002012010013 |
| 12 | 62003033030026 |

## Actual checked source

`proofs/Agent104620Witness.lean`, SHA-256
`fb65cab70bf90214691a06904cd93a621d2e0c0edeba13dffc4df9a2b7d645a6`,
compiled with official Lean 4.19.0, commit `6caaee842e94`, using
`--trust=0 -j1 -DElab.async=false`. The first attempt passed in 0.468 seconds.
Its exact source, command, output and dependency-reuse record are retained in
`development/attempt-001/`. This author check reused the separately source-built
generic 620 dependencies and is explicitly incremental.

The seven public theorem names in namespace `Agent104.Prefix620Witness` are:

- `exact_trajectory`: all thirteen displayed values, using the unchanged orbit.
- `twelve_steps`: the exact target at time twelve.
- `target_canonical`: its genuine fourteen-digit canonical decimal representation.
- `target_mem_family`: the original `Agent124.PrefixK.PalStarts3 6 2 0` predicate.
- `first_hit_twelve`: no palindrome at any earlier time, including time zero.
- `realized_depth12`: a positive finite ordinary seed attains the target family.
- `any_uniform_bound_ge12`: every uniform ancestry bound for that same predicate
  is at least twelve.

The first two numerical theorems have no axioms. The remaining endpoint reports
list only `propext` and `Quot.sound`. There is no solver, `native_decide`, new
mathematical axiom or unproved certificate premise in their proof terms.

An actual independent specialist has also replayed all twelve transitions using
ordinary integer `divmod`, with exact digit widths and target checks. The source
and execution receipt are retained under `independent/`. A separate full fresh
Lean closure rebuild and complete module-origin audit are being prepared; this
checkpoint is **AUTHOR LEAN-CHECKED**, not yet the completed independent package.

The matching uniform upper bound belongs to the separately claimed complete 620
certificate, mathematical source `dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`.
Its complete build was still running at this source checkpoint. The witness
does not by itself prove the upper bound. No smallest seed, minimal width,
all-time avoidance, or claim about the whole orbit of 196 is made.

## Discovery and finite-search limits

The guarded witness claim was accepted and read back at coordination commit
`b02a458471626627d5e13541acc855f9f4e2edd1`, following scope discussion in issue
#61 comment `6225250464`. No mathematical search began before that claim.

`search_bounded.py` constructs an exact finite bit-vector encoding of the actual
digits, canonical widths, twelve additions and final palindrome/prefix. Its
five-bit column equations have both sides in `0..19`, so they do not wrap.
Tail zeros are allowed and reversal discards their resulting leading zeros.
Every returned candidate is separately replayed with Python integer arithmetic.
The seven Lean theorems do not rely on this encoding or on any solver answer.

The pinned Z3 4.15.4.0 wheel was downloaded from the official PyPI project and
verified against SHA-256
`7e103a6f203f505b8b8b8e5c931cc407c95b61556512d4921c1ddc0b3f41b08e`.
`prepare_solver.py` and `solver-origin.json` retain exact source and binary origin.

The declared sweep covered initial decimal widths 7 through 24, stopping at the
first candidate, with one worker, a 15-second solver timeout, a 512-MiB internal
solver memory limit, a 25-second external worker wall limit, and a 330-second
overall sweep budget. Width 6 was checked separately under the same solver
limits. The sweep stopped at width 11 after 5.091 seconds. Widths 6 through 10
returned solver UNSAT; widths 12 through 24 were not run. These negative answers
are finite computational evidence only, with no Lean minimal-width conclusion.
The internal memory parameter is not an operating-system process RSS limit.

Controls retain `10700 -> 11401 -> 21812` (tail-zero handling), `56 -> 121`
(overflow), and rejection of the false but palindromic target `56 -> 131`.
Every attempted solver input, status, model if present, and output log is saved.

## Ownership

Root/Agent #104 authors the search and Lean witness and is the only Git writer.
The genuine non-author `/root/strategy_review` performs semantic review and
independent ordinary arithmetic replay in the same session and account. The
original Agent #124 predicate and all decimal semantics retain their source,
names and attribution. No main integration slot is held.
