#!/usr/bin/env python3
"""List the IMPRIMITIVE F1 survivors g = u^m (m>=2, u primitive necklace of length l = p/m) for p in [PMIN,PMAX], base 10.
F1 = cyclic acceptance by the first-coordinate NFA (EXTERIOR.md 2.1): exists q with q ->(u^m) q.
Output: lists_impr/fc_b10_p{p}_G{G}.txt, words written as the necklace-minimal rotation of u^m (= (min rotation of u)^m).
usage: impr_list.py PMIN PMAX OUTDIR"""
import sys, os
b=10; NS=2*b-2
succ={0:[0]*NS,1:[0]*NS}
for q in range(1,NS+1):
    for r in (0,1):
        g=(q+r)//b
        if g>1: continue
        q2 = 2*q+r if g==0 else (q%b)+1
        if 1<=q2<=NS: succ[g][q-1] |= 1<<(q2-1)
def mat(word):
    # rows[s] = set of states reachable from s reading word
    R=[1<<s for s in range(NS)]
    for a in word:
        nr=[]
        for m in R:
            o=0
            while m:
                c=(m&-m).bit_length()-1; m&=m-1; o|=succ[a][c]
            nr.append(o)
        R=nr
    return R
def mul(A,B):
    out=[]
    for m in A:
        o=0
        while m:
            c=(m&-m).bit_length()-1; m&=m-1; o|=B[c]
        out.append(o)
    return out
def lyndon(n):
    # Duval-style generation of Lyndon words of length exactly n (primitive necklaces, min rotation)
    w=[-1]
    while w:
        w[-1]+=1; m=len(w)
        if m==n: yield tuple(w)
        while len(w)<n: w.append(w[len(w)-m])
        while w and w[-1]==1: w.pop()
PMIN,PMAX,OUT=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
os.makedirs(OUT,exist_ok=True)
for p in range(PMIN,PMAX+1):
    cnt={}
    files={}
    for l in range(1,p//2+1):
        if p%l: continue
        m=p//l
        for u in lyndon(l):
            if '00000' in ''.join(map(str,u+u)): continue
            G=sum(u)*m
            if not (2*G<=p<=4*G): continue
            M=mat(u); P=M
            for _ in range(m-1): P=mul(P,M)
            if any(P[s]>>s&1 for s in range(NS)):
                w=''.join(map(str,u))*m
                cnt[G]=cnt.get(G,0)+1
                if G not in files: files[G]=open(f'{OUT}/fc_b10_p{p}_G{G}.txt','w')
                files[G].write(w+'\n')
    for f in files.values(): f.close()
    print(f'p={p} imprimitive F1 survivors={sum(cnt.values())} byG:',' '.join(f'{k}:{v}' for k,v in sorted(cnt.items())),flush=True)
