# Complementary-band cycle period obstructions — Agent #8

This contribution builds on `../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, Git blob `f48a0ec61e7ff0419bb9121a792e79505810db50`, initially read at main `a71d6e79b009da691e2d97057f83e108a3fcff4f`. Coordination is in issue #4, with complementary search work discussed in #7 and #8. No external novelty, human review, or proof about 196 is claimed.

## Established results and evidence boundary

For any nonempty returned phase/interface in the stated complementary two-gap quotient, let P be its period, H its total number of actual overflows, and dg,dh its signed total gap changes. Then

    P/4 <= H <= P/2,                 H = 2(dg+dh).

Consequently P >= 4; in particular no two-step returned interface exists, regardless of its interface sizes. This is NOT an assertion that the leading coefficient alone has no two-cycle: the necessary exterior graph contains 18 -> 9 -> 18 with one overflow, but one overflow cannot supply the even width gain of a returned two-gap template.

For a phase in {2,4,8,16,14,10}, P is divisible by six and

    dg-dh = 0 (mod 9).

At P=6 these conditions force H=2, dg+dh=1, and at least one of dg,dh is <= -4. Thus no six-step interface cycle in these six phases can meet the nonnegative-two-gain criterion for infinite repetition. This is an all-interface written obstruction, not a finite search result. It does not exclude higher periods, unbounded interfaces, or unrelated safe-orbit constructions.

For these same six phases, if P<36 and both gains are nonnegative, they must be equal: dg=dh=a and H=4a, where ceil(P/16) <= a <= floor(P/8). Hence a hypothetical period-12 cycle must have (dg,dh,H)=(1,1,4), and a period-18 cycle must have (2,2,8). Periods 24 and 30 permit only a=2 or a=3 under these necessary tests. These are filters, not existence claims.

`PeriodObstructions.lean` has 24 supporting theorem declarations, freshly compiled with official Lean 4.19.0 using only `Std`. All 24 declarations have explicit printed dependency audits; the only dependencies reported are `propext`, `Classical.choice`, and `Quot.sound`, and the finite exterior certificate has no axiom dependencies. No admitted proof, custom axiom, or native evaluation shortcut appears in the accepted source.

The formal file proves normalization/mirrored-word mass congruence, its arbitrary six-multiple iteration, the actual template mass congruence, the complete finite exterior table, telescoping path bounds, and the arithmetic exclusions. Its final template theorem STILL HAS explicit exterior-evolution and width-identity premises. The all-word interpretation of those premises is the written argument below. This first publication does not claim a standalone end-to-end Lean theorem about ordinary reverse-and-add. Formalizing that remaining bridge is a subsequent task.

## 1. Actual exterior dynamics

Use the source note's convention: words are least-significant first, Q is a canonical symmetric mirrored-sum word with coefficients 0 through 18, and G(Q) is the mirrored-sum word of the canonical digits of Q evaluated at ten. Write p for Q's positive exterior coefficient and e in {0,1} for the actual carry entering its last column. The actual final overflow is gamma=1 exactly when p+e>=10.

The low digit after normalization is p mod 10. Without overflow, the high digit is p+e, necessarily positive and at most nine; p<=9 then gives new exterior 2p+e. With overflow, the new high digit is one, so the new exterior is p mod 10 + 1. Therefore every actual step projects to

    gamma=0:  p' = 2p+e,       p+e<10;
    gamma=1:  p' = p mod 10+1, p+e>=10.

All carries remain bits because each column input is at most 18+1. No leading-zero trimming occurs: without overflow the last digit is p+e>=1; with overflow the appended one is leading. Hence actual width increases by exactly gamma. The argument also covers width one, where e=0.

The finite relation allows both e choices; it is an overapproximation. No assertion of global realizability is made for an arbitrary graph edge or path.

## 2. Two exact potentials

For p=1,...,18 in that order, set

    U = [0,0,0,1,0,1,1,1,2,1,1,1,2,1,2,2,2,3]
    V = [4,3,2,2,2,1,1,1,1,1,1,0,0,0,0,0,0,0].

For every one of the 36 (p,e) choices, direct substitution in the exact exterior formula gives

    2 gamma <= 1 + U(p)-U(p'),
    1 <= 4 gamma + V(p)-V(p').

`finite_exterior_certificate` proves all choices by kernel-reduced finite decision. `path_potential_bounds` proves the arbitrary-length telescoping identities by induction. On a path returning to its initial exterior, both potential differences cancel, giving P<=4H and 2H<=P. In particular a nonempty closed path has H>0.

For a nonclosed actual path the boundary terms remain: 2H<=P+U(p0)-U(pP) and P<=4H+V(p0)-V(pP). Replacing these terms by zero without an exterior return would be invalid.

## 3. Width and signed gap gains

The source quotient parameterizes

    Q(c;B,A,C;g,h) = B c^g A d^h C d^h rev(A) c^g rev(B),  d=18-c.

Its width is 2|B|+2|A|+|C|+2g+2h. If the phase and all three finite interfaces return after P steps, comparison of widths gives H=2(dg+dh). This works with signed gains. A finite quotient cycle can always be realized for one full traversal by choosing both initial gaps above every finite within-cycle loss; it is not necessary to assume the cycle can be repeated indefinitely to derive this identity.

Since H is positive and even, H>=2. The upper potential bound then yields P>=4 and excludes P=2.

## 4. Digit mass, not a probabilistic argument

Let M(W) be the sum of a coefficient word. A carry replaces ten units at one column by one unit at the next and therefore changes this sum by a multiple of nine. Normalization, including the optional final carry, preserves M modulo nine. Pairing a digit word with its reversal doubles its mass. Thus

    M(G(W)) = 2 M(W) (mod 9).

This identity is formally proved for the recursive list normalization itself; it is not merely checked on examples. Since 2^6=1 modulo nine, a six-multiple number of G steps preserves M modulo nine.

If the template returns with the same phase and interfaces, its mass change is

    2c dg + 2d dh = 2c(dg-dh) (mod 9).

For c in {2,4,8,16,14,10}, 2c is invertible modulo nine, proving dg-dh=0 modulo nine. This argument uses the six-phase restriction; invertibility cannot be asserted for c=6 or c=12.

At P=6 the potential inequalities imply 2<=H<=3. Evenness gives H=2 and dg+dh=1. The difference dg-dh is an odd multiple of nine, hence has absolute value at least nine, forcing one gain <=-4. Both nonnegative gains are impossible.

For P<36 with nonnegative gains, dg+dh=H/2<=P/4<9, so |dg-dh|<9. The congruence forces dg=dh=a. Substitution gives H=4a and the stated period filters.

## 5. Verification and provenance

Accepted Lean source commit: `8902b2b8d5cf495d7ee407e905817e1737aae770`.

- Source bytes: 11080.
- Source SHA-256: `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a`.
- Source Git blob: `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119`; fetched again after publication and matched to the locally compiled bytes.
- Compiler: Lean 4.19.0, x86_64-unknown-linux-gnu, commit `6caaee842e94`.
- Official compiler archive SHA-256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
- Compiler recovered through concurrent Agent5's successful workflow run `38682012925`, artifact `11948452826`, from commit `cf719675bc5efd3e91bce8f76d137a25808c1e0d`.

Reproduce from this directory with `lean -o PeriodObstructions.olean PeriodObstructions.lean`. No mathlib checkout is required. The fresh audit output is retained as `lean-audit.log`; compiler distributions and compiled objects are reproducible infrastructure and are not research-source artifacts.

The independently reconstructed Python quotient passed 100,536 literal-integer normalization controls: all 28,512 trimmed states with each of B,A,C of length at most one in the eight periodic phases, at gaps (2,2),(3,5),(7,2), plus 5,000 deterministic random states over all sixteen legal phases at those three gaps. These are formula controls, not a cycle proof. A capped exterior-only exploration from 144 small outer states visited 31,748 distinct states without finding a cycle before the bound |B|=200; every initial case reached a cap and remains UNKNOWN. This exploratory cap is not used in any theorem. Reproducibility source and raw command logs are being published separately in the same directory.

A proposed shortcut from the saturated exterior cycles to the existing full-high-region theorem was rejected: that theorem requires EVERY coefficient to lie in 9 through 18, which a leading-coefficient condition does not establish. No such implication is used here.

## Current limits

No qualifying complementary-interface cycle is exhibited. The ordinary whole-word exterior and width bridge is written, not yet integrated into this Lean module. No other agent's formal module has been independently rebuilt in this pass. No conclusion about whether the orbit of 196 eventually reaches a palindrome follows from these exclusions.
