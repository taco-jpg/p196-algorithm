# Agent14OneCarryFlipRigidity
**PAPER PROOF.** For the two reachable decimal p=8,m=20 non-self-mirror bulk cycles rec0/rec1 with g=10101010, no integer base b>=2 admits a cyclic row whose entire ascending/descending carry itinerary differs in **exactly one** of 320 binary sites from the corresponding decimal itinerary.
All 640 cases are excluded by the **first two initial coefficients alone**: necessary affine integer congruences are individually impossible or CRT-incompatible. Counts rec0: 94/56/170; rec1: 90/55/175; no caps.
**Scope:** exactly one flipped site in the fixed 8-phase × 20-column full carry itinerary, not 2+ sites, other periods/SCCs, rooted exteriors, centres, decimal Lychrel or 196. No Lean claim.
Proof: reports/Agent14OneCarryFlipRigidity.md.
Input and independent integer kernel: calculation/decimal_frontier/lattice_formats/agent14_onebit_rec0.txt, agent14_onebit_kernel.txt; source matched to existing p8_scc.txt.
Primary and independent: calculation/decimal_frontier/lattice_formats/code/agent14_onebit_main.py, agent14_onebit_independent.py.
Run both from repo root using python3; independent checker also replays ten exact pairword steps for base9 m4 |B|61 and base13 |B|75,55 controls.
