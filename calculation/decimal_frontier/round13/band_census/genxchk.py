#!/usr/bin/env python3
"""r13a: cross-check jobs for every ALLUNSAT band result: re-run with (cadical195, enc1) and (kissat404, enc2) [--all --timeout 1800].
usage: genxchk.py OUT   (skips tuples already present in xchk_done.txt; appends to it)"""
import sys, re, glob, os
ROOT=os.path.expanduser('~/p196_run/r13a')
seen=set()
pf=ROOT+'/xchk_done.txt'
if os.path.exists(pf):
    seen=set(l.strip() for l in open(pf))
out=[]; new=[]
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT') or 'status=ALLUNSAT' not in line: continue
            m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) :',line)
            if not m: continue
            mode,b,clk,V,T,M,tau,R,Rf,solver,enc=m.groups()
            key=f'{mode}|{b}|{clk}|{V}|{T}|{M}|{tau}|{R}|{Rf}'
            if key in seen or key in new: continue
            new.append(key)
            base=mode[0]  # L or R
            star='*' in mode
            flags=''
            if star and base=='L': flags+=' --allepochs'
            if star and base=='R': flags+=' --comoving'
            PY=sys.executable; J=ROOT+'/bandjob.py'
            cmd0=f"{PY} {J} {base} --b {b} --clock {clk} --V {V} --T {T} --epochs {M} --tau {tau} --R {R}"
            if int(Rf): cmd0+=f" --Rfree {Rf}"
            cmd0+=flags+" --all --timeout 1800"
            out.append(cmd0+" --solver cadical195 --enc 1")
            out.append(cmd0+" --solver kissat404 --enc 2")
open(sys.argv[1],'w').write('\n'.join(out)+('\n' if out else ''))
with open(pf,'a') as f:
    for k in new: f.write(k+'\n')
print(len(new),'ALLUNSAT results ->',len(out),'cross-check jobs ->',sys.argv[1])
