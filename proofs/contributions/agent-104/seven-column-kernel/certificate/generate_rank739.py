#!/usr/bin/env python3
"""Emit untrusted data and kernel-decide proof obligations for certificate 739.

No proof is inferred from JSON metadata. Every generated lookup verifies its
stored word; closure proofs run the complete Lean inverse, not the Python list.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / '2026-10-15-seven-column-prefix' / 'certificate_739.json'
VERIFY = SOURCE.with_name('verify_certificates.py')


def code(w):
    n = 1
    for d in w:
        n = 19 * n + d
    return n


def word(w):
    return '[' + ','.join(map(str, w)) + ']'


def main():
    cert = json.loads(SOURCE.read_text())
    nodes = sorted(cert['nodes'], key=lambda n: code(n['word']))
    assert len({tuple(n['word']) for n in nodes}) == len(nodes)
    assert len({code(n['word']) for n in nodes}) == len(nodes)
    spec = importlib.util.spec_from_file_location('verify739', VERIFY)
    verify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verify)
    definitions, leaves, interiors = [], [], []

    def expr(ns):
        if not ns:
            return '.empty'
        m = len(ns) // 2
        n = ns[m]
        return f'(.node {code(n["word"])} {word(n["word"])} {n["rank"]} {expr(ns[:m])} {expr(ns[m+1:])})'

    def build(ns):
        if len(ns) <= 64:
            name = f'leaf{len(leaves):04d}'
            leaves.append({'name': name, 'count': len(ns), 'rows': ns})
            definitions.append(f'def {name} : RankTree := {expr(ns)}')
            return name
        m = len(ns) // 2
        left, right = build(ns[:m]), build(ns[m+1:])
        name = f'branch{len(interiors):04d}'
        n = ns[m]
        interiors.append({'name': name, 'left': left, 'right': right, 'row': n})
        definitions.append(f'def {name} : RankTree := .node {code(n["word"])} {word(n["word"])} {n["rank"]} {left} {right}')
        return name

    root = build(nodes)
    header = 'import PrefixCertificate\n\nnamespace SevenColumn.Certificate739\nopen Certificate\nset_option maxRecDepth 10000\n'
    chunks = [definitions[i:i+128] for i in range(0,len(definitions),128)]
    for i,chunk in enumerate(chunks):
        module = f'Rank739Data{i:02d}'
        previous = 'PrefixCertificate' if i == 0 else f'Rank739Data{i-1:02d}'
        (HERE / f'{module}.lean').write_text(header.replace('import PrefixCertificate',f'import {previous}') + '\n'.join(chunk) + '\nend SevenColumn.Certificate739\n')
    (HERE / 'Rank739.lean').write_text(header.replace('import PrefixCertificate',f'import Rank739Data{len(chunks)-1:02d}') + f'\ndef ranks : RankTree := {root}\ndef rank (w : List Nat) : Option Nat := lookup ranks w\nend SevenColumn.Certificate739\n')
    samples = [nodes[0], max(nodes, key=lambda n:n['rank']), nodes[-1]]
    long_nodes = [n for n in nodes if len(n['word']) == 7]
    max_degree = max(long_nodes, key=lambda n:len(verify.prefix_predecessors(tuple(n['word']))))
    samples.append(max_degree)
    pilot = 'import Rank739\nimport FastInverse\nnamespace SevenColumn.Certificate739\nopen Certificate\nset_option maxRecDepth 100000\nset_option maxHeartbeats 10000000\n'
    pilot += 'def fastLongPred (p : List Nat) : List (List Nat) := if p.length = 7 then fastPrefixPredecessors p else []\n'
    for i,n in enumerate(samples):
        pilot += f'theorem pilot{i} : checkRow ranks fastLongPred {word(n["word"])} {n["rank"]} = true := by decide\n#print axioms pilot{i}\n'
    pilot += 'end SevenColumn.Certificate739\n'
    (HERE / 'Pilot739.lean').write_text(pilot)
    metadata = {
        'source':str(SOURCE.relative_to(HERE.parents[4])),
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'nodes':len(nodes), 'root':root,
        'leaves':leaves, 'interiors':interiors,
        'pilot_rows':[{'word':n['word'],'rank':n['rank'],'degree':len(verify.prefix_predecessors(tuple(n['word']))) if len(n['word'])==7 else 0} for n in samples],
    }
    (HERE / 'rank739-layout.json').write_text(json.dumps(metadata, separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in metadata.items() if k not in ('leaves','interiors')},indent=2))


if __name__ == '__main__':
    main()
