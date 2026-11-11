#!/usr/bin/env python3
"""r12e: final census table for T = 49..: pass-1 summaries (out/census/summary_T*.json, surv_T*.txt) + deep-pass verdicts
(out/deep*/T_word.out, khxt lines).  A word is DECIDED (no 9-wire exterior, no uniform-band template; Theorem K) if pass 1 or a deep
pass printed DIES; otherwise UNDECIDED.  Writes out/final_table.md and out/final_open.txt; prints the table."""
import os, re, json, glob, collections
D = os.path.expanduser('~/p196_run/r12e')
deep = {}
for f in sorted(glob.glob(f'{D}/out/deep*/*.out')):
    txt = open(f).read()
    m = re.search(r'word=([01]+) root=([01]+)', txt)
    if not m: continue
    w = m.group(1)
    for l in txt.splitlines():
        if l.startswith('KHXT '):
            st = 'DIES' if ' DIES ' in l else 'SURVIVES'
            K = int(re.search(r'(?:DIES|SURVIVES) K=(\d+)', l).group(1))
            t99 = re.search(r'top99_first=(-?\d+)', l); tuu = re.search(r'topUU_first=(-?\d+)', l)
            prev = deep.get(w)
            if prev is None or (prev[0] != 'DIES' and (st == 'DIES' or K > prev[1])):
                deep[w] = (st, K, os.path.relpath(f, D), int(t99.group(1)) if t99 else None, int(tuu.group(1)) if tuu else None)
rows = []; open_words = []
for js in sorted(glob.glob(f'{D}/out/census/summary_T*.json')):
    s = json.load(open(js)); T = s['T']
    surv = [l.split() for l in open(f'{D}/out/census/surv_T{T}.txt')] if os.path.exists(f'{D}/out/census/surv_T{T}.txt') else []
    ddies = 0; und = []; hits = []
    for r in surv:
        w = r[1]; v = deep.get(w)
        if v and v[0] == 'DIES': ddies += 1
        else: und.append((w, ' '.join(r[4:]), v))
        if v and ((v[3] or -1) >= 0 or (v[4] or -1) >= 0): hits.append(w)
    rows.append((T, s['csv_total'], s['csv_primitive'], s['counts_ok'], s['dies'], s['survivors'], ddies, len(und), s['csv_total'] - len(und), s['maxK'], hits))
    for w, typ, v in und: open_words.append(f"{T} {w} {typ} :: " + (f"deep pass {v[0]} K={v[1]} ({v[2]})" if v else "no deep pass yet"))
hdr = "| T | F1 words | primitive | counts = CSV | pass-1 DIES | pass-1 survivors | deep DIES | UNDECIDED | decided | max pass-1 K | TOP hits |\n|--:|--:|--:|:-:|--:|--:|--:|--:|--:|--:|--:|\n"
body = ''.join(f"| {T} | {a} | {p} | {'yes' if ok else 'NO'} | {d} | {s} | {dd} | {u} | {dec} | {mk} | {len(h)} |\n" for T, a, p, ok, d, s, dd, u, dec, mk, h in rows)
tot = [sum(r[i] for r in rows) for i in (1, 2, 4, 5, 6, 7, 8)]
body += f"| all | {tot[0]} | {tot[1]} | | {tot[2]} | {tot[3]} | {tot[4]} | {tot[5]} | {tot[6]} | | |\n"
open(f'{D}/out/final_table.md', 'w').write(hdr + body)
open(f'{D}/out/final_open.txt', 'w').write('\n'.join(open_words) + ('\n' if open_words else ''))
print(hdr + body); print('\n'.join(open_words))
