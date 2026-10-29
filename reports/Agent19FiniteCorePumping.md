# Finite-core mirrored-lattice pumping: exact sufficient cycle criterion

**PAPER PROOF.** This establishes a new finite, base-generic sufficient criterion for a *periodic band with a finite palindromic core* to propagate under ordinary reverse-and-add, without requiring an already self-mirror bulk lattice. The criterion has a source-level Boolean implementation and positive controls in bases 9 and 26. **It is not Lean-verified.** It does not supply a decimal certificate or prove anything about 196.

## 1. Word conventions and hypotheses

Words are least significant coefficient first. `val_b(w)=sum w_i b^i` and `norm_b(w,c)` performs the standard left-to-right (low-to-high) carry normalization of a coefficient word. `pairs(D)_i = D_i + D_{n-1-i}` for a canonical digit word `D` of length `n`. Fix `b >= 2`, a nonempty block `B` with `B_0 > 0`, a nonempty periodic block `W` of length `m`, and a palindromic finite core `C`. All coefficients of `B,W,C` lie in `[0,2(b-1)]`. Fix `0 <= rho < m`, set `U=W[:rho]`, and for every integer `k >= 0` put

```
P_k = B ++ W^(k+2) ++ U ++ C ++ rev(U) ++ rev(W)^(k+2) ++ rev(B)
    = coreTm(B,W,C,m*(k+2)+rho).
```

There are no hidden asymptotic assumptions: `k=0` is included. `P_k` is a symmetric pair-coefficient word, not itself necessarily canonical. Its evaluated integer is `N_k=val_b(P_k)`. `step_b(N)=N+reverse_b(N)`, where `reverse_b` reverses canonical base-`b` digits (the ordinary reverse-and-add operation).

## 2. Exact finite normalization signature

Let `(DB,e)=norm(B,0)`, `(X,c)=norm(W,e)`, `(Y,c')=norm(W,c)`, `(T,d)=norm(U++C++rev(U),c)`, `(Z0,h)=norm(rev(W),d)`, `(Z,h')=norm(rev(W),h)`, and `(DR,gamma)=norm(rev(B),h)`. Every entering carry here is 0 or 1. The carry-out map `f_W:{0,1}->{0,1}` is monotone: increasing the entering carry never decreases the outgoing carry. Therefore `f_W` is exactly one of `(0,0)`, `(0,1)`, `(1,1)`, i.e. constant zero, identity, or constant one. In each case `f_W(f_W(e))=f_W(e)`. The same argument applies to `rev(W)`, proving `c'=c` and `h'=h` automatically (the implementation checks both guards). The final outgoing carry is `gamma in {0,1}`.

With `A=DB++X`, `F0=DR++([1] if gamma=1 else [])`, and `T0=T++Z0`, normalization of all blocks gives the exact *canonical* digit word

```
D_k = A ++ Y^(k+1) ++ T0 ++ Z^(k+1) ++ F0.
```

This follows from the `norm_append` identity and the fixed carries. The digits are all `< b`; if `gamma=1` the last digit is the appended `1`, while if `gamma=0` the final normalized digit is nonzero because `B_0>0` and the last carry is zero. Thus no leading-zero ambiguity is introduced by normalization.

Define `R=Z[gamma:]++Z[:gamma]`, `M=Y++T0++Z[:gamma]`, and `F=Z[gamma:]++F0`. The elementary rotation identity

```
Z^k ++ Z[:gamma] = Z[:gamma] ++ R^k
```

holds for all `k` by induction (including `gamma=0`), giving the finite pumped form

```
D_k = A ++ Y^k ++ M ++ R^k ++ F,
|A|=|F|=|B|+m,     |Y|=|R|=m.
```

## 3. Exact pair-word pumping and finite checker

Put `H=zipadd(A,rev(F))`, `Q=zipadd(Y,rev(R))`, and `K=pairs(M)`. Reflection and equal block lengths give, *for all k>=0*:

```
pairs(D_k) = H ++ Q^k ++ K ++ rev(Q)^k ++ rev(H).              (1)
```

A sufficient finite non-palindrome guard is `A != rev(F)` because those two blocks are exactly the two outer canonical digit ends of `D_k` for all k. The next word `pairs(D_k)` is the full coefficient representation of `step_b(N_k)` by place-value distributivity.

For a prospective target state `(B2,Q,C2,rho2)` and signed length shift `delta`, let `n=2m+rho+delta` and require `n>=0`, `rho2 == n % m`, `C2` palindromic, the target coefficients within bounds, and `|Q|=m`. Define `E=band(Q,n)` and `K2=E++C2++rev(E)`. By definition,

```
coreTm(B2,Q,C2,m*(k+2)+rho+delta)
 = B2 ++ Q^k ++ K2 ++ rev(Q)^k ++ rev(B2).                   (2)
```

The finite Boolean edge checker accepts either of two alternatives:

```
(A) H=B2++T; T++Q=Q++T; K2=T++K++rev(T),
(B) B2=H++T; T++Q=Q++T; K=T++K2++rev(T).
```

A word `T` commuting with `Q` also commutes with every `Q^k`. Reversing this equality gives the corresponding right-side commuting law. Thus the two-sided extra `T` strips can be transferred into or out of the finite centre. Consequently (1)=(2) for **every** `k>=0`, not only the finitely tested values. Since `step_b(N_k)=val_b(pairs(D_k))`, every accepted edge propagates an actual integer reverse-and-add step without palindrome. All tests are on finite words, and the data-independent theorem is the argument above.

## 4. Cycle induction and exact limitations

For a finite nonempty cycle of accepted edges, require that each edge target equals the following edge source, including `B,W,C` and phase, that all intermediate band lengths remain `>=2m` with their specified phases, and that the sum of signed length shifts around the cycle is nonnegative. For any starting length in the initial phase satisfying the finite minimum-prefix-bound (the `minimal_gap` helper), induction on cycle rounds works: the same state returns with no smaller band length, so every subsequent round remains admissible. Within each round, the finite checker guarantees nonpalindromicity before each transition. Euclidean division of an arbitrary orbit time by the positive cycle length gives palindrome avoidance at every time. The Python checker currently implements these guards but has **not** been proved equivalent to them in Lean. The finite theorem concerns the values of the template, not whether a particular input integer has that pair word.

The word-commutation condition is sufficient, **not necessary**; failure to satisfy it does not exclude a centre or a Lychrel number. This proof says nothing about the existence of a base-10 cycle, the actual orbit of 196, or all possible wider/multiple-band formats. Its distinct new contribution over the existing centreless `LatticeBand` proof is arbitrary finite palindromic cores, both absorbing and neutral periods, a precise two-sided rotation at overflow, and a finite commuting-strip check without an unspecified large-gap threshold.

## 5. Reproducibility and controls

From the repository root (Python 3 only; no external dependency):

```
python3 calculation/decimal_frontier/finite_core_pumping/finite_core_check.py .
```

The one script implements the complete finite word-algebra checker and an independently written Python big-integer place-value/digit-list reverse-add checker. It parses existing base-13 control coefficients from the two pre-registered Lean source files already in this repository. Its deterministic randomized test runs 2,000 input templates at four repetition counts (8,000 canonical-digit and pair-word comparisons).
The published base-26 four-edge neutral-band control is accepted; the original base-9 spatial-period-4, |B|=61 lattice gives a 20-edge *finite-core* control, with a smaller alternate control whose initial core is empty and whose maximal core length is 1. Their exact signed band-shift words, arithmetic control sizes, and base-13 control parses are in the executable files. Ordinary-big-integer replay independently checks every step's pair word, reverse-add value, absence of palindromes and exact next template. Negative test: corrupting a base-26 centre must fail the Boolean checker. The mandatory previously known controls for b13 `g=1010010000` with exterior widths 75 and 55, and b9 `g=1100011000, m=4, |B|=61`, are reproduced, not claimed as new discoveries. A separate finite exhaustive and randomized test suite was run locally but not relied upon for this paper proof; no unreviewed census is asserted.