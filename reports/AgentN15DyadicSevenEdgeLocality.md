# Agent N15: all-height seven-step dyadic decimal carry locality

**PAPER PROOF**, for the exact finite scope below. Neither Lean-verified nor an infinite decimal Lychrel certificate. The independent integer program and the finite-factor arithmetic are supplementary checks, not a substitute for the symbolic all-height argument.

## 1. Input words and arithmetic convention

Work least-significant coefficient first. Let A=14, B=16 and let sigma(A)=AB, sigma(B)=BA. For every h>=2 put `w_h=sigma^h(A)`, L=2^h, `H_h=[4]++w_h` and `P_0(h)=H_h++reverse(H_h)`. Each P is a symmetric *pair-coefficient* list with entries in [0,18]; its base-10 normalisation gives the next ordinary reverse-and-add integer, and its normalised digits paired with their reverse give the next pair-coefficient word. Choose an actual N_0(h) with lowest digit 0, highest digit 4, and for each intermediate lower pair coefficient p in {14,16} choose lower digit p-9 and opposing upper digit 9. This is a positive ordinary decimal integer with pairword exactly P_0(h).

Earlier N15 work proved the exact first two pairword steps for every h>=2. Here is a self-contained explicit description. Set m=L+1, `q=[9,9]++[2(w_h[i-1]-9) for 2<=i<m]` and

```
r[0:3] = [10,9,q[2]-10] = [10,9,4]
r[i] = q[i]+q[i-1]-18                     (3<=i<m)
r[m] = 2(q[m-1]-9)
P_2(h) = r ++ reverse(r[:-1])              (length 2m+1)
```

These are the first two exact identities; both can be checked by direct carries, with `P_1=q++reverse(q)` and its step having a final overflow digit 1. For h>=2 the first two source letters after A are B,B, hence `r[3]=10`.

## 2. New exact third step, all h

In the normalisation of P_2, the lower three entries `[10,9,4]` have carries 1,1,0, and the high mirrored entries have the corresponding isolated boundary carries. For every `i>=3`, r[i] belongs to {2,6,10}; in particular all carries become **local** away from the single initial neutral coefficient 9 and its mirror. Define `a(x)=1` for x>=10 and 0 otherwise, and

```
g = [1,0,14,5]
for 4<=i<=m:
    g[i] = r[i]+r[i-1]-9*(a(r[i])+a(r[i-1]))
P_3(h) = g ++ reverse(g)                  (length 2m+2)
```

This is the exact arithmetic next pairword, including both ends and the overflow-induced partner shift. The low-side 3-letter bulk coding is explicit: `r[i]=d(w[i-2],w[i-1])`, where `d(x,y)=2(x+y-27)` for 3<=i<m; hence `g[i]=d(w[i-2],w[i-1])+d(w[i-3],w[i-2])-9*(a(d(...))+a(d(...)))` for 4<=i<m. The fixed prefix and the single last exceptional coefficient are determined by the first and last few w letters. Thus P_3 is a genuine uniform length-doubling substitution-derived 3-block word, not a claimed periodic kink.

## 3. New base-generic local-carry lemma

Let b>=2 and P be any symmetric pairword with all coefficients `0<=P[i]<=2b-2` and **no coefficient equals b-1**. Write `a_i=floor(P[i]/b)`, `e_i=P[i] mod b`. Incoming carries are always 0/1. Since e_i<=b-2, the outgoing carry after processing cell i is **exactly a_i, regardless of incoming carry**. If `a_0=0`, there is no final overflow and the full next pairword of the same length is given by the radius-one cellular operator

```
F_b(P)[i] = 2*e_i + a_(i-1) + a_(i+1),
a_(-1)=a_n=0.
```

This follows by normalising the low and its mirror high digit independently: their incoming carries are a_(i-1) and a_(i+1). For general `a_0=1` and a final overflow digit, the new word has length n+1, endpoints `e_0+1` and interior entries `e_i+e_(i-1)+a_i+a_(i-1)` (i=1,...,n-1). This latter identity is also exact for any n; it explains the one-cell shift at P_2. These formulas are a **sound one-step certificate format** for nonneutral stretches in every base, and do not assume a fixed spatial period.

For base10, write F=F_10. The newly certified identities are

```
P_4=F(P_3), P_5=F(P_4), P_6=F(P_5), P_7=F(P_6).
```

The crucial, non-circular obligation is that P_3,P_4,P_5,P_6 contain NO coefficient 9 for **all** h>=2, so F applies at each step. Their first coefficients are 1,2,4,8 respectively; none causes a terminal overflow. P_7 starts with 16 and may contain 9, so no P_7-to-P_8 identity by this lemma is claimed.

## 4. Finite factor argument for *all heights*, not sampled heights

For each k=0,1,2,3, a potential bulk coefficient at time t=3+k depends on a radius-k neighbourhood of the 3-letter coding of w_h, hence on **a length-(2k+3) factor of w_h**. The relevant factor lengths are 3,5,7,9. Since all are <=9<16, and `w_h=sigma^4(sigma^(h-4)(A))`, every such factor of w_h at h>=4 lies entirely within one or two successive sigma^4 letter-blocks. Therefore it belongs to the finite union of factors of `sigma^4(UV)` over U,V in {A,B}. This is a universal containment valid for **arbitrarily large h**, with no periodicity hypothesis. The all-factor computation (only 6,12,20,24 distinct factors respectively) gives the EXACT allowed bulk values:

| time t | length of original w factor | bulk coefficients |
|---|---:|---|
| 3 | 3 | 7,8,12 |
| 4 | 5 | 5,14,15,16,17 |
| 5 | 7 | 10,11,14,15 |
| 6 | 9 | 2,4,10,12 |

None contains the neutral coefficient 9, so the local-carry hypothesis holds throughout all bulk positions for the preceding steps.

Only bounded windows next to the two exterior endpoints and the mirrored centre remain. After k<=3 radius-one steps, those windows depend on at most 16 original w letters at each end. At h>=8, the first 16 letters of w_h always equal sigma^4(A). The last 16 equal sigma^4(U), where U is the last letter of sigma^(h-4)(A), which is A or B according to the parity of h-4. This is an immediate inductive consequence of sigma(A) ending B and sigma(B) ending A. Thus **exactly two boundary classes**, represented by h=8 and h=9, cover *all* h>=8; h=2..7 are each checked directly. The boundary checks also confirm no9 and the fixed root coefficients at all four intermediate times. The supplied `ca_proof.py` enumerates the four complete universal factor sets, exact edge/centre boundary windows of the two parity classes, all six exceptional finite heights, and positive controls h=2..15. The proof of universal coverage is the substitution block decomposition just given, not any extrapolation from the finite-height controls.

By induction, all four applications of F are real ordinary reverse-and-add pairword edges for every h>=2. Together with the first three edges, this gives **seven exact transitions for every dyadic level**.

## 5. No-palindrome witnesses, limits and reproduction

For the actual ordinary decimal initial integer N_0(h) in section 1, the extreme digits 0 and 4 differ. For steps t=1,...,7 the first opposing unequal digit pairs `(position from low end, low digit, opposing high digit)` are **independent of h** and equal, in order, to `(0,4,5),(0,9,1),(0,0,1),(1,0,1),(2,8,9),(1,2,3),(1,5,6)`. Their uniformity follows from the same finite edge windows, and direct carry calculation at those edges proves N_0,...,N_7 nonpalindromic for every h>=2. The full word away from the ends is not required for this latter check.

An independent `ca_independent.cpp` constructs positive ordinary decimal seeds, iterates actual digit-vector `N+reverse(N)` (without using the symbolic carry engine), and compares the entire predicted P_3,...,P_7 at h=2..15. It rejects a deliberately corrupted predicted coefficient at all 14 heights. `ca_proof.py` also directly compares P_3,...,P_7 with pairword arithmetic h=2..12; the **universal theorem** relies on the finite-factor lemma above. Both checkers are committed with the result; reproduce with `sh calculation/new_structures/agent-N15/run_ca.sh` from the repository root. These are the first seven steps only, NOT a recurrence returning to the initial template, not a guaranteed >=20,000-step morphic representation, not Lean verification and not a proven decimal Lychrel number.

**Construction consequence:** This is a new *height-uniform local-transfer* building block for a prospective period-doubling certificate. To turn it into an infinite certificate, one must additionally exhibit a checked temporal-block rule that returns a transformed dyadic word at a new scale after a positive number of steps and preserves nonpalindromicity. None is claimed here.
