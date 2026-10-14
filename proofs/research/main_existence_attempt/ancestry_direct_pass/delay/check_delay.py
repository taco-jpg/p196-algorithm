"""Exact finite-delay ancestry witnesses; no unbounded-delay assertion.

The published 289-step seed is independently recomputed by ordinary integer
reversal and by schoolbook column addition. No existing project checker is
imported. First-hit indexing is least POSITIVE iterate, allowing a palindromic
initial seed in the general definition. The checked seed itself is nonpalindromic.
"""
from pathlib import Path
import json
import sys

sys.set_int_max_str_digits(100000)

SEED = 13968441660506503386020
SOURCES = [
    "https://jasondoucette.com/pal/13968441660506503386020",
    "https://oeis.org/A340397",
    "https://habr.com/ru/articles/536104/",
    "https://jasondoucette.com/worldrecords.html",
]


def pal(n):
    s = str(n)
    return s == s[::-1]


def ra(n):
    return n + int(str(n)[::-1])


def digits(n):
    return tuple(map(int, str(n)[::-1]))


def pair_sums(n):
    d = digits(n)
    return tuple(x+y for x,y in zip(d,d[::-1]))


def columns(q):
    c = 0
    d = []
    for x in q:
        v = x+c
        d.append(v % 10)
        c = v//10
    if c:
        d.append(c)
    return int(''.join(map(str,d[::-1])))


def bad(q):
    return (all(x <= 9 for x in q)
            or (q[0] == 11 and all(x in (0,11) for x in q)))


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d = [0]*len(q)
    for i in range(len(q)//2):
        d[i] = max(0,q[i]-9)
        d[-1-i] = min(9,q[i])
    if len(q)%2:
        assert q[len(q)//2]%2 == 0
        d[len(q)//2] = q[len(q)//2]//2
    return int(''.join(map(str,d[::-1])))


def center_18_length(q):
    j = len(q)//2
    if q[j] != 18:
        return 0
    lo = hi = j
    while lo and q[lo-1] == 18:
        lo -= 1
    while hi+1 < len(q) and q[hi+1] == 18:
        hi += 1
    return hi-lo+1


def long_safe_controls():
    transitions = 0
    controls = list(range(33)) + [64,128,289]
    for r in controls:
        m = 2*r+1
        n = int('9'*(m+2)+'00')
        assert not pal(n)
        for t in range(r+1):
            q = pair_sums(n)
            assert center_18_length(q) >= m-2*t > 0
            assert not bad(q)
            out = ra(n)
            assert out == columns(q) and not pal(out)
            n = out
            transitions += 1
    return {"r_controls":controls,"literal_transitions":transitions}


def main():
    values = [SEED]
    assert not pal(SEED)
    while True:
        n = values[-1]
        q = pair_sums(n)
        out = ra(n)
        assert out == columns(q)
        assert bad(q) == pal(out)
        values.append(out)
        if pal(out):
            break
        assert len(values) < 400
    delay = len(values)-1
    assert delay == 289
    assert all(not pal(n) for n in values[:-1])
    qs = [pair_sums(n) for n in values]
    canonical_seed = realize(qs[0])
    assert not pal(canonical_seed)
    assert ra(canonical_seed) == values[1]
    # b=q_288 has r safe generating ancestors for each 0<=r<=288.
    assert bad(qs[288])
    s_b_witnesses = []
    for r in range(289):
        start = 288-r
        assert all(not bad(qs[j]) for j in range(start,288))
        s_b_witnesses.append({"r":r,"start_orbit_index":start})
    # a=q_287 lies in K_r, but G(a)=b does not, for 0<=r<=287.
    assert not bad(qs[287]) and bad(qs[288])
    k_failures = []
    for r in range(288):
        start = 287-r
        assert all(not bad(qs[j]) for j in range(start,288))
        k_failures.append({"r":r,"start_orbit_index":start})
    base = Path(__file__).parent
    trajectory = {"seed":str(SEED),"first_positive_hit":delay,
                  "ordinary_integers":[str(n) for n in values]}
    (base/'delay_289_trajectory.json').write_text(json.dumps(trajectory,indent=2)+'\n')
    result = {
        "status":"finite-depth obstruction plus exact delay equivalences; unbounded delays unproved",
        "seed":str(SEED),"canonical_realization_same_q":str(canonical_seed),
        "initial_seed_palindrome":False,"canonical_seed_palindrome":False,
        "first_positive_palindrome_step":delay,
        "final_palindrome_digits":len(str(values[-1])),
        "predecessor_ordinary_integer":str(values[288]),
        "predecessor_q":list(qs[288]),
        "predecessor_B_branch":"all coefficients <=9" if max(qs[288]) <= 9 else "0/11",
        "K_nonclosure_input_integer":str(values[287]),
        "K_nonclosure_input_q":list(qs[287]),
        "S_r_intersects_B_for_every_r_inclusive":[0,288],
        "K_r_not_forward_closed_for_every_r_inclusive":[0,287],
        "S_r_B_ancestry_starts":s_b_witnesses,
        "K_r_nonclosure_ancestry_starts":k_failures,
        "long_safe_reservoir_controls":long_safe_controls(),
        "primary_source_urls":SOURCES,
        "unbounded_finite_first_hit_times_proved":False,
        "all_finite_ancestry_depths_obstructed":False,
        "finite_Lychrel_witness":False,
    }
    (base/'check_delay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ('predecessor_ordinary_integer','predecessor_q',
                                   'K_nonclosure_input_integer','K_nonclosure_input_q',
                                   'S_r_B_ancestry_starts','K_r_nonclosure_ancestry_starts')},indent=2))


if __name__ == '__main__':
    main()
