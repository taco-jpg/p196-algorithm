import sys, json, time
sys.path.insert(0,'.')
import rar, nbs, orbit_scan as os_
import numpy as np
cands = json.load(open('data/candidates.json'))
T = int(sys.argv[1]); lo=int(sys.argv[2]); hi=int(sys.argv[3]); ncand=int(sys.argv[4])
for b in range(lo, hi+1):
    for n in cands[str(b)][:ncand]:
        dig = rar.to_digits(n, b)
        recs, summ, gh, nh = os_.scan(b, dig, T, W=8, imax=300, tmax=60)
        last = recs[-8:]
        if summ['palindrome_at'] is not None:
            print(b, n, 'PALINDROME at', summ['palindrome_at']); continue
        # summarize last window
        gs = [r['tpl_g'] for r in last]; ok = [r.get('pred_ok') for r in last]
        r = last[-1]
        print(f"b={b} n={n} steps={summ['steps_done']} digits={summ['final_digits']} gamdens={summ['gam_density']:.3f} last-g={gs} pred_ok={sum(1 for o in ok if o is True)}/{len(ok)} tplB={r['tpl'][0] if r['tpl'] else None} C={len(r['tpl'][1]) if r['tpl'] else None} run={r.get('run')} cyc={r.get('cyc_len')}", flush=True)
