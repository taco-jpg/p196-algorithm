#!/usr/bin/env python3
"""Independent all-k time-rooted first-column check via 6-step transfer graph."""
from collections import defaultdict
from itertools import product
import argparse

def block_edges(b,g):
    p=len(g);edges=defaultdict(lambda:defaultdict(int));witness={}
    for first in range(1,2*b-1):
        for c in product((0,1),repeat=p):
            x=first;seq=[]
            for t,bit in enumerate(g):
                if x<0 or x>2*b-2 or (x+c[t])//b != int(bit):break
                seq.append(x)
                x=x%b+(1 if bit=='1' else (x+c[t])%b)
            else:
                if 0<=x<=2*b-2:
                    edges[first][x]+=1
                    witness[first,x]=(seq,c)
    return edges,witness

def periodic_counts(edges,kmax):
    # Closed time histories: trace of the weighted kth power of the
    # six-step transfer adjacency matrix. Count multiplicities exactly.
    values=[0]*kmax
    for start in edges:
        state={start:1}
        for k in range(1,kmax+1):
            nxt=defaultdict(int)
            for u,num in state.items():
                for v,weight in edges.get(u,{}).items():nxt[v]+=num*weight
            state=nxt
            values[k-1]+=state.get(start,0)
    return values

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--max-base',type=int,default=100);arg.add_argument('--max-k',type=int,default=8)
    opts=arg.parse_args();g='101100'
    for b in range(2,opts.max_base+1):
        for shift in range(6):
            word=g[shift:]+g[:shift]
            edges,w=block_edges(b,word)
            result=periodic_counts(edges,opts.max_k)
            want=[(4**k if b in (4,5,6) else 0) for k in range(1,opts.max_k+1)]
            assert result==want,(b,shift,result,want)
        if b in (2,3,4,5,6,7,10,50,100):print('PASS b',b,'all rotations k<=',opts.max_k, flush=True)
    print('COMPLETE finite controls',opts.max_base,opts.max_k)

if __name__=='__main__':main()
