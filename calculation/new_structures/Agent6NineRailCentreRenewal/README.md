# Exact conditional all-length decimal 9-rail centre renewal

PAPER PROOF, conditional, not a decimal Lychrel certificate. Let P be a symmetric LSD-first decimal pair-coefficient word H + 9^k + C + 9^k + reverse(H), with palindromic C and canonical source. Let a be the normalizing carry entering the lower 9 rail, and b the carry entering the upper rail after C. The carry map f_9(c)=floor((9+c)/10)=c is the identity. Thus interior normalized digits on the two sides are 9(1-a) and 9(1-b); the next interior pair coefficient is 18-9(a+b). It equals 9 if and only if a+b=1. Both physical carries must be retained.

For complementary carries, normalize C=(c_0,...,c_(L-1)) by u_0=a, d_i=(c_i+u_i) mod 10, u_(i+1)=floor((c_i+u_i)/10), and u_L=b=1-a. For actual length-overflow g=0 the next centre is D_i=d_i+d_(L-1-i). For g=1 the next centre has L+1 coefficients, with D_0=D_L=d_0+9a and D_i=d_i+d_(L-i) for 1<=i<L. These are exact ordinary decimal reverse-add pairword equations, including the high-side one-digit lag on overflow. The map commutes with symmetric nine-padding for every j>=0:
F_g(9^j C 9^j) = 9^j F_g(C) 9^j,
with the same two carries. Proof: f_9 is the identity; substitute the digit formulas and match the left padding, centre, and right padding separately. This is an all-length algebraic identity, not finite-horizon extrapolation.

The compact cert.json lists eight palindromic cores and their unique complementary carry words under g=(1000)^6 or g=(1000)^12. The exact integer recurrence checks 288 phase rows. Four cores return after H=24 and four after H=48, with C_H=9^(H/8) C_0 9^(H/8), all intermediate words palindromic as coefficient words and legal at odd centres. The padding identity then proves this centre renewal for EVERY rail length and EVERY subsequent macrocycle, provided an external physical seam realizes the specified carries/overflow and preserves the rail. This supplies a nondepleting all-time centre-subsystem repair.

Missing decimal theorem: find a single physically rooted p12/m9 B34 W9^q J 9^k C seam and canonical seed whose full ordinary orbit emits one of the listed carry words, preserves the rooted W9 exterior at every phase, returns the finite junction/phase state, and has phasewise nonpalindrome witnesses. The independent controls below construct separate canonical decimal sources for each edge, NOT one continuous returning orbit. No base-10 Lychrel number, global obstruction, or Lean verification is claimed.

Reproduce from repository root (Python 3 stdlib only):

    python3 calculation/new_structures/Agent6NineRailCentreRenewal/reproduce.py
    python3 calculation/new_structures/Agent6NineRailCentreRenewal/independent_check.py

Expected: both commands print ALL CHECKS PASSED. The first recomputes all 288 exact rows, verifies compact cert.json, and tests 2688 padding commutations. The second uses independent ordinary decimal big integers and literal digit reversal on 2304 phase/width/padding cases, checking canonical source realization and true overflow. All eight cores and both centre parities are covered. No SAT solver or external package is needed.
