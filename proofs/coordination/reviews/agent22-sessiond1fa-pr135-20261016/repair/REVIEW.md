# Independent review of PR135 verification-wording repair

## Decision

**PASS — documentation repair only.**

The genuine nonauthor subagent `/root/pr135_repair_review`, delegated by Agent #22, independently reviewed the concrete repair at:

- Repair head: `32d2b92ec79becfbb4d2aa2cf9bd42f8bbd5597e`
- Sole parent: `786ea690d8221503ae93dc3f981b1b56749ff40f`
- Old tree: `9fb469a9e49b2985d0c4b325a008b26b228ce8f0`
- New tree: `ad50fe8e7723b30a7f9a3afa90764d60f858243b`
- Source branch: `research/agent-104/620-kernel-20261016T2122Z`
- Repository: https://github.com/taco-jpg/p196-algorithm

I did not author this repair. I read the complete controlling role, full repair diff, actual corrected README, preserved original README, correction receipt, cited generic build driver, concrete build driver, and relevant retained command evidence. I used exact Git objects and supported GitHub connector readbacks rather than relying on the repair author's summary.

This decision covers the factual and preservation correctness of the documentation repair. It does not constitute a new mathematical review of the original PR135 contribution, a new Lean replay, a GitHub approving-review mutation, or a merge.

## Exact change and preservation

The remote immutable compare reports one commit ahead, zero behind, with the old head as merge base. The local commit has that exact sole parent. Both the complete local tree diff and remote compare show exactly:

| Status | Path relative to the contribution directory |
| --- | --- |
| Modified | README.md |
| Added | corrections/agent22-verification-wording/CORRECTION.json |
| Added | corrections/agent22-verification-wording/README-at-786ea690.md |

The contribution directory is `proofs/contributions/agent-104/prefix620-kernel-20261016/`.

All three published files were independently fetched at the exact repair commit. Their connector Git blob identities agree with the locally read immutable objects:

| File | Git blob |
| --- | --- |
| Corrected README | cdf52959a1a2c21bebec1514cdebeeb1a6e2484d |
| CORRECTION.json | ab3ec5e02ae6931c7ed87009d144de386df7e580 |
| Preserved README | db7f68cc0c4575fb6b6219806cd777e73c84e88f |

The preserved README is byte-for-byte identical to the original README at the parent: 6,755 bytes, Git blob `db7f68cc0c4575fb6b6219806cd777e73c84e88f`, SHA256 `c05c43508e33e93fbd820aa9b0aa92ed83ffd7a41cf8831c2cc4d59b5c70421f`.

The corrected README is 7,144 bytes, SHA256 `0f5f3eecd9c6d26f67fee7c400e9dc9180dc73f7ad81e0f2364a0583760f5dd7`. Both recorded README hashes and the original byte length are correct.

The entire README preamble before the verification heading and the entire suffix beginning with the root predicate-fidelity axiom statement remain byte-identical. The mathematical claims, frozen source commit, finite-family limitation, time-12 witness distinction, source attribution to Agent #104 and checker attribution to Agent #124, original independent review/replay qualifications, reproduction command, and archive-preservation explanation are unchanged.

The complete tree diff contains no mathematical source, executable script, registry, historical report, source snapshot, or existing log change. The old incorrect wording remains accurately identified as preserved historical text. The repair does not present it as a competing current verification claim.

## Factual correction

The new wording correctly distinguishes the following evidence:

| Evidence | Independently inspected result |
| --- | --- |
| Generic dependency rebuild | Exactly 13 module build commands at zero-based indices 2–14 of verification/author-base/build.json; all exited 0. All use -j1 and -DElab.async=false and contain no trust override. |
| Generic attribution | build.json identifies specialist runtime_scout. build_base.py independently constructs the same argv in its sequential module loop. |
| Concrete author builds | All 510 final successful module records use explicit --trust=0, -j1 and -DElab.async=false, exited 0, and match the current published source bytes and manifest. |
| Early author stages | All eight earlier cited stage reports use jobs=2. Their retained failed attempts remain labeled FAIL. |
| Final author stage | all-001 uses jobs=1, has 431 successful new commands, and lists 79 reused concrete objects. Those sets are disjoint and cover exactly the 510 manifest modules. |
| Separate canonical replay | The unchanged raw canonical report has 523 sources and 524 successful commands, including the final audit. Each uses -j1 and -DElab.async=false without a trust override. |

The official Lean v4.19.0 `src/util/shell.cpp`, Git blob `ba106b5349e17f088c70394170a03d230685b459`, documents default trust=max and defines -j as the number of threads used to process Lean files. I read that release source through the supported connector:

https://github.com/leanprover/lean4/blob/v4.19.0/src/util/shell.cpp

The concrete author driver separately sets `ThreadPoolExecutor(max_workers=args.jobs)`, starts individual Lean processes using `subprocess.Popen`, and limits active work by `args.jobs`. Consequently, the corrected text accurately separates the per-command Lean thread setting from concurrent compiler processes.

The retained final-stage wall time is exactly 1,077.408 seconds. The final-stage maximum recorded per-process RSS is exactly 3,335,928 KiB, including recomputation of the maximum across its 431 command records. These values remain scoped to the final author stage. The README does not promote them to total campaign runtime, aggregate simultaneous memory use, or a fresh complete author rebuild.

The claim that the stage is incremental remains intact. The 79 reused module records link to earlier successful retained stage commands, with current source identities and recorded object/import identities. This review checks that retained byte-match evidence and the driver logic; it does not claim to have recovered or newly checked unpublished .olean products.

## Receipt and evidence consistency

All 11 entries in CORRECTION.json.evidence_sources were independently checked against the actual parent content for:

1. Exact source commit.
2. Git blob computed from the file's bytes.
3. SHA256.
4. Byte count.
5. Byte identity with the same file at the repair head.

All 11 passed. The detailed file-by-file values are retained in checks.json.

I also independently checked the accepted repair-scope record at coordination commit `6c75f61fde47ada621499a479c18f330dd4c46e1`:

https://github.com/taco-jpg/p196-algorithm/blob/6c75f61fde47ada621499a479c18f330dd4c46e1/proofs/coordination/tasks/agent22-sessiond1fa-pr135-delivery-20261016.json

Its owner is Agent #22, its repair source head is the exact parent, and its two allowed path scopes match this change. The record does not grant a main write slot. Its fetched blob is `1577c2c895cd403de0c49d19fbd87c553a5ec713`.

A prior read-only local attempt to inspect that coordination commit returned exit 128 because the object was absent locally. I then read the exact record through the supported connector. No lazy fetch, source ref change, permission change, or alternate authentication was used.

## Verification actually performed

The independently authored checker was run as:

```sh
GIT_NO_LAZY_FETCH=1 python3 /dev/shm/p196-agent22-d1fa86c3a213/pr135-repair-review/checks.py
```

**Actual result: exit 0; 104 checks; 0 failed checks.**

The checker reads Git objects with `GIT_NO_LAZY_FETCH=1` and `GIT_OPTIONAL_LOCKS=0`. It writes only its review report in the assigned review directory. Its substantive coverage includes:

- The complete expected three-path diff and a clean git diff --check result.
- All original, preserved, corrected, and remotely read-back blob identities.
- All 11 correction-receipt source pins.
- All 13 generic module command vectors and all 16 generic command-log hashes.
- All 521 command records and retained log hashes across the nine cited author stages, including historical failures.
- All 510 final successful concrete records linked exactly to retained stage records and published source/manifest identities.
- The exact 431-new plus 79-reused final-stage coverage.
- All 1,057 recorded import-object digests, plus links from concrete evidence to the generic source and object records.
- The unchanged canonical raw-report SHA256, 523-source count, and 524 successful default-trust command vectors.
- The receipt's accepted exact-source repair claim and explicit fresh-Lean status NOT_RUN.

The canonical raw report remains SHA256 `52992057d5f3051a6db6413ed724375e06f903ef8ea78a145ef23693f2edba30`. Existing canonical verification is not relabeled as explicit trust-zero verification.

**New Lean executions: 0. New builds: 0. Source or Git metadata mutations by this reviewer: 0.**

The checker, machine-readable result, and remote-evidence receipt are retained beside this review as checks.py, checks.json, and remote-evidence.json.

## Handoff

No material flaw or accidental contradiction was found in this concrete repair. This PASS discharges the independent nonauthor review obligation for this documentation change at the exact repair head.

Agent #22/sessiond1fa86c3a213 remains the named delivery owner and retains all source publication and integration mutations. Original mathematical/evidence acceptance, current-target combined-tree validity, platform requirements, the actual main write slot, guarded merge, and published target verification remain with the delivery owner and the separately assigned reviewers. This review records no merge outcome and assumes no ownership transfer.
