#!/usr/bin/env python3
"""Emit untrusted Lean data and kernel-decide obligations for one prefix certificate.

Usage: python3 generate_instance.py PREFIX [--leaf N] [--leaves-per-module N] [--split-cost N]

Reads the frozen proofs/contributions/2026-10-15-seven-column-prefix/certificate_PREFIX.json
(its SHA256 must match that directory's SHA256SUMS.txt) and writes cert<PREFIX>/ next to this
script. Nothing here is a proof: every emitted obligation is re-checked by the Lean kernel
against the complete executable inverse (`fastLongPred 7`), the exact short update
(`nextWord`) and the full lookup (`lookup` compares whole words). The layout, the cost
model and the batching are performance choices only.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # never leave caches in the frozen source directory

HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE.parents[1] / '2026-10-15-seven-column-prefix'


def code(w):
    n = 1
    for d in w:
        n = 19 * n + d
    return n


def word(w):
    return '[' + ','.join(map(str, w)) + ']'


def load_verifier():
    import importlib.util
    spec = importlib.util.spec_from_file_location('vc', SOURCE_DIR / 'verify_certificates.py')
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)
    return vc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('prefix')
    ap.add_argument('--leaf', type=int, default=64, help='maximum nodes per leaf subtree')
    ap.add_argument('--leaves-per-module', type=int, default=4)
    ap.add_argument('--split-cost', type=int, default=400,
                    help='leaves whose predicted cost exceeds this are checked row by row')
    ap.add_argument('--module-cost', type=int, default=900,
                    help='predicted cost budget per row module')
    a = ap.parse_args()
    P = a.prefix
    assert len(P) == 3 and P.isdigit() and int(P[0]) >= 2, P
    src = SOURCE_DIR / f'certificate_{P}.json'
    blob = src.read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    sums = dict(line.split()[::-1] for line in (SOURCE_DIR / 'SHA256SUMS.txt').read_text().splitlines() if line.strip())
    assert sums[src.name] == digest, ('frozen certificate hash mismatch', src.name)
    cert = json.loads(blob)
    assert cert['width'] == 7 and cert['prefix'] == P
    abc = list(map(int, P))
    rank_of = {tuple(n['word']): n['rank'] for n in cert['nodes']}
    assert len(rank_of) == len(cert['nodes'])
    bound = max(rank_of[tuple(p)] for p in cert['initial'])
    assert cert['palindrome_height_bound'] == bound + 1
    H = bound + 1
    assert H <= 100
    nodes = sorted(cert['nodes'], key=lambda n: code(n['word']))
    assert len({code(n['word']) for n in nodes}) == len(nodes)
    vc = load_verifier()
    def cost(n):
        w = tuple(n['word'])
        return 1 + (len(vc.prefix_predecessors(w)) if len(w) == 7 else 0)

    out = HERE / f'cert{P}'
    out.mkdir(exist_ok=True)
    ns_data = f'Agent118.Cert{P}'
    header_data = f'namespace {ns_data}\nopen SevenColumn.Certificate\nset_option maxRecDepth 10000\n'

    definitions, leaves, interiors = [], [], []

    def expr(ns):
        if not ns:
            return '.empty'
        m = len(ns) // 2
        n = ns[m]
        return f'(.node {code(n["word"])} {word(n["word"])} {n["rank"]} {expr(ns[:m])} {expr(ns[m+1:])})'

    def build(ns):
        if len(ns) <= a.leaf:
            name = f'leaf{len(leaves):04d}'
            leaves.append({'name': name, 'rows': ns, 'cost': sum(cost(n) for n in ns)})
            definitions.append(f'def {name} : RankTree := {expr(ns)}')
            return name
        m = len(ns) // 2
        left, right = build(ns[:m]), build(ns[m + 1:])
        name = f'branch{len(interiors):04d}'
        n = ns[m]
        interiors.append({'name': name, 'left': left, 'right': right, 'row': n, 'cost': cost(n)})
        definitions.append(f'def {name} : RankTree := .node {code(n["word"])} {word(n["word"])} {n["rank"]} {left} {right}')
        return name

    root = build(nodes)
    data_modules = []
    chunks = [definitions[i:i + 128] for i in range(0, len(definitions), 128)]
    for i, chunk in enumerate(chunks):
        mod = f'Rank{P}Data{i:02d}'
        prev = 'PrefixCertificate' if i == 0 else f'Rank{P}Data{i-1:02d}'
        (out / f'{mod}.lean').write_text(f'import {prev}\n\n' + header_data + '\n'.join(chunk) + f'\nend {ns_data}\n')
        data_modules.append(mod)
    (out / f'Rank{P}.lean').write_text(
        f'import {data_modules[-1]}\n\n' + header_data +
        f'\n/-- Untrusted certificate data; every use is re-checked. -/\ndef ranks : RankTree := {root}\nend {ns_data}\n')

    # ---- rows: leaves via one boolean traversal each, heavy leaves row by row ----
    hdr = (f'namespace {ns_data}\nopen SevenColumn.Certificate Agent118.PrefixKernel\n'
           'set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n')
    pred = 'fastLongPred 7'
    row_modules, cur, cur_cost = [], [], 0
    leaf_proof = {}
    items = []
    for i, leaf in enumerate(leaves):
        items.append(('leaf', leaf))
        if i < len(interiors):
            items.append(('branch', interiors[i]))

    def flush():
        nonlocal cur, cur_cost
        if not cur:
            return
        mod = f'Rows{P}_{len(row_modules):03d}'
        text = f'import Rank{P}\nimport PrefixChecksBase\n' + hdr
        text += ''.join(cur) + f'end {ns_data}\n'
        (out / f'{mod}.lean').write_text(text)
        row_modules.append(mod)
        cur, cur_cost = [], 0

    for kind, it in items:
        if kind == 'leaf' and it['cost'] > a.split_cost:
            # one theorem per stored row, recombined along the stored subtree shape
            flush()
            rows = it['rows']
            lines = []
            for j, n in enumerate(rows):
                lines.append(f'theorem row_{it["name"]}_{j} : checkRow ranks ({pred}) {word(n["word"])} {n["rank"]} = true := by decide +kernel\n')
            # pack the per-row theorems into modules by cost
            k = 0
            group, gcost = [], 0
            for j, n in enumerate(rows):
                group.append(lines[j]); gcost += cost(n)
                if gcost >= a.module_cost // 2:
                    cur = group; flush(); group, gcost = [], 0
            if group:
                cur = group; flush()

            def tree_proof(name, lo, hi):
                if lo == hi:
                    return 'True.intro'
                mid = (lo + hi) // 2
                return f'⟨{tree_proof(name, lo, mid)}, row_{name}_{mid}, {tree_proof(name, mid + 1, hi)}⟩'
            leaf_proof[it['name']] = ('split', tree_proof(it['name'], 0, len(rows)))
            continue
        if kind == 'leaf':
            line = f'theorem checked_{it["name"]} : checkRowsBlock ranks ({pred}) {it["name"]} = true := by decide +kernel\n'
            leaf_proof[it['name']] = ('block', f'leaf_rows_of_block checked_{it["name"]}')
        else:
            n = it['row']
            line = f'theorem row_{it["name"]} : checkRow ranks ({pred}) {word(n["word"])} {n["rank"]} = true := by decide +kernel\n'
        if cur and cur_cost + it['cost'] > a.module_cost:
            flush()
        cur.append(line)
        cur_cost += it['cost']
    flush()

    branches = {n['name']: n for n in interiors}

    def proof(name):
        if name.startswith('leaf'):
            return leaf_proof[name][1]
        n = branches[name]
        return f'⟨{proof(n["left"])}, row_{name}, {proof(n["right"])}⟩'

    text = ''.join(f'import {m}\n' for m in row_modules) + hdr
    text += f'theorem allRowsFast : CheckedRows ranks ({pred}) :=\n  {proof(root)}\n'
    text += 'theorem allRows : CheckedRows ranks (longPred 7) := checkedRows_fast_to_long allRowsFast\n'
    text += f'#print axioms allRowsFast\n#print axioms allRows\nend {ns_data}\n'
    (out / f'AllRows{P}.lean').write_text(text)

    # ---- initial family ----
    targ = f'targetInitialWord {abc[0]} {abc[1]} {abc[2]}'
    init_modules = []
    for batch in range(10):
        mod = f'Initial{P}_{batch:02d}'
        text = f'import Rank{P}\nimport PrefixChecksBase\n' + hdr
        for chunk in range(batch * 10, (batch + 1) * 10):
            text += (f'theorem initial_{chunk:03d} : ∀ i : Fin 100, checkInitial ranks {bound} '
                     f'({targ} ({chunk*100} + i.val)) = true := by decide +kernel\n')
        text += f'end {ns_data}\n'
        (out / f'{mod}.lean').write_text(text)
        init_modules.append(mod)

    def range_proof(lo, hi):
        p = f'fun i => checkInitial ranks {bound} ({targ} i) = true'
        if hi - lo == 1:
            return f'(checked_range ({p}) {lo*100} 100 initial_{lo:03d})'
        mid = (lo + hi) // 2
        return f'(join_ranges ({p}) {lo*100} {mid*100} {hi*100} {range_proof(lo, mid)} {range_proof(mid, hi)})'

    text = ''.join(f'import {m}\n' for m in init_modules) + hdr
    text += f'theorem initialLongChecked : ∀ i, i < 10000 → checkInitial ranks {bound} ({targ} i) = true := by\n'
    text += f'  intro i hi\n  exact {range_proof(0, 100)} i (Nat.zero_le i) hi\n'
    text += (f'theorem initialShortChecked : ∀ p ∈ shortTargets {abc[0]} {abc[1]} {abc[2]}, '
             f'checkInitial ranks {bound} p = true := by decide +kernel\n')
    text += (f'theorem initialCovered : ∀ p ∈ targetInitialWords {abc[0]} {abc[1]} {abc[2]}, '
             f'checkInitial ranks {bound} p = true :=\n'
             f'  initialCovered_of_checks {abc[0]} {abc[1]} {abc[2]} {bound} ranks initialShortChecked initialLongChecked\n')
    text += f'#print axioms initialLongChecked\n#print axioms initialShortChecked\n#print axioms initialCovered\nend {ns_data}\n'
    (out / f'Initial{P}.lean').write_text(text)

    # ---- short-transition rank descent ----
    short_modules = []
    for s in range(18):
        mod = f'Short{P}_{s:02d}'
        text = f'import Rank{P}\nimport PrefixChecksBase\n' + hdr
        text += f'theorem shortAt{s:02d} : ShortDescentAt ranks {s} := by decide +kernel\nend {ns_data}\n'
        (out / f'{mod}.lean').write_text(text)
        short_modules.append(mod)
    text = ''.join(f'import {m}\n' for m in short_modules) + hdr
    text += 'theorem shortOne : ∀ a : Fin 9, shortDescentOK ranks [2*(a.val+1)] = true := by decide +kernel\n'
    text += 'theorem shortRest : ∀ a, a < 18 → ShortDescentAt ranks a := by\n  intro a ha\n'
    text += '  have cases : ' + ' ∨ '.join(f'a = {s}' for s in range(18)) + ' := by omega\n'
    text += '  rcases cases with ' + ' | '.join('rfl' for _ in range(18)) + '\n'
    text += ''.join(f'  · exact shortAt{s:02d}\n' for s in range(18))
    text += 'theorem shortDesc : ShortDescent ranks := shortDescent_of_cases ranks shortOne shortRest\n'
    text += f'#print axioms shortOne\n#print axioms shortDesc\nend {ns_data}\n'
    (out / f'Short{P}.lean').write_text(text)

    # ---- conclusion ----
    a0, b0, c0 = abc
    text = (f'import AllRows{P}\nimport Initial{P}\nimport Short{P}\n\n'
            f'/-! Final application for the leading-digit family {P}. Accepted only after every\n'
            f'imported check module compiled and the transitive axiom audit passed. -/\n'
            f'namespace Agent118.Finite{P}\n\n'
            f'open Lychrel196 DecimalDigits SevenColumn.Certificate Agent118.PrefixKernel {ns_data}\n\n'
            f'/-- Every positive ordinary integer reaching a palindrome that begins with {P} does so\n'
            f'within {H} reverse-and-add steps. The digit length is not bounded. -/\n'
            f'theorem ancestry_bound{H} :\n'
            f'    ∀ A P t, 0 < A → PalindromeStarts3 {a0} {b0} {c0} P → orbit A t = P → t ≤ {H} :=\n'
            f'  ancestry_bound_of_finite_checks {a0} {b0} {c0} {bound} (by decide) ranks allRows shortDesc initialCovered\n\n'
            f'/-- All-time avoidance of this restricted palindrome family by the ordinary orbit of 196. -/\n'
            f'theorem no_196_{P}_palindrome :\n'
            f'    ∀ t, ¬ PalindromeStarts3 {a0} {b0} {c0} (orbit 196 t) :=\n'
            f'  no_196_of_finite_checks {a0} {b0} {c0} {bound} (by decide) (by decide) ranks allRows shortDesc initialCovered\n\n'
            f'/-- The same statement with the target family unfolded to canonical decimal digits. -/\n'
            f'theorem no_196_{P}_palindrome_unfolded (t : Nat) :\n'
            f'    ¬ (Palindrome (orbit 196 t) ∧ ∃ e W, Canonical (orbit 196 t) e W ∧ 3 ≤ W ∧\n'
            f'        e (W - 1) = {a0} ∧ e (W - 2) = {b0} ∧ e (W - 3) = {c0}) :=\n'
            f'  no_196_{P}_palindrome t\n\n'
            f'#print axioms ancestry_bound{H}\n#print axioms no_196_{P}_palindrome\n#print axioms no_196_{P}_palindrome_unfolded\n'
            f'end Agent118.Finite{P}\n')
    (out / f'Conclusion{P}.lean').write_text(text)

    layout = {
        'prefix': P, 'source': str(src.relative_to(HERE.parents[2])), 'source_sha256': digest,
        'nodes': len(nodes), 'bound_rank': bound, 'height_bound': H, 'root': root,
        'leaves': len(leaves), 'interiors': len(interiors),
        'split_leaves': [k for k, v in leaf_proof.items() if v[0] == 'split'],
        'data_modules': data_modules, 'row_modules': row_modules,
        'initial_modules': init_modules, 'short_modules': short_modules,
        'parameters': {'leaf': a.leaf, 'split_cost': a.split_cost, 'module_cost': a.module_cost},
        'predicted_cost_total': sum(l['cost'] for l in leaves) + sum(b['cost'] for b in interiors),
    }
    (out / 'layout.json').write_text(json.dumps(layout, indent=1) + '\n')
    print(json.dumps({k: v for k, v in layout.items() if not isinstance(v, list) or len(v) < 8}, indent=1))
    print('row modules', len(row_modules), 'data modules', len(data_modules))


if __name__ == '__main__':
    main()
