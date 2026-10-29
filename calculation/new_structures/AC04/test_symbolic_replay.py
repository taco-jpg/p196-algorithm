"""Independent Python bigint checks for prefixes rejected by all-length symbolic pumping."""
import random,sys
from symbolic_all_lengths import scan
from independent import templ,canonical
from centre_scan_data import U
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
rng=random.Random(4042026)
h=34+9*14+1+3*100
cut=h+15
nchecks=0
for ui in range(3):
    candidates=[(a,b,fail[0]) for a in range(19) for b in range(19)
                if (z:=scan(ui,a,b))[0] and (fail:=z[1])]
    assert len(candidates)==[228,25,82][ui]
    for t in range(20):
        a,b,delta=candidates[(t*37+rng.randrange(10000))%len(candidates)]
        length=7+t*2+(t%2)
        half=(length+1)//2
        cs=[a,b]+[rng.randrange(19) for _ in range(half-2)]
        if length%2:cs[-1]=2*rng.randrange(10)
        C=cs+cs[-2::-1] if length%2 else cs+cs[::-1]
        P=templ(14,100,ui,C)
        N=canonical(P)
        for k in range(120):
            N=N+int(str(N)[::-1])
        d=list(map(int,str(N)[::-1]))
        got=[x+y for x,y in zip(d,d[::-1])]
        i=cut+delta
        want=U[ui][(i-(h-300))%3]
        assert got[i]!=want,(ui,t,a,b,delta)
        nchecks+=1
print('physical decimal rejected-prefix replay PASS',nchecks,
      'cases, 120 steps each')