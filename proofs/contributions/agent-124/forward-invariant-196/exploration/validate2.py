import sys
def T(n): return n + int(str(n)[::-1])
def pal(n): s=str(n); return s==s[::-1]
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
def closure(w0):
    seen={w0}; st=[w0]
    while st:
        w=st.pop()
        for p in forward_prefixes(w):
            if p not in seen: seen.add(p); st.append(p)
    return seen
for seed in (89, 187, 10911, 1186060307891929990, 4782, 1993, 7, 79):
    n=seed; orbit=[n]
    for _ in range(400):
        n=T(n); orbit.append(n)
        if pal(n): break
    t=len(orbit)-1
    P=orbit[-1]
    if not pal(P): print(seed,'no palindrome within 400'); continue
    for k in (3,4,5):
        # earliest t0 with width >= k
        t0=next((i for i,x in enumerate(orbit[:-1]) if len(str(x))>=k), None)
        if t0 is None: continue
        F=closure(tuple(pair_word(orbit[t0])[:k]))
        last=tuple(pair_word(orbit[-2])[:k])
        lead=tuple(int(c) for c in str(P)[:k])
        print(seed,'k',k,'t0',t0,'T',t,'last-pred projection in F:', last in F, '| last proj', last, 'lead digits', lead, '|F|', len(F))
