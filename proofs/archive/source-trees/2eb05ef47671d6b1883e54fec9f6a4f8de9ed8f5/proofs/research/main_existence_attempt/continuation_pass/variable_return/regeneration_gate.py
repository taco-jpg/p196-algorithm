"""Exact finite safe regeneration gate, its origin, and its failed return.

The affine certificate covers R=4+k, k>=0; the R=3 boundary is ordinary
integer arithmetic. There is no claim of a recurrent safe family.
"""
from pathlib import Path
import json
import sys
import hashlib

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'main_existence_attempt/smart_pass/collision'))
import orthant_runs as run

HERE=Path(__file__).resolve().parent
ONE=run.Length((0,),1)
R=run.Length((1,),4)

# state at time t = B bulk^(R+offset) H bulk^(R+offset) reverse(B).
TEMPLATES=[
 ((18,18,4),(14,0,0,14),9,0),
 ((9,18,13,14),(4,5,0,5,4),9,-1),
 ((10,8,13,9,4),(14,9,5,5,9,14),9,-2),
 ((1,9,12,3,14,14),(4,4,15,10,15,4,4),9,-3),
 ((3,9,4,8),(11,2,11),9,1),
 ((6,18,8,17),(2,6,2),9,1),
 ((13,16,18,14),(5,12,5),9,1),
 ((4,11,16,14,4),(15,8,8,15),9,0),
 ((9,3,14,9,10),(10,17,17,10),9,0),
 ((18,7,9,0,2),(2,16,16,2),0,0),
]


def family(template):
    b,h,bulk,offset=template
    gap=R+run.Length((0,),offset)
    return run.canon([(v,ONE) for v in b]+[(bulk,gap)]+[(v,ONE) for v in h]
                     +[(bulk,gap)]+[(v,ONE) for v in b[::-1]])


def literal(template,r):
    b,h,bulk,offset=template
    assert r+offset>=0
    return b+(bulk,)*(r+offset)+h+(bulk,)*(r+offset)+b[::-1]


def realize(q):
    d=[0]*len(q)
    for i in range(len(q)//2):
        d[i]=max(q[i]-9,0)
        d[-i-1]=min(q[i],9)
    if len(q)%2:
        assert q[len(q)//2]%2==0
        d[len(q)//2]=q[len(q)//2]//2
    return int(''.join(map(str,d[::-1])))


def pair(n):
    s=str(n)
    return tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))


def main():
    q=family(TEMPLATES[0])
    states=[run.as_json(q)]
    clocks=[]
    for target in TEMPLATES[1:]:
        symbols={s for s,_ in q}
        assert max(symbols)>=10 and not(q[0][0]==11 and symbols<={0,11})
        q,h=run.step(q)
        assert q==family(target)
        clocks.append(h)
        states.append(run.as_json(q))
    assert clocks==[1,1,1,0,0,0,1,0,0]
    controls=[]
    for r in list(range(3,35))+[64,127,1024]:
        n=realize(literal(TEMPLATES[0],r))
        values=[str(n)]
        for t in range(1,10):
            n+=int(str(n)[::-1])
            assert pair(n)==literal(TEMPLATES[t],r)
            assert str(n)!=str(n)[::-1]
            values.append(str(n))
        controls.append({'R':r,'integers':values})
    # The source gate g=0 is itself canonically realizable, whether or not
    # one chooses to reach it through the three-step originating family.
    gate=literal(TEMPLATES[3],3)
    seed=realize(gate)
    n=seed
    primitive_values=[str(n)]
    for _ in range(2):
        n+=int(str(n)[::-1])
        assert str(n)!=str(n)[::-1]
        primitive_values.append(str(n))
    result={'status':'exact safe finite regeneration; no recurrent return',
            'origin_parameter':'R>=3','affine_parameter':'R=4+k, k>=0',
            'gate_parameter':'g=R-3>=0','templates':TEMPLATES,'states':states,
            'overflow_clock':clocks,'safe_positive_outputs':9,
            'primitive_g0_seed':str(seed),'primitive_g0_first_two_outputs':primitive_values[1:],
            'ordinary_integer_controls':controls,
            'origin_return_at_time9_to_R_plus2':False,
            'failed_return_witness':{'actual_second_coefficient':7,'target_second_coefficient':18,
                                     'actual_bulk':0,'target_bulk':9},
            'decimal_lychrel_existence_proved':False}
    path=HERE/'regeneration_gate.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('states','ordinary_integer_controls')},indent=2))


if __name__=='__main__':
    main()
