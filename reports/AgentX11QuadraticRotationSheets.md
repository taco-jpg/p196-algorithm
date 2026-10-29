# Agent X11: quadratic-rotation sheets for decimal reverse-add

## Claim and limitations

**PAPER PROOF:** a conditional soundness theorem and finite sound verification criterion for rotation-sheet reverse-add certificates; also an explicit exact all-length two-phase decimal edge. **COMPUTED:** exact-circle bulk tests and 20,000-step independent genuine decimal integer replay. This is **not LEAN-VERIFIED**, not a base-10 Lychrel proof, and not a claim about 196. The general all-time two-torus verifier is proposed, NOT implemented. Only the one-circle bulk step checker is implemented.

N03 used spatial concatenations of return loops, with a fixed spatial morphic sequence. N20 used affine-moving boundaries but periodic symbols inside strips. The present format uses a strip symbol `h({u*i*alpha + v*q*alpha + theta})` for integer u,v and a quadratic irrational alpha, so the centre/walls can wind **nonperiodically in the temporal cycle counter q**, and reflected letters depend on a second torus phase. This is neither a restatement of a fixed morphic word nor just another wider fixed kink.

## Conditional all-time certificate theorem (PAPER PROOF)

Fix quadratic irrational alpha in (0,1), temporal period T>=1, whole-cycle growth G>=0, and q>=q0. For t=q*T+p with 0<=p<T, prescribe least-significant-first digits D_p(q,i) (0<=i<n_p(q)=a_p+G*q) and carries C_p(q,i) (0<=i<=n_p(q)). Each array is partitioned into finitely many strips by integer-affine boundaries a_j*q+b_j. Within each strip its value is a finite step function h evaluated at `{u*i*alpha+v*q*alpha+theta}` with integers u,v, quadratic-algebraic theta and cut endpoints in Q(alpha). Digit outputs are in 0..9, carries in 0..1. Distinct strips and independent moving boundaries are permitted.

For each edge p to p+1 (with q'=q+1 on wraparound and q'=q otherwise) and every q>=q0, require:
1. Top digit D_p(q,n-1)>0, initial carry C_p(q,0)=0, and gamma=n_next(q')-n is 0 or 1.
2. For every 0<=i<n, s=D_p(q,i)+D_p(q,n-1-i)+C_p(q,i) satisfies D_next(q',i)=s mod 10 and C_p(q,i+1)=floor(s/10).
3. If gamma=1, D_next(q',n)=1.
4. A valid designated index w_p(q) has D_p(q,w_p(q)) != D_p(q,n-1-w_p(q)).

**Soundness proof:** multiply (2) by 10^i and sum: all internal carry terms telescope, yielding val(D_next)=val(D_p)+val(reverse(D_p)); (3) accounts for top overflow; (1) preserves canonical leading digits; (4) gives nonpalindromicity. Induct over phases and cycles. In particular any *accepted* cycle is an infinite Lychrel orbit, with no implication that a base-10 cycle has been found.

## Conservative finite exact checker criterion (PAPER PROOF)

Collect affine breakpoints from each source/target digit/carry strip, reflected source indices n-1-i, shifted carry positions i+1, top overflow and designated witness indices. Beyond a finite computable threshold Q, the sorted order of these finitely many affine functions stabilizes (compare slopes and intercepts). For q<Q, check each actual integer index. For q>=Q, divide the index range by its stabilized boundaries. A fixed-width region has i=a*q+r for finitely many r, so with Y={q*alpha} and X={i*alpha} constrain X={a*Y+r*alpha}. For growing-width regions, conservatively allow (X,Y) to be **any** point of the entire two-torus. This overapproximates the attainable integer pairs, making the test sound but possibly incomplete.

Every asserted equality, leading-digit or nonpalindrome witness is piecewise constant on a finite arrangement of lines `{u X+v Y+theta}=cut` in the unit torus. Integers u,v bound the number of translated lines in [0,1)^2. The line arrangement has finitely many open cells, edge segments and vertices, all endpoints/comparisons effective in Q(alpha). Test an exact representative of each open cell and lower-dimensional face, using right-continuity at cuts. If all pass, every actual integer (q,i) satisfies the edge equations, therefore the telescoping theorem applies to **all** future q. This is a finite soundness algorithm design, not a claim that the full algorithm is implemented or complete. For a Lean proof, define exact quadratic order, torus-region membership and cell evaluation, prove finite_cutoff_sound via stabilized affine orders, then apply the existing digit-carry telescoping induction. No Lean source has been compiled.

## Explicit all-width rank-two Beatty edge (PAPER PROOF)

Let alpha=(sqrt(5)-1)/2, s_i=floor((i+1)*alpha+theta)-floor(i*alpha+theta) in {0,1}, theta any real phase and q>=2. Define LSD-first
`D0=[2] ++ [8+s_0,...,8+s_(q-1)] ++ [8]`.
The symmetric pair coefficients are 10 at both ends and 16+s_i+s_(q-1-i) internally. The first 10 gives digit 0 and carry 1. Every inner coefficient plus carry 1 gives digit 7+s_i+s_(q-1-i) and carry 1; the final 10 gives digit 1 and overflow 1. Thus the exact next digits are
`D1=[0] ++ [7+s_i+s_(q-1-i) for i=0..q-1] ++ [1,1]`.
Both endpoints are nonpalindromes because D0 starts/ends 2/8, D1 starts/ends 0/1. The inner target symbol depends on `{i*alpha}` and `{q*alpha}` simultaneously: this is a concrete nonconstant **two-torus** arithmetic edge for EVERY q, not a temporal return/certificate. Independent schoolbook checks cover 7,996 combinations: q=2..2000, phases 0,1/7,2/7,3/11; altered outputs are rejected.

## Exact one-circle temporal bulk and decimal controls

For a symmetric pair-coefficient bulk f({i*alpha}), let c_-(x),c_+(x) be the incoming carries from the nearest previous/following non-9 coefficient (if every run of 9 has a bounded reset). If the actual digit length grows by gamma in {0,1}, the new bulk is exactly
`f'(x) = ((f(x)+c_-(x)) mod 10) + ((f(x-gamma*alpha)+c_+(x-gamma*alpha)) mod 10)`.
This accounts for the high-side partner shifting by one column on overflow, with independent high/low carries. All new discontinuities occur at finitely many shifted old cut points. For the golden alpha, their positions are exact elements of Z[alpha]; sign tests in Q(sqrt5) make the interval computation exact even on each discontinuity. `rotation_bulk.py` aborts rather than guessing if radius R=24 fails to locate a carry reset.

Take the LSD-first real decimal seed `[7+s_0,...,7+s_1499] ++ [9]*1500`, 3,000 digits. For phases theta 0,1/7,2/7,3/11, compare every lower-half pair coefficient 100<=i<floor(n_t/2)-100 from the exact-cut bulk with independent schoolbook digit-list reverse-add at every t=0..88. Checks: 116403 / 116409 / 116495 / 116495, no mismatches. Maximum cut counts 58/64/68/68, and final cut counts 54/64/68/68; overflow gains 34/35/38/38. The theta 2/7 and 3/11 genuine numbers actually become palindromic at t=4; this is why correct bulk dynamics alone must not be called a Lychrel certificate. Theta 0 and 1/7 are nonpalindromic through t=88.

The theta-0 seed also survives **20,000** actual steps with no palindrome: two separate complete-integer algorithms, GNU GMP arithmetic and schoolbook decimal vectors, agree on the **whole numeral at every step**, final digit count 11,271, full-vector FNV64 10703165220441700701, mismatches 0. These finite-time checks do NOT assert that the bulk persists intact forever. Indeed, the number of cut intervals rises from 2 to 54 by time 88; no finite recurrent phase/cut-cycle or centre closure is known. The constructive redirect is a rank-two phase-winding/expanding-interface cycle, not a finite-horizon infinity inference.

Reproduce with code and concise data at `calculation/new_structures/agent-X11/README.md`. This environment has no GitHub shell checkout or Lean 4.19.0; `tools/verify.py --changed` could not be run, and no Lean changes were made.
