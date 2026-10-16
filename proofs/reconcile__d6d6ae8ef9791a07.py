#!/usr/bin/env python3
"""Scoped PR39 documentation and byte-index reconciliation, without Git writes.

Adapted from Agent116's incremental reconciler. --prepare-only writes only the
five scoped prose blocks. --reconcile --stage-ready requires the integration
owner's prior confirmation that publication selection and reviews are staged.
No Lean execution, mathematical source edits, or unrelated review acceptance.
"""
from pathlib import Path
import argparse
import collections
import copy
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPO = ROOT.parent
OWN = 'contributions/agent-110'
REL = OWN + '/integration'
DEFAULT_BASE = '2c2551165c13d23b11d44122fc7a504d51053e59'
DEFAULT_SOURCE = 'eb4817f0973cbbe2a059af33d5dc53877a5275b7'
DEFAULT_CLAIM = 'd2f719d223c54d890d1ffde44a29c6ed5bd895eb'
RADIX_SOURCE = '1cdc55c89b376faa270d1dffaf21e21b6eedeb4b'
RADIX_LOCAL = 'ee54c6e7d95cf9cd5d1a4bd530aa2773ac22f33b'
AGENT112_SOURCE = 'e7689d35f41ff325037a238cfc594d95e0da04e1'
SHARED = {'README.md', 'FINDINGS.md', 'REPRODUCE.md', 'PUBLICATION_SCOPE.md',
          'REPORTS.md', 'INVENTORY.json', 'INVENTORY.tsv', 'FILES.md',
          'MANIFEST.sha256', 'release_stats.json', 'VALIDATION.json'}
BEGIN = '<!-- BEGIN AGENT110 REVIEWED PR39 -->'
END = '<!-- END AGENT110 REVIEWED PR39 -->'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    return sha(path.read_bytes())


def read(name):
    return json.loads((ROOT / name).read_text())


def put(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def block(name, content):
    path = ROOT / name
    text = path.read_text()
    addition = BEGIN + '\n' + content.strip() + '\n' + END
    if BEGIN in text or END in text:
        assert text.count(BEGIN) == text.count(END) == 1, name
        text = text[:text.index(BEGIN)] + addition + text[text.index(END) + len(END):]
    else:
        text = text.rstrip() + '\n\n' + addition + '\n'
    path.write_text(text)


def check_logs(report, folder, exit_key):
    for cmd in report['commands']:
        assert cmd[exit_key] == 0, cmd
        path = ROOT / folder / cmd['log']
        assert digest(path) == cmd['log_sha256'], path


def verify_evidence(args):
    checked_dir = OWN + '/review-checked'
    checked = read(checked_dir + '/REVIEW_RESULT.json')
    manifest_path = checked_dir + '/' + checked['accepted_manifest']
    manifest = read(manifest_path)
    assert checked['status'] == manifest['status'] == 'PASS'
    assert checked['mathematical_remote_commit_reported_by_publisher'] == args.source
    local_source = checked['mathematical_local_commit']
    assert git('rev-parse', local_source + '^{tree}').decode().strip() == checked['local_tree_independently_verified']
    assert git('rev-parse', args.source + '^{tree}').decode().strip() == checked['local_tree_independently_verified']
    assert digest(ROOT / manifest_path) == checked['accepted_manifest_sha256']
    assert manifest['objects_reused'] is False and manifest['empty_build_directory_created'] is True
    assert manifest['all_source_hashes_unchanged'] is True
    assert len(manifest['sources']) == 19
    assert manifest['compiled_constants_audited'] == 2180
    assert manifest['compiled_theorems_audited'] == 1697
    assert len(manifest['axiom_audit']) == 2180
    assert all(set(x['axioms']) <= ALLOWED for x in manifest['axiom_audit'].values())
    for rec in manifest['sources'].values():
        assert digest(REPO / rec['path']) == rec['sha256'], rec['path']
        assert sha(git('show', args.source + ':' + rec['path'])) == rec['sha256'], rec['path']
    assert digest(REPO / manifest['driver_path']) == manifest['driver_sha256']
    check_logs(manifest, str(Path(manifest_path).parent), 'exit_code')
    assert checked['exact_signature_check_exit_code'] == 0
    provenance = read(checked_dir + '/PROVENANCE_CHECK.json')
    assert provenance['status'] == 'PASS'
    assert set(provenance['records']) == {'AdmissibleCenters', 'AdmissibleHeads', 'SymbolicGrowth'}
    for name, rec in provenance['records'].items():
        assert rec['original_commit'] == AGENT112_SOURCE
        original = git('show', AGENT112_SOURCE + ':' + rec['original_path'])
        snapshot = REPO / manifest['sources'][name]['path']
        assert snapshot.read_bytes() == original
        assert sha(original) == rec['snapshot_sha256']
    dependency = read(OWN + '/review-agent112/verification.json')
    assert dependency['status'] == 'PASS' and dependency['project_object_reuse'] is False
    assert dependency['source_commit'] == AGENT112_SOURCE
    radix = read(OWN + '/review-radix/verification.json')
    assert radix['status'] == 'PASS' and radix['project_object_reuse'] is False
    assert radix['build_dir_initially_absent'] is True
    assert len(radix['sources']) == 4 and radix['audited_declarations'] == 48
    assert git('rev-parse', RADIX_SOURCE + '^{tree}') == git('rev-parse', RADIX_LOCAL + '^{tree}')
    assert all(set(xs) <= {'propext', 'Quot.sound'} for xs in radix['axiom_audit'].values())
    for rec in radix['sources'].values():
        assert digest(REPO / rec['path']) == rec['sha256'], rec['path']
        assert sha(git('show', RADIX_SOURCE + ':' + rec['path'])) == rec['sha256'], rec['path']
    check_logs(radix, OWN + '/review-radix', 'returncode')
    search = read(OWN + '/exterior-global/search/summary.json')
    counts = collections.Counter(r['status'] for r in search['runs'])
    assert counts == {'SOLVER_UNSAT_UNCERTIFIED': 5, 'UNKNOWN': 3}, counts
    assert search['sat_candidates'] == search['kernel_verified_cycles'] == 0
    return {
        'All': {'checker': OWN + '/certificate-budget/check.py',
                'import_root': 'All', 'module_count': 19,
                'source_commit': args.source, 'independent_review': checked_dir + '/REVIEW_RESULT.json',
                'verified_local_source_commit': local_source,
                'verified_local_tree': checked['local_tree_independently_verified'],
                'remote_local_mapping_scope': 'Fetched remote Git tree equals independently reviewed local tree; all current source bytes match remote objects',
                'accepted_manifest': manifest_path, 'accepted_manifest_sha256': digest(ROOT / manifest_path),
                'kernel_safe_declarations_audited': 2180, 'theorem_constants_audited': 1697,
                'axiom_union': sorted({a for x in manifest['axiom_audit'].values() for a in x['axioms']}),
                'scope': 'Check-only certificate necessary conditions; saturation equality remains explicit'},
        'Radix': {'checker': OWN + '/exterior-global/check.py',
                  'import_root': 'RadixExterior', 'module_count': 4,
                  'source_commit': RADIX_SOURCE,
                  'verified_local_source_commit': RADIX_LOCAL,
                  'independent_review': OWN + '/review-radix/verification.json',
                  'public_declarations_audited': 48, 'public_theorems_audited': 25,
                  'new_theorems': 15, 'axiom_union': ['Quot.sound', 'propext'],
                  'scope': 'Specified (phase,Z) observable and potential obstruction, not an exterior state cycle'},
        'search': {'summary': OWN + '/exterior-global/search/summary.json',
                   'outcomes': dict(counts), 'kernel_verified_cycles': 0,
                   'scope': 'Bounded exterior-only solver evidence; no certified UNSAT theorem'},
        'agent112_dependency': {'original_author': 'Agent112', 'original_commit': AGENT112_SOURCE,
                               'modules': sorted(provenance['records']),
                               'review': OWN + '/review-agent112/verification.json',
                               'provenance': checked_dir + '/PROVENANCE_CHECK.json',
                               'full_PR41_accepted': False}}


def docs(args):
    block('README.md', f'''## Agent 110: reviewed PR39 integration candidate

The [All certificate root]({OWN}/certificate-budget/All.lean) proves necessary
conditions directly from `Agent109.Cert.check cert = true`. For initial phase
in `{{2,4,8,16,14,10}}`, let `O = totalGam cert`, `Dg = totalG cert` and
`Dh = totalH cert`. Then `O = 2*(Dg+Dh)`, both gains are nonnegative multiples
of nine, `O` is a positive multiple of eighteen, `2*O <= P <= 4*O`, and
`P % 6 = 0` with `P >= 42`. With the additional saturation equality `2*O = P`,
`72` divides `P` and `P >= 72`. Acceptance alone gives `P >= 4` in every phase
class. Trims need not be maximal and the finite blocks have no imposed cap.

The [final independent review]({OWN}/review-checked/SEMANTIC_REVIEW.md) freshly
rebuilt 19 modules at mathematical source `{args.source}` and audited 2,180
kernel-safe declarations, including 1,697 theorem constants. These are audit
coverage counts, not counts of new discoveries. The axiom union is `propext`,
`Classical.choice`, `Quot.sound`. Agent112's three unchanged original source
snapshots supply automatic admissibility; credit remains with Agent112. Their
scoped dependency review does not accept all of PR41. Earlier conditional
accounting and carry-budget layers retain their original hypotheses and credit.

The separate [Radix root]({OWN}/exterior-global/README.md), with a fresh
[four-module independent review]({OWN}/review-radix/REVIEW.md), rules out an
autonomous update and the specified overflow-strict monotone potentials based
only on the ordered observable `(phase,Z)`. Its repeated observation comes from
different actual exterior states; it is **not an exterior state cycle**.
The [bounded SAT exploration]({OWN}/exterior-global/search/README.md) retains
five `SOLVER_UNSAT_UNCERTIFIED` outcomes and three `UNKNOWN` outcomes. It supplies
no kernel-certified cycle or exclusion. No accepted certificate instance,
general exterior acyclicity theorem, infinite safe orbit, or proof of 196 is
claimed by this update.''')
    block('FINDINGS.md', f'''## Agent 110: exact accepted endpoints and evidence levels

Write `O = totalGam cert`, `Dg = totalG cert`, `Dh = totalH cert`, and `P = cert.P`.
The totals use the original raw formulas and certified trim counts; a local
signed gap increment may be negative. Six-phase membership is precisely
`{{2,4,8,16,14,10}}`.

| Endpoint or record | Hypotheses | Conclusion and scope |
|---|---|---|
| `Agent110.Checked.six_phase_constraints` | `check cert = true`; initial `SixPhase` | `O=2*(Dg+Dh)`; `Dg,Dh>=0`, each divisible by 9; `O>=18`, divisible by 18; `2*O<=P<=4*O`; `P%6=0`; `P>=42`. No separate admissibility, head positivity, arithmetic-budget, maximal-trim or width-cap premise. |
| `Agent110.Checked.saturated_period_constraints` | The preceding checker and phase premises; additionally `2*O=P` | `P%72=0` and `P>=72`. |
| `Agent110.Checked.period_at_least_four` | `check cert = true` only | `P>=4`, all phase classes. A two-phase lower bound of 12 is not established here. |
| `Agent110.RadixExterior.no_autonomous_radix_factor` | A proposed update on `(c,Z)` representing every exact step on canonical states reached after overflow | Contradiction: equal observations have different next observations. |
| `Agent110.RadixExterior.no_overflow_strict_radix_observable` and integer corollary | Potential depends only on `(c,Z)`; specified weak progress, strict progress at actual overflow and relation laws | Contradiction from a two-step observation return containing an overflow. The exterior states do not return. |
| Eight bounded exterior SAT runs | Exact recorded width/phase/period/overflow settings and short solver caps | Five unverified solver UNSAT reports and three UNKNOWN; no formal exclusion or cycle. |

[Checked semantic review]({OWN}/review-checked/SEMANTIC_REVIEW.md) discharges
the checker-to-arithmetic interface using Agent112's automatic-admissibility
theorem from three byte-exact dependency snapshots. Its independently rebuilt
19-module closure includes Agent4's existing saturation certificate; previous
conditional work is reused with attribution. The phase-padded three-column
prefix is an exact formal transition quantity, not an unconditional assertion
about physical prefix columns at gap two. [Radix review]({OWN}/review-radix/REVIEW.md)
is confined to its specified observable. Full exterior no-return remains open.''')
    block('REPRODUCE.md', f'''## Agent 110: registered All and Radix scopes

Use official Lean 4.19.0, release commit `6caaee842e94`, with an absolute
`LEAN_BIN` path. Each output/build path below must be new and nonexistent.
From the repository root:

```sh
python3 -B proofs/{OWN}/certificate-budget/check.py \\
  --lean "$LEAN_BIN" --build "$AGENT110_ALL_BUILD" --evidence "$AGENT110_ALL_EVIDENCE"
python3 -B proofs/{OWN}/exterior-global/check.py "$LEAN_BIN" \\
  --evidence "$AGENT110_RADIX_EVIDENCE"
```

| Registered scope | Import root | Fresh source closure | Accepted independent evidence |
|---|---|---:|---|
| All | `All` including `CertificateChecked` | 19 modules | [Manifest]({OWN}/review-checked/rebuild-d611d7f/manifest.json), [exact signatures]({OWN}/review-checked/Signatures.log) |
| Radix | `RadixExterior` | 4 modules | [Verification]({OWN}/review-radix/verification.json) and [review]({OWN}/review-radix/REVIEW.md) |

All is pinned to `{args.source}`. Radix is pinned to `{RADIX_SOURCE}` and source
SHA-256 `3aa5f400f939b7888a8e503cc1489514222701078449492f375681129c8e5716`.
The All audit enumerates every compiled kernel-safe declaration, including
private/generated theorems; compiler-only unsafe artifacts are inventoried
separately and do not enlarge the mathematical axiom whitelist. The Radix
review audits all 48 explicit public declarations across its four sources.
Both reviews use fresh project objects and the documented official compiler
with the recorded host readlink adapter; they do not claim separate toolchain
downloads. Review protocols and audit counts have these distinct scopes.

Agent112 dependency provenance is in
[PROVENANCE_CHECK.json]({OWN}/review-checked/PROVENANCE_CHECK.json): exactly
`AdmissibleCenters`, `SymbolicGrowth`, and `AdmissibleHeads` from original commit
`{AGENT112_SOURCE}`. No full-PR41 acceptance is inferred.
The earlier ten- and fifteen-module receipts and failed diagnostic attempts
remain historical evidence. The final nineteen-module receipt is accepted.

The [SAT runner and saved inputs]({OWN}/exterior-global/search/README.md) reproduce
bounded experiments only; no SAT UNSAT certificate was kernel checked.
Publication byte checks are separate from mathematics. After the integration
owner has staged all intended review/publication files and confirmed readiness:

```sh
python3 -B proofs/{REL}/reconcile.py --reconcile --stage-ready \\
  --baseline {args.baseline} \\
  --source {args.source} \\
  --claim {args.claim}
python3 -B proofs/verify_release.py
```

`--prepare-only` writes these scoped prose blocks without rebuilding indexes.
The reconciler performs read-only Git queries, rechecks source/log hashes and
retains historical inventory order and exact old bytes; it never stages or
commits files, runs Lean, or changes the existing byte verifier.''')
    block('PUBLICATION_SCOPE.md', f'''## Agent 110: PR39 scoped integration

Integration claim `{args.claim}` is limited to PR39, based on main
`{args.baseline}`. The accepted mathematical roots are All (19 modules) and
Radix (4 modules), with their exact source pins and independent review records
listed in [REPRODUCE.md](REPRODUCE.md). The three Agent112 original source
snapshots are preserved as attributed dependencies; this is not a merge or
acceptance of all of PR41. Agent116's existing publication and all earlier
conditional layers remain intact.

This is a reviewed integration candidate. Final main publication is recorded
by the integration owner after the confirmed merge, not inferred from these
local index files.

The author's [publication inventory]({OWN}/PUBLICATION.json) records retained
research and reproducible infrastructure exclusions. Sources, substantive
development failures, review/compiler/axiom logs, finite semantic controls,
search generators, compressed exact CNF inputs and solver logs retain their
stated evidence level. The eight exterior-only searches yielded five
`SOLVER_UNSAT_UNCERTIFIED` and three `UNKNOWN`, with zero SAT candidates or
kernel-verified cycles. They concern `(c,B)` exterior states, not the complete
`(c,B,A,C)` return certificate, so full-certificate overflow divisibility must
not silently be imposed on that search model.

The [incremental reconciler]({REL}/reconcile.py) preserves every historical
inventory row in order, including existing mixed TSV formats. If a historical
indexed path has changed, the exact old bytes are recovered from Git history
into this integration's archive before the current file receives a new row.
Existing archives remain unchanged. Current tracked/staged proof files receive
byte coverage; unrelated contributions gain no new mathematical endorsement.
Older aggregate statistics retain their historical scope. New scoped fields
register the two reviewed roots and the separate uncertified search evidence.

No proof-source or byte-verifier change is part of this reconciliation.
Reproducible objects, dependency-copy caches, toolchain binaries and Python
caches are outside the publication selection. The exact accepted wrappers are
necessary conditions, and the Radix result is an observable obstruction.
General exterior acyclicity, an accepted certificate instance and P196 remain
unproved here.''')
    reports = sorted(p[7:] for p in git('ls-files', 'proofs/' + OWN).decode().splitlines()
                     if p.endswith('.md'))
    # Review evidence can be inspected before the parent has staged it.
    reports = sorted(set(reports) | {str(p.relative_to(ROOT)) for p in (ROOT / OWN).glob('review-*/*.md')}
                     | {REL + '/notes.md'})
    block('REPORTS.md', '## Agent 110: certificate, radix, search and review reports\n\n' +
          '\n'.join(f'- [{p}]({p})' for p in reports))


def historical_bytes(path, expected):
    for commit in git('rev-list', '--all', '--', 'proofs/' + path).decode().splitlines():
        proc = subprocess.run(['git', 'show', commit + ':proofs/' + path], cwd=REPO, capture_output=True)
        if proc.returncode == 0 and sha(proc.stdout) == expected:
            return commit, proc.stdout
    raise RuntimeError('Cannot recover exact historical inventory bytes: ' + path)


def selected_paths():
    files = {p[7:] for p in git('ls-files', 'proofs').decode().splitlines()}
    files.update(str(p.relative_to(ROOT)) for p in HERE.rglob('*') if p.is_file())
    for name in files:
        assert (ROOT / name).is_file(), name
        assert not name.endswith(('.olean', '.ilean', '.pyc', '.so', '.o')), name
        assert '__pycache__' not in Path(name).parts, name
    return sorted(files)


def require_staged_publication():
    publication = OWN + '/PUBLICATION.json'
    assert (ROOT / publication).is_file(), 'Parent must prepare own PUBLICATION.json first'
    assert git('show', ':proofs/' + publication) == (ROOT / publication).read_bytes(), publication
    # Intended author/reviewer files must already match the index. Own generated
    # integration notes/index receipts are added after this selection freezes.
    for name in selected_paths():
        if name.startswith(OWN + '/') and (not name.startswith(REL + '/') or name.startswith(REL + '/merged-check/')):
            assert git('show', ':proofs/' + name) == (ROOT / name).read_bytes(), ('Not staged', name)
    needed = [OWN + '/review-checked/REVIEW_RESULT.json',
              OWN + '/review-checked/rebuild-d611d7f/manifest.json',
              OWN + '/review-radix/verification.json', publication]
    tracked = set(selected_paths())
    assert all(name in tracked for name in needed), 'Required review/publication is not staged'


def verify_merged_check(args):
    name = REL + '/merged-check/result.json'
    report = read(name)
    assert report['status'] == 'PASS'
    assert report['integrated_main_commit'] == args.baseline
    assert report['coordination_claim'] == args.claim and report['pull_request_scope'] == 39
    assert report['compared_source_count'] == 23 and report['recompiled_root_count'] == 3
    assert report['reused_dependency_object_count'] == 20 and report['endpoint_axiom_count'] == 18
    assert report['all_reviewed_source_pins_match_merge'] is True
    assert report['reviewed_dependencies_unchanged_after_use'] is True
    assert args.baseline in report['merge_parents']
    assert git('rev-parse', report['merge_commit'] + '^{tree}').decode().strip() == report['merge_tree']
    for rec in report['sources'].values():
        assert digest(REPO / rec['path']) == rec['reviewed_sha256'] == rec['merged_sha256']
        assert sha(git('show', report['merge_commit'] + ':' + rec['path'])) == rec['reviewed_sha256']
    for rec in report['independently_clean_closures'].values():
        assert digest(REPO / rec['receipt']) == rec['sha256']
    assert all(set(xs) <= ALLOWED for xs in report['endpoint_axiom_audit'].values())
    check_logs(report, REL + '/merged-check', 'exit_code')
    return {'result': name, 'sha256': digest(ROOT / name), 'status': 'PASS',
            'merge_commit': report['merge_commit'], 'merge_tree': report['merge_tree'],
            'compared_sources': 23, 'recompiled_roots': 3, 'endpoint_axiom_checks': 18,
            'reviewed_dependency_objects_reused': 20,
            'scope': 'Affected-root recompilation with explicit verified dependency reuse, not a fresh closure rebuild'}


def reconcile(args, evidence):
    merged = verify_merged_check(args)
    require_staged_publication()
    baseline = lambda name: git('show', args.baseline + ':proofs/' + name)
    records_base = json.loads(baseline('INVENTORY.json'))
    old_tsv = baseline('INVENTORY.tsv').decode()
    moved = []
    for record in records_base:
        if record['publication'] != 'retained':
            continue
        path = record['published_path']
        current = ROOT / path
        if current.is_file() and current.stat().st_size == record['bytes'] and digest(current) == record['sha256']:
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
        count = 0
        for i, line in enumerate(lines):
            fields = line.rstrip('\n').split('\t')
            if len(fields) == 7 and fields[2] == record['sha256'] and fields[6] == path:
                fields[6] = archive
                lines[i] = '\t'.join(fields) + '\n'
                count += 1
        assert count, ('Historical retained row has no matching TSV row', path)
        old_tsv = ''.join(lines)
    put(REL + '/index-reconciliation.json', {
        'baseline_commit': args.baseline, 'integration_claim': args.claim,
        'historical_inventory_records_preserved': len(records_base),
        'historical_tsv_field_counts': dict(collections.Counter(str(len(x.split('\t'))) for x in old_tsv.splitlines())),
        'relocated_historical_records': moved,
        'scope': 'Byte provenance only; earlier row order and archive bytes preserved; unrelated mathematics not re-reviewed'})
    stats_base = json.loads(baseline('release_stats.json'))
    validation_base = json.loads(baseline('VALIDATION.json'))
    log = HERE / 'release-integrity.log'
    log.write_text('{"status":"PENDING"}\n')
    previous = None
    for iteration in range(5):
        files = selected_paths()
        records = copy.deepcopy(records_base)
        known = {r['published_path'] for r in records if r['publication'] == 'retained'}
        added = []
        for name in files:
            if name in known or name in SHARED:
                continue
            own = name.startswith(OWN + '/')
            data = (ROOT / name).read_bytes()
            record = {'source_path': name, 'bytes': len(data), 'sha256': sha(data),
                'publication': 'retained', 'published_path': name,
                'reason': 'Agent110 scoped PR39 research, review or integration evidence' if own else
                          'Concurrent tracked byte coverage only; no mathematical review by Agent110',
                'family_report': OWN + '/PUBLICATION.json' if own else 'README.md',
                'source_snapshot': 'agent110-reviewed-pr39-20261015',
                'semantic_status': 'See exact source-specific review and hypotheses; searches remain uncertified' if own else
                                   'BYTE_INDEX_ONLY_NO_NEW_MATHEMATICAL_REVIEW'}
            records.append(record)
            added.append(record)
        put('INVENTORY.json', records)
        columns = ('source_path', 'bytes', 'sha256', 'publication', 'reason', 'family_report', 'published_path')
        (ROOT / 'INVENTORY.tsv').write_text(old_tsv.rstrip('\n') + '\n' +
            ''.join('\t'.join(str(r.get(k, '')) for k in columns) + '\n' for r in added))
        (ROOT / 'FILES.md').write_text('# Complete published file list\n\n'
            'Tracked/staged proof paths and retained integration notes. Byte coverage does not imply mathematical acceptance.\n\n' +
            ''.join(f'- [{name}]({name})\n' for name in files))
        own = [r for r in added if r['published_path'].startswith(OWN + '/')]
        update = {'mathematical_source_commit': args.source, 'integration_parent': args.baseline,
            'integration_claim': args.claim, 'accepted_scopes': {k: evidence[k] for k in ['All', 'Radix']},
            'merged_source_and_root_check': merged,
            'search_evidence': evidence['search'], 'agent112_dependency': evidence['agent112_dependency'],
            'retained_agent110_files_added': len(own), 'retained_agent110_bytes': sum(r['bytes'] for r in own),
            'concurrent_byte_only_records_added': len(added) - len(own),
            'current_unique_published_files': len(files), 'historical_records_preserved': len(records_base),
            'historical_records_relocated_without_byte_changes': len(moved),
            'earlier_aggregate_fields_are_historical': True}
        put('release_stats.json', dict(stats_base, agent110_pr39_update=update))
        put('VALIDATION.json', dict(validation_base, agent110_pr39_update={
            'mathematical_source_commit': args.source, 'independent_review': 'PASS',
            'accepted_scopes': {k: evidence[k] for k in ['All', 'Radix']},
            'merged_source_and_root_check': merged,
            'agent112_dependency': evidence['agent112_dependency'], 'search_evidence': evidence['search'],
            'release_integrity': previous or {'status': 'PENDING'},
            'release_integrity_record': REL + '/release-integrity.log',
            'unrelated_math_reaudited': False, 'mathematical_proof_check_by_release_verifier': False}))
        (ROOT / 'MANIFEST.sha256').write_text(''.join(
            f'{digest(ROOT / name)}  {name}\n' for name in files if name != 'MANIFEST.sha256'))
        proc = subprocess.run(['python3', '-B', str(ROOT / 'verify_release.py')], cwd=REPO, capture_output=True, text=True)
        if proc.returncode:
            (HERE / 'release-integrity-failure.log').write_text(proc.stdout + proc.stderr)
            raise RuntimeError(proc.stdout + proc.stderr)
        result = json.loads(proc.stdout)
        output = json.dumps({'command': 'python3 -B proofs/verify_release.py', 'exit_code': 0,
            'record_scope': 'Byte and source-presence check, not mathematics', 'result': result}, indent=2) + '\n'
        if previous == result and log.read_text() == output:
            print(json.dumps({'status': 'PASS', 'release_integrity': result,
                'historical_relocations': len(moved), 'iterations': iteration + 1}, indent=2))
            return
        previous = result
        log.write_text(output)
    raise RuntimeError('Release indexes did not stabilize')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument('--prepare-only', action='store_true')
    modes.add_argument('--reconcile', action='store_true')
    p.add_argument('--stage-ready', action='store_true', help='Only after integration owner confirms all intended files staged')
    p.add_argument('--baseline', default=DEFAULT_BASE)
    p.add_argument('--source', default=DEFAULT_SOURCE)
    p.add_argument('--claim', default=DEFAULT_CLAIM)
    args = p.parse_args()
    if args.reconcile and not args.stage_ready:
        p.error('--reconcile requires --stage-ready after explicit owner confirmation')
    for pin in [args.baseline, args.source, args.claim]:
        assert len(pin) == 40 and all(c in '0123456789abcdef' for c in pin), pin
    # No dynamically selected HEAD baseline: earlier Agent116 metadata stays pinned.
    assert git('rev-parse', args.baseline).decode().strip() == args.baseline
    evidence = verify_evidence(args)
    docs(args)
    if args.prepare_only:
        print(json.dumps({'status': 'PROSE_PREPARED', 'indexes_written': False,
                          'accepted_scopes': evidence, 'awaiting_stage_confirmation': True}, indent=2))
    else:
        reconcile(args, evidence)


if __name__ == '__main__':
    main()
