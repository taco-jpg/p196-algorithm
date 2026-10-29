#!/usr/bin/env python3
"""X16: bounded-scope nine-step neutral-port guard; no infinite claim."""
import random,json,time,sys
sys.set_int_max_str_digits(0)
from carry_ribbon import tm,seed,pairs,norm,direct
PATTERNS={'101100','001101'}
def run(k):
    d=seed(17,14,k);g=[]
    big=k in (0,1,2,7,21,25,63,127,255)
    for t in range(9):
        p=pairs(d);nxt,_=norm(p)
        assert nxt==direct(d)
        if big:
            val=int(''.join(map(str,reversed(d))))
            assert val+int(str(val)[::-1])==int(''.join(map(str,reversed(nxt))))
        g.append(len(nxt)-len(d));d=nxt
    p9=pairs(d);n=len(p9)
    assert ''.join(map(str,g))=='101010101'
    got={i for i,v in enumerate(p9) if v==9}
    if k<2:return {'k':k,'ports':sorted(got),'special':True}
    bits=''.join(str(tm(k+j)) for j in range(-2,4))
    want={2,n-3}
    if bits in PATTERNS:want.update({k+5,k+7})
    assert got==want,(k,bits,got,want)
    return {'k':k,'center_exception':bits in PATTERNS,'window':bits,'ports':len(got)}
def main():
    start=time.time();samples=[];extra=0
    for k in range(3001):
        v=run(k)
        extra+=bool(v.get('center_exception'))
        if k in (0,1,2,7,21,25,63,127,255,511,1023,2047):
            samples.append(v)
    rng=random.Random(160016)
    others=[rng.randrange(3001,20001) for _ in range(40)]
    for k in others:run(k)
    data={'tested_all_k':[0,3000],'random_seed':160016,
          'random_large_range':[3001,20000],'random_large_count':len(others),
          'extra_centre_pairs_k2_to_3000':extra,'exception_patterns':sorted(PATTERNS),
          'mismatches':0,'snapshots':samples,'elapsed_seconds':round(time.time()-start,2)}
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
