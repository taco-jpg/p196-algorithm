#!/usr/bin/env python3
"""Q2 (light version): for each primitive exterior stream (g,e) of a base, run cauto_fast on k repetitions (G*k even, p*k<=32), all widths/trims.
usage: q2b.py base tmo cap  'g:e,e;g:e'  [kmax]"""
import sys, subprocess, re, time
b=int(sys.argv[1]); TMO=int(sys.argv[2]); CAP=sys.argv[3]; spec=sys.argv[4]; KMAX=int(sys.argv[5]) if len(sys.argv)>5 else 8
for item in spec.split(';'):
    g,es=item.split(':')
    for e in es.split(','):
        for k in range(1,KMAX+1):
            if len(g)*k>32: break
            G=g.count('1')*k
            if G%2: continue
            t0=time.time()
            try:
                r=subprocess.run(['sh','-c',f'ulimit -v 2000000; exec ../bin/cauto_fast {b} {e*k} {g*k} 1 1 -vall -allm -sym -cap {CAP}'],capture_output=True,text=True,timeout=TMO)
                out=r.stdout
                st={}
                for l in out.splitlines():
                    mm=re.search(r"^DONE .*status=(\w+)",l)
                    if mm: st[mm[1]]=st.get(mm[1],0)+1
                summ=' '.join(f"{a}={c}" for a,c in sorted(st.items()))
                fe=[l for l in out.splitlines() if l.startswith('FEASIBLE ')]
                note=fe[0][:70] if fe else ''
            except subprocess.TimeoutExpired:
                summ='TIMEOUT'; note=''
            print(f"b={b} g={g} e={e} k={k} p={len(g)*k} G={G}: {summ} {note} ({time.time()-t0:.1f}s)",flush=True)
