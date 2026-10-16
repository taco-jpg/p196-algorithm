#!/usr/bin/env python3
"""Expand a pinned source specification into an exact named audit inventory.

The public declaration scanner is reused from the explicitly pinned Agent105
checker. Its output must reproduce the independently retained name-set hash.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--spec', type=Path, required=True)
    p.add_argument('--early-root', type=Path, required=True)
    p.add_argument('--late-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.spec.read_text())
    roots = {'early': args.early_root, 'late': args.late_root}
    source = args.late_root / data['enumerator_path']
    if digest(source) != data['enumerator_sha256']:
        raise ValueError('Unexpected source enumerator.')
    spec = importlib.util.spec_from_file_location('pinned_declaration_scanner', source)
    scanner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scanner)
    names = []
    for item in data['modules']:
        path = roots[item['snapshot']] / item['path']
        if digest(path) != item['sha256']:
            raise ValueError('Unexpected source hash: ' + str(path))
        names.extend(d['name'] for d in scanner.public_theorems(path.read_text()))
    names.sort()
    if len(names) != len(set(names)) or len(names) != data['expected_theorem_count']:
        raise ValueError('Unexpected declaration count or repeated name.')
    if hashlib.sha256(('\n'.join(names)+'\n').encode()).hexdigest() != data['theorem_names_sha256']:
        raise ValueError('Declaration inventory differs from the retained audit.')
    if args.output.exists():
        raise ValueError('Manifest output must not already exist.')
    data['theorem_names'] = names
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print('Manifest PASS:', len(data['modules']), 'sources;', len(names), 'names')


if __name__ == '__main__':
    main()
