"""Exact periodic bulk identities; these do not construct a finite Lychrel seed."""
from itertools import product
import json
from family_search_bulk_periods import bulk_step


def deterministic_step(word, overflow):
    assert any(x != 9 for x in word)
    result = bulk_step(tuple(word), overflow)
    assert len(result) == 1
    return next(iter(result))


def single_packet(q, gap):
    return (q,) + (9,) * gap + (18-q,) + (9,) * gap


def double_packet(q, gap):
    return (q, q) + (9,) * gap + (18-q, 18-q) + (9,) * gap


def no_overflow_single(q):
    return 2*q+2 if q < 9 else 2*q-20


def overflow_single(q):
    return q+10 if q < 9 else q-10


def phase_table():
    q = (3, 10, 15, 8)
    table = []
    for t in range(4):
        h = t % 2
        right_in = tuple(int(q[(i-1) % 4] >= 10) for i in range(4))
        left_in = tuple(int(q[(i+1) % 4] >= 10) for i in range(4))
        right_out = tuple((q[i]+right_in[i]) % 10 for i in range(4))
        left_raw = tuple((q[i]+left_in[i]) % 10 for i in range(4))
        left_out = tuple(left_raw[(i-h) % 4] for i in range(4))
        out = tuple(a+b for a,b in zip(left_out, right_out))
        assert out == deterministic_step(q,h)
        table.append(dict(phase=t,q=q,overflow=h,right_in=right_in,
                          left_in=left_in,next_left=left_out,
                          next_right=right_out,next_q=out))
        q=out
    assert q == (3,10,15,8)
    return table


def validate():
    cases=0
    for gap in range(1,101):
        for q in range(0,19,2):
            w=single_packet(q,gap)
            assert deterministic_step(w,0)==single_packet(no_overflow_single(q),gap)
            a=overflow_single(q)
            assert deterministic_step(w,1)==double_packet(a,gap-1)
            b=2*(a%10)+1
            assert deterministic_step(double_packet(a,gap-1),0)==double_packet(b,gap-1)
            cases+=3
    anti_cases=0
    for p in (1,2,3):
        for first in product(range(19),repeat=p):
            word=first+tuple(18-x for x in first)
            if all(x==9 for x in word):continue
            for h in (0,1):
                nxt=deterministic_step(word,h)
                assert all(nxt[i]+nxt[i+p]==18 for i in range(p))
                anti_cases+=1
    annihilations=0
    for n in range(1,13):
        for carry in product((0,1),repeat=n):
            neighbors=tuple(carry[(i-1)%n]+carry[(i+1)%n] for i in range(n))
            if max(neighbors)>1:continue
            word=tuple(6+10*carry[i]-5*neighbors[i] for i in range(n))
            middle=deterministic_step(word,0)
            assert middle==tuple(12-9*s for s in neighbors)
            assert deterministic_step(middle,1)==(6,)*n
            annihilations+=1
    return dict(packet_checks=cases,anti_complement_checks=anti_cases,
                annihilating_domain_checks=annihilations,
                phase_table=phase_table(),finite_seed_found=False)


if __name__=='__main__':
    result=validate()
    print(json.dumps(result,indent=2))
