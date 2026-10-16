"""Solve complete finite exteriors for saved free-clock candidates.

Requires z3-solver and the original all-length periodic-pump encoding.
UNSAT here applies only to the exact supplied temporal/bulk/outer cycle
and chosen exterior width. It is not an exclusion of the free-clock model.
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from exist_geom_periodic_qpump import solve

HERE = Path(__file__).resolve().parent

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--period', type=int, default=5)
    ap.add_argument('--width', type=int, default=32)
    ap.add_argument('--seconds', type=float, default=12)
    args = ap.parse_args()
    data = json.loads((HERE/f'cycles_p{args.period}.json').read_text())
    rows = []
    for i, c in enumerate(data['candidates']):
        ans = solve(c['period'], args.width, args.period, c['growth'],
                    seconds=args.seconds, forced_clock=c['clock'],
                    forced_bulk=c['bulk'], forced_outer=c['outer'])
        ans['candidate_index'] = i
        rows.append(ans)
        (HERE/f'exteriors_p{args.period}_w{args.width}.json').write_text(json.dumps(dict(
            scope=__doc__, decimal_lychrel_existence_proved=False, queries=rows),indent=2)+'\n')
        print(json.dumps(ans), flush=True)
        if ans['result'] == 'sat':
            break
