# Independent review: A65-DOC-002 pinned mapping metadata audit

## Verdict and independence

**PASS for the stated pinned Git metadata scope.** No blocking correctness defect was found in the frozen author script, result, captured execution evidence, or final report. A separately implemented, bounded reviewer comparison independently confirmed the complete 9,161-entry mapping and the exact metadata input stream hashes. This verdict is not a mapped-source SHA-256 audit, original-layout replay, Lean result, mathematical approval, or integration event.

Reviewer role: distinct non-author reproduction-audit specialist. The command-validation specialist authored and ran the audited implementation. This reviewer neither edited nor executed/imported that implementation. The review began after the implementation was present, and final report review used the frozen hash supplied by the parent. The earlier reproduction-document scouting work is separate from authorship of this new audit.

Task claim: `69324983850c944f9246653a45a87f4af9333393` on `p196/coordination`. The first guide publication at `e6a1a883d3cb67a5b46ebddd88c612fcc0bf96cc` is context only. Both the author and reviewer checks remain pinned to:

- Migrated source snapshot: `ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`.
- Original-layout baseline: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Source-map Git blob: `e5f8d27bf09f50f8b9756bf91dff02e992aa4a32`.
- Source-map SHA-256: `f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba`.

No source revision was inferred from local HEAD. README/REPRODUCE and all prior evidence were outside this review's write scope. FIRST_PUBLICATION_RECEIPT.json was not read or audited; its filename appeared only in a directory listing.

## Frozen reviewed artifacts

The following files were read in full. Their observed sizes and hashes matched the frozen author inventory and the parent's handoff. AUDIT_ARTIFACTS.json lists eight members and excludes its own hash, for a nine-file author package. This review is separate.

| Path relative to mapping-audit/ | Bytes | SHA-256 |
|---|---:|---|
| audit_mapping_metadata.py | 19472 | 0e9f02c19160435fe9b4f449349b785cf5f9f2c835634a021456711abd41ff00 |
| preparation.json | 1228 | 75dce5b59b33077a3e53c660a28c814c805d7a891789583a574528e11a358c2b |
| execution-receipt.json | 1080 | 3f0eda8288d48f38d8f99bbe4407e21932612c45b6b0a4ff6b0e49242a8d194f |
| audit.stdout.txt | 1638 | cc73e9666f4892930ea812b6e5298ddaecc5c5df29e97a0560a9987c9468da2f |
| audit.stderr.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| run-001/result.json | 3191 | 17e519f8eb70e87ca111150930f9e76d80532e15b4f3d56fbecf1b8c6889abf8 |
| run-001/run-metadata.json | 7726 | 358c09a31c25caea486d0b69a4fb1efc45b39c7630a50e5e20022ed142401d95 |
| REPORT.md | 9955 | 888601a0cfcfd566ee76a113502e63aa047e415a7eb8e2a215a6543bcb7ae1f4 |
| AUDIT_ARTIFACTS.json | 2082 | 24d682857674add8a26ea474d894c6fa4f3f127c0a0b3fe82a022d1b66588464 |

References in this review identify these exact bytes. The author stdout, structured result, receipt and per-command metadata agree on the successful recorded execution. All nine Git input commands report exit zero and empty stderr. This reviewer inspected the receipts and streams; the reviewer did not witness or independently rerun the author's process. Its recorded execution is distinct from the independent metadata comparison below.

## Source review

### Enumeration and immutable inputs

The script fixes both commits and the expected source-map hash at lines 19–22. Lines 137–167 check the Git object format, resolve each explicit commit and tree, collect complete recursive NUL-delimited tree listings, read the map at its pinned commit/path, and verify the map's SHA-256 and recomputed Git blob identity. It does not select source input through HEAD or the working copy.

The tree parser checks the final NUL, every record, repeated paths, metadata shape, mode/type agreement, and OID syntax (lines 84–107). Lines 180–188 compare the complete map and baseline key sets in both directions, retain every difference, and report the counts. The loop at lines 205–288 visits every normalized map entry. No sample, fixed prefix, selected contribution directory, or truncating result limit replaces enumeration.

### Malformed input and duplicate keys

The object-pairs hook preserves duplicate JSON members for inspection before dictionary conversion. normalize_json records every duplicate at its JSON location; although the last value is retained for subsequent analysis, any duplicate leaves an issue and prevents PASS. The parser rejects nonstandard JSON constants. Invalid root/path-container types cause an execution error, not success.

Each entry is checked for required fields, entry type, canonical relative paths, current/preserved types, mode and OID syntax, SHA-256 syntax, optional English-field types and pairing. Unsafe original/selected paths and malformed fields are recorded before continuation. An invalid entry cannot disappear silently behind an overall PASS. Unknown fields are inventoried rather than treated as automatically invalid; the actual pinned map has none.

This was source inspection and an actual-input review, not an adversarial fixture suite or proof of total correctness on every possible malformed input. No synthetic duplicate, malformed path, symlink, gitlink, or execution-failure fixture was run.

### Effective selection and identity comparisons

The effective choice at lines 259–261 reproduces the wrapper's truthy-current/otherwise-preserved rule. For every original key, the script compares recorded mode/OID with baseline metadata, then selected snapshot metadata with recorded mode/OID, then complete selected metadata (including Git kind) with baseline metadata. Missing selected paths are retained as issues.

Missing required fields are already flagged even though the implementation uses get() when selecting. Non-string current values are separately rejected, so a falsey invalid current value cannot silently produce a valid PASS by falling back.

Selected-path sharing is explicitly recorded and evaluated through the per-original identities; it is not mistakenly rejected merely because it is many-to-one. The pinned map has no such collisions. Unselected preserved paths receive field/path-syntax checks only. REPORT.md lines 50 and 63 accurately limit unselected preserved and English presentation metadata; the report does not claim both alternatives or English presentation target contents were validated.

### Modes, symlinks and path semantics

The mode/type table distinguishes ordinary files, executables, symlink blobs and gitlink commits. Selected identities are compared without following a symlink or reading its target. The complete baseline and snapshot listings contain no symlinks or gitlinks, so this run does not exercise those branches or establish full wrapper behavior for such entries.

The path checks exclude absolute paths, empty components, dot/dot-dot components, .git components and NULs. They are a conservative metadata validation for the inspected Linux/Git paths, not a claim about every operating system's filesystem semantics. The audit does not inspect sparse working-tree files, filesystem symlink ancestry, checkout filters, or local materialization.

### Status and failure handling

Issues accumulated during valid-input processing select FAIL/exit 1; input or execution exceptions leave ERROR/exit 2. Successful status is assigned only after the complete comparison. The result contains the full issues and exceptional-case arrays. For recorded Git calls the script retains status, stderr and exact input stream identities/hashes; it does not emit huge per-entry success dumps.

The author execution's complete captured stdout/stderr are retained and agree with execution-receipt.json. The successful run does not establish that every possible output-directory or final-write failure would produce a complete receipt: output-directory creation precedes the catch block and final evidence writes occur after it. That general runner limitation did not occur in this run and is not represented as having been tested.

## Independently confirmed outcome

The reviewer performed one independent local metadata comparison using separate inline code, without importing or executing the author implementation. It used GIT_NO_LAZY_FETCH=1 and GIT_OPTIONAL_LOCKS=0, and also disabled replacement objects. The two complete recursive tree inputs and the sole source-map JSON blob were read locally; no mapped source blob was read or fetched.

| Independently checked quantity | Result |
|---|---:|
| Baseline keys and map keys | 9161 each, exact equality |
| Snapshot recursive entries | 19225 |
| Entries whose recorded mode/type/OID agree with baseline and effective selection | 9161 |
| Unique effective selected paths | 9161 |
| Selection from current | 2565 |
| Selection from preserved | 6596 |
| Map and baseline mode 100644 | 9152 |
| Map and baseline mode 100755 | 9 |
| Snapshot mode 100644 | 19210 |
| Snapshot mode 100755 | 15 |
| Duplicate JSON keys | 0 |
| Independent metadata mismatches | 0 |
| Mapped source blobs read | 0 |
| Independent process exit code | 0 |

The independent input streams matched the author's exact lengths and SHA-256 values:

- Snapshot listing: 3,451,946 bytes, SHA-256 34d7d7503fcf110bfb79ee702f6e8b83548893d0f9dbf2c07114dfac1af16741.
- Baseline listing: 1,284,526 bytes, SHA-256 4adf1b7055ba528cde1a382930a47f2d48bb5a740f7d360df58763f3d262e4dc.
- Source-map JSON: 4,396,780 bytes, SHA-256 f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba.

The result and author stdout also agree on status, issue counts/categories, all counts, scope and not-claimed fields. These are independent metadata/evidence-consistency confirmations, not new per-source hash measurements.

## Interpretation and remaining limits

REPORT.md accurately distinguishes Git metadata identity from direct source-byte auditing. Its claims about complete key coverage, effective selections, zero issues, modes and exceptional cases are supported by the source and retained run evidence, and by the reviewer's independent comparison.

Only SOURCE_MAP.json was directly byte-hashed as a source blob. Each mapped sha256 field was syntax-checked, not recomputed against source bytes. Equal Git object IDs are the asserted identity within the Git representation. This review does not validate both preservation alternatives, inspect all archived versions, prove source object availability in a sparse checkout, run replay_original_layout.py, re-execute the first guide's command tests, rebuild Lean, or approve a mathematical result. Metadata review status is separate from source publication and main-branch integration.

## Preparatory failure preservation

The initial frozen preparation.json and REPORT.md correctly disclosed that only an excerpt of a preparatory parse failure was retained at that checkpoint. This was a preservation concern, not a failed mapping audit or evidence that the metadata PASS was incorrect.

The author subsequently supplied two new artifacts without changing the frozen package:

| Additional artifact | Bytes | SHA-256 |
|---|---:|---|
| preparation-failure-original.json | 976 | 31e4bd1b543c1afb951080d8b514f9d80cd809e721dc43240b9d9b536e88cd17 |
| PRESERVATION_NOTE.md | 2372 | 7ec0322ce3fff976258751d08c203706497e2f6e6edb5054d805bef92040b604 |

Both additions were read in full. The decoded UTF-8 output string in the JSON is 842 bytes with SHA-256 bbe7aead41e917e167c269fa146453d7e2d159b258188edf49ec232c167796d9; this length and hash were independently checked during review finalization. It contains the complete supplied diagnostic line, caret indentation and SyntaxError text, plus the recorded chunk ID 1faac1, exit code 1, timing and token count.

The provenance that these values were recovered from the author's still-visible, untruncated original tool result is attributed to the author and parent. This reviewer did not have an independent view of that original conversation chunk and does not claim to have compared original transport bytes. The new serialization is accurately described as a preservation of structured field values and the combined output string, not an original JSON transport capture, invented stdout/stderr separation, or a rerun.

The additional preservation evidence addresses the previously identified incomplete-record concern at that disclosed provenance level. The old excerpt/report remain truthful frozen checkpoints. The parent should include both additions and this review in the final outer manifest; the frozen author inventory deliberately remains unchanged. No blocking metadata-review issue remains.

## Complete reviewer comparison command

The following independent inline command was actually executed once. It neither imports nor executes the author's audit implementation. Its only blob read is the local pinned source-map JSON. The exact compact result follows in full, including input stream hashes, empty mismatch arrays and all three Git subprocess statuses. The large immutable input streams themselves are pinned rather than copied into this review.

```sh
python3 - <<'AGENT65_INDEPENDENT_METADATA'
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib, json, os, subprocess

repo = Path('/dev/shm/p196-agent65-dbfcd4')
directory = repo / 'proofs/contributions/agent-65/source-map-guide-20261016/mapping-audit'
snapshot = 'ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3'
baseline = '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5'
env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1', LC_ALL='C', LANG='C')
commands, mismatches, duplicates = [], [], []
def run(*args):
    command = ['git', '--no-replace-objects', '-C', str(repo), *args]
    p = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    record = {'argv': command, 'exit_code': p.returncode, 'stdout_bytes': len(p.stdout), 'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'stderr': p.stderr.decode('utf-8', 'backslashreplace')}
    if p.returncode:
        record['stdout'] = p.stdout.decode('utf-8', 'backslashreplace')
    commands.append(record)
    if p.returncode:
        raise RuntimeError(json.dumps(record))
    return p.stdout
def tree(commit):
    raw = run('ls-tree', '-r', '-z', '--full-tree', commit)
    assert raw.endswith(b'\0')
    result = {}
    for record in raw[:-1].split(b'\0'):
        metadata, raw_path = record.split(b'\t', 1)
        mode, kind, oid = metadata.decode('ascii').split()
        path = raw_path.decode('utf-8')
        assert path not in result
        result[path] = (mode, kind, oid)
    return result
def pairs(entries):
    out = {}
    for key, value in entries:
        if key in out:
            duplicates.append(key)
        out[key] = value
    return out
current = tree(snapshot)
old = tree(baseline)
raw_map = run('cat-file', 'blob', snapshot + ':proofs/SOURCE_MAP.json')
mapping = json.loads(raw_map, object_pairs_hook=pairs)
paths = mapping['paths']
assert mapping['base'] == baseline
for name in sorted(set(old) - set(paths)):
    mismatches.append({'missing_map_key': name})
for name in sorted(set(paths) - set(old)):
    mismatches.append({'extra_map_key': name})
selected = []
selections = Counter()
for name, entry in sorted(paths.items()):
    expected = (entry['mode'], 'commit' if entry['mode'] == '160000' else 'blob', entry['oid'])
    target = entry.get('current') or entry['preserved']
    selected.append(target)
    selections['current' if entry.get('current') else 'preserved'] += 1
    if old.get(name) != expected or current.get(target) != expected:
        mismatches.append({'original': name, 'selected': target, 'recorded': expected, 'baseline': old.get(name), 'snapshot': current.get(target)})
author = json.loads((directory / 'run-001/result.json').read_bytes())
stream = json.loads((directory / 'audit.stdout.txt').read_bytes())
agreement_fields = ['status', 'issue_count', 'issue_categories', 'counts', 'scope', 'not_claimed']
agreement = {key: author[key] == stream[key] for key in agreement_fields}
summary = {
    'reviewer_check': 'Independent local metadata comparison; author script not executed or imported',
    'snapshot': snapshot, 'baseline': baseline,
    'environment_overrides': {k: env[k] for k in ['GIT_NO_LAZY_FETCH','GIT_OPTIONAL_LOCKS','GIT_NO_REPLACE_OBJECTS','LC_ALL','LANG']},
    'commands': commands,
    'duplicate_json_keys': duplicates,
    'map_entries': len(paths), 'baseline_entries': len(old), 'snapshot_entries': len(current),
    'selected_unique_paths': len(set(selected)),
    'selection_counts': dict(sorted(selections.items())),
    'map_mode_counts': dict(sorted(Counter(x['mode'] for x in paths.values()).items())),
    'baseline_mode_counts': dict(sorted(Counter(x[0] for x in old.values()).items())),
    'snapshot_mode_counts': dict(sorted(Counter(x[0] for x in current.values()).items())),
    'metadata_mismatches': mismatches,
    'author_result_stdout_agreement': agreement,
    'author_input_hash_agreement': {
        'snapshot_tree': commands[0]['stdout_sha256'] == author['immutable_inputs']['snapshot_tree']['sha256'],
        'baseline_tree': commands[1]['stdout_sha256'] == author['immutable_inputs']['baseline_tree']['sha256'],
        'source_map': commands[2]['stdout_sha256'] == author['immutable_inputs']['source_map']['sha256']
    },
    'source_map_blob_oid': hashlib.sha1(b'blob ' + str(len(raw_map)).encode() + b'\0' + raw_map).hexdigest(),
    'mapped_source_blobs_read': 0,
    'scope': 'Metadata identity and evidence consistency only; no per-source SHA-256 validation, wrapper execution, Lean check, or mathematical approval',
    'finished_utc': datetime.now(timezone.utc).isoformat()
}
ok = not duplicates and not mismatches and all(agreement.values()) and all(summary['author_input_hash_agreement'].values()) and len(paths) == len(old) == len(set(selected)) == 9161
summary['status'] = 'PASS' if ok else 'FAIL'
print(json.dumps(summary, indent=2, ensure_ascii=True))
raise SystemExit(0 if ok else 1)
AGENT65_INDEPENDENT_METADATA
```

## Complete reviewer comparison output

The containing exec process returned exit code 0. Its complete substantive stdout is preserved below; there was no reported failure or truncation. The inner Git stderr values are all empty.

```json
{
  "reviewer_check": "Independent local metadata comparison; author script not executed or imported",
  "snapshot": "ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3",
  "baseline": "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5",
  "environment_overrides": {
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "LC_ALL": "C",
    "LANG": "C"
  },
  "commands": [
    {
      "argv": [
        "git",
        "--no-replace-objects",
        "-C",
        "/dev/shm/p196-agent65-dbfcd4",
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        "ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3"
      ],
      "exit_code": 0,
      "stdout_bytes": 3451946,
      "stdout_sha256": "34d7d7503fcf110bfb79ee702f6e8b83548893d0f9dbf2c07114dfac1af16741",
      "stderr": ""
    },
    {
      "argv": [
        "git",
        "--no-replace-objects",
        "-C",
        "/dev/shm/p196-agent65-dbfcd4",
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"
      ],
      "exit_code": 0,
      "stdout_bytes": 1284526,
      "stdout_sha256": "4adf1b7055ba528cde1a382930a47f2d48bb5a740f7d360df58763f3d262e4dc",
      "stderr": ""
    },
    {
      "argv": [
        "git",
        "--no-replace-objects",
        "-C",
        "/dev/shm/p196-agent65-dbfcd4",
        "cat-file",
        "blob",
        "ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3:proofs/SOURCE_MAP.json"
      ],
      "exit_code": 0,
      "stdout_bytes": 4396780,
      "stdout_sha256": "f6354e0411bc63c014c1ca0db07352a22f76ec6890417c097639a77c9539f8ba",
      "stderr": ""
    }
  ],
  "duplicate_json_keys": [],
  "map_entries": 9161,
  "baseline_entries": 9161,
  "snapshot_entries": 19225,
  "selected_unique_paths": 9161,
  "selection_counts": {
    "current": 2565,
    "preserved": 6596
  },
  "map_mode_counts": {
    "100644": 9152,
    "100755": 9
  },
  "baseline_mode_counts": {
    "100644": 9152,
    "100755": 9
  },
  "snapshot_mode_counts": {
    "100644": 19210,
    "100755": 15
  },
  "metadata_mismatches": [],
  "author_result_stdout_agreement": {
    "status": true,
    "issue_count": true,
    "issue_categories": true,
    "counts": true,
    "scope": true,
    "not_claimed": true
  },
  "author_input_hash_agreement": {
    "snapshot_tree": true,
    "baseline_tree": true,
    "source_map": true
  },
  "source_map_blob_oid": "e5f8d27bf09f50f8b9756bf91dff02e992aa4a32",
  "mapped_source_blobs_read": 0,
  "scope": "Metadata identity and evidence consistency only; no per-source SHA-256 validation, wrapper execution, Lean check, or mathematical approval",
  "finished_utc": "2026-10-17T00:21:21.291038+00:00",
  "status": "PASS"
}
```

## Final review boundary

This document is the reviewer's sole written artifact. Implementation, author evidence, source maps, wrappers, generated indexes, README/REPRODUCE, Git configuration, index and refs were not edited. The reviewer used local read-only metadata commands and created no Lean objects, source downloads, wrapper workspace, tests of mathematical claims, or GPU work.

The approved conclusion is a non-author independent review of the exact pinned metadata audit, with an independently implemented metadata comparison. It is not a review of every mathematical source and does not confer LEAN_CHECKED or INTEGRATED status. Publication and any main-branch integration remain the parent's separate responsibility.
