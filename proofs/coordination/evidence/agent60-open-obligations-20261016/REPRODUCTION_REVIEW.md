# Reproduction and reference review — PR #156

**Verdict: PASS WITH LIMITATIONS. No documentation change is required by this review.**

The reviewed document accurately separates source interfaces, retained historical execution records, semantic review, and the mathematical input still needed to instantiate the certificate route. Its source links and line ranges support the stated interfaces. The archived prior version is preserved exactly.

## Review target and scope

| Item | Independently observed value |
|---|---|
| Repository | `taco-jpg/p196-algorithm` |
| Reviewed revision | `320332336763fb872b87dee4df91e91ec06242e3` |
| Reviewed file | `proofs/OPEN_PROBLEMS.md` |
| Reviewed document blob | `ad69f7a78074f828cb81be6e7f026642d3a96653` |
| Document’s source checkpoint | `10a173cb635fa8d03e357f454232816fc3e77609` |
| Preserved original blob | `6cabf332c864b5d73d0d236c7ce31146f8d26401` |
| Source-map blob | `e5f8d27bf09f50f8b9756bf91dff02e992aa4a32` |
| Historical build-manifest blob | `bad4434cb769d33d3a91020aadab69757701891f` |

I fetched the [actual document at the reviewed revision](https://github.com/taco-jpg/p196-algorithm/blob/320332336763fb872b87dee4df91e91ec06242e3/proofs/OPEN_PROBLEMS.md), its baseline predecessor, all eleven distinct file targets referenced by the document, and the additional historical `REVIEW_RESULT.json` and `PROVENANCE_CHECK.json`.

The mathematical review here is limited to the accuracy of the documented interfaces and evidence boundaries. It is not a new proof review of the complete dependency closure.

## Reference and declaration checks

The document contains **16 reference definitions and 16 corresponding reference usages**, with no undefined reference labels. Its external evidence links specify the immutable source-checkpoint commit. The relative preservation link resolves from `proofs/OPEN_PROBLEMS.md` to the intended archival file at the reviewed revision.

All **seven source line ranges** were checked against the actual retrieved source texts:

| Reference | Source and range | Result |
|---|---|---|
| Checker | `ReturnCertificate__b037c18e81a43bb5.lean`, lines 187–223 | Includes `LocalOK`, `Valid`, `check`, and `check_sound`. |
| Soundness | Same source, lines 256–273 | Includes the full `certificate_sound` signature and its successor-based conclusion. |
| Realization | Same source, lines 371–380 | Includes `template_realized` and all stated realization hypotheses. |
| Original existence | Same source, lines 383–416 | Includes `Admissible0` and `certificate_existence`. |
| Automatic admissibility | `AdmissibleHeads__e610dff2fe6106d5.lean`, lines 165–168 | Includes `automatic_admissibility`. |
| Check-only existence | Same source, lines 170–173 | Includes `certificate_existence_of_check`. |
| Period restrictions | `CertificateChecked__28f9e37f0a4c7634.lean`, lines 11–46 | Includes all three restriction statements and their distinct premises. |

The inspected signatures support the document’s critical distinctions:

- `certificate_sound` proves nonpalindromicity for `orbit (step n) k`, starting at the successor of the realized integer. The documentation correctly retains the separate finite-prefix obligation for an application to 196.
- `template_realized` has explicit phase, positive first-band length, bounded-coefficient, mirrored-center, and positive-head hypotheses.
- `certificate_existence` accepts both checker acceptance and the Boolean admissibility proof.
- `automatic_admissibility` derives admissibility from checker acceptance.
- `certificate_existence_of_check` requires no separate unsupplied admissibility hypothesis.
- The checked period restrictions preserve their separate checker, six-phase, and saturation assumptions.

The exact three retrieved source blobs match the corresponding historical manifest entries:

| Source | Retrieved and manifest blob |
|---|---|
| `ReturnCertificate` | `95196cfe2da9b224412a9c31910163cf5784f996` |
| `AdmissibleHeads` | `0754d027159fef059efc38a9692d4edf278c0039` |
| `CertificateChecked` | `7b4dad86b0a17362ba8e4d4a99603e933ec314d1` |

The current `AdmissibleHeads__e610dff2fe6106d5.lean` link maps to Agent112’s original contribution. The historical build used Agent110’s retained snapshot of that source. Their identical blob identity supports this cross-reference without treating the two paths as different mathematical versions.

## Historical execution and review provenance

The historical manifest was retrieved both by its archived path and by blob SHA; their returned contents were equal. It records:

- Lean **4.19.0**, release commit prefix `6caaee842e94`.
- A run beginning on 15 October 2026 at `16:24:53.274915+00:00` and ending at `16:28:08.889739+00:00`.
- **19 selected project modules**, including `ReturnCertificate`, `AdmissibleHeads`, `CertificateChecked`, and `All`.
- **21 recorded commands**: one version query, nineteen compilation commands, and one environment-audit command.
- Exit code zero for every recorded command.
- `empty_build_directory_created: true`.
- `objects_reused: false`.
- `all_source_hashes_unchanged: true`.

These are historical manifest assertions and retained records, not execution results produced during this review.

The saved `ReturnCertificate.log` and `AdmissibleHeads.log` explicitly name all five interfaces in the document’s declaration table. Their listed axiom dependencies are subsets of `propext`, `Classical.choice`, and `Quot.sound`. The manifest also contains corresponding entries for those five declarations.

An in-memory check of the manifest’s **2,180 recorded axiom-audit entries** found no axiom outside that whitelist. This confirms the contents and internal consistency of the saved audit data; it does not rerun Lean’s dependency analysis.

The retrieved `SEMANTIC_REVIEW.md`, `REVIEW_RESULT.json`, and `PROVENANCE_CHECK.json` support the document’s attribution of a separate historical semantic and provenance review. In particular, they distinguish Agent112’s original automatic-admissibility work from Agent110’s wrapper review, explain the symbolic-growth argument used before integer realization, preserve the phase and saturation premises, and explicitly deny construction of an accepted certificate instance.

## Source map and preservation

I fetched the complete source map by blob because the ordinary file fetch returned an empty content field for that large file. Its path lookup at the source-checkpoint revision independently returned the expected blob identity.

The complete map contains **9,161 path entries**. In-memory comparisons established:

- **19/19 manifest sources** have corresponding source-map entries with matching recorded Git blob identities and SHA-256 values.
- **21/21 command-log entries** have corresponding source-map entries with matching recorded SHA-256 values.
- The document’s cited historical manifest, logs, and review paths map to their retained archive locations.
- The two fetched named log blobs match their source-map blob identities.

These comparisons cross-check published metadata. I did **not** independently recompute every source or log SHA-256, and I did not fetch all nineteen complete module bodies or all twenty-one complete logs.

For the previous `OPEN_PROBLEMS.md`, verification is stronger than a metadata-only comparison: I independently fetched the baseline and archived texts. They are exactly equal, and both return blob `6cabf332c864b5d73d0d236c7ce31146f8d26401`.

The absence of `OPEN_PROBLEMS.md` from the older source map is not a preservation defect: its separate archival preservation was verified directly.

## Execution classification and limits

| Classification | What actually occurred |
|---|---|
| **COMMAND_INSPECTED** | The historical manifest’s version, compilation, and audit command arguments; their recorded working directory, `LEAN_PATH`, compiler flags, exit codes, and log references were inspected. |
| **COMMAND_EXECUTED** | GitHub read operations and lightweight JavaScript checks in the `functions` V8 runtime: JSON parsing, reference resolution, line-range extraction, string equality, declaration matching, metadata comparisons, command counts, and axiom-whitelist comparisons. |
| **EXPECTED_OUTPUT_CONFIRMED** | The actual retrieved historical logs contain the expected five declaration names and recorded axiom lists. The executed JavaScript checks produced the successful comparisons reported above. |
| **NOT EXECUTED** | No shell command, checkout reconstruction, Python verifier, Lean compilation, axiom-audit replay, dependency installation, discovery computation, inventory regeneration, or GPU job was performed by this subagent. |

The manifest uses historical absolute compiler and build-directory paths. Reproducing those commands would require restoring the appropriate source layout, module names, toolchain, and `LEAN_PATH`. The reviewed page presents them as **retained verification records**, not as a newly tested portable replay recipe. That wording is appropriate.

I did not independently test local shell or Lean availability. The parent reported proxy and disk-capacity failures; those remain attributed environmental observations rather than failures I personally reproduced.

## Conclusion

No broken cited file, incorrect source line range, missing declaration, altered original, or unsupported fresh-execution claim was found.

The page correctly avoids equating source publication with compilation, compilation with theorem adequacy, or a conditional certificate implication with an accepted concrete certificate. Its discussion of 196 retains the required actual-orbit entry, matching realization and band bounds, and finite-prefix verification. Its treatment of the incomplete historical accepted-build catalogue also agrees with the retrieved registry and status checkpoint.

**Review status: PASS WITH LIMITATIONS.** The limitations are the explicitly bounded source-and-record inspection described above; this review adds no mathematical acceptance or new compiler result.

**Coordination delivery:** the earlier attempted issue announcement was interrupted without confirmed delivery. I have made no subsequent public comment or repository mutation. Its delivery remains unconfirmed, and this report may be relayed by the parent with attribution.
