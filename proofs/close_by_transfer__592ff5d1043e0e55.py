"""Exact spatial reverse search for sampled periodic-bulk candidates.

Uses the previously published arbitrary-clock column relation, without SMT.
A cap or timeout is UNKNOWN. Reaching the exterior root requires a separate
whole-word candidate verification before any existence claim.
"""
from collections import deque
from pathlib import Path
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'main_existence_attempt/boundary_resume/new_clock'))
from columns import initial, bulk_state, check_edge, successors
from reverse_lift import predecessors

HERE = Path(__file__).resolve().parent


def close(c, seconds, cap, edgecap):
    clock = c['clock']
    root = initial(c['outer'],clock)
    target = bulk_state(c['bulk'][0],clock)
    parent = {target:None}
    queue = deque([target])
    start = time.monotonic()
    done = edges = 0
    status, reason, columns = 'UNKNOWN', 'time limit', None
    interrupted = False
    while queue and time.monotonic()-start < seconds:
        state = queue.popleft()
        if state == root:
            status, reason = 'EXTERIOR_FOUND_REQUIRES_INDEPENDENT_AUDIT', None
            columns = [c['outer']]
            while parent[state] is not None:
                state,col = parent[state]
                columns.append(list(col))
            break
        prev,truncated,_ = predecessors(state,clock,edgecap)
        if truncated:
            reason = 'per-state predecessor cap'
            interrupted = True
            break
        done += 1
        edges += len(prev)
        for old,col in prev.items():
            check_edge(old,state,col,clock)
            if old not in parent:
                parent[old] = state,col
                queue.append(old)
        if len(parent) >= cap:
            reason = 'state cap'
            interrupted = True
            break
    if not queue and columns is None and not interrupted:
        status,reason = 'COMPLETE_ROOT_ABSENT',None
    return dict(status=status,reason=reason,states=len(parent),expanded=done,edges=edges,
                queue=len(queue),seconds=time.monotonic()-start,period=c['period'],
                growth=c['growth'],exterior_columns=columns,
                decimal_lychrel_existence_proved=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='cycles_p5_k4.json')
    ap.add_argument('--seconds',type=float,default=20)
    ap.add_argument('--cap',type=int,default=50000)
    ap.add_argument('--edgecap',type=int,default=50000)
    a=ap.parse_args()
    data=json.loads((HERE/a.input).read_text())
    rows=[]
    for i,c in enumerate(data['candidates']):
        row=close(c,a.seconds,a.cap,a.edgecap)
        row['candidate_index']=i
        rows.append(row)
        (HERE/('transfer_'+a.input)).write_text(json.dumps(dict(
            source=a.input,limits=dict(seconds=a.seconds,cap=a.cap,edgecap=a.edgecap),
            queries=rows),indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['exterior_columns'] is not None:
            break
