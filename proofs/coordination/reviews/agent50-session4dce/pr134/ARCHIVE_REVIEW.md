# PR134 retained verification archive — independent supplemental check

**Result: PASS_RETAINED_EVIDENCE_BYTES_AND_AUDIT_COVERAGE.**

Reviewer: Agent #50/session4dce66859b6c. Delivery owner remains **Agent #18/session1a324de41cc8**. This bounded supplemental task makes no ownership claim or integration decision.

## Source and archive identity

- PR: https://github.com/taco-jpg/p196-algorithm/pull/134
- Reviewed head H: `ec7aa17a36548cc629d2a4a309e802406fc862e7`.
- Recorded verification checkpoint: `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`.
- All 12 registered source modules are byte-identical across the independently fetched H files, canonical snapshots, and strict snapshots. Their SHA256 and Git-blob pins agree with the registry, original evidence manifest, and final receipt.
- The registry fetched at H is byte-identical to the archived replay registry; SHA256 `10aa02456c15914a8dd00a1b3bf639a7e9f129262c54ef7bd894ec635eec9f52`.

The [published manifest at H](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/VERIFICATION_ARCHIVE.json) and [archive at H](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/verification-evidence.tar.gz) were fetched through the supported connector; the archive required base64 encoding.

| Check | Independently verified result |
| --- | --- |
| Compressed bytes | 174,360 |
| Compressed SHA256 | `068b07e5af5aabd6390d9e8636ce8f1efecef450bbeec04af4dfd2782aed23d9` |
| Git blob | `6edcaec03b229e117613d57df9ad22f4c43e97b3` |
| Full member set | Exactly 71 regular files; no additions, omissions, duplicates, links, or unsafe relative paths |
| Uncompressed bytes | 929,758; each member's size and SHA256 matched |
| Original evidence manifest | All 70 entries, plus the manifest itself |
| Per-run FILES indexes | Canonical 27 entries and strict 29 entries; exact sets, sizes, and hashes |
| Direct review copies | All four byte-identical to their archived originals |
| Headers | File mode 0644; uid/gid/mtime zero; gzip mtime zero and filename header absent |

All original archive members remain retained byte for byte. Gzip decompression was bounded to 2 MiB, and tar members were read as data without using extraction commands or executing their contents.

## Actual commands and completion evidence

The canonical receipt records **12 source compilations and one ProjectAudit run**. The strict receipt records **the same 12 source compilations and audit, plus one help command**. Every recorded command has the exact expected argument list, exit code zero, and an existing complete log whose hash matches its receipt. Canonical and strict driver logs separately enumerate all 13 and 14 command exits in the same order. Both driver receipts report completion and zero exit.

The recorded canonical run spans 22:05:39–22:07:21 UTC; the strict run spans 22:08:00–22:09:36 UTC on 2026-10-16. Their timestamps and elapsed durations agree, and the two recorded runs are sequential. All corresponding source compilation logs and the complete audit logs are byte-identical.

No error, sorry, custom-axiom, or disallowed-axiom failure diagnostic appears in those logs. Both runs retain the same pre-existing simp/simpa linter warning in Agent101MultiplicityBounds. An empty Agent101SplitEnumeration log is preserved with the correct empty-file hash and explicit zero exit.

The [canonical verifier source at H](https://github.com/taco-jpg/p196-algorithm/blob/ec7aa17a36548cc629d2a4a309e802406fc862e7/proofs/verify_project__214bf7673efe116b.py) was read in full, hashed, and compared with the receipt pin: `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. The archived strict helper was also read in full and matched `5836600e3e5a70bc891e1c3e393c4314eb27d08a0e5674a11819c94b5b7c7e6f`. Both create new source directories and issue explicit source compilation commands with a local source search path. They were inspected as text only.

## Complete theorem and axiom coverage

The generated ProjectAudit.lean is identical in both runs, with SHA256 `2b09bd716fc3964f4e33988c3b0acef3842479e1f7b190ce4feb1850ece8d56b`. It exactly matches the inspected full module-origin audit program:

1. Import both registry roots and check all 29 public endpoint types.
2. Select the full 12-module build order.
3. Iterate environment constants by originating module.
4. For every selected theorem declaration, call Lean.collectAxioms and reject any dependency outside propext, Classical.choice, and Quot.sound.
5. Reject safe custom axioms and separately record unsafe implementation declarations.

The independent checker parsed **full multiline dependency lists**, accounted for every theorem-record occurrence, enforced unique theorem names, reconstructed both complete maps, and compared them. Each map has exactly **1,096 theorem constants**, including all 29 public endpoints. The recomputed union is **Classical.choice, Quot.sound, propext**, with **zero forbidden theorem dependencies**.

| Module | Audited theorem constants |
| --- | ---: |
| Lychrel196Research | 787 |
| Agent101DigitPairs | 27 |
| Agent101MultiplicityBounds | 28 |
| Agent101SplitEnumeration | 58 |
| Agent101NumericFibers | 56 |
| Agent105WidthSupport9df76b | 8 |
| Agent105DecoderTarget9df76b | 7 |
| Agent105DecoderLocal9df76b | 27 |
| Agent105DecoderScan9df76b | 66 |
| Agent105NumericDecoder9df76b | 6 |
| Agent105CrossWidthWitness9df76b | 20 |
| Agent105DecoderControls9df76b | 6 |
| **Total** | **1,096** |

The five new decoder modules account for **112** audited theorem constants. An additional 215 direct #print axioms records were parsed and checked; 207 name theorems in the full map and agree with it.

Both audit logs contain the same **22 unsafe implementation declarations** from existing foundation/Agent101 modules. None belongs to a new decoder module, and none appears in any audited theorem dependency set. The complete list is retained in unsafe-implementation-declarations.json.

## Scope, limitations, and delivery

This result validates retained evidence bytes, source identity at H, actual recorded command/log consistency, and intended and completed audit coverage. **No Lean compiler or repository code was executed by this supplemental check.**

Compiler version and five recorded binary digests agree across the receipts; this checker did not independently rehash the runtime binaries. The `--trust=0` option and archived help wording alone are **not** treated as evidence that imported proofs were rechecked. The retained fresh-source commands and actual transitive axiom audit support the reused result.

This result concerns the exact scoped contribution. It does not assert a repository-wide build, enumerate historical attempts outside this archive, validate the current target combination, promote the PR, or merge it. Existing independent source review is not repeated here. The named delivery owner handles the remaining live integration actions and checks.

## Preserved checker execution and files

Two Python checker executions completed with exit zero:

- `inspect_archive_001.py`: complete structural and byte-identity check.
- `audit_evidence_002.py`: complete source-pin, manifest, command, and axiom-map check; **7,954 recorded conditions passed**.

One JavaScript serialization attempt failed **before any Python command ran** with `TypeError: String.raw(...) is not a function` at `exec_main.mjs:246:32`. Lean backtick notation conflicted with the JavaScript template literal. The exact failure and corrected serialization method are preserved in retrieval/orchestration-failure-001.json. The earlier parent-reported argument-list-too-long failure belongs to the parent's evidence and is not presented as one of these Python runs.

| Deliverable | Local path relative to this directory |
| --- | --- |
| Machine-readable conclusions and exact commands | results.json |
| Every check and outcome | checks.json |
| Full canonical theorem-to-axiom map | canonical-theorem-axiom-map.json |
| Full strict theorem-to-axiom map | strict-theorem-axiom-map.json |
| Per-member archive checks | archive-member-checks.json |
| Raw checker stdout, stderr, and exit receipts | checker-attempts/001-archive-structure/ and checker-attempts/002-full-evidence/ |
| Original fetched archive, manifest, and direct copies | inputs/ |
| Head-pinned source bytes | head-sources/ |
| Connector identities and serialization failure | retrieval/ |
| Every original archive member | retained/ |
| Full preservation inventory | preservation-index.json |

Evidence directory: `/dev/shm/p196-agent50-4dce66859b6c/pr134-archive`.
