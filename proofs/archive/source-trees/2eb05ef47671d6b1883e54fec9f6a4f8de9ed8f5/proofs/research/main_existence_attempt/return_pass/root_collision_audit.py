"""Independent arithmetic check of the proposed motif identities."""
from pathlib import Path
import importlib.util, json, random
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("candidate",here/"collision/motif_collision.py")
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
rng=random.Random(10937)
def motif():
    half=[rng.randrange(19) for _ in range(rng.randrange(1,17))]
    half[0]=rng.randrange(1,19)
    center=[2*rng.randrange(10)] if rng.randrange(2) else []
    return tuple(half+center+half[::-1])
def integer(q):
    mid=len(q)//2
    high=[min(9,x) for x in q[:mid]]
    low=[x-min(9,x) for x in q[:mid]][::-1]
    return int(''.join(map(str,high+([q[mid]//2] if len(q)%2 else [])+low)))
def profile(n):
    s=str(n)
    return tuple(int(x)+int(y) for x,y in zip(s,s[::-1]))
for i in range(10000):
    a,b=motif(),motif(); gap=rng.randrange(1,12)
    aa,bb,delta,h,pa,pb=c.companion(a,b)
    q=a+(0,)*gap+b+(0,)*gap+a
    n=integer(q); assert profile(n)==q
    out=n+int(str(n)[::-1])
    assert profile(out)==aa+(0,)*(gap-delta)+bb+(0,)*(gap-delta)+aa
    assert (str(out)==str(out)[::-1])==(pa and pb)
    assert len(str(out))-len(str(n))==h
    q=a+b+a; n=integer(q); out=n+int(str(n)[::-1])
    predicted, h, pal=c.collision_step(a,b)
    assert profile(out)==predicted
    assert pal==(str(out)==str(out)[::-1])
    assert len(str(out))-len(str(n))==h
report=dict(status="PASS", separated_cases=10000, zero_gap_cases=10000,
            source_of_expected_values="ordinary integer reversal/addition; no candidate normalizer",
            all_time_avoidance_proved=False)
(here/"root_collision_audit.json").write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
