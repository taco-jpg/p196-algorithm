#!/usr/bin/env python3
"""Independent actual Python BIGINT replay of a moving decimal pairword frontier."""
import json,sys
from pathlib import Path
sys.set_int_max_str_digits(0)
PH=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
B,W=PH["B0"],PH["W0"]
def seed(k,core):
    h=B+W*k
    if core==1:h+=[0,18]
    if core==2:h+=[2,4]
    if core==3:h+=[9,6]
    lo=[p//2 for p in h]
    hi=[p-p//2 for p in h]
    return int("".join(map(str,hi+lo[::-1])))
def front(n,t):
    s=str(n)
    p=[int(s[i])+int(s[-1-i]) for i in range(len(s)//2)]
    b=PH["phase_B"][t%8]
    w=PH["phase_W"][t%8]
    h=next((i for i,x in enumerate(p)
            if x!=(b[i] if i<39 else w[(i-39)%20])),len(p))
    assert h>=59
    win="".join("0123456789ABCDEFGHI"[x] for x in p[h-40:h+80])
    if t>=1082:assert len(win)==120
    return h,win
def run(k=300,core=0,steps=1400):
    n=seed(k,core);seen={};checked=0
    for t in range(steps+1):
        s=str(n)
        assert s!=s[::-1],("palindrome",t)
        h,win=front(n,t)
        if t>=1170:
            prev_h,prev_win=seen[t-88]
            assert prev_h-h==20 and prev_win==win,("glider mismatch",t)
            checked+=1
        if t>=1082:seen[t]=(h,win)
        if t<steps:n+=int(s[::-1])
    print(f"PASS independent Python BIGINT k={k} core={core} "
          f"steps={steps} verified_glider_pairs={checked}")
if __name__=="__main__":
    run(int(sys.argv[1]) if len(sys.argv)>1 else 300,
        int(sys.argv[2]) if len(sys.argv)>2 else 0,
        int(sys.argv[3]) if len(sys.argv)>3 else 1400)
