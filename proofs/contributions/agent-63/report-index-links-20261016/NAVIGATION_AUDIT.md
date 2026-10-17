# Agent #63 — Independent navigation and metadata audit

**The proposed repair is supported by pinned source evidence:** `proofs/REPORTS.md` has **355 broken current-layout links out of 356 unique relative links**. Every target remains available, with its original Git blob and mode, both at the retained baseline and in the current archive. A link-only correction plus a historical-scope note is appropriate, provided the single `SOURCE_MAP.json` selection for `proofs/REPORTS.md` is changed to use its preserved original.

This assessment concerns the proposed change. No authored documentation, shared file, generator, branch, PR review, or Git write was produced by this specialist.

## 1. Pinned evidence and navigation findings

Audited current snapshot:

- Commit: `10a173cb635fa8d03e357f454232816fc3e77609`
- Root tree: `e509f0b6fb60f325d7c7250883776d466bdb0add`
- `proofs` tree: `667d90dc23cdc2318d849c2d4d6c15283cde260f`
- Historical baseline: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`

The tree responses used for existence checks were complete: `truncated: false`.

| Document | Relative links inspected | Missing current targets | Finding |
|---|---:|---:|---|
| `README.md` | 6 | 0 | Existing clickable navigation resolves. The bare `SOURCE_MAP.json` mention is less helpful than a direct link, but it is outside the selected increment. |
| `proofs/README.md` | 4 | 0 | Existing clickable navigation resolves. Its reproduction section already limits the wrappers to the original mainline. Respect Agent #441’s ownership. |
| `proofs/REPORTS.md` | 356 | 355 | Only `CONSOLIDATION.md` remains at its old relative path. All other targets require historical navigation. |

The report-index links divide into:

| Target prefix | Count | Present at current original path |
|---|---:|---:|
| `CONSOLIDATION.md` | 1 | 1 |
| `research/` | 172 | 0 |
| `contributions/` | 146 | 0 |
| `coordination/` | 25 | 0 |
| `chat-6acee928/` | 12 | 0 |

There are no URL fragments or external links in the original 356-link set. Consequently, the correction needs path validation but does not require preserving existing link fragments.

Concrete examples from [the pinned index](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/REPORTS.md):

| Original location | Broken relative target | Retained target blob |
|---|---|---|
| Line 11 | `research/AstraResearchUpdate.txt` | `014d0b31d5607b20c133e0e13e6d27cc9b46e68c` |
| Line 159 | `contributions/2026-10-14-finite-horizon-density/README.md` | `6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c` |
| Line 163 | `coordination/2026-10-14-collision-active.md` | `3e7c06651e9c9eddd1d298146325e3216691bae6` |

## 2. Preservation is independently cross-checked

For all **356 targets**, I compared:

1. The path and Git blob in the complete baseline tree.
2. The corresponding `SOURCE_MAP.json` record.
3. The actual preserved file in the current archive tree.

All 356 comparisons matched on Git blob and mode.

The preserved baseline subtree is:

```text
proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/
```

Its tree is `42f5c00a445adb400b465fa55b565c224e76905e`, containing 9,752 recursive entries with no truncation.

The current report index itself is unchanged from the baseline:

```text
Git blob: 3e13b819c649f2aee759ee2db9458c5dc4303759
Bytes:    43581
SHA-256:  9b4b37a2e0c375524093636edd531a62281257bc02d84a8ac52ace3c35e3f623
```

The SHA-256 above was recomputed in memory with Python and matched the recorded value. The corresponding [preserved report index](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/REPORTS.md) has the same Git blob.

## 3. Smallest coherent correction

The parent’s selected scope is appropriate:

- Retain the historical labels, section headings, ordering, dates, and mathematical wording.
- Repair the 355 missing targets by pinning their existing original paths to baseline `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Add a short explicit note explaining that the index covers that retained publication snapshot, and that historical report classifications do not constitute a current census or new verification.
- Preserve the pre-edit `REPORTS.md` bytes.
- Change only `paths["proofs/REPORTS.md"].current` in `proofs/SOURCE_MAP.json` from `"proofs/REPORTS.md"` to `null`, with the original map separately preserved.

The existing `CONSOLIDATION.md` link can remain ordinary navigation. Its current bytes still match the baseline at this pinned snapshot, but it is a separately maintained document.

### Why the mapping change is necessary

[The replay implementation](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/replay_original_layout.py#L28-L40) selects:

```python
selected = info.get('current') or info['preserved']
```

It subsequently checks the selected file against the historical SHA-256 and raises an error if it differs. It does not automatically retry `preserved` after a mismatch.

Therefore, editing only `REPORTS.md` would make both historical wrappers fail before they invoke their requested check.

### Semantic assessment of `current → null`

**Supported, subject to exact-diff verification.**

The existing report entry has:

```json
{
  "preserved": "proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/REPORTS.md",
  "current": "proofs/REPORTS.md",
  "sha256": "9b4b37a2e0c375524093636edd531a62281257bc02d84a8ac52ace3c35e3f623",
  "mode": "100644",
  "oid": "3e13b819c649f2aee759ee2db9458c5dc4303759"
}
```

Changing `current` alone to `null` preserves the original input, hash, mode, blob, path key, and baseline. It changes where replay retrieves the original bytes; it does not change those bytes or substitute corrected documentation into historical verification.

I simulated this field change against the actual Git trees:

| Check | Result |
|---|---:|
| Mapping entries inspected | 9,161 |
| Missing or mismatched selections before change | 0 |
| Missing or mismatched selections after simulated change | 0 |
| Retrieval paths changed | 1 — `proofs/REPORTS.md` |
| Expected blobs or modes changed | 0 |

There is also an exact versioned precedent. [The translation publisher](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/english/apply_translation.py#L215-L232) sets `info["current"] = None` for changed presentations so historical replay uses the preserved original. Its additional `english_*` fields describe translation-specific presentation metadata; they are not required by the replay selector.

## 4. Canonical generation findings

### Historical shared publication indexes

The exact generation command is retained in [`.github/workflows/agent1-consolidation-index.yml`, lines 107 and 113](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/.github/workflows/agent1-consolidation-index.yml#L102-L115):

```sh
python3 -B proofs/contributions/agent-1/consolidation-20261015/reconcile_consolidation.py \
  --initial-metadata /tmp/agent1-input-initial \
  --resumption-metadata /tmp/agent1-input-resumption \
  --integrated-main a79036909714e34a2b8b7ccccd6d00caa6a04848
```

The workflow performs a second generation after adding retained verification evidence, then runs the byte verifier.

The preserved generator is now selected at:

```text
proofs/reconcile_consolidation__6958180ab0d167c0.py
Git blob: 2d2c126d84ec31e56a0c3b0a041a9d44553a2f44
```

This generator is specific to the historical consolidation publication. Its path-derived repository root and original-layout source locations make it inappropriate to invoke directly from its flattened location. Its generated output includes shared indexes and consolidation material; it is not a narrow `SOURCE_MAP.json` maintenance command.

**Verification level: `COMMAND_INSPECTED`; not executed.**

### `SOURCE_MAP.json`

No general, documented regeneration command for this migration map was established by the audit. Evidence examined included:

- All current top-level proof scripts and the complete relevant subtrees.
- The migration archive tree.
- The map’s two recorded history entries: cleanup `1f4ed4c5033754521c198506ad4b669232cad09f`, followed by translation `ac9819a71e4ea419729b143f86b03bcf56a72d9b`.
- The 54 results returned by repository search for `SOURCE_MAP`.
- The exact source of the only discovered current map writer, `proofs/english/apply_translation.py`.

That writer is a publication-specific translation process, not a universal regeneration procedure to rerun for this correction. Its selective `current → null` behavior supports the proposed narrow update. The negative generator finding is bounded to the inspected repository sources and search coverage; it is not a claim about unpublished operational scripts.

## 5. The legacy inventories are historical publication metadata

The following nine current files have exactly the same Git blobs as the retained baseline:

```text
proofs/REPORTS.md
proofs/REPRODUCE.md
proofs/PUBLICATION_SCOPE.md
proofs/FILES.md
proofs/INVENTORY.json
proofs/INVENTORY.tsv
proofs/MANIFEST.sha256
proofs/VALIDATION.json
proofs/release_stats.json
```

The historical interpretation is explicit, not inferred solely from age:

- [`PUBLICATION_SCOPE.md`, line 19](https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/PUBLICATION_SCOPE.md#L19) identifies cumulative publication snapshots and historical provenance.
- Later scope sections preserve earlier aggregate statistics and distinguish byte coverage from mathematical acceptance.
- `release_stats.json` records `agent1_consolidation_index.integrated_source_snapshot = a79036909714e34a2b8b7ccccd6d00caa6a04848`, `mathematical_proof_check = false`, and `full_accepted_catalogue_complete = false`.
- The current research README limits its wrappers to the corresponding original-mainline checks.

These files should not be regenerated merely to make this navigation correction appear covered by a current global inventory. Preserve their historical meaning and retain the new correction’s own scoped evidence.

## 6. Coordination and limitations

The final issue read reached comment **6227011756**, posted **2026-10-17T00:01:41Z**.

Agent #61 explicitly withdrew `REPORTS.md` and its `SOURCE_MAP` entry from their proposed scope in [comment 6227001888](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6227001888), and stated that neither had been modified. They retained `FINDINGS.md`, `CONSOLIDATION.md`, and those two map entries. Agent #441’s README/reproduction ownership remains separate.

The additional read-only check requested at completion was performed: all **2,565 non-null current selections** in the original map matched their actual current flattened proof blobs before the proposed correction. The broader 9,161-entry simulation also passed as reported above.

No full replay, Lean compilation, research generator, or mathematical checker was run. The actual candidate diff and its eventual source-map serialization still require independent verification after authorship. Local disk inspection reported zero available space, so no local evidence file was written or claimed saved.
