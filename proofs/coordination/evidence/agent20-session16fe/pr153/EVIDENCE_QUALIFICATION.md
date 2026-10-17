# PR #153 evidence qualification and completion packet

## Disposition

**PASS_EVIDENCE_INTEGRITY; REUSE_EXISTING_SEMANTIC_REVIEW; INDEPENDENT_BUILD_NOT_ESTABLISHED_BY_PUBLISHED_EVIDENCE.**

The 13 incoming files and all 46 development-archive members are internally consistent. The frozen generic and numeric Lean modules exactly match the completed independent semantic implementation review. All 11 local dependency identities are unchanged between the contribution head, the observed target base, and the declared source-main revision. No new mathematical review is required merely because this evidence qualification was performed.

The published compiler evidence is author development. It records successful final author attempts and complete 21 + 8 theorem axiom outputs, but contains no independent compiler-run logs, no independent API-error logs, no completed independent runtime report, and no portable build verifier. This report does not certify compilation, runtime authenticity, a combined-tree build, platform checks, readiness, or merge acceptance. No Lean build or source repair was performed in this task.

## Scope, identities, and ownership

- Repository: `taco-jpg/p196-algorithm`; PR #153.
- Source head H: `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`.
- Observed target base B: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
- Declared source main S: `54ac7c885e54ce74190b85ec82cceca2b23c2e38`.
- Original mathematical source revision: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Evidence qualifier: Agent #20, session `16fe9eef625c`, genuine scoped specialist `/root/evidence_qualifier`; no source authorship or independent Lean execution.
- Source owner and assigned runtime auditor remain Agent #52, session `04d7e624b3b0`, and its `/root/runtime_audit`.
- Main writer, as supplied by the coordinator: Agent #31, session `02893e4f368d`; no main slot claimed by this task.
- The coordinator supplied accepted evidence-task readback at coordination commit `f68c81c25b6147f668494cebdfe49eaab92a15ad`, task blob `809ca03aaf03a291cdc051ce1e7313cc81a4a39a`. This specialist did not mutate remote state.
- This qualification covers exact files in `proofs/contributions/agent-52/digit-sum-density-20261016/` and their declared dependency identities. Current remote PR/check/ownership state remains the delivery coordinator's responsibility.

## Incoming file inventory

The path prefix below is the contribution directory above. All 13 files are added relative to B, have Git mode `100644`, and total **114,502 bytes**. The JSON inventory also records complete repository paths.

| File | Bytes | Git blob | SHA256 | Qualification |
|---|---:|---|---|---|
| `Agent52Density.lean` | 10068 | `7b2e0b94973a9f76db21e90d635c9660ff357aef` | `cb68857fee8f4bf8df25158ac1d19a7d3996894dbc4f8dc81789861ef8f5f549` | Accepted candidate source: 3 definitions, 21 theorems; exact semantic-review and final author-attempt identity. |
| `Agent52DigitSumDensity.lean` | 4817 | `045d69bc98c868b47e8b26d83f195acceae8d45b` | `47efae19090c66b43973d5dc754f2375f83747b900b3cc5f16966af06608bc46` | Accepted candidate source: 8 theorems; exact semantic-review and author numeric-attempt identity. |
| `CONTRACT.json` | 4376 | `da4a71ac68eea914f5577509e1ff597a428b6d3e` | `86b6242e6b4331ed56a89d85a944bfd70e18bbbacf3b0eee4b211b3cae0e1d32` | Exact independently reviewed contract; operational status remains the initial NOT_YET_BUILT checkpoint. |
| `COVERAGE.json` | 989 | `14daad8651ab083cb108e76705cc7a111d51630f` | `899ef42d16caa82c5ccefd90070e4642996aa765f4361ec0b0475375e7cb26ae` | Accurately distinguishes author-checked claims and pending independent full closure; no independent pass claimed. |
| `README.md` | 5127 | `5c80bcd7618a0c5e71b63d27fa0942474f680707` | `c752024e16abe23614122a59a19156026a27eb3f1d722d8b84e8f41f8108126b` | Accurately reports author development, completed semantic review, and independent build/verifier still in progress. |
| `dependencies.json` | 4493 | `a4e1745c95c1c13fa48b6644a194f5f26be552b4` | `3debdf14f7c8efc13997e3c4d23555b1fc4a6deaa5df9d3e7f4e439713495030` | 11 local modules; every declared blob and SHA256 matches H, B, and source_main. |
| `evidence/development-20261016.tar.gz` | 12532 | `ac0b3a51994bc1af58a2b7fbdfcb473e951329f9` | `1b0639ca1b28442392cbbcf6b0c4a8d2f861b64873d43e92e6537b38c6b433ca` | Complete author-development archive; 46 verified regular members, including both failed attempts. |
| `evidence/development-manifest.json` | 8956 | `40f54e0da7718f538ad5de52f674d4d4e2e6ddec` | `400b24b39aa56b39ec3e6240d0e44c2771cdaef95a4bb13fbb0ef4283bf3667a` | Exact archive digest and complete per-member path/size/SHA256 manifest; all 46 entries match. |
| `review/semantic/CENSUS.md` | 16085 | `f2ce61c04aff3ea84dd1fc889ba8cf3d8e377944` | `8d273ae1a7e798e16b9a727bec6668eabfd4077f0e4bbe0cad23e43ea2e16bc4` | Retained scoped historical census; explicit search limits; does not certify build or claim ownership of other tasks. |
| `review/semantic/CONTRACT_REVIEW.md` | 16010 | `b06c8b95e8f26439b9fc7a81aa74e024e319c83e` | `ec40a2ef8b4abf6c5826765707507f57f62f50985c66d584d690278a9e534989` | Reusable independent PASS_SEMANTIC_CONTRACT; exact contract and named dependency hashes agree. |
| `review/semantic/IMPLEMENTATION_REVIEW.md` | 15089 | `de32e17b5838fd5154e7e3e3f54c6742b4d87436` | `37a943aef1a9c7345a90fb4406c1705d750adec9cee106a4ce0cfbd03fec9b2a` | Reusable independent PASS_SEMANTIC_IMPLEMENTATION for both exact current modules; explicitly excludes compiler acceptance. |
| `source/mathlib-lake-manifest.json` | 2786 | `92a8049abc1f1b43ae2b4a6605616034f0dd2682` | `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752` | Exact declared manifest hash; 8 pinned package revisions; records environment input, not cache authenticity or an executed build. |
| `source/strengthening_notes.txt` | 13174 | `7103ee939d82740b970dd23fb91e9db50db4ea54` | `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` | Byte-identical original mathematical source, matching recorded Git blob and SHA256; section 6 supplies the decimal specialization. |

## Archive verification and preservation

Archive `development-20261016.tar.gz`: **12,532 bytes**, SHA256 `1b0639ca1b28442392cbbcf6b0c4a8d2f861b64873d43e92e6537b38c6b433ca`. It contains **46 regular members**, **0 directory entries**, and **85,372 uncompressed member bytes**. Exactly 46 manifest entries match the archive by canonical relative path, byte length, and SHA256. There are no duplicate names, missing entries, unlisted entries, symbolic links, hard links, sparse files, absolute paths, or parent-traversal paths. Each file was read from the tar stream and written beneath the permitted evidence directory only after validation; `extractall` was not used.

The complete member inventory is retained in `archive-verification.json`; the original manifest and archive are preserved unchanged under `source/evidence/`. Archive content consists of **32 logs, 9 Lean source snapshots, and 5 JSON result/summary records**.

| Group | Members | Retained evidence | Recorded outcome |
|---|---:|---|---|
| `development/baseline-001/` | 30 | 26 stdout/stderr logs, 3 Agent9 snapshots, 1 summary | Lean version plus 12 module commands each record exit 0; author baseline |
| `development/generic/attempt-001/` | 3 | Agent9 count source, log, result | Exit 1 before generic compilation: input source outside current Lean root directory |
| `development/generic/attempt-002/` | 5 | Count and generic sources, both logs, result | Count exit 0; superseded generic exit 1 on liminf boundedness arguments |
| `development/generic/attempt-003/` | 5 | Count and final generic sources, both logs, result | Both record exit 0; final generic SHA256 matches H |
| `development/numeric/attempt-001/` | 3 | Numeric source, log, result | Records exit 0; explicitly labeled `AUTHOR_DEVELOPMENT_BUILD_NOT_FULL_CLOSURE` |

The baseline includes eleven dependency modules and the Agent9 audit module: **12 modules**, rather than twelve dependencies of the new density source. A fresh verification of the density contribution requires the **eleven dependency modules plus two new modules**. Adding an audit driver does not change that source-closure count.

The archive has 19 recorded command invocations: one Lean-version query and 18 compilation invocations. Two compilation invocations record exit 1; the other 16 record exit 0. This is an inventory of retained records, not an independently witnessed execution count. All 26 baseline stdout/stderr hashes match their summary, and the baseline source snapshot hashes match the declared source identities.

### Failed attempts remain part of the evidence

The first failure is the exact Lean root-directory diagnostic in `generic/attempt-001/Agent9WindowIntervalCounts.log`. The second first reports `Agent52Density.lean:89:8: error: could not synthesize default value for parameter 'hu' using tactics`, followed by failures at lines 101 and 108 and consequential no-goals diagnostics. Its source SHA256 is `98ec96d671ea8235097cc9113d7181ba2460e2558e424448d115089a249252ef`.

The failed generic log contains `sorryAx` in five declarations: `lowerAsymptoticDensity_le_one`, `lowerBanachDensity_le_one`, `lowerBanachDensity_le_lowerAsymptoticDensity`, `count_lowerAsymptoticDensity`, and `window_lowerAsymptoticDensity`. These occurrences belong to the explicitly failed, superseded attempt; they are not evidence that the frozen final source passed with `sorryAx`. Both source versions and the original logs remain intact. `generic-failed-to-published.diff` records their difference without changing either.

## Author versus independent verification

| Evidence | What is established here | What is not established |
|---|---|---|
| Baseline author summary and logs | Log hashes, source pins, declared fresh-directory/no-copied-local-objects flags, command arguments, exit records, Lean version output | Runtime executable authenticity or independently reproduced baseline execution |
| Final generic author attempt | Exact current source snapshot; 21 theorem declarations, 21 `#print axioms` directives, 21 matching reported axiom inventories | Complete independent local closure, effective generic `LEAN_PATH`, or independently reproduced output |
| Numeric author attempt | Exact current source snapshot; 8 directives and 8 matching reported axiom inventories; explicit recorded reuse of author generic and baseline object directories | An independent build or a fresh numeric closure |
| Semantic contract review | Independent `PASS_SEMANTIC_CONTRACT`; contract SHA256 and named source interfaces match | Compiler, runtime, or axiom audit |
| Semantic implementation review | Independent `PASS_SEMANTIC_IMPLEMENTATION`; both frozen modules and CONTRACT.json exactly match | Fresh build; review explicitly states no Lean run and no inspection of final compiler/axiom logs |
| Mathlib Lake manifest | Exact contract hash; eight package pins retained | That a particular cached object set matches the manifest, a clean Mathlib rebuild, or authenticity of any downloaded runtime |

The final generic author log has SHA256 `cee1a3414c145f38f29e05888b7d946904d075ecdd29dc1b4f32f4e16d16fffe`; the numeric log has SHA256 `bc423128f5493f1a4cf50b88bcb186aca69265a389e25a045a7a85368cad5d1e`. Their 29 distinct theorem names exactly match the current source theorem inventory and source `#print axioms` directives. Each reported set is a subset of `{propext, Classical.choice, Quot.sound}`; `intervalCount_le_length` reports only `propext`, and the other 28 report the three allowed axioms. The generic module additionally has three definitions.

The baseline metadata names Lean `4.19.0`, commit `6caaee842e94`, and executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The contract names Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b` and Lake-manifest SHA256 `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752`. The manifest bytes match that hash. This task did not inspect or execute those runtime binaries or cached Mathlib objects.

**No independent compiler execution or independent API-error log is present in the 13 incoming files or the 46 archive members.** The only retained build outcomes belong to author development. README and COVERAGE explicitly leave the independent build pending, so absence is consistent with the checkpoint and cannot be promoted to a passed gate. This statement is limited to the inspected published package; unpublished audit checkpoints may exist with the active owner.

## Source closure and reuse of semantic review

All eleven entries in `dependencies.json` have matching Git blob identities at H, B, and S; their declared SHA256 values also match actual recovered bytes. The nine original dependency blobs were read directly from local Git objects. The two Agent9 blob objects were absent from the local object store despite their tree entries being present. Their exact source snapshots were recovered from the verified published archive: both SHA256 and Git's blob SHA1 match the tree entries at all three revisions. Initial read errors are retained in `dependency-verification-initial.json`; corrected verified recovery appears in `dependency-verification.json`. This was a local object-availability issue, not missing repository source.

The inspected local import names close over the eleven declared modules, Std, and the new module imports; the generic module additionally imports the explicitly named Mathlib modules. No dependency source identity change was found that would invalidate the retained semantic review. This establishes source correspondence, not resolution of imports in an unobserved runtime search path.

The original `strengthening_notes.txt` source has Git blob `7103ee939d82740b970dd23fb91e9db50db4ea54` and SHA256 `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`; its preserved original-layout archive entry and the incoming source copy have the same blob identity.

The generic current SHA256 is `cb68857fee8f4bf8df25158ac1d19a7d3996894dbc4f8dc81789861ef8f5f549`; the numeric current SHA256 is `47efae19090c66b43973d5dc754f2375f83747b900b3cc5f16966af06608bc46`; CONTRACT.json is `86b6242e6b4331ed56a89d85a944bfd70e18bbbacf3b0eee4b211b3cae0e1d32`. These are exactly the reviewed values. The review can therefore be reused for its stated semantic scope. This task did not repeat its proof analysis as a new acceptance gate.

## Concrete recovery and audit-completion packet

1. **Recover the active independent auditor checkpoint first.** Ask Agent #52 and its assigned `/root/runtime_audit` for the exact audit checkpoint covering the two frozen source hashes above. Request any existing successful, failed, interrupted, or API-error records with source identities, commands, exit status, timestamps, and substantive raw logs. The present archive does not contain them; do not start a duplicate full build merely because they are unpublished.
2. **Retain and qualify the independent run environment.** The checkpoint must identify Lean version/commit and executable provenance, Mathlib commit and exact Lake manifest, cached-package provenance if cached dependencies are used, the source-to-module filename mapping, effective `LEAN_PATH`, and whether the local build directory was initially free of repository-generated `.olean` files. Lean/Mathlib distribution binaries and compiled objects remain reproducible infrastructure; they need not be committed as research evidence.
3. **Complete only the uncovered build obligation.** If no qualifying run exists, the authorized independent auditor must freshly compile the eleven pinned local dependencies plus `Agent52Density` and `Agent52DigitSumDensity`, preserving actual commands and stdout/stderr/exit codes. Module order can be `LychrelDigitSums`, `SharedProfile`, `ProfileDynamics`, `ProfileIsolation`, `UniformEscape`, `SharpProfileBounds`, `SharpUniformEscape`, `DecimalEmbedding`, `SharpUniformDecimal`, `Agent9WindowIntervalCounts`, `Agent9DigitSumIntervalCounts`, `Agent52Density`, `Agent52DigitSumDensity`. Mathlib cached build products may be used according to existing policy; do not relabel that as a fresh build of all Mathlib.
4. **Audit the actual independent axiom output.** Require all 29 current theorem declarations, compare the exact inventory, reject omissions/duplicates and every axiom outside the allowed three, and record the source and log SHA256 values. Retain failed independent attempts too. Reusing the author log does not satisfy this independent-execution obligation.
5. **Publish a portable verifier and evidence through the source owner.** The current package has no build script or portable verifier. The owner should add the audited reproduction procedure/script, complete manifests, runtime report, and substantive failure/success logs in an additive checkpoint while preserving the 13 incoming files and development archive. Record the initial CONTRACT status as historical rather than silently treating `NOT_YET_BUILT` as current truth. A new status document may preserve the reviewed contract bytes.
6. **Refresh delivery at the new exact head.** The delivery coordinator should confirm that the two mathematical source hashes and dependency identities remain unchanged, reuse the semantic pass for unchanged mathematics, qualify the completed runtime evidence, and check the actual combined tree and platform requirements against the then-current base. Any substantive source repair needs the affected independent review; evidence-only additions do not inherently reset semantic review. The actual main writer must own the final mutation.

### Current precise blockers and boundaries

- Independent source-closure build: **NOT_ESTABLISHED_BY_PUBLISHED_EVIDENCE**. Remedy attempted here: exhaustive package/archive qualification and exact artifact-gap identification. Remaining dependency: active source owner/assigned auditor checkpoint or its authorized completion.
- Independent transitive axiom audit: **NOT_ESTABLISHED_BY_PUBLISHED_EVIDENCE**. Existing author outputs are retained and complete; remaining dependency is independent execution and authenticated environment/source linkage.
- Portable reproduction verifier: **ABSENT_FROM_PUBLISHED_PACKAGE**. Remaining dependency is additive owner publication and review of the actual script/procedure.
- Combined-tree/platform/ready/merge state: **OUTSIDE_THIS_SCOPED_QUALIFICATION**. No claim about current remote success, readiness, or integration follows from this report.
- New mathematical source defect: **NONE IDENTIFIED BY THIS EVIDENCE QUALIFICATION**; the reused independent semantic report remains the authority for semantic acceptance. No source repair was authored here.

## Reproduction and local outputs

`python pr153-evidence/verify_evidence.py` performs only byte/hash/tree/log-inventory checks. It executes no Lean code and makes no Git or remote mutation. It checks the 13 files, all 46 archive members, eleven dependency identities at three revisions, 26 baseline log hashes, and all 29 current author axiom records. Its result is deliberately named `PASS_EVIDENCE_INTEGRITY_ONLY`.

The packet contains the original incoming source files, safely extracted original archive members, machine-readable inventories, the retained initial dependency-read failures, their verified recovery, the failed-to-published source diff, this report, and the checker. It contains no unrelated user prompt, credentials, runtime distribution, compiled objects, or unrelated transport metadata. The delivery coordinator retains accountability for review, publication, routing, and further integration actions.
