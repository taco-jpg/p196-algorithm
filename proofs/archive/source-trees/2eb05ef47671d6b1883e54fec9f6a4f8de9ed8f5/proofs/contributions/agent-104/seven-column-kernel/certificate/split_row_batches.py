#!/usr/bin/env python3
"""Split resource-heavy row blocks into small checked lemmas, preserving targets.

The wrapper retains exactly the original checked_leaf and row_branch statements.
Its tuple proofs are checked against the original stored tree by Lean.
"""
import json
from pathlib import Path
import sys

here = Path(__file__).resolve().parent
layout = json.loads((here / 'rank739-layout.json').read_text())
header = ('namespace SevenColumn.Certificate739\nopen Certificate\n'
          'set_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n')
word = lambda w: '[' + ','.join(map(str, w)) + ']'
history = here / 'unsplit-history'
history.mkdir(exist_ok=True)
manifest_path = here / 'split-batches.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
for batch in map(int, sys.argv[1:]):
    name = f'Rows739_{batch:03d}'
    original = here / (name + '.lean')
    if not (history / original.name).exists():
        (history / original.name).write_bytes(original.read_bytes())
    leaves = layout['leaves'][batch*4:batch*4+4]
    modules = []
    for leaf in leaves:
        for start in range(0, len(leaf['rows']), 14):
            module = f'{name}_{leaf["name"]}_{start//14}'
            modules.append(module)
            text = 'import Rank739\nimport FastRowsBase\n' + header
            for j, row in enumerate(leaf['rows'][start:start+14], start):
                text += (f'theorem row_{leaf["name"]}_{j} : checkRow ranks (fastLongPred 7) '
                         f'{word(row["word"])} {row["rank"]} = true := by decide +kernel\n')
            text += 'end SevenColumn.Certificate739\n'
            (here / (module + '.lean')).write_text(text)
    wrapper = ''.join('import ' + m + '\n' for m in modules) + header
    def tree_proof(leaf, lo, hi):
        if lo == hi:
            return 'True.intro'
        mid = (lo + hi) // 2
        return (f'⟨{tree_proof(leaf, lo, mid)}, row_{leaf}_{mid}, '
                f'{tree_proof(leaf, mid+1, hi)}⟩')
    for leaf in leaves:
        wrapper += (f'theorem checked_{leaf["name"]} : {leaf["name"]}.All '
                    '(fun p r => checkRow ranks (fastLongPred 7) p r = true) :=\n  '
                    + tree_proof(leaf['name'], 0, len(leaf['rows'])) + '\n')
    for branch in layout['interiors'][batch*4:batch*4+4]:
        row = branch['row']
        wrapper += (f'theorem row_{branch["name"]} : checkRow ranks (fastLongPred 7) '
                    f'{word(row["word"])} {row["rank"]} = true := by decide +kernel\n')
    wrapper += 'end SevenColumn.Certificate739\n'
    original.write_text(wrapper)
    manifest[name] = modules
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({k:len(v) for k,v in manifest.items()}))
