#!/usr/bin/env python3
"""Independent decimal seed construction. No repository imports."""
import argparse, json, pathlib, hashlib
B0=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
W0=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
B1=(8,13,5,1,5,8,9,8,2,18,14,13,15,12,12,7,11,5,8,6,10,15,7,10,4,7,2,2,8,10,13,8,14,11,15,14,5,17,11)
W1=(12,11,4,5,12,10,7,8,12,10,3,2,7,10,8,8,9,5,17,11)
def split(P):
    assert P==P[::-1] and P[len(P)//2]%2==0
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=P[i]//2;d[-1-i]=P[i]-d[i]
    if len(P)%2:d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]>0
    return d
def step(d):
    o=[]; carry=0
    for a,b in zip(d,reversed(d)):
        x=a+b+carry;o.append(x%10);carry=x//10
    if carry:o.append(carry)
    return o
def pairs(d):return [a+b for a,b in zip(d,reversed(d))]
def construct(k,m,q,packet=False):
    H=list(B1)+list(W1)*k+[5,5,2]*m+[18]*q
    if packet:
        j=len(B1)+20*k+3*50+1
        assert H[j:j+3]==[5,2,5]
        H[j:j+3]=[7,7,7]
    return split(H+[18]+H[::-1])
def string(d):return ''.join(str(i) for i in reversed(d))
def main():
    ar=argparse.ArgumentParser();ar.add_argument('--k',type=int,default=300);ar.add_argument('--m',type=int,default=80);ar.add_argument('--q',type=int,default=6500);ar.add_argument('--out',default='/tmp/x29_seeds');a=ar.parse_args()
    source=split(list(B0)+list(W0)*20+[18]+list(W0[::-1])*20+list(B0[::-1]))
    phase=pairs(step(source))
    assert phase[:39]==list(B1) and phase[39:59]==list(W1)
    assert phase[39:39+20*15]==list(W1)*15
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    data={}
    for name,k,q,packet in [('base',a.k,a.q,False),('packet',a.k,a.q,True),('plus',a.k,a.q+1,False)]:
        d=construct(k,a.m,q,packet)
        s=string(d)
        (out/(name+'.seed')).write_text(s+'\n')
        data[name]={'digits':len(s),'sha256':hashlib.sha256(s.encode()).hexdigest()}
    if a.k<=40 and a.q<=100:
        nums=[int((out/(x+'.seed')).read_text().strip()) for x in ('base','packet','plus')]
        for t in range(151):
            z=[str(x) for x in nums]
            assert all(s!=s[::-1] for s in z)
            if t>=5:assert nums[0]==nums[1]
            if t>=4:assert pairs([int(c) for c in z[0][::-1]])==pairs([int(c) for c in z[1][::-1]])
            if t<150:nums=[x+int(str(x)[::-1]) for x in nums]
    (out/'seed_metadata.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data))
if __name__=='__main__':main()
