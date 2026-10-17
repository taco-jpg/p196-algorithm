# Preserved parent canonical verification

This package preserves the already completed parent canonical ReducedCore run.
Agent1 specialist `/root/research_status` verified and copied its existing
evidence; no Lean command was rerun during packaging. The parent executed the
build. The packager authored the earlier EighteenClock dependency, so this
packaging action is not an independent mathematical review.

The original `verification.json` reports **PASS**, with 48 project modules plus
ProjectAudit: 49 actual commands, all exit 0. Its complete module-origin theorem
audit reports **2,267 theorem constants**, with only `propext`, `Classical.choice`
and `Quot.sound`. The original inventory separately lists 32 generated unsafe
implementation axioms; they are not permitted theorem dependencies. This
canonical report does not claim the separate reviewer's safe-definition audit.

The original start metadata is retained byte-for-byte:

- `source_commit`: `e84dfed51f9dfd48995ddc4920f5bf2bd6b80f82`.
- `source_tree_clean`: `true`.
- Registry SHA256: `02854c6cf0631e0605ddb83a859ff98f1347bb8130120d7101357b4cfe4e9c06`.

The verifier's clean flag is based on tracked-file status and excludes
untracked files. Packaging does not revise that historical flag. Every one of
the 48 compiled source snapshots and the complete registry was independently
matched against the exact published commit above and the current working bytes.
The original registry's pre-verification status text is preserved, not rewritten
to alter historical metadata; the separate addendum records the actual result.

All original Lean argv are preserved in `parent-clean-001/verification.json`.
They use `-j1 -DElab.async=false` and **do not explicitly pass `--trust=0`**.
They must not be described as the separate strict reviewer execution. The
official compiler is Lean 4.19.0 release `6caaee842e94`; the original compiler
binary/library hashes are retained. No compiler defaults are inferred beyond
what the preserved argv establishes.

`parent-launch.json` records the exact top-level Python argv and workdir as
confirmed by the original parent executor's tool transcript (session 47137,
exit 0). Each actual child argv/exit/log hash is directly recorded in the
original report. `parent-console.log` is the original console output.

The original 99 manifest entries are copied unchanged into `parent-clean-001/`,
together with its original `FILES.json`. Those entries include all 48 compiled
mathematical sources, the generated ProjectAudit source, all 49 logs and the
original report. Compiled objects are excluded. `canonical-verifier.py` and
`registry.json` are exact published snapshots. `publication-source-receipt.json`
records all source/build/commit hash comparisons. `parent-result-addendum.json`
summarizes the actual preserved result without replacing its original report.

`PACKAGE-FILES.json` is a separate package manifest covering these copies and
the additive metadata, including the untouched original manifest. It does not
replace or edit `parent-clean-001/FILES.json`. The executed packaging driver is
retained as `package.py`. No mathematical source, original report, log, manifest,
checker, or registry was modified.
