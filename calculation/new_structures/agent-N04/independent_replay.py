#!/usr/bin/env python3
"""Independent Python BIG-INTEGER replay for phasefront_scan seeds and steps."""
import argparse, json
from phasefront_scan import load, step

def digits_of(n):return [int(d) for d in str(n)[::-1]]

def replay(scc, cases=((8,16),(14,7),(0,18)), steps=64, half=1000):
    pref,w=load(scc);out=[]
    for off,sh in cases:
        seam=300+off
        low=[pref[i] if i<39 else w[0][(i-39+(sh if i>=seam else 0))%20] for i in range(half)]
        p=low+low[::-1]
        # Construct a canonical ordinary decimal integer, with (low, high) digit-sums p.
        ds=[0]*len(p)
        for i,x in enumerate(low):ds[i]=x-min(x,9);ds[-1-i]=min(x,9)
        n=sum(d*10**i for i,d in enumerate(ds))
        assert n>=10**(2*half-1)
        for t in range(steps+1):
            digits=digits_of(n)
            pair=[digits[i]+digits[-1-i] for i in range(len(digits))]
            assert pair==p,(off,sh,t,'pair mismatch')
            if t==steps:break
            n=n+int(str(n)[::-1])
            p,g=step(p)
            assert g==(t+1)%2,(off,sh,t,'overflow mismatch')
        out.append({'offset':off,'shift':sh,'steps':steps,'initial_digits':2*half,'final_digits':len(digits),'pairword_verified_all_steps':True})
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--scc',default='calculation/decimal_frontier/lattice_formats/p8_scc.txt');ap.add_argument('--output',default='');a=ap.parse_args()
    out=replay(a.scc)
    if a.output:open(a.output,'w').write(json.dumps(out,indent=2)+'\n')
