#!/usr/bin/env python3
"""Exact algebraic reverse-add checker: affine repetitions are rational polynomials in X=base**q.
No numerical sampling is used for identity or all-q palindrome checks.
"""
from fractions import Fraction
from math import lcm
import json

BASE=10

def add(a,b):
    c=a.copy()
    for exp,x in b.items():
        c[exp]=c.get(exp,Fraction(0))+x
        if not c[exp]:del c[exp]
    return c

def scalar(a,s):
    return {k:v*s for k,v in a.items() if v*s}

def monomial(a,exponent,coeff):
    return {k+exponent:v*coeff for k,v in a.items() if v*coeff}

def word_value(word,base):
    value=0
    for ch in word:
        d=int(ch,36)
        if d>=base:raise ValueError('digit out of base')
        value=base*value+d
    return value

def pvalue(template,base=BASE):
    F={}
    for segment in template:
        if 'lit' in segment:
            w=segment['lit']
            F=add(monomial(F,0,base**len(w)),{0:Fraction(word_value(w,base))})
        else:
            w=segment['rep'];a=segment['a'];c=segment['c']
            assert a>=0 and w
            m=len(w)
            shift=Fraction(base)**(m*c)
            exponent=m*a
            pw=word_value(w,base)
            run=add({exponent:shift},{0:Fraction(-1)})
            F=add(monomial(F,exponent,shift),scalar(run,Fraction(pw,base**m-1)))
    return F

def reverse_template(template):
    return [{'lit':x['lit'][::-1]} if 'lit' in x
            else {'rep':x['rep'][::-1],'a':x['a'],'c':x['c']}
            for x in reversed(template)]

def eval_poly(poly,x):
    return sum((v*x**k for k,v in poly.items()),Fraction(0))

def root_check(poly,base,qmin):
    """Certify P(base**q)!=0 for ALL q>=qmin by integer-root constant divisibility."""
    if not poly:return False,{'failure':'identically zero'}
    denom=lcm(*(v.denominator for v in poly.values()))
    ints={k:int(v*denom) for k,v in poly.items()}
    lowest=min(ints)
    c=abs(ints[lowest]); assert c>0
    cap=0
    while base**(cap+1)<=c:cap+=1
    for q in range(qmin,cap+1):
        if eval_poly(poly,base**q)==0:
            return False,{'failure':'palindromic q','q':q}
    return True,{'tested_through':cap,'constant_factor':c,'lowest_power':lowest}

def materialize(template,q):
    return ''.join(x['lit'] if 'lit' in x
                   else x['rep']*(x['a']*q+x['c']) for x in template)

def validate_counts(template,qmin):
    for x in template:
        if 'rep' in x and x['a']*qmin+x['c']<0:raise ValueError('negative repeat count')
    v0=materialize(template,qmin)
    if not v0 or v0[0]=='0':raise ValueError('leading zero at qmin')
    # Cover an initially empty leading repetition that grows when q increases.
    for seg in template:
        if 'lit' in seg:
            if seg['lit']:
                if seg['lit'][0]=='0':raise ValueError('eventual leading zero')
                break
        else:
            if seg['a']>0 or seg['c']>0:
                if seg['rep'][0]=='0':raise ValueError('eventual leading zero')
                break

def check_finite_chain(templates,qmin,base=BASE):
    if not(0<=qmin and 2<=base<=36):raise ValueError('invalid base/qmin')
    for T in templates:validate_counts(T,qmin)
    identities=[]
    paltests=[]
    for T in templates:
        P=pvalue(T,base)
        diff=add(P,scalar(pvalue(reverse_template(T),base),-1))
        valid,why=root_check(diff,base,qmin)
        if not valid:raise ValueError(('palindrome obstruction',why))
        paltests.append(why)
    for T,U in zip(templates,templates[1:]):
        lhs=add(pvalue(T,base),pvalue(reverse_template(T),base))
        rhs=pvalue(U,base)
        if lhs!=rhs:raise ValueError(('bad identity',lhs,rhs))
        identities.append(True)
    # Extra ordinary-integer controls, NOT part of the universal proof.
    if base==10:
        for q in (qmin,qmin+1,qmin+2,qmin+9,1000):
            n=int(materialize(templates[0],q))
            for T in templates:
                assert n==int(materialize(T,q))
                assert str(n)!=str(n)[::-1]
                n+=int(str(n)[::-1])
    return {'base':base,'qmin':qmin,'verified_edges':len(identities),
            'nonpal_states':len(paltests),'all_q_symbolic':True,
            'nonpal_root_checks':paltests}

def shift_q(template,gain):
    return [dict(x) if 'lit' in x
            else {'rep':x['rep'],'a':x['a'],'c':x['c']+x['a']*gain} for x in template]

def check_cycle(states,qmin,gain,base=BASE):
    """Exact cycle test: if accepted, all q>=qmin give infinite Lychrel orbits."""
    if gain<0:raise ValueError('gap gain must not be negative')
    details=check_finite_chain(states,qmin,base)
    terminal=shift_q(states[0],gain)
    last=states[-1]
    if add(pvalue(last,base),pvalue(reverse_template(last),base))!=pvalue(terminal,base):
        raise ValueError('nonclosing algebraic cycle')
    return dict(details,terminal_gain=gain,cycle_verified=True)

def control():
    L=lambda s:{'lit':s}
    R=lambda w,c:{'rep':w,'a':1,'c':c}
    templates=[
        [L('12'),R('9',0),L('34')],
        [L('569'),R('9',-2),L('855')],
        [L('1128'),R('9',-2),L('820')],
        [L('1418'),R('9',-3),L('8031')],
        [L('2727'),R('9',-3),L('6172')],
        [L('5444'),R('9',-3),L('3444')],
    ]
    result=check_finite_chain(templates,3)
    broken=json.loads(json.dumps(templates));broken[2][2]['lit']='821'
    try:check_finite_chain(broken,3)
    except ValueError:pass
    else:raise AssertionError('corruption undetected')
    try:check_cycle(templates,3,1)
    except ValueError as err:assert 'nonclosing' in str(err)
    else:raise AssertionError('false infinite certificate accepted')
    return result

if __name__=='__main__':
    print(json.dumps(control(),indent=2))
