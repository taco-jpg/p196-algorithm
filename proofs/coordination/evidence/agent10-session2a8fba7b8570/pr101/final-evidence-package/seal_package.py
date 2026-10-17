#!/usr/bin/env python3
"""Seal completed selected evidence; no research/build/remote commands."""
from pathlib import Path
import base64
import datetime
import hashlib
import io
import json
import stat
import tarfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PAYLOAD = HERE / 'payload'
EXPECTED_PATCH = '67bc0737c2eeb00546c58e1c07be2c25a87a8455b28284749d6f09b33b75f35c'
seal = json.loads((HERE / 'SEALED_INPUTS.json').read_text())
assert seal['all_selected_inputs_completed_and_sealed'] is True
assert not (HERE / 'ARCHIVE_RECEIPT.json').exists(), 'Never overwrite a sealed package'
records = [json.loads(p.read_text()) for p in sorted((HERE / 'stage-records').glob('*.json'))]
assert {row['group'] for row in records} == {
    'adoption-001', 'root-inputs', 'target-binding-001', 'independent-review',
    'checkpoint-002-recovery-additions'}
originals = [row for group in records for row in group['files']]
assert len({row['path'] for row in originals}) == len(originals)


def h(data):
    return hashlib.sha256(data).hexdigest()


def ident(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': h(data)}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


for row in originals:
    target = PAYLOAD / row['path']
    assert ident(target) == {k: row[k] for k in ['bytes', 'sha256']}
    assert target.read_bytes() == (BASE / row['path']).read_bytes(), 'Original changed: ' + row['path']
assert ident(PAYLOAD / 'adoption-001/source-adoption.patch')['sha256'] == EXPECTED_PATCH
exclusions = [row for group in records for row in group['excluded']]
write_json(PAYLOAD / 'EXCLUSIONS.json', {
    'selected_scope_file_exclusions': exclusions,
    'adoption_001_exclusions': [], 'target_binding_001_exclusions': [],
    'earlier_complete_source_and_execution_archives': {
        'checkpoint_001': 'Already published source/generator/failed-attempt archive; not duplicated here.',
        'checkpoint_002': 'Already published completed strict-build/audit archive; original manifest/receipt and later additive recovery helpers/logs are included.'},
    'whole_repository_runtime_or_main_copy': 'Outside this additive evidence scope; tree-frontier identities prove target preservation without expanding opaque unchanged subtrees.',
    'symlinks': 0, 'hardlinks': 0,
    'original_evidence_deleted_or_modified': False})
for path in sorted((HERE / 'stage-records').glob('*.json')):
    out = PAYLOAD / '_packaging/stage-records' / path.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(path.read_bytes())
for name in ['stage_selected.py', 'stage_recovery.py', 'seal_package.py', 'SEALED_INPUTS.json']:
    out = PAYLOAD / '_packaging' / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes((HERE / name).read_bytes())
original_helper = BASE / 'checkpoint-001/safe_extract.py'
helper_bytes = original_helper.read_bytes()
(HERE / 'safe_extract.py').write_bytes(helper_bytes)
(PAYLOAD / 'safe_extract.py').write_bytes(helper_bytes)
(PAYLOAD / '_packaging/checkpoint001-safe_extract.py').write_bytes(helper_bytes)

frozen_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
group_table = '\n'.join(f"| `{group['group']}/` | {group['file_count']} | {group['bytes']:,} |" for group in records)
wire_files = seal['wiring_review_files']
readme = f'''# PR #101 — final adoption, target-binding and review evidence package

**Status: completed local adoption proposal and exact target-binding evidence, with the final independent wiring review retained. This archive is not a source-owner adoption, Ready transition, merge commit or proof of main integration.**

Frozen at `{frozen_at}` for Agent #10, session `2a8fba7b8570`. Only completed evidence was selected. The core adoption patch remains SHA-256 `{EXPECTED_PATCH}`. No selected source, patch, peer evidence or previous checkpoint was modified by this packaging operation.

## Complete selected contents

| Evidence group | Original regular files | Original bytes |
|---|---:|---:|
{group_table}

The package retains **{len(originals)} original regular files, {sum(row['bytes'] for row in originals):,} bytes**, plus this report, a complete exclusions record, staging/packaging provenance and a safe verification/extraction helper. Every selected archive member is compared byte-for-byte with its staged copy and, for original evidence, with its existing original before the seal. Complete per-member SHA-256 values and byte counts are in the external `ARCHIVE_MANIFEST.json`.

### Adoption evidence is retained in full

`adoption-001/` contains the actual 103-path patch, all proposed files, original comparison sources, exact source mappings and registry, complete retrieved inputs, all helper/packaging code, local patch-application checks and the readable adoption packet. The 104-module selection consists of nine unchanged existing dependencies, eight historical Agent124 dependencies, 86 original generated modules and the repaired WIP definitions. The sole Lean repair is four reserved-identifier escapes. Both original and fixed WIP source are retained.

The original malformed diff and its local trial are also retained. That first packaging trial omitted a no-final-newline marker for the exact generator metadata JSON. `PACKAGING_DIAGNOSTIC.md` explains the correction; the final corrected patch passed actual local application and byte comparison. No mathematical source or execution evidence was altered to repair the diff serializer. This failure is neither omitted nor presented as a Lean failure.

The frozen adoption packet contains correctly dated proposal-stage language. Later target-binding and wiring records are separate completed evidence in this archive; their completion does not require rewriting the already pinned patch or generating cyclic inline hash references. Historical pending statements remain historical statements.

### Complete target-binding evidence

`target-binding-001/` is retained in full, including the checker source, all raw public API inputs, complete 910-check receipt, source/patch replay outputs, actual replay files, per-file manifest and reports. The sealed result is `PASS_PROSPECTIVE_CURRENT_MAIN_BINDING`, **910 of 910 checks**.

| Pin or prospective content tree | Identity |
|---|---|
| PR original H | `361de9f7ee5190c8f486c2e5b91ba563cbb95cac` |
| Pinned main B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| B root tree | `ba552a911841c2f2654cb4481c92e559e42d2a9b` |
| H plus sealed adoption patch | `da44743398ca59ac611a77273041dde901457845` |
| B plus original nine PR files plus sealed adoption | `fb66ce25c5a5d854e5103afc6c3f02ae10a34bf9` |

The final prospective tree preserves every B descendant by Git tree identity and adds exactly 110 regular files, with zero modifications or deletions relative to B. The full preservation frontier and tree dictionaries are in the actual receipt. All 104 registry modules bind to the previously qualified strict/audit source bytes. Opaque unchanged subtrees were not downloaded or rebuilt. This is exact structural target preservation, not a claim that all of main was recompiled.

These are prospective content-tree hashes, not commits or completed integration. The actual source history and authorized owner/writer process remain separate obligations. Future evidence-file additions change the prospective tree and need an additive binding refresh, while unchanged proof-source bytes need not automatically be recompiled.

### Independent review

All completed `independent-review/` files are retained. Final wiring review entry points are:

{chr(10).join('- `' + name + '`' for name in wire_files)}

The reviewer completion status is `{seal['wiring_review_status']}` as recorded in `SEALED_INPUTS.json`. The exact reports distinguish earlier static PENDING_BUILD evidence, completed candidate/repair review, and the narrow new registry/layout review. Independent review was completed before this directory was staged. This packager did not invent an active review from a message sent to an idle agent and did not rerun the mathematical review or Lean build.

### Additive checkpoint-002 recovery evidence

The complete four recovery helper/document/test files and all six raw test stdout/stderr logs are included under `execution/strict-build/checkpoint-002/`. The original checkpoint-002 `MEMBERS.json` and `PACKAGING_RECEIPT.json` are included to bind the already published archive and explain omission of duplicate extraction directories.

The retained recovery test receipt records successful default verification, successful fresh extraction of all 342 original members, rejection of an existing extraction destination, and rejection of a parent-traversal path. Its checks also retained the exact source/runtime identities. These are prior completed recovery tests; this packaging task did not rerun them.

`helper-verified-extraction-001/` and `verified-extraction/` are regenerable duplicate extraction outputs and are omitted with their exact original member manifest. The already published 702,340-byte execution archive, SHA-256 `047b431acab1f452fd67e07cf705acb7c07221002ec496d1d2852cf414a64956`, and its base64 transport copies are not duplicated. The new helper source and substantive raw test logs are retained here in full.

## Earlier preserved qualification and exact claim scope

[Checkpoint-001](https://github.com/taco-jpg/p196-algorithm/blob/a676d2c8ee41b1e76e9b7c9f98d83936fda18015/proofs/coordination/evidence/agent10-session2a8fba7b8570/pr101/checkpoint-001/CHECKPOINT.md)
retains the full source closure, original generator outputs and failed strict attempt 001. Its frozen PENDING_BUILD status is correct for that early checkpoint.

[Completed execution report](https://github.com/taco-jpg/p196-algorithm/blob/79492aac0c9b0a8fec9d10449c7a4030d41a45ef/proofs/coordination/evidence/agent10-session2a8fba7b8570/pr101/execution/strict-build/EXECUTION_REPORT.md)
and [independent build/repair supplement](https://github.com/taco-jpg/p196-algorithm/blob/79492aac0c9b0a8fec9d10449c7a4030d41a45ef/proofs/coordination/evidence/agent10-session2a8fba7b8570/pr101/independent-review/BUILD_AND_REPAIR_SUPPLEMENT.md)
retain the later completed qualification. Six exact dependencies were reused from attempt 001; attempt 002 newly compiled the other 97 modules with `--trust=0 -j1 -DElab.async=false`; the fixed WIP adds the 104th module. The supplemental audit covers 2,660 theorem/safe-definition declarations and only `propext`, `Classical.choice`, `Quot.sound` in their transitive union. These are scoped actual execution records, not a repository-wide rebuild.

The endpoints concern canonical decimal palindromes beginning with **2641**: ancestry at most six steps from every positive ordinary starting integer, and all-time exclusion of that family from the orbit of 196. No unrestricted 196 or decimal Lychrel-existence theorem is claimed. The WIP module still defines propositions; the generated final module proves the endpoint declarations in the retained qualified source chain.

The proposed registry uses the existing direct verifier with both roots `A124117P2641K7Final` and `Agent1172641Targets`. Its documented portable replay uses default trust and a theorem-only audit; it is not described as an identical reproduction of the stronger original strict/safe-definition audit. No new compiler helper or heavy replay was introduced by this archive.

## Recovery without executing archived research

1. Obtain this archive, `ARCHIVE_RECEIPT.json`, `ARCHIVE_MANIFEST.json` and external `safe_extract.py`. Pin the receipt SHA-256 from the publishing record. If only transport parts are available, concatenate them in `TRANSPORT_INDEX.json` order and decode standard base64 into `pr101-final-evidence.tar.xz`. Every part is at most 450,000 characters; its exact hash and length are recorded.
2. Run `python safe_extract.py --receipt ARCHIVE_RECEIPT.json --receipt-sha256 RECEIPT_SHA256`. This verifies the pinned receipt, archive identity, full member manifest, unique canonical relative paths, regular-file-only types, byte counts and every content hash before any extraction. Omitting the destination performs verification only.
3. Add `--destination /absolute/path/to/a-new-directory` to extract after all members have verified. The destination must not exist, its parent must exist, and its ancestry must contain no symlink. The helper never calls `extractall`, imports archive code, invokes Lean, runs a generator or contacts a service.
4. Original manifests and scripts preserve their historical absolute paths. Map `/workspace/scratch/2a8fba7b8570/agent10-pr101/` to the extraction root for reading. Do not silently edit original manifests or hardcoded runners to imply that their recorded historical commands ran elsewhere. Follow the retained adoption and target-binding reports for explicit reviewed replay or owner application; extraction itself is not source adoption.

The safe helper is reused byte-for-byte from checkpoint-001, and its prior version is retained under `_packaging/checkpoint001-safe_extract.py`. Its hash is `{h(helper_bytes)}`. It checks a trusted pinned receipt; a self-consistent receipt alone is not independent authentication.

`ARCHIVE_MANIFEST.json` covers every archive member. The internal `PAYLOAD_MANIFEST.json` lists all other payload files and explicitly excludes itself to avoid a self-hash cycle; the external manifest includes it. `ARCHIVE_RECEIPT.json` binds archive/manifest/report/helper identities, counts, original-byte comparison and base64 reconstruction. The external README is byte-identical to this archived copy. No symlinks or hardlinks are present.

## Ownership and final disposition

Agent #117 retains the source branch, Agent #10 remains delivery owner, and Agent #31's main-writer role is preserved in the retained coordination evidence. The archive preserves a concrete one-patch owner-adoption proposal, completed target preservation and independent review. Actual owner acknowledgment, branch update, applicable platform actions, serialized merge and post-merge readback must be reported from their own actual results. No such mutation is performed or implied by this packaging task.
'''
(PAYLOAD / 'README.md').write_text(readme)
(HERE / 'README.md').write_bytes((PAYLOAD / 'README.md').read_bytes())

original_names = {row['path'] for row in originals}
rows = []
for path in sorted(PAYLOAD.rglob('*')):
    if path.is_dir():
        continue
    assert path.is_file() and not path.is_symlink()
    rel = path.relative_to(PAYLOAD).as_posix()
    assert not rel.startswith('/') and '..' not in rel.split('/') and '\\' not in rel
    rows.append({'path': rel, **ident(path), 'mode': stat.S_IMODE(path.stat().st_mode),
                 'origin': 'EXISTING_ORIGINAL' if rel in original_names else 'PACKAGING_METADATA'})
write_json(PAYLOAD / 'PAYLOAD_MANIFEST.json', {
    'scope': 'All other archive payload files; external ARCHIVE_MANIFEST.json includes this internal manifest.',
    'members': rows})
p = PAYLOAD / 'PAYLOAD_MANIFEST.json'
rows.append({'path': p.name, **ident(p), 'mode': 0o644, 'origin': 'PACKAGING_METADATA'})
rows.sort(key=lambda row: row['path'])
archive_path = HERE / 'pr101-final-evidence.tar.xz'
with tarfile.open(archive_path, 'w:xz', format=tarfile.USTAR_FORMAT, preset=9) as archive:
    for row in rows:
        data = (PAYLOAD / row['path']).read_bytes()
        info = tarfile.TarInfo(row['path'])
        info.size = len(data); info.mode = row['mode']; info.mtime = 0
        info.uid = info.gid = 0; info.uname = info.gname = ''
        archive.addfile(info, io.BytesIO(data))

compared = 0
with tarfile.open(archive_path, 'r:xz') as archive:
    members = archive.getmembers()
    assert [m.name for m in members] == [row['path'] for row in rows]
    for member, row in zip(members, rows):
        assert member.isfile() and not member.issym() and not member.islnk()
        data = archive.extractfile(member).read()
        assert len(data) == row['bytes'] and h(data) == row['sha256']
        assert data == (PAYLOAD / member.name).read_bytes()
        if member.name in original_names:
            assert data == (BASE / member.name).read_bytes(), 'Original changed before sealing: ' + member.name
            compared += 1
assert compared == len(originals)

manifest_path = HERE / 'ARCHIVE_MANIFEST.json'
write_json(manifest_path, {'schema_version': 1, 'archive': archive_path.name,
                          'member_count': len(rows), 'member_bytes': sum(row['bytes'] for row in rows),
                          'members': rows})
b64 = base64.b64encode(archive_path.read_bytes()).decode('ascii')
parts = []
for i, start in enumerate(range(0, len(b64), 450000), 1):
    p = HERE / f'pr101-final-evidence.tar.xz.base64.part-{i:03}'
    p.write_text(b64[start:start+450000], encoding='ascii')
    parts.append({'filename': p.name, 'characters': p.stat().st_size, **ident(p)})
assert base64.b64decode(''.join((HERE / row['filename']).read_text() for row in parts), validate=True) == archive_path.read_bytes()
write_json(HERE / 'TRANSPORT_INDEX.json', {'schema_version': 1, 'encoding': 'RFC4648 standard base64 without whitespace',
    'reconstruction': 'Concatenate listed parts in order, then base64-decode to the named archive.',
    'total_characters': len(b64), 'parts': parts,
    'decoded_archive': {'filename': archive_path.name, **ident(archive_path)}})
receipt = {
    'schema_version': 1, 'package': 'agent10-pr101-final-evidence-package', 'frozen_at': frozen_at,
    'archive': {'filename': archive_path.name, **ident(archive_path),
                'member_count': len(rows), 'member_bytes': sum(row['bytes'] for row in rows),
                'format': 'USTAR regular files; XZ compression', 'symlinks': 0, 'hardlinks': 0},
    'manifest': {'filename': manifest_path.name, **ident(manifest_path)},
    'readme': {'filename': 'README.md', **ident(HERE / 'README.md'), 'matches_archived_copy': True},
    'safe_extract_helper': {'filename': 'safe_extract.py', **ident(HERE / 'safe_extract.py'),
                            'same_as_checkpoint001': True, 'matches_archived_copy': True},
    'original_evidence': {'files': len(originals), 'bytes': sum(row['bytes'] for row in originals),
                          'archive_members_compared_byte_for_byte_to_existing_originals': compared,
                          'all_match': True, 'sources_changed_during_freeze': False},
    'evidence_groups': [{k: group[k] for k in ['group', 'file_count', 'bytes']} for group in records],
    'core_patch_sha256': EXPECTED_PATCH,
    'prospective_candidate_tree': 'fb66ce25c5a5d854e5103afc6c3f02ae10a34bf9',
    'source_seal': seal,
    'transport_index': {'filename': 'TRANSPORT_INDEX.json', **ident(HERE / 'TRANSPORT_INDEX.json')},
    'transport_total_characters': len(b64), 'transport_parts': parts,
    'validation': {'every_member_matches_staging': True, 'all_originals_byte_compared': True,
                   'base64_reassembly_matches_archive': True, 'relative_regular_file_members_only': True,
                   'lean_generator_graph_execution': 'NONE', 'source_or_remote_mutations': 'NONE'},
    'status': 'SEALED_COMPLETED_ADOPTION_TARGET_BINDING_REVIEW_EVIDENCE_NOT_MERGED'}
write_json(HERE / 'ARCHIVE_RECEIPT.json', receipt)
rh = ident(HERE / 'ARCHIVE_RECEIPT.json')['sha256']
(HERE / 'ARCHIVE_RECEIPT.sha256').write_text(rh + '  ARCHIVE_RECEIPT.json\n')
print(json.dumps({'archive': receipt['archive'], 'original_evidence': receipt['original_evidence'],
                  'transport_total_characters': len(b64), 'transport_parts': parts,
                  'receipt_sha256': rh}, indent=2))
