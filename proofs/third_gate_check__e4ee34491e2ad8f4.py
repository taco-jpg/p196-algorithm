"""Decide precisely the next two-step reuse of the four double-return images.

This checks a six-update composition, not arbitrary later selected returns.
All r=13+k are exact affine calculations; r=1,...,12 are independent controls.
"""
from __future__ import annotations
import json
from pathlib import Path
import padded_core_classification as pc
from seam_overlap import literal_step,realize
from variable_overlap import shifted_double

HERE=Path(__file__).resolve().parent
CASES=((1,6,1),(5,6,2),(6,6,2),(10,6,2))

def run_case(u,v):
 a=pc.component(1,u,v);q=pc.phi(a,1);states=[];aa=[a];qq=[q]
 for t in range(1,7):
  safe=pc.safe(q);a,ha=pc.run.step(a);q,hq=pc.run.step(q)
  d=pc.size(q)-pc.size(a);assert d.coefficients==(0,)
  s=d.constant
  states.append({'time':t,'clock_a':ha,'clock_q':hq,'shift':s,
                 'closed':s>=0 and q==pc.phi(a,s),'safe':safe})
  aa.append(a);qq.append(q)
 return states,aa,qq

def finite(u,v,r):
 a=(1,)+(0,)*r+(u,v,v,u)+(0,)*r+(1,);q=shifted_double(a,1);states=[]
 for t in range(1,7):
  n=realize(q);n+=int(str(n)[::-1]);safe=str(n)!=str(n)[::-1]
  na=literal_step(a);nq=literal_step(q);ha=len(na)-len(a);hq=len(nq)-len(q)
  a,q=na,nq;s=len(q)-len(a)
  states.append({'time':t,'clock_a':ha,'clock_q':hq,'shift':s,
                 'closed':s>=0 and q==shifted_double(a,s),'safe':safe})
 return states

def main():
 pc.GAP=pc.run.Length((1,),13)
 result={'status':'third two-step reuse fails for all four double-return images',
         'affine_domain':'r=13+k for every k>=0','small_domain':'every r from valid minimum through 12',
         'updates':6,'cases':[],'literal_parameter_instances':0}
 for u,v,rmin in CASES:
  st,aa,qq=run_case(u,v);exceptions=[]
  assert st[3]['closed'] and not st[5]['closed']
  for r in tuple(range(rmin,14))+(29,):
   actual=finite(u,v,r);result['literal_parameter_instances']+=1
   assert actual[3]['closed'] and not actual[5]['closed']
   if r>=13:
    assert actual==st
    for t in range(1,7):
     assert literal_step(pc.run.expand(aa[t-1],(r-13,)))==pc.run.expand(aa[t],(r-13,))
     assert literal_step(pc.run.expand(qq[t-1],(r-13,)))==pc.run.expand(qq[t],(r-13,))
   elif actual!=st:exceptions.append({'r':r,'states':actual})
  result['cases'].append({'u':u,'v':v,'r_min':rmin,'states':st,
    'component_at_6':pc.run.as_json(aa[6]),'whole_at_6':pc.run.as_json(qq[6]),
    'small_spacer_exceptions':exceptions})
 (HERE/'third_gate_check.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
