# Agent W20: a quantized decimal centre collision delay clock
**COMPUTED**, not a base-10 Lychrel proof or a general all-q theorem. This extends the independently committed `AgentW20ProgrammableRenewalGate` result from macro-return signatures to exact *first exterior failure times* and tests a clocked insertion law at large q.

## Construction
Reuse its exact seed with 39-column rooted phase-8 exterior B and time-zero spatial period-20 W from `calculation/new_structures/agent-N18/lattice.txt`:
`P(q;x,y,z)=B ++ W^q ++ C(x,y,z) ++ reverse(W^q) ++ reverse(B)`.
The 93-coefficient palindromic centre `C=[8,0,0] ++ U ++ [16] ++ reverse(U) ++ [0,0,8]`, with U length 43, U[13]=7, U[20]=7, U[30]=6, and free U[40:43]=(x,y,z), has real positive-decimal seed digits as in the first W20 result. The first exterior mismatch time is the earliest integer t>=0 for which any of the first 39 pair coefficients differs from the N18 8-phase rooted target (not the first palindrome).

## Exhaustive positive programmable delay
`clock_lifetimes.cpp` enumerates all 6,859 values of (x,y,z) in 0..18 at q=1. The exhaustive table contains exactly three first-mismatch times:

| first mismatch t | count | witness (x,y,z) | previous t=264 gate prefix |
| --- | ---: | --- | ---: |
| 300 | 64 | (4,0,3) | 8/20 |
| 324 | 603 | (8,1,8) | 13/20 |
| 364 | 6,192 | (0,0,0) | 20/20 |

The three codewords produce a 64-step or 24-step or zero delay deficit, which is temporally quantized in 8-phase units. No claim is made that any particular class is unique under larger centre alphabets.

## Tested insertion clock (not an inductive proof)
For each representative above, the program tests all q=1,2,...,16 and q=32,64,128,240. There are exactly 20 q values per class. For every q tested, the observed first mismatch is `88q+212`, `88q+236`, or `88q+276`, respectively. Thus the measured delay from adding one full period-20 exterior copy is 88 steps. This is a finite, explicitly enumerated list of q, *not* a universal pump lemma; the previously known long-horizon W10/N02 insertion phenomena are compatible but are not cited as proving this one.

## Independent ordinary-integer verification at q=240
`clock_gmp.cpp` starts from the exact decimal digit integer constructed independently of coefficient stepping, and executes `mpz_class N += mpz_class(reverse(decimal(N)))` until the first root failure. It compares all 39 coefficients at every t and checks that every integer through and including the failure state is nonpalindromic. For (4,0,3): t=21332, mismatch at j=38, digit length=20437, ASCII-decimal FNV64=6665814142250305921. For (8,1,8): t=21356, j=38, length=20449, FNV64=9107711604172587816. For (0,0,0): t=21396, j=38, length=20469, FNV64=17591857383264762646. These are genuine conventional integers, not merely formal pairwords. The earlier first W20 commit independently replayed (0,0,0) to 20,000 and compared all pairword states with ordinary digit addition.

## Reproduction from repository root
```
g++ -std=c++17 -O3 -Wall -Wextra -Werror calculation/new_structures/agent-W20/clock_lifetimes.cpp -o /tmp/w20_clock
/tmp/w20_clock calculation/new_structures/agent-N18/lattice.txt
g++ -std=c++17 -O3 -Wall -Wextra -Werror calculation/new_structures/agent-W20/clock_gmp.cpp -lgmpxx -lgmp -o /tmp/w20_clock_gmp
/tmp/w20_clock_gmp calculation/new_structures/agent-N18/lattice.txt 240 4 0 3 21332
/tmp/w20_clock_gmp calculation/new_structures/agent-N18/lattice.txt 240 8 1 8 21356
/tmp/w20_clock_gmp calculation/new_structures/agent-N18/lattice.txt 240 0 0 0 21396
```

## Next constructive target
The gate output timing is highly rigid in this family. A finite certificate would require a **clocked reinsertion interface** that takes the 8/13/20 truncated W signatures after a collision and restores a full 20-site return, possibly by coupling two separated gates or allowing a time-dependent reflection-axis shift. The present tested delay line does not close and cannot certify infinite nonpalindromicity.
