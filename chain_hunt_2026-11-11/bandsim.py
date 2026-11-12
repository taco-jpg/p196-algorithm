# folded band+centre simulator with imposed clock and a periodic-lattice reservoir on the left
def step(s, odd, g, m, B=10):
    """s: list of pair sums, outer->inner. odd: True if innermost entry is a middle digit (s=2x). m: lattice period at left."""
    K=len(s)-1
    # low carries with periodic reservoir at the left
    c=[0]*(K+2)
    for it in range(3):
        for j in range(K+1):
            c[j+1]=1 if s[j]+c[j]>=B else 0
        c0=c[m]
        if c0==c[0]: break
        c[0]=c0
    d=[0]*(K+1)
    d[K]= c[K] if odd else c[K+1]
    for j in range(K,0,-1):
        d[j-1]=1 if s[j]+d[j]>=B else 0
    a=[(s[j]+c[j])%B for j in range(K+1)]
    z=[(s[j]+d[j])%B for j in range(K+1)]
    if g==0:
        return [a[j]+z[j] for j in range(K+1)], odd
    ns=[a[0]+z[m-1]]+[a[j]+z[j-1] for j in range(1,K+1)]
    if not odd:
        ns.append(2*z[K]); return ns, True
    else:
        return ns, False
if __name__=='__main__':
    V=[11,8,5]
    for rot in range(3):
        Vr=V[rot:]+V[:rot]
        for ph in range(4):
            clock=[1 if (t+ph)%4==0 else 0 for t in range(48)]
            s=Vr*12+[13,2]; odd=True
            s0=list(s)
            hist=[]
            for t in range(24):
                s,odd=step(s,odd,clock[t],3)
                hist.append((list(s[-8:]),odd))
            ok = (s[-(len(s0)):]==s0) and odd and len(s)==len(s0)+3
            print('rot',rot,'phase',ph,'after 24: tail',s[-10:],'odd',odd,'len+',len(s)-len(s0),'RETURN' if ok else '')
            if ok:
                s=list(s0); odd=True
                print('   t=0 ',s[-9:])
                for t in range(24):
                    s,odd=step(s,odd,clock[t],3)
                    print('   t=%2d g=%d'%(t+1,clock[t]),s[-10:],'mid' if odd else '')
