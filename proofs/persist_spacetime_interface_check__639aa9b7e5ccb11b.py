"""Independent fixed-cut carry-interface validation for the neutral exterior.

This verifies the local conditional rule against exact ordinary addition; it
does not assume that an arbitrary core supplies the required boundary carries.
"""
from persist_wake_neutral_center import P, CLOCK, candidate
from resume_front_collision import numeric_q_step
from itertools import product
import json

RIGHT=(0,1,0,0,1,1,0,0,1,1,1)
LEFT=tuple(1-c for c in RIGHT)

def add_row(q, incoming=0):
    digits=[]; carries=[]; c=incoming
    for x in q:
        z=x+c; digits.append(z%10); c=z//10; carries.append(c)
    return tuple(digits),tuple(carries)

def local_core_step(core,h,r):
    ds,cs=add_row(core,r)
    if cs[-1:] != (1-r,): return None
    if not h:return tuple(a+b for a,b in zip(ds,ds[::-1]))
    # The newly admitted boundary digit is 9*r on either side.
    return (ds[0]+9*r,)+tuple(ds[i]+ds[len(ds)-i] for i in range(1,len(ds)))+(ds[0]+9*r,)

def validate(maxpairs=2,m=8):
    checked=0; clock_matches=0; interface_matches=0; accepted=[]; first_mismatches={}
    for p in range(maxpairs+1):
        for half in product(range(19),repeat=p):
            for mid in [()]+[(c,) for c in range(0,19,2)]:
                core=half+mid+half[::-1]
                if not core:continue
                q=candidate(core,m);w=len(P)+m;good=True;phases=[]
                for t,h in enumerate(CLOCK):
                    ds,cs=add_row(q)
                    r,l=cs[w-1],cs[len(q)-w-1]
                    qn,hn=numeric_q_step(q)
                    assert tuple(a+b for a,b in zip(ds+(hn,) if hn else ds,(ds+(hn,) if hn else ds)[::-1]))==qn
                    current=q[w:-w]
                    if hn==h and (r,l)==(RIGHT[t],LEFT[t]):
                        local=local_core_step(current,h,r)
                        assert local==qn[w:-w],(core,t,local,qn[w:-w])
                        checked+=1
                    else:
                        good=False
                        first_mismatches.setdefault(t,core)
                        break
                    phases.append((hn,r,l));q=qn
                clock_matches+=len(phases)==11 and tuple(x[0] for x in phases)==CLOCK
                interface_matches+=good
                if good:accepted.append(core)
    return dict(local_equalities_checked=checked,clock_matches=clock_matches,
                all_interface_phases_match=interface_matches,examples=accepted[:5],
                first_mismatch_examples=first_mismatches,infinite_existence_proved=False)

if __name__=='__main__':
    out=validate();print(json.dumps(out,indent=2))
    open('persist_spacetime_interface_check_results.json','w').write(json.dumps(out,indent=2))
