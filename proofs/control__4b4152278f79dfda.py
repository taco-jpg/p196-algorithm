# Independent literal-integer control of the statement of RunAncestry.descendant_step
# (semantics check only; the Lean proof is the authority). Enumerates all integers of width 1..6.
import itertools, json, hashlib
def colsum(n):
    s=str(n)[::-1]; L=len(s); d=[int(x) for x in s]
    return [d[i]+d[L-1-i] for i in range(L)]
def carries(q):
    c=[0]
    for x in q: c.append((x+c[-1])//10)
    return c
reset=lambda c: 1 if c==18 else 0
checked=0; runs=0
for L in range(1,7):
    seen=set()
    for n in range(10**(L-1),10**L):
        q=tuple(colsum(n))
        if q in seen: continue
        seen.add(q)
        m=n+int(str(n)[::-1]); q2=colsum(m); L2=len(q2)
        car=carries(q)
        for c in (0,18):
            i=0
            while i<L:
                if q[i]!=c: i+=1; continue
                a=i
                while i<L and q[i]==c: i+=1
                b=i; runs+=1
                if car[L]==0:
                    d=(a if car[a]==reset(c) else a+1, b if car[L-b]==reset(c) else b-1)
                else: d=(a+1,b)
                for j in range(a,b):
                    assert (q2[j]==c)==(d[0]<=j<d[1]),(n,c,a,b,j)
                if d[0]<d[1]:
                    assert all(q2[j]==c for j in range(*d))
                    assert d[0]==0 or q2[d[0]-1]!=c
                    assert d[1]==L2 or q2[d[1]]!=c
                assert d[1]-d[0] if d[1]>d[0] else 0 <= b-a-car[L]
                assert max(d[1]-d[0],0)+car[L] <= b-a
        checked+=1
print(json.dumps(dict(widths="1..6",distinct_words=checked,maximal_runs=runs,status="PASS")))
