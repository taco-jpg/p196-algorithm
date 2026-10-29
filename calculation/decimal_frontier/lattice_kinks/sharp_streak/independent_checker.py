#!/usr/bin/env python3
"""Independent bitset-matrix closure + canonical big-integer controls.
No import of the primary graph implementation.
"""
import json,sys
from pathlib import Path

def read_input(path):
    seq=list(map(int,Path(path).read_text().split()))
    assert seq[:4]==[12,34,9,10]
    g=seq[4:16]
    pos=16
    w=[seq[pos+9*t:pos+9*(t+1)] for t in range(12)];pos+=108
    cups=[seq[pos+9*t:pos+9*(t+1)] for t in range(12)];pos+=108
    b=[seq[pos+34*t:pos+34*(t+1)] for t in range(12)]
    assert pos+408==len(seq)
    return g,w,cups,b

def make_word(t,n,W,B):
    data=[0]*n
    for j in range((n+1)//2):
        val=B[t][j] if j<34 else W[t][(j-34)%9]
        if j==n-j-1 and val%2:val+=1 if val<18 else -1
        data[j]=data[n-j-1]=val
    return data

def canonical_step(p):
    n=len(p); digits=[0]*n
    for i in range((n+1)//2):
        q=p[i]
        if i==n-1-i:
            assert q%2==0;digits[i]=q//2
        else:
            upper=max(1 if i==0 else 0,q-9)
            digits[i]=q-upper;digits[n-1-i]=upper
            assert 0<=digits[i]<=9 and 0<=digits[n-1-i]<=9
    value=int(''.join(map(str,digits[::-1])))
    add=value+int(str(value)[::-1]);s=str(add)
    return [int(s[i])+int(s[-1-i]) for i in range(len(s))]

def matrix_table(p):
    n=len(p);output=canonical_step(p)
    assert len(output)==n
    c=[0]
    for v in p:c.append((v+c[-1])//10)
    assert c[-1]==0
    return [(p[52+r],output[52+r],c[52+r],c[n-52-r]) for r in range(9)]

def neighbours(front,table):
    out=0
    while front:
        bit=front&-front
        i=bit.bit_length()-1
        out|=table[i]
        front-=bit
    return out

def closure(seed,edges):
    visited=0;front=seed
    while True:
        new=front & ~visited
        if not new:return visited
        visited|=new
        front=neighbours(new,edges)

def calculate(tab):
    edge=[0]*36;different=[0]*36;reverse=[0]*36;count=0
    for r,(q,s,_,_) in enumerate(tab):
        for a in (0,1):
            for b in (0,1):
                i=4*r+2*a+b
                for v in range(19):
                    for u in (0,1):
                        if (v+u)//10!=b:continue
                        if (v+a)%10+(v+u)%10!=s:continue
                        j=4*((r+1)%9)+2*((v+a)//10)+u
                        count+=1
                        edge[i]|=1<<j
                        if v!=q:different[i]|=1<<j
                        reverse[j]|=1<<i
    base=0
    for r,(_,_,a,b) in enumerate(tab):base|=1<<(r*4+2*a+b)
    first=neighbours(base,different)
    initial=first.bit_count()
    relevant=closure(first,edge)&closure(base,reverse)
    depth=0;active=relevant
    while True:
        active=neighbours(active,different)&relevant
        if not active:break
        depth+=1
        assert depth<=36,('changed-only recurrent cycle',depth)
    # Separately test the initial changed edge from the baseline cut.
    initial_depth=0
    active=first&relevant
    while active:
        initial_depth+=1
        assert initial_depth<=36,('initial changed-cycle',initial_depth)
        active=neighbours(active,different)&relevant
    depth=max(depth,initial_depth)
    return [depth,relevant.bit_count(),count,initial]

def controls(path,expected_path):
    gam,W,cups,B=read_input(path)
    expected={r[0]:r[1:] for r in json.loads(Path(expected_path).read_text())}
    assert len(expected)==9
    for t in sorted(expected):
        for n in (400,401,800,801):
            p=make_word(t,n,W,B);tab=matrix_table(p)
            q=canonical_step(p)
            c=[0]
            for v in p:c.append((v+c[-1])//10)
            for j in range(72,n//2-11):
                assert (p[j],q[j],c[j],c[n-j])==tab[(j-52)%9]
            assert calculate(tab)==expected[t],(t,n,calculate(tab),expected[t])
    # Sharpness controls: both gamma0 7-column transfer witnesses must remain
    # indistinguishable under ordinary integer reverse-add for both parities.
    motifs={1:([4,5,10,14,13,12,9],[9,5,0,15,3,12,14],3),
            2:([9,11,1,10,8,5,9],[14,10,11,9,18,5,4],5)}
    for t,(original,repl,sharp) in motifs.items():
        for n in (400,401,800,801):
            p=make_word(t,n,W,B)
            assert p[59:66]==original
            changed=p[:]
            for j,val in enumerate(repl):
                changed[59+j]=changed[n-60-j]=val
            diffs=[a!=b for a,b in zip(original,repl)]
            runs=''.join('1' if z else '0' for z in diffs).split('0')
            assert max(map(len,runs))==sharp
            assert canonical_step(p)==canonical_step(changed)
    print('INDEPENDENT_BITSET_36_STATE_GRAPH_PASS 81 entries, 4 lengths each')
    print('INDEPENDENT_BIGINT_SHARPNESS_CONTROLS_PASS gamma0 phases 1,2 odd/even')

if __name__=='__main__':controls(sys.argv[1],sys.argv[2])
