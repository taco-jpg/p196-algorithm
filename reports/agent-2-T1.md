# Agent 2 / T1: a width-independent neutral-band digit-sum invariant

Status: PAPER PROOF + COMPUTED. Not LEAN-VERIFIED; no decimal Lychrel certificate. Related to coordination issue #289. The independently scoped exterior p16 result is PR #309.

## Statement and proof

Take any base b>=3 and set h=b-1. For a legal neutral-band edge, let B be the exterior coefficient list, C its symmetric center, e the B carry, e2=1-e the required complementary center carry, g the exterior overflow and u,v arbitrary permitted neutral-letter trims. Write SB=sum(B) and SC=sum(C), reduced modulo h.

For normalization with input carry a, output carry z, summing the positional equations d_i=W_i+c_i-b*c_(i+1) gives sum(digits)=sum(W)+a-z (mod h). In the exterior, this gives SB'=2SB+1-2e (mod h); in the center, SC'=2SC+4e-2 (mod h). The neutral letters appended at overflow and removed at trims have coefficient h, hence vanish modulo h.

Therefore H=SC+2SB obeys H'=2H (mod h) on each legal edge, regardless of B and C widths or the trim counts. For a closed cycle with P edges,

    (2^P - 1)*H = 0 (mod h).

In decimal base b=10, h=9, so odd P implies H=0 mod9; even P not divisible by six implies H=0 mod3; P divisible by six imposes no H restriction from this invariant alone.

For a prescribed B carry stream e[0..P-1], the center sum maps as

    SC[P] = 2^P SC[0] + Q (mod 9)
    Q = sum_t 2^(P-1-t)*(4e[t]-2).

A center cycle must solve (1-2^P)SC[0]=Q (mod 9). For documented period-11 stream e=10100110011, one and three repetitions require SC[0]=3 mod9; two repetitions allow 0,3,6. For the documented period-12 example e=101010010101, all center residues pass this arithmetic condition.

## Important negative limitation

This congruence cannot exclude a genuine B-cycle by its carry stream alone. For a closed B-cycle, write QB=sum_t 2^(P-1-t)*(1-2e[t]); exterior closure implies (1-2^P)SB[0]=QB. Since Q=-2QB, the choice SC[0]=-2SB[0] (mod9) always solves the center congruence. It guarantees only an algebraic residue, NOT an actual symmetric center list/cycle. Thus rejecting raw binary streams with this test is not a valid B-cycle obstruction.

## COMPUTED checks and exact commands

The standalone standard-library Python file calculation/agent-2/center_residue.py reimplements norm/one-step/neutral trimming and checks the two modular formulas on 105,000 seeded random cases, in bases 3,4,7,10,11,17,26; it also compares an exact nine-state DP with direct exhaustive enumeration of every binary carry stream at periods p=1..12.

    python3 calculation/agent-2/center_residue.py selftest
    python3 calculation/agent-2/center_residue.py check 10100110011 3
    python3 calculation/agent-2/center_residue.py census 11 12 16 18 20 22 24

The originally tested implementation yielded 51,883 admissible one-step examples among 105,000 random draws and all DP comparisons passed. For raw arbitrary streams (NOT B-cycle counts), p12 456/4096, p16 21846/65536, p18 29128/262144, p24 1864136/16777216 satisfy the residue-existence test.

No cycleOK base-10 certificate is supplied; no Lean module was modified and full repository python3 tools/verify.py --changed has NOT been run. **UNVERIFIED / DO NOT MERGE** pending review.
