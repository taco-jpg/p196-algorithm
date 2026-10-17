# Research workflow publication migration

This change removes autonomous repository publication from five historical
workflows. The October 17 campaign uses one canonical writer. Research replay
jobs retain their exact source identities and downloadable evidence, then hand
the result to that writer for current review, preservation, and target checks.

The baseline is `74a1c3922eb7af438fe40b23d2105ad07556e3f5`. Each changed workflow's
original bytes, mode, Git blob, SHA-256, preserved path, and replacement identity
are recorded in `preservation.json`. The `originals` directory is historical
evidence. GitHub runs workflows only from the active `.github/workflows` paths.

| Active workflow | Resulting behavior |
| --- | --- |
| `p196-cleanup-retire.yml` | Manual, read-only complete branch-ref observation. It reports that campaign acceptance was not evaluated and that no retirement occurred. |
| `agent1-english-publish.yml` | Manual candidate preparation, original source guards, exact candidate validation, and artifact handoff. No direct main update. |
| `agent4-certificate-replay.yml` | Manual historical cap-six generation and independent replay from the pinned original source tree; evidence handoff. |
| `agent4-saturation-audit.yml` | Manual historical saturation and reciprocal source replay; evidence handoff. |
| `agent4-whole-word-bridge.yml` | Manual historical numeric-bridge replay and retained reciprocal-review inputs; evidence handoff. |

## Historical retirement procedure

The unchanged script and plan under
`proofs/archive/migration/668beb73f0a69c7ad8d8` describe an earlier migration.
They retain the earlier owner's waiver and excluded-branch policy as historical
evidence. The active status workflow does not execute them. The r2 campaign
requires content accounting, independent review, tested durable recovery,
complete source history, PR-reference disposition, active-producer checks,
current writer authority, preservation tags, and an exact expected-old-tip
guard for each eventual branch retirement. A one-branch observation alone is
not campaign acceptance. The current coordinator in issue #61 owns cutover.

## Historical replay identity

The three Agent4 jobs previously checked out current main while invoking the
removed `proofs/agent4` layout. They now check out immutable historical commit
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` and verify its `proofs/agent4` tree as
`6d59c68f8f5922f85f5238081ce46226af0e1c02` before running. All 43 original files
and relative import paths are retained. This tree also matches the preserved
source-tree copy already present in the baseline.

`WORKFLOW_SOURCE.json` records both the current workflow definition commit and
the historical input commit. The unchanged historical Python checker receives
the input commit in its source-receipt environment. Reciprocal sources retain
their individual immutable URLs and hashes. Retained historical log directories,
certificate results, and the saturation summary are moved into a separate
artifact section before each execution. Fresh output directories begin empty,
so failed runs cannot inherit an old successful audit or replay summary. The math, finite certificate
domain, generators, theorem statements, compiler pin, and historical checker
are unchanged. These are historical replay jobs, not the campaign's final
current-main build or strict complete axiom audit.

## English candidate boundary

The original translation generator's landing-page, source-map, and output
ownership guards are unchanged. At the baseline, the landing-page guard rejects
the old patch context because current pages advanced after the original
reviewed translation. This migration does not relax that check, replace current
text with old text, or claim the translation task is complete. The manual job
retains its diagnostic stderr alongside any candidate evidence. Applying a
translation to a changed context requires a separately reviewed current patch.

## Evidence delivery

The retained upload steps run even after a replay fails. The generated artifact
and raw logs distinguish success, failure, workflow source, input sources, and
scope. When a replay is requested, the canonical writer must capture its useful
evidence into the campaign's durable record before the temporary Actions
artifact expires. No automatic main push, branch creation, branch deletion, or
tag operation remains in these five active workflows.

This bounded change does not certify every historical workflow in the
repository. The complete workflow inventory and remaining staging-branch
publishers are a separate recorded automation obligation. No calculation file,
historical research source, or accepted proof interface is changed.
