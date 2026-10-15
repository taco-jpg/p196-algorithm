import json, itertools
def T(n): return n+int(str(n)[::-1])
def pair_word(n):
    d=[int(c) for c in str(n)][::-1]; L=len(d); return [d[i]+d[L-1-i] for i in range(L)]
def fp(s,inner):
    k=len(s); low,carry=[],0
    for v in s:
        carry,d=divmod(v+carry,10); low.append(d)
    high,c=[0]*k,inner
    for i in range(k-1,-1,-1):
        c,high[i]=divmod(s[i]+c,10)
    if c: return (1+low[0],)+tuple(low[i]+high[i-1] for i in range(1,k))
    return tuple(a+b for a,b in zip(low,high))
n=196
for _ in range(100): n=T(n)
for k in (4,5):
    w0=tuple(pair_word(n)[:k]); F={w0}; st=[w0]
    while st:
        w=st.pop()
        for c in (0,1):
            p=fp(w,c)
            if p not in F: F.add(p); st.append(p)
    base=json.load(open('/home/claude/p196-algorithm/proofs/contributions/2026-10-15-seven-column-prefix/baseline_396.json'))
    S3=set(base)|{'739'}
    S4=set(json.load(open('/home/claude/work124/screen/four_digit_targets.json')))
    words=[w for w in itertools.product(range(10),repeat=k) if w[0]>0]
    def anc(w):
        s=''.join(map(str,w)); return s[:3] in S3 or s[:4] in S4
    fwd=[w for w in words if w not in F]
    a=sum(1 for w in words if anc(w)); f=len(fwd); both=sum(1 for w in fwd if anc(w))
    print(f'k={k}: words {len(words)} ancestry-excluded {a} forward-excluded {f} both {both} union {a+f-both} ({(a+f-both)/len(words):.3f}) forward-only {f-both}')
