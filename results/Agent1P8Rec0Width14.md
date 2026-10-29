# Agent1P8Rec0Width14

**COMPUTED.** For decimal overflow `10101010`, the period-8 rec0 lattice
(spatial period m=20) has no indefinitely surviving centre with lower-half
free window of width 14 for any initial n0=400+o, o=0,1,2,3.
The exact one-hot horizon-SAT checks are UNSAT at horizons
(H0,H1,H2,H3)=(80,72,76,80), without a state cap.
These are sufficient bounds, not necessarily minimal. Any periodic centre
would survive arbitrarily long, so all temporal periods are excluded.
Reproduce from repository root:
`bash calculation/decimal_frontier/lattice_kinks/code/agent1_width14_controls.sh`
Same-commit source and independent checker: `calculation/decimal_frontier/lattice_kinks/code/agent1_width14_*.py`,
`calculation/decimal_frontier/lattice_kinks/code/agent1_independent_replay.py`;
case data: `calculation/decimal_frontier/lattice_kinks/data/agent1_width14_cases.json`.
Not claimed: widths >=15, other exteriors, decimal certificate, or 196.
