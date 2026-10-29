#!/usr/bin/env python3
"""Independent ordinary-integer checks of Markov tile mosaics."""
import sys,random,json
from sft import B0,W,cycles
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
def numeral_from_folded(half):
    lo=[min(9,p) for p in half]
    hi=[p-a for p,a in zip(half,lo)]
    assert hi[0]>0
    return int(''.join(map(str,hi+lo[::-1])))
def integer_pairs(n):
    d=[int(x) for x in str(n)]
    return [d[-1-i]+d[i] for i in range(len(d))]
def run():
    opts=[ps for ps,st in cycles(W[1],1) if st[0]==(1,1,4)]
    assert len(opts)==12800
    assert len({ps for ps in opts})==12800
    assert all(any(x%2 for x in ps) for ps in opts)
    rng=random.Random(20261028);total=0
    for trial in range(40):
        blocks=10+(trial%8)*4
        tiles=[rng.choice(opts) for _ in range(blocks)]
        half=B0+[x for tile in tiles for x in tile]
        N=numeral_from_folded(half)
        R=N+int(str(N)[::-1])
        assert len(str(R))==len(str(N))+1
        P=integer_pairs(R)
        first=len(B0)+20;last=len(half)-20
        assert all(P[i]==W[1][(i-len(B0))%20] for i in range(first,last))
        total+=last-first
    tiles=[rng.choice(opts) for _ in range(30)]
    half=B0+[x for tile in tiles for x in tile]
    N=numeral_from_folded(half)
    for t in range(300):
        s=str(N)
        assert s!=s[::-1],t
        N+=int(s[::-1])
    print(json.dumps({"random_seed":20261028,"mosaics":40,"checked_interior_sites":total,"independent_bigint_steps":300,"fixed_port_choices":12800},indent=2))
if __name__=="__main__":run()
