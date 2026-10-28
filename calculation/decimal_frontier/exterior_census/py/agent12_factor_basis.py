#!/usr/bin/env python3
"""Exact complete base-10 first-column impossible-substring basis.

For a pair sum x_t in 0..18 at a single spatial position of the
canonical-root position automaton, choose upper carry h_t in {0,1};
its required overflow bit g_t = (x_t+h_t)//10 and its next coefficient is
x_(t+1) = x_t%10 + (1 if g_t else (x_t+h_t)%10).

A finite binary word w is locally impossible if no x-sequence can read
its bits starting at ANY x in 0..18 (thus it is impossible as a cyclic
substring of ANY time-closed root trajectory). A minimal impossible
substring has viable prefix w[:-1] and viable suffix w[1:]. Track their
reachable state subsets jointly. Exhaustively enumerate their finite graph
and its co-reachable-to-zero subgraph; if the latter has no cycles, all
minimal impossible substrings are explicitly enumerable, for ALL lengths.

Then use the complete basis in a weighted Aho automaton / Burnside-Mobius
necklace census. All counts are necessary filters, not B-cycle decisions.
"""
from __future__ import annotations
from collections import deque
from math import comb
import argparse,csv
B=10
U=(1<<(2*B-1))-1


def digit_transitions():
    R=[[0]*(2*B-1) for _ in (0,1)]
    for bit in (0,1):
        for x in range(2*B-1):
            for h in (0,1):
                if (x+h)//B!=bit:continue
                y=x%B+(1 if bit else (x+h)%B)
                R[bit][x]|=1<<y
    return R
R=digit_transitions()


def after(state,bit):
    out=0
    while state:
        v=state&-state
        out|=R[bit][v.bit_length()-1]
        state^=v
    return out


def word_state(w):
    x=U
    for c in w:x=after(x,int(c))
    return x


def factor_basis(max_states=100000):
    starts=[(after(U,0),U),(after(U,1),U)]
    assert all(x for x,_ in starts)
    states=starts[:]; index={s:i for i,s in enumerate(starts)}
    edges=[];kill=set()
    i=0
    while i<len(states):
        assert len(states)<max_states, 'unverified state-space cap hit'
        x,y=states[i]; row=[]
        for bit in (0,1):
            xx,yy=after(x,bit),after(y,bit)
            if not xx:
                if yy:kill.add((i,bit))
                row.append(-1)
            else:
                s=(xx,yy)
                if s not in index:
                    index[s]=len(states);states.append(s)
                row.append(index[s])
        edges.append(tuple(row));i+=1
    # Viable prefix states that can eventually reach a minimal killing edge.
    backward=[[] for _ in states]
    for i,row in enumerate(edges):
        for v in row:
            if v>=0:backward[v].append(i)
    co=set(i for i,b in kill);queue=deque(co)
    while queue:
        i=queue.popleft()
        for j in backward[i]:
            if j not in co:co.add(j);queue.append(j)
    # Complete, independent acyclicity check by Kahn's algorithm.
    indeg={i:0 for i in co}
    for i in co:
        for j in edges[i]:
            if j in co:indeg[j]+=1
    todo=deque(i for i in co if indeg[i]==0)
    seen=0
    while todo:
        i=todo.popleft();seen+=1
        for j in edges[i]:
            if j in co:
                indeg[j]-=1
                if indeg[j]==0:todo.append(j)
    assert seen==len(co), 'infinite minimal-factor language (cycle detected)'
    basis=[]
    def enumerate_paths(i,w):
        for bit,j in enumerate(edges[i]):
            z=w+str(bit)
            if (i,bit) in kill:basis.append(z)
            elif j in co:enumerate_paths(j,z)
    for i,bit in enumerate('01'):
        if i in co:enumerate_paths(i,bit)
    basis=tuple(sorted(basis,key=lambda w:(len(w),w)))
    assert len(basis)==len(set(basis))
    for w in basis:
        assert word_state(w)==0 and word_state(w[:-1]) and word_state(w[1:])
    return basis,len(states),len(co),len(kill)


def automaton(patterns):
    prefixes={''}
    for w in patterns:
        for n in range(1,len(w)):prefixes.add(w[:n])
    states=tuple(sorted(prefixes,key=lambda s:(len(s),s)))
    state_id={s:i for i,s in enumerate(states)}
    edges=[]
    for s in states:
        row=[]
        for bit in '01':
            w=s+bit
            if any(w.endswith(p) for p in patterns):row.append(-1);continue
            suffix=max((q for q in prefixes if w.endswith(q)),key=len)
            row.append(state_id[suffix])
        edges.append(tuple(row))
    return states,edges


def rooted_cyclic_avoid(p,edges):
    total=0
    for start in range(len(edges)):
        dp={(start,0):1}
        for _ in range(p):
            nd={}
            for (state,weight),count in dp.items():
                for bit,v in enumerate(edges[state]):
                    if v<0:continue
                    key=(v,weight+bit)
                    nd[key]=nd.get(key,0)+count
            dp=nd
        total+=sum(count for (s,w),count in dp.items() if s==start and 2*w<=p)
    return total


def divs(n):return [d for d in range(1,n+1) if n%d==0]
def gcd(a,b):
    while b:a,b=b,a%b
    return a

def phi(n):return sum(gcd(k,n)==1 for k in range(1,n+1))
def mobius(n):
    count=0;d=2
    while d*d<=n:
        if n%d==0:
            n//=d;count+=1
            if n%d==0:return 0
        d+=1
    return (-1)**(count+(n>1))


def direct(p,basis):
    all_root=ok_root=0;all_neck=set();ok_neck=set()
    for mask in range(1<<p):
        w=''.join(str((mask>>i)&1) for i in range(p))
        if 2*w.count('1')>p:continue
        all_root+=1
        key=min(w[i:]+w[:i] for i in range(p))
        all_neck.add(key)
        safe=all(not all(w[(i+j)%p]==c for j,c in enumerate(f))
                 for f in basis for i in range(p))
        if safe:ok_root+=1;ok_neck.add(key)
    return all_root,ok_root,len(all_neck),len(ok_neck)


def census(basis,nmax=32,brute=15):
    _,edges=automaton(basis)
    A={};D={};rows=[]
    for p in range(1,nmax+1):
        A[p]=rooted_cyclic_avoid(p,edges)
        D[p]=sum(comb(p,k) for k in range(p//2+1))
        b0=sum(phi(p//d)*D[d] for d in divs(p))
        b1=sum(phi(p//d)*A[d] for d in divs(p))
        b2=sum(mobius(p//d)*D[d] for d in divs(p))
        b3=sum(mobius(p//d)*A[d] for d in divs(p))
        assert all(x%p==0 for x in (b0,b1,b2,b3))
        n0,n1,k0,k1=(b0//p,b1//p,b2//p,b3//p)
        if p<=brute:
            assert direct(p,basis)==(D[p],A[p],n0,n1),(p,direct(p,basis),(D[p],A[p],n0,n1))
        rows.append({'p':p,'density_admissible_necklaces':n0,'excluded_necklaces':n0-n1,
              'surviving_necklaces':n1,'density_admissible_primitive':k0,
              'excluded_primitive':k0-k1,'surviving_primitive':k1})
    return rows,len(edges)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pmax',type=int,default=32)
    ap.add_argument('--brute-upto',type=int,default=15)
    ap.add_argument('--csv');a=ap.parse_args()
    basis,nodes,coreach,kill=factor_basis()
    print('BASIS',basis);print('SUBSET_GRAPH',nodes,'CO_REACH',coreach,'KILL_EDGES',kill)
    # Independent brute checks of every word at and beyond the longest basis length.
    for p in range(1,17):
        for mask in range(1<<p):
            w=''.join(str((mask>>i)&1) for i in range(p))
            impossible=not word_state(w)
            covered=any(v in w for v in basis)
            assert impossible==covered,(p,w,impossible,covered)
    print('PASS: all 131070 binary words of length 1..16 classified by basis')
    rows,aho=census(basis,a.pmax,a.brute_upto)
    print('AHO_STATES',aho)
    for r in rows:
        if r['p'] in (8,12,16,24,32):print('COUNT',r)
    if a.csv:
        with open(a.csv,'w',newline='') as f:
            writer=csv.DictWriter(f,list(rows[0]));writer.writeheader();writer.writerows(rows)
    print('PASS: complete finite factor basis and exact cyclic necklace count')

if __name__=='__main__':main()
