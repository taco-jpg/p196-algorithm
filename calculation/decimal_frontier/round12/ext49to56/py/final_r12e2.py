#!/usr/bin/env python3
"""r12e2: final census table T = 49..56 from the pass-1 summaries (out/census/summary_T*.json, surv_T*.txt) and every deep-pass
verdict (deep pass 1: out/deep1, deep53, deep54, deep5556; deep pass 2: out/deep2; the long run: out/decisive/T52w.out).
A word is DECIDED (Theorem K: no 9-wire exterior, no uniform-band template) iff pass 1 or some deep run printed DIES.  For the
other survivors: KNOWN = TOP99 hit verified as a known stream (out/hits/*.extract VERIFIED and listed in KNOWN below), else
UNDECIDED with the largest level reached without a TOP hit (Lemma W: no exterior of width <= K-2, no band of height <= K-3).
Writes out/final_table_r12e2.md, out/final_open_r12e2.txt and prints both."""
import os, re, json, glob
D = os.path.expanduser('~/p196_run/r12e')
P1 = ['deep1', 'deep53', 'deep54', 'deep5556']
def parse(f):
    txt = open(f).read(); m = re.search(r'word=([01]+) root=([01]+)', txt)
    k = [l for l in txt.splitlines() if l.startswith('KHXT ')]
    if not k: return None
    l = k[-1]; g = lambda p: (re.search(p, l).group(1) if re.search(p, l) else None)
    return dict(word=m.group(1) if m else None, root=m.group(2) if m else None, verdict='DIES' if ' DIES ' in l else 'SURVIVES',
                K=int(g(r'(?:DIES|SURVIVES) K=(\d+)')), reason=g(r'reason=(\w+)'), secs=float(g(r'secs=([\d.]+)')),
                t99=int(g(r'top99_first=(-?\d+)') or -1), tuu=int(g(r'topUU_first=(-?\d+)') or -1), file=os.path.relpath(f, D))
runs = {}
for d in P1 + ['deep2']:
    for f in sorted(glob.glob(f'{D}/out/{d}/*.out')):
        r = parse(f)
        if r and r['word']: runs.setdefault(r['word'], []).append(('deep2' if d == 'deep2' else 'deep1', r))
dec = f'{D}/out/decisive/T52w.out'
if os.path.exists(dec):
    r = parse(dec)
    if r: r['word'] = '0001000100010001000100011000100011000100011000100011'; runs.setdefault(r['word'], []).append(('long', r))
KNOWN = {'00001110001' * 5: 'p11^5: only the p11 stream (r12b Theorem U, T = 55)'}
rows = []; opn = []
for js in sorted(glob.glob(f'{D}/out/census/summary_T*.json')):
    s = json.load(open(js)); T = s['T']
    surv = [l.split() for l in open(f'{D}/out/census/surv_T{T}.txt')]
    d1 = d2 = dl = 0; capped = []; known = []
    for x in surv:
        w = x[1]; rr = runs.get(w, [])
        dies = [(p, r) for p, r in rr if r['verdict'] == 'DIES']
        if dies:
            p = dies[0][0]; d1 += (p == 'deep1'); d2 += (p == 'deep2'); dl += (p == 'long'); continue
        if w in KNOWN: known.append(w); continue
        best = max(rr, key=lambda pr: pr[1]['K']) if rr else None
        hits = [r for p, r in rr if r['t99'] >= 0 or r['tuu'] >= 0]
        capped.append(w)
        cap = ', '.join(f"{p} {r['reason']} K={r['K']} ({r['secs']:.0f} s)" for p, r in rr) if rr else 'no deep run'
        opn.append(f"{T} {w} {' '.join(x[4:])} :: UNDECIDED; runs: {cap}" + (f"; no TOP hit up to K={best[1]['K']}: no exterior of width <= {best[1]['K']-2}" if best and not hits else '') + (f"; TOP HIT {hits}" if hits else ''))
    rows.append((T, s['csv_total'], s['csv_primitive'], 'yes' if s['counts_ok'] else 'NO', s['dies'], s['survivors'], d1, d2, dl, len(known), len(capped), s['csv_total'] - len(capped) - len(known), s['maxK']))
hdr = ("| T | F1 words | primitive | counts = CSV | pass-1 DIES | pass-1 survivors | deep-1 DIES | deep-2 DIES | long-run DIES | known stream only | UNDECIDED (capped) | decided (Thm K) | max pass-1 K |\n"
       "|--:|--:|--:|:-:|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
body = ''.join('| ' + ' | '.join(str(v) for v in r) + ' |\n' for r in rows)
tot = [sum(r[i] for r in rows) for i in (1, 2, 4, 5, 6, 7, 8, 9, 10, 11)]
body += f"| all | {tot[0]} | {tot[1]} | | {tot[2]} | {tot[3]} | {tot[4]} | {tot[5]} | {tot[6]} | {tot[7]} | {tot[8]} | {tot[9]} | |\n"
open(f'{D}/out/final_table_r12e2.md', 'w').write(hdr + body)
open(f'{D}/out/final_open_r12e2.txt', 'w').write('\n'.join(opn) + '\n')
print(hdr + body); print('\n'.join(opn))
