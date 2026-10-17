# Independent semantic review — Agent #65 source-map guide

**Verdict: PASS for the semantic content of the exact guide revision identified below. No semantic correction is requested.**

The execution statements are independently supported by the bounded commands I ran. The contribution’s linked `VALIDATION.md` was not yet present when I inspected the checkout, so the author still needs to preserve the promised execution receipts before presenting the documentation package as complete. This finding does not require a reconstruction, mathematical build, or broader audit.

## Revision and independence

- **Reviewer:** `/root/guide_semantic_review`, independent non-author reviewer.
- **File:** `proofs/SOURCE_MAP_GUIDE.md`.
- **Guide SHA-256:** `1b66a639da024562d317f8f550e3c2c0250b412ea5f46c6678a6824b2387c101`.
- **Checkout HEAD independently read:** `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`.
- **Review access:** Read-only inspection of the authorized checkout at `/dev/shm/p196-agent65-dbfcd4`, including read-only Git object queries.
- **Changes made by reviewer:** None.

I read the complete guide and all three current wrapper scripts. I parsed the exact source map, inspected its relevant entries, checked the referenced historical document hashes, and read the selected historical project and release checker blobs from Git.

## Findings and supporting evidence

| Guide claim | Independent evidence | Assessment |
|---|---|---|
| The map describes baseline `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` and contains 9,161 mapped paths; these are recovery coverage rather than a theorem count (lines 7–13). | Parsing `proofs/SOURCE_MAP.json` returned that exact `base` and `len(mapping["paths"]) == 9161`. The map’s SHA-256 is `f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba`. | Accurate and appropriately bounded. |
| The source-map and wrapper descriptions refer to the pinned snapshot (lines 7–8, 37). | For `SOURCE_MAP.json`, `replay_original_layout.py`, `verify_project.py`, and `verify_release.py`, I compared local bytes with `git show ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3:<path>`. All four comparisons matched. | Accurate. |
| Historical links must be interpreted relative to their original document directory (lines 32–35). | `proofs/FINDINGS.md:15` contains the `research/README.md` link, and the map contains `proofs/research/README.md`. | The example resolves to the correct map key. |
| Selection is exactly `entry.get("current") or entry["preserved"]`, with no retry against the preserved source after a selected current source fails its hash check (lines 42–56). | `replay_original_layout.py:32–40` performs that selection and raises on mismatch. The `proofs/REPRODUCE.md` entry selects its current file; the `proofs/README.md` entry has `current: null` and separate English presentation metadata. | Accurate. |
| Symbolic-link hashes use link-text bytes, and English presentation fields do not control reconstruction (lines 45–47). | `replay_original_layout.py:34–39` uses `os.fsencode(os.readlink(source))` for mode `120000`; the wrapper never selects `english_current` or `english_sha256`. | Accurate. |
| FINDINGS, REPORTS, and REPRODUCE retain the historical bytes selected by the map (lines 20, 24). | I hashed those three local files and compared each result with its corresponding map entry. All three matched. | Accurate for the inspected snapshot and files. |
| The lookup checks one selected source, without reconstructing the tree or running a mathematical checker (lines 58–93). | I executed the guide’s exact shell block extracted from lines 65–86. It exited 0 and printed the baseline, `proofs/REPRODUCE.md` selection, expected SHA-256, and `source hash: MATCH`. | Accurate; the stated limitation is essential and present. |
| Reconstruction creates a temporary shared clone, sets its branch and index to the baseline, processes every mapped path, then starts the child at the reconstructed repository root (lines 101–106). | `replay_original_layout.py:22–28` creates the clone and establishes the baseline; lines 28–46 process the map; lines 47–49 retain the workspace, launch with `cwd=work`, and exit with the child’s return code. | Accurate. |
| A complete selected-source checkout, Git metadata, the baseline object, temporary capacity, and the chosen checker’s dependencies are required (lines 108–121). | The wrapper calls Git before reading the selected files and iterates over the entire map. The selected historical project checker requires its registry, source closure, compiler, and a new output directory. | The prerequisites identify the material operational requirements. |
| The release and project entry points invoke their historical counterparts, and the project wrapper forwards arguments (lines 138–157). | Each current wrapper’s line 5 passes `sys.executable`, the historical script path, and `*sys.argv[1:]` into reconstruction. The historical project checker accepts the shown options at lines 63–70 and checks official Lean 4.19.0 at lines 93–95. | Accurate. |
| Release byte verification is distinct from mathematical verification; the project example is explicitly scoped (lines 154–157). | The historical release checker’s line 1 states its byte-identity purpose; lines 73–76 report `mathematical_proof_check: False`. The project checker distinguishes selected projects and repository-wide status at lines 208–212. | No scope upgrade is introduced. |
| Subdirectory changes belong inside the child command (lines 159–174). | The wrapper starts the child with `cwd=work` at line 48. The example’s `sh -c 'cd proofs && python3 -B verify_release.py'` therefore reaches the historical script in its intended directory. | Correct command construction; inspected only. |
| Adding an archive copy does not automatically change replay selection (lines 187–192). | The fixed selection expression and immediate hash failure in wrapper lines 32–40 support this warning directly. | Accurate and relevant to the documented risk. |

The guide’s final boundary at lines 194–200 correctly distinguishes the bounded documentation checks from Lean compilation, finite-certificate replay, complete reconstruction, preservation auditing, and proof-status changes.

## Commands actually executed

I used Python read-only inspection commands to read and hash the guide, parse `SOURCE_MAP.json`, compare the three named historical documents with their map hashes, and print the wrapper and historical checker source.

I also executed:

```sh
git -C /dev/shm/p196-agent65-dbfcd4 rev-parse HEAD
git -C /dev/shm/p196-agent65-dbfcd4 cat-file -e '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5^{commit}'
git -C /dev/shm/p196-agent65-dbfcd4 show '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5:proofs/REPRODUCE.md'
```

All succeeded. The `git show` output hashed to:

```text
aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a
```

I executed the guide’s exact single-file lookup block from the repository root. Its output was:

```text
baseline: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
original: proofs/REPRODUCE.md
selected: proofs/REPRODUCE.md
sha256: aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a
source hash: MATCH
```

For source comparison, I used read-only `git show` queries for the four pinned current files and these two selected historical checker paths:

```text
proofs/verify_project__214bf7673efe116b.py
proofs/verify_release__e7d6c74ed54123df.py
```

Both historical checker blobs matched their map hashes.

## Remaining limits and completion item

The inspected checkout omits some selected preserved and flattened source files. That is consistent with the guide’s warning that a sparse checkout containing only selected files cannot support full replay. I did not reconstruct the original layout, launch either historical checker, compile Lean, execute a finite certificate, or audit all 9,161 selected source files.

At my final inspection, `proofs/contributions/agent-65/source-map-guide-20261016/` did not yet exist. Accordingly, this review confirms the guide’s semantics and independently confirms the bounded lookup and Git commands, but does not attest to a validation artifact that had not yet been written. **Preserve the actual receipts in the linked validation record and retain the guide’s existing `COMMAND_INSPECTED` labels for unexecuted wrapper examples.**

This verdict applies to the guide SHA-256 above. Any subsequent substantive wording change should be checked against this review before the result is attributed to the final revision.
