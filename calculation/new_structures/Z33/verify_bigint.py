#!/usr/bin/env python3
"""Independent arbitrary-precision decimal checks for the phase-9 seam census."""
from __future__ import annotations
import random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

B0 = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W0 = [5,18,4,8,1,15,4,0,5]
GAMMA = [1,0,0,0,1,0,0,0,1,0,0,0]

def pair_step(p):
    carry = 0
    digits = []
    for x in p:
        z = x + carry
        digits.append(z % 10)
        carry = z // 10
    out_digits = digits + ([carry] if carry else [])
    return [out_digits[i] + out_digits[-1-i] for i in range(len(out_digits))], carry

def make_template(q, k, j, u, c, b=B0, w=W0):
    h = b + w*q + j + u*k
    return h + c + h[::-1]

def derive_rows():
    controls = [
        ([5], [9,14,4], [10]),
        ([18,0,1,1,2], [6,9,12], [8,8]),
        ([4,9,14], [8,9,10], [12]),
        ([1,2,3,4,5], [9,16,2], [14,14]),
    ]
    rows0 = None
    for j,u,c in controls:
        p = make_template(14,100,j,u,c)
        rows = []
        for t in range(12):
            rows.append((p[:34], p[34:43]))
            p,g = pair_step(p)
            assert g == GAMMA[t], (t,g)
        if rows0 is None:
            rows0 = rows
        else:
            assert rows == rows0, "root phase rows depend on control"
    assert rows0[0] == (B0,W0)
    assert rows0[1][1] == [10,14,13,12,9,7,10,4,5]
    assert all(w[-1] != 9 for _,w in rows0)
    return rows0

def bulk_step(u, gamma):
    m = len(u)
    def cyclic_low():
        for s in (0,1):
            a=[0]*(m+1); a[0]=s
            for i in range(m): a[i+1]=(u[i]+a[i])//10
            if a[m] == s: return a
        raise AssertionError("no cyclic low carry")
    def cyclic_high():
        for s in (0,1):
            b=[0]*(m+1); b[m]=s
            for i in range(m-1,-1,-1): b[i]=(u[i]+b[i+1])//10
            if b[0] == s: return b
        raise AssertionError("no cyclic high carry")
    a,b=cyclic_low(),cyclic_high()
    z=[]
    for i in range(m):
        lo=(u[i]+a[i])%10
        hi=((u[(i+m-1)%m]+b[i])%10) if gamma else ((u[i]+b[i+1])%10)
        z.append(lo+hi)
    return z

def u_words():
    out=set()
    for a in range(0,19,2):
        base=[9,a,18-a]
        for r in range(3):
            out.add(tuple(base[r:]+base[:r]))
    assert len(out)==30
    return [list(u) for u in sorted(out)]

def digits_from_pairword(p):
    n=len(p); d=[0]*n
    for i in range(n//2):
        s=p[i]
        d[i]=max(0,s-9)
        d[n-1-i]=s-d[i]
        assert 0<=d[i]<=9 and 0<=d[n-1-i]<=9
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1] != 0
    return d

def value_from_digits(d):
    return sum(x*10**i for i,x in enumerate(d))

def pairword_of_int(n):
    ds=list(map(int,str(n)[::-1]))
    return [ds[i]+ds[-1-i] for i in range(len(ds))]

def reverse10(n):
    return int(str(n)[::-1])

def first_non9_state(u):
    for x in u:
        if x != 9: return int(x >= 10)
    raise AssertionError("no non-9 in U")

def high_u(u,j,g):
    start=0 if g else 1
    for d in range(start,start+3):
        x=u[(j+d)%3]
        if x != 9: return int(x >= 10)
    raise AssertionError("U port failed to reset")

def phase_info(rows,q):
    infos=[]
    for ph in range(12):
        pref=rows[ph][0] + rows[ph][1]*q
        c=0
        for x in pref: c=(x+c)//10
        carry_at_seam=c
        c=0
        for x in pref[:-1]: c=(x+c)//10
        lo=(pref[-1]+c)%10
        target=rows[(ph+1)%12][1][-1]
        g=GAMMA[ph]
        if not g:
            req=[h for h in (0,1) if lo+((pref[-1]+h)%10)==target]
            assert len(req)==1
            infos.append((carry_at_seam,req[0],True,pref))
        else:
            h=int(pref[-1]>=10)
            fixed=(lo+((pref[-2]+h)%10)==target)
            assert fixed
            infos.append((carry_at_seam,h,fixed,pref))
    return infos

def seam_raw(j,u,unext,ph,infos):
    carry_at_seam,req,fixed,pref=infos[ph]
    g=GAMMA[ph]
    state_u=first_non9_state(u)
    state=state_u
    for x in reversed(j):
        if x!=9: state=int(x>=10)
    if not g:
        w_ok=(state==req)
    else:
        w_ok=fixed
    lo=[]; c=carry_at_seam
    for x in j:
        z=x+c;lo.append(z%10);c=z//10
    h=[0]*len(j);state=state_u
    for i in range(len(j)-1,-1,-1):
        if not g:
            h[i]=state
            if j[i]!=9: state=int(j[i]>=10)
        else:
            if j[i]!=9: state=int(j[i]>=10)
            h[i]=state
    jp=[]
    for i,x in enumerate(j):
        if not g: jp.append(lo[i]+((x+h[i])%10))
        else:
            prev=j[i-1] if i else pref[-1]
            jp.append(lo[i]+((prev+h[i])%10))
    c=carry_at_seam
    for x in j: c=(x+c)//10
    uout=[]
    for i,x in enumerate(u):
        z=x+c; low=z%10; c=z//10
        prev=j[-1] if i==0 else u[i-1]
        uout.append(low+(((prev if g else x)+high_u(u,i,g))%10))
    return jp,w_ok,(uout==unext),uout

def local_collar_step(h,u,ustart,g):
    n=len(h); low=[0]*n; high=[0]*n; out=[0]*n
    state=-1
    for j in range(3):
        x=u[(n+j-ustart)%3]
        if x!=9:
            state=int(x>=10); break
    assert state>=0
    c=0
    for i,x in enumerate(h):
        z=x+c;low[i]=z%10;c=z//10
    for i in range(n-1,-1,-1):
        if not g:
            high[i]=state
            if h[i]!=9:state=int(h[i]>=10)
        else:
            if h[i]!=9:state=int(h[i]>=10)
            high[i]=state
    for i in range(n):
        if not g:out[i]=low[i]+((h[i]+high[i])%10)
        elif i==0:out[i]=low[i]+1
        else:out[i]=low[i]+((h[i-1]+high[i])%10)
    return out

def main():
    rows=derive_rows()
    Us=u_words()
    rng=random.Random(19633)
    infos=phase_info(rows,14)
    for _ in range(10000):
        ph=rng.randrange(12);u=rng.choice(Us);m=rng.choice((3,4,5))
        j=[rng.randrange(19) for _ in range(m)]
        unext=bulk_step(u,GAMMA[ph])
        root=34+9*14;collar=170
        pref=rows[ph][0]+rows[ph][1]*14
        h=pref+j+[u[i%3] for i in range(collar)]
        out=local_collar_step(h,u,root+m,GAMMA[ph])
        jp,wok,uok,uout=seam_raw(j,u,unext,ph,infos)
        exp=rows[(ph+1)%12][0]+rows[(ph+1)%12][1]*14
        prefix_ok=(out[:root]==exp)
        assert prefix_ok==wok
        if prefix_ok: assert out[root:root+m]==jp
        assert (out[root+m:root+m+3]==unext)==uok
    controls=[
        ([8,3,15],[9,16,2],[10]),
        ([4,9,14],[6,9,12],[8,8]),
        ([0,9,4,14],[8,9,10],[12]),
        ([18,0,1,1],[9,14,4],[14,14]),
        ([1,2,3,4,5],[9,14,4],[12]),
        ([18,0,1,1,2],[8,9,10],[14,14]),
    ]
    count=0
    for q in (20,40,80,160):
        k=5*q; root=34+9*q; infos=phase_info(rows,q)
        for j,u,c in controls:
            ph0=9
            h=rows[ph0][0]+rows[ph0][1]*q+j+u*k
            p=h+c+h[::-1]
            n=value_from_digits(digits_from_pairword(p))
            assert pairword_of_int(n)==p
            p1,g1=pair_step(p)
            n1=n+reverse10(n)
            assert pairword_of_int(n1)==p1
            assert g1==GAMMA[ph0]
            unext=bulk_step(u,GAMMA[ph0])
            jp,wok,uok,uout=seam_raw(j,u,unext,ph0,infos)
            assert (p1[:root]==rows[(ph0+1)%12][0]+rows[(ph0+1)%12][1]*q)==wok
            assert p1[root:root+len(j)]==jp
            assert (p1[root+len(j):root+len(j)+3]==unext)==uok
            for t in range(121):
                pnow=pairword_of_int(n)
                ph=(ph0+t)%12
                assert pnow[:34]==rows[ph][0]
                assert pnow[34:43]==rows[ph][1]
                assert pnow[34:34+9*(q-3)]==rows[ph][1]*(q-3)
                if t<120:
                    n2=n+reverse10(n)
                    assert int(len(str(n2))>len(str(n)))==GAMMA[ph]
                    n=n2
            count+=1
    print(f"PASS: 10,000 random seam transitions; {count} genuine-bigint 120-step controls.")
    print("Widths q=20,40,80,160; k=5q; J lengths 3,4,5; both centre parities.")
    print("Every overflow bit, rooted B row, first W row, first q-3 W copies, seam output, and U port matched.")

if __name__=="__main__":
    main()
