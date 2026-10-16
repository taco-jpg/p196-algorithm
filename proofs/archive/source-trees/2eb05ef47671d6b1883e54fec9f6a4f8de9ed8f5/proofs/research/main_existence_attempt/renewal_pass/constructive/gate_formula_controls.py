"""Independent integer controls for the proved gate and overflow formulas.

Proofs for every spacer length are in STATUS.md. These finite controls do not
stand in for those proofs. No symbolic run engine is used in this file.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'main_existence_attempt/correlation_pass/constructive'))
from seam_overlap import canonical,literal_step,pair,realize
from variable_overlap import shifted_double
HERE=Path(__file__).resolve().parent
GROUPS={
 'I':[(u,v) for u in range(1,4) for v in range(5,8) if u+v<=8],
 'II':[(u,v) for u in range(5,9) for v in range(5,7) if u+v<=13],
 'III':[(u,v) for u in range(10,14) for v in range(5,7) if u+v<=18],
}
RS=tuple(range(1,33))+(64,127,256)

def digits(q):
 n=sum(x*10**i for i,x in enumerate(q))
 d=tuple(map(int,str(n)[::-1]))
 return d+(0,)*max(0,len(q)-len(d))

def local(length,start,coefficients):
 a=[0]*length;a[start:start+len(coefficients)]=coefficients
 return tuple(a)

def plus(a,b):
 assert len(a)==len(b)
 return tuple(x+y for x,y in zip(a,b))

def minus(a,b):
 assert len(a)==len(b)
 return tuple(x-y for x,y in zip(a,b))

def component(p,r,u,v):return (p,)+(0,)*r+(u,v,v,u)+(0,)*r+(p,)

def first_component(p,r,u,v,group):
 if group in ('I','II'):return component(2*p,r,2*u,2*v)
 return (2*p,)+(0,)*(r-1)+(1,2*u-20,2*v+1,2*v+1,2*u-20,1)+(0,)*(r-1)+(2*p,)

def returned_component(p,r,u,v,group):
 if group=='I':return component(4*p,r,4*u+1,4*v-19)
 if group=='II':core=(1,4*u-19,4*v-18,4*v-18,4*u-19,1)
 else:core=(2,4*u-39,4*v-17,4*v-17,4*u-39,2)
 return (4*p,)+(0,)*(r-1)+core+(0,)*(r-1)+(4*p,)

def check(p,r,u,v,group):
 a=component(p,r,u,v);q=shifted_double(a,1)
 assert canonical(a) and canonical(q)
 a1=literal_step(a);q1=literal_step(q);raw1=shifted_double(a1,1)
 assert a1==first_component(p,r,u,v,group)
 length=len(q)
 if group=='II':
  delta=local(length,r+1,(1,-19,-18,-19,1))
  e=local(length,r+1,(1,1,0,-1,-1))
 else:
  delta=local(length,r+2,(1,-20,1))
  e=local(length,r+2,(1,0,-1))
 assert minus(q1,raw1)==delta
 h=int(p>=5)
 assert len(digits(q1))==length+h
 assert minus(digits(q1),digits(raw1))==e+(0,)*h
 a2=literal_step(a1);q2=literal_step(q1)
 # This is precisely the independent-overlap commutation needed in the proof.
 assert pair(digits(raw1))==shifted_double(a2,1)
 defect=minus(q2,shifted_double(a2,1))
 if not h:
  assert a2==returned_component(p,r,u,v,group)
  assert not any(defect)
  n=realize(q)
  for _ in range(2):
   n+=int(str(n)[::-1]);assert str(n)!=str(n)[::-1]
 else:
  derivative=(e[0],)+tuple(e[i]-e[i-1] for i in range(1,len(e)))+(-e[-1],)
  assert defect==derivative and any(defect)

DOUBLE_RETURNS={
 (1,6):(1,(1,1,2,2,1,1)),
 (5,6):(2,(4,5,5,5,5,4)),
 (6,6):(2,(5,1,6,6,1,5)),
 (10,6):(2,(8,5,9,9,5,8)),
}

def double_return(u,v,r,core):
 a=component(1,r,u,v);q=shifted_double(a,1);n=realize(q)
 closed=[];safe=[]
 for t in range(1,7):
  a=literal_step(a);q=literal_step(q);n+=int(str(n)[::-1])
  closed.append(len(q)==len(a)+1 and q==shifted_double(a,1))
  safe.append(str(n)!=str(n)[::-1])
  if t==4:
   expected=(16,)+(0,)*(r-1)+core+(0,)*(r-1)+(16,)
   assert a==expected and q==shifted_double(expected,1)
  if t==6:assert a[0]==14 and q[0]==15 and len(q)==len(a)+1
 assert closed[:4]==[False,True,False,True] and all(safe[:4])
 assert not closed[5]
 return {'r':r,'u':u,'v':v,'closed':closed,'safe':safe}

def main():
 gate_controls=overflow_controls=0
 for group,pairs in GROUPS.items():
  for u,v in pairs:
   for p in range(1,5):
    for r in RS:check(p,r,u,v,group);gate_controls+=1
   for p in range(5,10):
    for r in RS:
     if r<2:continue
     check(p,r,u,v,group);overflow_controls+=1
 double=[]
 for (u,v),(minimum,core) in DOUBLE_RETURNS.items():
  for r in RS:
   if r>=minimum:double.append(double_return(u,v,r,core))
 # The excluded r=1,p=9 boundary can overflow one phase earlier. Preserve it.
 a=component(9,1,10,5);q=shifted_double(a,1)
 exception={'p':9,'r':1,'u':10,'v':5,'component_first_clock':len(literal_step(a))-len(a),
            'whole_first_clock':len(literal_step(q))-len(q)}
 assert exception['component_first_clock']==0 and exception['whole_first_clock']==1
 result={'status':'all stated integer controls PASS; all-r proofs are in STATUS.md',
         'spacers':RS,'core_groups':GROUPS,
         'gate_literal_controls':gate_controls,'overflow_literal_controls':overflow_controls,
         'double_return_literal_controls':len(double),'double_return_boundary_cases':[d for d in double if d['r']<=3],
         'overflow_formula_excluded_boundary_counterexample':exception,
         'generic_transport':'e antisymmetric at old width L and common final carry h implies output defect (1-x^h)e',
         'all_time_safety':False,'finite_Lychrel_witness':False}
 (HERE/'gate_formula_controls.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
