# Q36 target: T* U3 screw phase

Prove the exact local bulk transfer for every charge-zero U3 word
S = { cyclic rotations of (9,a,18-a) : a in {0,2,...,18} }
under the rooted p12/m9 overflow clock gamma_t = 1 iff t mod 12 is 0, 4, or 8.

For each U, decimal normalization of U and reverse(U) has a carry-reset state
because each word contains a coefficient other than 9. If Y- and Y+ are their
normalized digit blocks with their reset carries, define
F_gamma(U)[r] = Y-[r] + Y+[(gamma-1-r) mod 3], r=0,1,2.

Exact finite-state target: for every U0 in S, iterating U_(t+1)=F_gamma_t(U_t)
keeps U_t in S and gives U_(t+40)=rotate_left(U_t,1),
U_(t+80)=rotate_left(U_t,2), and U_(t+120)=U_t, with every U_t having
three distinct entries. The 12-step macro graph should split into three
10-cycles. The local formula must be justified for any sufficiently protected
interior U^k / reverse(U)^k block, independently of J, C, q, and k.

What remains open: synthesize a physical J/C carry-history transition that
respects this three-state screw phase and restores the complete T* interface
with positive net growth. This target alone is not a seam return or a Lychrel proof.
