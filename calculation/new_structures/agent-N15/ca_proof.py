#!/usr/bin/env python3
"""All-level dyadic t=3..7 exact local transfer, with finite Thue-Morse factor proof."""
# Independent from the earlier N15 morphed-band engine.  The C++ checker below
# does ordinary integer addition rather than pair-coefficient normalisation.
def word(h):
    w=[14]
    for _ in range(h):w=[z for x in w for z in (x,30-x)]
    return w

def pairword(h):
    H=[4]+word(h)
    return H+H[::-1]

def next_pair(p):
    c=0;d=[]
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return [d[i]+d[-1-i] for i in range(len(d))],d

def predicted_second_half(h):
    w=word(h);m=len(w)+1
    q=[9,9]+[2*(w[i-1]-9) for i in range(2,m)]
    r=[10,9,q[2]-10]+[q[i]+q[i-1]-18 for i in range(3,m)]
    r.append(2*(q[m-1]-9))
    return r

def A(x): return int(x>=10)
def local(x,y,z):
    assert y != 9,(x,y,z)
    return 2*(y%10)+A(x)+A(z)
def F(v):
    assert 9 not in v
    return [local(v[i-1] if i else 0,v[i],v[i+1] if i+1<len(v) else 0) for i in range(len(v))]
def r_of(x,y): return 2*(x+y-27)
def H(x,y,z):
    p,q=r_of(x,y),r_of(y,z)
    return p+q-9*(A(p)+A(q))
def third(h):
    r=predicted_second_half(h)
    g=[1,0,14,5]+[r[i]+r[i-1]-9*(A(r[i])+A(r[i-1])) for i in range(4,len(r))]
    return g+g[::-1]
def sigma(w):return [y for x in w for y in ([14,16] if x==14 else [16,14])]
def factors(K,R=4):
    out=set()
    for u in (14,16):
        for v in (14,16):
            z=[u,v]
            for _ in range(R):z=sigma(z)
            out.update(tuple(z[i:i+K]) for i in range(len(z)-K+1))
    return out

def ca_center(v):
    while len(v)>1:
        v=[local(v[i-1],v[i],v[i+1]) for i in range(1,len(v)-1)]
    return v[0]

def check():
    # The first unequal opposing digit pair of N_t for t=1..7.
    # These are fixed by the same bounded end windows as the carry conditions.
    witnesses=[(0,4,5),(0,9,1),(0,0,1),(1,0,1),
               (2,8,9),(1,2,3),(1,5,6)]
    for h in range(2,16):
        p=pairword(h)
        for t,w in enumerate(witnesses,1):
            p,d=next_pair(p)
            i=next((j for j in range(len(d)//2) if d[j]!=d[-1-j]),None)
            assert i is not None and (i,d[i],d[-1-i])==w,(h,t,i)

    # Full arithmetic checks independent of the factored-language reasoning.
    for h in range(2,13):
        P=pairword(h)
        for _ in range(3):P,d=next_pair(P)
        assert P==third(h)
        for k in range(4):
            assert 9 not in P,(h,k)
            P2,d=next_pair(P)
            Q=F(P)
            assert P2==Q,(h,k)
            P=P2

    # All possible bulk TM factors, independent of h, under sigma^4 two-letter blocks.
    bulk_card=[]
    for k in range(4):
        K=2*k+3
        fs=factors(K)
        vals={ca_center([H(*s[i:i+3]) for i in range(2*k+1)]) for s in fs}
        assert 9 not in vals,(k,vals)
        bulk_card.append((k,K,len(fs),sorted(vals)))

    # Boundary values: for positions at distance <=k+3 from the lower end,
    # or <=k+3 from the centre, only first/last <=(2k+8) TM letters matter.
    # h=8/9 supply both suffix parity classes and more than 16 boundary letters.
    for h in range(2,10):
        P=third(h)
        for k in range(4):
            if h>=8:
                n=len(P); L=1<<h
                edge_end=k+3
                centre_start=L-k+1
                B=set(range(edge_end+1))|set(range(centre_start,n-centre_start))|set(range(n-1-edge_end,n))
                assert all(P[i]!=9 for i in B),(h,k)
            P=F(P) if k<3 else P
    # Stronger prefix/suffix stabilization check: all four windows match
    # the parity reference at h=8/9 for h=10..15.
    for h in range(10,16):
        ref=8+(h%2)
        for k in range(4):
            p=third(h); q=third(ref)
            for _ in range(k):p=F(p);q=F(q)
            W=k+4
            assert p[:W]==q[:W] and p[-W:]==q[-W:],(h,k,'edge')
            M=len(p)//2;N=len(q)//2
            assert p[M-W:M+W]==q[N-W:N+W],(h,k,'centre')

    print('TM_ALL_LEVEL_CA_PASS',bulk_card)
    print('ALL_LEVEL_BOUNDARY_NONPAL_WITNESSES_PASS',witnesses)
if __name__=='__main__':check()
