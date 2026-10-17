# Runtime evidence for Agent #20 PR #153 verification

## Scope and status

This package preserves the acquisition and recovery evidence for the external Mathlib runtime used by the separately executed PR #153 verifier. Mathlib is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b` with the eight dependency revisions recorded in the original manifest. The runtime recovery status is `PINNED_LIBRARY_CACHE_CLOSURE_PRESENT_NOT_PROJECT_VERIFIED`.

The package does not establish a successful PR theorem build. The separately retained fresh verifier results establish their own exact source, scope, commands, and outcomes. No Lean execution, network request, remote write, source edit, or runtime mutation was performed during this publication assembly.

## Evidence contents

The `runtime` subtree preserves byte-identical copies of the current acquisition receipt, every preserved clarification variant, the complete substantive recovery directory, the original workflow source, and all eight files in the workflow's `library-audit` directory. The original checksum file is also included. `COPY_MAP.json` identifies every original path and its copied byte identity. Historical absolute paths and commands remain unchanged as evidence; scripts should be reviewed and given an isolated owned destination before any later execution.

The recovery evidence includes the 76 missing source-hash cache keys, the full 1,362-module required cache-key inventory, the operational `CacheNeeded.lean` program and execution receipt, both download scripts, every completed failed DNS attempt record, the first-attempt terminal summary, all successful retry records, leantar help/version output, safe archive extraction and unpack receipts, promotion preflight, producer comments, and the complete staged/installed artifact inventories.

## Recovery outcome

All 76 canonical cache downloads returned HTTP 200 on the successful attempt. Sequential decompression produced exactly 532 expected build artifacts, totaling 47,615,327 bytes. All were installed with exclusive creation; no existing artifact was overwritten. Every one of the 1,362 required external library objects was then present and individually hashed.

Before and after recovery, all 7,265 source files matched the retained source inventory. All eight dependency commit records matched the manifest, and all 29 protected manifest, toolchain, and configuration files remained unchanged. These are source and infrastructure identity checks; the external Mathlib library was not rebuilt.

The first attempt omitted platform proxy configuration and failed DNS resolution. Its individual records are preserved. The successful retry retained only the existing proxy/certificate settings in addition to a minimal process environment. Queued first-attempt operations subsequently stopped at the no-overwrite assertion when successful destinations already existed; no successful artifact was overwritten. See `runtime/cache-recovery/downloads-attempt-1-summary.json`.

## Provenance boundaries and receipt clarification

Use `runtime/mathlib-acquisition.json` as the current clarified receipt. Earlier variants are historical records and remain unchanged. Their phrase “signed-artifact manifest” was corrected: the nested tarball matched its supplied SHA-256 checksum and the outer ZIP matched the GitHub artifact API digest; no detached artifact signature was validated. The official workflow source is pinned by the receipt's workflow source commit and is included as `runtime/agent13-real-library.workflow.yml`.

The leantar release is exactly 0.1.15, official release ID 208746645 and asset ID 241338509. Its observed archive SHA-256 is `87ea796fb4a6cc9a7b7548b392ba19e7da509324ecced9579692fe299d1516df`; its executable SHA-256 is `c3294bf820d5d1d7cc59bc3ce9bdc244b3f45cab37ea9dd649e1a388c20dbe3c`. No independently published upstream digest was supplied for this release asset.

The cache filenames match the exact source/dependency hashes computed by the pinned canonical cache hashing implementation. Producer comments name the requested Mathlib commit for 68 archives and `05b58472fbb0a1a8a1b3e52bd0228e50afdcccb4` for eight archives. Producer comments are retained as written; this package does not claim that every object was created at the requested source commit. See `runtime/cache-recovery/cache-comments-summary.json`.

## Excluded reproducible infrastructure

`EXCLUDED_RUNTIME_INFRASTRUCTURE.json` records the exact reasons, archive identities, release/artifact IDs, and inventory references for omitted third-party compiler distributions, Mathlib source and compiled trees, `.ltar` files, leantar, and duplicate staged artifacts. Those payloads remain preserved in their original locations. They are not deleted, replaced, or reclassified as project proof evidence. The source inventory, all required object hashes, and the complete recovery supplement manifests are included here.

## Integrity and publication screening

`FILES.json` inventories every payload file by path, size, and SHA-256, excluding only itself and `MANIFEST.sha256` to avoid self-reference. `MANIFEST.sha256` covers every other file, including `FILES.json`; its own hash is delivered separately to the coordinator. Run `sha256sum -c MANIFEST.sha256` from the package root to verify its contents.

`PUBLICATION_SCAN.json` records local checks for private key material, common credential formats, authenticated URL user information, signed URL query parameters, and temporary release-asset URLs. Only filenames, categories, counts, and outcomes are recorded; matched values would never be printed. Pattern screening is a bounded check, not a claim that arbitrary secrets are mathematically impossible. All copied inputs were screened before copying, and the assembled payload was screened again.
