#!/usr/bin/env python3
"""独立核对实际 Lean 字面数据与原 Python 程序产物；不作为一般数学证明。"""
import ast
import hashlib
import json
from pathlib import Path
import re
import types

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PROOFS = REPO / 'proofs'


def original_functions(filename, names, scope):
    path = PROOFS / filename
    nodes = [node for node in ast.parse(path.read_text()).body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), scope)


def main():
    helper = {}
    original_functions('creative_regular_invariant__ea923cdb26a39825.py', {'C', 'D'}, helper)
    scope = {'r': types.SimpleNamespace(C=helper['C'], D=helper['D'])}
    original_functions('creative_regular_direct__8988fd8c6a0aad92.py', {'fst_graph'}, scope)
    states, edges = scope['fst_graph']()
    weighted = PROOFS / 'persist_spacetime_weighted__d53dd1c09dcfc34a.py'
    nodes = ast.parse(weighted.read_text()).body
    names = lambda n: [t.id for t in n.targets if isinstance(t, ast.Name)] if isinstance(n, ast.Assign) else []
    start = next(i for i, node in enumerate(nodes) if 'TERMS' in names(node))
    end = next(i for i, node in enumerate(nodes) if 'NW' in names(node))
    scope.update(FS=states, FE=edges)
    exec(compile(ast.Module(body=nodes[start:end+1], type_ignores=[]), str(weighted), 'exec'), scope)
    terminals = scope['TS']

    lean = PROOFS / 'Agent107TransducerTablesData.lean'
    if not lean.exists():
        lean = PROOFS / 'Agent107TransducerTables.lean'
    text = lean.read_text()
    literals = {}
    for row in re.finditer(r'^def state(\d+) : State := ⟨(\d+), (\d+), (\d+), (\(-1\)|\d+), (true|false)⟩$', text, re.M):
        index, h, a, b, d, started = row.groups()
        literals[int(index)] = (int(h), int(a), int(b), int(d.strip('()')), started == 'true')
    state_order = re.search(r'def states : List State := \[([^\]]*)\]', text).group(1)
    order = [int(value) for value in re.findall(r'state(\d+)', state_order)]
    assert order == list(range(len(states)))
    assert [literals[i] for i in order] == states

    parsed_edges, parsed_terminals = [], []
    option = r'(none|\(some \d+\))'
    option_value = lambda value: None if value == 'none' else int(value[6:-1])
    for index in order:
        block = re.search(rf'def edges{index} : List Edge := \[\n(.*?)\n\]', text, re.S).group(1)
        row = [tuple(map(int, match)) for match in re.findall(r'⟨state(\d+), (\d+), (\d+), state(\d+)⟩', block)]
        assert len(row) == block.count('⟨')
        parsed_edges.extend(row)
        block = re.search(rf'def terminals{index} : List TerminalRow := \[\n(.*?)\n\]', text, re.S).group(1)
        matches = re.findall(r'⟨state(\d+), ' + option + ', ' + option + ', ' + option + r'⟩', block)
        row = [(int(i), option_value(c), option_value(e), option_value(o)) for i, c, e, o in matches]
        assert len(row) == block.count('⟨')
        parsed_terminals.extend(row)
    for name, prefix in [('edgeRows', 'edges'), ('terminalRows', 'terminals')]:
        block = re.search(rf'def {name} : .* := \[([^\]]*)\]', text).group(1)
        assert [int(v) for v in re.findall(prefix + r'(\d+)', block)] == order
    assert parsed_edges == edges
    assert parsed_terminals == terminals
    result = {
        'status': 'EXACT_ORDERED_LITERAL_DATA_MATCH',
        'scope': '实际Lean字面表与原Python AST运算结果逐项一致；这只是源码对应核对，一般定理由Lean内核证明负责。',
        'lean_source': str(lean.relative_to(REPO)),
        'lean_sha256': hashlib.sha256(lean.read_bytes()).hexdigest(),
        'counts': {'states': len(states), 'edges': len(edges), 'terminals': len(terminals)},
        'original_sources': {
            name: hashlib.sha256((PROOFS / name).read_bytes()).hexdigest()
            for name in [
                'creative_regular_invariant__ea923cdb26a39825.py',
                'creative_regular_direct__8988fd8c6a0aad92.py',
                'persist_spacetime_weighted__d53dd1c09dcfc34a.py']
        },
        'independence': '不导入或调用作者的generator或extracted-tables.json，重新执行原AST并解析当前Lean字面列表。',
    }
    (HERE / 'literal-table-comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
