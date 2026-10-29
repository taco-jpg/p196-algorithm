#!/usr/bin/env python3
"""Agent N02: symbolic one-step preimage and inductive refinement of regular centres.
No negative-width census; seeks a finite automaton fixed point for the DECIMAL p8 centre.
"""
from collections import deque
from carry_relation import DFA,literal_step
from decimal_cut_probe import exterior_rows

B=10; A=2*B-1; g=[1,0,1,0,1,0,1,0]

def dfa_prefix(B_t,odd):
    """Physically valid halfwords starting with B_t, no centre bound.
    All tracked B_t contain odd pair coefficients (nonpalindrome guard).
    """
    k=len(B_t);sink=k+3;tab=[]
    for s in range(sink+1):
        rr=[sink]*A
        if s<k:rr[B_t[s]]=s+1
        elif s==k:
            for a in range(A):rr[a]=(k+1 if a%2==0 else k+2)
        elif s in (k+1,k+2):
            for a in range(A):rr[a]=k+1 if a%2==0 else k+2
        tab.append(rr)
    finals={k,k+1,k+2} if not odd else {k+1}
    return DFA(0,finals,tab)

def preimage(target,odd,gam,state_limit=20000):
    """Determinize exact NFA for predecessor of target under one reverse-add.
    No source word cap: every reachable subset is explored.
    """
    # NFA state (low,high,previous_high,target_DFA_state,first)
    start=(0,gam,-1,target.initial,True)
    END='END'
    def step_one(s,a):
        if s==END:return ()
        low,high,prev,dst,first=s
        if first and a==0:return ()
        out=[]
        if odd and a%2==0 and (a+low)//B==high:
            mid=(a+low)%B
            z=2*mid if gam==0 else mid+(gam if first else prev)
            if target.go(dst,z) in target.finals:out.append(END)
        v=a+low;low2=v//B
        for high2 in (0,1):
            if (a+high2)//B!=high:continue
            hi=(a+high2)%B
            z=v%B+hi if gam==0 else v%B+(gam if first else prev)
            out.append((low2,high2,hi,target.go(dst,z),False))
        return tuple(out)
    def accept(s):
        if s==END:return True
        if odd:return False
        low,high,prev,dst,first=s
        if first or low!=high:return False
        if gam:dst=target.go(dst,2*prev)
        return dst in target.finals
    startsubset=frozenset((start,))
    subsets=[startsubset]; ids={startsubset:0};tab=[];finals=set()
    for subset in subsets:
        if len(subsets)>state_limit:raise RuntimeError(('STATE_CAP',state_limit,len(subsets)))
        si=ids[subset]
        if any(accept(s) for s in subset):finals.add(si)
        row=[]
        for a in range(A):
            nxt=frozenset(x for s in subset for x in step_one(s,a))
            if nxt not in ids:
                ids[nxt]=len(subsets);subsets.append(nxt)
            row.append(ids[nxt])
        tab.append(row)
    return DFA(0,finals,tab)

def intersect(a,b,limit=80000):
    pairs=[(a.initial,b.initial)];ids={pairs[0]:0};tab=[];finals=set()
    for pair in pairs:
        if len(pairs)>limit:raise RuntimeError(('INTERSECT_CAP',len(pairs)))
        s,t=pair;i=ids[pair]
        if s in a.finals and t in b.finals:finals.add(i)
        row=[]
        for z in range(A):
            nxt=(a.go(s,z),b.go(t,z))
            if nxt not in ids:ids[nxt]=len(pairs);pairs.append(nxt)
            row.append(ids[nxt])
        tab.append(row)
    return DFA(0,finals,tab)

def minimize(d):
    """Unoptimized partition refinement on a complete reachable DFA."""
    N=len(d.table)
    blocks=[set(range(N))-d.finals, set(d.finals)]
    blocks=[x for x in blocks if x]
    for _ in range(N+1):
        c=[-1]*N
        for j,block in enumerate(blocks):
            for state in block:c[state]=j
        refined=[]
        for block in blocks:
            bins={}
            for state in block:
                key=tuple(c[v] for v in d.table[state])
                bins.setdefault(key,set()).add(state)
            refined.extend(bins.values())
        if len(refined)==len(blocks):
            break
        blocks=refined
    else:raise AssertionError('minimization did not converge')
    state_map={s:i for i,part in enumerate(blocks) for s in part}
    return DFA(state_map[d.initial],{state_map[s] for s in d.finals},[[state_map[v] for v in d.table[next(iter(part))]] for part in blocks])

def shortest(d):
    qq=deque([d.initial]); seen={d.initial:()}
    while qq:
        s=qq.popleft()
        if s in d.finals:return seen[s]
        for z in range(A):
            t=d.go(s,z)
            if t not in seen:seen[t]=seen[s]+(z,);qq.append(t)
    return None

def run(levels=4):
    pref=exterior_rows();U=[[dfa_prefix(pref[t],odd) for odd in (0,1)] for t in range(8)];S=U
    for k in range(levels+1):
        summary=[]
        for t in range(8):
            for odd in (0,1):
                witness=shortest(S[t][odd]);summary.append((t,odd,len(S[t][odd].table),len(witness) if witness else -1))
                if witness:
                    p=witness;eps=odd
                    for i in range(k):
                        gam,q=literal_step(p,bool(eps),B)
                        assert gam==g[(t+i)%8],('gamma',t,i,gam)
                        eps=(eps+gam)%2
                        p=q
                        assert len(p)>=len(pref[(t+i+1)%8]) and list(p[:len(pref[0])])==pref[(t+i+1)%8]
        print('DEPTH',k,'SUM',summary,flush=True)
        if k==levels:break
        NS=[[None,None] for _ in range(8)]
        for t in range(8):
            for odd in (0,1):
                tar=S[(t+1)%8][(odd+g[t])%2]
                pre=preimage(tar,bool(odd),g[t])
                common=intersect(U[t][odd],pre)
                NS[t][odd]=minimize(common)
        S=NS
    return S

if __name__=='__main__':
    import sys
    run(int(sys.argv[1]) if len(sys.argv)>1 else 4)