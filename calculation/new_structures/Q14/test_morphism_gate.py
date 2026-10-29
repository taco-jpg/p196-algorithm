#!/usr/bin/env python3
"""Small exhaustive sanity test; the mathematical theorem is proved separately."""
from itertools import product
from morphism_gate import gate, exact_increment_bound
A="AB"; words=["A","B","AA","AB","BA","BB"]
count=accepted=0
for image_a,image_b in product(words,repeat=2):
    sigma={"A":image_a,"B":image_b}
    for seed in words:
        ok,reason,_=gate(sigma,seed)
        counts={a:seed.count(a) for a in A}; deltas=[]
        for _ in range(100):
            deltas.append(sum(counts[a]*(len(sigma[a])-1) for a in A))
            nxt={a:0 for a in A}
            for a,image in sigma.items():
                for b in image: nxt[b]+=counts[a]
            counts=nxt
        if ok:
            bound,checked,period=exact_increment_bound(sigma,seed)
            assert bound==max(deltas[:checked]),(sigma,seed,bound,checked)
            assert all(deltas[i]==deltas[i+period] for i in range(3*len(A),100-period)),(sigma,seed,period)
            accepted+=1
        else:
            assert max(deltas[50:])>max(deltas[:10]),(sigma,seed,reason,deltas)
        count+=1
print(f"PASS: {count} two-letter morphism/seed cases; {accepted} bounded cases")
