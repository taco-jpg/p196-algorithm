#!/usr/bin/env python3
"""Build the eight-phase decimal exterior using coefficient normalization."""
import json
from pathlib import Path
B = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def step(p):
    d=[]; c=0
    for x in p:
        s=x+c
        d.append(s%10)
        c=s//10
    if c: d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],c
def run():
    half=B+W*20
    p=half+half[::-1]
    bs=[];ws=[];ov=[]
    for t in range(16):
        b,w=p[:39],p[39:59]
        if t<8:
            bs.append(b);ws.append(w)
        else:
            assert b==bs[t-8] and w==ws[t-8],t
        for i in range(39,39+15*20):
            assert p[i]==ws[t%8][(i-39)%20],(t,i)
        p,g=step(p);ov.append(g)
    assert ov==[1,0,1,0,1,0,1,0]*2
    dat={"base":10,"B0":B,"W0":W,"phase_B":bs,"phase_W":ws,"gammas":ov[:8],
         "source":"period-8 rec0 SCC, first39 spatial columns and 20-column bulk; independently sampled with coefficient normalizer"}
    here=Path(__file__).resolve().parent
    (here/"phase.json").write_text(json.dumps(dat,indent=2)+"\n")
    a=["// GENERATED from build_phase.py, checked 16 temporal transitions.",
       "#pragma once","#include <array>",
       "inline constexpr std::array<int,39> B0 = {"+",".join(map(str,B))+"};",
       "inline constexpr std::array<int,20> W0 = {"+",".join(map(str,W))+"};"]
    for label,rows,width in [("B",bs,39),("W",ws,20)]:
        a.append(f"inline constexpr std::array<std::array<int,{width}>,8> PHASE_{label} = {{{{")
        a.extend("    {"+",".join(map(str,v))+"}," for v in rows)
        a.append("}};")
    (here/"phase.h").write_text("\n".join(a)+"\n")
    print("PASS eight-phase bulk: 16 transitions, 15 repeated bulk periods per phase")
if __name__=="__main__":run()
