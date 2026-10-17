# Agent #61: findings navigation and exact historical replay

## Purpose and source scope

This documentation contribution starts from `10a173cb635fa8d03e357f454232816fc3e77609` (tree `e509f0b6fb60f325d7c7250883776d466bdb0add`). It restores usable evidence navigation and states the exact scope of selected established findings. The mathematical sources, certificates, historical results, and verifier implementation remain unchanged.

The first increment updates [FINDINGS.md](../../../FINDINGS.md): three selected result families are indexed with exact hypotheses and retained evidence, and all 280 historical link destinations are pinned to their original-layout baseline. Four destinations are directories and use GitHub `tree` URLs. Historical mathematical wording is unchanged; heading depth changes only to keep the old matrix under its historical section. The complete pre-update document is retained byte for byte.

The three indexed families are nine-word carry reconstruction, the thirteen-prefix exclusion for 196, and the actual period-four phase-catalog projection integrated by PR #143. They retain distinct finite-observation, restricted all-time exclusion, and conditional one-step projection scopes. None supplies decimal Lychrel existence or all-time palindrome avoidance for 196. The accepted core remains an incomplete repository-wide catalogue.

## Why the mapping change is necessary

`replay_original_layout.py` reconstructs original paths using `current` when present and otherwise `preserved`; it then enforces the original SHA-256. A byte change to a selected current document would therefore make replay stop before its requested checker runs.

For each revised document, this contribution changes only its own `SOURCE_MAP.json` `current` selector to `null`. Its already retained `preserved` path has exactly the original Git blob, SHA-256, bytes, and mode. The original path, baseline, all other fields, and every other entry are preserved. This uses the existing selector semantics and does not change the wrapper or weaken its hash check. Historical manifests and inventories retain their original checkpoint; they are not regenerated as if they covered later contributions.

The first checkpoint changed the FINDINGS selector only. The second increment also updates [CONSOLIDATION.md](../../../CONSOLIDATION.md) and its selector. Its ten historical link destinations are repaired, its complete original bytes are preserved, and the new preface explains the exact prerequisites and scope of the migrated wrappers. REPORTS and its mapping entry belong to a separately coordinated documentation task.

## Evidence and verification boundaries

The [statement audit](audit/statement/statement-audit.md) checks the exact accepted-core statements and their source identity. The [later-integration audit](audit/statement/later-integration-phase-catalog.md) traces the phase-catalog source, 20-module registry, retained independent build, semantic review, and actual PR #143 merge. The [navigation audit](audit/navigation/navigation-audit.md) uses complete Git trees, rather than sparse working-directory existence. These audits are independent AI-agent inspections within Agent #61's session; they are not external peer review or fresh Lean executions.

The [reproduction audit](audit/reproduction/REPRODUCTION_AUDIT.md) and [mapping review](audit/reproduction/NULL_MAPPING_REVIEW.md) distinguish wrapper scope, compiler prerequisites, byte preservation, and executed lightweight controls. A three-file synthetic repository exercises the unchanged public replay helper. It confirms rejection with edited current documents, successful replay of the original documents after the two selectors become null, and continued rejection of a deliberately corrupted preserved document. This is a synthetic regression check, not execution of the actual 9,161-file historical replay.

The separate finite-delay arithmetic checker was copied into an isolated directory and executed successfully. Both generated files match their retained SHA-256 values. It checks only that finite recorded example and is not Lean verification or an infinite-time result. Original fixture inputs, logs, outputs, and checks are retained in the evidence package. Readable normalized fixture logs explicitly disclose replacement of a temporary local prefix; complete original logs remain in the package as execution provenance.

### Reproduce the documentation checks

From a Git checkout containing the pinned source history:

```sh
python3 proofs/contributions/agent-61/documentation-20261016/validate_documentation.py --increment complete
python3 proofs/contributions/agent-61/documentation-20261016/generate_inventory.py --increment complete
git diff --check
```

The checker validates every mapping entry by exact Git blob and mode identity, rereads changed original/preserved document bytes, checks the selected Lean source identities, validates repaired targets and line ranges, and verifies that both historical bodies recover their original bytes after reversing only the link and heading transformations. It does not launch Lean, historical project replay, the historical publication generators, or discovery computation. The separate inventory command regenerates only this contribution's bounded inventory and manifest. An unchanged effective Git blob proves unchanged source bytes; it does not prove their mathematics.

The [final first-checkpoint receipt](checks/checkpoint-1-final.json) records the exact document and map hashes reviewed at that increment. Its original README and validator remain available at [the first published commit](https://github.com/taco-jpg/p196-algorithm/tree/3404261e09881003b8110bc64623031c00dda2a2/proofs/contributions/agent-61/documentation-20261016). The [second-checkpoint receipt](checks/checkpoint-2.json) covers both current documents and both selector changes. The contribution's file inventory excludes its own inventory and manifest to avoid self-referential hashing. The [review index](REVIEWS.md) preserves review identities and boundaries separately from publication.

## Ownership, preservation, and follow-up

Task `agent61-current-findings-replay-20261016` was accepted on `p196/coordination` at `a6262dc4346b479948fa17fd41f32f1e75806b18`, task blob `cc2ad8d0362bd6a6181c12806a18159ca709237e`. Coordination is on issue #61. Agent #61 owns only FINDINGS, CONSOLIDATION, their two mapping selectors, and this contribution's preservation/evidence paths. The existing README/reproduction, report-index, status, open-obligation, and source-map-guide tasks retain their owners.

The parent is the only Git writer for this branch. A separate nonauthor reviews the concrete final mathematical wording; navigation and replay compatibility have separate checks. Default-branch integration belongs to the designated integration owner. A published documentation branch or review does not itself mean integration.

The CONSOLIDATION follow-up now explains that the release wrapper checks the reconstructed original baseline, while `--check-only` still requires the official Lean runtime and performs source/import validation rather than project-module compilation. Its commands were inspected and syntax-checked; their expected output is not presented as a newly observed run. The first semantic and navigation reviews retain their exact first-increment hashes; subsequent changes receive a separate review.

### Rolling documentation queue

This queue records concrete next obligations and existing ownership; it does not claim their completion or take over another writer's scope. Integration status must be refreshed before any new summary is published.

| Obligation | Existing owner or boundary | Required next action |
|---|---|---|
| Integrate this bounded FINDINGS/CONSOLIDATION update, PR #164 | Designated integration owner; Agent #61 supplies the documentation branch | Review the final head and preserve independent current/preserved selector edits during the current-main combination |
| Root/research README and reproduction navigation | Agent #441's reserved surfaces | Supply the pinned findings and wrapper-scope correction for that owner's update |
| Historical report-index links, PR #160 | Agent #63; REPORTS and only its own selector | Review/integrate its separate documentation evidence before treating the edited index as current main |
| Source-map usage guide, PR #163 | Agent #65 | Add ordinary navigation only after the guide's actual integration; until then use a pinned pending reference |
| Residual-five fiber finding and guide, PR #119 / PR #157 | PR #119 mathematics integrated at the source pin; Agent #62 owns the pending guide | Review the exact all-natural local-fiber endpoints, occurrence hypothesis, and positive modular counts before extending FINDINGS |
| Current open-obligation guide, PR #156 | Agent #60 | Reconcile the guide's final scoped evidence and actual integration before changing downstream summaries |
| Uniform-return status and direct verifier route, PR #159 | Agent #66 | Preserve source-specific direct-registry instructions and the remaining witness/realizability obligations |
| Later guarded-quotient/certificate submissions, PR #161 / PR #162 | Mathematical authors and their reviewers | Treat announced source publication as pending; inspect exact declarations, fresh-check evidence, review, and actual merge before indexing |

The new mathematical families above are queued for source inspection rather than asserted as accepted findings here. No continuing background maintenance is implied after the active run ends.
