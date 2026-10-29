#!/usr/bin/env python3
"""All-base fixed-itinerary rigidity for the three decimal p8 nonmirror SCCs.
Pure standard library. Run from repo root:
  python3 calculation/decimal_frontier/lattice_formats/code/agent14_fixed_carry_lift.py
"""
import argparse, json, math, re
from fractions import Fraction as Q
from pathlib import Path
G=(1,0,1,0,1,0,1,0)

def parse_canonical(path):
    lines=[line for line in path.read_text().splitlines() if line.startswith('SCC p=8')]
    assert len(lines)==3
    out={}
    for k,line in enumerate(lines):
        match=re.fullmatch(r'SCC p=8 g=([01]+) size=(\d+) cyclen=(\d+) depth=(\d+) path=(.*?) cyc=(.*)',line)
        assert match,(k,line[:100])
        g,_,m,_,_,cyc=match.groups()
        assert g==''.join(map(str,G))
        cols=[list(map(int,s.split(','))) for s in re.findall(r'\[([0-9,]+)\]',cyc)]
        m=int(m);assert len(cols)==m and all(len(c)==8 for c in cols)
        out[f'rec{k}']=[[col[t] for col in cols] for t in range(8)]
    return out

def carries(w,b):
    m=len(w);ls=[];hs=[]
    for seed in (0,1):
        c=seed;row=[]
        for P in w:row.append(c);c=int(P+c>=b)
        if c==seed:ls.append(row)
        D=[0]*m;D[-1]=seed
        for j in range(m-2,-1,-1):D[j]=int(w[j+1]+D[j+1]>=b)
        if seed==int(w[0]+D[0]>=b):hs.append(D)
    assert len(ls)==len(hs)==1,(len(ls),len(hs))
    return ls[0],hs[0]

def check_physical(W):
    p=8;m=len(W[0]);c=[carries(row,10) for row in W]
    assert all(len(w)==m and all(0<=z<=18 for z in w) for w in W)
    for t in range(8):
        lo,hi=c[t];g=G[t]
        for j in range(m):
            prev=(j-g)%m
            out=(W[t][j]+lo[j])%10+(W[t][prev]+hi[prev])%10
            assert out==W[(t+1)%8][j],(t,j,out,W[(t+1)%8][j])
            assert lo[(j+1)%m]==int(W[t][j]+lo[j]>=10)
            assert hi[(j-1)%m]==int(W[t][j]+hi[j]>=10)
    return c

def slope_rhs(c,m):
    rhs=[0]*m
    for t in range(8):
        lo,hi=c[t];g=G[t]
        rhs=[rhs[j]+rhs[(j-g)%m]-(lo[(j+1)%m]+hi[((j-g)%m-1)%m]) for j in range(m)]
    return rhs

def solve_exact(c,m):
    # Every eight-step map has linear part 16(I+S)^4, S[x]_j=x_(j-1).
    rhs=slope_rhs(c,m)
    comb=(1,4,6,4,1)
    a=[]
    for j in range(m):
        line=[0]*m
        line[j]=1
        for k,v in enumerate(comb):line[(j-k)%m]-=16*v
        a.append([Q(z) for z in line]+[Q(rhs[j])])
    for i in range(m):
        q=next(j for j in range(i,m) if a[j][i])
        a[i],a[q]=a[q],a[i]
        pivot=a[i][i]
        a[i][i:]=[z/pivot for z in a[i][i:]]
        for j in range(m):
            if j==i or not a[j][i]:continue
            fac=a[j][i]
            a[j][i:]=[u-fac*v for u,v in zip(a[j][i:],a[i][i:])]
    return [row[-1] for row in a]

def prove_case(name,W):
    m=len(W[0]);c=check_physical(W)
    alpha=solve_exact(c,m)
    denominator=math.lcm(*[a.denominator for a in alpha])
    assert denominator>8
    sl=alpha[:];bad_upper=None
    for t in range(8):
        lo,hi=c[t]
        for j in range(m):
            for side,incoming,outgoing in (
                ('ascending',lo[j],lo[(j+1)%m]),
                ('descending',hi[j],hi[(j-1)%m])):
                if outgoing==0 and W[t][j]+incoming==9 and sl[j]>1 and bad_upper is None:
                    bad_upper=(t,j,side,W[t][j],incoming,outgoing,sl[j])
        g=G[t]
        sl=[sl[j]+sl[(j-g)%m]-(lo[(j+1)%m]+hi[((j-g)%m-1)%m]) for j in range(m)]
    assert sl==alpha
    assert bad_upper is not None, (name,'no b>10 obstruction found')
    low_coord=next(j for j,a in enumerate(alpha) if a.denominator>8)
    for base in range(2,10):
        assert ((base-10)*alpha[low_coord]).denominator>1
    print(f'{name}: m={m}; checked={8*m} row edges; slope-lcm={denominator}; '+
          f'fractional-coordinate={low_coord} slope={alpha[low_coord]}; '+
          f'b>10-obstruction={bad_upper}; no other integer b>=2 with SAME carries')
    return {"name":name,"m":m,"denominator":denominator,"coord":low_coord,
            "slope0":str(alpha[low_coord]),"witness":str(bad_upper)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--snapshot',type=Path,default=Path('calculation/decimal_frontier/lattice_formats/agent14_p8_rows.json'))
    parser.add_argument('--canonical',type=Path,default=Path('calculation/decimal_frontier/lattice_formats/p8_scc.txt'))
    args=parser.parse_args()
    data=json.loads(args.snapshot.read_text());assert data['overflow']=='10101010'
    assert args.canonical.exists(), "run from repository root with canonical p8_scc.txt"
    canonical=parse_canonical(args.canonical)
    assert all(canonical[n]==data[n] for n in ('rec0','rec1','rec2'))
    print('CANONICAL SCC SOURCE ROWS MATCH SNAPSHOT')
    for n in ('rec0','rec1','rec2'):prove_case(n,data[n])
    print('ALL THREE FIXED-ITINERARY RIGIDITY CASES PASSED')
if __name__=='__main__':main()
