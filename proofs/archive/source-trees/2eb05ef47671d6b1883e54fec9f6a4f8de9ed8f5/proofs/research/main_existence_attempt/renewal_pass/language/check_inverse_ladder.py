"""Independent all-parameter carry-polynomial and integer audit.

No generator, reverse-add transducer, automata synthesis, or run normalizer
is imported. Each affine run is checked symbolically on the entire k>=0
domain. The relevant pre-existing first-hit11 proof is replayed as data.
"""
from collections import defaultdict
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent


def clean(p):
    return {e:c for e,c in p.items() if c}


def plus(a,b):
    return a[0]+b[0],a[1]+b[1]


def combine(*polys):
    out=defaultdict(int)
    for p in polys:
        for e,c in p.items():out[e]+=c
    return clean(out)


def scaled(p,f):
    return {e:c*f for e,c in p.items() if c*f}


def numerator(runs,carrying=False):
    # (x-1) times the represented polynomial. A run contributes only its
    # two endpoints; endpoint exponents are affine pairs (coefficient,k0).
    p=defaultdict(int)
    position=(0,0)
    carry=0
    for value,coefficient,constant in runs:
        assert len(coefficient)==1 and coefficient[0]>=0 and constant>=1
        end=plus(position,(coefficient[0],constant))
        if carrying:
            assert 0<=value<=18
            incoming=carry
            carry=(value+incoming)//10
            assert carry in (0,1)
            assert (value+carry)//10==carry
            assert 0<=value+incoming-10*carry<=9
            assert 0<=value-9*carry<=9
            digit=carry
        else:digit=value
        p[end]+=digit;p[position]-=digit
        position=end
    return clean(p),position,carry


def reflected(numerator,width):
    return {(width[0]-e[0],width[1]-e[1]):-c for e,c in numerator.items()}


def normalized(runs):
    q,length,_=numerator(runs)
    carries,unused,h=numerator(runs,True)
    digits=combine(q,{plus(e,(0,1)):c for e,c in carries.items()},scaled(carries,-10))
    return digits,plus(length,(0,h)),h


def expanded(runs,k):
    return tuple(value for value,coefficient,constant in runs
                 for _ in range(coefficient[0]*k+constant))


def reverse(n):
    out=0
    while n:out=10*out+n%10;n//=10
    return out


def seed(full):
    assert tuple(full)==tuple(full)[::-1] and 1<=full[0]<=18
    low=[max(0,q-9) for q in full[:len(full)//2]]
    if len(full)%2:
        assert full[len(full)//2]%2==0
        low.append(full[len(full)//2]//2)
    low.extend(min(9,q) for q in reversed(full[:len(full)//2]))
    return sum(d*10**i for i,d in enumerate(low))


def folded_full(n):
    ds=[int(x) for x in str(n)]
    return tuple(a+b for a,b in zip(ds,ds[::-1]))


def literal_word(name,r):
    if name=='A':p=(2,12,4,4)+(9,)*(r-5)+(14,16,16,15);c=None
    elif name=='B':p=(5,4)+(9,)*(r-2)+(14,14,12);c=None
    elif name=='C':p=(10,)+(9,)*r+(10,6);c=None
    else:p=(1,1)+(0,)*(r-1)+(1,7);c=12
    return p+(() if c is None else (c,))+p[::-1]


def replay_tail(record):
    assert (record['u'],record['v'],record['r_min'],record['first_positive_palindrome_time'])==(1,6,6,11)
    states=record['states'];ds=record['output_digit_words'];diffs=record['digit_reflection_differences']
    assert len(states)==12 and len(ds)==len(diffs)==11
    for index,(q,out,d,delta,overflow) in enumerate(zip(states,states[1:],ds,diffs,record['overflow_flags'])):
        Q,L,_=numerator(q)
        assert Q==reflected(Q,L)
        D,W,h=normalized(q)
        assert h==overflow and numerator(d)[:2]==(D,W)
        assert all(0<=v<=9 for v,_,_ in d) and d[-1][0]>0
        assert numerator(out)[:2]==(combine(D,reflected(D,W)),W)
        assert numerator(delta)[:2]==(combine(D,scaled(reflected(D,W),-1)),W)
        assert all(-9<=v<=9 for v,_,_ in delta)
        assert all(v==0 for v,_,_ in delta)==(index==10)
    return 11


def main():
    source=HERE/'inverse_ladder_certificate.json'
    cert=json.loads(source.read_text())
    tail_path=(HERE/cert['tail_certificate_path']).resolve()
    assert hashlib.sha256(tail_path.read_bytes()).hexdigest()==cert['tail_certificate_sha256']
    tails=json.loads(tail_path.read_text())
    tail=next(r for r in tails['certificates'] if (r['u'],r['v'])==(1,6))
    tail_count=replay_tail(tail)
    words=cert['full_pair_words']
    assert numerator(words['Q'])[:2]==numerator(tail['states'][0])[:2]
    transitions=[]
    for a,b in cert['transitions']:
        Q,L,_=numerator(words[a]);target,W,_=numerator(words[b])
        assert Q==reflected(Q,L) and target==reflected(target,W)
        D,width,h=normalized(words[a])
        assert width==W and target==combine(D,reflected(D,W))
        assert all(0<=v<=18 for v,_,_ in words[a]+words[b])
        transitions.append(dict(source=a,target=b,overflow=h))
    # Safety is proved by explicit present coefficients, independently of
    # tests of arbitrary digits or a particular realization.
    for name,q in cert['safety_pairs'].items():
        assert q>9 and q!=11 and any(v==q for v,_,_ in words[name])
        assert words[name][0][0]!=11
    controls=[];ordinary_steps=0
    for r in (5,6,7,8,11,37,128,1024):
        for name in ('A','B','C','Q'):
            full=literal_word(name,r)
            if r>=6:assert full==expanded(words[name],r-6)
            n=seed(full);start=n;expected=cert['first_positive_palindrome_times'][name]
            orbit=[]
            for h in range(1,expected+1):
                n+=reverse(n);ordinary_steps+=1
                assert (n==reverse(n))==(h==expected)
                if h==1 and name!='Q':
                    successor={'A':'B','B':'C','C':'Q'}[name]
                    assert folded_full(n)==literal_word(successor,r)
                orbit.append(str(n))
            controls.append(dict(r=r,family=name,seed=str(start),first_hit=expected,
                palindrome=str(n),orbit_sha256=hashlib.sha256('\n'.join(orbit).encode()).hexdigest()))
    result=dict(status='PASS',scope='all r>=5 exact inverse ladder and finite-excision obstruction',
        new_symbolic_transitions=len(transitions),replayed_tail_transitions=tail_count,
        transition_overflow_flags=transitions,ordinary_integer_cases=len(controls),
        ordinary_integer_steps=ordinary_steps,controls=controls,
        certificate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        dependency_sha256=cert['tail_certificate_sha256'],imports_generator=False,
        finite_excision_obstruction=True,positive_invariant_found=False)
    (HERE/'inverse_ladder_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='controls'},indent=2))


if __name__=='__main__':main()
