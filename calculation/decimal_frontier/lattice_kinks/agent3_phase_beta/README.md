# Agent3PhaseBetaNoGo: standalone reproduction

Two independent Python 3 standard-library implementations plus the exact 1.95 KB rec2 lattice snapshot are included. From repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_phase_beta/witness.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_phase_beta/independent_check.py
```

The first checker uses integer cyclic carry recurrences, tests all seven explicit perturbation equations, all eight rec2 row transitions and every admissible one-site perturbation for positive controls M=3,9,11,33,99. The second uses cyclic digit normalization, independently reconstructs carry arrays and perturbation coefficients, and checks 2,400 random cyclic bulk updates. No external dependencies, memory caps or uncommitted data.

Expected primary output:

```text
PASS: 8 phases, 4 stable-site witnesses, 3 defect witnesses, 3/9/11/33/99 complete controls
CERTIFICATE: 11(b1-b0)=0; 2(b2-b1)=0; 11(b3-b2)=0; 2(b4-b3)=0
CERTIFICATE: (10^47+1)b1-11*10^47*b0=0
CERTIFICATE: 11*10^5(b3-b2)+10^4*a34=0
CERTIFICATE: -79*10^4*b4-2*10^5*b3-2*10^4*a34=0
CONCLUSION: M|(10^48-1), M|99*10^4, gcd=99; beta0=1 => M|99
```

Expected independent output:
`INDEPENDENT PASS: digit-normalized 7 perturbation witnesses and 2400 random cyclic bulk updates`

This classifies a specified cyclic-bulk covariance ansatz, not real-centre dynamics or decimal Lychrel existence.
