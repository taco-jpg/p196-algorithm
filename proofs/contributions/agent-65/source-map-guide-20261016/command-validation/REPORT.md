# Independent command and link validation report

**Result: PASS for the bounded checks performed.** No defect was found in the inspected guide. The new `VALIDATION.md` destination was still absent when checked; it was treated as an explicitly allowlisted candidate path, not as an existing source-tree file. The publisher must include that file before publishing the guide.

## 1. Scope and identity

Reviewed artifact:

```text
proofs/SOURCE_MAP_GUIDE.md
SHA-256: 1b66a639da024562d317f8f550e3c2c0250b412ea5f46c6678a6824b2387c101
```

The guide hash was identical before execution, after execution, and at the final inventory check.

Repository source snapshot:

```text
Repository: taco-jpg/p196-algorithm
Snapshot:   ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3
Baseline:   2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
Checkout:   /dev/shm/p196-agent65-dbfcd4
```

The guide, the entire current replay wrapper, and both current entry-point wrappers were inspected. Exactly the guide's first Python lookup and its two Git commands were executed. The remaining guide commands were inspected and syntax-checked, without executing wrappers or checkers.

No source file, guide, index, ref, branch, PR, manifest, or generated inventory was changed by this reviewer.

## 2. Executed commands

All three executions used the repository root as their working directory:

```text
/dev/shm/p196-agent65-dbfcd4
```

### 2.1 Source-map lookup

**Status: EXECUTED; EXPECTED_OUTPUT_CONFIRMED**

Exact process argv:

```json
["python3", "-", "proofs/REPRODUCE.md"]
```

Standard input was extracted verbatim from the first guide shell block, between its opening heredoc command and terminating `PY`.

```text
Python stdin SHA-256:
aab3f5f61eb33f78f739257f402a06fcc247b584f5d6cc2b6eaf28ac9a33c15e
```

Exact stdout, including the final newline:

```text
baseline: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
original: proofs/REPRODUCE.md
selected: proofs/REPRODUCE.md
sha256: aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a
source hash: MATCH
```

```text
Exit code:     0
stderr:        empty
stdout SHA-256:
91479112c822fe8b2d21d6cccdc44d60901eb67549fcc09d8abf3f59cd5ba6c0
stderr SHA-256:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This directly confirms the selected path and SHA-256 printed in the guide.

### 2.2 Baseline commit availability

**Status: EXECUTED; EXPECTED_OUTPUT_CONFIRMED**

Exact argv:

```json
["git", "cat-file", "-e", "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5^{commit}"]
```

```text
Exit code: 0
stdout:    empty
stderr:    empty
```

Both empty streams have SHA-256:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

This confirms availability of the specified commit object. It does not establish availability of every selected replay input.

### 2.3 Historical document retrieval

**Status: EXECUTED; EXPECTED_OUTPUT_CONFIRMED**

Exact argv:

```json
["git", "show", "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5:proofs/REPRODUCE.md"]
```

```text
Exit code:     0
stderr:        empty
stdout length: 39,464 bytes
stdout SHA-256:
aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a
stderr SHA-256:
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The exact stdout is the complete content of the baseline blob:

```text
Commit: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5
Path:   proofs/REPRODUCE.md
OID:    88a4e1d927be6960aa95cebe22112f5c09d6ebdb
```

The current checkout's `proofs/REPRODUCE.md` has the same 39,464-byte content identity and SHA-256. For a durable standalone execution receipt, preserve those exact bytes as the command's stdout artifact. The tool captured the complete stdout, although its displayed result was truncated because of output length. This report identifies the complete stream by its pinned source blob, size, and hash; it does not represent a displayed excerpt as the complete stream.

## 3. Shell syntax checks and unexecuted commands

All six `sh` fenced blocks were independently supplied to:

```json
["sh", "-n"]
```

Every syntax check returned exit code `0`, with empty stdout and stderr. These were parse-only checks: `sh -n` did not execute any block.

| Block | Guide command | Shell-block SHA-256 |
|---|---|---|
| 1 | Python source-map lookup | `e58229ed87379559f621aaa8d72ec36097697d6ad4e69fd508d102b5a980af1e` |
| 2 | `git cat-file -e ...` | `b0c5fadfffaae918b62826b465138ea5d03983680d63ad7b8f9e493a030790ac` |
| 3 | `git show ...` | `8d39f94890c896246023afaf9b9e322fc77b63d1f6b23e9598e4643da5b7b6ab` |
| 4 | Current release wrapper | `85a11c7bc58e50e62213977e690c96cd46b0add9d50845b820770340c6dfd17c` |
| 5 | Current project wrapper with illustrative Lean/output paths | `008d8b5f942e4ad8ed6dbb4400033e3a76c044bef2ae83957b4fe93c3f588dfb` |
| 6 | Replay wrapper with child `cd proofs` | `519dbd8634df0b5b0305b419373774969cdd295f3ebcbd43f6c2414eda2c2520` |

Blocks 4-6 remain **COMMAND_INSPECTED**, with shell syntax confirmed. They were **not executed**.

Source inspection confirms these guide statements about the replay wrapper:

- Selection is exactly `info.get('current') or info['preserved']`.
- A hash mismatch raises an error; it does not fall back from a non-null current selection to the preserved copy.
- The wrapper creates a temporary external shared Git clone.
- It sets the replay branch and index to the map's baseline.
- It iterates over every mapped path before starting the requested child.
- The child runs with the reconstructed repository root as `cwd`.
- The temporary workspace is retained.
- The wrapper exits using the child's returned status.
- The optional English presentation fields do not participate in selection.
- Both current entry-point wrappers forward their arguments to their historical checker paths through the replay wrapper.

## 4. Complete-tree checks

For link and object comparisons, the reviewer read both complete recursive Git trees with these exact metadata commands:

```json
["git", "ls-tree", "-r", "-z", "--full-tree", "ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3"]
["git", "ls-tree", "-r", "-z", "--full-tree", "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"]
```

The metadata queries ran with:

```text
GIT_NO_LAZY_FETCH=1
GIT_OPTIONAL_LOCKS=0
```

Both returned exit code `0` and empty stderr.

| Tree | Complete recursive entries | Raw NUL-delimited stdout bytes | stdout SHA-256 |
|---|---:|---:|---|
| Current snapshot | 19,225 | 3,451,946 | `34d7d7503fcf110bfb79ee702f6e8b83548893d0f9dbf2c07114dfac1af16741` |
| Baseline | 9,161 | 1,284,526 | `4adf1b7055ba528cde1a382930a47f2d48bb5a740f7d360df58763f3d262e4dc` |

The map contains **9,161 entries**. The equality of these counts is reported only as a count observation; this review did not compare every mapping entry with every baseline path.

## 5. Markdown link inventory

Final counts:

```text
Link usages:                         15
Unique destinations:                14
Relative link usages:               10
Unique relative destinations:        9
Pinned repository link usages:       5
Reference definitions:               6
Errors among existing destinations:   0
Allowlisted new destination:          1, used twice
```

The first inventory parser removed inline-code labels entirely and therefore omitted the commit link whose label is formatted as code. That parser defect was corrected by preserving label text while removing only backtick delimiters. **The counts above supersede the initial 14-usage/13-destination intermediate count.**

### Relative destinations

Each destination is resolved relative to `proofs/SOURCE_MAP_GUIDE.md`.

| Destination | Result |
|---|---|
| `SOURCE_MAP.json` | Present in the pinned snapshot tree |
| `replay_original_layout.py` | Present in the pinned snapshot tree |
| `README.md` | Present in the pinned snapshot tree |
| `STATUS.md` | Present in the pinned snapshot tree |
| `FINDINGS.md` | Present in the pinned snapshot tree |
| `REPORTS.md` | Present in the pinned snapshot tree |
| `REPRODUCE.md` | Present in the pinned snapshot tree |
| `RESULTS.md` | Present in the pinned snapshot tree |
| `contributions/agent-65/source-map-guide-20261016/VALIDATION.md` | Explicitly allowlisted new candidate; absent when checked; used twice |

### Pinned repository destinations

All five links use the exact source snapshot `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`.

| Link kind | Destination within the repository | Result |
|---|---|---|
| Commit | Source snapshot itself | Commit and complete tree available |
| Blob | `proofs/SOURCE_MAP.json` | Present |
| Blob | `proofs/replay_original_layout.py` | Present |
| Blob | `proofs/verify_release.py` | Present |
| Blob | `proofs/verify_project.py` | Present |

These are repository-object/path checks against the complete pinned tree. No live HTTP status check is claimed.

## 6. Seven relevant source-map entries

For all seven entries below:

- `mode` is `100644`.
- The map's recorded OID equals the baseline tree's OID for the original path.
- The selected source path in the current snapshot has that same OID and mode.

The three locally available selected files were also read and independently hashed. Four selected files were absent from the sparse checkout; their contents were not fetched or hash-checked by this reviewer.

| Original path | Selected source path | Git blob OID | Local selected-byte check |
|---|---|---|---|
| `proofs/README.md` | `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/README.md` | `f70a3c0b133c8b630a2ce9b93beeeb0b305de712` | Absent locally; tree identity confirmed |
| `proofs/FINDINGS.md` | `proofs/FINDINGS.md` | `ed5e20ae4b79fda696203bc031aa1bf93f52bc7c` | SHA-256 and Git blob identity match; 66,891 bytes |
| `proofs/REPORTS.md` | `proofs/REPORTS.md` | `3e13b819c649f2aee759ee2db9458c5dc4303759` | SHA-256 and Git blob identity match; 43,581 bytes |
| `proofs/REPRODUCE.md` | `proofs/REPRODUCE.md` | `88a4e1d927be6960aa95cebe22112f5c09d6ebdb` | SHA-256 and Git blob identity match; 39,464 bytes |
| `proofs/research/README.md` | `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/README.md` | `c747144bb37dfe0ec218f805a76a558b84ddd3a8` | Absent locally; tree identity confirmed |
| `proofs/verify_release.py` | `proofs/verify_release__e7d6c74ed54123df.py` | `28a44124dc15d53d1a3a493daad1459ba8e10a71` | Absent locally; tree identity confirmed |
| `proofs/verify_project.py` | `proofs/verify_project__214bf7673efe116b.py` | `21131b03dfa516eb19a0a7a4df4f2a41020d4db1` | Absent locally; tree identity confirmed |

Recorded source-map SHA-256 pins:

```text
proofs/README.md
0509ee4e0fa8cb7d37a58ac632f0bf5e553732915182cdd09dc7f9c2977e4448

proofs/FINDINGS.md
b20a40d1b948424cfc1b5e4fd466234ab54296df6ffa50752a6a8db91fbb4b09

proofs/REPORTS.md
9b4b37a2e0c375524093636edd531a62281257bc02d84a8ac52ace3c35e3f623

proofs/REPRODUCE.md
aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a

proofs/research/README.md
c64970d72372842eedecb7b3d35b9e7483905790fe7fe5fe1371e8ae1f196b27

proofs/verify_release.py
7761f1db1fc653f85d10ae0c0ff7d15ec4e70375ccebc4bb65dee59481d4e2b6

proofs/verify_project.py
c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a
```

The historical `proofs/README.md` entry has `current: null`. It additionally records:

```text
english_current: proofs/README__a9cde297f7bac39f.md
english_sha256:  e5e5e5c2f6c7a348794e6524b5fb343ccac6eb97136bacedda0e085385d4c39d
```

Those fields are presentation metadata, not the replay selection.

## 7. Inspected source pins

All four current source files below were read locally. Their independently calculated Git blob IDs match their paths in the pinned snapshot tree.

| Current source | Snapshot blob OID | SHA-256 |
|---|---|---|
| `proofs/SOURCE_MAP.json` | `e5f8d27bf09f50f8b9756bf91dff02e992aa4a32` | `f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba` |
| `proofs/replay_original_layout.py` | `4745990a5477a4b6a5c537b368bf78d214ce2622` | `744180f651360c1df34d1fad465dc009a304abbafab5277ddfb163a738430c70` |
| `proofs/verify_release.py` | `3824235f83b037503a178e94b3d50a1a9300e14a` | `c77049937475e4783ce3e6c489fd95efab6dac0e78c3bd3cb9db760f19653629` |
| `proofs/verify_project.py` | `aefba7a0d80643342b0128f32a0cf038d9b12c96` | `e314b0656470773e81d14d04bbb548f914cd9e9808c89fdb07166d8ca58ef55b` |

The replay wrapper is 2,885 bytes. Each current entry-point wrapper is 174 bytes.

## 8. Operational limitations and publication handoff

Initial sandbox access probes did not expose the authorized `/dev/shm` checkout: the apparent working directory was `/root`, and an explicit `cd` failed. The first attempted `git status --short` therefore failed with "not a git repository" before any guide access. Subsequent explicitly approved read-only escalated commands reached the intended isolated checkout. Those initial failures are access-probe failures, not failures of guide commands.

The review made no network lookup, large-blob download, installation, reconstruction, release replay, mathematical-checker run, Lean compilation, GPU execution, or cleanup attempt. Four unavailable selected files remain a disclosed sparse-checkout limitation. Their pinned Git object identities were compared through the complete trees.

**No `LEAN_CHECKED` status is asserted.** No repository-wide preservation audit, full-map hash audit, full original-layout replay, or proof-status upgrade is asserted.

Before publication, retain this report, materialize the allowlisted `VALIDATION.md` target, and preserve the exact historical-document stdout using the source identity recorded in section 2.3. All findings above apply to guide SHA-256:

```text
1b66a639da024562d317f8f550e3c2c0250b412ea5f46c6678a6824b2387c101
```

## 9. Preservation-only continuation

Sections 1-8 preserve the complete substantive independent report issued before evidence files were requested. This continuation adds no new guide, wrapper, link, source-map, Git-tree, or mathematical test. The parent subsequently reported creation of `VALIDATION.md`; that later report does not replace the original observation that it was absent during link validation.

The evidence directory contains exact Python stdin and stdout reconstructed from the captured text and checked against their previously recorded hashes, explicit empty stream files, all six shell-block inputs, structured command receipts, source pins, seven-entry comparisons, the corrected link inventory, the superseded initial parser inventory, and original sandbox access failures. The JSON receipts are newly assembled preservation records of actual observations, not an assertion that an original complete runner JSON file survived. No original complete runner/control JSON file was retained.

`git-show.stdout.reconstructed.md` contains the exact 39,464 retained source bytes identified in section 2.3. It was recovered from the already available `proofs/REPRODUCE.md`, with length and SHA-256 checked against the earlier recorded output identity. It is explicitly a reconstructed stdout artifact, not a newly executed Git command or an original untruncated capture file.

The reconstructed stdout is **raw historical evidence**. Its relative links, historical commands, and original workspace paths retain the source document's original context and must not be treated as editorial navigation from this evidence directory. Similarly, absolute workspace paths in `receipts.json` and `access-probes.json` are raw execution provenance, not navigation links. Editorial source references in this report use repository paths and exact commit identities.

`ARTIFACTS.partial.json` records the first preservation batch only. `ARTIFACTS.json` inventories the completed evidence files with byte sizes and SHA-256 hashes; it excludes itself to avoid a circular self-hash. Neither file is a repository source or proof inventory.
