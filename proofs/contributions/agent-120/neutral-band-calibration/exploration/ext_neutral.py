"""Autonomous exterior map for a persistent neutral outermost band (exploratory)."""
import sys, itertools
def make(b):
    n=b-1
    def norm(word,cin):
        out=[];c=cin
        for v in word:
            s=v+c; out.append(s%b); c=s//b
        return out,c
    def E(B):
        s=len(B)
        D,e1=norm(list(B),0)
        x=n*(1-e1); e2=1-e1
        DR,g=norm(list(reversed(B)),e2)   # DR[j] digit of position j in the top block (low to high)
        if g==0:
            Bp=[D[i]+DR[s-1-i] for i in range(s)]
        else:
            low=D+[x]; high=[1]+list(reversed(DR))
            Bp=[low[i]+high[i] for i in range(s+1)]
        trim=0
        while Bp and Bp[-1]==n: Bp.pop(); trim+=1
        return tuple(Bp), g, trim
    return E
def orbit_stats(b, B, steps):
    E=make(b); seen={B:0}; cur=B; lens=[]
    for t in range(1,steps+1):
        cur,g,tr=E(cur)
        lens.append(len(cur))
        if cur in seen: return ('cycle', seen[cur], t, cur)
        seen[cur]=t
        if len(cur)>60: return ('grow', t, len(cur))
    return ('open', steps, len(cur))
if __name__=='__main__':
    b=int(sys.argv[1]); maxlen=int(sys.argv[2])
    cycles=set(); grow=0; opened=0
    for m in range(0,maxlen+1):
        for B in itertools.product(range(2*b-1),repeat=m):
            if m and (B[0]==0 or B[-1]==b-1): continue
            r=orbit_stats(b,tuple(B),3000)
            if r[0]=='cycle':
                # extract the cycle's canonical rep
                E=make(b); cur=r[3]; cyc=[cur]
                while True:
                    cur=E(cur)[0]
                    if cur==r[3]: break
                    cyc.append(cur)
                cycles.add(min(cyc))
            elif r[0]=='grow': grow+=1
            else: opened+=1
    print('base',b,'maxlen',maxlen,'distinct cycles',len(cycles),'grow',grow,'open',opened)
    E=make(b)
    for c in sorted(cycles, key=len)[:10]:
        cur=c; seq=[c]
        for _ in range(12):
            cur=E(cur)[0]; seq.append(cur)
            if cur==c: break
        print('  cycle',seq)
