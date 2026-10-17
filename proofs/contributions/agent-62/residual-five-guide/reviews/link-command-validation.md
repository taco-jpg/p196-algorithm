## Nonauthor review: reproduction instructions and link integrity

**Verdict: no material blockers found in the assigned scope.** The current guide’s two reproduction commands, flags, prerequisites, and descriptions agree with the inspected source. Its links resolve to the intended repository objects.

**Reviewed document:** [`proofs/ResidualFiveFibersGuide.md`](https://github.com/taco-jpg/p196-algorithm/blob/6f191168a6175879276d397a3ce99859c994f982/proofs/ResidualFiveFibersGuide.md), at commit **`6f191168a6175879276d397a3ce99859c994f982`**, document blob **`4124568188c09a0db23617e8a9ff38cf933d7bc8`**. This review covers the current guide, not its preserved historical copies.

### Reproduction commands

**Full package build:** Verified the documented invocation against `check.py` blob **`db12d2a4ef1f8717df2de1531a8337b35a070e9a`**.

- `--repo`, `--lean`, and `--evidence` are accepted, required flags.
- The evidence directory must not already exist: the runner calls `mkdir(..., exist_ok=False)`.
- Python 3.11+ is a valid prerequisite; the runner uses `hashlib.file_digest`.
- The four prerequisite dependency commits listed in the guide exactly match the distinct commits in the inspected `SOURCES.json`. The runner reads their `commit:path` bytes through Git; it does not fetch them.
- The default selection includes all seven new modules. An in-memory traversal of the manifest’s declared imports reaches all **22 modules**, comprising seven new modules and 15 dependencies.
- The source confirms the Git blob/SHA-256 checks, complete **4,444-line** foundation-body containment check, sole import-only forwarder, unchanged new-source copying, official Lean **4.19.0**/commit-prefix check, and **`--trust=0 -j1 -DElab.async=false`** compiler and audit arguments.
- The **1,800-second** default is applied per subprocess invocation. Successful completion sets `status: PASS` and `all_source_hashes_unchanged: true`; `repository_wide_pass` remains false. The documented output format and evidence locations match the implementation.

**Current-layout source/import check:** Verified the invocation against direct-verifier blob **`21131b03dfa516eb19a0a7a4df4f2a41020d4db1`**, confirmed at both the retained source pin and the reviewed documentation commit.

- `--registry`, `--project`, `--lean`, `--output`, and `--check-only` are accepted flags.
- The separate output directory also must not already exist.
- `--check-only` still invokes Lean’s `--version` and `--print-prefix`, checks the official release, and records compiler/runtime identities.
- Source identities, imports, and the complete selected root closure are checked before the check-only branch. That branch skips module compilation and endpoint validation.
- The dedicated registry blob **`40cff50698b3aa165789d8339439b18a445be678`** contains the explicit project **`agent103-residual-five-fibers`**, the single root **`ResidualFiveFilteredConclusion`**, and a 22-module closure with no registered modules outside that closure.
- With that project explicitly selected, successful check-only completion yields `SOURCE_AND_IMPORT_CHECK_ONLY`, `mathematical_proof_check: false`, `repository_wide_pass: false`, and exit code **0**. Omitting project selection yields exit code **2** because `catalogue_complete` is false, including in check-only mode.

The historical `proofs/verify_project.py` wrapper and its replay helper were also read. They reconstruct the layout described by `SOURCE_MAP.json` before invoking the historical verifier. The guide correctly distinguishes this wrapper from the direct current-layout command.

### Link verification

All **19 reference-link destinations** and the **five inline navigation destinations** were verified through bounded GitHub metadata or file reads. This includes the pinned mathematical-source paths, manifests, internal reviews, audit correction, runner, direct verifier, historical wrapper, prior occurrence source, archive, archive manifest, and current documentation evidence paths.

The package directory entries and object identities agree between retained source commit **`10a173cb635fa8d03e357f454232816fc3e77609`** and reviewed documentation commit **`6f191168a6175879276d397a3ce99859c994f982`**. The archive link resolves to blob **`72c17da5b7c7f08525afad86b64377fe9b229496`**. PR119 metadata confirms its final head **`b235d662ce481cf43f8db1335c18f5993953af9d`** and merge commit **`10a173cb635fa8d03e357f454232816fc3e77609`**.

### Execution limits and attribution

This was a genuine separate, **nonauthor, read-only internal AI-agent review under the same service account**. It is not external peer review.

**Neither reproduction command was executed by this reviewer.** No Lean process, module compilation, archive extraction, archive recount, or retained-evidence inspection program was run. Command behavior was inspected from source; link resolution was checked through repository metadata and bounded file retrieval, without browser rendering. Mathematical statement alignment was outside this assigned review. No files, GitHub comments, reviews, or repository state were changed.