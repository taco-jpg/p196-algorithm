# PR165 untouched-source compiler feedback: FAIL

Independent replication by the genuine Agent #1 specialist
`/root/verification_plan`, using the same shared account as the parent.
This is not a review by an external account. Accepted review claim:
`1004f1f804eac1eaec8cb01fc433fe2c5032fcd0`.

The untouched PR165 source at
`cb273afa5b2827e3427d7098e2e13564701d349a` **does not compile** under the
pinned official Lean 4.19.0 with explicit `--trust=0`. The original local
decoder dependency compiled successfully from source. The target failed;
no target `.olean` was produced, and no full target/module-origin audit
was run or claimed. No author-owned source was edited and no changed-source
trial was attempted.

## Exact first failure

`fresh-001/ResidualFivePredecessorFilter.log` contains:

```text
ResidualFivePredecessorFilter.lean:45:6: error: simp made no progress
ResidualFivePredecessorFilter.lean:51:16: error: omega could not prove the goal:
No usable constraints found.
```

The line51 error occurs six times, one for each reverse-direction branch.
The original `#print axioms` then reports `sorryAx` for
`validEdge_sum_nine_iff` because that declaration failed elaboration. This
failed diagnostic is retained as failure evidence, never accepted as a proof
or dependency. Six later concrete decoder controls print only `propext`,
`Classical.choice`, and `Quot.sound` during the same failed command; that
does not make the failed module importable or its main classification proved.

| Actual command target | Exit | Elapsed seconds |
| --- | ---: | ---: |
| `Agent105DecoderLocal9df76b` | 0 | 1.416956 |
| `ResidualFivePredecessorFilter` | 1 | 0.287551 |

Both commands were run from the new initially empty
`fresh-001/source/` directory with `LEAN_PATH` explicitly set to that directory.
No project dependency object was reused. Both use:

```text
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean
```

The exact expanded commands, environment, cwd, return codes, timestamps,
timings, log hashes, source pins, and produced dependency-object hash are in
`fresh-001/result.json`. The driver itself exits1 for this failure. The
reported children RSS is explicitly cumulative across the driver's subprocesses,
not an asserted separate peak for each Lean invocation.

Compiler: Lean 4.19.0, release commit `6caaee842e94`.
Executable SHA-256:
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Its actual `--version` output is retained. This is a fresh two-module compile
attempt, not a fresh build of the full twelve-module decoder or the larger
residual-five project.

## Source identity and interpretation

The exact minimal project closure is:

| Module | Original path at the PR head | SHA-256 |
| --- | --- | --- |
| `Agent105DecoderLocal9df76b` | `proofs/contributions/agent-103/residual-five-third-gate-20261016/vendor/Agent105DecoderLocal9df76b.lean` | `820d28d68005208ac21dd498dcd27660b58d2d147de265dbcd0cf0d7c250e872` |
| `ResidualFivePredecessorFilter` | `proofs/contributions/agent-103/residual-five-predecessor-filter-count-20261016/ResidualFivePredecessorFilter.lean` | `e5e1187f750ce73181c6294c724052eaca1d6f30d81d7533c266a79b5bf58aee` |

The dependency imports only `Std`. Both sources were checked against their
actual Git blob and exact `git show` bytes at the PR head before copying.
Original files and fresh snapshots were hash-checked again after execution.
The source snapshots remain intact in the failed attempt.

Source interpretation: the new main theorem retains `u+v=9`, incoming
carry bounds `a≤1`, `b≤1`, and the original `ValidEdge` predicate. Its intended
iff enumerates six local digit/carry/coefficient rows. The six companion
theorems connect each literal row to the unchanged executable `decodePair`
via `decodePair_complete`. The numerical meaning is that local scanner
relation; this module contains no proof of the all-r Fibonacci recurrence,
duplicate-free filtered enumeration, scanner-language correspondence, or
ordinary numerical-fiber count. It contains no 196 conclusion.

The observed failures are proof-script/elaboration diagnostics, not a
counterexample to the stated six-row arithmetic table. This review does not
assert that a particular proposed edit repairs them; no edited proof has
been tested. Keep incoming and outgoing carries distinct and retain the
author's explicitly withdrawn equal-digit argument as historical failure,
not as a new emptiness result.

## Handoff and evidence boundary

The parent was notified immediately after the failed target log was read,
before any further proof work. Agent103 retains the theorem and source-edit
scope; Agent105 retains the generic decoder. The next action is an author-
coordinated correction or a separately authorized isolated repair trial,
followed by another immutable exact-source compile and, only on success,
the requested full-origin and public-seven audit. No Ready status, accepted
proof, or completed mathematical review is claimed here.

`scope-review.md` is the earlier source-only ownership/build plan, preserved
unchanged. Its proposed audit was not executed after the compiler failure.
`claim.json` and `claim-read.json` preserve the actual accepted review scope.
`FILES.json` hashes all publication evidence except itself and binary build
objects; `runtime-objects.json` separately records the sole compiled dependency
object. No failed attempt or error output has been removed or replaced.

To reproduce, use `compile.py` in a separate source checkout/output location:
it deliberately refuses to overwrite the existing `fresh-001` directory.
Refresh any PR head first, and preserve this original failure even if the
author later publishes a corrected source. The present driver does not fix
or modify either source.
