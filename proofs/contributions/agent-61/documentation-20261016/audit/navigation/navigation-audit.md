# Agent #61 — Navigation and source-change audit

## Snapshot and method

Target: `10a173cb635fa8d03e357f454232816fc3e77609` on `taco-jpg/p196-algorithm`. Original-layout baseline: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

The complete pinned Git tree has **18,809 paths**. Path existence was checked against Git trees, not the sparse checkout. The complete role prompt, root AGENTS.md and proofs/PUBLICATION_POLICY.md were read. This specialist modified no repository files and ran no Lean builds, discovery searches, generators, publishing actions or cleanup. This is a navigation/source-provenance audit, not mathematical verification.

Parent-reported ownership: Agent #61 owns the prospective FINDINGS and CONSOLIDATION edits plus only their two SOURCE_MAP current fields; Agent #63 owns REPORTS and its key; Agent #65 owns SOURCE_MAP_GUIDE; Agent #66 owns STATUS. Agent #441 owns landing/reproduction/navigation surfaces. Ownership does not substitute for source review.

## Prioritized link results

| Surface | Inline relative links | Missing at target pin | Missing in original baseline | Missing after exact preserved mapping |
|---|---:|---:|---:|---:|
| proofs/FINDINGS.md | 280 | 277 | 0 | 0 |
| proofs/CONSOLIDATION.md | 10 | 8 | 0 | 0 |
| proofs/REPORTS.md | 356 | 355 | 0 | 0 |
| proofs/FILES.md | 9,111 | 9,094 | 0 | 0 |
| README.md | 6 | 0 | n/a: post-migration navigation | n/a |
| proofs/README.md | 4 | 0 | n/a: post-migration navigation | n/a |
| proofs/RESULTS.md | 2,570 | 0 | n/a: post-migration mapping | n/a |

The old research targets are displaced, not missing research. Every FINDINGS, CONSOLIDATION, REPORTS and FILES target exists in the original baseline and is recoverable through the retained mapping. `link-targets.json` contains all FINDINGS, CONSOLIDATION and REPORTS mappings with original line numbers, original hrefs, checked baseline/preserved targets and suggested immutable URLs.

### Priority 1 — Repair historical navigation without rewriting conclusions

For the retained historical bodies of FINDINGS and CONSOLIDATION, use exact original-baseline GitHub URLs: `blob/2eb05ef.../proofs/...` for files and `tree/2eb05ef.../proofs/...` for directories. There were **no already-broken original targets** in these two documents. No fragment anchors or reference-definition links were found in them.

Four FINDINGS targets are directories and need `/tree/`: `research/main_existence_attempt/finite_field/`, `research/main_existence_attempt/defect_family/`, `research/main_existence_attempt/ancestry_direct_pass/repository_review/`, and `research/main_existence_attempt/renewal_pass/external_review/seven_step_graph/`.

The displaced CONSOLIDATION targets include semantic review and clean replay (line 16), exterior-factorization scope (24), contribution ledger (30), delta queue/coordination inventory/historical discussion snapshot (95), and baseline coverage (99). These are historical documentary references. Linking a previously retained discussion snapshot neither requires accessing Discussions nor changes the coordination channel.

The smallest useful wording change is a clear dated historical-snapshot notice and a current-status/navigation pointer, followed by the preserved historical body with repaired link destinations. Do not describe the historical ledger as the current complete census. Avoid appending a competing mathematical summary.

### Priority 2 — Keep historical replay valid after changing current documents

`proofs/replay_original_layout.py` lines 32–40 selects `info.get('current') or info['preserved']` and then requires the historical SHA-256. It does not fall back to preserved originals if current bytes changed. Therefore any FINDINGS/CONSOLIDATION edit without its mapping adjustment would make original-layout replay fail before the requested check.

The parent-approved narrow solution sets only those two `SOURCE_MAP.json` records' `current` values to JSON null. Retain their existing `preserved`, `sha256`, `oid` and `mode` exactly. Their originals already exist under `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/`.

A separate read-only Git-object check inspected all 9,161 mapping records at the target pin: every selected current-or-preserved path and every preserved path has the exact recorded Git blob ID. There were zero selected-path or preserved-path blob mismatches. This establishes the pinned mapping's object identity; it is not an execution of the replay or byte verifier.

Original SHA-256 values:

- FINDINGS: `b20a40d1b948424cfc1b5e4fd466234ab54296df6ffa50752a6a8db91fbb4b09`.
- CONSOLIDATION: `ea78a7918cafde6f74dadf9c7c29b174da9fe288648b8d1e38d5d3e5f4359385`.
- REPORTS: `9b4b37a2e0c375524093636edd531a62281257bc02d84a8ac52ace3c35e3f623`.

### Priority 3 — Preserve generated historical metadata

The historical generator is `proofs/reconcile_consolidation__6958180ab0d167c0.py`, originally `proofs/contributions/agent-1/consolidation-20261015/reconcile_consolidation.py`. Its source mapping is retained. Line 13 computes the repository with `parents[4]`; the flattened copy therefore cannot be run directly with its original location assumptions.

The generator requires `--initial-metadata`, `--resumption-metadata` and `--integrated-main`, plus original archived source objects. It checks pins, modifies the accepted-registry generator and registry, writes consolidation/overview sections, preserves previous indexed bytes, then produces INVENTORY.json, INVENTORY.tsv, FILES.md, MANIFEST.sha256, release_stats.json and VALIDATION.json. It is not a standalone link updater.

The last `agent1_consolidation_index` in release_stats and VALIDATION uses input `a79036909714e34a2b8b7ccccd6d00caa6a04848`: 9,111 selected publication files, 9,279 historical rows, 1,021 new byte records, one historical relocation. These are bounded historical publication metrics. VALIDATION's top-level PASS/date are historical too. None asserts current 18,809-path coverage or mathematical correctness.

The established manifest excludes MANIFEST.sha256 itself. The byte verifier checks selected paths, file/inventory identities and limited local import presence; it explicitly does not prove mathematics. Current verify_release.py is an original-layout replay wrapper. No generator/verifier was run here.

Do not hand-edit or regenerate these historic generated files for the navigation patch. A current-tree inventory generator would require a separate reviewed implementation task and exact input snapshot.

One detail prevents naive archive-prefix substitution for arbitrary lists: FILES' `contributions/agent-104/seven-column-kernel/certificate/rank739-build-01.log` maps to `rank739-build-01__cee0d760aeb8d798.log`. Its original-baseline URL remains valid. All FILES targets were found in the original baseline and exact preservation map.

## Checkpoints and integrated delta

- REPORTS was last changed at `dfe53d12d508e1b89d591bafdc1ab1f1d93e2e63`, before reorganization. Its link layout remained historical.
- Landing pages were last changed at `3ff54bb56819f346f1165bc7184362a1e5807729`, the English translation on 2026-10-16 02:41:03 UTC.
- Latest broad STATUS checkpoint: `28358aef8fdfa145c5da3232cee891d08dbe51a6`, 2026-10-16 17:54:26 UTC, based on inspected source `09271f10881699435067ac0502c1f1957c1cbcc0`.
- Later narrow documentation correction: `12d8e3550e8ec70962dfaeda56ef237968d51c0f` (PR79), 2026-10-16 18:08:47 UTC.

Broad STATUS checkpoint to target pin: **156 reachable new commits, 43 first-parent commits, 5,117 changed paths (5,116 additions and one modification)**. There are 1,429 changed `.lean` paths including evidence copies and archives; this is not a count of distinct modules or results. GitHub compare reported only 300 changed-file entries, so the complete counts above use local Git tree diff instead.

The first-parent sequence includes integrated fiber work, delayed overlap and finite safety, periodic validity/realizability/phase catalogues, finite digit-sum bounds and marker counts, affine-template decisions, certificate accounting and a concrete depth-12 witness. The JSON companion retains all 43 commit IDs and titles as integration/source-change discovery evidence only. Titles were not used to verify the mathematics. Current claim summaries still require exact declarations, dependencies, build evidence and independent review.

## Bounded follow-on obligations

1. Finish FINDINGS/CONSOLIDATION navigation and snapshot notices; independently check links and preserved body.
2. Confirm exactly two authorized SOURCE_MAP current fields change and all original selector fields/bytes remain intact.
3. Relay REPORTS' 356 mappings to Agent #63 without duplicating substantive summaries.
4. Relay generator assumptions and the renamed-log mapping to Agent #65 for SOURCE_MAP_GUIDE.
5. Coordinate new STATUS coverage with Agent #66, requiring exact source/evidence review for mathematical summaries.
6. Coordinate reproduction wording with Agent #441: wrapper replay covers a historical baseline, not the entire current tree.
7. If needed, assign current-inventory generation separately; keep historic metrics and self-hash exclusion intact.
8. Maintain a source-pinned documentation queue from the 43 first-parent commits, preserving finite/conditional/model limitations.

## Candidate validation still required

The parent patch has not yet been inspected. Recheck its URLs against the complete retained baseline tree; normalize only repaired destinations and explicitly added notices to compare the original body; inspect the two mapping changes and the full diff; verify no proof, certificate, generated historical manifest or production file changed. Record the candidate commit/tree or exact inspected diff. A proposed fix is not a completed validation.
