#!/usr/bin/env python3
"""Independent dynamic-programming census and constructive replay for F2 g_r.

Default r=1..5 all bases 2..2**(r+2)+3 and all time rotations.
Checkpoint after each (r,base), append-only, resume without recomputation.
Does not search beyond the canonical initial spatial coordinate.
"""
import argparse
import json
from pathlib import Path


def word(r):
    return '1'+'0'*r+'11'+'0'*(r+1)


def expected(b, r):
    a=1<<r
    return 4 if (b in (4,5,6) if r==1 else 2*a<=b<=4*a-3) else 0


def count_paths(b, g):
    bits=tuple(map(int,g))
    answer=0
    for first in range(1,2*b-1):
        frontier={first:1}
        for gam in bits:
            nxt={}
            for x,num in frontier.items():
                for c in (0,1):
                    if (x+c)//b != gam: continue
                    y=x%b+(1 if gam else (x+c)%b)
                    nxt[y]=nxt.get(y,0)+num
            frontier=nxt
            if not frontier:break
        answer+=frontier.get(first,0)
    return answer


def construct(b,r):
    if expected(b,r)!=4: return None
    a=1<<r
    if b==2*a: U,V=a-1,0
    elif b<=3*a: U,V=b-2*a-1,b-2*a+1
    else:
        U=b-3*a-1
        V=U+a+3
    cs=[0]*(2*r+4)
    for j in range(r):
        cs[1+j]=(U>>(r-1-j))&1
    cs[r+1]=1
    for j in range(r+1):
        cs[r+3+j]=(V>>(r-j))&1
    g=word(r)
    first=2*a+V
    vals=[]; x=first
    for t, gam in enumerate(map(int,g)):
        assert (x+cs[t])//b==gam, ('carry',r,b,t,x,cs[t])
        vals.append(x)
        x=x%b+(1 if gam else (x+cs[t])%b)
    assert x==first, ('close',r,b)
    assert all(1<=v<=2*b-2 for v in vals),('coeff range',r,b)
    return vals,cs


def main():
    pa=argparse.ArgumentParser()
    pa.add_argument('--min-r',type=int,default=1)
    pa.add_argument('--max-r',type=int,default=7)
    pa.add_argument('--output',type=Path,default=Path('/tmp/agent16_param_f1_progress.jsonl'))
    args=pa.parse_args()
    done={}
    if args.output.exists():
        for line in args.output.read_text().splitlines():
            obj=json.loads(line)
            done[obj['r'],obj['base']]=obj
    for r in range(args.min_r,args.max_r+1):
        g=word(r)
        for b in range(2,(1<<(r+2))+4):
            key=(r,b)
            if key in done: continue
            values=[]
            for k in range(len(g)):
                actual=count_paths(b,g[k:]+g[:k])
                assert actual==expected(b,r), (r,b,k,actual,expected(b,r))
                values.append(actual)
            if expected(b,r): construct(b,r)
            row={'r':r,'base':b,'rotations':values,'expected':expected(b,r)}
            with args.output.open('a') as f: f.write(json.dumps(row)+'\n')
            if b%8==0: print(f'CHECK r={r} b={b} all {len(g)} rotations agree',flush=True)
        print(f'DONE r={r} tested bases 2..{(1<<(r+2))+3}',flush=True)
    print('COMPLETE',flush=True)

if __name__=='__main__':main()
