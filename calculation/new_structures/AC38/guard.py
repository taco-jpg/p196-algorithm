#!/usr/bin/env python3
"""Sound carry-set overapproximation for published p12/m9 phase-5 root."""
from pathlib import Path
from functools import lru_cache
import argparse

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/"calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
ALL19=(1<<19)-1

def load_exterior(path=SOURCE,phase=5):
    rows=[[int(y) for y in x.split()] for x in Path(path).read_text().splitlines() if x.strip()]
    assert len(rows)==38 and rows[0]==[12,34,9,10]
    assert all(len(row)==34 for row in rows[26:38])
    return rows[26+phase],rows[2+phase]

@lru_cache(None)
def normalize(mask,carry_mask):
    dm=0;co=0
    for c in (0,1):
        if carry_mask & (1<<c):
            for v in range(19):
                if mask & (1<<v):
                    z=v+c;dm|=1<<(z%10);co|=1<<(z//10)
    return dm,co

@lru_cache(None)
def sumset(a,b):
    result=0
    for x in range(10):
        if a & (1<<x):
            for y in range(10):
                if b & (1<<y):result|=1<<(x+y)
    return result

def next_masks(p):
    carry=1;d=[]
    for mask in p:
        dm,carry=normalize(mask,carry);d.append(dm)
    if carry not in (1,2):
        raise ValueError("terminal carry not singleton: "+str(carry))
    gamma=int(carry==2)
    if gamma:d.append(2)  # output's new leading decimal digit is 1
    n=len(d)
    return [sumset(d[i],d[n-1-i]) for i in range(n)],gamma

def prove(q=14,k=100,c_len=2,path=SOURCE):
    B,W=load_exterior(path)
    ext=B+W*q
    inner_len=2*(6+3*k)+c_len
    p=[1<<v for v in ext]+[ALL19]*inner_len+[1<<v for v in ext[::-1]]
    assert len(p)==2*(34+9*q+6+3*k)+c_len
    gammas=[]
    for _ in range(120):
        p,g=next_masks(p);gammas.append(g)
    known=0
    while known<len(p) and p[known].bit_count()==1:known+=1
    assert all(p[i]==1<<ext[i] for i in range(min(known,len(ext))))
    assert sum(gammas)==30
    return {"q":q,"k":k,"centre_len":c_len,
            "initial_length":len(p)-30,"final_length":len(p),
            "forced_prefix":known,"cut":len(ext),
            "growth_count":sum(gammas),"gamma_bits":"".join(map(str,gammas)),
            "root_idx8":p[8].bit_length()-1}

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--path",type=Path,default=SOURCE)
    a.add_argument("--q",type=int,default=14)
    a.add_argument("--k",type=int,default=100)
    a.add_argument("--centre-len",type=int,default=2)
    z=a.parse_args()
    print(prove(z.q,z.k,z.centre_len,z.path))
