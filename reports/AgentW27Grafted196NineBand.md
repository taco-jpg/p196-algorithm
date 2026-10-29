# W27: a parameterized 196-shell graft with an exact centre insertion law

## Result and scope
**COMPUTED** (20,001 steps for a parametric decimal family) with an elementary **PAPER PROOF** insertion lemma. For Q>=6005 define the genuine decimal integer N_Q(0) by the most-significant-first string `196 9^(2Q) 196`, with no spaces. Let N_Q(t+1)=N_Q(t)+reverse_decimal(N_Q(t)), without leading zero padding. At each t=0..20000 the number is nonpalindromic. These are not iterates of the three-digit number 196: the two copies of 196 are end blocks of a different, large integer.

## Exact algebraic insertion lemma
Let I(x) insert two 9 digits at the central cut floor(n/2) of the length-n least-significant-first digit word of x. If x and F(x)=x+reverse(x) both have >=5 consecutive 9 digits crossing their central cut, then F(I(x))=I(F(x)). Indeed, the palindromic pair coefficient word P_i=d_i+d_(n-1-i) of x has 18 at the two sites straddling its centre. Inserting two central 9 digits replaces P by P with two central coefficients 18 inserted. The 18 immediately before the insertion sends carry 1 into the cut, independent of earlier carries. Normalizing the two extra 18 coefficients therefore yields digits 9,9 and still carry 1, so all subsequent output digits and the final overflow are unchanged. For odd n with an overflow, the insertion cut shifts by one between input/output canonical centres; the >=5 central 9s in F(x) make the two placements identical digit words. Hence the equality in both parities and for gamma=0 or 1. Extra central 9s preserve both the hypotheses and the location of any off-centre palindrome mismatch.

By induction on Q and t, if every baseline N_6005(t) and successor retain >=5 central 9s for t<T, then every N_Q(t) is obtained from N_6005(t) by inserting 2(Q-6005) central 9 digits, for every Q>=6005 and t<=T. Inserting digits equal to both central digits cannot repair an existing mismatch outside the central region. It therefore preserves nonpalindromicity. The full symmetric coefficient word has a central run of coefficient 18 whose length increases by exactly 2(Q-6005). The surrounding finite word B_t is unrestricted and NOT claimed periodic.

## Independent finite replay and checkpoints
`hybrid.cpp` implements (1) a least-significant-first array pair-addition carry engine and (2) a separate most-significant-first decimal string addition against an explicitly reversed string. It compares their entire decimal words on EVERY step, checks palindrome and centre-band on EVERY step, and independently evolves Q+1 for the insertion identity. It uses no hashes to establish word equality; FNV-1a numbers are merely reproducibility checkpoints.

| t | decimal length Q6005 | central 9 run | central pair-18 run | FNV-1a (LSB digit bytes) |
|---:|---:|---:|---:|---:|
| 0 | 12016 | 12010 | 12010 | 7141967785145180873 |
| 5000 | 14114 | 9016 | 9016 | 18347609432454092447 |
| 10000 | 16178 | 5991 | 5990 | 1410202196998345974 |
| 15000 | 18233 | 2997 | 2997 | 5202476119325710156 |
| 20000 | 20317 | 5 | 5 | 8356616497710298383 |

The minimum centre-9 and coefficient-18 lengths over ALL 20,001 states are 5; 8,301 overflows. The Python `lemma_check.py` uses actual arbitrary-precision integer reversal/addition through t=160 for both Q6005 and Q6006; it also exhaustively checks 19,566 small-flank transition cases satisfying the >=5 successor-band criterion. All passed.

Reproduce (no libraries beyond C++17 and Python3):
```sh
c++ -O3 -std=c++17 calculation/new_structures/agent-W27/hybrid.cpp -o /tmp/w27
/tmp/w27 6005 20000
python3 calculation/new_structures/agent-W27/lemma_check.py
```

## Connection to the true 196 problem
The real orbit of 196 has no 6005-copy central 9 reservoir; its overflow schedule differs, and this construction is not a proof about 196 itself. The result is a rigorous *finite-horizon lift* from the 196 shell: the two-end 196 boundary data can coexist with arbitrarily many exact centre-9 cells for 20,000 steps and preserve an externally checked palindrome mismatch. The mechanism ultimately consumes the finite baseline band (only five central 9 digits remain at t=20000). To obtain an **infinite certificate**, a future construction must replenish the band at least as fast as the boundary dynamics depletes it; adding an arbitrarily large finite Q is not enough. Unlike a fixed finite orbit check, the Q-insertion law is an exact all-Q statement for the verified time interval. It does not establish a periodic centre, an infinite decimal Lychrel number, or Lean verification.
