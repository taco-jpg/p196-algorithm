#!/usr/bin/env python3
"""Independent ordinary decimal bigint replay, checking complete words and nonpalindromicity."""
import json,sys
j=json.load(open(sys.argv[1]));assert j['base']==100 and len(j['phases'])>=2
def word_value(phase,q):
    groups=[]
    for part in phase['parts']:
        groups+=part['digits'] if 'digits' in part else part['motif']*(part['slope']*q+part['offset'])
    assert groups[-1]>0
    return sum(x*100**i for i,x in enumerate(groups))
def rev(n):return int(str(n)[::-1])
for q in [0,1,2,10,50,100,250]:
    x=int('12'+'99'*(52+q)+'34')
    for t,phase in enumerate(j['phases']):
        assert x==word_value(phase,q),(q,t,'word mismatch')
        assert x!=rev(x),(q,t,'palindrome')
        if t+1<len(j['phases']):x=x+rev(x)
    print('PASS q=',q,len(j['phases'])-1,'ordinary decimal steps, exact complete state words, no palindrome')
