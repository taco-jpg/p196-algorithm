# Verify, edge by edge, the potentials that prove (for base 10) 2G<=p<=4G from the first-coordinate NFA.
from fc_graph import edges
b=10
psi={1:3,2:2,3:2,4:1,5:1,6:1,7:1,8:1,9:1,10:2,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0}
phi={q:-(q.bit_length()-1) for q in range(1,19)}          # phi(q) = -floor(log2 q)
E=edges(b); ok1=ok2=True
for (q,q2,g,h) in E:
    if psi[q2]-psi[q] < 2*g-1: ok1=False; print('psi violated',q,q2,g,h)
    if phi[q2]-phi[q] > 4*g-1: ok2=False; print('phi violated',q,q2,g,h)
print(len(E),'edges;  psi: psi(q2)-psi(q) >= 2g-1  ->  sum over a cycle: 0 >= 2G-p   :',ok1)
print('             phi: phi(q2)-phi(q) <= 4g-1  ->  sum over a cycle: 0 <= 4G-p   :',ok2)
