#!/usr/bin/env python3
"""All-width necessary Beatty winding-charge condition, NOT a Lychrel certificate.
Paper proof: reports/AgentY15BeattyWindingCharge.md
"""
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

@dataclass(frozen=True)
class Term:
    coefficient: int
    outer_slope: int
    inner_slope: int
    theta_num: int = 0
    theta_den: int = 1

def charge(terms):
    return sum(t.coefficient*(t.outer_slope-t.inner_slope) for t in terms)

def exact_circle_cells(terms):
    """Necessary constant-mod9 H cell test, exact for rational phases.
    Passing is NOT sufficient for a real RAA cycle."""
    cuts={Fraction(0), Fraction(1)}
    for t in terms:
        theta=Fraction(t.theta_num,t.theta_den)
        for a in (t.outer_slope,t.inner_slope):
            if not a: continue
            low=min(theta, theta+9*a)
            high=max(theta, theta+9*a)
            for k in range(low.numerator//low.denominator,
                           high.numerator//high.denominator+2):
                x=(Fraction(k)-theta)/(9*a)
                if 0<x<1: cuts.add(x)
    xs=sorted(cuts)
    def H(x):
        return sum(t.coefficient*(
            (9*t.outer_slope*x+Fraction(t.theta_num,t.theta_den)).__floor__()
            -(9*t.inner_slope*x+Fraction(t.theta_num,t.theta_den)).__floor__()
        ) for t in terms)
    residues={H((lo+hi)/2)%9 for lo,hi in zip(xs,xs[1:])}
    return sorted(residues),len(xs)-1

def floor_golden(k):
    """Exact floor(k*(sqrt(5)-1)/2), for positive OR negative k."""
    m=isqrt(5*k*k)
    if k<0: m=-m-1
    return (m-k)//2

def schoolbook_step(d):
    c=0; out=[]
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c
        out.append(z%10)
        c=z//10
    if c: out.append(c)
    return out

def run_tests():
    for v in range(-8,9):
        term=Term(1,v+1,v)
        assert charge([term])==1
        residues,cells=exact_circle_cells([term])
        assert len(residues)>1 and cells>=9
        for q in range(2,85):
            s=[floor_golden(v*q+i+1)-floor_golden(v*q+i)
               for i in range(q)]
            assert set(s)<= {0,1}
            d=[2]+[8+x for x in s]+[8]
            sigma=10+8*q+floor_golden((v+1)*q)-floor_golden(v*q)
            assert sum(d)==sigma
            # Independent full arbitrary-precision decimal arithmetic.
            n=int(''.join(map(str,reversed(d))))
            actual=n+int(str(n)[::-1])
            digit_result=schoolbook_step(d)
            assert actual==int(''.join(map(str,reversed(digit_result))))
            assert sum(digit_result)%9==(2*sum(d))%9

    balanced=[Term(1,1,0),Term(-1,1,0)]
    assert charge(balanced)==0
    assert len(exact_circle_cells(balanced)[0])==1
    # Charge zero does NOT imply the exact cut-constancy gate.
    misaligned=[Term(1,1,0),Term(-1,1,0,1,7)]
    assert charge(misaligned)==0
    assert len(exact_circle_cells(misaligned)[0])>1
    print("PASS exact mod-9 circle cells and independent ordinary-integer controls")
    print("Single Beatty source: charge 1, NO all-width positive-gain return")
    print("Balanced multi-sheet carry closure remains UNDECIDED")

if __name__=="__main__":
    run_tests()
