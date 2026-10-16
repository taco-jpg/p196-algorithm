# Parent integration evidence: premerge checkpoint

## Result and boundary

**The specified parent evidence has been sealed as a premerge checkpoint.** This is an evidence preservation result, not a merge receipt or a new mathematical acceptance decision. No Lean process, project verifier, remote API call, source edit or external mutation was performed in this sealing task. Existing parent reports were copied without modification.

The snapshot began at `2026-10-16T23:31:51.862147+00:00` and finished copying at `2026-10-16T23:31:52.007969+00:00`. It retains **608 original files totaling 8,161,485 bytes**, together with preservation metadata and the complete losslessly restored initial PR #127 publication report. Every original copy was checked against its source bytes; a second hash pass found no changed or missing retained inputs. The frozen inventory and any later-created paths are recorded in `SNAPSHOT_BOUNDARY.json`. This local file snapshot does not assert an atomic remote GitHub state.

The parent remains responsible for actual reviews, final current-base checks, required platform gates, publication and merge. This package must not be cited as evidence that any merge occurred.

## Complete retained input scope

| Stored input group | Original files | Original bytes |
| --- | ---: | ---: |
| `memory/SCOPE.json` | 1 | 566 |
| `memory/check_selected_closure.py` | 1 | 2474 |
| `memory/integration` | 6 | 351046 |
| `memory/integration-git-setup.json` | 1 | 1974 |
| `memory/parent-evidence` | 3 | 75240 |
| `memory/publication` | 11 | 1150918 |
| `scratch/evidence` | 486 | 4933871 |
| `scratch/integration-tools` | 2 | 11608 |
| `scratch/ownership-scout` | 2 | 125738 |
| `scratch/review109` | 25 | 303048 |
| `scratch/review123` | 67 | 691322 |
| `scratch/runtime-scout` | 3 | 513680 |

`INPUT_SNAPSHOT_MANIFEST.json` provides every full original absolute path, full stored absolute path, archive member path, byte count and SHA-256. It also records each read completion time and original modification timestamp. `MANIFEST.json` covers every delivered package file other than itself; the outer archive receipt separately pins the manifest.

Original source snapshots, discovery/replay scripts, solver data, failed attempts, exact logs and intermediate reports remain intact. Ownership and runtime reconnaissance, received source identities, integration programs and combination/closure results are included. Inclusion of an author's historical report does not convert it into this agent's execution.

## Initial publication failures and corrections

The original `memory/publication/pr127-v1.json.xz` is retained byte-for-byte. Its complete decompressed report is also retained as `restored/publication/pr127-v1.json`: **717,043 bytes**, SHA-256 `d720702a091abac0c58101884261f776a9d086c75ecba6ad7ab2485c8cbeca1b`. The complete JSON parses and retains the original status `NEEDS_CLASSIFICATION_OR_REPAIR`. Neither failures nor fields were rewritten. Both publication program versions are preserved.

The existing reports retain these labels:

| Original report | PR | Preserved status |
| --- | ---: | --- |
| `pr110-initial.json` | 110 | `NEEDS_CLASSIFICATION_OR_REPAIR` |
| `pr110-final.json` | 110 | `PASS_CURRENT_PUBLICATION_WITH_VERIFIED_HISTORICAL_CHECKPOINTS` |
| `pr127-final.json` | 127 | `PASS` |
| `pr128-final.json` | 128 | `PASS` |

These labels describe retained parent reports; this task does not rerun their underlying checks. The PR #110 historical recovery receipt and all three recovered Git files are included. Every recovered file matches its recorded byte count, SHA-256 and Git blob identity. `PRESERVATION_CHECKS.json` gives the exact commits, paths and results. Both initial and corrected PR #110 reports remain available.

## Stopped review records and exclusions

PR #109 retains `STOPPED_DUPLICATE_COORDINATION`, zero Lean processes and `NOT_RUN` for required builds and audits. PR #123 retains `STOPPED_ON_PARENT_SCOPE_REASSIGNMENT`, zero compile attempts and the corresponding `NOT_RUN` results. Their acquired source material and acquisition evidence are included. Neither interrupted review is represented as accepted.

No user attachment, hidden configuration, Git metadata directory or alternate object store was read into this package. The recognized user-attachment copy `review123/evidence/ROLE_PROMPT.txt` was excluded without reading or hashing its contents. The two private Git directories were not traversed. `EXCLUSIONS.json` identifies every observed exclusion. All other substantive files in the specified inputs were retained.

The parent identifies the complete PR #131 supplement as already published at commit `1a8c4b93df46a8b6172cc1323004e0c2a17ad1db`; its separate archive is not duplicated. Existing references remain in the session records. This task did not query or republish that commit.

## Resource, preparation failure and recovery

The stored package is `/dev/shm/p196-agent13-session6124-20261016/parent-package`; its archive is `/dev/shm/p196-agent13-session6124-20261016/parent-integration-evidence-premerge.tar.xz`. The initial session memory directory held 143,303,025 logical file bytes; the added original snapshot was 8,161,485 bytes. The archive receipt records the final session total against the authorized 512 MiB output budget.

The original ENOSPC incident and recovery records remain included. A first attempt to prepare this packaging program failed to parse before executing because of nested quoting and a reused heredoc delimiter. Its actual diagnostic and execution boundary are retained in `PACKAGING_PREPARATION_FAILURE.json`; the failed request's complete text remains in its original tool transcript. No program source file existed from that failed preparation. The replacement executed program is retained as `SEAL_CHECKPOINT.py`.

No original source, failed record, log or research artifact was deleted. `RECOVER.md` explains extraction into a fresh directory and hash verification. Every archive member was separately decompressed and compared byte-for-byte with its staged original.
