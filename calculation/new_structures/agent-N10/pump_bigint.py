#!/usr/bin/env python3
"""Independent arbitrary-precision INTEGER verification of whole-word pumping."""
import sys,json
from pathlib import Path
sys.set_int_max_str_digits(0)
from independent_bigint import seed
W=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())["phase_W"]
def coeff(n):
    s=str(n)
    return [int(s[i])+int(s[-1-i]) for i in range(len(s))],s
def run(k=300,steps=1000):
    a,b=seed(k),seed(k+1)
    for t in range(steps+1):
        pa,sa=coeff(a);pb,sb=coeff(b)
        expected=pa[:39]+W[t%8]+pa[39:-39]+W[t%8][::-1]+pa[-39:]
        assert len(sb)==len(sa)+40 and pb==expected,("pump mismatch",t)
        if t in (0,1,100,1000,steps):
            print("bigint full pump",t,len(sa),len(sb))
        if t<steps:
            a+=int(sa[::-1]);b+=int(sb[::-1])
    print("PASS full-pairword bigint pump",k,steps)
if __name__=="__main__":
    run(int(sys.argv[1]) if len(sys.argv)>1 else 300,
        int(sys.argv[2]) if len(sys.argv)>2 else 1000)
