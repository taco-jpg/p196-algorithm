#!/usr/bin/env python3
"""W28 independent local carry table, arbitrary mask controls and integer checks."""
import random
B=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
def pairword(k,sites):
    h=list(B+W*k+(8,))
    for j in sites:
        assert 3<=j<=k-4
        i=39+20*j+5
        assert tuple(h[i:i+3])==(11,14,3)
        h[i:i+3]=[6,6,7]
    return h+h[-2::-1]
def step(p):
    d=[];c=0
    for a in p:
        a+=c;d.append(a%10);c=a//10
    if c:d.append(c)
    return [a+b for a,b in zip(d,reversed(d))]
def local(p,i,gamma):
    assert p[i-1]!=9 and p[i]!=9
    if gamma:
        return ((p[i]+(p[i-1]>=10))%10+(p[i-1]+(p[i]>=10))%10)
    assert p[i+1]!=9
    return ((p[i]+(p[i-1]>=10))%10+(p[i]+(p[i+1]>=10))%10)
def integer_of(p):
    assert p==p[::-1] and len(p)%2
    n=len(p);d=[0]*n
    for i in range(n//2):
        v=p[i];d[i]=max(0,v-9);d[n-1-i]=v-d[i]
    d[n//2]=p[n//2]//2
    assert d[-1]!=0
    return int(''.join(map(str,d[::-1])))
def check():
    s=39+20*3+5
    a,b=pairword(10,[]),pairword(10,[3])
    expected=[[(11,6),(14,6),(3,7)],[(10,14),(7,12),(8,13),(12,16)],[(1,10),(15,6),(17,8),(5,14)],[]]
    for t,g in enumerate((1,0,1)):
        assert len(a)==len(b)
        diffs=[(i,a[i],b[i]) for i in range(len(a)//2+1) if a[i]!=b[i]]
        assert [(x,y) for _,x,y in diffs]==expected[t]
        assert [i for i,_,_ in diffs]==list(range(s,s+len(diffs)))
        aa,bb=step(a),step(b)
        for i in range(s-1,s+5):
            assert local(a,i,g)==aa[i] and local(b,i,g)==bb[i]
        a,b=aa,bb
        assert len(a)==2*(39+20*10)+1+sum((1,0,1)[:t+1])
    assert a==b
    print('LOCAL_TABLE: three-step non-gauge packet erases; exact local carries PASS')
    rng=random.Random(281028);cases=0;physical=0
    for k in (8,9,10,12,15,20,25,50,100,260,420):
        for trial in range(40):
            sites=[j for j in range(3,k-3) if rng.randrange(7)==0]
            a,b=pairword(k,[]),pairword(k,sites)
            if k<=25 and trial<3:
                n0,n1=integer_of(a),integer_of(b)
            for _ in range(3):
                if k<=25 and trial<3:
                    s0,s1=str(n0),str(n1)
                    assert [int(x)+int(y) for x,y in zip(s0[::-1],s0)]==a
                    assert [int(x)+int(y) for x,y in zip(s1[::-1],s1)]==b
                    n0+=int(s0[::-1]);n1+=int(s1[::-1])
                a,b=step(a),step(b)
            assert a==b,(k,trial)
            if k<=25 and trial<3:
                n0+=int(str(n0)[::-1]);n1+=int(str(n1)[::-1])
                assert n0==n1;physical+=1
            cases+=1
    print(f'INDEPENDENT_MASKS: {cases} whole pairword erasures PASS')
    print(f'PHYSICAL_INTEGER: {physical} independent short integer coalescences PASS')
    print('ALL CHECKS PASSED')
if __name__=='__main__':check()
