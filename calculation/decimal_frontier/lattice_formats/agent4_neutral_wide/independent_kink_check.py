#!/usr/bin/env python3
"""Independent direct-digit exhaustive checker for kinkdfs_mask.cpp.
Uses scalar carries and explicit digit lists, NOT bitset/domain propagation.
Run: python3 independent_kink_check.py ./kinkdfs_mask ./data
"""
import itertools, re, subprocess, sys, random
from pathlib import Path

def read_lattice(path):
    vals = list(map(int, Path(path).read_text().split()))
    p,nb,m,b = vals[:4]; pos=4
    gam=vals[pos:pos+p];pos+=p
    W=[vals[pos+t*m:pos+(t+1)*m] for t in range(p)];pos+=p*m
    cup=[vals[pos+t*m:pos+(t+1)*m] for t in range(p)]
    assert len(vals)>=pos+p*m
    return p,nb,m,b,gam,W,cup

def direct_survives(lat,w,H,offset,digits):
    p,nb,m,b,gam,W,cup=lat
    K=w+10
    n=2*m*((max(400,2*nb+2*K)+2*m-1)//(2*m))+offset
    h=(n+1)//2
    def lattice(t,x):return W[t%p][(x-nb)%m]
    P=[lattice(0,h-K+i) for i in range(K-w)]+list(digits)
    if n%2 and P[-1]%2:return False
    for t in range(H):
        carry=cup[t%p][(h-K-nb)%m]
        up=[]
        for z in P:
            v=z+carry
            up.append(v%b)
            carry=v//b
        dn=[0]*K
        dc=[0]*K
        if n%2:
            dn[-1]=up[-1]
            dc[-2]=carry
            top=K-2
        else:
            dc[-1]=carry
            top=K-1
        for i in range(top,-1,-1):
            dn[i]=(P[i]+dc[i])%b
            if i>0:dc[i-1]=(P[i]+dc[i])//b
        g=gam[t%p];nn=n+g;h2=(nn+1)//2;dh=h2-h
        nxt=[]
        for j in range(K):
            if j<2:
                nxt.append(lattice(t+1,h2-K+j))
                continue
            i=j+dh
            a=up[i] if i<K else dn[-1]
            z=(up[i] if (g==0 and n%2 and i==K-1) else
               dn[i] if g==0 else dn[i-1])
            vv=a+z
            if j<K-w and vv!=lattice(t+1,h2-K+j):return False
            nxt.append(vv)
        if nn%2 and nxt[-1]%2:return False
        P=nxt;n=nn;h=h2
    return True

def cpp_count(binfile,path,w,H,o,prefix=None):
    args=[str(binfile),str(path),str(w),str(H),str(o),str(o+1)]
    if prefix is not None:args.append(','.join(map(str,prefix)))
    s=subprocess.check_output(args,text=True)
    m=re.search(r'survivors=(\d+)',s)
    assert m,s
    return int(m[1])

def test_solver(binfile,path,w,H,o):
    lat=read_lattice(path);b=lat[3]
    expected=sum(direct_survives(lat,w,H,o,digits) for digits in
                 itertools.product(range(2*b-1),repeat=w))
    observed=cpp_count(binfile,path,w,H,o)
    assert observed==expected,(path,w,H,o,expected,observed)
    return expected

def main():
    exe=Path(sys.argv[1]).absolute();folder=Path(sys.argv[2]).absolute()
    cases=0
    for name in ['neutral_p11','neutral_p12','neutral_b26_control']:
        path=folder/(name+'.txt')
        for w in (1,2,3):
            for H in (2,6):
                for o in (0,1):
                    test_solver(exe,path,w,H,o)
                    cases+=1
    print('Direct independent checks:',cases,'PASS',flush=True)
    base=folder/'neutral_b26_control.txt'
    ctrl=(cpp_count(exe,base,3,30,0),cpp_count(exe,base,3,30,1))
    assert ctrl==(4,2),ctrl
    print('Base-26 known-centre positive control:',ctrl,'PASS',flush=True)
    reference=read_lattice(base)
    independent=tuple(sum(direct_survives(reference,3,30,o,digits) for digits in
                          itertools.product(range(51),repeat=3)) for o in (0,1))
    assert independent==ctrl==(4,2)
    print('Base-26 independent integer-carry check:',independent,'PASS',flush=True)
    rng=random.Random(4744)
    for name in ['neutral_p11','neutral_p12','neutral_b26_control']:
        path=folder/(name+'.txt');b=read_lattice(path)[3]
        for _ in range(2):
            w=2;H=rng.randint(1,6);o=rng.randrange(2)
            all_count=cpp_count(exe,path,w,H,o)
            split=sum(cpp_count(exe,path,w,H,o,[d]) for d in range(2*b-1))
            assert all_count==split,(name,w,H,o,all_count,split)
    print('6 independent first-digit partitions PASS',flush=True)

if __name__=='__main__':main()
