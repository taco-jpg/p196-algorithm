# Agent18 PR134 delivery review and preserved independent evidence

Reviewed mathematical head: `ec7aa17a36548cc629d2a4a309e802406fc862e7`.
Mathematical checkpoint: `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`.
Delivery owner: Agent #18/session1a324de41cc8. Original authorship: Agent #105/session9df76b.

Source review and retained evidence reuse passed. No source repair or new Lean run was needed. Actual integration is a separate remaining operation; consult the current task and any later PREMERGE/POSTMERGE records.

## Multiple-merge-base correction

MERGE_BASE_ERRATUM.md corrects the earlier conflict interpretation. PR113 has two incomparable merge bases; the three Agent5 documents are unchanged inherited content on the PR side and updated only on main. Agent12's actual ordinary merge-tree preserves main automatically. No manual source repair or duplicate build is needed. All earlier path/blob observations and the83-addition PR134 manifest remain preserved.

## Complete review records

- SOURCE_REVIEW.md: complete new source semantics, original decimal bridges, guards, both center parities, controls and limits.
- EVIDENCE_REUSE.md: complete83-file/77-ancillary assessment, existing strict12-module verification, full1096-theorem maps,206 safe definitions, failed attempts and reviewer attribution.
- TREE_PREPARATION.json: complete83-file manifest, exact sibling-PR113 evidence that must remain, historical Agent5 content differences (corrected by MERGE_BASE_ERRATUM.md), and current-target preconditions.
- DELIVERY_REVIEW.json: parent script assessment, policy/platform observations and truthful status.
- AGENT11_EVIDENCE.tar.gz, AGENT11_EVIDENCE_MANIFEST.json and AGENT11_ARCHIVE.json: preserved original independent review corpus described below.

All documents use English as required for durable technical deliverables; issue61 coordination and user conversation use Spanish.

## Existing independent Agent11 execution preserved without rerunning it

The historical independent reviewer is Agent #11 /root/review83, who authored none of the reviewed sources. The retained completed receipt is dated2026-10-16T22:52:09.812743+00:00. Agent18 independently checked the actual source pins, command/log hashes, raw audit maps and complete source/evidence scope, and now preserves the accessible originals without changing their bytes.

The archive contains50 original content files (798427 bytes) plus its packaging manifest:51 members,822599 uncompressed bytes. All51 were reopened in memory and compared byte for byte after compression.

```text
Archive bytes: 131143
Archive SHA256: baaf13d357e03584f4ae81ff1e60593f6b7939c32e2d6a0f226a0328eb6e9492
Archive Git blob: 73130946d5a0e026d0d2c95b8cb17ea1cc4a878e
Internal manifest SHA256: f2955a50dc7c28fc5951a0848aa3a656f4f40e144734e5f17669edab6c2e32d1
Original independent receipt SHA256: 43271fe3dd445fe5303aa71b1cca001eb9c94a3458720f36a751aca37570c679
```

Included: original review receipt and14 referenced files, all fresh nonobject snapshots/logs/manifests, full expanded audit, literal public audit, mapped/original registries, setup provenance, original narrative draft, validation helper and unchanged full-closure verifier. The narrative remains explicitly a draft; preserving it does not claim that it was submitted on GitHub.

Twelve reproducible oleans are omitted with their original sizes/hashes and reasons in the packaging manifest. The original FILES.json is unchanged and still lists them. Runtime binaries are not copied; original compiler/library identity records remain.

The separately recovered71-file original scope105 corpus is already published at the reviewed head:
`proofs/contributions/agent-105/numeric-decoder-9df76b-20261016/verification-evidence.tar.gz`,
SHA256 `068b07e5af5aabd6390d9e8636ce8f1efecef450bbeec04af4dfd2782aed23d9`,
Git blob `6edcaec03b229e117613d57df9ad22f4c43e97b3`.
No unique recovered file is omitted. The checkout is reproducible from the frozen Git history; duplicate checkout files and operational publication helpers are excluded rather than relabeled as mathematical evidence.

## Recovery and integrity

From a checkout containing this coordination record, obtain the archive and manifest at these exact repository paths. Validate the archive SHA256 before extraction. Create a new extraction directory, then extract only this validated archive; all members were checked to be regular0644 files with unique relative paths, no traversal/symlinks, and zero uid/gid/mtime.

For independent in-memory validation, use ordinary Python3 (without optimization):

```python
import hashlib, json, pathlib, tarfile
archive = pathlib.Path("AGENT11_EVIDENCE.tar.gz")
assert hashlib.sha256(archive.read_bytes()).hexdigest() == "baaf13d357e03584f4ae81ff1e60593f6b7939c32e2d6a0f226a0328eb6e9492"
with tarfile.open(archive, "r:gz") as tf:
    members = tf.getmembers()
    assert len(members) == 51
    assert len({m.name for m in members}) == 51
    for m in members:
        assert m.isfile() and not m.name.startswith("/")
        assert ".." not in pathlib.PurePosixPath(m.name).parts
    raw = tf.extractfile("PACKAGING_MANIFEST.json").read()
    assert hashlib.sha256(raw).hexdigest() == "f2955a50dc7c28fc5951a0848aa3a656f4f40e144734e5f17669edab6c2e32d1"
    manifest = json.loads(raw)
    assert {m.name for m in members} == set(manifest["members"]) | {"PACKAGING_MANIFEST.json"}
    for name, record in manifest["members"].items():
        data = tf.extractfile(name).read()
        assert len(data) == record["bytes"]
        assert hashlib.sha256(data).hexdigest() == record["sha256"]
        assert hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == record["git_blob"]
print("PASS: all preserved content bytes match")
```

The parent executed its own equivalent full-member checks while constructing the archive; this printed example is a recovery recipe, not a claim of another executed validation.

Historical final_checks.py is not a self-contained replay driver for this compact archive. It expects original sibling Git repositories, recovered scope105 evidence, original layout and the omitted compiled objects. It uses Python assertions and writes evidence-validation.json if executed. Preserve it unchanged without rerunning it during recovery.

The original fresh compiler run used the included unchanged verify_closure.py with the exact mapped registry and an initially empty build directory. Those recorded source compilations explicitly used --trust=0 -j1 -DElab.async=false; subsequent audits inspect the freshly produced closure. Their old absolute paths and timestamps are preserved rather than rewritten into invented new receipts.

## Acceptance and remaining delivery

The accepted result is a fixed-source-width coefficient decoder for a supplied canonical ordinary target, equivalent to existence of a positive canonical predecessor under the original step. It does not enumerate all predecessor integers or resolve196.

The genuine existing strict executions and source review can be reused only if the selected12-module closure and relevant configuration retain their exact bytes. Current-main preservation, actual prerequisite113 integration, platform enforcement, the serialized write slot and merge/readback remain the delivery owner's obligations. No evidence report itself constitutes delivery.
