# Agent3ScalarCarryModuli
**PAPER PROOF.** In the decimal period-8, spatial-period-48 rec2 bulk, let Q_t=sum_j 10^j W_t[j], and D_t=sum_j 10^j d_t[j], where d_t is the unique periodic descending carry on the 48-cell lattice.
For **every integer modulus M>=2**, a single phase-independent scalar alpha (mod M) satisfying Q_t+alpha D_t=0 for all eight phases exists **if and only if M divides 99**. In that case the unique alpha is 0.
Exact integer witnesses: gcd(Q_0,...,Q_7)=99; gcd(D_0,D_2)=1; gcd(Q_0 D_1-Q_1 D_0, Q_1 D_2-Q_2 D_1)=99.
Scope: only this *constant scalar, fixed 10^j-weight* bulk correction ansatz; not phase-dependent or vector corrections, physical centre dynamics, any centre-width exclusion, or a decimal Lychrel certificate.
Proof: reports/Agent3ScalarCarryModuli.md.
Reproduce and independently verify with the two scripts and rec2 snapshot in calculation/decimal_frontier/lattice_kinks/agent3_scalar_charge/README.md.
