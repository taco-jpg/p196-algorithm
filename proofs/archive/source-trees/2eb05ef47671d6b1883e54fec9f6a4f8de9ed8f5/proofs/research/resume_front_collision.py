"""Exact collision windows for symmetric8/6 fronts.

The overflow schedule is supplied, not established for an infinite integer
orbit. Boundary carries are universally branched in local computations.
"""
from itertools import product
import json

S=(4,5,6,7,8,9,10,11,13)


def local_step(q,h,incoming):
    carry=incoming;digits=[]
    for x in q:
        z=x+carry;digits.append(z%10);carry=z//10
    if h:
        # Drop the outer output pair, whose digits require omitted input.
        return tuple(digits[i]+digits[len(q)-i] for i in range(1,len(q)))
    return tuple(a+b for a,b in zip(digits,digits[::-1]))


def local_states(initial,steps=6):
    states={tuple(initial)}
    for t in range(steps):
        states={local_step(q,t%2,c) for q in states for c in (0,1)}
    return states


def numeric_q_step(q):
    carry=0;digits=[]
    for x in q:
        z=x+carry;digits.append(z%10);carry=z//10
    if carry:digits.append(carry)
    return tuple(a+b for a,b in zip(digits,digits[::-1])),carry


def representative(q):
    digits=[0]*len(q)
    for i in range(len(q)//2):
        lead=max(1 if i==0 else 0,q[i]-9)
        digits[-1-i]=lead;digits[i]=q[i]-lead
    if len(q)%2:digits[len(q)//2]=q[len(q)//2]//2
    return int(''.join(map(str,digits[::-1])))


def genuine_collision_examples():
    examples={}
    for x,y,s in product(range(19),range(19),S):
        p=(8,12,9,x,y,s,8)
        initial=p+p[::-1];q=initial
        for t in range(6):
            q,h=numeric_q_step(q)
            assert h==t%2
        central=q[len(q)//2]
        if central not in examples:
            n=representative(initial);orbit=[n]
            for _ in range(6):n+=int(str(n)[::-1]);orbit.append(n)
            assert len(str(n))%2==1
            assert 2*int(str(n)[len(str(n))//2])==central
            examples[central]=dict(seed=orbit[0],orbit=orbit,initial_q=initial)
    assert set(examples)==set(range(0,19,2))
    return examples


def gap_four_next_step_examples():
    """Actual N,O,N,O,N,O,N orbits realizing both center outcomes."""
    examples={}
    for seed in (130000000668400997,130000000668500997):
        digits=tuple(map(int,str(seed)))
        initial_q=tuple(a+b for a,b in zip(digits,digits[::-1]))
        assert initial_q[6:12]==(8,6,6,6,6,8)
        n=seed;orbit=[n];flags=[]
        for _ in range(7):
            old_length=len(str(n))
            n+=int(str(n)[::-1])
            flags.append(len(str(n))-old_length);orbit.append(n)
        assert flags==[0,1,0,1,0,1,0]
        def center_q(value):
            ds=str(value);i=len(ds)//2
            return int(ds[i])+int(ds[-1-i])
        assert center_q(orbit[6])==10
        final_center=center_q(orbit[7])
        examples[final_center]=dict(seed=seed,orbit=orbit,
                                   overflow_flags=flags,initial_q=initial_q)
    assert set(examples)=={0,2}
    return examples


def validate():
    for m in range(5,201):
        actual=local_states((8,)+(6,)*m+(8,))
        expected={(s,8)+(6,)*(m-5)+(8,s) for s in S}
        assert actual==expected
    expected={
      2:{(x,) for x in range(2,17,2)},
      3:{(s+2,s+2) for s in S},
      4:{(s,10,s) for s in S},
      5:{(s,8,8,s) for s in S}}
    for m,exp in expected.items():
        assert local_states((8,)+(6,)*m+(8,))==exp
    wake_collisions={}
    for m in range(5):
        states=set()
        for s in S:states.update(local_states((s,8)+(6,)*m+(8,s)))
        wake_collisions[m]=dict(count=len(states),states=sorted(states))
    return dict(general_lengths_checked=196,
                minimal_collisions={m:sorted(x) for m,x in expected.items()},
                wake_collisions=wake_collisions,
                actual_decimal_examples=genuine_collision_examples(),
                gap_four_next_step_examples=gap_four_next_step_examples(),
                infinite_existence_proved=False)


if __name__=='__main__':
    result=validate()
    open('resume_front_collision_results.json','w').write(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in('wake_collisions','actual_decimal_examples','gap_four_next_step_examples')},indent=2))
