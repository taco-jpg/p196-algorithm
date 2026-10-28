import sys
from fc_graph import edges
# find integer potentials: for all edges (q,q2,g): lo-type: psi(q2)-psi(q) >= 2g-1  (=> 2G<=p);   phi(q2)-phi(q) <= 4g-1 (=> p<=4G)
def solve(b, a, c, sign):
    # constraints psi(q2) - psi(q) >= w  with w = a*g - c   (sign=+1)   ; or <= for sign=-1
    E=edges(b); n=2*b-2
    # longest-path potentials: psi(q2) >= psi(q) + w ; Bellman-Ford maximizing from 0
    psi=[0]*(n+1)
    for it in range(n+5):
        ch=False
        for (q,q2,g,h) in E:
            w=(a*g-c)
            if sign==1:
                if psi[q2]<psi[q]+w: psi[q2]=psi[q]+w; ch=True
            else:
                # psi(q2) <= psi(q)+w  -> psi(q) >= psi(q2)-w
                if psi[q]<psi[q2]-w: psi[q]=psi[q2]-w; ch=True
        if not ch: return psi
    return None
b=int(sys.argv[1]) if len(sys.argv)>1 else 10
psi=solve(b,2,1,1)
print('psi (2G<=p): ',{q:psi[q] for q in range(1,2*b-1)} if psi else None)
phi=solve(b,4,1,-1)
print('phi (p<=4G): ',{q:phi[q] for q in range(1,2*b-1)} if phi else None)
