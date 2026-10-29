# Q01 formal target

## Original certificate-spec target

Given a canonical base-10 seed n0 and R(n)=n+rev10(n), find q0,p,k,g, fixed finite B,C and period-m W (or phase-indexed blocks), plus a finite complete edge checker E, such that the exact template transitions hold for all q>=q0, every ordinary intermediate state is nonpalindromic, and the complete cycle returns to the same finite state with positive band growth g>0. The fixed-centre necessary gates are k=p*r, r*S=2*m*g for paired bands (or r*S=m*g for merged bands), plus the mod-9 coefficient-mass congruences in docs/CERT_SPEC_Q01.md. These necessities do not produce a seed or physical repair.

## Current T* target

For the rooted p12/m9 template P=H C reverse(H), H=B W^q J U^k, prove or refute whether the **steady interior carry path can be reflection-symmetric** for any of the 30 charge-zero U3 rows. Exact target now established in reports/Q01TStarCarrySymmetry.md: for every U, all q, k>=3 and every legal finite J,C, actual mirrored interior carries obey c_i+c_(|P|-i)=1 on copies 1..k-2. Thus equal-carry reflection is impossible in the protected bulk. The remaining T* gap is still a genuinely physical phase-changing or fixed-state seam/centre return with positive resource drift, canonical seed, true carries/overflows, and a nonpalindrome witness at every ordinary step.
