#!/usr/bin/env python3
"""Check that every v2 JobData module denotes the same tables as the original.

Independent of both generators: parses the emitted Lean `def NAME (i : Nat) : Nat := EXPR`
lines (EXPR built only from `if i < K then X else Y`, literals and calls `NAME_cK i`),
evaluates each table at every index 0..N+16 in both files, and requires all other
lines (non-table definitions) to be byte-identical.
"""
import hashlib, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG = HERE.parents[4] / 'proofs/contributions/2026-10-15-scalar-finite-certificate-formal/generated'
DEF = re.compile(r'^def (\w+) \(i : Nat\) : Nat := (.*)$')


def tokenize(e):
    return re.findall(r'\(|\)|<|if|then|else|\w+', e)


def parse(tokens, pos):
    t = tokens[pos]
    if t == '(':
        node, pos = parse(tokens, pos + 1)
        assert tokens[pos] == ')'
        return node, pos + 1
    if t == 'if':
        assert tokens[pos + 1] == 'i' and tokens[pos + 2] == '<'
        k = int(tokens[pos + 3]); assert tokens[pos + 4] == 'then'
        a, pos = parse(tokens, pos + 5); assert tokens[pos] == 'else'
        b, pos = parse(tokens, pos + 1)
        return ('if', k, a, b), pos
    if t.isdigit():
        return ('lit', int(t)), pos + 1
    assert re.fullmatch(r'\w+', t) and tokens[pos + 1] == 'i', (t, tokens[pos:pos + 3])
    return ('call', t), pos + 2


def load(path):
    defs, other = {}, []
    for line in path.read_text().split('\n'):
        m = DEF.match(line)
        if m:
            tokens = tokenize(m.group(2)); node, end = parse(tokens, 0)
            assert end == len(tokens), (path, m.group(1))
            defs[m.group(1)] = node
        else:
            other.append(line)
    return defs, other


def evaluate(defs, node, i):
    while True:
        if node[0] == 'lit': return node[1]
        if node[0] == 'call': node = defs[node[1]]; continue
        node = node[2] if i < node[1] else node[3]


def bound(node):
    assert node[0] == 'if'; return node[1]


report = []
for n in range(16):
    od, oo = load(ORIG / f'JobData{n}.lean')
    vd, vo = load(HERE / 'generated' / f'JobData{n}.lean')
    assert oo == vo, f'non-table text differs in JobData{n}'
    tables = sorted(k for k in od if od[k][0] == 'if')
    aliases = sorted(k for k in od if od[k][0] != 'if')
    assert set(vd) == set(od) | {k for k in vd if re.fullmatch(r'\w+_c\d+', k)}, n
    for a in aliases:
        assert od[a] == vd[a], (n, a)
    checked = 0
    for t in tables:
        N = bound(od[t]); assert bound(vd[t]) == N, (n, t)
        for i in range(N + 17):
            assert evaluate(od, od[t], i) == evaluate(vd, vd[t], i), (n, t, i)
        checked += N + 17
    report.append(dict(job=n, tables=tables, aliases=aliases, evaluations=checked,
                       original_sha256=hashlib.sha256((ORIG / f'JobData{n}.lean').read_bytes()).hexdigest(),
                       v2_sha256=hashlib.sha256((HERE / 'generated' / f'JobData{n}.lean').read_bytes()).hexdigest()))
    print(n, len(tables), checked, flush=True)
out = dict(status='PASS', total_evaluations=sum(r['evaluations'] for r in report), jobs=report,
           scope='Original and v2 emitted tables agree at every index 0..N+16; all non-table lines identical.')
(HERE / 'v2_equivalence.json').write_text(json.dumps(out, indent=2) + '\n')
print(out['status'], out['total_evaluations'])
