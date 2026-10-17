# Bounded documentation validation

## Identified revision

Source snapshot: `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`.

Reviewed guide SHA-256:
`1b66a639da024562d317f8f550e3c2c0250b412ea5f46c6678a6824b2387c101`.

Source-map Git blob:
`e5f8d27bf09f50f8b9756bf91dff02e992aa4a32`.

Source-map SHA-256:
`f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba`.

The map contains 9,161 entries and names original-layout baseline
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
These are source-recovery facts; no mathematical status is inferred.

## Executed checks

| Check | Result and boundary |
|---|---|
| The guide's exact read-only Python lookup block, with argument `proofs/REPRODUCE.md` | Exit 0, empty stderr, exact expected stdout below. One selected file's hash, not complete recovery. |
| `git cat-file -e '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5^{commit}'` | Exit 0, empty stdout/stderr; baseline object is locally available. |
| `git show '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5:proofs/REPRODUCE.md'` | Exit 0, empty stderr; 39,464 stdout bytes match the historical/current document and its mapped SHA-256. |
| Shell syntax of all six guide shell blocks | All six parse with `sh -n`; this does not execute the three reconstruction/project examples. |
| Seven relevant source-map entries against the complete pinned Git trees | Each selected path's Git mode and object ID agree with its recorded baseline entry. Only materialized files were byte-hashed. |
| Local original/current historical documentation bytes | The named FINDINGS, REPORTS and REPRODUCE files match their mapped SHA-256 values. |
| Current map and three current wrapper files against the pinned commit | Local bytes match the exact Git source objects. |
| Guide navigation | 15 link uses, 14 distinct destinations: 10 relative uses / 9 distinct relative targets and five pinned GitHub destinations. All existing source targets resolve. The new validation target was deliberately recorded as pending during review and is supplied by this file. |

Exact Python lookup stdout:

```text
baseline: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
original: proofs/REPRODUCE.md
selected: proofs/REPRODUCE.md
sha256: aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a
source hash: MATCH
```

The corresponding three guide commands were independently executed by
`/root/guide_command_validation`. The non-author semantic reviewer
`/root/guide_semantic_review` separately executed the lookup and Git commands
while confirming their meaning. Neither specialist authored the guide or
modified existing repository source. Their complete reports are retained;
these are genuine separate specialists within the same parent session.

The seven entry comparisons concern `proofs/README.md`,
`proofs/FINDINGS.md`, `proofs/REPORTS.md`, `proofs/REPRODUCE.md`,
`proofs/research/README.md`, `proofs/verify_release.py`, and
`proofs/verify_project.py`. The command validator hashed three materialized
selected files and reported four selected files absent from the sparse checkout;
it did not silently download or claim to hash those absent contents.

## Inspection-only commands

The direct release wrapper, the scoped consolidation-core Lean command, and
the subdirectory `sh -c` example are **COMMAND_INSPECTED**. Their command syntax
and semantics were inspected, but they were not run as project checks.
No full source-map reconstruction, release replay, fresh Lean build, finite
certificate replay, or complete migration-preservation audit occurred.

The parent also scanned all map entries for the exact current/preserved paths
`proofs/STATUS.md` and `proofs/OPEN_PROBLEMS.md`. Neither path is an original
key or an exact current/preserved selection at this snapshot. That scoped
selector fact was relayed to the responsible documentation agents; it does
not approve their later edits or anticipate later source-map changes.

## Completion and publication checks

The semantic review passed the exact guide hash above and requested that this
linked validation record be supplied before publication. The command review
likewise treated this new target as an explicit pending package file. The
author completes that target and retains the original reviewers' observations
rather than rewriting them as observations of a later state.

Final file membership, byte hashes, whitespace and remote readback belong to
the publication receipt for the exact resulting commit. Neither a published
branch nor a documentation review is represented here as main integration
or a new mathematical verification result.
