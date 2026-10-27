#!/usr/bin/env python3
"""Independent integer-arithmetic controls for center trim-schedule transport.

Run from any working directory with ordinary (non-optimized) Python 3.  This
standard-library-only verifier imports neither the repository checker mirror
nor Agent 110's transformation implementation.  Normalization is independently
computed from positional integer values.  Existing Lean files supply only the
eight published positive certificates, parsed as literal data.

The finite-cap checks use both complementary balanced length profiles and keep
the stated maximum width unchanged.  They corroborate the accompanying paper
proof; no decimal nonexistence or Lean verification follows from these tests.
"""
import itertools
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def normalize(b, coeff, carry):
    value = sum(a * b ** i for i, a in enumerate(coeff)) + carry
    digits = []
    for _ in coeff:
        value, d = divmod(value, b)
        digits.append(d)
    return tuple(digits), value


def pairs(digits):
    return tuple(digits[i] + digits[-i-1] for i in range(len(digits)))


def raw_center(b, center, e, g):
    digits, out = normalize(b, center, e)
    assert out == 1-e
    return pairs(digits + ((b-1)*e,) if g else digits)


def pad(b, c, n):
    assert n >= 0
    h = (b-1,) * n
    return h + tuple(c) + h


def outgoing(b, B, C):
    db, e = normalize(b, B, 0)
    dc, f = normalize(b, C, e)
    if f != 1-e:
        return None
    dr, g = normalize(b, tuple(reversed(B)), f)
    assert g in (0,1)
    if g:
        left = db + ((b-1)*(1-e),)
        right = (1,) + tuple(reversed(dr))
    else:
        left, right = db, tuple(reversed(dr))
    return tuple(x+y for x,y in zip(left,right)), raw_center(b,C,e,g), e, g


def cert_ok(b, es):
    assert es, 'a certificate must contain at least one edge'
    total_g = total_gain = 0
    for i, (B,C,B2,C2,u,v) in enumerate(es):
        assert u>=0 and v>=0
        assert b >= 2 and all(0<=a<=2*b-2 for a in B+C)
        assert not B or B[0] != 0
        assert (B2,C2) == es[(i+1)%len(es)][:2]
        z = outgoing(b,B,C)
        assert z is not None
        rB,rC,e,g = z
        assert rB == B2 + (b-1,)*u
        assert rC == pad(b,C2,v)
        total_g += g
        total_gain += u+v
    assert total_g <= total_gain
    return total_g


def read_known_data():
    rows = []
    src = (ROOT/'lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean').read_text()
    nums = lambda s: tuple(map(int,s.split(','))) if s.strip() else ()
    for m in re.finditer(r'def cert(\d+) : List Edge :=\s*(\[.*?\])\n\n',src,re.S):
        es = []
        for z in re.finditer(r'⟨\[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], (\d+), (\d+)⟩',m[2]):
            es.append(tuple(nums(z[i]) for i in range(1,5))+(int(z[5]),int(z[6])))
        rows.append((int(m[1]),es))
    src=(ROOT/'lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean').read_text()
    defs={z[1]:nums(z[2]) for z in re.finditer(r'def (\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]',src)}
    for m in re.finditer(r'def cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\n\n',src,re.S):
        es=[]
        for z in re.finditer(r'⟨(\w+), (\w+), (\w+), (\w+), (\d+), (\d+)⟩',m[2]):
            es.append(tuple(defs[z[i]] for i in range(1,5))+(int(z[5]),int(z[6])))
        rows.append((int(m[1]),es))
    assert len(rows)==8
    return rows


def transfer(b,es,w):
    v=[z[5] for z in es]
    assert len(v)==len(w) and sum(v)==sum(w)
    rel=[0]
    for x,y in zip(v,w): rel.append(rel[-1]+x-y)
    assert rel[-1]==0
    offset=-min(rel)
    a=[x+offset for x in rel]
    ns=[]
    for i,(B,C,B2,C2,u,_) in enumerate(es):
        ns.append((B,pad(b,C,a[i]),B2,pad(b,C2,a[i+1]),u,w[i]))
    assert cert_ok(b,ns)==cert_ok(b,es)
    return ns,a


def compositions(n,total):
    for chosen in itertools.combinations_with_replacement(range(n),total):
        v=[0]*n
        for j in chosen: v[j]+=1
        yield v


def balanced(b,es):
    s=0; w=[]; residues=[]
    for z in es:
        residues.append(s%2)
        g=outgoing(b,z[0],z[1])[3]
        w.append((s+g)//2-s//2); s+=g
    assert s%2==0
    ns,a=transfer(b,es,w)
    M=max(len(z[1])-r for z,r in zip(es,residues))
    assert len(ns[0][1])==M
    assert all(len(z[1])==M+r for z,r in zip(ns,residues))
    assert M%2==len(es[0][1])%2
    assert max(len(z[1]) for z in ns)<=max(len(z[1]) for z in es)+1
    return ns,M


def finite_bound_audit(b,es):
    ns,M=balanced(b,es)
    oldmax=max(len(z[1]) for z in es)
    for W in (oldmax,oldmax+1,oldmax+5):
        endpoint=W-((W-M)%2)
        assert endpoint in (W-1,W) and endpoint>=M
        extra=(endpoint-M)//2
        raised=[(B,pad(b,C,extra),B2,pad(b,C2,extra),u,v)
                for B,C,B2,C2,u,v in ns]
        assert len(raised[0][1])==endpoint
        assert max(len(z[1]) for z in raised)<=W+1
        cert_ok(b,raised)
        # Stronger exact-W reduction: select one of two complementary profiles.
        assert W>=2
        s=0; ws=[]; residues=[]
        opposite=(len(es[0][1])-W)%2==0
        for z in es:
            residues.append(s%2)
            g=outgoing(b,z[0],z[1])[3]
            if opposite:
                ws.append((s+g+1)//2-(s+1)//2)
            else:
                ws.append((s+g)//2-s//2)
            s+=g
        L=[W-r if opposite else W-1+r for r in residues]
        aa=[]
        for m,z in zip(L,es):
            delta=m-len(z[1])
            assert delta>=0 and delta%2==0
            aa.append(delta//2)
        exact=[]
        for i,(B,C,B2,C2,u,v) in enumerate(es):
            j=(i+1)%len(es)
            assert aa[j]==aa[i]+v-ws[i]
            exact.append((B,pad(b,C,aa[i]),B2,pad(b,C2,aa[j]),u,ws[i]))
        cert_ok(b,exact)
        assert [len(z[1]) for z in exact]==L
        assert max(L)<=W and min(L)>=1
    return len(es[0][1])%2


def main():
    identity_checks=0
    eligible_words=0
    degenerate_rejections=0
    for b in (2,3,4,5,10):
        for m in range(5):
            for C in itertools.product(range(2*b-1),repeat=m):
                for e in (0,1):
                    _,out=normalize(b,C,e)
                    if not C or all(x==b-1 for x in C):
                        assert out==e
                        degenerate_rejections+=1
                    if out!=1-e: continue
                    eligible_words+=1
                    for g in (0,1):
                        raw=raw_center(b,C,e,g)
                        for a in (0,1,3):
                            Cp=pad(b,C,a)
                            assert normalize(b,Cp,e)[1]==1-e
                            assert raw_center(b,Cp,e,g)==pad(b,raw,a)
                            identity_checks+=1
    print('padding_identity_checks',identity_checks,'eligible_C_e_pairs',eligible_words,'degenerate_rejections',degenerate_rejections)
    certs=read_known_data()
    transformed=0; nonbinary=0; checked_edges=0; bound_checks=0; parity_counts=[0,0]
    for b,base in certs:
        for rep in (1,2):
            es=base*rep
            G=cert_ok(b,es)
            for w in compositions(len(es),G//2):
                ns,a=transfer(b,es,w)
                transformed+=1
                nonbinary+=max(w)>1
                checked_edges+=len(ns)
                parity_counts[finite_bound_audit(b,ns)]+=1
                bound_checks+=3
            w=[]; s=0
            for z in es:
                g=outgoing(b,z[0],z[1])[3]
                w.append((s+g)//2-s//2);s+=g
            ns,a=transfer(b,es,w)
            widths=[len(z[1]) for z in ns]
            prefix=0
            for i,z in enumerate(es):
                assert widths[i]==widths[0]+prefix%2
                prefix+=outgoing(b,z[0],z[1])[3]
            assert max(widths)-min(widths)<=1
            print('balanced',b,'repeat',rep,'period',len(es),'w',''.join(map(str,w)),'widths',min(widths),max(widths),'max_padding',max(a))
        for shift in range(len(base)):
            rotated=base[shift:]+base[:shift]
            parity_counts[finite_bound_audit(b,rotated)]+=1
            bound_checks+=3
    print('known_certificates',len(certs),'schedule_transforms',transformed,'nonbinary_targets',nonbinary,'verified_edges',checked_edges)
    print('finite_bound_endpoint_checks',bound_checks,'initial_parity_even_odd',parity_counts)
    stream_checks=0
    for p in range(1,13):
        for g in itertools.product((0,1),repeat=p):
            if sum(g)%2: continue
            s=0; w=[]; d=0
            for gg in g:
                ww=(s+gg)//2-s//2
                assert ww in (0,1) and (not ww or gg==1)
                w.append(ww); d+=gg-2*ww; s+=gg
                assert d==s%2
            assert sum(w)==sum(g)//2 and d==0
            stream_checks+=1
    print('balanced_binary_streams',stream_checks,'ALL_CHECKS_PASSED')


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Do not disable assertions: run without Python -O.')
    main()
