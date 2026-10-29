#!/usr/bin/env python3
"""Independent reachability and canonical ordinary-integer control.
Reads the original repo lattice data and an independently computed 9x9
root-reachable-state-count table. No import from classify.py.
python3 independent_check.py <lat_p12m9.txt> <counts.json>
"""
import sys,json
from pathlib import Path

def load(path):
    z=list(map(int,Path(path).read_text().split()))
    p,bwidth,m,b=z[:4]
    assert (p,bwidth,m,b)==(12,34,9,10)
    pos=4
    gam=z[pos:pos+p];pos+=p
    W=[z[pos+9*t:pos+9*t+9] for t in range(p)];pos+=p*9
    carries=[z[pos+9*t:pos+9*t+9] for t in range(p)];pos+=p*9
    B=[z[pos+bwidth*t:pos+bwidth*(t+1)] for t in range(p)];pos+=p*bwidth
    assert pos==len(z)
    return gam,W,carries,B

def generate(t,n,W,B):
    P=[0]*n
    for i in range((n+1)//2):
        q=B[t][i] if i<34 else W[t][(i-34)%9]
        if n%2 and i==n//2 and q%2:q+=1 if q<18 else -1
        P[i]=P[n-1-i]=q
    return P

def carry_from_pair(P):
    c=[0]
    for v in P:c.append((c[-1]+v)//10)
    return c

def ordinary(P):
    n=len(P)
    lo=[0]*n
    for i in range((n+1)//2):
        if i==n-1-i:
            assert P[i]%2==0
            lo[i]=P[i]//2
        else:
            q=P[i];upper=max(1 if i==0 else 0,q-9);lower=q-upper
            assert 0<=lower<=9 and 0<=upper<=9
            lo[i]=lower;lo[n-1-i]=upper
    value=int(''.join(str(v) for v in reversed(lo)))
    out=value+int(str(value)[::-1])
    d=[int(v) for v in str(out)]
    return [d[i]+d[-1-i] for i in range(len(d))]

def table(P):
    n=len(P);C=carry_from_pair(P)
    Q=ordinary(P)
    assert len(Q)==n
    return [(P[52+r],Q[52+r],C[52+r],C[n-52-r]) for r in range(9)]

def independent_matrix(tab,root):
    # States encoded as integers (position residue * 4 + carry bits).
    # Matrix of the 36-state regular language over nonbaseline coefficients.
    adjacency=[0]*36
    for r,(q,output,a0,b0) in enumerate(tab):
        for left in (0,1):
            for right in (0,1):
                source=r*4+left*2+right
                for qnew in range(19):
                    if qnew==q:continue
                    new_left=(qnew+left)//10
                    for next_right in (0,1):
                        if (qnew+next_right)//10==right and (qnew+left)%10+(qnew+next_right)%10==output:
                            target=((r+1)%9)*4+new_left*2+next_right
                            adjacency[source]|=1<<target
    ra,rb=tab[root][2:]
    start=root*4+ra*2+rb
    reached=0
    current=adjacency[start]
    layers=0
    while current and layers<37:
        layers+=1
        # No successful return to the expected boundary carry pair at any positive length.
        for r in range(9):
            a,b=tab[r][2:]
            goal=r*4+a*2+b
            assert not ((current>>goal)&1),('false theorem',root,layers,goal)
        nxt=current & ~reached
        if not nxt:break
        reached|=nxt
        future=0
        while nxt:
            low=nxt&-nxt
            i=low.bit_length()-1
            future|=adjacency[i]
            nxt-=low
        current=future
    assert layers<=37
    return reached.bit_count()

def control():
    gam,W,C,B=load(sys.argv[1]); counts=json.loads(Path(sys.argv[2]).read_text())
    byphase={row[0]:row[1:] for row in counts}
    assert len(byphase)==9 and set(byphase)=={1,2,3,5,6,7,9,10,11}
    for t in byphase:
        allcounts=[]
        for n in (800,801):
            p=generate(t,n,W,B)
            tab=table(p)
            assert carry_from_pair(p)[-1]==0
            # Periodic validation at 100 spatial positions, including reflected columns.
            Q=ordinary(p);C0=carry_from_pair(p)
            for i in range(70,170):
                assert (p[i],Q[i],C0[i],C0[n-i])==tab[(i-52)%9]
            allcounts.append([independent_matrix(tab,r) for r in range(9)])
        assert allcounts[0]==allcounts[1]==byphase[t],(t,allcounts,byphase[t])
    # Positive controls: genuine seven-column collision motifs which REQUIRE
    # at least one unchanged internal site, and thus must not be excluded.
    motifs={1:([9,5,0,15,3,12,14],[4,5,10,14,13,12,9]),
            2:([14,10,11,9,18,5,4],[9,11,1,10,8,5,9])}
    for phase,(repl,expected) in motifs.items():
        for n in (800,801):
            p=generate(phase,n,W,B)
            i=59
            assert p[i:i+7]==expected
            changed=p.copy()
            for j,v in enumerate(repl):changed[i+j]=changed[n-1-i-j]=v
            assert changed!=p and any(changed[i+j]==p[i+j] for j in range(7))
            assert ordinary(changed)==ordinary(p)
            # direct numeral addition never uses the pairword normalization recurrence.
    # Negative controls: all 18 single coefficient substitutions in one gamma0 phase.
    base=generate(2,800,W,B); out=ordinary(base)
    for replacement in range(19):
        if replacement==base[59]:continue
        test=base.copy();test[59]=test[740]=replacement
        assert ordinary(test)!=out
    print('INDEPENDENT_MATRIX_81_ROOTS_EVEN_ODD_PASS')
    print('CANONICAL_BIGINT_7_COLUMN_POSITIVE_CONTROLS_PASS')
    print('CANONICAL_BIGINT_18_SINGLE_SITE_NEGATIVE_CONTROLS_PASS')

if __name__=='__main__':control()
