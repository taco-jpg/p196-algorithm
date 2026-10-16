"""Replay symbolic gate transitions by sparse carry polynomials.

This checker does not import the run normalizer or align runs. Exponents
are affine tuples. It verifies polynomial identities for every parameter
value simultaneously, independently of finite integer controls.
"""
from collections import defaultdict
from pathlib import Path
import json


def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))


def minus(a,b):
    return tuple(x-y for x,y in zip(a,b))


def clean(poly):
    return {e:c for e,c in poly.items() if c}


def numerator(runs,carry_polynomial=False):
    dimension=len(runs[0][1])+1
    p=(0,)*dimension
    polynomial=defaultdict(int)
    carry=0
    for x,a,b in runs:
        assert b>0 and all(c>=0 for c in a)
        n=tuple(a)+(b,)
        end=plus(p,n)
        carry=int(x+carry>=10)
        # x=9 transmits; x<=8 kills and x>=10 sets. The outgoing
        # carry is therefore constant throughout this entire run.
        assert int(x+carry>=10)==carry
        coefficient=carry if carry_polynomial else x
        polynomial[end]+=coefficient
        polynomial[p]-=coefficient
        p=end
    return clean(polynomial),p,carry


def add(*polys):
    result=defaultdict(int)
    for poly in polys:
        for e,c in poly.items():result[e]+=c
    return clean(result)


def reverse_numerator(poly,width):
    return {minus(width,e):-c for e,c in poly.items()}


def check_transition(q,r,h_expected):
    P,L,h=numerator(q)
    C,_,_=numerator(q,True)
    assert h==h_expected
    unit=(0,)*(len(L)-1)+(1,)
    # D=Q+(x-10)C includes the final leading overflow digit, if any.
    D=add(P,{plus(e,unit):c for e,c in C.items()},
          {e:-10*c for e,c in C.items()})
    width=plus(L,tuple(0 for _ in L[:-1])+(h,))
    predicted=add(D,reverse_numerator(D,width))
    target,W,_=numerator(r)
    assert W==width
    assert predicted==target


def main():
    data=json.loads(Path(__file__).with_name('reservoir_gate.json').read_text())
    checked=0
    for name in ('three_band','seven_band_nonreturn','two_parameter_gate'):
        record=data[name]
        for q,r,h in zip(record['states'],record['states'][1:],record['overflow_flags']):
            check_transition(q,r,h);checked+=1
    result={'status':'all-parameter carry-polynomial identities verified',
            'transitions':checked,'uses_run_normalizer':False,
            'uses_parameter_samples_for_identities':False,
            'all_time_claim':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
