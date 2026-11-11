#!/usr/bin/env python3
"""Run my all-period closed-walk closure (mc13c runscc) on every band of the r13a census, as a lattice exterior.
Output: for each band and phase orbit: closure level or last level reached, exact centres found (any period), and depth-0 result."""
import os, re, sys, json, subprocess, itertools
from concurrent.futures import ThreadPoolExecutor
HOME=os.path.expanduser('~')
CENSUS=HOME+'/p196_run/r13a/census'
BIN=HOME+'/p196_run/mchk13b/mc13c'
clock=sys.argv[1]; Tmax=int(sys.argv[2]); sec=int(sys.argv[3]); workers=int(sys.argv[4]); outfn=sys.argv[5]
kmax=int(sys.argv[6]) if len(sys.argv)>6 else 60
g=[int(c) for c in clock]; p=len(g)
def rowstep(x,gam):
    n=len(x)
    al=[0]*n
    for _ in range(3):
        for c in range(n):
            al[(c+1)%n]=1 if x[c]+al[c]>=10 else 0
    be=[0]*n
    for _ in range(3):
        for c in range(n-1,-1,-1):
            be[c]=1 if x[c]+be[(c+1)%n]>=10 else 0
    lo=[(x[c]+al[c])%10 for c in range(n)]
    hi=[(x[c]+be[(c+1)%n])%10 for c in range(n)]
    return [lo[c]+(hi[(c-1)%n] if gam else hi[c]) for c in range(n)]
bands=[]
for s in range(1,9):
    fn=f'{CENSUS}/b{clock}_s{s}.txt'
    if not os.path.exists(fn): continue
    for line in open(fn):
        m=re.match(r'BAND s=(\d+) T=(\d+) Trot=(\d+) twist=(-?\d+) cyclelen=(\d+) V=([\d,]+)',line)
        if m:
            bands.append((int(m[1]),int(m[2]),[int(c) for c in m[6].split(',')]))
print('bands listed',len(bands),flush=True)
os.makedirs('lat',exist_ok=True)
def run(band):
    s,T,V=band
    if T>Tmax: return None
    rows=[list(V)]
    for t in range(T):
        rows.append(rowstep(rows[-1],g[t%p]))
    if rows[T]!=list(V):
        return dict(V=V,T=T,error='V_T != V')
    name='lat/'+clock+'_'+'_'.join(map(str,V))+'.txt'
    with open(name,'w') as f:
        f.write(f'10 {T} 0 {s}\n'+' '.join(str(g[t%p]) for t in range(T))+'\n')
        for t in range(T):
            f.write(' '.join(map(str,rows[t]))+'\n')
    res=subprocess.run([BIN,'orbits',name],capture_output=True,text=True)
    orbs=[l for l in res.stdout.splitlines() if l.startswith('orbit')]
    out=dict(V=V,T=T,s=s,orbits=[])
    for o in range(len(orbs)):
        cmd=['perl','-e','alarm shift; exec @ARGV',str(sec),BIN,'runscc',name,str(o),str(kmax),'1','1']
        res=subprocess.run(cmd,capture_output=True,text=True)
        lv=re.findall(r'^K (\d+) Eacc (\d+) accepting (\d+)',res.stdout,re.M)
        pe=re.findall(r'^# PERIODIC exact orbit K=(\d+) laps=(\d+) period=(\d+) anchor phase \(t=(\d+),j=(\d+),par=(\d+)\): ([\d ]+)',res.stdout,re.M)
        empty=re.search(r'EMPTY at K=(\d+)',res.stdout)
        out['orbits'].append(dict(o=o,lastK=int(lv[-1][0]) if lv else 0,lastSize=int(lv[-1][1]) if lv else None,empty=int(empty[1]) if empty else None,periodic=[list(x) for x in pe[:6]],nper=len(pe)))
    return out
with ThreadPoolExecutor(workers) as ex, open(outfn,'w') as f:
    n=0
    for r in ex.map(run,bands):
        n+=1
        if r is None: continue
        f.write(json.dumps(r)+'\n'); f.flush()
print('done',flush=True)
