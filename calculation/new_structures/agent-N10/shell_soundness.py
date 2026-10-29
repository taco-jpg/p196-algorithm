#!/usr/bin/env python3
"""Finite symbolic audit of the universal r -> r-1 decimal shell rule."""
from symbolic_pump import P,word,pairs
def run():
    count=0
    for t in range(8):
        nextB=P["phase_B"][(t+1)%8]
        nextW=P["phase_W"][(t+1)%8]
        for r in (1,2,3,4):
            for u in (0,1):
                for m in (0,1,2,3,7,17):
                    d,c,g=word(t,r,u,m)
                    q=pairs(d)
                    want=[(x,()) for x in nextB+nextW*(r-1)]
                    assert q[:len(want)]==want,(t,r,u,m)
                    assert g==P["gammas"][t],(t,r,u,m,g)
                    count+=1
    odd=[sum(x%2 for x in row) for row in P["phase_B"]]
    assert min(odd)>0
    print("PASS",count,"independent symbolic centre shell checks")
    print("odd exterior coefficient counts:",odd)
if __name__=="__main__":run()
