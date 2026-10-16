import random, sys, json
CLOCKS={'seven_4':(4,8,16,7,15,6,13),'seven_1':(1,2,4,9,18,9,10)}
def outer(n):
    s=str(n); return int(s[0])+int(s[-1])
def longest(n, clock, steps=400):
    # longest run of consecutive times t..t+m with outer pair sum following clock at some phase
    best=0; run=0; phase=None
    vals=[]
    for t in range(steps):
        s=str(n); 
        if s==s[::-1]: vals.append(None); break
        vals.append(int(s[0])+int(s[-1])); n=n+int(s[::-1])
    i=0; L=len(vals)
    for start in range(L):
        v=vals[start]
        if v is None or v not in clock: continue
        for ph in [k for k,c in enumerate(clock) if c==v]:
            m=0
            while start+m+1<L and vals[start+m+1] is not None and vals[start+m+1]==clock[(ph+m+1)%7]: m+=1
            best=max(best,m)
    return best
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
res={k:[] for k in CLOCKS}
for trial in range(3000):
    d=random.randint(6,30)
    n=random.randint(10**(d-1),10**d-1)
    for k,c in CLOCKS.items(): res[k].append(longest(n,c,300))
for k in res:
    v=sorted(res[k]); print(k,'max steps',v[-1],'top',v[-10:],'mean',sum(v)/len(v))
