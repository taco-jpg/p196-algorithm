import os
"""Ansatz scan: for each base b, (1) B-cycles from the exact B-automaton (all n), (2) C-survivors for the resulting (e,g) stream
(exhaustive over symmetric C with |C|<=mmax), (3) end-to-end check with the exact Python mirror (cycleOK).
usage: python3 family_scan.py bmin bmax pmax mmax [step]"""
import sys, re, subprocess
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from joint_check import joint
bmin,bmax,pmax,mmax=map(int,sys.argv[1:5]); step=int(sys.argv[5]) if len(sys.argv)>5 else 1
for b in range(bmin,bmax+1,step):
    out=subprocess.run(['./bauto',str(b),'1',str(pmax),'-w'],capture_output=True,text=True).stdout
    seen=set(); hits=[]
    nB=0
    for line in out.splitlines():
        if not line.startswith('ACCEPT'): continue
        p=int(re.search(r"p=(\d+)",line)[1]); g=re.search(r" g=(\d+)",line)[1]; e=re.search(r" e=(\d+)",line)[1]
        depth=int(re.search(r"depth=(\d+)",line)[1])
        Bs=[[int(x) for x in m.split(',') if x] for m in re.findall(r"\[([^\]]*)\]",line)]
        key=(g,e)
        # skip pure repetitions of a shorter stream
        nB+=1
        # C survivors on stream repeated until total gam is even
        gs,es=g,e
        if g.count('1')%2==1: gs,es=g+g,e+e
        r=subprocess.run(['./cmatch',str(b),str(mmax),es,gs,'3'],capture_output=True,text=True).stdout
        for m in re.finditer(r"SURVIVOR m0=(\d+) C=\[([^\]]*)\]",r):
            C=[int(x) for x in m[2].split(',')]
            res=joint(b,Bs[0],C,maxsteps=400)
            hits.append((p,g,e,depth,C,res[:6] if res[0]=='cycle' else res))
    print(f"b={b}: B-cycles(p<={pmax})={nB}; joint hits={len(hits)}",flush=True)
    for h in hits[:4]: print("   ",h,flush=True)
