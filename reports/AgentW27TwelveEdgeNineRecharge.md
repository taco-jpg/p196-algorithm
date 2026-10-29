# W27: exact decimal 12-edge polynomial recharge gadget

**PAPER PROOF of all-parameter finite edges**, with independent COMPUTED arithmetic controls. The goal is a reusable central 9 source, not a negative centre census.

Let F(n)=n+decimal_reverse(n). For each integer q>=2 take N_q(0) to be the literal base-10 concatenation `2905 ++ 9^(2q) ++ 8723`. The **entire exact orbit** for t=0..12 is the following. All strings below are most significant digit first; the exponent of 9 is 2q+e.

| t | prefix A | e | suffix B |
|---:|---|---:|---|
| 0 | 2905 | 0 | 8723 |
| 1 | 6184 | 0 | 3815 |
| 2 | 11368 | -1 | 88631 |
| 3 | 25057 | -1 | 74942 |
| 4 | 50005 | -1 | 49994 |
| 5 | 100000 | -2 | 899999 |
| 6 | 10 | +2 | 8900000 |
| 7 | 1100098 | -3 | 8899901 |
| 8 | 2200087 | -3 | 7799912 |
| 9 | 4400065 | -3 | 5599934 |
| 10 | 8800021 | -3 | 1199978 |
| 11 | 17599933 | -4 | 82400066 |
| 12 | 83600362 | -4 | 16399637 |

## Proof, valid for every q>=2

Put X=10^(2q-4). For each row (A,e,B), with lengths p=|A| and r=|B|, the full integer is exactly
```
V(A,e,B) = [(int(A)+1) * 10^(e+r+4)] * X + [int(B)-10^r].
```
Its decimal reversal, understood numerically and allowing leading zeros in the reversed string, is exactly
```
R(A,e,B) = [(int(reverse(B))+1) * 10^(e+p+4)] * X
         + [int(reverse(A))-10^p].
```
All powers of ten are nonnegative integers in this table. For EACH of the 12 adjacent rows, both independent coefficients of X and the constant coefficients satisfy
`V(t)+R(t)=V(t+1)`. The standalone Python checker exhaustively asserts all 24 small-integer equalities; they are fixed arithmetic identities, not experiments at selected q. Substitution of any q>=2 then proves every orbit edge by induction. First-two-digit comparisons of each prefix with the reverse of each suffix (13 finite cases) show a mismatch at index 0 or 1 in every row, so ALL these states are nonpalindromic.

The first 6 edges raise the central 9-band exponent from 2q to 2q+2, with a **+4 jump at edge 5->6**. At phase 6 the two caps are `10` and `8900000`, not the initial caps `2905`, `8723`. Through phase 12, the band falls to 2q-4, demonstrating exactly why this is NOT a cycle or indefinitely self-recharging certificate. This yields a finite, proven base-10 source of neutral 9-band growth that could be coupled to a cap-restoration mechanism; that coupling remains open.

## Independent checks

`recharge.py` uses integer coefficient identities for the proof and separate Python arbitrary-precision literal `int(s)+int(s[::-1])` controls at q=2,3,4,5,40,100,600. `recharge_digits.cpp` independently implements least-significant-first carry arithmetic and compares ALL digits of every one of the 13 phase words at the same q. The 2-site palindrome-obstruction condition is separately asserted by the Python tests.

Reproduce from the root:
```sh
python3 calculation/new_structures/agent-W27/recharge.py
c++ -O3 -std=c++17 calculation/new_structures/agent-W27/recharge_digits.cpp -o /tmp/w27-recharge
/tmp/w27-recharge
```

**Scope limits:** twelve steps, all integer q>=2; no infinite-time claim, no eventual repetition, no Lean proof, and no claim about the actual orbit starting at 196.
