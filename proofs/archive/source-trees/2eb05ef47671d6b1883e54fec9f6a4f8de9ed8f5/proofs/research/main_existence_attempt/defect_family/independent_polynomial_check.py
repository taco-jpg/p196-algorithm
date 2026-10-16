"""Independent all-parameter replay using finite polynomial identities.

This checker does not call the run normalizer, run merger, or residue-folding
code.  It checks the exact q/carry polynomial update and reduction modulo
x^D-1.  Each exponent is an affine integer expression in m.  A zero formal
coefficient dictionary proves equality for every permitted m, including
any exceptional exponent coincidences.
"""
from pathlib import Path
from collections import defaultdict
import json

M=256


def poly(runs):
    # Represent (x-1) * sum q_i x^i by its affine-exponent monomials.
    out=defaultdict(int);a=b=0
    for value,slope,offset in runs:
        assert slope>=0 and slope*M+offset>=1
        out[(a,b)]-=value
        a+=slope;b+=offset
        out[(a,b)]+=value
    return {e:v for e,v in out.items() if v}


def combine(*parts):
    out=defaultdict(int)
    for p,scale,shift in parts:
        for (a,b),v in p.items():out[(a,b+shift)]+=scale*v
    return {e:v for e,v in out.items() if v}


def carry(runs):
    c=0;out=[]
    for value,a,b in runs:
        if value!=9:c=int(value>=10)
        out.append((c,a,b))
    return out,c


def valid(runs):
    assert runs==list(reversed(runs))
    assert runs[0][0]>0 and all(0<=x<=18 for x,a,b in runs)
    assert all(a>=0 and a*M+b>=1 for x,a,b in runs)
    length_a=sum(a for x,a,b in runs);length_b=sum(b for x,a,b in runs)
    assert length_a%2==0
    if length_b%2:assert runs[len(runs)//2][0]%2==0


def check_step(q,r):
    valid(q);valid(r)
    c,h=carry(q)
    Q=poly(q);C=poly(c);Cr=poly(list(reversed(c)))
    if h==0:
        expected=combine((Q,2,0),(C,1,1),(C,-10,0),(Cr,1,-1),(Cr,-10,0))
    else:
        expected=combine((Q,1,0),(Q,1,1),(C,1,1),(C,-10,0),(Cr,1,0),(Cr,-10,1))
    assert expected==poly(r)
    assert sum(a for x,a,b in r)==sum(a for x,a,b in q)
    assert sum(b for x,a,b in r)==sum(b for x,a,b in q)+h


def reduced(p,c):
    out=defaultdict(int)
    D0=6*M+c
    assert D0>0
    for (a,b),v in p.items():
        k=(a*M+b)//D0
        aa=a-6*k;bb=b-c*k
        # 0 <= aa*m+bb < 6m+c, for every m>=M.
        assert aa>=0 and aa*M+bb>=0
        assert 6-aa>=0 and (6-aa)*M+c-bb>=1
        out[(aa,bb)]+=v
    return {e:v for e,v in out.items() if v}


def check_budget(q,B,c):
    assert sum(a for x,a,b in B)==6 and sum(b for x,a,b in B)==c
    assert all(x>=0 for x,a,b in B)
    assert reduced(poly(q),c)==reduced(poly(B),c)
    # Reduction of (x-1)P leaves a possible repunit kernel; equal total
    # coefficient sums eliminate that kernel exactly.
    assert sum(x*a for x,a,b in q)==sum(x*a for x,a,b in B)
    assert sum(x*b for x,a,b in q)==sum(x*b for x,a,b in B)


def run():
    directory=Path(__file__).parent
    source=json.loads((directory/"symbolic_defects.json").read_text())
    opt=json.loads((directory/"optimal_defect_charge.json").read_text())
    rows=source["rows"]
    for a,b in zip(rows,rows[1:]):check_step(a["q"],b["q"])
    checked=0
    for row,orec in zip(rows,opt["rows"]):
        check_budget(row["q"],row["budgets"],row["D_offset"])
        assert orec["radius"]==orec["initial_upper_bound"]//18
        radius=orec["radius"];center=row["D_offset"]
        assert [a["c"] for a in orec["trials"]]==list(range(center-radius,center+radius+1))
        for trial in orec["trials"]:
            check_budget(row["q"],trial["budgets"],trial["c"])
            assert all(x==18 or a==0 for x,a,b in trial["budgets"])
            charge=sum(abs(x-18)*b for x,a,b in trial["budgets"] if x!=18)
            assert charge==trial["charge"]
            checked+=1
        assert orec["minimum_charge"]==min(a["charge"] for a in orec["trials"])
        assert orec["minimum_charge"]<=orec["initial_upper_bound"]
    result={"all_parameter_domain":"every integer m>=256",
            "exact_symbolic_steps_checked":len(rows)-1,
            "exact_budget_families_checked":checked+len(rows),
            "finite_orbit_samples_used_for_proof":0}
    (directory/"independent_polynomial_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":run()
