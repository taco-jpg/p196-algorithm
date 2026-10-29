#!/usr/bin/env python3
"""Sound centre-wide proof of identical actual carry ports and overflow clock.
An overapproximation that allows all centre digits independently (stronger
than palindromic restriction) is checked for every C length 7..14.
"""
import abstract
def carries(p,cut):
    carry=1;at=None
    for i,pm in enumerate(p):
        if i==cut:at=carry
        cout=0
        for v in abstract.bits(pm):
            for c in abstract.bits(carry):cout|=1<<((v+c)//10)
        carry=cout
    return at,carry
def check(u,cl,q=14,k=100,s=60):
    h=abstract.B+abstract.W*q+[5]+list(abstract.U[u])*k
    begin=len(h);cut=34+9*q+1+3*(k-s)
    p=[1<<x for x in h+[0]*cl+h[::-1]]
    for i in range(begin,begin+cl):
        p[i]=(abstract.MASK19 if not(cl%2 and i==begin+cl//2)
              else sum(1<<j for j in range(0,19,2)))
    ports=[];mindistance=1000000
    for t,g in enumerate(abstract.G):
        cm,gm=carries(p,cut+t)
        assert cm and cm&(cm-1)==0,(u,cl,t,'ambiguous port',cm)
        assert gm==(1<<g),(u,cl,t,'ambiguous clock',gm)
        ports.append(cm.bit_length()-1)
        uncertain=[i for i,x in enumerate(p) if x.bit_count()>1]
        if uncertain:mindistance=min(mindistance,min(uncertain)-(cut+t))
        p=abstract.step(p,g)
    return (u,cl,30,mindistance,''.join(map(str,ports)))
if __name__=='__main__':
    for u in range(3):
        for cl in range(7,15):print('PORT_CERT',*check(u,cl))
