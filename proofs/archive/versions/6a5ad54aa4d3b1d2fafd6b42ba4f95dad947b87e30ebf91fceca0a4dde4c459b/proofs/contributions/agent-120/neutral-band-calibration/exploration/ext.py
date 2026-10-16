import sys, itertools
def make(b):
    K=lambda c: 1 if c>=b else 0
    t=lambda c: c-(b-1)*K(c)
    def norm(word,cin):
        out=[];c=cin
        for v in word:
            s=v+c; out.append(s%b); c=s//b
        return out,c
    def step(c,B):
        m=len(B); kc=K(c); tc=t(c)
        D,e0=norm(B,0)
        u0=c+e0-b*kc
        # high block: rev(B) low-to-high = B[m-1],...,B[0], incoming kc
        DR,g=norm(list(reversed(B)),kc)   # DR[j] digit of B[m-1-j]
        eps=[DR[m-1-i] for i in range(m)] # eps[i] digit at mirror of B[i]
        if g==0:
            Br=[D[i]+eps[i] for i in range(m)]+[u0+tc]
        else:
            Br=[D[0]+1]+[D[i]+eps[i-1] for i in range(1,m)]+[u0+(eps[m-1] if m>0 else 1)] if m>0 else [u0+1]
        c2=2*tc
        while Br and Br[-1]==c2: Br.pop()
        return c2,tuple(Br),g
    return step,t,K
def search(b,cap):
    step,t,K=make(b)
    phases=[c for c in range(1,2*b-1) if c!=b-1]
    # canonical states: B entries 0..2b-2, first positive if nonempty, last != c (trimmed)
    color={}
    cycles=[]
    def states():
        for c in phases:
            for m in range(0,cap+1):
                for B in itertools.product(range(2*b-1),repeat=m):
                    if m and (B[0]==0 or B[-1]==c): continue
                    yield (c,B)
    # functional graph: each state has one successor; detect cycles among states that stay within cap
    nxt={}
    for s in states():
        c,B=s
        n=step(c,B)
        nxt[s]=(n[0],n[1])
    # follow
    seen={}
    found=set()
    for s in nxt:
        path=[];x=s
        while x in nxt and x not in seen:
            seen[x]=s; path.append(x); x=nxt[x]
        if x in nxt and seen.get(x)==s:
            # cycle
            i=path.index(x); cyc=tuple(path[i:])
            found.add(min(cyc))
            cycles.append(cyc)
    return cycles
if __name__=='__main__':
    for b in range(2,31):
        cap = 6 if b<=5 else (4 if b<=8 else (3 if b<=16 else 2))
        cyc=search(b,cap)
        print(b,'cap',cap,'cycles',len(cyc), [ (len(c), c[0]) for c in cyc[:3]], flush=True)
