#!/usr/bin/env python3
"""Read-only integration acceptance checks; emit JSON, never rewrite indexes."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PROOFS = REPO / 'proofs'
OWN = PROOFS / 'contributions/agent-110'
BASE = '2c2551165c13d23b11d44122fc7a504d51053e59'
PRIOR = '069e139e9d1bf6fcfdb4fc10ec25982536759ae3'
CERT = 'eb4817f0973cbbe2a059af33d5dc53877a5275b7'
RADIX = '1cdc55c89b376faa270d1dffaf21e21b6eedeb4b'
MERGE = 'b337ce1e3c3058468bc1562bf30e536f685960dd'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
PINS = {
    'proofs/contributions/agent-110/README.md': '7cf5fa7fe4285dfcdca3dd798974fa190d2b2e36143a2c86092d87ff4580565b',
    'proofs/contributions/agent-110/certificate-budget/README.md': 'e6100362c5eb3bb55f1e355cd6f817e6b809ac9e332012863bd9b8929a6c8bdf',
    'proofs/contributions/agent-110/integration/reconcile.py': '71416a2b8a2a994c943e481840b3e219c3fce63e704b3be40667c60e960cccb4',
    'proofs/contributions/agent-110/publication.py': 'a9823c1464a53204dadb6fc7a1de033a94dbbe39864f7d8f20c805bb6be204f8',
    'proofs/verify_release.py': '5aa24fd9e8cb5265d1f2e4ccbc74b704d22c734dcdd623a537a5ec1d3bb9312b',
    'proofs/contributions/agent-110/integration/merged-check/check.py': '09df562dd87eab4c8f4955640cab0a1b7851ebb9a67356b6d8538322b5c84977',
    'proofs/contributions/agent-110/integration/merged-check/result.json': '268959d1baddfc985fec42ba480216cdbc3b62dcbb59025aaad9cf8f0a81800e',
    'proofs/contributions/agent-110/review/independent_rebuild.py': 'ebaa8b5fd88fc168f8245c51dac203760d6d3f475fa6ec5063e8ba74cd6849e6',
    'proofs/contributions/agent-110/review-checked/REVIEW_RESULT.json': '3c8f1cc7c64250a67e27bad5504c0ea8761ef079f8dc81faca6e627c591374a3',
    'proofs/contributions/agent-110/review-checked/rebuild-d611d7f/manifest.json': '1a03fa46d6ab20224be224ef50bd7664af87e616a2643c963f2078c1add98906',
    'proofs/contributions/agent-110/review-radix/verification.json': '81851617ff0edcff9204df273cd97ca4714fc6c5ebe89382ae4a6c5927282b1f',
}


def digest(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def read(p):
    return json.loads(p.read_bytes())


def main():
    for p, expected in PINS.items():
        assert digest((REPO / p).read_bytes()) == expected, ('Pinned input changed', p)
    merge = read(OWN / 'integration/merged-check/result.json')
    assert merge['status'] == 'PASS'
    assert merge['merge_commit'] == MERGE
    assert BASE in git('show', '-s', '--format=%P', MERGE).decode().split()
    assert merge['merge_tree'] == git('rev-parse', MERGE + '^{tree}').decode().strip()
    assert len(merge['sources']) == 23
    assert len(merge['dependency_objects_reused']) == 20
    assert merge['roots_recompiled'] == ['CertificateChecked', 'All', 'RadixExterior']
    assert len(merge['endpoint_axiom_audit']) == 18
    assert all(set(xs) <= ALLOWED for xs in merge['endpoint_axiom_audit'].values())
    for name, rec in merge['sources'].items():
        data = (REPO / rec['path']).read_bytes()
        source = CERT if rec['closure'] == 'certificate_19' else RADIX
        assert rec['published_source_commit'] == source
        assert digest(data) == rec['reviewed_sha256'] == rec['merged_sha256']
        assert data == git('show', source + ':' + rec['path'])
        assert data == git('show', MERGE + ':' + rec['path'])
    for cmd in merge['commands']:
        assert cmd['exit_code'] == 0
        assert digest((OWN / 'integration/merged-check' / cmd['log']).read_bytes()) == cmd['log_sha256']
    for closure in merge['independently_clean_closures'].values():
        assert closure['status'] == 'PASS' and closure['objects_reused_in_that_run'] is False
        assert digest((REPO / closure['receipt']).read_bytes()) == closure['sha256']

    # Historical research and review evidence remains byte-identical. The two
    # exact pinned README changes only update integration/remaining-work prose.
    prior_paths = git('ls-tree', '-r', '--name-only', PRIOR, '--',
                      'proofs/contributions/agent-110').decode().splitlines()
    assert prior_paths
    updated_prose = {'proofs/contributions/agent-110/README.md',
                     'proofs/contributions/agent-110/certificate-budget/README.md'}
    for p in prior_paths:
        if p in updated_prose:
            continue
        assert (REPO / p).read_bytes() == git('show', PRIOR + ':' + p), ('Prior evidence changed', p)

    old = json.loads(git('show', BASE + ':proofs/INVENTORY.json'))
    current = read(PROOFS / 'INVENTORY.json')
    assert len(old) == 8886 and current[:len(old)] == old
    old_tsv = git('show', BASE + ':proofs/INVENTORY.tsv')
    assert (PROOFS / 'INVENTORY.tsv').read_bytes().startswith(old_tsv)
    for f in ['release_stats.json', 'VALIDATION.json']:
        before = json.loads(git('show', BASE + ':proofs/' + f))
        after = read(PROOFS / f)
        assert all(after.get(k) == v for k, v in before.items()), f
        scope = after['agent110_pr39_update']
        assert scope['accepted_scopes']['All']['module_count'] == 19
        assert scope['accepted_scopes']['Radix']['module_count'] == 4
        assert scope['agent112_dependency']['full_PR41_accepted'] is False
        assert scope['search_evidence']['kernel_verified_cycles'] == 0
    reconciliation = read(OWN / 'integration/index-reconciliation.json')
    assert reconciliation['relocated_historical_records'] == []
    assert reconciliation['historical_inventory_records_preserved'] == len(old)
    for f in ['README.md', 'FINDINGS.md', 'REPRODUCE.md', 'PUBLICATION_SCOPE.md', 'REPORTS.md']:
        text = (PROOFS / f).read_text()
        begin, end = '<!-- BEGIN AGENT110 REVIEWED PR39 -->', '<!-- END AGENT110 REVIEWED PR39 -->'
        assert text.count(begin) == text.count(end) == 1
        outside = text[:text.index(begin)] + text[text.index(end) + len(end):]
        assert outside.strip() == git('show', BASE + ':proofs/' + f).decode().strip(), f
    assert (PROOFS / 'verify_release.py').read_bytes() == git('show', BASE + ':proofs/verify_release.py')
    old_manifest_paths = {line.split('  ', 1)[1] for line in git('show', BASE + ':proofs/MANIFEST.sha256').decode().splitlines()}
    new_manifest_paths = {line.split('  ', 1)[1] for line in (PROOFS / 'MANIFEST.sha256').read_text().splitlines()}
    assert old_manifest_paths <= new_manifest_paths

    # Validate the nested contribution inventory in addition to the legacy
    # outer release verifier, which does not interpret PUBLICATION.json.
    publication = read(OWN / 'PUBLICATION.json')
    retained = publication['retained']
    assert len({r['path'] for r in retained}) == len(retained)
    for rec in retained:
        data = (OWN / rec['path']).read_bytes()
        assert len(data) == rec['bytes'] and digest(data) == rec['sha256'], rec['path']
    outputs = {'PUBLICATION.json', 'SHA256SUMS'}
    prefix = 'proofs/contributions/agent-110/'
    selected = {p[len(prefix):] for p in git('ls-files', '--', prefix).decode().splitlines()}
    assert {r['path'] for r in retained} == selected - outputs
    assert (OWN / 'SHA256SUMS').read_text() == ''.join(r['sha256'] + '  ' + r['path'] + '\n' for r in retained)
    assert publication['retained_file_count_excluding_inventory_outputs'] == len(retained)
    assert publication['retained_bytes_excluding_inventory_outputs'] == sum(r['bytes'] for r in retained)
    assert publication['research_omissions'] == []
    search = read(OWN / 'exterior-global/search/summary.json')
    assert Counter(x['status'] for x in search['runs']) == {'SOLVER_UNSAT_UNCERTIFIED': 5, 'UNKNOWN': 3}
    assert search['sat_candidates'] == search['kernel_verified_cycles'] == 0
    proc = subprocess.run(['python3', '-B', 'proofs/verify_release.py'], cwd=REPO,
                          text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    release = json.loads(proc.stdout)
    assert release['status'] == 'PASS' and release['mathematical_proof_check'] is False
    print(json.dumps({
        'status': 'PASS',
        'scope': 'Read-only packaging/integration review; no new Lean build or additional mathematical acceptance',
        'baseline_commit': BASE, 'previous_accepted_publication': PRIOR,
        'source_pins': {'certificate_19': CERT, 'radix_4': RADIX},
        'pinned_inputs': PINS,
        'mathematical_sources_unchanged': 23,
        'historical_contribution_files_byte_preserved': len(prior_paths) - len(updated_prose),
        'reviewed_pinned_integration_prose_updates': sorted(updated_prose),
        'merged_check': {'roots_recompiled': 3, 'dependencies_explicitly_reused': 20, 'endpoint_axioms': 18},
        'historical_inventory_records_byte_preserved_in_order': len(old),
        'historical_tsv_is_exact_byte_prefix': True,
        'historical_stats_and_validation_fields_unchanged': True,
        'historical_manifest_paths_preserved': len(old_manifest_paths),
        'historical_bytes_relocated': 0,
        'shared_prose_outside_scoped_additions_unchanged': True,
        'own_publication_files_verified': len(retained),
        'own_publication_bytes_verified': sum(r['bytes'] for r in retained),
        'legacy_verifier_unchanged': True,
        'release_verifier': release,
        'self_reference_policy': 'No full current-tree, publication-inventory or release-manifest hash is recorded; final metadata refresh is followed by read-only rerun.'
    }, ensure_ascii=False, indent=2) + '\n', end='')


if __name__ == '__main__':
    main()
