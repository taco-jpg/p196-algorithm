import sys, itertools
def T(n): return n + int(str(n)[::-1])
def pair_word(n):
    d=[int(c) for c in str(n)][::-1]; L=len(d); return [d[i]+d[L-1-i] for i in range(L)]
def forward_prefixes(s):
    k=len(s); low,carry=[],0
    for v in s:
        carry,d=divmod(v+carry,10); low.append(d)
    out=set()
    for inner in (0,1):
        high,c=[0]*k,inner
        for i in range(k-1,-1,-1):
            c,high[i]=divmod(s[i]+c,10)
        if c: p=(1+low[0],)+tuple(low[i]+high[i-1] for i in range(1,k))
        else: p=tuple(a+b for a,b in zip(low,high))
        out.add(p)
    return out
k=int(sys.argv[1]); t0=int(sys.argv[2])
n=196
for _ in range(t0): n=T(n)
w0=tuple(pair_word(n)[:k])
seen={w0}; st=[w0]
while st:
    w=st.pop()
    for p in forward_prefixes(w):
        if p not in seen: seen.add(p); st.append(p)
ov=[w for w in seen if w[0]==11 and all(x in (0,11) for x in w)]
dig=[w for w in seen if all(x<=9 for x in w)]
print('k',k,'|F|',len(seen),'overflow-target words in F',len(ov),ov[:8],'digit words',len(dig),'of',9*10**(k-1))
# leading-digit distribution of reachable digit words
from collections import Counter
print(sorted(Counter(w[0] for w in dig).items()))
