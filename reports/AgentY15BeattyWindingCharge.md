# Agent Y15: a necessary all-time mod-9 balance for Beatty rotation sheets

**PAPER PROOF; no decimal Lychrel existence claim.** This theorem concerns *every* width and every possible later return, not a finite-step survival measurement.

## All-width winding-charge theorem

Let alpha be ANY irrational real, q>=q0 an integer, and N(q) a family of positive canonical decimal integers. Suppose its digit sum, modulo 9, is

    F(q) = A*q + B + P(q) + sum_j c_j *
           (floor(a_j*q*alpha + theta_j) - floor(b_j*q*alpha + theta_j)).

All a_j,b_j,c_j,A,B are integers, theta_j are fixed real phases, and P is an integer-valued periodic function of period p. If for some T,G >= 1 the **actual** reverse-and-add map R(N)=N+reverse_10(N) obeys

    R^T(N(q)) = N(q+G)     for EVERY integer q>=q0,

then the finite-cut function

    H(x) = sum_j c_j*(floor(9*a_j*x + theta_j)
                     - floor(9*b_j*x + theta_j))

must be **constant modulo 9 on all its open continuity cells**. In particular,

    C = sum_j c_j*(a_j-b_j) = 0 (mod 9).

The constant-cell test is a strictly stronger necessary condition than charge zero. Neither condition is sufficient to build a carry-closed certificate.

## Proof

1. Reversal preserves digit sum. Consequently digit_sum(R(N)) = 2*digit_sum(N) (mod 9), and a hypothetical T-step return implies F(q+G)=2^T F(q) (mod 9). Since 2^6=1 (mod 9), F(q+6G)=F(q) (mod 9). Set L=54*G*p, a positive multiple of both 6G and 9p. Therefore F(q+L)=F(q) (mod 9) at every sufficiently large q.

2. Fix any residue r (mod 9p), and let x_q = frac(q*alpha/9). Writing q*alpha=9k+9x_q gives, by the *integrality* of every slope a_j,b_j,

    F(q) = A*r+B+P(r)+H(x_q) (mod 9),   q=r (mod 9p).

The same formula applies at q+L. Its circle coordinate is x_(q+L)=frac(x_q+delta) with delta=L*alpha/9=6Gp*alpha, irrational mod 1. Thus H(x_q+delta)=H(x_q) (mod 9) for every sufficiently large q in that residue class.

3. For q=r+9p*t, x_q=frac(r*alpha/9+p*t*alpha), dense on the unit circle. H modulo 9 is a finite step function on the circle because H(x+1)=H(x)+9C. Equality on that dense orbit implies H(x+delta)=H(x) at all points away from the finite set of cuts and translated cuts. An almost-everywhere irrational-rotation-invariant finite step function must be constant: otherwise its nonempty finite set of *essential discontinuities* would have to be invariant under the irrational rotation, yielding an infinite orbit of discontinuities. Therefore H is constant modulo 9 on every open cell.

4. Every integer slope yields floor(9a(x+1/9)+theta)=floor(9ax+theta)+a. Hence H(x+1/9)-H(x)=C **exactly**. Since H is constant modulo 9 away from finitely many cuts, C=0 (mod 9). QED.

Nothing in this proof assumes bounded centre width, uniform carries, a particular overflow sequence, or any finite trial horizon. A proposed exotic carry repair cannot rescue a template that fails the stated digit-sum condition.

## X11 single-sheet corollary (all irrational slopes and winding phases)

For any integer v and real theta, define the two-ended source of X11 in LSD-first order by

    s_i(q) = floor((i+1+v*q)*alpha+theta)-floor((i+v*q)*alpha+theta)
    N(q) digits = [2] ++ [8+s_i(q) for i=0..q-1] ++ [8].

The digit sum telescopes to

    F(q) = 10+8q + floor((v+1)*q*alpha+theta)
                    - floor(v*q*alpha+theta).

Here C=(v+1)-v=1, not 0 modulo 9. Thus, for **every** irrational alpha (including every quadratic irrational), every theta and v, and every positive T and G, it is IMPOSSIBLE that R^T(N(q))=N(q+G) for all sufficiently large q. This eliminates a regenerative return to *that exact X11 source family*, even if intermediate carries and the central interface are arbitrary. It does not eliminate balanced multi-sheet rotations or prove any Lychrel number.

## Constructive redirection

**Search only complementary multi-sheet Beatty bands with net mod-9 winding charge zero, and test that their whole 9-fold torus cut function H is constant modulo 9 before attempting the nonlinear carry/overflow closure.** Charge-zero sheets with distinct phases can still fail the stronger test. If these necessary conditions pass, the unknown task remains a fully rooted, nonshrinking, nonpalindromic decimal edge cycle with exact carries.

## Reproduction / limitations

Run: python3 calculation/new_structures/agent-Y15/beatty_charge.py

The script computes an exact rational-phase finite-circle partition and tests winding charges v=-8..8; it compares two independent implementations of ordinary decimal reverse-add (arbitrary-precision integer and schoolbook digits) on arithmetic controls. Those finite tests confirm code behavior only, not the theorem. The exact partition implementation accepts rational phases; the PAPER PROOF applies to arbitrary fixed real phases. No Lean, all-time decimal witness, or infinite orbit is claimed.
