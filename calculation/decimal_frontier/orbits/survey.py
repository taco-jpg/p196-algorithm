#!/usr/bin/env python3
"""survey.py LO HI T [K]  -- natural unique-orbit candidates of bases LO..HI, T steps each; one JSON line per orbit."""
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, nbs, orbit_scan as os_
cands = json.load(open('data/candidates_unique.json'))
lo, hi, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); K = int(sys.argv[4]) if len(sys.argv) > 4 else 6
tag = sys.argv[5] if len(sys.argv) > 5 else 'survey'
out = open(f'data/{tag}_{lo}_{hi}.jsonl', 'a')
for b in range(lo, hi + 1):
    for n in cands[str(b)][:K]:
        t0 = time.time()
        recs, summ, gh, nh = os_.scan(b, rar.to_digits(n, b), T, W=8, imax=300, tmax=240, heavy=True)
        # series at window starts
        ser = []
        cur = None
        for r in recs:
            ser.append([r['t'], r['tpl_g'], r['tpl_i'], r['pw_run_any'], r['pw_run_nb'], r.get('cr_pw'), r['pw_per2'], r['pw_per3'], r['pw_per4'], r.get('run'), r.get('pred_ok')])
        last = recs[-8:]
        res = {'base': b, 'seed': n, 'steps': summ['steps_done'], 'digits': summ['final_digits'], 'pal': summ['palindrome_at'],
               'gam_density': summ['gam_density'], 'late_g': [r['tpl_g'] for r in last], 'late_i': [r['tpl_i'] for r in last],
               'late_pred_ok': sum(1 for r in last if r.get('pred_ok') is True),
               'late_run': [r.get('run') for r in last], 'late_cyc': [r.get('cyc_len') for r in last],
               'late_cert': [r.get('cyc_cert') for r in last], 'secs': round(time.time() - t0, 1), 'series': ser}
        out.write(json.dumps(res) + '\n'); out.flush()
        print(f"b={b} n={n} steps={res['steps']} dig={res['digits']} pal={res['pal']} gam={res['gam_density']:.3f} late_g={res['late_g']} i={res['late_i'][-1]} ok={res['late_pred_ok']} run={set(res['late_run'])} {res['secs']}s", flush=True)
