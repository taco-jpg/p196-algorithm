"""Exact two-parameter collision and regeneration, with a missing return.

The proofs are symbolic carry identities in a nonnegative integer orthant.
Literal integer reversal supplies independent finite implementation controls.
No finite Lychrel witness is asserted.
"""
from pathlib import Path
import json
from orthant_runs import Length,constant,canon,normal,add_runs,step,expand,as_json


def trace(q,count):
    states=[q];clock=[]
    for _ in range(count):
        # A surviving coefficient 18 excludes both palindrome predecessors.
        assert any(x==18 and n.positive() for x,n in q)
        # Direct symbolic safety check as well: normalize the actual output
        # digits and exhibit a positive-length unequal mirrored interval.
        digits,h=normal(q)
        if h:
            digits=canon(digits+[(1,constant(1,len(q[0][1].coefficients)))])
        differences=add_runs(digits,[(-x,n) for x,n in digits[::-1]])
        assert any(x!=0 and n.positive() for x,n in differences)
        q,h=step(q);states.append(q);clock.append(h)
    return states,clock


def three_band():
    e=lambda n:constant(n,1)
    m=Length((1,),6)
    q=[(9,e(2)),(18,m),(9,e(2))]
    states,clock=trace(q,12)
    assert states[-1]==[(9,e(7)),(18,m-e(5)),(9,e(7))]
    assert sum(clock)==5
    return states,clock


def seven_band_nonreturn():
    e=lambda n:constant(n,1)
    m=Length((1,),6)
    q=[(9,e(7)),(18,m),(9,e(7))]
    states,clock=trace(q,12)
    left=[(x,e(1)) for x in (8,17,7,12,13)]+[(9,e(2))]
    left += [(x,e(1)) for x in (5,6,11,1,10)]
    assert states[-1]==left+[(18,m-e(5))]+left[::-1]
    assert states[-1][0][0]==8
    return states,clock


def collision_gate():
    e=lambda n:constant(n,2)
    m=Length((1,0),8);n=Length((0,1),7)
    q=[(9,e(2)),(18,e(5)),(9,e(2)),(0,n),(9,e(2)),(18,m),
       (9,e(2)),(0,n),(9,e(2)),(18,e(5)),(9,e(2))]
    states,clock=trace(q,13)
    expected12=[(9,e(14)),(0,n-e(5)),(9,e(7)),(18,m-e(5)),
                (9,e(7)),(0,n-e(5)),(9,e(14))]
    expected13=[(18,e(14)),(0,n-e(6)),(1,e(1)),(9,e(7)),(17,e(1)),
                (18,m-e(7)),(17,e(1)),(9,e(7)),(1,e(1)),
                (0,n-e(6)),(18,e(14))]
    assert states[12]==expected12
    assert states[13]==expected13
    assert clock[-1]==0 and sum(clock)==5
    # Initial q has odd coefficients; later safety follows from the previous
    # state's 18 coefficient. The endpoint also has explicit odd coefficients.
    assert any(x%2 and length.positive() for x,length in q)
    assert any(x%2 and length.positive() for x,length in states[-1])
    return states,clock


def realize(q):
    assert q==q[::-1]
    d=[0]*len(q)
    for i in range(len(q)//2):
        d[i]=max(0,q[i]-9)
        d[-1-i]=q[i]-d[i]
    if len(q)%2:
        assert q[len(q)//2]%2==0
        d[len(q)//2]=q[len(q)//2]//2
    assert d[-1]>0
    return int(''.join(map(str,d[::-1])))


def pair_sums(n):
    digits=tuple(map(int,str(n)[::-1]))
    return tuple(x+y for x,y in zip(digits,digits[::-1]))


def controls(states,values):
    count=0
    for params in values:
        n=realize(expand(states[0],params))
        for t,q in enumerate(states):
            assert pair_sums(n)==expand(q,params)
            assert str(n)!=str(n)[::-1]
            if t+1<len(states):
                n+=int(str(n)[::-1]);count+=1
    return count


def finite_counterexample():
    # Central reservoir of length 5 is exhausted. The state at step 12 is
    # 9^14, so its next ordinary reverse-and-add result is a palindrome.
    q=(9,9)+(18,)*5+(9,9)
    n=realize(q);seed=n
    for t in range(14):
        if t==12:assert pair_sums(n)==(9,)*14
        if t==13:
            assert str(n)==str(n)[::-1]
            return dict(seed=str(seed),first_palindrome_step=13,palindrome=str(n))
        assert str(n)!=str(n)[::-1]
        n+=int(str(n)[::-1])


def main():
    a,ha=three_band();b,hb=collision_gate();c,hc=seven_band_nonreturn()
    controls_a=controls(a,[(k,) for k in range(32)]+[(100,),(1000,)])
    controls_b=controls(b,[(m,n) for m in range(15) for n in range(15)]+[(100,137)])
    controls_c=controls(c,[(k,) for k in range(16)])
    result={
        "status":"exact collision components; no recurrent family",
        "three_band":{"domain":"M=6+k, k>=0","overflow_flags":ha,
                      "states":[as_json(q) for q in a]},
        "seven_band_nonreturn":{"domain":"M=6+k, k>=0","overflow_flags":hc,
                               "states":[as_json(q) for q in c]},
        "two_parameter_gate":{"domain":"M=8+k, N=7+l, independent integers k,l>=0",
                              "overflow_flags":hb,"states":[as_json(q) for q in b],
                              "initial_q_mass":"18M+288","after_12_q_mass":"18M+288",
                              "after_13_q_mass":"18M+540"},
        "independent_integer_control_transitions":controls_a+controls_b+controls_c,
        "exhausted_reservoir_counterexample":finite_counterexample(),
        "variable_time_return_proved":False,"finite_Lychrel_witness":False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('three_band','seven_band_nonreturn','two_parameter_gate')},indent=2))


if __name__=='__main__':main()
