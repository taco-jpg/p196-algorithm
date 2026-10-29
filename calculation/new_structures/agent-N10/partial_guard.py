#!/usr/bin/env python3
"""Symbolic check for universal 1/2-column erosion at every spatial cut."""
from symbolic_pump import P,norm,pairs
def run():
    checks=0
    for t in range(8):
        b=P["phase_B"][t];w=P["phase_W"][t]
        bn=P["phase_B"][(t+1)%8];wn=P["phase_W"][(t+1)%8]
        assert all(not(w[i]==w[(i+1)%20]==9) for i in range(20))
        for k in (1,2,3):
            for j in range(20):
                side=b+w*k+w[:j];h=len(side)
                loss=2 if side[-1]==9 else 1
                for u in (0,1):
                    low,carry=norm(side,0)
                    high,g=norm(side[::-1],u)
                    for m in (0,1,2,7,17):
                        d=[(x,()) for x in low]+[(0,(i,)) for i in range(m)]+[(x,()) for x in high]
                        if g:d.append((g,()))
                        q=pairs(d)
                        expect=[(x,()) for x in bn+[wn[i%20] for i in range(h-loss-39)]]
                        assert q[:h-loss]==expect,(t,k,j,u,m)
                        assert g==P["gammas"][t],(t,k,j,u,m)
                        checks+=1
    print("PASS",checks,"symbolic partial-cut guard cases")
if __name__=="__main__":run()
