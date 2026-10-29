#!/usr/bin/env python3
"""Independent true-integer oracle for the W20 centre-gate classes.

Run from repository root:
    python3 calculation/new_structures/agent-W20/ordinary_integer_oracle.py \
        calculation/new_structures/agent-N18/lattice.txt
"""
import sys
sys.set_int_max_str_digits(0)

def check(fixture):
    rows = [list(map(int, line.split())) for line in open(fixture, encoding='utf-8')]
    assert len(rows) == 47 and all(len(r) == 8 for r in rows[:39])
    assert all(len(r) == 20 for r in rows[39:])
    B = [r[0] for r in rows[:39]]
    W = rows[39]
    reps = ((0, 0, 0, 20), (4, 0, 3, 8), (8, 1, 8, 13))
    for x, y, z, target in reps:
        U = [1]*43
        U[13],U[20],U[30]=7,7,6
        U[40:43]=[x,y,z]
        C = [8,0,0]+U+[16]+U[::-1]+[0,0,8]
        reference=None
        for q in range(1,5):
            A=B+W*q
            P=A+C+A[::-1]
            assert P==P[::-1] and P[len(P)//2]%2==0
            # Construct the entire ordinary decimal integer directly, not via a pairword step.
            d=[0]*len(P)
            for i in range(len(P)//2):
                d[i]=min(P[i],9)
                d[-1-i]=P[i]-d[i]
            d[len(P)//2]=P[len(P)//2]//2
            N=int(''.join(map(str,d[::-1])))
            steps=352 if target==20 else 264
            checkpoints={}
            for t in range(steps+1):
                s=str(N)
                assert s!=s[::-1],(x,y,z,q,t,'palindrome')
                digits=[int(c) for c in s[::-1]]
                actual=[digits[i]+digits[-1-i] for i in range(len(digits))]
                assert actual[:39]==[r[t%8] for r in rows[:39]],(x,y,z,q,t,'root')
                if t in (88,176,264,352):
                    # Strip exactly q-1 exterior lattice blocks. The remainder is the
                    # centre-facing boundary, including whichever lattice block survived.
                    cut=39+20*(q-1)
                    inner=actual[cut:-cut]
                    m=0
                    while m<20 and inner[m]==W[m]:m+=1
                    checkpoints[t]=(m,inner)
                if t<steps:
                    N+=int(s[::-1])
            assert (checkpoints[88][0],checkpoints[176][0],checkpoints[264][0]) == (20,20,target)
            if target==20:assert checkpoints[352][0]==2
            if reference is None:
                reference={t:inner for t,(m,inner) in checkpoints.items()}
            else:
                assert all(reference[t]==inner for t,(m,inner) in checkpoints.items()),(x,y,z,q,'q-dependent centre')
            print(f'ORACLE_PASS gate={target} suffix={x},{y},{z} q={q} steps={steps} last_digits={len(str(N))} checkpoints={[(t,m) for t,(m,_) in checkpoints.items()]}')
    print('ORACLE_PASS all 12 ordinary-integer orbits with q-independent macro cores')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: ordinary_integer_oracle.py lattice.txt')
    check(sys.argv[1])
