#!/usr/bin/env python3
"""Q03: exact first-contact classification with ordinary integer checks.
Run: python3 calculation/new_structures/Q03/verify_interface.py
"""
from itertools import product
import sys
sys.set_int_max_str_digits(1000000)

AL='0123456789ABCDEFGHI'
Bs=('H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D',
'8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB',
'H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4',
'8E8438GGCD99B9BC949B5397A498C98G8E7339A',
'H8H86HDE680040459A92B6IF09IH49ICI8F6791',
'8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA',
'HDEEAA6049H08899A1149HBBE0IF69I56GA68E1',
'8C9A62764E788GI90225E7A4759FCG8EBD87ED6')
Ws=('H31DHBE3I12073ECF97D','CB45CA78CA327A8895HB',
'639B51FH5174F0HGIBF4','A9D1767ED68BA68FGB8A',
'2073ECF97DH31DHBE3I1','327A8895HBCB45CA78CA',
'74F0HGIBF4639B51FH51','8BA68FGB8AA9D1767ED6')
B=[[AL.index(ch) for ch in row] for row in Bs]
W=[[AL.index(ch) for ch in row] for row in Ws]
G=[1,0,1,0,1,0,1,0]
assert all(len(a)==39 for a in B) and all(len(a)==20 for a in W)

# Independent canonical integer representation: no pair-normalizer is used
# to obtain the integer or its successor.
def integer_from_pairs(p):
    assert p==p[::-1] and p[0]>0
    n=len(p); d=[0]*n
    for i in range(n//2):
        d[i]=max(0,p[i]-9)
        d[n-1-i]=min(9,p[i])
    if n%2:
        assert p[n//2]%2==0
        d[n//2]=p[n//2]//2
    assert d[-1]!=0
    x=0
    for a in reversed(d):x=10*x+a
    return x

def actual_successor_pairs(p):
    n=integer_from_pairs(p)
    out=str(n+int(str(n)[::-1]))
    v=[int(a) for a in reversed(out)]
    return [v[i]+v[-1-i] for i in range(len(v))],len(v)

def incoming_carries(p):
    c=[0]
    for a in p:c.append((a+c[-1])//10)
    return c

G0={(4,1,0):9,(9,1,0):4,(9,0,1):14,(14,0,1):9}

def permitted(t,r,p,c,j):
    q=p[j]; cl=c[j]; high=len(p)-1-j; cu=c[high]
    if G[t]==0:
        return G0.get((q,cl,cu))
    # Overflow gate +/-9: lower carry must flip; boundary
    # q=0 and q=9/18 have further high-port guards.
    if p[j-1]==9:return None
    if q<=9:
        r2=q+9
        if (r2+cl)//10-(q+cl)//10==1 and (q!=9 or cu==0):
            return r2
    if q>=9:
        r2=q-9
        if (r2+cl)//10-(q+cl)//10==-1 and (q!=9 or cu==1):
            return r2
    return None

# Complete two-ended arithmetic enumeration for delta, low carry,
# old/new upper incoming carries; plus physical upper-outgoing reset.
def universal_table():
    lines=[]
    for gamma in (0,1):
        for q in range(19):
            for r in range(19):
                if q==r:continue
                opts=[]
                for cl,cu,du in product((0,1),repeat=3):
                    lo=(r+cl)//10-(q+cl)//10
                    up=(r+du)//10-(q+cu)//10
                    if gamma==0:
                        ok=2*(r-q)-10*lo==0 and du==cu and up==0
                    else:
                        ok=(r-q)-10*lo+up==0 and up!=0
                    if ok:opts.append((cl,cu,du))
                if opts:lines.append((gamma,q,r,tuple(opts)))
    assert len([v for v in lines if v[0]==0])==4
    assert len([v for v in lines if v[0]==1])==20
    assert all(abs(v[2]-v[1])==(5 if v[0]==0 else 9) for v in lines)
    return lines

def check_universal_witnesses(lines):
    """One changed mirrored source pair, full real decimal addition.
    Gamma=0: preserve through first contact, not necessarily farther.
    Gamma=1: complete successor pairword merges for the witnesses.
    """
    num=0
    for gam,q,r,ports in lines:
        found=None
        for before,after in product((2,8,10,14),repeat=2):
            h=[17 if gam else 8,5,3,before,q,after,4,6,2,7]
            p=h+[18]+h[::-1]
            z=p.copy();z[4]=z[-5]=r
            a,la=actual_successor_pairs(p)
            b,lb=actual_successor_pairs(z)
            if la==lb==len(p)+gam and a[:5]==b[:5]:
                found=(before,after,a==b)
                break
        assert found is not None,(gam,q,r)
        if gam:assert found[2],(gam,q,r,found)
        num+=1
        print('PHYSICAL',gam,q,r,'neighbor coefficients',found[:2],
              'whole successor identical',found[2])
    assert num==24
    print('24/24 arithmetic gate types have physical integer witnesses')

def check_root():
    expected={0:[0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,19],
              1:[2],
              2:[0,1,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19],
              3:[7],
              4:[0,2,3,4,5,6,9,10,11,12,13,14,15,16,17,18,19],
              5:[12],
              6:[0,1,2,3,4,5,7,8,9,10,11,14,15,16,17,18,19],
              7:[17]}
    total=0; full_erased={}
    for t,m in product(range(8),(4,5,6,7,20,40,80,160)):
        h=B[t]+W[t]*m
        p=h+[18]+h[::-1]
        orig,n=actual_successor_pairs(p)
        assert n==len(p)+G[t]
        c=incoming_carries(p)
        jblock=m//2
        hits=[]; full=[]
        for r in range(20):
            j=39+20*jblock+r
            new=permitted(t,r,p,c,j)
            if new is not None:hits.append(r)
            delta=5 if G[t]==0 else 9
            for v in (p[j]-delta,p[j]+delta):
                if not 0<=v<=18:continue
                alt=p.copy();alt[j]=alt[-1-j]=v
                actual,n2=actual_successor_pairs(alt)
                assert n2==n,(t,m,r,v)
                head=(orig[:j+1]==actual[:j+1])
                assert head==(v==new),(t,m,r,v,head,new)
                if head and orig==actual:full.append((r,v))
                total+=1
        assert hits==expected[t],(t,m,hits,expected[t])
        full_erased.setdefault(t,[]).append(len(full))
        if G[t]:assert len(full)==16,(t,m,full)
        else:assert not full,(t,m,full)
    print('ROOTED_FIRST_CONTACT:',expected)
    print('independent full decimal successor trials:',total)
    print('whole successor pairword same count per width:',full_erased)
    return expected

if __name__=='__main__':
    lines=universal_table()
    print('universal directed interface types:',len(lines), '(gamma0=4, gamma1=20)')
    for gm,q,r,opts in lines:
        print('TYPE',gm,q,r,'CL/CU/DU:',opts)
    check_universal_witnesses(lines)
    check_root()
    print('PASS Q03 actual-integer first-contact interface controls')
