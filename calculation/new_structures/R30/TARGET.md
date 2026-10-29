# R30 exact two-band decimal return checker

Scope: PAPER PROOF of a conditional checker-soundness lemma, plus COMPUTED differential controls. No base-10 Lychrel certificate or successful 120-step return is claimed.

For canonical phase-zero B34 and W9 of calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, let U=(9,a,18-a) with a even, J be a finite coefficient word, and C a finite palindrome of coefficients (an odd midpoint must be even). Let H(q,k)=B++W^q++J++U^k and P(q,k)=H(q,k)++C++reverse(H(q,k)), least-significant coefficient first.

Missing lemma to prove: for every independent q>=q0 and k>=k0, the genuine 120-step reverse-and-add map returns the pairword P(q,k+5), with the exact 120-bit physical overflow clock, and each intermediate pairword has an odd coefficient (sufficient to exclude a palindrome). Since q stays fixed and k increases, these conditions imply an all-time nonpalindromic decimal orbit by induction.

Checker-soundness theorem: if parametric.py returns a symbolic equality with certificate_ready=true, the above claim holds for EVERY q>=q0,k>=k0; there is no finite-sample inference. The checker is sound but incomplete and can return SYMBOLIC_UNDECIDED.

Proof of soundness:
1. For pair coefficients P_i=d_i+d_(n-1-i), the exact next integer has value sum_i P_i*10^i. Schoolbook carry c_(i+1)=floor((P_i+c_i)/10) normalizes this value; the top carry is appended.
2. A word w over coefficients 0..18 acts on the incoming carry 0 or 1 by either identity (all w_i=9) or a constant map (some w_i !=9). Therefore normalizing w^m is exactly one initial copy and m-1 identical steady copies. The implementation checks idempotence on every block.
3. The paired normalized words have a digitwise sum with period lcm of their word lengths. Splits on a symbolic affine length are made only if parameter coefficients are divisible by the period; otherwise the checker refuses. All interval orderings are certified from nonnegative affine coefficients and the value at the quadrant corner; mixed-sign comparisons are rejected.
4. By induction, every returned intermediate straight-line symbolic pairword equals the genuine pairword after that many decimal additions for every admissible q,k. Equality checks inspect every letter of every required period and exact total length. Odd pair coefficients prove nonpalindromicity without needing a particular source realization.
5. P(q,k) is the pairword of a canonical integer when P[0]>0, coefficients are 0..18, and any odd midpoint coefficient is even. The checker validates these input guards.

Negative demonstration, NOT a proof of a decimal Lychrel number: J=[5], U=[9,14,4], C=[10] gives the genuine overflow clock (100010001000)^10 and sum overflow 30. At ALL q,k>=256, the first mismatch from the required 120-step return is at coefficient index 9q+14. Independent Python integers and GMP-free C++ fresh-buffer digit arithmetic agree at q=k=20,40,80,160: positions 194,374,734,1454, respectively.

Verifier audit corrections: `clean` reduces repeated blocks to primitive periods before alignment, so exact aliases such as `(9)^q(99)^q=(999)^q` no longer spuriously return UNDECIDED. The C++ oracle reads the full fixture layout (12 W rows, 12 auxiliary 9-column rows, 12 B rows), and the regression compares symbolic pairwords through phase 120 at off-diagonal `(q,k)` values.

Reproduce:
  python3 tools/parametric_verify_r30.py --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt --J 5 --U 9,14,4 --C 10 --qmin 256 --kmin 256
  g++ -O2 -std=c++17 calculation/new_structures/R30/verify.cpp -o /tmp/r30_verify
  python3 calculation/new_structures/R30/test_parametric.py --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt --cpp /tmp/r30_verify

A failed seam is only a local negative test; moving/active junctions and the existence problem remain UNDECIDED.
