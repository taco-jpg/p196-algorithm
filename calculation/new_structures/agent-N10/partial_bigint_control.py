#!/usr/bin/env python3
"""Independent actual decimal-integer one-step guards for all 20 cut residues."""
import json,random,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
p=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def run():
    rng=random.Random(20000136);count=0
    for t in range(8):
        B=p["phase_B"][t];W=p["phase_W"][t]
        B2=p["phase_B"][(t+1)%8];W2=p["phase_W"][(t+1)%8]
        for j in range(20):
            for r in (1,2,3):
                for a in range(8):
                    c=[rng.randrange(19) for _ in range(rng.randrange(12))]
                    c=c+([2*rng.randrange(10)] if a%2 else [])+c[::-1]
                    h=B+W*r+W[:j];P=h+c+h[::-1]
                    digits=[0]*len(P)
                    for i in range(len(P)//2):
                        digits[i]=P[i]//2
                        digits[-1-i]=P[i]-digits[i]
                    if len(P)%2:digits[len(P)//2]=P[len(P)//2]//2
                    s="".join(map(str,digits[::-1]))
                    n=int(s);out=str(n+int(s[::-1]))
                    q=[int(out[i])+int(out[-1-i]) for i in range(len(out))]
                    loss=2 if h[-1]==9 else 1
                    end=len(h)-loss
                    assert q[:end]==B2+[W2[i%20] for i in range(end-39)],(t,j,r,a)
                    assert out!=out[::-1],(t,j,r,a)
                    count+=1
    print("PASS",count,"ordinary bigint partial-cut prefix controls")
if __name__=="__main__":run()
