"""Independent Python bigint orbit against carry-normalized pairwords, at EACH step."""
import sys,random
from independent import templ,canonical
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
def run(q,k,ui,C):
    p=templ(q,k,ui,C);n=canonical(p);over=[]
    for t in range(120):
        s=str(n);n1=n+int(s[::-1]);carry=0;d=[]
        for v in p:
            z=v+carry;d.append(z%10);carry=z//10
        if carry:d.append(carry)
        p=[a+b for a,b in zip(d,d[::-1])]
        compare=list(map(int,str(n1)[::-1]))
        actual=[a+b for a,b in zip(compare,compare[::-1])]
        assert p==actual,(q,k,ui,C,t)
        over.append(int(len(str(n1))>len(s)));n=n1
    assert over==[int(t%4==0) for t in range(120)]
    return "OK"
rng=random.Random(14004123)
for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
    for ui in range(3):
        for l in [7,8,9,10,11,12,13,14]:
            C=[rng.randrange(19) for _ in range(l//2)]
            C=C+([2*rng.randrange(10)] if l%2 else [])+C[::-1]
            assert run(q,k,ui,C)=="OK"
            print("STEPWISE_PASS",q,k,ui,l)
print("TOTAL 120 cases x 120 genuine decimal transitions = 14400 PASS")