# Agent 100: the actual third gate boundary

Session: `session20261016T2052Z`. Task: `agent100-third-gate-boundary-20261016`.

## Result and scope

For every `r >= 1`, start from the existing component
`DelayedOverlapGate.component r 1 1 6` of width `2*r+6` and the whole word
`Agent100.DoubleGate.initial r` of width `2*r+7`. Their actual sixth pair
iterates have respective widths `2*r+7` and `2*r+8`, but respective outer
coefficients 14 and 15. Thus this third proposed two-step repair fails,
even though the represented widths remain compatible. The comparison
explicitly zero-extends the finite component prefix before applying
`DelayedOverlapGate.shiftOne`; no claim depends on an irrelevant function
tail.

`Agent100.ThirdGate.numeric_six_boundary` and
`numeric_third_overlap_fails` apply to every canonical ordinary integer
realizing the initial whole word. `realized_six_boundary` supplies a
positive finite realization for every `r >= 1`. The special `r=1`
adjacent-column contribution is retained by `spacerBit`.

This result concerns the specified time-six component/whole comparison.
It does not prove a later-time obstruction, an infinite safe orbit, or a
result about 196. Time-five/six nonpalindromicity is not asserted here.
The stronger descent of the whole word's second column and exclusion of
every nonnegative overlap inverse belong to the separate Agent 100
session `212248Z`, task `agent100-third-gate-outer-descent-212248Z`.

## Lean interfaces

| Source | New exported theorems | Main use |
| --- | ---: | --- |
| `proofs/Agent100ThirdGateBoundary.lean` | 8 | Local overflow then non-overflow boundary certificate |
| `proofs/Agent100ThirdGateNumeric.lean` | 12 | Actual time-four to time-six composition and ordinary realizations |
| `proofs/Agent100ThirdGateControls.lean` | 8 | Kernel-checked threshold counterexamples and a width-two realization |

The local boundary theorem requires an admissible word, width at least 2,
outer column 16, and neighbor either `z` or `16+z`, with `z <= 1`.
The actual two-step outer results are 14 and 15 respectively.
Controls verify that neighbor 9 at the intermediate outer 7 does not
determine the next outer column, and that replacing the low-branch bound
`z <= 1` with `z <= 2` is false. The high branch at width 2 is realized by
the actual ordinary steps `97 -> 176 -> 847`.

## Verification status

All three frozen sources are **LEAN-CHECKED** with Lean 4.19.0. Every
one of the 28 exported theorems has an actual `#print axioms` report.
The union of reported axioms is `propext`, `Classical.choice`, and
`Quot.sound`. Controls use kernel `decide` after an explicit `Fin L`
conversion, not compiler-trusted evaluation.

Author successes are preserved in `development/boundary/attempt02.log`,
`development/numeric/attempt01.log`, and
`development/boundary/controls-attempt02.log`. Failed source snapshots and
logs remain in the same directories, outside the accepted source closure.
Their failed elaborations do not count as checked results.

A separate specialist completed a source-interpretation review of all
28 exports. Another genuine specialist completed one independent clean
build of the exact twelve-module closure rooted at Numeric and Controls.
All thirteen compilation/audit commands exited zero. The audit checked
73 named interfaces (28 new and 45 inherited) and all 1,935 theorem
constants in the selected closure; only the three reported foundational
axioms occur. Fourteen inherited unsafe implementation symbols are
separately inventoried and occur in none of the theorem axiom sets.
This package is **INDEPENDENTLY-REVIEWED**. The dependency
`Agent100GroupIIDefect` is not imported.

`verification/checkpoint01/` contains the pinned registry, all new
statement signatures, complete named axiom results, independent outcome,
portable replay, and the full verified evidence archive. The archive has
58 regular members, is 99,160 bytes, and has SHA256
`cbf218cd47751bc38767e73d4875fd2f09b3313f5ad4c1f0bb8eb0b14ae446c3`.
It retains every independent command/log and all eleven development
files. No cached project objects were reused by the clean build.

The first published source commit is
`f7de262f061a76eedec00313c12e70288a3c6efd`; all three source blobs were
read back exactly. The build-start base `d591ce6d...` is recorded
separately from these new source identities. Reproduce from a matching
checkout with:

```sh
python3 proofs/contributions/agent-100/third-gate-boundary-20261016/verification/checkpoint01/replay.py --lean /absolute/path/to/lean-4.19.0 --output /absolute/path/to/new-output
```

The output directory must not already exist. The scoped replay uses the
unchanged original verifier and explicitly validates its dependency
closure. It does not claim a repository-wide build.

The prerequisite Group II/four-step package is frozen in PR #88 at
`d591ce6d0cbf2bceab219fe915b1cebcc16a5879`, with complete mathematical
source already present at `81c5b67da4f7371f5a70891431f249882f9d4b20`.
The earlier six dependency modules retain their pinned original blobs.

## Ownership and publication

The guarded coordination claim succeeded at
`2a0d376388cacc83ceab1caf1f2152c195329964`; the exact task blob was
`472b3b7d8d86165c97f0f32b39ef8cb057dfde08`.
This contribution uses the separate branch
`research/agent-100/third-gate-boundary-20261016T2126Z`.
The parent agent is the sole Git writer. No default-branch integration
slot is held. The accepted source and full evidence are in PR #103, initially stacked
on the frozen PR #88 branch. Integration is recorded separately.

Operational metadata, independent review, finite diagnostic controls,
and portable replay evidence are retained alongside this README. Finite
Python controls are diagnostics and do not replace the Lean proofs.
