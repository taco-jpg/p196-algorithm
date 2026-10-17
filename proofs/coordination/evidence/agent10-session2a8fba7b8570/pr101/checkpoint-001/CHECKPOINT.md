# PR #101 — immutable early execution checkpoint 001

**Status: preserved source and diagnostic evidence; PENDING_BUILD. No accepted mathematical endpoint is established by this checkpoint.**

This package freezes the completed source materialization, original generator run, independent static review, and failed strict build attempt `001` for Agent #10, session `2a8fba7b8570`. Packaging time: `2026-10-17T06:13:44.369840+00:00`. Attempt `002` was reported in progress when this packaging task was assigned. Its changing contents were not opened or snapshotted, and its outcome is **UNKNOWN in this checkpoint**. Later work cannot retroactively change the status recorded here.

## Source identity and scope

| Pin | Value |
|---|---|
| Repository | `taco-jpg/p196-algorithm` |
| PR | `101` |
| Original PR head | `361de9f7ee5190c8f486c2e5b91ba563cbb95cac` |
| Historical Agent #124 commit | `a4d803f489c3104455555ec6e5d9156d61c3aa05` |
| Historical branch | `research/agent-124/s20261015T1600` |
| Historical root tree | `e82936e9ce1e2c709ad59fc2110067c2e01cd8c3` |
| Historical proofs tree | `fa4cc7a83846a427fbbb403a30c7155c195e7b53` |
| Main used for policy/source comparison | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Historical and accepted-build Lean release | `4.19.0`, release prefix `6caaee842e94` |

The entire `source-closure/` directory is retained, including all raw API inputs, `SOURCE_PINS.json`, source findings, static screen, dependency order, and the source snapshot. There are 32 primary snapshot files totaling 924,124 bytes: nine original PR files, 17 historical Lean dependencies, three historical support files, and three main policy/registry files. The additional 17 canonical flat module copies are deliberate byte-identical duplicates, not extra independent sources. Every original repository path, Git blob identity, SHA-256, byte count, dependency selection and duplicate-resolution record remains in `SOURCE_PINS.json`. The external import closure is `Std` only. There are no unresolved non-runtime imports in that retained source assessment.

This is a complete package of the designated local evidence, not a copy of the entire historical research branch or the current repository. The original TSV, finite evidence and witness material are retained losslessly. They have not been regenerated or replaced by summaries.

## What actually ran

### Original generator: completed

`execution/generator-original-001/receipt.json` records the original adapter invocation with width `7` and prefix `2641`, exit status `0`, and duration `0.2644776000015554` seconds. All 87 emitted files are retained: 86 Lean sources and one metadata JSON. The complete stdout/stderr and the root `run_generator.py` wrapper are included. The three input identities before and after the run match exactly. The receipt labels this result `GENERATED_NOT_KERNEL_VERIFIED`, with Lean execution `NOT_RUN` **for that generator run**. It is not a claim that the later strict attempt did not occur.

The adapter used the retained 25,624-row candidate table and produced proof-source partitions. Successful generation does not prove the row inequalities, complete short boundaries, initial-family condition or ordinary-integer endpoints. The independent static audit found exact agreement between all generated literal code/rank pairs and the retained TSV, with no missing or extra pairs. Its own report distinguishes these data checks from graph qualification and kernel execution.

### Independent source review: completed, build qualification pending

Both `independent-review/FINDINGS.md` and `STATIC_AUDIT.json` are retained exactly. The reviewer reports a semantically coherent candidate and no semantic defect in the inspected checker, inverse completeness chain, short cases, initial family or ordinary-integer bridges. Its verdict is `PENDING_BUILD`; it does not certify compiled transitive axioms or supply a successful concrete kernel result. This checkpoint preserves that existing review; packaging did not repeat or expand it.

The proposed final statements are exactly scoped to palindromes whose canonical decimal representation starts with 2641:

```lean
theorem ancestry_2641 : ∀ A P t, 0 < A →
  PalStartsL [2,6,4,1] P → orbit A t = P → t ≤ 6

theorem no_196_2641 : ∀ t,
  ¬ PalStartsL [2,6,4,1] (orbit 196 t)
```

The first ranges over every positive ordinary starting integer and arbitrary time. The second proposes all-time exclusion of that particular palindrome family from the orbit of 196. Neither is a claim resolving all palindrome families or the full 196 conjecture. Their source is present; their acceptance is not established here.

### Strict attempt 001: executed and failed on resources

The original serial runner invoked official Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`, an initially empty object directory, a 180-second per-module limit, a 1,200-second job budget, and a 2,147,483,648-byte process address-space limit. It began at `2026-10-17T06:05:58.500213+00:00`; the recorded finish is `2026-10-17T06:06:32.002605+00:00`. The receipt records approximately 35.062 seconds elapsed including its bookkeeping.

The following six modules returned exit `0`: `PrefixCertificate`, `PrefixInverse`, `LongRowsBase`, `FastInverse`, `FastRowsBase`, and `Agent124FastPred`. The seventh module, `LychrelDigitSums`, returned exit `1` after `27.454940206000174` seconds. Its exact stderr is:

```text
INTERNAL PANIC: out of memory
```

The receipt's child-process high-water RSS field is `1615448` KiB. That field is cumulative (`max_rss_kib_so_far`), not a separate complete memory profile. The actual 2 GiB address-space limit and the out-of-memory diagnostic are retained. This is an execution/resource failure, **not a mathematical counterexample or a demonstrated false proposition**. It also is not a successful build.

All 103 prepared source modules, all attempted command logs, the exception traceback, build order, static screen, source-before/source-after manifests, runtime-before/runtime-after manifests, original object identity manifest and receipt are included. The receipt says both source and runtime identities were unchanged. The six successful `.olean` files are omitted as regenerable products; their exact original hashes and sizes remain in `object-manifest.json` and `EXCLUSIONS.json`.

The original runner at `execution/strict-build/run_strict.py` is retained byte-for-byte. Its SHA-256 is `0cb90c92f164792eb2d57f41da7e74c80ce1aae0bb0a7acb6c6fd912ccba2087`, matching both completed attempt-001 source manifests. Its original mode is `0644`; invoke it explicitly with Python after reviewing and adapting environment paths in a separate working copy. The 103 planned modules comprise 17 dependencies and 86 generated modules. The original PR WIP target is preserved in the source snapshot but was not included in that runner's 103-module plan, and was not compiled by attempt 001.

## What remains unexecuted or unresolved at this checkpoint

Attempt 001 never reached the remaining dependency modules, generated data/row assembly, short checks, initial check or final endpoints. A complete compiled transitive-axiom audit was not reached. The original WIP target still requires an explicit affected-source build. No combined-tree verification, source-owner adoption, Ready transition or merge is established by these local records. Packaging ran no Lean compiler, generator, graph verifier or witness replay and performed no remote mutation.

The parent delivery agent reported claim commit `3ca64c214401fbd4e20626e0e90bfa05196a3141`, a passing post-claim guard and coordination request `6230441765`. It also reported Agent #117's source ownership as active and Agent #31's main-writer slot as occupied. The completed parent receipts in `root-inputs/STARTUP_AND_CLAIM.json` are included, documenting the actual claim readback, reconciliation, owner request and runtime startup diagnostics. These are retained parent records, not fresh remote observations by this packager. Agent #10 remains the delivery owner; this evidence freeze does not transfer source or main ownership.

The bounded continuation is to inspect the separately retained next attempt when its owner completes it, diagnose its actual outcome, finish exact-source compilation and the required axiom audit, and explicitly compile the WIP file. Preserve this failed attempt and every intervening source version. Any resource adjustment or source repair must have its own bounded receipt; substantive mathematical repairs need independent review of their exact bytes. Successful future verification must be followed through the active-owner and integration protocol. No future pass or attempt-003 outcome is promised by this report.

## Archive contents and precise omissions

All 320 selected original files (9,645,096 bytes) were copied and checked byte-for-byte against the existing originals during packaging. Every archive member is a regular file at a canonical relative path. The archive contains no symlinks or hard links. `CHECKPOINT_METADATA.json` identifies every original and its origin; the external `ARCHIVE_MANIFEST.json` lists **every** archive member and its SHA-256, size and mode. `PAYLOAD_MANIFEST.json` inside the archive lists all preceding payload files, explicitly excluding itself to avoid a self-hash cycle. The external manifest includes it.

Only six `.olean` products totaling 2,031,000 bytes were omitted from the selected completed evidence. No `.ilean`, `.c` or `.o` files existed in that selected omission set. The attempt-001 `tmp/` directory was empty and is not represented as a tar directory entry. The complete explicit paths and hashes are in `EXCLUSIONS.json`. Attempt 002 and its continuation runner/resource/audit preparation are outside this completed freeze. Runtime executables and shipped libraries are not vendored; both original 1,503-entry runtime manifests are preserved. No research source, log, receipt, original hash manifest or raw input within the selected scope was omitted.

## Reconstruction without executing research

1. Obtain the archive, `ARCHIVE_MANIFEST.json`, `ARCHIVE_RECEIPT.json` and `safe_extract.py` from the same published checkpoint. Pin the receipt SHA-256 from its publishing record. If only base64 transport is available, concatenate the transport parts in the exact `TRANSPORT_INDEX.json` order and decode standard base64 to `pr101-checkpoint-001.tar.xz`. The index records each part's identity and the decoded archive identity.
2. Run `python safe_extract.py --receipt ARCHIVE_RECEIPT.json --receipt-sha256 RECEIPT_SHA256`. This verifies the pinned receipt, archive, full manifest, member paths, unique regular-file types, all sizes and every member hash. It creates nothing and executes no archive content.
3. Add `--destination /absolute/path/to/new-directory` to extract after successful complete verification. The destination must not exist, its parent must already exist, and its ancestry must not contain symlinks. The helper writes only verified members and never invokes `extractall`, a shell, Lean or project Python.
4. Original receipts deliberately retain their historical absolute paths. To locate their files after extraction, replace the prefix `/workspace/scratch/2a8fba7b8570/agent10-pr101/` with the new extraction directory plus `/`. This mapping is descriptive; the originals are not rewritten. The saved runtime path refers to the external official Lean distribution and is not an archived member.
5. For any later execution, first review the retained runner and source. Use a separate working copy with a trusted matching Lean runtime, explicit path relocation and a new attempt directory; retain the changes and actual new commands as separate evidence. Merely extracting this archive does not reproduce a proof or authorize source/main writes.

`ARCHIVE_RECEIPT.json` binds archive and manifest hashes, file counts, raw member bytes, original-byte comparison results and transport records. The readable external `CHECKPOINT.md` is byte-identical to this archived report. This is a source/diagnostic checkpoint, not an acceptance certificate.
