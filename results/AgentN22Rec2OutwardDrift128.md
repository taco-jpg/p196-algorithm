# AgentN22Rec2OutwardDrift128
- Label: **COMPUTED**.
- New positive decimal mechanism: a rec2 spatial-m48 centre seam whose lattice frontier stays at least 2 sites *outward* at every eight-step clock checkpoint 8..128, reaching +7 at step128. The centre itself grows, not a stationary or one-step kink.
- Exact base-10 seed: even palindromic pairword `H ++ reverse(H)`, `H=B0 ++ W0^100 ++ tail80.csv`; canonical high/low decimal digit split defined in report. Initial 9,782 digits.
- Independent **20,000-step** ordinary digit-array and GMP big-integer reverse-and-add replays: all nonpalindromic, all 8-phase rooted B11 and W128 prefixes, all overflow bits, 19 checkpoints of full-number equality. Minimum rec2 match: 1,913 coefficients.
- Outward drift is transient, not a certificate: frontier returns to baseline t176, becomes negative t184, reaches -119 at t1000; B11 itself first fails t33166. No unbounded Lychrel claim, no claim about 196, no Lean theorem.
- Reproduce: `bash calculation/new_structures/agent-N22/run_outward.sh`. Exact tail/source/independent checkers/controls: `calculation/new_structures/agent-N22/{tail80.csv,outward_digits.cpp,outward_gmp.cpp,front_probe.cpp,front_optim.cpp,outward_stats.csv,run_outward.sh}` (shared B.csv,rows.csv from N22 earlier commit).
- Full report: `reports/AgentN22Rec2OutwardDrift128.md`.
