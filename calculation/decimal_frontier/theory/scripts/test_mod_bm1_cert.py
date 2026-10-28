"""mod-(b-1) charge law on all known certificates: for edge t (B_t,C_t):
   s(B_{t+1}) = 2 s(B_t) + 1 - 2 e1_t   and   s(C_{t+1}) = 2 s(C_t) - 2(1-2e1_t)  (mod b-1);   sigma_t = 2 s(B_t)+s(C_t), sigma_{t+1}=2 sigma_t."""
import sys, math; sys.path.insert(0,'/home/claude/research/w2_theory')
import lib, mirror as m
certs=list(m._lean_certs())
certs.append((20,lib.parse_lean_certs('/home/claude/r/lean/P196/Agent116Base20Certificate/Certificate.lean')))
for b,es in certs:
    p=len(es); M=b-1; ok1=ok2=ok3=True
    for t in range(p):
        B,C=es[t][0],es[t][1]; B2,C2=es[(t+1)%p][0],es[(t+1)%p][1]
        e=m.e1(b,B); eps=1-2*e
        ok1&= (sum(B2)-2*sum(B)-eps)%M==0
        ok2&= (sum(C2)-2*sum(C)+2*eps)%M==0
        ok3&= ((2*sum(B2)+sum(C2))-2*(2*sum(B)+sum(C)))%M==0
    E=int(''.join(str(m.e1(b,e[0])) for e in es),2)
    print(f"b={b} p={p} lawB={ok1} lawC={ok2} sigma={ok3}  gcd(2^p-1,b-1)={math.gcd(2**p-1,M)}  E mod gcd={E%math.gcd(2**p-1,M)}")
