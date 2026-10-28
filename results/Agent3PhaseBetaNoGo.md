# Agent3PhaseBetaNoGo

**PAPER PROOF.** The decimal p8/m48 rec2 cyclic bulk admits a normalized time-phase-varying pair-weight and descending-carry correction
`C_t(P)=sum_(j=0..47)10^j(beta_t P_j+alpha_(t,j)d_j(P)) (mod M)`, `beta_0=1`,
satisfying `C_(t+1)(F_(g_t)(P))=(11 if g_t=1 else 2)C_t(P)` on all eight rec2 rows and every admissible one-site ±1 perturbation **if and only if M divides 99**.
This allows seven independent pair-weight multipliers and 384 independent time-phase/spatial descending-carry coefficients, extending the fixed-pair-weight result 3486df7d.
Seven exact perturbation equations force `M|(10^48-1)` and `M|(99*10^4)`; their gcd is 99, and `beta_t=1, alpha_(t,j)=0` works for all divisors.
**Scope:** cyclic bulk and this local covariance ansatz only. Not a centre no-go, nonlocal/nonlinear invariant exclusion, base-10 certificate, or Lean-verified claim.
Proof: `reports/Agent3PhaseBetaNoGo.md`.
Independent reproduction and controls: `calculation/decimal_frontier/lattice_kinks/agent3_phase_beta/README.md`.
