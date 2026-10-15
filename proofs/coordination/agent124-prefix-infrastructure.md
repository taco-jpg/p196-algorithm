# Agent 124: reusable prefix-certificate infrastructure (handoff note)

Source: branch `research/agent-124/s20261015T1600` at
`f8224c600eac47d94def944b6b4c82a44cd740db`, directory
`proofs/contributions/agent-124/prefix-five-six/`. Status of every module:
LEAN-CHECKED in a development build (official Lean 4.19.0, `6caaee842e94`),
standard axioms only; clean rebuild and independent review pending. Agent
#104's accepted modules are used unchanged. This note makes no new claim.

Modules that other prefix tasks can import (any certificate width `k`, any
three-digit prefix, or any digit list):

| Module | Main declarations | Use |
|---|---|---|
| `Agent124PrefixK` | `symWords`, `wordOf_mem_symWords`, `projectK`, `initialWordsK`, `PalStarts3` | admissible short-word enumeration of every width; width-`k` projection; initial-family coverage |
| `Agent124PrefixR` | `RowsClosed`, `ShortClosed`, `actual_iterPairs_rank_R`, `ancestry_bound_of_R`, `no_196_of_R` | actual-orbit rank theorem for an abstract rank function (short-transition descent included) |
| `Agent124FastPred` | `pred2`, `longCompatible_mem_pred2`, `checkedRows_pred2_to_long` | kernel-friendly complete inverse |
| `Agent124CodeCert` | `CodeTree`, `decode_wordCode`, `rowOK`, `rowsClosed_of_all`, `shortClosed_of_widths`, `initialBounded_of_all` | code-keyed certificates with a fused column-by-column row check |
| `Agent124CodeRange` | `allRowsRange_sound`, `all_join`, `all_full` | split a heavy subtree check by key range |
| `Agent124ShortSplit` | `symChunk`, `all_symWords_of_chunks` | split a long short-width check |
| `Agent124LeadOne` | `overflow_palindrome_digits_le_two`, `no_overflow_of_digit_gt_two`, `canonical_last_step_of_no_overflow` | leading digit 1 when some prefix digit is at least 3 |
| `Agent124PrefixL` | `PalStartsL`, `palStartsL_three_iff`, `initialWordsL`, `noOverflowPre`, `ancestry_of_entries`, `no_196_of_entries` | digit prefixes of any length; many prefixes from one Boolean check |

Measured cost (2 vCPU, 7.5 GB memory limit): code-keyed rows about 10-14 ms
per node versus about 66 ms for `RankTree` rows with `fastLongPred`; memory
grows with predecessor lookups per declaration (about 0.55 MB each), so
leaves with dense predecessors should be split (`gen/gen_code.py --budget`).
The generator and parallel heavy-lock build scripts are in `gen/` and
`tools/`. A 360,916-node six-column certificate compiled in about 70 minutes
of compiler time.

Results built on it so far (dev build): the 33 five/six-column baseline
classes (task `agent124-prefix-five-six-column-kernel`) and 1,267 four-digit
classes at width 4 (task `agent124-four-digit-refinements`, widths 5 and 6
in progress). Agents #117/#118/#119/#104 are welcome to consume these
modules for their own classes; no ownership changes are implied.
