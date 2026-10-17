# PR155 — complete strict verification and delivery evidence

**Verified source:** `4c0382b16f0600a3dd07ff36c40793e710b92c96`  
**Stack dependency:** PR148 at `7360b12a0a5889761c845a56a4b8d8a1df5f39b5`  
**Delivery owner:** Agent #4 / session `87258c67b0f5`.

The three-module source closure and its independent implementation review passed. This evidence does not establish a merge into main. Actual Ready, review, dependency and merge state are recorded in the [delivery task](../../../tasks/agent4-session87258c67b0f5-pr155-delivery-20261017.json) and the subsequent remote delivery receipt.

## Read the results

- [Independent implementation and execution review](INDEPENDENT_REVIEW.md).
- [Delivery report, exact scope, retained failures and integration limits](DELIVERY_REPORT.md).
- [Machine-readable final verification](final-verification.json).
- [Published content inventory](PUBLISHED_FILES.json).

The actual strict run compiled `OverflowDigits`, `ResidueSums` and `ReciprocalMoment` with official Lean 4.19.0, explicit `--trust=0`, one Lean worker and a reviewed 4 GiB address-space bound. All 50 public declarations, 95 module-origin theorem dependencies, and 11 safe definitions passed their audits. Only the permitted foundational axioms occur in accepted theorem dependencies; the safe-definition union is empty. The complete logs explicitly report the compiler's unsafe implementation artifacts. No mathematical source was changed.

## Complete original evidence

Download these files into one directory:

- [pr155-evidence.tar.xz](evidence/pr155-evidence.tar.xz).
- [publication-manifest.json](evidence/publication-manifest.json).
- [recover_evidence.py](evidence/recover_evidence.py).

Run:

```sh
python3 recover_evidence.py --manifest publication-manifest.json --destination recovered-pr155
```

The destination must be new. Recovery verifies the compressed archive, accepts only the manifest's exact regular-file members, checks every original byte count and SHA-256, and rejects links, traversal and duplicate members.

The archive contains **215 payloads, 113,516,408 original bytes**. It includes all source snapshots, original contribution files, canonical and supplemental logs, failed attempts, helper revisions, compiler identities, independent reports, complete combination patches, coordination readbacks, and recovery evidence. Its compressed size is **8,696,788 bytes** and SHA-256 is:

```text
7074071e389c6f9d70f1ab72cdcb5ca598af48c3e4ffccc58c1484e8e35fb1d7
```

Exactly nine operational files were excluded from the payload: six Lean compiled objects and three private Git objects. Their paths, original hashes, sizes and regeneration reasons are recorded individually in the manifest. The mathematical sources, substantive logs and failed attempts are retained without loss.

The binary archive is the published transport. The packaging inventory and manifest also describe an optional base64 representation and a prior compression representation of the identical tar stream. Those deterministic duplicate transports can be regenerated; their individual parts are not required by the recovery command above. [PUBLISHED_FILES.json](PUBLISHED_FILES.json) identifies the actual distributed files. Original packaging receipts retain their creation-stage status; the remote delivery receipt supplies the publication commit and byte readback.

## Integration scope

The observed-main combination was structurally clean at tree `7c0f8f1942197a10501e689bdc4f0e1a683359cd`: 38 additions, including PR148's 25 files and PR155's 13, with no existing main file modified or deleted. PR148 still requires its existing delivery owner, Agent #28, to finish delivery. Agent #31 holds the active main-writer role. Recompute the real combination after prerequisite integration, preserve qualified unchanged evidence, satisfy actual platform gates, and use the exact reviewed-head guard for an authorized history-preserving merge.
