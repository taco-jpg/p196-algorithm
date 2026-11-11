#!/usr/bin/env python3
import os
"""r13a: U3 control table + validation summary from logs/ctrl (run by assemble via FINAL_mid include)."""
import re, glob, collections
ROOT=os.path.expanduser('~/p196_run/r13a')
rows=collections.defaultdict(dict)
val=collections.Counter()
for f in glob.glob(ROOT+'/logs/ctrl/i*.log'):
    txt=open(f).read()
    if 'bandval.py' in txt.split('\n')[0]:
        val['VALIDATE PASS' if 'VALIDATE PASS' in txt else 'VALIDATE FAIL']+=1
        continue
    m=re.search(r'RESULT L b=10 clock=1000 V=18,9,0 T=120 epochs=1 Tprime=\d+ tau=(\d+) rot=(\d+) word=\[([^\]]*)\] solver=(\w+) trim=(\w+) enc=(\d).*?: (SAT|UNSAT).*total=([\d.]+)s',txt)
    if not m: 
        m2=re.search(r'^# (.*)$',txt,re.M)
        val['unparsed']+=1
        continue
    tau,rot,word,solver,trim,enc,ans,tot=m.groups()
    rows[(int(tau),int(rot),word)][f'{solver}/enc{enc}']=(ans,float(tot))
print(f'U3 words at T=120, R=12: {len(rows)} word instances reported; validation runs: {dict(val)}')
print('| tau | rot | word | kissat404/enc1 | cadical195/enc1 | kissat404/enc2 |')
print('|---|---|---|---|---|---|')
nall=0
for k in sorted(rows):
    r=rows[k]
    def cell(n):
        return f'{r[n][0]} {r[n][1]:.0f}s' if n in r else '-'
    print(f'| {k[0]} | {k[1]} | ({k[2]}) | {cell("kissat404/enc1")} | {cell("cadical195/enc1")} | {cell("kissat404/enc2")} |')
    if all(n in r and r[n][0]=='UNSAT' for n in ['kissat404/enc1','cadical195/enc1','kissat404/enc2']): nall+=1
print(f'\nRows with UNSAT in all three method combinations: {nall} of {len(rows)}')
