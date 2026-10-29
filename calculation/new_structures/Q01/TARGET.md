# Q01 formal target

Given a canonical base-10 integer seed n0 and the exact step R(n)=n+rev10(n), find q0>=1, p>=1, k>=1, g>=1, fixed finite B,C and period-m word W (or phase-indexed B_t,C_t,W_t), plus a finite complete edge checker E, such that:
1. pairs10(digits10(n0))=T_0(q0);
2. for every q>=q0 and every 0<=t<k, E proves R's pairword step T_t(q+offset_t) -> T_(t+1)(q+offset_(t+1)) with actual digit carries, true overflows and a concrete nonpalindrome witness;
3. T_k(q)=T_0(q+g) *as complete canonical pairwords*, with each intermediate source length above E's pumping guard.
These conditions prove for all j>=0, t<k that R^(jk+t)(n0) is nonpalindromic, hence n0 is a decimal Lychrel number.

Q01's proved necessary spec for the fixed-centre paired version is k=p*r and r*S=2*m*g, with g>0 and the two mod-9 coefficient-mass congruences in docs/CERT_SPEC_Q01.md. None of these necessities by itself supplies condition 2 or a concrete decimal n0.
