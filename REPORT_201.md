# REPORT_201 — Direction 1: Template decidability

**Answer. THEOREM:** Decimal reverse-and-add has an exact finite-state carry checker on outside-in folded digit pairs, including overflow and palindrome avoidance. **THEOREM:** For any fixed iteration count m, a finite menu of templates with at most r constant runs and intervening blocks of length at most B, and an explicitly prescribed affine map v=Mu+t between input/output run-length vectors, existence of an m-step nonpalindromic return is decidable using effective semilinearity/Presburger arithmetic. **THEOREM:** A finite graph cycle of *phases alone* is not sufficient to conclude infinite recurrence, because run-length inequalities may fail on repeated traversals. **THEOREM:** An exact affine cycle whose guard inequalities remain invariant under its total displacement does give an infinite orbit; when each step avoids palindromes, the starting number is a decimal Lychrel number. **IDEA:** Find and close such a pumpable affine regime for concrete decimal templates. **CONJECTURE:** Useful two-band cases admit a finite family of guard-preserving affine regimes. Nothing here establishes an actual decimal Lychrel number or unrestricted decidability.

## Exact carries and finite-state checking

Write input digits d_0,...,d_(L-1) from units to highest (d_(L-1)>0). Let q_i=d_i+d_(L-1-i) (symmetric), c_0=0, e_i=(q_i+c_i) mod 10, and c_(i+1)=floor((q_i+c_i)/10). Since q_i<=18, each carry belongs to {0,1}; append a most-significant digit 1 iff c_L=1.

**THEOREM (two-frontier checker).** Reading pairs (d_i,d_(L-1-i)) from the outside inward, use state (a,b)=(c_i,c_(L-i)). Initially a=0; guess b=c_L in {0,1}. On reading the pair (u,v), let q=u+v and guess h=c_(L-1-i). Require floor((q+h)/10)=b. Emit low digit (q+a) mod 10 and high digit (q+h) mod 10. Update state to (floor((q+a)/10),h). For even L, accept the center precisely when a=b. For odd L with central input z, require b=floor((2z+a)/10), and emit central digit (2z+a) mod 10. The b=c_L guess determines whether the leading overflow digit 1 must be emitted. Folding this extra leading digit into the paired output uses only a one-digit alignment buffer. Comparing each output pair for equality detects a palindrome; its complement detects nonpalindromic outputs.

**Proof.** The low carry is propagated by the actual recurrence; high carry guesses are constrained by the exact recurrence in reverse; the center equations glue the chains. Every accepting path is therefore the unique actual carry chain. Conversely the unique actual chain yields an accepting path. All state components and the overflow alignment buffer range over finite sets. QED.

## Fixed-time return decidability

Fix m,r,B and finite template menus A,C. Each template prescribes a bounded number of constant-digit runs separated by specified blocks of length at most B, and has nonnegative run-length variables u,v. Leading-digit validity and zero-length ambiguities can be handled by finite-state constraints. Fix any affine target equation v=Mu+t with integer coefficients.

**THEOREM.** The set of u for which T^m(x_A(u))=x_C(Mu+t) and all T^j(x_A(u)), 1<=j<=m, are nonpalindromes is effectively semilinear.

**Proof.** The exact one-step relation in folded representations is finite-state by the preceding theorem. Finite-state relations are closed under fixed finite composition and projection. At most one most-significant overflow digit is added at each iteration, so alignment discrepancies over fixed m are bounded by m. Template schemas are finite-state checkable by scanning both outside-in frontiers through their prescribed ordered runs and bounded blocks. Label each transition by the unit vector(s) recording which run-length coordinate(s) it contributes to. The achievable length tuples are the additive image of a regular language and hence effectively semilinear (effective Parikh-image theorem). Intersect with v=Mu+t, enforce nonnegativity and project onto u; all of these operations preserve effective Presburger definability. QED.

**Limitation.** This proves fixed-m reachability. It does NOT reduce unbounded temporal recurrence to ordinary cycle search in a finite graph.

## Exact cycle obstruction and a sufficient replacement

**THEOREM (obstruction).** Let a symbolic phase graph have a sole state A and a self-loop with guard u>=1 and update u'=u-1. Its phase graph has a directed cycle, but no initial finite u allows infinitely many traversals. Thus finite *phase-only* cycles do not certify template recurrence. QED.

**THEOREM (pumpable-cycle sufficient condition).** Suppose a concrete, exact cycle has per-step affine-translation updates, total displacement Delta, and at intermediate step j the run-length vector equals u+Delta_prefix_j. Suppose each intermediate guard is a conjunction A_j v>=b_j, the starting vector satisfies every guard, and A_j Delta>=0 componentwise for every j. Then the cycle repeats indefinitely: on repetition k the guard left side is A_j(u+Delta_prefix_j)+k A_j Delta>=b_j. If the exact cycle represents genuine reverse-and-add iterations and every output is nonpalindromic, its starting number is Lychrel. QED.

## Small verification, not a proposed construction

No construction is claimed, so the >=1000-step check required for proposed constructions is inapplicable. An exhaustive checker of the two-frontier carry algorithm against ordinary arithmetic passed all 999 inputs n=1,...,999. Full reproducible program is in the local attached REPORT_201.md; core recurrence:

```python
def T(n): return n + int(str(n)[::-1])
# For each n=1..999 enumerate final carry b in {0,1},
# recursively guess high-side incoming carry h in {0,1},
# require (q+h)//10 == b, update (a,b)=((q+a)//10,h),
# glue at the center, reconstruct low+center+reversed(high),
# append 1 iff original b=c_L was 1.
# Verify exactly one reconstructed result, equal to T(n).
```

Output: `PASS: 999 inputs; unique output, carry and palindrome checks`.

## Sharpest open question

**IDEA:** Can a concrete finite set of exact affine update regimes for constant-run/bounded-interface templates be proved closed under an m-step return, with some cycle satisfying the guard-preservation inequalities? The unresolved step is *finite affine closure across arbitrarily many returns*, not fixed-m semilinearity.

**Status:** No decimal Lychrel number established. No Lean verification performed. No claims about any particular seed.
