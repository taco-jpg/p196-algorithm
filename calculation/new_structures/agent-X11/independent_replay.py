#!/usr/bin/env python3
"""Independent bigint + fresh-buffer digit-vector replay for the X11 phase-0 cell."""
import json, sys
if hasattr(sys,'set_int_max_str_digits'): sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[9,10,8]
WIDTHS=[(20,80),(40,160),(80,320),(160,640)]
JUNCTIONS=[[0,0,0],[18,18,18],[0,0,0,0],[18,18,18,18]]
CENTRE_LENGTHS=[14,16,18,20,22,24]
def rev(a): return list(reversed(a))
def template(q,k,J,C):
    h=B+W*q+J+U*k
    return h+C+rev(h)
def realize(p):
    assert p==rev(p);d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return d
def val(d): return int(''.join(map(str,rev(d)))) if d else 0
def pairword(d): return [d[i]+d[-1-i] for i in range(len(d))]
def digit_step(d):
    out=[];c=0
    for i in range(len(d)):
        z=d[i]+d[len(d)-1-i]+c
        out.append(z%10);c=z//10
    if c:out.append(c)
    return out,len(out)-len(d)
def pair_step(p):
    d=[];c=0
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return [d[i]+d[len(d)-1-i] for i in range(len(d))],c
def first_mismatch(a,b):
    for i,(x,y) in enumerate(zip(a,b)):
        if x!=y:return i
    return None if len(a)==len(b) else min(len(a),len(b))
def run(q,k,J,clen):
    C=[0]*clen;p=template(q,k,J,C);d=realize(p);n=val(d)
    assert pairword(d)==p and n>0
    target=template(q,k+5,J,C);gam=[];firstpal=None
    for t in range(121):
        nstr=str(n);dstr=''.join(map(str,rev(d)))
        assert nstr==dstr,(q,k,J,clen,t,'integer/vector mismatch')
        assert pairword(d)==p,(q,k,J,clen,t,'pairword mismatch')
        if d==rev(d) and firstpal is None:firstpal=t
        if t==120:break
        p2,g=pair_step(p);d2,gd=digit_step(d);n2=n+int(nstr[::-1])
        assert str(n2)==''.join(map(str,rev(d2))),(q,k,J,clen,t,'bigint/vector successor mismatch')
        assert p2==pairword(d2),(q,k,J,clen,t,'pairword/vector successor mismatch')
        assert g==gd,(q,k,J,clen,t,'overflow mismatch')
        assert g==int(t%4==0),(q,k,J,clen,t,'wrong rooted clock')
        gam.append(g);p,d,n=p2,d2,n2
    first=first_mismatch(p,target)
    assert first is not None and first<len(B)+len(W)*q,(q,k,J,clen,first,'target mismatch outside rooted prefix')
    assert firstpal is None,(q,k,J,clen,firstpal,'palindrome found')
    return {'q':q,'k':k,'J':J,'centre_length':clen,'steps':120,'first_mismatch':first,
            'gamma':''.join(map(str,gam)),'sum_gamma':sum(gam),'first_palindrome':firstpal,
            'source_digits':len(realize(template(q,k,J,C))),'final_digits':len(d)}
def all_cases():
    for q,k in WIDTHS:
        for J in JUNCTIONS:
            for clen in CENTRE_LENGTHS:
                yield run(q,k,J,clen)
def main():
    results=list(all_cases())
    hist={str(m):sum(x['first_mismatch']==m for x in results) for m in sorted({x['first_mismatch'] for x in results})}
    print(json.dumps({'status':'PASS','engine':'Python arbitrary-precision n+reverse + fresh-buffer decimal digit vector + folded pairword recurrence',
      'cases':len(results),'widths':WIDTHS,'junctions':JUNCTIONS,'centre_lengths':CENTRE_LENGTHS,
      'all_clocks_exact':all(x['gamma']=='1000'*30 and x['sum_gamma']==30 for x in results),
      'all_nonpalindromic':all(x['first_palindrome'] is None for x in results),
      'all_fail_rooted_prefix':all(x['first_mismatch'] is not None for x in results),
      'first_mismatch_range':[min(x['first_mismatch'] for x in results),max(x['first_mismatch'] for x in results)],
      'mismatch_histogram':hist,'details':results},separators=(',',':'))
if __name__=='__main__':main()