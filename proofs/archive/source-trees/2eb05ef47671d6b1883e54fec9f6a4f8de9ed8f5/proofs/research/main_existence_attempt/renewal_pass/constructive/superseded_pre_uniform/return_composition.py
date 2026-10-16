"""Exact test of a second two-step return on every new two-step gate image.

The run arithmetic covers all r=9+k, k>=0; r=1,...,8 are literal checks.
Only the fixed four-update question is decided. No long-orbit claim is made.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import padded_core_classification as pc
from seam_overlap import canonical,literal_step,realize
from variable_overlap import shifted_double

HERE=Path(__file__).resolve().parent
CORE_GROUPS={
 'I': [(u,v) for u in range(1,4) for v in range(5,8) if u+v<=8],
 'II': [(u,v) for u in range(5,9) for v in range(5,7) if u+v<=13],
 'III': [(u,v) for u in range(10,14) for v in range(5,7) if u+v<=18],
}

def one_case(p,u,v):
 a=pc.component(p,u,v);q=pc.phi(a,1)
 states=[];aa=[a];qq=[q]
 for t in range(1,5):
  safe=pc.safe(q)
  a,ha=pc.run.step(a);q,hq=pc.run.step(q)
  d=pc.size(q)-pc.size(a)
  assert d.coefficients==(0,)
  s=d.constant
  states.append({'time':t,'clock_a':ha,'clock_q':hq,'shift':s,
                 'closed':s>=0 and q==pc.phi(a,s),'safe':safe})
  aa.append(a);qq.append(q)
 assert not states[0]['closed'] and states[1]['closed']
 return states,aa,qq

def literal(p,u,v,r):
 a=(p,)+(0,)*r+(u,v,v,u)+(0,)*r+(p,)
 q=shifted_double(a,1);out=[]
 for t in range(1,5):
  n=realize(q);n+=int(str(n)[::-1])
  safe=str(n)!=str(n)[::-1]
  na=literal_step(a);nq=literal_step(q)
  ha=len(na)-len(a);hq=len(nq)-len(q);a,q=na,nq
  s=len(q)-len(a)
  out.append({'time':t,'clock_a':ha,'clock_q':hq,'shift':s,
              'closed':s>=0 and q==shifted_double(a,s),'safe':safe})
 return out

def main():
 pc.GAP=pc.run.Length((1,),9)
 cases=[];exceptions=[];controls=0
 for p in range(1,5):
  for group,pairs in CORE_GROUPS.items():
   for u,v in pairs:
    states,aa,qq=one_case(p,u,v)
    cases.append({'p':p,'u':u,'v':v,'group':group,'states':states,
                  'component_at_4':pc.run.as_json(aa[4]),
                  'whole_at_4':pc.run.as_json(qq[4])})
    for r in tuple(range(1,10))+(17,):
     actual=literal(p,u,v,r);controls+=1
     if r>=9:
      assert actual==states,(p,u,v,r,states,actual)
      for t in range(1,5):
       assert literal_step(pc.run.expand(aa[t-1],(r-9,)))==pc.run.expand(aa[t],(r-9,))
       assert literal_step(pc.run.expand(qq[t-1],(r-9,)))==pc.run.expand(qq[t],(r-9,))
     elif actual!=states:
      exceptions.append({'p':p,'u':u,'v':v,'r':r,'states':actual})
 second=[{k:c[k] for k in ('p','u','v','group')} for c in cases
          if not c['states'][2]['closed'] and c['states'][3]['closed']]
 result={'status':'complete second-gate-image class; no indefinite recurrence',
         'domain':{'p':'1..4','cores':CORE_GROUPS,'r':'all integers >=1'},
         'affine_domain':'r=9+k for every k>=0','updates':4,
         'exact_affine_cases':len(cases),'independent_literal_parameter_instances':controls,
         'second_genuine_return_cases':second,'small_spacer_exceptions':exceptions,
         'all_cases':cases}
 (HERE/'return_composition.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('all_cases',)},indent=2))

if __name__=='__main__':main()
