#!/usr/bin/env python3
"""Independent arithmetic checker for tracked base-50 certificate.
Does not import generator or position-automaton code.
Usage: python3 calculation/neutral_band/agent10_base50/check.py [data.json] [bigint_steps]
Default data path is cert_b50.json next to this file. Check 500 ordinary
Python arbitrary-precision integer reverse-and-add steps by default.
"""
from pathlib import Path
import json,sys

def normalize(base,word,initial):
    output=[];carry=initial
    for v in word:
        assert 0<=v<=2*(base-1)
        z=v+carry
        output.append(z-base*(z//base))
        carry=z//base
        assert carry in (0,1)
    return output,carry

def check_edges(data):
    b=data['base'];es=data['edges'];assert b==50 and len(es)==4
    assert data['width']==len(es[0]['B'])==36
    assert data['centre_length']==len(es[0]['C'])==8
    gain=0
    for i,edge in enumerate(es):
        B,C=edge['B'],edge['C']
        assert B and B[0]!=0 and C==C[::-1]
        assert all(0<=v<=2*b-2 for v in B+C)
        db,e=normalize(b,B,0)
        dc,e2=normalize(b,C,e)
        dr,g=normalize(b,list(reversed(B)),e2)
        assert e != e2
        assert (e,e2,g)==(edge['e'],edge['e2'],edge['gamma'])
        if g:
            top=(b-1)*(1-e)
            topc=(b-1)*(1-e2)
            rawB=[db[j]+([1]+dr[::-1])[j] for j in range(len(db))]+[top+dr[0]]
            rawC=[dc[0]+topc]+[dc[j]+dc[len(dc)-j] for j in range(1,len(dc))]+[topc+dc[0]]
        else:
            rawB=[db[j]+dr[len(dr)-1-j] for j in range(len(db))]
            rawC=[dc[j]+dc[len(dc)-1-j] for j in range(len(dc))]
        u,v=edge['u'],edge['v']
        assert all(z==b-1 for z in rawB[len(rawB)-u:]) if u else True
        assert rawB[:len(rawB)-u]==edge['B_next']
        assert (rawC[:v]==[b-1]*v and rawC[len(rawC)-v:]==[b-1]*v) if v else True
        assert rawC[v:len(rawC)-v if v else len(rawC)]==edge['C_next']
        gain+=u+v-g
        successor=es[(i+1)%4]
        assert edge['B_next']==successor['B'] and edge['C_next']==successor['C']
    assert gain==data['cycle_band_gain']==1
    return True

def digits(base,n):
    assert n>0
    d=[]
    while n:d.append(n%base);n//=base
    return d

def from_digits(base,d):
    acc=0
    for x in d[::-1]:acc=acc*base+x
    return acc

def initial_number(base,word):
    assert word==word[::-1]
    n=len(word)
    d=[0]*n
    for j in range(n//2):
        s=word[j];hi=min(s,base-1);lo=s-hi
        assert 0<=lo<base and 0<=hi<base
        d[j],d[n-1-j]=lo,hi
    if n&1:
        assert word[n//2]%2==0
        d[n//2]=word[n//2]//2
    assert d[-1]!=0
    return from_digits(base,d)

def check_bigint(data,steps):
    b=data['base'];edges=data['edges'];band=data['initial_band']
    def tmpl(edge,r):return edge['B']+[b-1]*r+edge['C']+[b-1]*r+edge['B'][::-1]
    n=initial_number(b,tmpl(edges[0],band))
    for t in range(steps):
        e=edges[t%4]
        d=digits(b,n)
        pair=[d[j]+d[len(d)-j-1] for j in range(len(d))]
        expected=tmpl(e,band)
        assert pair==expected,('mismatch',t,len(pair),len(expected))
        assert d!=d[::-1],('PALINDROME',t)
        nr=from_digits(b,d[::-1])
        n=n+nr
        band+=e['u']+e['v']-e['gamma']
        assert band>=data['initial_band']-1
    print('PASS: plain Python big-integer reverse+add and full pairword+nonpal',steps,'steps')
    print('LAST base50 length:',len(d),'neutral band:',band)

def main():
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('cert_b50.json')
    steps=int(sys.argv[2]) if len(sys.argv)>2 else 500
    with path.open() as f:data=json.load(f)
    check_edges(data)
    print('PASS: independent four-edge exact cycle, carry, trim, and positive band gain')
    check_bigint(data,steps)
if __name__=='__main__':main()
