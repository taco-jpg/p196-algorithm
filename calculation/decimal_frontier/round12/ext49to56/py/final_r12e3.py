#!/usr/bin/env python3
"""r12e3: tables for FINAL.md (= r12e2's py/final_r12e2.py logic, plus node counts, the T=55/56 survivor appendix and a hit check).
Sources: out/census/summary_T*.json + surv_T*.txt (pass 1), deep pass 1 (out/deep1, deep53, deep54, deep5556), deep pass 2
(out/deep2), the long run (out/decisive/T52w.out), TOP-hit extracts (out/hits/*.extract).
A word is DECIDED by Theorem K iff some run printed DIES.  KNOWN (Theorem U, r12b) only for p11^5 and only if its TOP99 hit was
extracted and VERIFIED.  Every other TOP99/TOPUU hit is printed as **HIT** (must go through extract_hit.py + replay_plain.py).
Writes out/final_table_r12e3.md, out/final_open_r12e3.txt, out/final_open_r12e3.md, out/final_surv5556_r12e3.md and prints them."""
import os, re, json, glob
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the route directory (Studio: ~/p196_run/r12e)
P1 = ['deep1', 'deep53', 'deep54', 'deep5556']
def parse(f):
    txt = open(f).read(); m = re.search(r'word=([01]+) root=([01]+)', txt)
    k = [l for l in txt.splitlines() if l.startswith('KHXT ')]
    if not k: return dict(word=m.group(1) if m else None, root=m.group(2) if m else None, verdict='NOVERDICT', file=os.path.relpath(f, D))
    l = k[-1]; g = lambda p: (re.search(p, l).group(1) if re.search(p, l) else None)
    return dict(word=m.group(1) if m else None, root=m.group(2) if m else None, verdict='DIES' if ' DIES ' in l else 'SURVIVES',
                K=int(g(r'(?:DIES|SURVIVES) K=(\d+)')), reason=g(r'reason=(\w+)'), secs=float(g(r'secs=([\d.]+)')),
                kept=int(g(r'kept=(\d+)') or 0), maxn=int(g(r'maxnodes=(\d+)') or 0),
                t99=int(g(r'top99_first=(-?\d+)') or -1), tuu=int(g(r'topUU_first=(-?\d+)') or -1), file=os.path.relpath(f, D))
runs = {}
for d in P1 + ['deep2']:
    for f in sorted(glob.glob(f'{D}/out/{d}/*.out')):
        r = parse(f)
        if r and r['word']: runs.setdefault(r['word'], []).append(('deep2' if d == 'deep2' else 'deep1', r))
T52W = '0001000100010001000100011000100011000100011000100011'
dec = f'{D}/out/decisive/T52w.out'
if os.path.exists(dec) and os.path.getsize(dec) > 0:
    r = parse(dec); r['word'] = r['root'] = T52W
    if r['verdict'] != 'NOVERDICT': runs.setdefault(T52W, []).append(('long', r))
P11_5 = '00001110001' * 5
def known(w):
    """p11^5 counts as 'known stream only' (r12b Theorem U, T = 55 row) only if its TOP99 hit was extracted and VERIFIED as p11."""
    if w != P11_5: return False
    ex = f'{D}/out/hits/55_{w}.extract'
    if not os.path.exists(ex): return False
    t = open(ex).read()
    return 'VERIFIED' in t and ('e=' + '00111010011' * 5) in t
rows = []; opn = []; hits = []; app = []; omd = []; tot = [0] * 10; totpend = 0
for js in sorted(glob.glob(f'{D}/out/census/summary_T*.json')):
    s = json.load(open(js)); T = s['T']
    surv = [l.split() for l in open(f'{D}/out/census/surv_T{T}.txt')]
    d1 = d2 = dl = 0; capped = []; kn = []; pend = 0
    for x in surv:
        w = x[1]; rr = [(p, r) for p, r in runs.get(w, []) if r['verdict'] != 'NOVERDICT']
        for p, r in rr:
            if r['t99'] >= 0 or r['tuu'] >= 0: hits.append((T, w, p, r['t99'], r['tuu'], r['file']))
        dies = [(p, r) for p, r in rr if r['verdict'] == 'DIES']
        desc = '; '.join(f"{p} {r['verdict']} K={r['K']}" + (f" ({r['reason']}, kept {r['kept']:,})" if r['verdict'] == 'SURVIVES' else '') +
                         f", widest {r['maxn']:,}, {r['secs']:.0f} s" + (f", TOP99 first {r['t99']}" if r['t99'] >= 0 else '') +
                         (f", TOPUU first {r['tuu']}" if r['tuu'] >= 0 else '') for p, r in rr) or 'no deep verdict yet'
        if T >= 55: app.append(f"| {T} | {w} | {x[2]} {x[3]} | {' '.join(x[4:])} | {desc} |")
        if dies:
            p = dies[0][0]; d1 += (p == 'deep1'); d2 += (p == 'deep2'); dl += (p == 'long'); continue
        if known(w): kn.append(w); continue
        if not rr: pend += 1
        capped.append(w)
        best = max(rr, key=lambda pr: pr[1]['K']) if rr else None
        if best:
            b = best[1]; omd.append(f"| {T} | {w} | {' '.join(x[4:])} | {best[0]} ({b['reason']}, {b['secs']:.0f} s) | {b['K']} | {b['kept']:,} | {b['maxn']:,} | {'TOP HIT' if b['t99'] >= 0 or b['tuu'] >= 0 else 'none'} |")
        else:
            omd.append(f"| {T} | {w} | {' '.join(x[4:])} | no deep verdict yet | | | | |")
        opn.append(f"{T} {w} {' '.join(x[4:])} :: " + (f"UNDECIDED; best K={best[1]['K']} ({best[0]}, {best[1]['reason']}), kept {best[1]['kept']:,}, widest {best[1]['maxn']:,}; runs: {desc}" if best else 'PENDING (no deep verdict yet)'))
    und = len(capped) - pend; totpend += pend
    for i, v in enumerate((s['csv_total'], s['csv_primitive'], s['dies'], s['survivors'], d1, d2, dl, len(kn), und, s['csv_total'] - len(capped) - len(kn))): tot[i] += v
    rows.append((T, f"{s['csv_total']:,}", f"{s['csv_primitive']:,}", 'yes' if s['counts_ok'] else 'NO', f"{s['dies']:,}", s['survivors'], d1, d2, dl, len(kn),
                 und if not pend else f"{und} (+{pend} pending)", f"{s['csv_total'] - len(capped) - len(kn):,}" + (' (so far)' if pend else ''), s['maxK']))
hdr = ("| T | F1 words | primitive | counts = CSV | pass-1 DIES | pass-1 survivors | deep-1 DIES | deep-2 DIES | long-run DIES | known stream only | UNDECIDED | decided (Thm K/U) | max pass-1 K |\n"
       "|--:|--:|--:|:-:|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
body = ''.join('| ' + ' | '.join(str(v) for v in r) + ' |\n' for r in rows)
body += f"| all | {tot[0]:,} | {tot[1]:,} | | {tot[2]:,} | {tot[3]} | {tot[4]} | {tot[5]} | {tot[6]} | {tot[7]} | {tot[8]}" + (f" (+{totpend} pending)" if totpend else '') + f" | {tot[9]:,} | |\n"
open(f'{D}/out/final_table_r12e3.md', 'w').write(hdr + body)
open(f'{D}/out/final_open_r12e3.txt', 'w').write('\n'.join(opn) + '\n')
omh = "| T | word | type | best run | K reached | exact set at stop | widest level | TOP99/TOPUU |\n|--:|---|---|---|--:|--:|--:|---|\n"
open(f'{D}/out/final_open_r12e3.md', 'w').write(omh + '\n'.join(omd) + '\n')
ah = "| T | word | pass 1 (reason K) | type | deep runs |\n|--:|---|---|---|---|\n"
open(f'{D}/out/final_surv5556_r12e3.md', 'w').write(ah + '\n'.join(app) + '\n')
print(hdr + body); print('\n'.join(opn)); print()
print('TOP hits:', hits if hits else 'none')
print(f'appendix rows: {len(app)}')
