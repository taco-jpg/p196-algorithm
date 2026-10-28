# Agent3TimeVaryCarryNoGo
**PAPER PROOF.** For the decimal p8/m48 rec2 cyclic row map, permit **384 independent** descending-carry correction coefficients alpha_(t,j), for every time phase t mod 8 and spatial cell j mod 48, in C_t(P)=sum 10^j(P_j+alpha_(t,j)d_j(P)) modulo arbitrary M>=2.
Require exact C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2)C_t(P) on the eight reference rec2 rows and every admissible one-site ±1 perturbation. Such a family exists **if and only if M divides 99**, where alpha=0 works.
Exact three-perturbation witness: phase0 cell47+1 yields bare 1-10^48 and no alpha terms; 2*(phase2 cell5+1)+(phase3 cell5+1) yields bare -99*10^4 and no alpha terms. Their gcd is 99.
Scope: time-dependent but *fixed 10^j weights*, cyclic bulk covariance only. Not a physical centre obstruction, not a decimal Lychrel certificate and not Lean verified.
Proof: reports/Agent3TimeVaryCarryNoGo.md.
Data, reproducible code, independent digit-normalization checker and exact commands: calculation/decimal_frontier/lattice_kinks/agent3_timevary_carry/README.md.
