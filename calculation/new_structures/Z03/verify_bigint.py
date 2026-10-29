#!/usr/bin/env python3
from pathlib import Path
import argparse, sys
sys.set_int_max_str_digits(0)
parser=argparse.ArgumentParser()
parser.add_argument('--lattice',default='calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
args=parser.parse_args()
lines=Path(args.lattice).read_text().splitlines()
p,nb,m,base=map(int,lines[0].split()); gamma=list(map(int,lines[1].split()))
W=[tuple(map(int,lines[2+i].split())) for i in range(12)]
B=[tuple(map(int,lines[26+i].split())) for i in range(12)]
assert (p,nb,m,base)==(12,34,9,10)
Uset=set()
for a in range(0,19,2):
    b=(9,a,18-a)
    for r in range(3): Uset.add(b[r:]+b[:r])
Us=sorted(Uset)
assert len(Us)==30
NJ=19**5

def bulk_step(w,g):
    a=None;b=None
    for s in (0,1):
        x=s; aa=[]
        for d in w: aa.append(x); x=(d+x)//10
        if x==s: a=aa; break
    for s in (0,1):
        x=s; bb=[0]*len(w)
        for i in range(len(w)-1,-1,-1): bb[i]=(w[i]+x)//10; x=bb[i]
        if x==s: b=bb; break
    assert a is not None and b is not None
    z=[]
    for i in range(len(w)):
        lo=(w[i]+a[i])%10
        hi=((w[(i-1)%len(w)]+b[i])%10) if g else ((w[i]+b[(i+1)%len(w)])%10)
        z.append(lo+hi)
    return tuple(z)
def local_step(H,g,lowin,prev,seed):
    lo=[];c=lowin
    for x in H: lo.append((x+c)%10);c=(x+c)//10
    hi=[0]*len(H);state=seed
    for i in range(len(H)-1,-1,-1):
        if not g:
            hi[i]=(H[i]+state)%10;state=(H[i]+state)//10
        else:
            state=(H[i]+state)//10
            hi[i]=((H[i-1] if i else prev)+state)%10
    return [a+b for a,b in zip(lo,hi)]
def digits_lsd(n): return [ord(ch)-48 for ch in str(n)[::-1]]
def lower_pairword(n):
    """Return the LSD half of the exact symmetric pairword, including its midpoint if odd."""
    d=digits_lsd(n)
    return [d[i]+d[-1-i] for i in range(len(d)//2)] + ([2*d[len(d)//2]] if len(d)%2 else [])
def realize(P):
    d=[0]*len(P)
    for i in range(len(P)//2):
        hi=min(9,P[i]);lo=P[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]!=0
    return int(''.join(map(str,d[::-1])))
def dec_j(idx):
    j=[]
    for _ in range(5):j.append(idx%19);idx//=19
    return j
# Check the rooted W9 clock and all 30 U3 bulk returns, and derive exact local cone bounds.
for ph in range(12):
    assert bulk_step(W[ph],gamma[ph])==W[(ph+1)%12],('W row transition',ph)
    assert gamma[ph]==int(B[ph][0]>=10),('root overflow gate',ph)
for U in Us:
    for phase in range(12):
        row=U
        for t in range(120): row=bulk_step(row,gamma[(phase+t)%12])
        assert row==U,('U3 120-return',U,phase)
def cone_losses(U,phase=0):
    rows=[U]
    for t in range(120): rows.append(bulk_step(rows[-1],gamma[(phase+t)%12]))
    left=right=0
    for t in range(120):
        row=rows[t]
        left += 1 + int(row[left%3]==9)
        right += 1 + int(row[(-right-1)%3]==9) - gamma[(phase+t)%12]
    return left,right
assert {U:cone_losses(U,0) for U in (Us[2],Us[14],Us[26])}=={Us[2]:(150,120),Us[14]:(152,121),Us[26]:(151,122)}
# Exact W-side cone loss at q=14 is 91, leaving 17 protected cells before the window start at 52.
m=34+9*14
for t in range(120):
    row=W[t%12];r=0
    while row[(m-35-r)%9]==9:r+=1
    m-=1+r-gamma[t%12]
assert (34+9*14)-m==91,('W cone loss',(34+9*14)-m)
print('PASS: all 12 rooted W transitions, all 30 U3 120-returns at all 12 phases, and phase-0 cone bounds W=91; U=(2,9,16):(150,120), (9,8,10):(152,121), (16,2,9):(151,122).')

# low carry entering the last 12 W copies; W's carry map is constant after one copy.
lowin=[];prev=[]
for ph in range(12):
    c=0
    for x in B[ph]:c=(x+c)//10
    for i in range(18):c=(W[ph][i%9]+c)//10
    lowin.append(c);prev.append(W[ph][8])

def test_one(ui, jid, q, k, C=(10,)):
    U=Us[ui];J=dec_j(jid);H0=list(B[0])+list(W[0])*q+J+list(U)*k
    P=H0+list(C)+H0[::-1]
    n=realize(P)
    cut=34+9*q;start=cut-108;local=list(W[0])*12+J+list(U)*60
    Urow=U
    for t in range(121):
        got=lower_pairword(n)
        assert got[start:start+len(local)]==local,(ui+1,jid,q,k,t,'local-window mismatch',got[start:start+len(local)][:20],local[:20])
        if t==120: break
        nn=n+int(str(n)[::-1])
        g=len(str(nn))-len(str(n))
        assert g==gamma[t%12],(ui+1,jid,q,k,t,'clock',g,gamma[t%12])
        seed=next((int(x>=10) for x in Urow if x!=9),None)
        assert seed is not None
        local=local_step(local,g,lowin[t%12],prev[t%12],seed)
        Urow=bulk_step(Urow,gamma[t%12])
        n=nn
    return {'u_rank':ui+1,'j_id':jid,'J':J,'q':q,'k':k,'mismatch':next((i for i,(a,b) in enumerate(zip(local[:108],W[0]*12)) if a!=b),None)}

# q/k=14/100 validates the precise census reference. Larger widths use q=20,40,80,160 and k=5q.
ids=[0,19,361,123456,NJ-1]
for ui in (2,14,26):
    for jid in ids:
        print('REF',test_one(ui,jid,14,100),flush=True)
for q in (20,40,80,160):
    k=5*q
    for ui in (2,14,26):
        for jid in (0,123456,NJ-1):
            print('BIGINT',test_one(ui,jid,q,k),flush=True)
print('PASS: local 293-coefficient bit-independent recurrence matches genuine arbitrary-precision decimal reverse-add at all 120 phases for 5 reference J values × 3 U rows and 3 J values × 3 U rows × four scaled widths; exact gamma verified each step.')
