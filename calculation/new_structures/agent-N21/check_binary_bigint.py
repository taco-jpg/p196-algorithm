#!/usr/bin/env python3
"""Independent ordinary-bigint replay for noncommutative AB and BA scattering."""
import sys
sys.set_int_max_str_digits(1000000)
from binary_scattering import background,insert_symbols,ANCHORS,K
from check_bigint import realize,from_integer
from packet_train import pair_step

def run():
    root=background();a,b=ANCHORS
    # Shared background, two singles per ordering, plus the two composites.
    specs=((),((a,'A'),),((b,'B'),),((a,'A'),(b,'B')),
              ((a,'B'),),((b,'A'),),((a,'B'),(b,'A')))
    words=[insert_symbols(root,s) for s in specs]
    nums=[realize(p) for p in words]
    first={'AB':None,'BA':None}
    for t in range(901):
        independent=[from_integer(N) for N in nums]
        assert independent==words,('full-pairword mismatch',t)
        assert all(str(N)!=str(N)[::-1] for N in nums),('palindrome',t)
        assert len({len(p) for p in independent})==1,('length disagreement',t)
        h=len(independent[0])//2
        for sy,i,j,k in (('AB',1,2,3),('BA',4,5,6)):
            bad=[z for z in range(h) if independent[i][z]+independent[j][z]-independent[0][z]!=independent[k][z]]
            if bad and first[sy] is None:first[sy]=(t,bad[0],len(bad))
        if t<900:
            nums=[N+int(str(N)[::-1]) for N in nums]
            words=[pair_step(p) for p in words]
    assert first['AB']==(840,661,2),first
    assert first['BA']==(801,650,3),first
    print('BINARY_BIGINT_PASS 7 canonical 5000-digit seeds, 900 steps, all pairwords/nonpalindromes, AB=840 BA=801')
if __name__=='__main__':run()
