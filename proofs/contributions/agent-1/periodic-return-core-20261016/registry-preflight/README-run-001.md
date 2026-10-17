# ReturnCore registry preflight — provisional

`run-001` completed source metadata preflight with exit 0. The generated
`proofs/Agent1PeriodicReturnCore.registry.json` is explicitly provisional:
the captured OuterRank and ReturnCore sources were still awaiting author
freeze. This preflight performs no Lean compilation or axiom audit and
does not certify proof correctness. No Git or publication action was taken.

The exact DFS closure of the actual `Agent1PeriodicReturnCore` root contains
38 project modules. It includes all four claimed new modules, the required
zero/outer foundations, WidthPath, and CondensationBound. It excludes unused
Width, WidthLift, WidthNumeric, ZeroEscape and their unrelated dependencies.
All module entries include actual imports, source SHA-256, and Git blob IDs
computed directly from bytes without invoking Git.

The three inherited registries are OuterCatalog, ZeroCycle and WidthLift.
All 42 duplicate module-pin encounters agreed exactly. Every inherited pin
used by the new closure also matched the actual current source bytes and
imports. `run-001/report.json` records the exact DFS order and comparison
records; `run-001/registry.json` is the immutable generated snapshot.

No top-level existing project registry supplied a CondensationBound alias.
The authoritative `SOURCE_MAP.json` entry for original
`proofs/contributions/2026-10-14-scc-bound-formal/CondensationBound.lean`
resolves logical module `CondensationBound` to
`proofs/CondensationBound__7ecf1469405ab8d0.lean`. Its actual import is `Std`,
Git blob is `6130c4c54acb9bf9f6f00932084eed66e3b45980`, and SHA-256 is
`04bb2ec87115a532ca91d5d0d453c0062f6c46f030c1fe072ee649db000a0ef8`.
The registry and report preserve this explicit alias provenance.

The accepted immutable claim at
`efe6d4b95f53ad8fbcebf113f8da0616dfa67b22` was read using the GitHub contents
API. Its actual intended-source list includes OuterRank, QuotientPath,
ZeroPath, ReturnCore, this registry and the contribution directory.
`claim.json` retains its original bytes; `claim-read.json` records the API
endpoint and verified Git blob `8fb5aed086fbcf3c2545e518e46be913395acc73`.
This read creates no new claim or scope.

The 14 public theorem endpoints were obtained from the actual four sources:
six in OuterRank, two in QuotientPath, three in ZeroPath, and three in
ReturnCore. Their names and complete source hashes are recorded in the
registry and preflight report. The four exact source snapshots are retained
inside `run-001`; no source endpoint was invented from the proposed claim.

The textual scan masks nested Lean comments and string literals, then checks
every module of the actual closure for `sorry`, `admit`, `sorryAx`,
`native_decide`, custom `axiom`, `implemented_by`, `extern`, `unsafe`,
`ofReduceBool`, and `trustCompiler`. There were no matches. This scan is a
limited source check; complete transitive axiom auditing still belongs to
the fresh build. The sources were rechecked for unchanged bytes before the
registry was written, preventing a mixed-source snapshot during this run.

Reproduction from `/workspace/p196-agent1-return-20261016`:

```
python3 proofs/contributions/agent-1/periodic-return-core-20261016/registry-preflight/prepare.py run-002
```

Use a new run directory each time. This regenerates the provisional scoped
registry from the current actual sources and preserves the preceding run;
it does not upgrade the status to a proof PASS. The parent should run it
again after the source freeze and explicitly update the release metadata
only after inspecting the real author/fresh verification receipts.

Initial registry SHA-256:
`a1209db0637e0e835a22f64e0c3ff4aa767ea3160eff202a3482d25b89820b93`.
Metadata script SHA-256:
`fbb8a8eb87902fae50870ae959731f07151ae4d7379033e8e0bd9633c9b9db9c`.
The accepted global registry and all author sources were untouched.
