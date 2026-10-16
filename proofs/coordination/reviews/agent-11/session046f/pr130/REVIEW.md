# PR 130 exact-source independent review

**PASS for the mathematical contribution and retained verification evidence at head `8a67ea8204757cc4f80bf5f576e2cc8024bea97b`. Fresh Lean execution by this reviewer: `NOT_RUN`.** No statement-preserving repair is needed. This is a nonauthor review by Agent #11's `/root/review130` specialist in session `046f9285a650`; it does not assert a distinct GitHub account or constitute a platform approval.

The parent remains responsible for current PR metadata/checks, ownership, the final moving-main combination, and any merge mutation. This report does not assert that those separate gates passed.

## Frozen scope and source identity

| Item | Exact value |
| --- | --- |
| PR head H | `8a67ea8204757cc4f80bf5f576e2cc8024bea97b` |
| Frozen current main B | `fa3921e58556250b1a6efd30af603fb65a9d9fbc` |
| Actual merge base M | `89287c9d3eb7dd801c2b1a59eff03140d47d24ec` |
| PR 91 integration | `e423f12c0bb7881fabd2ece40c9f68076a2dc97e` |
| Agent #11 review claim supplied by parent | `8dbd35b190deefe66436f4cf5a6c92867c9ce35c` |
| Original mathematical checkpoint | `6ce47fddb10f15b4af1025954f1694825093673d` |

I independently derived the merge base and confirmed that the PR 91 integration commit is an ancestor of B. The full M-to-H diff contains 145 added files, all beneath `proofs/contributions/agent-3/three-layer-prefix-20261016/`; it changes no existing source, workflow, security setting, build target, or historical record. All changed file bytes were retrieved. JSON files and Python ASTs were parsed; the four mathematical modules, their necessary original semantics, verifier implementations, documentation, original diagnostics, failed attempts, and source-preservation records were inspected. Large structured inventories and every raw verification log were checked completely by the retained audit script rather than relying on summary counts.

All 27 source modules match both retained executions by SHA-256, byte count, imports, and Git blob identity. Every module's original commit/path resolves to its claimed blob, including the original Agent #9 sources. All 23 inherited proof sources are byte-identical at H, M, B, and the PR 91 integration commit. The latter comparison also covered the inherited verifier, Agent #9 pins, and the scoped repository reproduction documents. The four additions exactly match the original mathematical checkpoint.

| New module | SHA-256 |
| --- | --- |
| `DeadPrefix.lean` | `09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64` |
| `ActualDepth.lean` | `dcc9655c0fe9f60419fc60b821e225f705f3ce713792419586d623125ca9d0e2` |
| `SharpHistoryFamily.lean` | `6e3b02999b118ed00133d7bebdbf553a6f19d6bfaec4f6abbf982ab7ee2fb002` |
| `SharpHistoryTheorem.lean` | `d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29` |

The accepted build entry is the contribution's portable `verification/verify.py` plus `verification/source-pins.json`. Its topological 27-module list explicitly includes all four additions, ending in `SharpHistoryTheorem`; each appears exactly once in both original compile command sequences. This is a standalone scoped build, not a claim that a repository-wide default target or all of main was rebuilt. Repository reproduction documentation itself identifies the global catalogue as incomplete and the core build as scoped.

## Mathematical and ordinary-integer review

The original `Local` relation uses coefficients below 19 and both decimal carry equations. `Path` retains equal list shapes and the terminal even-center condition `low p = high p`. `Forced` is a uniqueness implication, not an existence assertion; this is sufficient for exclusion. Nine finite rows are proved by ordinary kernel `decide` after unfolding `Forced`. The original arithmetic forces the following prefixes:

| Incoming layer | Target prefix | Predecessor prefix | Carry states after columns |
| --- | --- | --- | --- |
| First | `[14,14,14,5]` | `[7,7,7,2]` | `0,0,0,1` |
| Second | `[7,7,7,2]` | `[3,13,13,0]` | `1,3,2,1` |
| Third | `[3,13,13,0]` | `[1,16,16]`, then impossible | `1,3,2`, then no `Local 0 2` |

The contradiction occurs before any suffix or center assumption is used, so every target tail is covered. The final ancestor remains an arbitrary `List Nat`; the bound needed to package each peeled entry as `Fin 19` comes from the original `Local` premise. No unchecked historical graph table is a proof dependency.

The original `ActualFiber ss xs` means equal half-width, every coefficient below 19, zero final scan carry, and `Agent8.stepWord (mirror xs) = mirror (ss.map Fin.val)`. The complete unchanged `actual_realizes` and `realizes_path` converses transport each of three actual fibers to the original paths. Existing actual two-layer witnesses use the converse direction and the unchanged accepting two-history paths. `ExactlyTwoZeroCarryLayers` therefore asserts genuine two-layer existence and exclusion of every third layer in this same relation, not a vacuous bound.

The protected family fixes exactly `[true,true,false]` before the arbitrary length-m Boolean suffix. Its protected half begins `[14,14,14,5]`. Existing injectivity followed by cancellation of the fixed prefix gives `2^m` distinct initial coefficient words and `2^m` distinct protected coefficient words. Both widths are exactly `2*(m+k+10)`. The two-step word image agrees with the protected enumeration in order. The separate canonical-chain theorem retains the actual terminal carries `0,0,1` and the overflow target `target (m+9) k` for `k>0`.

The integer bridge is substantive and nonvacuous: `IntegerRealizes n w` uses the original finite `Canonical` decimal representation, with positive width, digits at most nine, nonzero leading digit, and value n. Even width discharges the unpaired-center parity condition in `valid_word_realizable`; `CanonicalPair` alone is not silently treated as sufficient in odd width. Every initial word has a positive ordinary integer realization, and the safety assertion applies to every realization. Original decimal reversal consumes ordinary digits and drops leading zeros after reversal; it is not fixed-width string reversal. The original definitions are `step n = n + reverse10 n`, `Palindrome n := reverse10 n = n`, and `orbit n 0 = n`.

For every m and k>0, every realization of each listed initial word is positive and avoids palindromes at every natural time `t <= k+3`, including both endpoints. The ordinary value at time four is `digitValue (target (m+9) k)`. The displayed coefficient list may contain 14 or 18; `digitValue` evaluates its finite base-ten polynomial, not a string of decimal digits. The time-three normalized integer and its next numeric step account correctly for the time-four equality. The construction depends on the prescribed finite horizon. This establishes neither a fixed seed with infinite avoidance nor any result about 196.

The additional predecessor exclusion preserves all premises: `2*ys.length = w.length`, every coefficient below 19, and `terminalCarry (mirror ys) 0 = 0`. It covers same-width mirrored zero-carry candidates. Different widths, incoming overflow, mixed schedules, unrestricted numerical ancestry, and an infinite-time conclusion are outside the theorem. Exact ancestry and counts allow k=0; the advertised combined ordinary-safety result explicitly requires k>0.

## Retained verification, independently reconciled

The user's role permits reuse of trustworthy exact-source evidence when closure, environment, and scope match. Here both retained executions compile exactly the 27 verified source bytes using Lean 4.19.0 release commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The canonical record also retains the installed Init/Std/Lean root-object hashes. Their commands stage only exact sources into separate new module directories, clear inherited Lean path/options overrides, set `LEAN_PATH` to that directory, and use `--trust=0` for every compilation and diagnostic audit. No preexisting project objects are used by those full builds.

| Original execution | Recorded interval on 2026-10-16 UTC | Commands | Reconciled result |
| --- | --- | ---: | --- |
| Agent #3 independent nonauthor reviewer | 22:15:55.699147–22:17:21.932536 | 29 | PASS: 27 builds plus version and complete ownership audit |
| Agent #3 canonical verifier | 22:19:19.567193–22:20:47.650697 | 31 | PASS: 27 builds, version/prefix, inventory, complete axiom audit |

Every raw log hash matches its command record; every recorded command exits zero, with no warnings or errors. The complete exact argument vectors, original paths/environments, exit codes, and actual committed-log hashes are in `original-commands-and-log-identities.json`. The canonical report hashes the exact verifier and manifest currently at H. The independent source freeze and all relevant published sources match the reviewed bytes. The original independent review candidly distinguished its observed local commit from a parent-reported remote checkpoint; this review resolves that distinction by checking the now-available published checkpoint blobs directly.

Both raw ownership inventories independently parse to the same 620 constants from 17 contribution modules. Both full raw `#print axioms` outputs parse to exactly the same 373 safe, nonpartial logical constants. This includes every one of 231 explicit declarations, all three inherited private helpers, all 52 new explicit declarations, and all 69 new safe constants. The 247 generated unsafe/partial implementation constants are inventoried separately; none is an explicit accepted source declaration. Every explicit declaration maps uniquely to a safe audited compiled constant. No definition or private helper is omitted merely because it is not a theorem.

The complete transitive audit union is exactly `Classical.choice`, `Quot.sound`, and `propext`. All 27 source files pass the inspected strict scan after comments and strings are removed. There is no `sorry`, `admit`, `sorryAx`, unsupported axiom, `native_decide`, `Lean.ofReduceBool`, explicit unsafe/partial shortcut, or accepted source metaprogramming bypass. Diagnostic `run_cmd` files inventory already compiled declarations and issue ordinary `#print axioms`; they are not accepted mathematical sources.

The predecessor verifier differs only in its description and the addition of the new audited namespace. This byte-for-byte adaptation was independently checked. Its 14 guard outcomes are correctly labeled inherited evidence, not a fresh execution. All 35 canonical artifact-index entries, all independent review-manifest entries, and every package-index entry match their byte counts and hashes.

Fresh Lean execution in this review is **NOT_RUN**. The parent reported the ordinary launcher's `error: failed to locate application` and a prior automatically rejected escalation. This reviewer did not retry, escalate, or seek another execution route. Original trusted execution remains attributed to the original verifiers above. Current fresh work is source/provenance/log auditing, not proof re-execution.

## Preservation and fresh review evidence

The six retained author attempts were checked against their complete source snapshots and raw logs. `DeadPrefix` attempt 001 fails because `Forced` was not unfolded for decidability; attempt 002 changes only the nine proof bodies to unfold it. `ActualDepth` attempt 001 leaves the finite coercion of 18 unresolved; attempt 002 supplies the literal value identity. Both original failing logs remain, alongside four successful final-source attempts. Their incremental cached-dependency checks are labeled as such and are superseded for clean-closure coverage by the two full original builds. The dependency preflight refusal, packaging refusal, and resource-cleanup preflight are retained as historical records.

The historical checkpoint, generator, and saved 4/16/65-state data were checked against their exact archived Git blobs, sizes, and SHA-256 values. Their original bytes are recoverable at H. The generator was inspected, not run. Its finite data remain historical observations; the new theorem neither assumes nor certifies the entire graph. Cleanup records exclude only reproducible compiler objects and a byte-identical runtime download wrapper, not mathematical attempts or evidence.

Fresh Python audit attempt 1 passed 718 explicit conditions; the separate preservation audit passed for all six source attempts, including two expected historical failures. No fresh checker attempt failed. No Lean process, source edit, remote write, branch mutation, PR review, or security change was performed. Optional testing stopped after the acceptance question was resolved.

`publish-evidence/` contains all new scripts, complete machine results and raw new logs, the full diff, provenance/command manifests, and exact recovery maps for the original committed bytes. The 174-entry recovery map identifies commit, path, Git blob, byte length, and SHA-256; it permits exact restoration with `git show <commit>:<path>`, followed by hash verification. Original sources and logs are not reclassified as new execution. `REVIEW.md` is the review result; `EVIDENCE_MANIFEST.json` inventories the final handoff files.
