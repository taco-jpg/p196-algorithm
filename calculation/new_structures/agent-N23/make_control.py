#!/usr/bin/env python3
"""Regenerate base-9 control from the documented lattice exterior B0 and W0.
Reconstruct digits by a symmetric split of pair coefficients, iterate ordinary
reverse-add, then infer every time-phase digit band independently.
"""
import json,sys
B0=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
W0=[1,1,15,15]
def seed(q):
    p=B0+[W0[i%4] for i in range(2+8*q)]+B0[::-1]
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=p[i]//2;d[-i-1]=p[i]-d[i]
    assert d[-1]>0
    return d

def add(d,b=9):
    carry=0;z=[]
    for x,y in zip(d,d[::-1]):
        s=x+y+carry;z.append(s%b);carry=s//b
    if carry:z.append(carry)
    return z

def infer(words,m=4):
    qs=sorted(words);arr=words[qs[0]];n=len(arr)
    out=[]
    for L in range(0,min(n,85)):
        v1=arr[L:L+m]
        if len(v1)<m:break
        if any(words[q][L:L+m*q]!=v1*q for q in qs):continue
        for R in range(0,min(n,85)):
            piece=arr[n-R-m*qs[0]:n-R if R else n]
            if len(piece)!=m*qs[0]:continue
            v2=piece[:m]
            if v1!=v2:continue
            if any(words[q][len(words[q])-R-m*q:len(words[q])-R if R else len(words[q])]!=v2*q for q in qs):continue
            centre=arr[L+m*qs[0]:n-R-m*qs[0]]
            if any(words[q][:L]!=arr[:L] or (words[q][-R:] if R else [])!=(arr[-R:] if R else []) or words[q][L+m*q:len(words[q])-R-m*q]!=centre for q in qs):continue
            out.append((L,R,len(centre),v1))
    if not out:return None
    L,R,c,v=min(out,key=lambda x:(x[2],abs(x[0]-61)+abs(x[1]-61)))
    assert c==0
    return {'parts':[{'digits':arr[:L]},{'motif':v,'slope':2,'offset':0},{'digits':arr[n-R:]}]}

def main(outpath,txtpath):
    snaps={q:[] for q in range(2,7)}
    for q in snaps:
        d=seed(q)
        for t in range(22):
            snaps[q].append(d)
            if t<21:d=add(d)
    assert all(snaps[q][21]==add(seed(q+1)) for q in snaps)
    phases=[]
    for t in range(1,21):
        x=infer({q:snaps[q][t] for q in snaps})
        if x is None:raise ValueError('No two-band template fit, phase '+str(t))
        phases.append(x)
    data={'base':9,'decimal_block_digits':1,'qmin':2,'cycle_parameter_gain':1,'phases':phases,'origin':'base9 lattice B0/W0 control, time phases 1..20'}
    with open(outpath,'w') as f:json.dump(data,f,separators=(',',':'))
    with open(txtpath,'w') as f:
        print(9,2,len(phases),file=f)
        for phase in phases:
            a,v,c=phase['parts']
            print(''.join(map(str,a['digits'])),''.join(map(str,v['motif'])),''.join(map(str,c['digits'])),file=f)
    print('Generated',outpath,txtpath,'phases',len(phases),'initial_length',len(snaps[2][1]))

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
