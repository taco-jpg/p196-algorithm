# Agent #110 | Actual exterior two-step return investigation (WIP)

**Claim:** agent110-exterior-two-step-return-20261016, coordinated in https://github.com/taco-jpg/p196-algorithm/issues/61. Source baseline: historical Agent6 ExteriorCore.lean and ExteriorCoverage.lean at commit e775dd342df5190643a61595ff8d93dabfe98a69. Authenticated GitHub account taco-jpg is NOT a dedicated agent identity.

**Precise target:** prove for every canonical P196.Agent6.Exterior state s with phase=6 that advance(advance s) != s, or construct and verify a true counterexample. The phase 6→12→6 is the only possible two-step phase loop of the canonical even nonneutral phases. All finite word lengths are in scope, with the empty word and singleton handled separately.

**Verification status:** This is written proof development and exact exploratory computation only. BoundaryArithmetic.lean has NOT been compiled or axiom audited. No final all-width Lean result, complete palindrome-avoidance result, new integer orbit or infinite 196 theorem is claimed. Do not put source in any accepted build yet.

## Concrete results

- reference_scan.py is a literal independent Python port of original norm, trim, advance and Canonical, validated against the six-state historical Agent110 radial-observable witness. Exhaustive phase6 canonical widths 0..5 yielded counts [1,17,324,6156,116964,2222316], **2,345,778 distinct states** total, zero exact two-step state returns. Full width histogram in scan-length-0-to-5.log. This proves nothing about all widths.
- boundary_obstruction.py checks all necessary terminal-column digit/carry constraints for a putative two-step return, permitting arbitrary digits of the unknown interior reflected normalizations. It finds zero candidate tuples over 3 choices of first trim, 2*2 overflow bits, x and w in 0..18, and both incoming carries in 0..1. This finite abstraction is width-independent but only gives an all-width theorem when the exact source-to-abstraction bridge is proved in Lean.
- BoundaryArithmetic.lean defines the same abstract finite predicate with an intended pure kernel decide theorem, isolated as uncompiled WIP. No native_decide, new axiom, sorry or admitted proof is used.
- An exploratory fixed-width mixed-integer model including full 0/1 carries and actual trim/width constraints found solver-infeasible cases for every width 1..40 and spot widths 50,100,200,400, across all 12 branches. This is **not** an UNSAT proof certificate and requires no acceptance inference.

## Width-independent terminal-column derivation (written candidate, not yet Lean verified)

Let B be a canonical phase6 word with n>=2, x its terminal coefficient (0<=x<=18, x!=6), a in {0,1} the forward carry entering x, and mu in {0,1} its reflected overflow bit. Since raw output length of each advance is old word length plus one, a true two-step equality implies **q+r=2**, where q is first trim count and r second trim count. Thus q is exactly 0,1,2. Set lam1=floor((x+a)/10), e=x%10. The last raw coefficient L1 equals 12+lam1 if mu=0, or 6+lam1+e if mu=1. The penultimate raw coefficient P1 is (x+a)%10+x%10 if mu=0, or (x+a)%10+d with a free reflected digit 0<=d<=9 if mu=1.

If q=0, the final surviving first-step coefficient is w=L1 !=12. If q=1, L1=12, w=P1 !=12. If q=2, L1=P1=12, and w is some 0..18 coefficient !=12.

For phase12 set b in {0,1} for incoming forward carry into w, nu in {0,1} for reflected overflow, lam2=floor((w+b)/10). The second raw final coefficient L2 equals 5+lam2 if nu=0, or 2+lam2+(w+1)%10 if nu=1. Its penultimate raw coefficient P2 equals (w+b)%10+(w+1)%10 if nu=0, or (w+b)%10+f for a free 0<=f<=9 if nu=1.

If q=0 then r=2 entails L2=P2=6; if q=1 then r=1 entails L2=6 and P2=x; if q=2 then r=0 entails L2=x. These necessary conditions are inconsistent, as checked by exhaustive finite arithmetic.

Manual case audit:
- q=0, mu=0: no first trim implies lam1=1, hence w=13. With nu=0, P2=7+b>6; with nu=1, L2=7.
- q=0, mu=1: w>=6 and w!=12. For nu=1, L2=6 would require w=3 or 12, impossible. For nu=0, L2=P2=6 would require w=12, impossible.
- q=1, mu=0: L1=12 implies x+a<=9 and w=2x+a !=12. If nu=0, equality of P2=x gives 3x+2a+b=19; its only solution with a,b in {0,1} is (x,a,b)=(6,0,1), excluded by canonicality. If nu=1, L2=6 implies w=3 (w12 excluded), giving x=1,a=1 but P2>=3>x.
- q=1, mu=1: L1=12 forces x=15 (alternative x=6 excluded), and w lies between 5 and 15 inclusive, w!=12. With nu=0, P2<=12<x; with nu=1, L2=6 forces w=3 or 12.
- q=2, mu=0: L1=P1=12 would force x=6 (excluded). For mu=1 it forces x=15, whereas the untrimmed second L2<=12.
- Boundary cases n=0 and n=1 checked by Python exact enumeration, but NOT by Lean; require separate kernel checks.

## Formalization obligations

(1) Prove terminal-digit/terminal-carry extraction from the *original* norm and both reflected normalizations. (2) Prove raw width = prior width +1, exact prefix/suffix trimming, and bound all new coefficients by 18 for the relevant canonical inputs. (3) Extract q,r and the abstract witness from actual equality of two exteriors; in particular n>=2 allows a penultimate raw coefficient, and q+r=2. (4) Rebuild the finite arithmetic kernel with Lean 4.19.0 and #print axioms; then prove the imported original-map two-cycle exclusion. (5) Kernel-check n=0 and1. Review exact semantics and hypothesis preservation independently before accepting any theorem.

The known Agent9 ExteriorErasure full_binary_collapse has arbitrarily deep one-step contractions for specific words, so width monotonicity must NOT be assumed. The existing historical Agent110 radion/phase observable returns without actual state return; the old result is preserved and not duplicated. The current scope does not take Agent #6 signed-beta update/telescope, Agent #416 return-certificate lower bounds, or any shared main-branch integration slot.

## Reproduce (Python 3, only the optional MILP discovery needs SciPy)

    python3 reference_scan.py 5
    python3 boundary_obstruction.py

Source of the exact port, finite scan, abstraction, and uncompiled Lean draft is retained in this contribution.
