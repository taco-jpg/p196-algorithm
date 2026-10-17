# Independent semantic and fresh-build review

PASS for published source `54e1e58b320dfdbe8dc7d2a3ca9e141df9b8ffe2`, registry SHA256 `d76263fe94ddaa93ea5ae364e39c8d3577faa6f6cc7c8b8422428b73b2c4a813`. Current reviewer: Agent #1 specialist `center_review_resume`. I authored none of the new modules or frozen dependency math. Earlier specialist `symbolic_scope` prepared the source interpretation and verification helpers and disclosed prior authorship of some frozen dependencies. That preparation did not execute Lean. All original preparation files remain byte-identical; `resumed-preparation.json` records their hashes. This report describes my new source inspection and actual fresh execution, not execution by the earlier preparer.

## Statement and semantic review

`stripPeriodCenter_wrap w K hw` assumes only `w ≠ []` and returns exact pair equality: the maximal residual of `w ++ K ++ w.reverse` is the residual of `K`, and the count is the count for `K` plus one. `K` may be empty, asymmetric, or already wrapped; `w` need not be primitive. The original empty-period convention remains unchanged and is correctly excluded from this theorem.

The private sufficient-fuel identity uses `H.length ≤ fuel`. At zero fuel, `H=[]`, and a nonempty period cannot pass the reconstruction test. At a successful successor step, the original strict length-decrease lemma yields the induction hypothesis's predecessor fuel bound. At an unsuccessful test both calls stop identically. The public wrapper has length `K.length + (2*w.length-1) + 1`, with the natural subtraction justified by positivity of `w.length`. After its first guaranteed removal, the sufficient-fuel identity equates the remaining call to the original length-fuel call on `K`. Thus the theorem compares literal algorithm results, including the exact count, without a hidden irreducibility or fuel assumption on the public interface.

For the three mixed-nine results let `W9=[9,9,9,9]`, `e=leftEntry B`, `f=rightEntry B H W9`, and `g=rawGamma B H W9`. The assumptions are exactly `Bounded B 18`, `Bounded H 18`, and `e+f=1`. `e` and `f` are the actual original scans; the all-nine blocks transmit these bits. `g` is the actual whole-word terminal carry of `periodicWord B H W9 3`, bounded by the existing scan theorem. It is neither a freely chosen bit nor the outgoing carry of `H`.

The raw result is exactly `W9 ++ R ++ W9`, where `R=pair (fixedDigits H e ++ List.replicate g (9*e))`. Existing `raw_blocks_eq_zipper` identifies the original literal raw center slice. The private zipper proof handles all four combinations of the two mixed orientations and the two possible clocks:

| Actual e/f | Left/right fixed nine digits | g=0 middle | g=1 middle |
| --- | --- | --- | --- |
| 0/1 | nines / zeros | fixedDigits H 0 | fixedDigits H 0 ++ [0] |
| 1/0 | zeros / nines | fixedDigits H 1 | fixedDigits H 1 ++ [9] |

`pair_three_parts` then produces the nine wrapper in each case. The fixed digits deliberately omit `H`'s outgoing carry; the separate pad belongs to the actual full-word clock. This is not a formula for `stepWord H` or standalone normalization of `H`.

No symmetry, even-middle, positivity, minimum length, initial irreducibility, or full `ValidPeriodic` premise is added for `H` or `B`. Empty or all-nine `H` makes the mixed-entry premise impossible because it transmits the same carry; this does not add an unstated exclusion. Small centers and centers with additional nine boundaries remain covered conditionally by the same statements.

The private simultaneous identity derives actual `rawPeriod B H W9=W9` from unchanged `rawPeriod_nines` and the mixed equality, then uses the generic wrapper result. `quotientCenter_nines_mixed` and `centerPeriods_nines_mixed` are precisely the unchanged first and second projections of maximal stripping by actual rawPeriod. All additional removals within `R` remain represented: `centerPeriods` is `stripPeriodCenter W9 R`'s count plus one, with no claim that the total equals one or is bounded above.

No semantic gap was found in these four statements. These are local arithmetic identities. They establish no temporal center descent, no-return theorem, actual cycle, ordinary positive witness, or result about 196. The exact closure imports existing Nines and Quotient with the two new modules; no phase graph, CycleNumeric, or RunAncestry enters this 17-module review.

## Actual verification

The new empty object directory was `/workspace/p196-agent1-session-20261016/nine-center-review-build-001`, outside the Git worktree. All 17 published sources were copied there and rebuilt; no external project objects were reused. The sole reviewer run `clean-001` passed 17 module compilation commands and one full-origin audit command. No reviewer Lean command failed, timed out, or was interrupted. Commands, original source snapshots, logs, resource limits and compiler identity are preserved. Earlier author attempts remain separate with their original outcomes.

Official Lean 4.19.0 binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` was invoked with `--trust=0 -j1 -DElab.async=false`, 8 GiB per-command address-space limit, and 600-second per-command timeout. The current driver is `replay_resumed.py`, copied from the preserved prepared driver with explicit reviewer attribution and four additional literal public `#print axioms` commands. Its exact executed bytes are also retained in `clean-001/replay.py`.

The full module-origin audit checked 1372 theorem constants and 227 safe definitions. The theorem axiom union is exactly `Classical.choice, Quot.sound, propext`; the safe-definition union is `propext`. Only the standard three axioms are accepted. The two new modules contain 18 theorem constants (CenterWrap 6; NinesCenter 12), four public theorems, zero safe definitions and zero runtime definitions. All four public types and literal axiom outputs appear in `clean-001/ReviewAudit.log`; all 74 top-level public Agent1 theorems in this closure were also type-checked. The source scan of all 17 modules masks nested comments and strings and found no `sorry`, `admit`, `native_decide`, `sorryAx`, `axiom` declaration, or `Lean.ofReduceBool`.

The separate implementation inventory records 944 generated non-safe runtime definitions: 916 compilation-stage helpers and 28 unsafe-recursion helpers whose corresponding safe definitions were audited. It records 13 inherited compiler implementation axioms, zero unsafe opaques, and no unclassified runtime definitions. No such implementation entry occurs among accepted theorem or safe-definition axiom dependencies. This inventory is not a proof shortcut or repository-wide acceptance.

The exact registry, imports, minimal closure, published source bytes, and evidence source snapshots were checked again while sealing. The initial source pin records the source-only stage honestly; this report and the execution receipt record the later completed execution. Coordination check-in 6228459948 was POSTed and GET-read back successfully. The initial unsupported `gh --slurp` attempt was a coordination-tooling failure, corrected with supported `gh api --paginate`; it was not a Lean failure and is preserved in the coordination record. No math source, registry, or Git state was written by this reviewer.
