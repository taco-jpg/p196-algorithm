"""Exact two-step delayed repair of the V_m balanced-wall family.

Affine run lengths mean every k >= 0, with m=k+4.  Cases m=2,3 are
separate exact calculations.  The result is a finite-stage identity,
not a recurrent scale-changing construction or a decimal Lychrel proof.
"""
from pathlib import Path
import sys, json

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/"continuation"), str(ROOT/"research")]
from wall_renewal_check import (
    Len, ONE, canon, normal, add_runs, symbolic_wall_step, symbol_list,
    expand, V, wall_step, difference_word, realize, integer_step, pair_sums,
)


def actual_step(q):
    d,h = normal(q,0)
    if h:
        d = canon(d+[(1,ONE)])
    return add_runs(d,list(reversed(d))),h


def signed_difference(w,c):
    return add_runs(canon(w+[(18,c)]),
                    canon([(0,c)]+[(-x,n) for x,n in w]))


def safe(q):
    # All listed runs have positive minimum at the phase being checked.
    present = [x for x,n in q if n.b>0]
    return max(present)>=10 and (present[0]!=11 or any(x not in (0,11) for x in present))


def small_case(m):
    c=6*m+3
    w=V(m)
    q=w+w[::-1]
    n=realize(q)
    events=[]
    for t in range(1,12):
        n=integer_step(n)
        q=pair_sums(n)
        w,h,_=wall_step(w)
        ghost=difference_word(w,c)
        assert str(n)!=str(n)[::-1]
        if t==9:
            diff=tuple(a-b for a,b in zip(q,ghost))
            assert diff==(0,)*c+(-1,20,-1)+(0,)*c
            assert q[c:c+3]==(3,14,3)
        if t==10:
            assert q==ghost
            assert all(sum(q[j::c])==18 for j in range(c))
            assert q[c:c+3]==(7,8,7)
            events.append({"step":t,"C":c,"wall":w})
        if t==11:
            assert len(q)==2*c+3 and sum(q)==18*(c+3)
            assert q[c+1]==16
    return {"m":m,"events":events}


def run():
    # m=k+4, every k>=0.
    c=Len(6,27)
    w=[(1,ONE),(9,Len(2,7)),(8,ONE),(2,ONE),(9,Len(2,7)),
       (16,ONE),(10,ONE),(9,Len(2,7)),(17,ONE)]
    q=canon(w+list(reversed(w)))
    phases=[]
    for t in range(1,12):
        assert safe(q)
        q,h=actual_step(q)
        w,wh=symbolic_wall_step(w)
        assert h==wh
        ghost=signed_difference(w,c)
        if t==9:
            diff=add_runs(q,[(-x,n) for x,n in ghost])
            assert diff==canon([(0,c),(-1,ONE),(20,ONE),(-1,ONE),(0,c)])
        if t==10:
            assert q==ghost
            expected=canon([(x,ONE) for x in (5,5,6,3,16,17)]
              +[(18,Len(2,1))]+[(x,ONE) for x in (17,16,15,6,1,12)]
              +[(9,Len(2,4))]+[(x,ONE) for x in (6,17,12,3,2,1)]
              +[(0,Len(2,1))]+[(x,ONE) for x in (1,2,15,12,13,13)])
            assert w==expected
            assert sum(x*n.a for x,n in q)==108
            assert sum(x*n.b for x,n in q)==18*27
        if t==11:
            assert sum(n.a for _,n in q)==12
            assert sum(n.b for _,n in q)==57
            assert sum(x*n.a for x,n in q)==108
            assert sum(x*n.b for x,n in q)==18*30
            center=Len(6,28)
            prefix=Len(0,0)
            certified_center=[]
            for x,n in q:
                if (center-prefix).nonnegative() and (prefix+n-center-ONE).nonnegative():
                    certified_center.append(x)
                prefix=prefix+n
            assert certified_center==[16]
        phases.append({"step":t,"wall":symbol_list(w),"q":symbol_list(q),"overflow":h})
    controls=[small_case(m) for m in list(range(2,65))+[96,128,192,256]]
    doc={"status":"exact finite-stage family identity; no all-time closure",
         "symbolic_parameter":"m=k+4, all k>=0",
         "small_cases_covering_missing_parameters":[2,3],
         "phases":phases,"ordinary_integer_controls":controls}
    Path(__file__).with_name("delayed_repair_identity.json").write_text(json.dumps(doc,indent=2)+"\n")
    print(json.dumps({"symbolic_m":"all m>=4", "separate_small_m":[2,3],
                      "integer_control_parameters":len(controls),
                      "integer_control_steps":11*len(controls)}))


if __name__ == "__main__":
    run()
