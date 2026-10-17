# Preserved parent canonical Nine verification

This package preserves the completed parent canonical Nine-cycle run.
Agent #1 specialist `/root/verification_plan` checked and copied the existing
evidence; no Lean command was rerun during packaging. The packager prepared
the scoped registry and authored some earlier dependencies, but authored
neither new Nine proof. Packaging is not an independent mathematical review.

The original `verification.json` reports **PASS** for 34 project modules and
ProjectAudit: 35 actual commands, all exit zero. Its complete module-origin
theorem audit reports **1,547 theorem constants**, with only `propext`,
`Classical.choice`, and `Quot.sound`. The report separately inventories 13
generated unsafe implementation axioms, none permitted as theorem
dependencies. This canonical report does not claim the separate reviewer's
safe-definition audit.

Original start metadata remains unchanged:

- Source commit: `24c29104b6855fe19ad593c0b78fd5ee766a7d26`.
- `source_tree_clean`: `true`.
- Registry SHA256: `d3fca8aa3b055bd287f347a21d132a02c41c6713cdd754fd42a90bf5afcccc80`.

The verifier's clean flag checks tracked-file status and excludes untracked
files. Packaging does not revise that historical value. Every one of the
34 compiled source snapshots and the complete registry was matched against
the exact published commit and current working bytes. The frozen registry's
earlier pending-verification text is preserved; the additive receipt records
the actual completed result without rewriting historical metadata.

All actual Lean argv are retained in `parent-clean-001/verification.json`.
They use `-j1 -DElab.async=false` and **do not explicitly pass `--trust=0`**.
This run is not relabeled as the separate strict reviewer execution. The
official compiler is Lean 4.19.0 release `6caaee842e94`; its original binary
and library hashes are retained. No undocumented compiler defaults are
inferred.

`parent-launch.json` records the exact top-level Python argv and workdir
supplied by the parent executor, session 57928, actual exit zero. Child
argv, exits, and log hashes come directly from the original report.
`parent-console.log` preserves the original console output.

All 71 original manifest entries are copied unchanged into
`parent-clean-001/`, together with its original `FILES.json`. These include
34 compiled mathematical source snapshots, the generated ProjectAudit
source, all 35 logs, and the original report. Compiled objects are excluded,
as they were from the original evidence manifest. `canonical-verifier.py`
and `registry.json` are exact published snapshots.

`publication-source-receipt.json` records every source/build/commit pin
comparison. `parent-result-addendum.json` records the completed result.
`PACKAGE-FILES.json` separately hashes the copies and additive metadata,
including the untouched original manifest. It does not replace that
manifest. `package.py` retains the executed packaging logic, and
`helper-provenance.json` identifies its exact published predecessor.

No original source, report, log, manifest, checker, registry, or Git state
was modified. The result is scoped to this registered closure and does not
assert a repository-wide accepted build. The mathematical positive-seed
endpoint remains conditional on a supplied qualifying full quotient return.
