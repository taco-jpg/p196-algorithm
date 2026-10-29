#!/usr/bin/env python3
"""Decimal p12 moving-defect packet: exact local carries vs ordinary integers.
Run: python3 calculation/new_structures/agent-N05/phase_packet.py --steps 1000 --band 3000 --x 1008 --phase 2 --patch 8,8,4,16
"""
import argparse, json, sys
sys.set_int_max_str_digits(0)
G=[1,0,0,0,1,0,0,0,1,0,0,0]
W=[
[5,18,4,8,1,15,4,0,5],[10,14,13,12,9,7,10,4,5],
[1,10,8,5,9,16,0,9,11],[4,0,17,11,9,12,2,9,2],
[8,1,15,4,0,5,5,18,4],[12,9,7,10,4,5,10,14,13],
[5,9,16,0,9,11,1,10,8],[11,9,12,2,9,2,4,0,17],
[4,0,5,5,18,4,8,1,15],[10,4,5,10,14,13,12,9,7],
[0,9,11,1,10,8,5,9,16],[2,9,2,4,0,17,11,9,12]]
C=[
[0,0,1,0,0,0,1,0,0],[0,1,1,1,1,1,0,1,0],
[1,0,1,0,0,0,1,0,0],[0,0,0,1,1,1,1,0,0],
[0,0,0,1,0,0,0,0,1],[1,1,1,0,1,0,0,1,1],
[0,0,0,1,0,0,1,0,1],[1,1,1,1,0,0,0,0,0],
[1,0,0,0,0,1,0,0,0],[0,1,0,0,1,1,1,1,1],
[1,0,0,1,0,1,0,0,0],[1,0,0,0,0,0,1,1,1]]
B0=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]

def bulk(t,x): return W[t%12][(x-34)%9]
def incarry(t,x): return C[t%12][(x-34)%9]

def local_step(t,patch):
    """Normalize both reflected halves using independently fixed bulk carries."""
    if not patch:return {}
    lo=min(patch)-18;hi=max(patch)+18
    vals={x:patch.get(x,bulk(t,x)) for x in range(lo-1,hi+2)}
    lower={};c=incarry(t,lo-1)
    for x in range(lo-1,hi+2):
        s=vals[x]+c;lower[x]=s%10;c=s//10
    upper={};c=0
    for x in range(hi+30,lo-3,-1):
        s=vals.get(x,bulk(t,x))+c;upper[x]=s%10;c=s//10
    out={}
    for x in range(lo+1,hi):
        p=lower[x]+upper[x-G[t%12]]
        if p!=bulk(t+1,x):out[x]=p
    return out

def digs(n): return [int(c) for c in str(n)[::-1]]
def num(ds): return int(''.join(map(str,reversed(ds))))
def pair(n):
    d=digs(n);return [a+b for a,b in zip(d,reversed(d))]
def revadd(n):
    d=digs(n);return n+num(d[::-1])
def realize(P):
    assert P and P[0]>0 and P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        hi=min(9,P[i]);d[i]=P[i]-hi;d[-1-i]=hi
        assert 0<=d[i]<=9
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0
    return num(d)

def test(steps,band,x,phase,patch):
    assert band%2==0 and band>2*steps and x>steps//4+100 and x+steps+80<band
    assert (x-207)%9==0 and phase in range(12)
    for t in range(12):
        for j in range(9):
            k=207+j
            assert local_step(t,{k:bulk(t,k)})=={},('bulk control',t,j)
    left=B0+[bulk(0,34+j) for j in range(band)]
    P0=left+[0,0]+left[::-1]
    n=realize(P0)
    for _ in range(phase):n=revadd(n)
    P=pair(n);assert P==P[::-1]
    changes={}
    for i,v in enumerate(patch):
        assert 0<=v<=18 and P[x+i]==bulk(phase,x+i)
        P[x+i]=P[-1-x-i]=v
        if v!=bulk(phase,x+i):changes[x+i]=v
    assert changes
    n=realize(P)
    points=[];overflow=0
    for k in range(steps):
        t=phase+k;actual=pair(n)
        assert all(actual[j]==changes.get(j,bulk(t,j))
                   for j in range(max(100,x-40-k),min(len(actual)//2-20,x+42+k))),('mismatch',k)
        assert digs(n)!=digs(n)[::-1],('palindrome',k)
        coords=sorted(changes)
        if k<20 or k%24==0 or k==steps-1:
            points.append({'step':k,'size':len(coords),'left':coords[0]-x if coords else None,
                           'right':coords[-1]-x if coords else None,
                           'coeff':[[j-x,changes[j]] for j in coords] if k<20 else None})
        n2=revadd(n)
        gam=len(digs(n2))-len(digs(n))
        assert gam==G[t%12],('overflow',k,gam)
        overflow+=gam
        changes=local_step(t,changes);n=n2
    return {'label':'COMPUTED','phase':phase,'seed_length':len(P),'band_half_length':band,
      'x':x,'patch':patch,'checked_steps':steps,'overflow_sum':overflow,
      'independent_integer_replay':True,'palindrome_hits':0,'first_local_mismatch':None,
      'samples':points}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--steps',type=int,default=1000)
    ap.add_argument('--band',type=int,default=3000)
    ap.add_argument('--x',type=int,default=1008)
    ap.add_argument('--phase',type=int,default=2)
    ap.add_argument('--patch',default='8,8,4,16')
    args=ap.parse_args()
    print(json.dumps(test(args.steps,args.band,args.x,args.phase,
                          [int(v) for v in args.patch.split(',')]),indent=2))
