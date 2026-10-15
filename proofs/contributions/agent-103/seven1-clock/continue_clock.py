#!/usr/bin/env python3
"""Agent #103: continue an UNKNOWN_CAP scalar-clock prefix hierarchy.

Uses the unchanged reviewed relation `2026-10-14-broader-return/branching_lift.py`
and the unchanged root construction `2026-10-14-scalar-clock/scalar_clock.py`
(`initial`). Widths are re-derived from width 1; every artifact whose width
was archived by the original capped run is compared byte-for-byte (SHA-256)
with the archived file before continuing. Only the caps differ.
Outcomes: EMPTY_AT_FINITE_WIDTH, or UNKNOWN_CAP at the new caps. A surviving
graph is not a realizable infinite integer orbit.
"""
import hashlib, importlib.util, json, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
C = REPO / 'proofs/contributions'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
LIFT = load('branching_lift', C / '2026-10-14-broader-return/branching_lift.py')
SC = load('scalar_clock', C / '2026-10-14-scalar-clock/scalar_clock.py')

name = sys.argv[1] if len(sys.argv) > 1 else 'seven_1'
MAX_RAW_VERTICES = int(sys.argv[2]) if len(sys.argv) > 2 else 30_000_000
MAX_WIDTH = 40
out = HERE / name; out.mkdir(exist_ok=True)
archived = C / '2026-10-14-scalar-clock' / name
graph, clock = SC.initial(SC.CLOCKS[name])
LIFT.HERE, LIFT.CLOCK = out, clock
result = dict(status='RUNNING', clock=name, outer_coefficients=SC.CLOCKS[name], overflow_clock=clock,
              caps=dict(raw_vertices=MAX_RAW_VERTICES, width=MAX_WIDTH),
              branching_lift_sha256=hashlib.sha256((C / '2026-10-14-broader-return/branching_lift.py').read_bytes()).hexdigest(),
              scalar_clock_sha256=hashlib.sha256((C / '2026-10-14-scalar-clock/scalar_clock.py').read_bytes()).hexdigest(),
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              completed_graphs=[], archived_matches=[],
              scope='Necessary exact prefix relation with arbitrary deeper temporal histories; a surviving graph is not an infinite integer witness.')
def record():
    (out / 'continuation.json').write_text(json.dumps(result, indent=2) + '\n')
while True:
    t0 = time.time()
    raw = LIFT.save(graph, 'raw')
    graph, meta = LIFT.recurrent_part(graph)
    meta.update(width=graph['width'], raw_artifact=raw, retained_artifact=LIFT.save(graph, 'recurrent'),
                seconds=round(time.time() - t0, 2))
    for kind in ('raw', 'recurrent'):
        a = archived / ('branch_width_%02d_%s.bin.gz' % (graph['width'], kind))
        if a.exists():
            mine = meta['raw_artifact' if kind == 'raw' else 'retained_artifact']['sha256']
            ok = hashlib.sha256(a.read_bytes()).hexdigest() == mine
            result['archived_matches'].append(dict(width=graph['width'], kind=kind, identical=ok))
            assert ok, ('archived artifact differs', graph['width'], kind)
    result['completed_graphs'].append(meta)
    print(json.dumps({k: meta[k] for k in ('width', 'raw_vertices', 'raw_edges', 'cyclic_components', 'retained_vertices', 'retained_edges', 'seconds')}), flush=True)
    if not graph['phase']:
        result.update(status='EMPTY_AT_FINITE_WIDTH', empty_width=graph['width']); break
    v, e = 19 * len(graph['phase']), 19 * len(graph['source'])
    if v > MAX_RAW_VERTICES or graph['width'] >= MAX_WIDTH:
        result.update(status='UNKNOWN_CAP', next_lift=dict(width=graph['width'] + 1, raw_vertices=v, raw_edges=e)); break
    record()
    graph = LIFT.lift(graph)
record()
print(json.dumps(dict(status=result['status'], last_width=graph['width'])), flush=True)
