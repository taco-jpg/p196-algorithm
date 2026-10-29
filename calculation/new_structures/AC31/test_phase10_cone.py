#!/usr/bin/env python3
"""One-step soundness tested on 15,000 genuine physical sources."""
from pathlib import Path
import sys,random
from phase10_cone import successors,realize,pair,load,enclosure,normalize
def main(path):
    rng=random.Random(0xAC31)
    for _ in range(15000):
        L=rng.randrange(2,40)
        a=[rng.randrange(19) for _ in range(L)]
        a[0]=rng.randrange(1,19)
        mid=[rng.randrange(19) for _ in range(rng.randrange(30))]
        P=a+mid+mid[::-1]+a[::-1]
        N=realize(P);NN=N+int(str(N)[::-1])
        gamma=len(str(NN))-len(str(N))
        assert (pair(NN)[:L-1],gamma) in successors(tuple(a))
    ports={(v,normalize((a,b,9,8)[::-1],v)[1])
           for a in range(1,19) for b in range(19) for v in (0,1)}
    assert ports=={(0,0),(0,1),(1,0),(1,1)}
    clock,B,W=load(path)
    states,rows=enclosure(B[10],W[10],clock)
    assert len(rows)==120 and len(states[120])==1
    assert max(x[2] for x in rows)==2
    print('PASS: 15000 true one-step cases, all inlet/gamma pairs, 120-layer phase10 enclosure')
if __name__=='__main__':main(Path(sys.argv[1]))
