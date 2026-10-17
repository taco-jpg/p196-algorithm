#!/usr/bin/env python3
"""Validate this bounded documentation change without compiling Lean or replaying the project."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

PIN = '10a173cb635fa8d03e357f454232816fc3e77609'
BASE = '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5'
PACKAGE = 'proofs/contributions/agent-61/documentation-20261016'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--increment', choices=['findings', 'complete'], required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()

    def git(*command):
        return subprocess.check_output(['git', '-C', str(repo), *command])

    trees = {}

    def tree(ref):
        if ref not in trees:
            entries = {}
            for line in git('ls-tree', '-r', '-t', ref).decode().splitlines():
                meta, path = line.split('\t', 1)
                mode, kind, oid = meta.split()
                entries[path] = {'mode': mode, 'kind': kind, 'oid': oid}
            trees[ref] = entries
        return trees[ref]

    originals = json.loads(git('show', f'{PIN}:proofs/SOURCE_MAP.json'))
    current = json.loads((repo / 'proofs/SOURCE_MAP.json').read_text())
    docs = ['proofs/FINDINGS.md']
    if args.increment == 'complete':
        docs.append('proofs/CONSOLIDATION.md')
    assert current.keys() == originals.keys()
    assert current['base'] == originals['base'] == BASE
    assert current['paths'].keys() == originals['paths'].keys()
    changed_fields = []
    effective = []
    for original_path, old in originals['paths'].items():
        new = current['paths'][original_path]
        expected = dict(old)
        if original_path in docs:
            assert old['current'] == original_path
            expected['current'] = None
            changed_fields.append({'original_path': original_path, 'field': 'current', 'old': old['current'], 'new': None})
        assert new == expected, ('unexpected map mutation', original_path)
        old_selected = old.get('current') or old['preserved']
        new_selected = new.get('current') or new['preserved']
        a, b = tree(PIN)[old_selected], tree(PIN)[new_selected]
        assert a['oid'] == b['oid'] == old['oid'], original_path
        assert a['mode'] == b['mode'] == old['mode'], original_path
        effective.append((original_path, b['mode'], b['oid']))

    preserved = []
    for doc in docs:
        original = git('show', f'{PIN}:{doc}')
        record = originals['paths'][doc]
        retained = git('cat-file', 'blob', tree(PIN)[record['preserved']]['oid'])
        archive_path = f'proofs/archive/documentation/agent-61/{PIN}/{Path(doc).name}'
        assert (repo / archive_path).read_bytes() == original == retained
        assert hashlib.sha256(original).hexdigest() == record['sha256']
        preserved.append({'path': doc, 'bytes': len(original), 'sha256': record['sha256'], 'git_blob': record['oid'], 'archive': archive_path})

    historical_checks = {}
    for doc in docs:
        name = Path(doc).stem
        text = (repo / doc).read_text()
        marker = f'<!-- BEGIN HISTORICAL {name}: {BASE} -->\n\n'
        body = text.split(marker, 1)[1]
        parts = re.split(r'\n<!-- END HISTORICAL ' + name + r'(?:: ' + BASE + r')? -->', body, maxsplit=1)
        assert len(parts) == 2, ('missing historical end marker', doc)
        historical = parts[0]
        rewrites = json.loads((repo / PACKAGE / f'{name.lower()}-link-rewrites.json').read_text())['links']
        inverse = {x['pinned']: x['original'] for x in rewrites}
        historical = re.sub(r'\[([^\]]*)\]\(([^\s)]+)\)', lambda m: f'[{m[1]}]({inverse.get(m[2], m[2])})', historical)
        historical = re.sub(r'^#(#{1,5}) ', r'\1 ', historical, flags=re.M)
        assert historical.encode() == git('show', f'{PIN}:{doc}'), ('historical prose changed', doc)
        historical_checks[doc] = {'original_bytes_restored_by_inverse': True, 'links_repaired': len(rewrites)}

    links_checked = []
    for doc in docs:
        text = (repo / doc).read_text()
        for _, target in re.findall(r'\[([^\]]*)\]\(([^\s)]+)\)', text):
            uri = urlsplit(target)
            if uri.scheme:
                if uri.netloc != 'github.com':
                    continue
                match = re.fullmatch(r'/taco-jpg/p196-algorithm/(blob|tree)/([0-9a-f]{40})/(.+)', unquote(uri.path))
                if not match:
                    continue
                kind, ref, path = match.groups()
                entry = tree(ref).get(path.rstrip('/'))
                assert entry is not None, (doc, target)
                assert (entry['kind'] == 'tree') == (kind == 'tree'), (doc, target)
                if uri.fragment.startswith('L'):
                    line_match = re.fullmatch(r'L(\d+)(?:-L(\d+))?', uri.fragment)
                    assert line_match, target
                    limit = int(line_match[2] or line_match[1])
                    assert int(line_match[1]) <= limit
                    data = git('cat-file', 'blob', entry['oid'])
                    assert limit <= len(data.splitlines()), target
                links_checked.append({'document': doc, 'target': target, 'git_blob_or_tree': entry['oid']})
            elif not target.startswith('#'):
                local = (repo / doc).parent / unquote(uri.path)
                relative = local.resolve().relative_to(repo).as_posix()
                assert relative in tree(PIN) or local.is_file(), (doc, target)
                links_checked.append({'document': doc, 'target': target, 'relative_path': relative})

    registry = json.loads((repo / 'proofs/Agent1PeriodicPhaseCatalog.registry.json').read_text())
    modules = registry['projects']['agent1-periodic-phase-catalog']['modules']
    for name, item in modules.items():
        source = (repo / item['path']).read_bytes()
        assert hashlib.sha256(source).hexdigest() == item['sha256'], name
        assert tree(PIN)[item['path']]['oid'] == item['git_blob'], name
    for path, oid in [('proofs/DifferenceObservability__dc8ff21a6bd34973.lean', 'd0727d391ee901ddaa782c218f493a23b8aadff3'), ('proofs/TwoDigitMain__ebb172c52d262b85.lean', '460096733d4ac9145371d63421b400f56e7090d5')]:
        assert tree(PIN)[path]['oid'] == oid
        assert (repo / path).read_bytes() == git('cat-file', 'blob', oid)

    changed = git('diff', '--name-only', PIN).decode().splitlines()
    allowed = set(docs + ['proofs/SOURCE_MAP.json'])
    for path in changed:
        assert path in allowed or path.startswith(PACKAGE + '/') or path.startswith(f'proofs/archive/documentation/agent-61/{PIN}/'), path
    git('diff', '--check')
    hashes = {path: hashlib.sha256((repo / path).read_bytes()).hexdigest() for path in docs + ['proofs/SOURCE_MAP.json']}
    print(json.dumps({
        'status': 'PASS', 'verification': 'DOCUMENTATION_AND_REPLAY_INPUT_IDENTITY_ONLY',
        'source_commit': PIN, 'historical_baseline': BASE, 'increment': args.increment,
        'source_map_entries_checked': len(effective), 'effective_replay_git_identities_unchanged': len(effective),
        'effective_replay_identity_digest': hashlib.sha256(json.dumps(effective, separators=(',', ':')).encode()).hexdigest(),
        'map_fields_changed': changed_fields, 'originals_preserved': preserved,
        'historical_findings_prose_unchanged_except_heading_depth_and_link_destinations': True,
        'historical_findings_links_repaired': historical_checks['proofs/FINDINGS.md']['links_repaired'],
        'historical_documents': historical_checks, 'document_links_checked': len(links_checked),
        'phase_catalog_module_source_hashes_checked': len(modules),
        'current_file_sha256': hashes, 'tracked_changed_paths': changed,
        'lean_execution': 'NOT_RUN', 'actual_original_layout_replay': 'NOT_RUN',
        'scope_limit': 'Complete mapping compared through exact Git blob/mode identities; only changed documents and selected mathematical sources reread as bytes. No full repository theorem or preservation replay.',
        'link_checks': links_checked,
    }, indent=2))


if __name__ == '__main__':
    main()
