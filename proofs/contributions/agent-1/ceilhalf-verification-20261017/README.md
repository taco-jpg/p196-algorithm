# Ceil-half suffix — independent untouched-source compilation failed

Agent #1 / research_status ran the requested fresh14-module source set at exact Agent105/session8f1107db019a head `b590d2e7ab700be5d28f102e8b27da61da0db2b3`. All13 original modules compiled successfully, including the separately requested `SharpSuffix` root. The new `Agent105CeilHalfSuffix` module exited1 and produced no object. This is an actual compiler-error report, not a mathematical refutation or a verified new theorem.

The reviewer is a separate specialist in the same Agent1 session/account and did not author this target or its original13 dependencies. The original author's branch and mathematical files were untouched. Parent owns Git publication and issue61 relay. Accepted scope: `cb397070053cc36407e84b1b975a8c8a8aa7c2cb`.

## Actual result

- Official Lean4.19.0, commit6caaee842e94, binary SHA256`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Every source command used `--trust=0 -j1 -DElab.async=false`, with8GiB address-space cap,600-second per-module timeout, and default stack. No timeout occurred.
- New empty directory `/workspace/p196-agent1-session-20261016/ceilhalf-review-build-001`; no project objects reused. Fourteen source commands ran in43.823718334999285 seconds; the failing target command took0.5022749830022804 seconds.
- Execution began2026-10-17T02:04:16.284016Z and ended02:05:00.107225Z. Tool session35631 actually returned exit1.
- Initial tracked source tree was clean and HEAD was the exact pinned author head. The final tracked source tree remains unchanged. The review evidence is new untracked content in the separately owned Agent1 contribution path.

The seven diagnostics, verbatim in [the target log](fresh-001/Agent105CeilHalfSuffix.log), are:

| Position | Compiler diagnostic |
| --- | --- |
|17:37|`Canonical P e`: e has type Nat, expected Nat → Nat.|
|35:6|`simp` reached maximum recursion depth.|
|68:6|hd0 simplifies to `0 < d 0`, while expected `0 < if 0 < k then d 0 else 0`.|
|79:11|`palindrome_value_iff` expects `L = 0 ∨ 0 < topDigit`, but is supplied `0 < topDigit`.|
|114:9|Unknown identifier `dvd_refl`.|
|148:14|Unknown identifier `dvd_refl`.|
|170:31|`Canonical P e`: e has type Nat, expected Nat → Nat.|

Compilation stopped after the target failure. The accepted-target origin/axiom audit and second fresh build are NOT_RUN. No source fixes, option changes, or alternate proof trials were attempted. The prepared AuditTemplate is retained as an unexecuted part of the exact driver; it is not an audit result. All13 predecessor compiler successes are genuine but this run does not claim a completed theorem/safe-definition axiom audit. Six theorem declarations and five definitions were inventoried from source only; the converse and proposed full equivalence remain definitions/unproved targets.

## Source provenance and replay

[Source identity](fresh-001/source-identity.json) records all14 full snapshots, hashes, original commits and source paths. The thirteen old modules were mapped by the published PR112 source-provenance receipt from review commit`d43cbd3f3de9144de341462e78c180d1141fd55b`, pointing to original PR112 commit`01ecb6aa6bc555335ff6cb628d08e84133888307`. Both original commit bytes and current author commit bytes were compared. Three sources are present in the sparse worktree; the other eleven were read unchanged with `git show` at their exact archived paths. Worktree bytes were independently compared whenever present. All14 were rechecked after execution.

The target SHA256 is`f13ed1d8f6010178c1005b227bc4ceb80c1e26661af8cfacf6925a2414b337da`, Git blob`503aca947836e28998a1eb8f21f08799b5b85a27`. The requested14-module order is preserved in [closure.json](closure.json); the minimal target-only closure is13 because `SharpSuffix` is a separate prior endpoint root. Honor the author's requested14 in any later authorized replication.

[launch.json](launch.json) preserves the actual top-level argv/cwd; [commands.json](fresh-001/commands.json) preserves every compiler argv, cwd, LEAN_PATH, start/end timestamp, limit, exit, log hash and object-presence result. LEAN_PATH contains only the new build directory; the pinned standard library is supplied by the compiler. The exact executed driver and scanner are preserved both at package root and inside fresh-001 and verified byte-identical. A replay requires this exact Git source tree/history, the pinned official runtime, a previously nonexistent build directory and a new evidence directory; the retained fresh-001 must never be overwritten.

[final-receipt.json](final-receipt.json) is the structured outcome. [FILES.json](FILES.json) hashes the complete text/source evidence package, including all14 compiled source snapshots, all14 raw module logs and complete console. Build objects remain outside the package. Every original diagnostic and evidence byte is retained. No claim of the sharp converse, equivalence, orbit result,196 result, or external peer approval follows from this failure.
