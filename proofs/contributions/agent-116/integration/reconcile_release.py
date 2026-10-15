#!/usr/bin/env python3
"""Reconcile Agent116's reviewed source and complete byte publication.

Adapted from Agent104's release reconciler. No Git mutation or Lean execution.
Requires completed independent review and affected-root integration verification.
Historical inventory bytes are preserved; concurrent files gain no math status.
"""
from pathlib import Path
import collections
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO = ROOT.parent
REL = 'contributions/agent-116/integration'
OWN = 'contributions/agent-116'
BASE = 'eec3d5f3646cab50abad6e610ea19626cd249070'
SOURCE = 'c0bca37913df5b52963c484ef20cbeb5b3838a32'
CLAIM = '4605dabc828a584923f8bf91f94ec3369e1b10b9'
COORD = 'coordination/agent116-cap3-reviewed.json'
SHARED = {'README.md', 'FINDINGS.md', 'REPRODUCE.md', 'REPORTS.md',
          'PUBLICATION_SCOPE.md', 'INVENTORY.json', 'INVENTORY.tsv',
          'FILES.md', 'MANIFEST.sha256', 'release_stats.json', 'VALIDATION.json'}
BEGIN = '<!-- BEGIN AGENT116 REVIEWED CAP3 -->'
END = '<!-- END AGENT116 REVIEWED CAP3 -->'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return sha(path.read_bytes())


def put(path, obj):
    (ROOT / path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def baseline(path):
    return git('show', BASE + ':proofs/' + path)


def block(path, content):
    text = (ROOT / path).read_text()
    addition = BEGIN + '\n' + content.strip() + '\n' + END
    if BEGIN in text:
        assert text.count(BEGIN) == text.count(END) == 1
        text = text[:text.index(BEGIN)] + addition + text[text.index(END) + len(END):]
    else:
        text = text.rstrip() + '\n\n' + addition + '\n'
    (ROOT / path).write_text(text)


def verify_evidence():
    review = json.loads((ROOT / OWN / 'review/REVIEW.json').read_text())
    report = json.loads((ROOT / OWN / 'review/execution/final/manifest.json').read_text())
    assert review['verdict'] == 'INDEPENDENTLY_REVIEWED_PASS'
    assert review['remote_source_commit'] == SOURCE
    assert report['status'] == 'PASS' and report['fresh_local_objects'] is True
    assert len(report['sources']) == 137 and report['theorem_count'] == 1991
    for rec in report['sources'].values():
        assert digest(REPO / rec['source']) == rec['sha256'], rec['source']
    assert all(cmd['exit'] == 0 for cmd in report['commands'])
    assert all(set(xs) <= {'propext', 'Classical.choice', 'Quot.sound'}
               for xs in report['theorem_axioms'].values())
    integration = json.loads((HERE / 'endpoints/verification.json').read_text())
    assert integration['status'] == 'PASS'
    return review, report, integration


def docs():
    block('README.md', f'''## Agent 116: reviewed cap-three certificate obstruction

`Agent116.CertificateExterior.accepted_exceeds_three` proves that every
certificate accepted by the original return checker has a state whose exterior,
after maximal phase-suffix trimming, has length greater than three. The sole
premise is `check cert = true`; no realizability, positive-head or period-bound
premise is added. The [aggregate source]({OWN}/certificate-exterior/Agent116All.lean)
imports both complete finite certificate assemblies and the actual-orbit bridge.

The unrestricted bounded exterior domain exits length at most three within ten
updates; the valid domain within nine. For genuine decimal templates with both
bands initially at least eighteen, the latter bound transfers to the specified
exterior coordinate along `Lychrel196.orbit`. It is not a palindrome-hit claim,
nor a claim about every possible representation of that integer.

[Independent AI review]({OWN}/review/REVIEW.md) rebuilt 137 modules from an empty
object directory and audited 1,991 compiled theorem constants. Only `propext`,
`Classical.choice`, and `Quot.sound` occur transitively. Source commit `{SOURCE}`
is frozen; [integration checks]({REL}/endpoints/verification.json) recheck its
source pins and explicitly reuse those fresh verified dependencies for endpoint
recompilation. This excludes this bounded certificate class; no accepted return
certificate, infinite safe integer orbit, or resolution of 196 is supplied.
Final publication status is recorded on the coordination branch after main moves.''')
    block('FINDINGS.md', f'''## Agent 116: certificate normalization and exact cap-three bounds

| Lean result | Exact scope | Verification |
|---|---|---|
| `Agent116.CertificateExterior.accepted_exceeds_three` | Original checker acceptance alone implies some maximally trimmed exterior has length at least four; all periods and internal blocks are allowed. | [Source and full review]({OWN}/review/REVIEW.md) |
| `check_eq_false_of_normalized_cap_three`, `check_eq_false_of_raw_cap_three` | Every candidate satisfying the stated cap is rejected, including the empty candidate. | Same reviewed aggregate |
| `P196.Agent116.Cap3.cap3_exit_witness` | Valid eight-phase bounded exterior of length at most three exits within nine updates; `(8,[11,9])` attains nine. | Concrete kernel-checked batches and completeness proof |
| `P196.Agent116.Cap3.cap3_all_exit_witness` | Without positive-head or canonical-trim restrictions, the bound is ten; `(6,[0])` attains ten in this relaxed domain. | Separate complete kernel-checked batch assembly |
| `Agent116.ActualCap3.lychrel_cap3_exit` | Bounded ordinary decimal template with valid exterior and both bands at least eighteen: its specified exterior grows beyond three by actual time nine. | Formal correspondence to `Lychrel196.orbit` |

The 1,991 audited constants measure coverage, not independent discoveries.
All finite certificate hypotheses used by these endpoints are discharged in
Lean; the Python scan is only an independent diagnostic. None of these results
constructs an accepted cyclic certificate or settles 196.''')
    block('REPRODUCE.md', f'''## Agent 116: reviewed complete cap-three aggregate

Use official Lean 4.19.0, release commit `6caaee842e94`, with an absolute
executable path and a nonexistent evidence directory, from the repository root:

```sh
python3 -B proofs/{OWN}/check.py "$LEAN_BIN" \\
  --evidence "$AGENT116_EVIDENCE" --module Agent116All --jobs 2 --require-committed
```

The separate reviewer did not invoke that author runner. Its independently
implemented complete build, including the additional semantic-scope fixture, is:

```sh
python3 -B proofs/{OWN}/review/rebuild.py --lean "$LEAN_BIN" \\
  --build "$AGENT116_REVIEW_EVIDENCE" --jobs 2 Agent116All CanonicalityCounterexample
```

See [review evidence]({OWN}/review/execution/final/manifest.json) for all 137
source hashes, commands, exit statuses and 1,991 actual `#print axioms` results.
The shared official toolchain plus documented host readlink shim was reused;
the review does not claim an independent toolchain download. Local project
objects were built fresh. Standard foundational axioms are reported, not hidden.

The [integration endpoint check]({REL}/endpoints/verification.json) deliberately
reuses those independently rebuilt dependency objects after comparing every
source pin. Byte indexes can be reproduced separately:

```sh
python3 -B proofs/{REL}/reconcile_release.py
python3 -B proofs/verify_release.py
```

The byte verifier does not prove mathematics. The reconciler requires the
frozen independent PASS reports and integration evidence before changing files.''')
    block('PUBLICATION_SCOPE.md', f'''## Agent 116: complete research and review evidence

This update retains Agent116's source, complete finite batches and generators,
successful and failed development attempts, full substantive compiler and axiom
logs, independent arithmetic controls, semantic review, and integration evidence.
Only the endpoints and hypotheses stated in the [review]({OWN}/review/REVIEW.md)
receive mathematical acceptance. Existing concurrent files receive byte coverage
without any new mathematical endorsement.

Three pre-existing Agent102 inventory records referred to earlier source bytes.
The [reconciliation record]({REL}/index-reconciliation.json) relocates those
exact historical bytes into an Agent116 archive and indexes current originals
without altering them. Five exact historical Agent11 dependency modules missing
from the existing Agent102/109 audit closure are preserved with their reviewed
commit and hash provenance in `historical-review-deps/`. Four already pinned
Mathlib imports used by the existing real-weights contribution are recognized
as external source dependencies by the byte verifier; no Mathlib theorem is
re-audited or newly trusted by Agent116. Earlier inventory provenance and mixed TSV row formats
are preserved. Older aggregate statistics retain their historical scope.

Toolchain installations, reproducible `.olean` and `.ilean` objects, Python
caches, and duplicate build source snapshots are excluded. Their committed
original sources, source hashes, compiler hashes, commands and complete logs
remain available. Failed proof development is retained outside the accepted
aggregate and never presented as a completed theorem. No P196 or infinite-safe-
orbit result is claimed.''')
    reports = sorted(str(p.relative_to(ROOT)) for p in (ROOT / OWN).rglob('*.md')
                     if '__pycache__' not in p.parts)
    block('REPORTS.md', '## Agent 116: cap-three source, review and integration\n\n' +
          '\n'.join(f'- [{p}]({p})' for p in reports))


def historical_bytes(path, expected):
    for commit in git('rev-list', '--all', '--', 'proofs/' + path).decode().splitlines():
        proc = subprocess.run(['git', 'show', commit + ':proofs/' + path],
                              cwd=REPO, capture_output=True)
        if proc.returncode == 0 and sha(proc.stdout) == expected:
            return commit, proc.stdout
    raise RuntimeError('Cannot recover historical inventory bytes: ' + path)


def selected_paths():
    files = {p[7:] for p in git('ls-files', 'proofs').decode().splitlines()}
    files.update(str(p.relative_to(ROOT)) for p in (ROOT / OWN).rglob('*')
                 if p.is_file() and '__pycache__' not in p.parts)
    files.add(COORD)
    for name in files:
        assert (ROOT / name).is_file(), name
        assert not name.endswith(('.olean', '.ilean', '.pyc', '.so', '.o')), name
    return sorted(files)


def main():
    review, report, integration = verify_evidence()
    put(COORD, {'agent': 'Agent #116', 'task': 'agent116-certificate-exterior-obstruction',
        'integration_task': 'agent116-integrate-cap3', 'integration_claim': CLAIM,
        'mathematical_source_commit': SOURCE, 'integration_parent': BASE,
        'accepted_root': 'Agent116All', 'independent_source_review': review,
        'integration_endpoint_check': REL + '/endpoints/verification.json',
        'publication_status': 'VERIFIED_CANDIDATE; final main SHA recorded on coordination after confirmed merge',
        'scope': 'Check-only cap3 certificate exclusion and specified ordinary-orbit exterior growth; no P196'})
    docs()
    records_base = json.loads(baseline('INVENTORY.json'))
    old_tsv = baseline('INVENTORY.tsv').decode()
    moved = []
    for record in records_base:
        if record['publication'] != 'retained':
            continue
        path = record['published_path']
        current = ROOT / path
        if current.exists() and current.stat().st_size == record['bytes'] and digest(current) == record['sha256']:
            continue
        commit, data = historical_bytes(path, record['sha256'])
        archive = f"{REL}/historical-index/{record['sha256']}/{Path(path).name}"
        (ROOT / archive).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / archive).write_bytes(data)
        record.update(published_path=archive, superseded_published_path=path,
                      original_git_commit=commit,
                      reconciliation_note='Exact indexed historical bytes retained; current original unchanged')
        moved.append({'original_path': path, 'archive_path': archive,
                      'sha256': sha(data), 'bytes': len(data), 'commit': commit})
        lines = old_tsv.splitlines(keepends=True)
        for i, line in enumerate(lines):
            fields = line.rstrip('\n').split('\t')
            if len(fields) == 7 and fields[2] == record['sha256'] and fields[6] == path:
                fields[6] = archive
                lines[i] = '\t'.join(fields) + '\n'
        old_tsv = ''.join(lines)
    put(REL + '/index-reconciliation.json', {'baseline_commit': BASE,
        'historical_inventory_records_preserved': len(records_base),
        'historical_tsv_field_counts': dict(collections.Counter(str(len(x.split('\t'))) for x in old_tsv.splitlines())),
        'relocated_historical_records': moved,
        'scope': 'Byte provenance only; current Agent102 files unchanged; no concurrent math re-review'})
    docs()
    log = HERE / 'release-integrity.log'
    log.write_text('{"status":"PENDING"}\n')
    stats_base = json.loads(baseline('release_stats.json'))
    validation_base = json.loads(baseline('VALIDATION.json'))
    previous = None
    for iteration in range(5):
        files = selected_paths()
        records = list(records_base)
        known = {r['published_path'] for r in records if r['publication'] == 'retained'}
        added = []
        for name in files:
            if name in known or name in SHARED:
                continue
            own = name.startswith(OWN + '/') or name == COORD
            data = (ROOT / name).read_bytes()
            record = {'source_path': name, 'bytes': len(data), 'sha256': sha(data),
                'publication': 'retained', 'published_path': name,
                'reason': 'Agent116 research, review or scoped integration evidence' if own else
                          'Concurrent tracked byte coverage only; no mathematical review by Agent116',
                'family_report': OWN + '/README.md' if own else 'README.md',
                'source_snapshot': 'agent116-reviewed-cap3-20261015',
                'semantic_status': 'See exact source-specific review and hypotheses' if own else
                                   'BYTE_INDEX_ONLY_NO_NEW_MATHEMATICAL_REVIEW'}
            records.append(record)
            added.append(record)
        put('INVENTORY.json', records)
        columns = ('source_path', 'bytes', 'sha256', 'publication', 'reason', 'family_report', 'published_path')
        (ROOT / 'INVENTORY.tsv').write_text(old_tsv.rstrip('\n') + '\n' +
            ''.join('\t'.join(str(r.get(k, '')) for k in columns) + '\n' for r in added))
        (ROOT / 'FILES.md').write_text('# Complete published file list\n\n'
            'Tracked proof paths and retained Agent116 evidence. Byte coverage does not imply mathematical acceptance.\n\n' +
            ''.join(f'- [{name}]({name})\n' for name in files))
        own = [r for r in added if r['published_path'].startswith(OWN + '/') or r['published_path'] == COORD]
        update = {'mathematical_source_commit': SOURCE, 'integration_parent': BASE,
            'source_modules': 137, 'audited_theorem_constants': 1991,
            'retained_agent116_files_added': len(own), 'retained_agent116_bytes': sum(r['bytes'] for r in own),
            'concurrent_byte_only_records_added': len(added) - len(own),
            'current_unique_published_files': len(files), 'historical_records_preserved': len(records_base),
            'historical_records_relocated_without_byte_changes': len(moved),
            'earlier_aggregate_fields_are_historical': True, 'substantive_agent116_research_omissions': 0}
        put('release_stats.json', dict(stats_base, agent116_cap3_update=update))
        put('VALIDATION.json', dict(validation_base, agent116_cap3_update={
            'mathematical_source_commit': SOURCE, 'independent_review': 'PASS',
            'source_modules': 137, 'audited_theorem_constants': 1991,
            'axiom_union': review['axiom_union'], 'integration_endpoint_check': integration,
            'release_integrity': previous or {'status': 'PENDING'},
            'release_integrity_record': REL + '/release-integrity.log',
            'unrelated_math_reaudited': False, 'mathematical_proof_check_by_release_verifier': False}))
        (ROOT / 'MANIFEST.sha256').write_text(''.join(
            f'{digest(ROOT / name)}  {name}\n' for name in files if name != 'MANIFEST.sha256'))
        proc = subprocess.run(['python3', '-B', str(ROOT / 'verify_release.py')],
                              cwd=REPO, capture_output=True, text=True)
        if proc.returncode:
            (HERE / 'release-integrity-failure.log').write_text(proc.stdout + proc.stderr)
            raise RuntimeError(proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        output = json.dumps({'command': 'python3 -B proofs/verify_release.py',
            'exit_code': 0, 'record_scope': 'Byte and source-presence check, not mathematics',
            'result': result}, indent=2) + '\n'
        if previous == result and log.read_text() == output:
            print(json.dumps({'status': 'PASS', 'release_integrity': result,
                'historical_relocations': len(moved), 'iterations': iteration + 1}, indent=2))
            return
        previous = result
        log.write_text(output)
    raise RuntimeError('Release indexes did not stabilize')


if __name__ == '__main__':
    main()
