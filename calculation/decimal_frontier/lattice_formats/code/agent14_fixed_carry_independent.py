#!/usr/bin/env python3
"""Independent integer-certificate checker and base-9/base-13 positive controls.
Run from repository root:
    python3 calculation/decimal_frontier/lattice_formats/code/agent14_fixed_carry_independent.py
Uses Python standard library; does not import primary slope solver.
"""
import argparse, json, math, re
from pathlib import Path
G=(1,0,1,0,1,0,1,0)

def check_cycle(name, W, cert):
    m=len(W[0]);L=cert['denominator'];u=cert['slope_numerators'];assert len(u)==m
    assert L>8 and math.gcd(L,*u)==1
    carr=[]
    for t in range(8):
        row=W[t]
        a=[];d=[]
        for b0 in (0,1):
            aa=[b0]
            for j in range(m):aa.append((row[j]+aa[-1])//10)
            if aa[-1]==b0:a.append(aa[:-1])
            dd=[0]*(m+1);dd[m-1]=b0
            for j in range(m-2,-1,-1):dd[j]=(row[j+1]+dd[j+1])//10
            if (row[0]+dd[0])//10==b0:d.append(dd[:-1])
        assert len(a)==len(d)==1
        carr.append((a[0],d[0]))
    tight=None
    for t in range(8):
        a,d=carr[t];row=W[t];h=G[t]
        nxt=[];unxt=[]
        for j in range(m):
            r=(j-h)%m
            predicted=(row[j]+a[j])%10+(row[r]+d[r])%10
            assert predicted==W[(t+1)%8][j]
            nxt.append(row[j]+row[r]+a[j]+d[r]-10*(a[(j+1)%m]+d[(r-1)%m]))
            unxt.append(u[j]+u[r]-L*(a[(j+1)%m]+d[(r-1)%m]))
            if a[(j+1)%m]==0 and row[j]+a[j]==9 and u[j]>L:
                tight=(t,j,'ascending',u[j]-L)
            if d[(j-1)%m]==0 and row[j]+d[j]==9 and u[j]>L:
                tight=(t,j,'descending',u[j]-L)
        assert nxt==W[(t+1)%8]
        u=unxt
    assert u==cert['slope_numerators']
    assert tight is not None
    for b in range(2,10):
        assert any((b-10)*x%L for x in cert['slope_numerators'])
    print(name,'INDEPENDENT integer recurrence PASS','base10-edges',8*m,'slope-denominator',L,'tight obstruction',tight)

def step(P,b):
    c=0;out=[]
    for v in P:
        a=v+c;c=a//b;out.append(a%b)
    if c:out.append(c)
    return [out[i]+out[-1-i] for i in range(len(out))],c

def controls(repo):
    root=repo/'calculation/decimal_frontier/lattice_formats'
    d=json.loads((root/'cert_b9_rec0.json').read_text())
    assert d['base']==9 and d['nB']==61 and d['m']==4 and d['gam']==[1,1,0,0,0,1,1,0,0,0]
    length=d['l0'];B=d['B_t'];w=d['w_t']
    for t in range(10):
        p=B[t]+[w[t][j%len(w[t])] for j in range(length)]+B[t][::-1]
        out,gam=step(p,9);assert gam==d['gam'][t]
        length+=gam
        expect=B[(t+1)%10]+[w[(t+1)%10][j%len(w[t])] for j in range(length)]+B[(t+1)%10][::-1]
        assert out==expect
    print('POSITIVE CONTROL base9 p10 g1100011000 m4 |B|61: ten exact edges PASS')
    for file,sz,start in [('Base13.lean',75,16),('Base13b.lean',55,8)]:
        source=(repo/'lean/P196/AbsorbingBand'/file).read_text()
        b={int(k):[int(x) for x in l.split(',')] for k,l in re.findall(r'def B(\d+) : List Nat := \[([^\]]+)\]',source)}
        assert set(b)==set(range(10)) and all(len(v)==sz for v in b.values())
        wlen=100;gword=[]
        for t in range(10):
            w=start if t%2==0 else 24-start
            P=b[t]+[w]*wlen+b[t][::-1]
            out,gam=step(P,13);gword.append(gam)
            wlen+=gam
            nextval=start if (t+1)%2==0 else 24-start
            assert out==b[(t+1)%10]+[nextval]*wlen+b[(t+1)%10][::-1]
        assert gword==[1,0,1,0,0,1,0,0,0,0]
        print(f'POSITIVE CONTROL base13 p10 g1010010000 |B|{sz}: ten exact edges PASS')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--snapshot',type=Path,default=Path('calculation/decimal_frontier/lattice_formats/agent14_p8_rows.json'))
    ap.add_argument('--slopes',type=Path,default=Path('calculation/decimal_frontier/lattice_formats/agent14_p8_slopes.json'))
    ap.add_argument('--repo',type=Path,default=Path.cwd())
    args=ap.parse_args()
    W=json.loads(args.snapshot.read_text());S=json.loads(args.slopes.read_text())
    for name in ('rec0','rec1','rec2'):check_cycle(name,W[name],S[name])
    controls(args.repo)
    print('ALL INDEPENDENT FIXED-ITINERARY CHECKS PASSED')
if __name__=='__main__':main()
