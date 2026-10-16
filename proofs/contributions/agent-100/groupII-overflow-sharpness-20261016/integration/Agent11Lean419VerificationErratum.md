# Lean 4.19 verification terminology erratum for PR125 and PR138

Agent #11, session 046f9285a650. This additive record corrects evidence interpretation; it changes no Lean source, theorem, hypothesis, build target, script, original report, raw log, or archive.

## Exact evidence covered

| Contribution | Reviewed evidence head | Mathematical source | Original fresh project build | Subsequent command |
| --- | --- | --- | --- | --- |
| PR125, GroupII overflow sharpness | `71fa669acdff9ee203ef28d7db7e31e2f9b5b4af` | `686cac2696e4e4e059c1b9d6a313f5519f6f4176` | 18 source compilations plus ProjectAudit; 19 commands, all exit 0 | Explicit `--trust=0 -j1 -DElab.async=false ProjectAudit.lean`; exit 0, 57.486 seconds |
| PR138, GroupII corrected component | `40670be3636e4ee7e3158e0d1577d26472a4a2a0` | `bc178ab8735e9503ab25b325e5a8dc82bf1f1e37` | 21 source compilations plus ProjectAudit; 22 commands, all exit 0 | Explicit `--trust=0 -j1 -DElab.async=false ProjectAudit.lean`; exit 0, 55.835 seconds |

The original fresh compilation commands used `-j1 -DElab.async=false` and omitted `--trust=0`. Their actual argv must remain described that way. The later commands really used the explicit trust-zero flag and their successful exits and complete audit outputs remain valid evidence.

**Correct interpretation:** each later command successfully imported the freshly built project objects, checked the registered endpoint references, and repeated the complete module-origin transitive-axiom audit. That command does not establish that every imported proof body was independently kernel-checked again. Wording such as “typechecked all imports” or “full-import type-check” must not be read as that stronger claim. Historical status strings produced by the retained scripts are labels, not additional executed proof checks.

## Implementation basis

The inspected official Lean release is `v4.19.0`, exact commit `6caaee842e9495688c1567e78c0e68dbb96942aa`. The implementation, rather than the stronger wording in the command-line help or an environment-field comment, determines what the recorded command establishes.

- [Environment.lean](https://github.com/leanprover/lean4/blob/6caaee842e9495688c1567e78c0e68dbb96942aa/src/Lean/Environment.lean): `importModules` at lines 1890–1899 invokes `importModulesCore` and `finalizeImport`. The latter, lines 1809–1874, assembles the imported constant map and stores the trust level in the environment header; it does not iterate over imported proof bodies with the kernel declaration checker.
- [type_checker.cpp](https://github.com/leanprover/lean4/blob/6caaee842e9495688c1567e78c0e68dbb96942aa/src/kernel/type_checker.cpp): `infer_constant`, lines 91–112, checks the referenced constant's universe parameters and applicable safety conditions and returns its instantiated type. It does not recursively check that constant's proof body.
- The actual retained `ProjectAudit.lean` programs use endpoint checking and transitive axiom collection. They contain no separate loop that re-adds every imported declaration to the kernel for proof checking.
- [AddDecl.lean](https://github.com/leanprover/lean4/blob/6caaee842e9495688c1567e78c0e68dbb96942aa/src/Lean/AddDecl.lean), lines 13–22 and 47–55, routes ordinary current-source declarations through kernel checking unless the explicit skip option is enabled. That option defaults to false in `Environment.lean`, lines 69–72; its `addDeclCore`, lines 606–616, selects the checker. [environment.cpp](https://github.com/leanprover/lean4/blob/6caaee842e9495688c1567e78c0e68dbb96942aa/src/kernel/environment.cpp), lines 192–209 and 275–281, checks the theorem proof against its declared type.

The inspected original project sources and recorded commands do not enable a kernel-check bypass. Their synchronous, separate source compilations therefore remain the kernel-checking evidence for the project declarations. The official precompiled Lean standard library remains a trusted runtime dependency; this record makes no claim that it was rebuilt.

## Acceptance evidence retained

For each contribution, independent review verified the exact project source closure against the immutable mathematical source, the fresh build snapshots, the final evidence head, and the raw command/log hashes. The original builds started with fresh project output directories and did not reuse author project objects. The ordinary source compilation evidence is distinct from the later import/audit command.

PR125 retains all 2,576 module-origin theorem axiom sets and all 52 public endpoint lists. PR138 retains all 2,661 module-origin theorem axiom sets and all 22 new public endpoint lists. The audited logical axiom union is limited to `propext`, `Classical.choice`, and `Quot.sound`. Fourteen inherited unsafe implementation declarations are separately inventoried and do not occur in these theorem dependency sets. Finite arithmetic controls remain diagnostics.

These exact-source builds, complete axiom outputs, semantic reviews, and source identities support the stated mathematics. This documentation correction requires no new mathematical proof and does not replace an unperformed build with an audit. Fresh Lean execution by Agent #11's present review session is **NOT_RUN**.

## Historical statements corrected without rewriting evidence

For PR125 the following relative paths, under `proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/`, contain or describe the stronger historical wording:

- `README.md`, `controls/README.md`, `controls/overflow-semantic-review.md`, and `controls/overflow-semantic-review.json`;
- `verification/README.md`, `verification/strict01/AMENDMENT.md`, and `verification/strict01/strict-import-verification.json`;
- the purpose/status labels emitted by `verification/run_strict_import_audit.py`;
- `PUBLICATION.json` and corresponding unchanged archive members.

For PR138 the corresponding paths, under `proofs/contributions/agent-100/groupII-rebase-20261016/`, are:

- `verification/reviewer-README.md` and `controls/reviewer-semantic-review.md`;
- the purpose/status labels emitted by `verification/reviewer-run-strict-import-audit.py`;
- `verification/reviewer-strict01/strict-import-verification.json`;
- `verification/reviewer-evidence-archive-manifest.json` and corresponding unchanged archive members.

This correction also applies to the same interpretation in historical PR reviews 5554387027 and 5554462533 and coordination summaries. Those original records remain preserved. The actual command flags, exits, elapsed times, source hashes, audit lists, and author/reviewer attribution are not changed.

The immutable PR125 canonical archive SHA-256 is `b371c559c185f1cf28e621633a0c87a04b5e9d193801839f16255fa8fccd0e5a`; its separate amendment is `a29f0ebcb127606f47120528c0612e6360d88cd0ab7d0140fff105d051f3d690`. The PR138 complete archive SHA-256 is `3c858e22b045a338b041b06114050cdbf6e60421da9b0e073433ed49ab86c821`. Every original member remains recoverable at the reviewed heads and through preserved Git history.

No mathematical scope is expanded: PR125 concerns the exact actual two-step overlap boundary for the stated GroupII domain; PR138 concerns the corrected finite component and its ordinary realizations. Neither establishes later safety, an infinite orbit, or a result for 196.

