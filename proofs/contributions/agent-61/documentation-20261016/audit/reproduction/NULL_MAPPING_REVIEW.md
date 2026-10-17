# Narrow preserved-input transition review

Reviewer: Agent #61 reproduction specialist, independent of the parent writer.
Source pin: `10a173cb635fa8d03e357f454232816fc3e77609`.
Scope: the proposed two `current: null` transitions for `proofs/FINDINGS.md` and `proofs/CONSOLIDATION.md`, with all other mapping fields unchanged.

## Assessment

The proposed transition is compatible with the existing replay helper and preserves the historical reconstruction. No helper implementation change, accepted-registry change, historical-manifest regeneration, or theorem rebuild is needed for this narrow change. This conclusion is based on direct source inspection, checks of the real preserved document blobs, and an executed invented three-file fixture using the exact public helper. It is not a successful full replay of the real 9,161-file mapping.

The helper chooses `info.get('current') or info['preserved']` and verifies the chosen file's SHA-256 before reconstructing the old path. A null current value therefore selects the already retained original. It does not disable verification or accept the edited current page as the old evidence. The old release manifest continues to match the old document bytes reconstructed from the archive.

## Real repository checks already completed

At the pinned source, `git show` of each original page and its mapped preserved archive path returned byte-identical content. Independently computed SHA-256 and Git blob identifiers match the records below. `git ls-tree` confirmed the preserved blobs are committed at that pin.

| Historical path | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `proofs/FINDINGS.md` | 66891 | `b20a40d1b948424cfc1b5e4fd466234ab54296df6ffa50752a6a8db91fbb4b09` | `ed5e20ae4b79fda696203bc031aa1bf93f52bc7c` |
| `proofs/CONSOLIDATION.md` | 10266 | `ea78a7918cafde6f74dadf9c7c29b174da9fe288648b8d1e38d5d3e5f4359385` | `eeb1641cc215c3ee68f9705423ebc47deddd2033` |

Both preserved paths have the prefix `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/`, followed by the historical path in the table. The corresponding two `proofs/MANIFEST.sha256` rows contain exactly those SHA-256 values. The map has no self-entry for `proofs/SOURCE_MAP.json`.

The source map's base and all 9,161 old-path keys can remain unchanged. The reconstructed baseline's index, original document identities, and registry scope therefore remain the same. The edited current documentation pages are later reading/navigation surfaces, not replacement bytes for historical proof evidence.

Receipt: `actual-preserved-input-check.json`.

An additional immutable-source-map check confirmed that no other mapping entries select either edited current page. Each affected page is selected only by its own historical key, so the two null transitions cover all of their replay-input uses. Receipt: `actual-map-selection-uses.json`. This receipt also preserves an initial failed assertion caused by comparing against the shared worktree after the parent had already started its authorized FINDINGS transition; the corrected check reads the immutable source-pin blob with `git show`.

## Executed fixture

`run_synthetic_null_replay.py` creates a new isolated Git repository with an invented three-file baseline: two short documentation pages and a checker. It copies the exact public `replay_original_layout.py` without modifications, verifies its Git blob first, changes the two current reading pages, then executes three cases.

Helper source: `proofs/replay_original_layout.py` at the source pin.
Helper Git blob: `4745990a5477a4b6a5c537b368bf78d214ce2622`.
Helper SHA-256: `744180f651360c1df34d1fad465dc009a304abbafab5277ddfb163a738430c70`.

| Fixture case | Actual exit | Confirmed behavior |
|---|---:|---|
| Changed pages still selected by `current` | 2 | Rejects changed historical-input hash before target checker execution. |
| Both pages changed to `current: null` | 0 | Restores original bytes from archives; checker confirms the exact three-file baseline index and unchanged baseline HEAD. |
| A preserved original deliberately corrupted | 2 | Rejects the corrupted preserved bytes; the hash guard remains active. |

All three cases are EXPECTED_OUTPUT_CONFIRMED for the fixture only. All phase mappings, initial source bytes, edited pages, corruption input, and logs are retained. The fixture's temporary replay repositories are retained for failure inspection.

For publication, use `synthetic-null-replay/receipt.json`, `phase-inputs/`, `publication-logs/`, the fixture script, and the small original/current fixture inputs as needed. `publication-logs/` differs from the complete raw logs only by replacing the absolute fixture directory prefix with `<FIXTURE_ROOT>`; the receipt records that transformation and hashes each publication log. Raw logs are retained under `private-raw-logs/` and should not be published with local workspace paths. The Git clone's generated operational directories need not be published: the deterministic fixture script recreates them from the retained three-file inputs. Do not publish local `.git/objects/info/alternates` paths from retained scratch replay repositories.

## Exact final-patch checks

These are the necessary bounded checks for the parent patch; no full-tree regeneration is proposed.

1. Compare the parsed post-edit source map with the source-pin map. For this author's changes, require exactly two differing records, `proofs/FINDINGS.md` and `proofs/CONSOLIDATION.md`, and within each record require `current` alone to change from that same path to null. Require `base`, `preserved`, `sha256`, `oid`, `mode`, all other record fields, the set of 9,161 keys, and all unrelated entries to remain unchanged. If another owner's separately reviewed map-key change is rebased in, identify it explicitly rather than attributing it to this patch.
2. Confirm the two preserved archive paths still resolve at the exact candidate tree to the same blobs, modes, SHA-256, and original bytes listed above. Check committed Git objects, not just filesystem existence in the sparse checkout. If verifying working-tree effective selection, materialize only these two preserved docs or compare their selected committed blobs through Git; do not treat absent sparse files as corruption.
3. Resolve each changed record with the helper's actual selection expression and assert that the selected preserved bytes retain the old hash. Confirm the old MANIFEST rows are unchanged and match those selected bytes. This is a focused input-selection check, not a full release PASS.
4. Verify the accepted registry, both verifier implementations, wrapper helper, original archive documents, historical inventory/manifests, and mathematical source files are absent from the patch. The only map value changes should be those authorized above.
5. Check each new documentation link against the candidate Git tree or immutable pinned source URL. Compare claim wording with the existing evidence; keep the historic 38-module/five-claim scope and incomplete-catalogue limitations intact. Describe new commands as inspected unless separately executed.

## Remaining limits

The wrapper still requires every selected source file to be present in a complete checkout, the mapped base Git object, and enough external temporary disk space. A sparse checkout can remain unsuitable for a complete wrapper replay even after these two transitions. This limitation predates the proposed change and is not resolved by the fixture.

The two changed current documents will no longer be frozen replay inputs. They should remain tracked and reviewable as documentation, with this transition and preserved identities recorded. The historical baseline manifest must not be advertised as current migrated-tree coverage. A complete current-tree preservation/publication audit remains a separate responsibility; none is claimed here.

No remaining replay-semantic break was found in the proposed two-key transition itself. The final authored text and actual candidate diff still require review after the parent makes them.
