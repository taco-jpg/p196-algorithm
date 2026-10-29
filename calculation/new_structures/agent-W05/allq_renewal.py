#!/usr/bin/env python3
"""W05 independent all-q symbolic checker for the N18 three-renewal centre.

Soundness principle: segments of a normalized symmetric pairword carry affine
position and length in q; variable segments are 20-periodic. Pairing an output
word with its reverse gives a finite crossing and residue partition. Beyond the
computed saturation bound the segment boundaries have fixed order, literal
segment overlaps are fixed and all variable-only overlaps expose every residue
mod 20. Thus checked finite q imply the identity for every integer q>=1.
"""
from dataclasses import dataclass
from math import ceil
import json

B_STR='''H501D4EC98FGHDH9144B8G09EB9B6DI947HF97D
8D5158982IEDFCC7B586AF7A47228AD8EBFE5HB
H6B2AGIG5HA8C65G2BGD1BG09E44H17I94C9CF4
8E8438GGCD99B9BC949B5397A498C98G8E7339A
H8H86HDE680040459A92B6IF09IH49ICI8F6791
8GGGEEC9BE804449F00C48FF6A8HCE8CCHECDGA
HDEEAA6049H08899A1149HBBE0IF69I56GA68E1
8C9A62764E788GI90225E7A4759FCG8EBD87ED6'''
W_STR='''H31DHBE3I12073ECF97D
CB45CA78CA327A8895HB
639B51FH5174F0HGIBF4
A9D1767ED68BA68FGB8A
2073ECF97DH31DHBE3I1
327A8895HBCB45CA78CA
74F0HGIBF4639B51FH51
8BA68FGB8AA9D1767ED6'''
B=[[int(z,19) for z in s] for s in B_STR.splitlines()]
W=[[int(z,19) for z in s] for s in W_STR.splitlines()]
M=20
U=[1]*40
U[13],U[20],U[30]=7,7,6
C=[8,0,0]+U+[16]+U[::-1]+[0,0,8]
assert C==C[::-1] and len(C)==87

def normalize(block, incoming):
    ds=[];c=incoming
    for v in block:
        k=v+c;ds.append(k%10);c=k//10
        assert 0<=c<=1
    return ds,c

def literal(v):return (0,len(v),v,False)
def variable(v,offset):return (len(v),-len(v)*offset,v,True)

@dataclass
class Part:
    start:tuple
    end:tuple
    pat:list
    repeat:bool
    def value(self,q,i):
        pos=i-(self.start[0]*q+self.start[1]);
        if self.repeat:return self.pat[pos%len(self.pat)]
        return self.pat[pos]

def pack_parts(spec):
    a=b=0; ret=[]
    for slope,offset,pat,r in spec:
        sa,sb=a,b
        a+=slope;b+=offset
        if pat:ret.append(Part((sa,sb),(a,b),pat,r))
    return ret

def reverse_parts(parts):
    length=parts[-1].end
    return [Part((length[0]-x.end[0],length[1]-x.end[1]),
                 (length[0]-x.start[0],length[1]-x.start[1]),
                 x.pat[::-1],x.repeat) for x in parts[::-1]]

def eval_part(parts,q):
    out=[]
    for x in parts:
        a=x.start[0]*q+x.start[1]; b=x.end[0]*q+x.end[1]
        assert b>=a
        out.extend(x.value(q,i) for i in range(a,b))
    return out

def q_saturation(all_parts):
    endpoints={p.start for group in all_parts for p in group}|{p.end for group in all_parts for p in group}
    crossings=0
    for sa,ba in endpoints:
        for sb,bb in endpoints:
            if sa!=sb:
                # Require strictly beyond all crossings of affine endpoints.
                crossings=max(crossings,(abs(ba-bb)+abs(sa-sb)-1)//abs(sa-sb))
    return crossings+M+2

def exact_one_step(t,center):
    a=B[t%8];w=W[t%8];an=B[(t+1)%8];wn=W[(t+1)%8]
    assert normalize(w,0)[1]==normalize(w,1)[1]
    assert normalize(w[::-1],0)[1]==normalize(w[::-1],1)[1]
    d0,c0=normalize(a,0)
    dw,c1=normalize(w,c0)
    dy,cy=normalize(w,c1)
    assert cy==c1
    dc,c2=normalize(center,c1)
    dr,c3=normalize(w[::-1],c2)
    dz,cz=normalize(w[::-1],c3)
    assert cz==c3
    dend,gamma=normalize(a[::-1],c3)
    assert gamma==int(t%2==0),(t,gamma)
    dparts=pack_parts([literal(d0+dw),variable(dy,1),literal(dc+dr),
                       variable(dz,1),literal(dend+([1] if gamma else []))])
    assert dparts[-1].end==(40,2*len(a)+len(center)+gamma)
    # Construct centre from q=1 actual resulting paired output, independently.
    d1=eval_part(dparts,1)
    p1=[d1[i]+d1[-1-i] for i in range(len(d1))]
    prefix=an+wn
    assert p1[:len(prefix)]==prefix,(t,'no first-band output',next((i for i in range(len(prefix)) if p1[i]!=prefix[i]),None))
    assert p1[-len(prefix):]==prefix[::-1]
    nc=p1[len(prefix):-len(prefix)]
    assert nc==nc[::-1] and len(nc)==len(center)+gamma
    targets=pack_parts([literal(an),variable(wn,0),literal(nc),variable(wn[::-1],0),literal(an[::-1])])
    rparts=reverse_parts(dparts)
    assert rparts[-1].end==targets[-1].end
    bound=q_saturation([dparts,rparts,targets])
    # Each source/reverse/target overlap has eventual stable endpoint ordering.
    # At q >= bound all growing overlaps are >= M long, so all residues mod M
    # appear. Literal intersected ranges have fixed offset and never grow.
    for q in range(1,bound+1):
        d=eval_part(dparts,q)
        expected=eval_part(targets,q)
        assert len(d)==len(expected)
        for i,(k,v) in enumerate(zip(expected, d)):
            if k!=v+d[-1-i]:
                raise AssertionError((t,q,i,k,v+d[-1-i],bound))
    return nc,bound

def main():
    center=C; maxima=(0,0); checkpoints=[]
    for t in range(264):
        center,bound=exact_one_step(t,center)
        maxima=max(maxima,(bound,t))
        if (t+1)%88==0:checkpoints.append({'t':t+1,'center_len':len(center),'head':center[:24], 'tail':center[-24:]})
        if t%44==0:print('t',t,'new_c_len',len(center),'bound',bound,flush=True)
    print(json.dumps({'checks':264,'all_positive_q':True,'largest_q_bound':maxima,'checkpoints':checkpoints}))

if __name__=='__main__':main()
