#!/usr/bin/env python3
"""Independent actual-big-integer / schoolbook double-step replay.
No import of local_certificate.py or discover.cpp.
"""
import sys,json
from pathlib import Path

def inputs(file):
    z=list(map(int,Path(file).read_text().split()))
    assert z[:4]==[12,34,9,10]
    g=z[4:16]
    w=[z[16+9*t:16+9*(t+1)] for t in range(12)]
    k=16+108+108
    border=[z[k+34*t:k+34*(t+1)] for t in range(12)]
    assert k+408==len(z)
    return g,w,border

def pair(t,n,W,B):
    out=[0]*n
    for j in range((n+1)//2):
        v=B[t][j] if j<34 else W[t][(j-34)%9]
        if j==n-j-1 and v%2:v+=1 if v<18 else -1
        out[j]=out[n-j-1]=v
    return out

def digits_of_pair(P):
    n=len(P);d=[0]*n
    for j in range((n+1)//2):
        v=P[j]
        if n-j-1==j:
            assert v%2==0;d[j]=v//2
        else:
            upper=max(v-9,1 if j==0 else 0)
            lower=v-upper
            assert 0<=lower<=9 and 0<=upper<=9
            d[j]=lower;d[n-j-1]=upper
    assert d[-1]>0
    return d

def pair_of_number(N):
    digits=list(map(int,str(N)))
    return [digits[j]+digits[-1-j] for j in range(len(digits))]

def reverseadd_integer(N):return N+int(str(N)[::-1])

def reverseadd_schoolbook(d):
    carry=0;answer=[];n=len(d)
    for i in range(n):
        v=d[i]+d[n-i-1]+carry
        answer.append(v%10)
        carry=v//10
    if carry:answer.append(carry)
    return answer

def normalize_pair(P):
    carry=0;answer=[]
    for q in P:
        v=q+carry
        answer.append(v%10)
        carry=v//10
    if carry:answer.append(carry)
    return [answer[i]+answer[-1-i] for i in range(len(answer))]

def check(file,motif_file):
    g,W,B=inputs(file)
    motifs=json.loads(Path(motif_file).read_text())
    checked=0
    for motif in motifs:
        t,r,vals=motif['phase'],motif['residue'],motif['replace']
        assert len(vals)==3
        for n in (200,201,218,219,400,401,418,419,800,801,1800,1801):
            for shift in (0,9,18,36,72):
                j=52+r+shift
                if j+30>=n//2:continue
                P=pair(t,n,W,B)
                Q=P.copy()
                for offset,new in enumerate(vals):
                    i=j+offset
                    assert new!=P[i],(t,r,n,shift)
                    Q[i]=Q[n-i-1]=new
                A=digits_of_pair(P);D=digits_of_pair(Q)
                av=int(''.join(map(str,A[::-1])))
                dv=int(''.join(map(str,D[::-1])))
                assert av!=dv
                assert pair_of_number(av)==P and pair_of_number(dv)==Q
                A1=reverseadd_schoolbook(A)
                D1=reverseadd_schoolbook(D)
                a1=reverseadd_integer(av)
                d1=reverseadd_integer(dv)
                assert A1==list(map(int,str(a1)[::-1]))
                assert D1==list(map(int,str(d1)[::-1]))
                assert len(A1)==len(D1)==n+g[t]
                P1=pair_of_number(a1)
                Q1=pair_of_number(d1)
                assert P1==normalize_pair(P) and Q1==normalize_pair(Q)
                assert P1!=Q1
                A2=reverseadd_schoolbook(A1)
                D2=reverseadd_schoolbook(D1)
                a2=reverseadd_integer(a1)
                d2=reverseadd_integer(d1)
                assert A2==list(map(int,str(a2)[::-1]))
                assert D2==list(map(int,str(d2)[::-1]))
                assert len(A2)==len(D2)==n+g[t]+g[(t+1)%12]
                assert pair_of_number(a2)==pair_of_number(d2)
                assert normalize_pair(P1)==normalize_pair(Q1)==pair_of_number(a2)
                # Stronger actual-integer coalescence at the NEXT (third) step.
                assert a2!=d2,('early integer coalescence',t,r,n,shift)
                a3=reverseadd_integer(a2);d3=reverseadd_integer(d2)
                assert a3==d3,('third-step integer noncoalescence',t,r,n,shift)
                checked+=1
    assert checked>=300
    print('INDEPENDENT_BIGINT_AND_SCHOOLBOOK_TWO_STEP_PASS',checked,'cases')

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    check(sys.argv[1] if len(sys.argv)>1 else str(root/'lattice_input.txt'),
          sys.argv[2] if len(sys.argv)>2 else str(root/'motifs.json'))
