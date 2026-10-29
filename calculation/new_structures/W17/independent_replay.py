#!/usr/bin/env python3
"""Independent native-bigint and LSD digit-array controls for W17's pairword cone."""
from itertools import product
import argparse, sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[8,9,10]
CENTRES=[[0,0],[18,18,18,18],[6,12,12,6,8,10,10,8,6,12,12,6]]
ODD_CENTRES=[[4,12,4],[6,12,8,12,6]]
JUNCTIONS=[[0,0,0,0],[12,14,9,16],[2,1,9,10],[9,9,9,9]]
WIDTHS=[(20,100),(40,200),(80,400),(160,800)]
def pairword(d): return [d[i]+d[-1-i] for i in range(len(d))]
def value_lsd(d):
    n=0
    for x in reversed(d): n=10*n+x
    return n
def digits_lsd(n): return [int(x) for x in str(n)[::-1]]
def realize(p):
    assert p==p[::-1] and all(0<=x<=18 for x in p)
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]); lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo; d[-1-i]=hi
    if len(p)%2:
        mid=p[len(p)//2]
        assert mid%2==0
        d[len(p)//2]=mid//2
    assert d[-1]>0
    return d
def step_pair(p):
    y=[];c=0
    for x in p:
        z=x+c;y.append(z%10);c=z//10
    if c:y.append(c)
    return [y[i]+y[-1-i] for i in range(len(y))]
def step_digits(d):
    y=[];c=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c;y.append(z%10);c=z//10
    if c:y.append(c)
    return y
def template(q,k,J,C):
    h=B+W*q+J+U*k
    p=h+C+h[::-1]
    assert p==p[::-1]
    return p
def run(q,k,J,C):
    p=template(q,k,J,C); d=realize(p); n=value_lsd(d)
    assert pairword(d)==p and n==int(''.join(map(str,d[::-1])))
    gam=[]
    for t in range(120):
        assert pairword(d)==p, (q,k,J,C,t,'source pairword')
        n2=n+int(str(n)[::-1])
        d2=step_digits(d)
        assert value_lsd(d2)==n2, (q,k,J,C,t,'bigint vs digit array')
        p2=step_pair(p)
        assert pairword(d2)==p2, (q,k,J,C,t,'pairword vs digit array')
        g=len(str(n2))-len(str(n)); gam.append(g)
        assert g in (0,1)
        assert g==(1 if t%4==0 else 0), (q,k,J,C,t,g)
        n,d,p=n2,d2,p2
    target=template(q,k+5,J,C)
    first=next((i for i,(x,y) in enumerate(zip(p,target)) if x!=y),None)
    if first is None and len(p)!=len(target): first=min(len(p),len(target))
    return first,sum(gam),len(str(n))
parser=argparse.ArgumentParser()
parser.add_argument("--reference", action="store_true", help="also check q=14,k=100 pumping reference")
parser.add_argument("--odd-centres", action="store_true", help="add odd palindromic-centre controls at q=14/20")
args=parser.parse_args()
widths=([(14,100)] if args.reference else [])+WIDTHS
count=0
for q,k in widths:
    for J,C in product(JUNCTIONS,CENTRES):
        first,gs,digits=run(q,k,J,C)
        count+=1
        print(f'PASS q={q} k={k} J={J} |C|={len(C)} first_target_mismatch={first} overflow_sum={gs} final_digits={digits}')
if args.odd_centres:
    odd_widths=[(14,100),(20,100)] if args.reference else [(20,100)]
    for q,k in odd_widths:
        for J,C in product(JUNCTIONS,ODD_CENTRES):
            first,gs,digits=run(q,k,J,C)
            count+=1
            print(f'PASS_ODD_C q={q} k={k} J={J} |C|={len(C)} first_target_mismatch={first} overflow_sum={gs} final_digits={digits}')
print(f'INDEPENDENT_BIGINT_DIGIT_ARRAY_PASS cases={count} each=120-steps even_widths={widths} even_centres=2/4/12 odd_centres={bool(args.odd_centres)}')
