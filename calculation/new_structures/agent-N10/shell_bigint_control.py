#!/usr/bin/env python3
"""Independent true decimal big-integer check of the one-step shell invariant."""
import json,random,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
ph=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def real_seed(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        p=P[i];d[i]=p//2;d[-1-i]=p-p//2
    if len(P)%2:d[len(P)//2]=P[len(P)//2]//2
    return int("".join(str(x) for x in d[::-1]))
def run():
    rng=random.Random(20001196474);tested=0
    for t in range(8):
        b=ph["phase_B"][t];w=ph["phase_W"][t]
        bn=ph["phase_B"][(t+1)%8];wn=ph["phase_W"][(t+1)%8]
        for r in (1,2,3,4):
            for j in range(100):
                half=[rng.randrange(19) for _ in range(rng.randrange(25))]
                core=half+([rng.randrange(10)*2] if j%2 else [])+half[::-1]
                side=b+w*r;P=side+core+side[::-1]
                n=real_seed(P)
                s=str(n);out=str(n+int(s[::-1]))
                q=[int(out[i])+int(out[-1-i]) for i in range(len(out))]
                assert q[:39+20*(r-1)]==bn+wn*(r-1),(t,r,j)
                assert out!=out[::-1],(t,r,j)
                tested+=1
    print(f"PASS {tested} genuine decimal one-step shell controls")
if __name__=="__main__":run()
