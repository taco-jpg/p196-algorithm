# Agent #102 literal-integer spot control for Agent #105 residue trap (semantics only; Lean is the proof).
import json, random
def T(n): return n+int(str(n)[::-1])
random.seed(105); seeds=[196,89,10911,1,2,9,10,59]+[random.randint(1,10**8) for _ in range(40)]
checked=0
for n0 in seeds:
    orb=[n0]
    for _ in range(11+4*40): orb.append(T(orb[-1]))
    for B in range(0,41):
        ok=False
        for t in range(6+4*B, 12+4*B):
            m=orb[t]; L=len(str(m))
            if L%2==0 and L>=B and m%11==0:
                r=m%99; a=9 if r==0 else r//11
                p=a+a*10**(L-1); s=str(p)
                assert len(s)==L and s==s[::-1] and p%99==r
                ok=True; break
        assert ok,(n0,B); checked+=1
print(json.dumps(dict(seed_B_pairs=checked,status="PASS")))
