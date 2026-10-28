#!/usr/bin/env python3
"""Construct exact integer and mod-4 proof certificates using only Python 3 standard library."""
from pathlib import Path
from fractions import Fraction
from math import gcd,lcm
import json,time
from model import parse,row,all_tags
OUT=Path('/tmp/agent3_rec2_spatial_certificates')
W,cu=parse(Path(__file__).with_name('lat2.txt'))
TAGS=list(all_tags(W));assert len(TAGS)==2252
SELECT={(7,7,1,0),(7,9,-1,0),(7,44,1,0),(7,45,1,0)}
def check_certificate(terms,mod):
 total={};rhs=0
 for tag,c in terms:
  eq,b=row(W,tuple(tag));rhs+=c*b
  for k,v in eq.items():total[k]=total.get(k,0)+c*v
 assert all((v%mod if mod else v)==0 for v in total.values())
 return rhs%mod if mod else rhs
def integer_certificates():
 piv={};certs=[]
 for index,tag in enumerate(TAGS):
  c,b=row(W,tag);c={j:Fraction(v) for j,v in c.items()};b=Fraction(b)
  proof={index:Fraction(1)}
  while c:
   k=min(c)
   if k not in piv:break
   v,rr,pp=piv[k];fac=c[k]
   for j,x in v.items():
    z=c.get(j,0)-fac*x
    if z:c[j]=z
    elif j in c:del c[j]
   b-=fac*rr
   for j,x in pp.items():
    z=proof.get(j,0)-fac*x
    if z:proof[j]=z
    elif j in proof:del proof[j]
  if not c:
   if b and tag in SELECT:
    den=1
    for x in proof.values():den=lcm(den,x.denominator)
    co={j:int(x*den) for j,x in proof.items()}
    div=0
    for x in co.values():div=gcd(div,abs(x))
    assert int(b*den)%div==0
    co={j:x//div for j,x in co.items()};rhs=int(b*den)//div
    terms=[[list(TAGS[j]),x] for j,x in sorted(co.items())]
    assert check_certificate(terms,None)==rhs
    certs.append({'tag':list(tag),'rhs':rhs,'coefficients':terms})
    print('INTEGER CERTIFICATE',tag,'terms',len(terms),'rhs',rhs,flush=True)
    if len(certs)==4:break
  else:
   k=min(c);d=c[k]
   piv[k]=({j:x/d for j,x in c.items()},b/d,{j:x/d for j,x in proof.items()})
 assert len(certs)==4
 GG=gcd(*(x['rhs'] for x in certs));assert GG==396,GG
 return {'gcd':GG,'certs':certs}
def modular4_certificate():
 M=4;rows=[]
 for name in TAGS:
  c,b=row(W,name);c={j:v%M for j,v in c.items() if v%M}
  rows.append([c,b%M,name,{name:1}])
 def vp(c):return (0 if c%2 else 1) if c else 2
 count=0
 while rows:
  i=min(range(len(rows)),key=lambda j:(min(vp(v) for v in rows[j][0].values()) if rows[j][0] else 3,len(rows[j][0])))
  c,b,tag,pr=rows.pop(i)
  if not c:
   if b:
    terms=[[list(k),v] for k,v in pr.items()]
    assert check_certificate(terms,4)==b==2
    return {'M':4,'rhs':b,'terms':terms}
   continue
  v=min(vp(x) for x in c.values());pivot=min(j for j,x in c.items() if vp(x)==v)
  factor=2**v;unit=c[pivot]//factor;scale=pow(unit,-1,4)
  c={j:x*scale%4 for j,x in c.items() if x*scale%4};b=b*scale%4
  pr={j:x*scale%4 for j,x in pr.items() if x*scale%4}
  assert c[pivot]==factor and b%factor==0
  keep=[]
  for d,z,name,proof in rows:
   u=d.get(pivot,0)
   if u:
    coeff=u//factor
    for j,x in c.items():
     r=(d.get(j,0)-coeff*x)%4
     if r:d[j]=r
     elif j in d:del d[j]
    z=(z-coeff*b)%4
    for j,x in pr.items():
     r=(proof.get(j,0)-coeff*x)%4
     if r:proof[j]=r
     elif j in proof:del proof[j]
   if not d and z:
    terms=[[list(k),val] for k,val in proof.items()]
    assert check_certificate(terms,4)==z==2
    print('MOD-4 CERTIFICATE',name,'terms',len(terms),'rhs=2',flush=True)
    return {'M':4,'rhs':z,'terms':terms}
   if d or z:keep.append([d,z,name,proof])
  rows=keep;count+=1
 raise AssertionError('mod-4 certificate not found')
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 t=time.monotonic();data=integer_certificates()
 (OUT/'int_certificates.json').write_text(json.dumps(data,separators=(',',':')))
 cert=modular4_certificate()
 (OUT/'mod4_certificate.json').write_text(json.dumps(cert,separators=(',',':')))
 print('CERTIFICATES WRITTEN',OUT,'seconds',round(time.monotonic()-t,2))
