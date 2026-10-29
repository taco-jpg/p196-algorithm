# AgentN23ParametricDecimal20kBand
**COMPUTED.** ONE exact two-sided absorbing-9 digit transducer certifies the first **20,000** nonpalindromic decimal reverse-add steps for **EVERY integer Q>=6016**, seed N0(Q)=12(99)^Q34.
Source/target digits are U_t ++ 9^(L_t(Q)) ++ V_t (least significant first), with equal widths |U_t|=|V_t| and L_t(Q)=L_t(6016)+2(Q-6016).
At all 20,001 time slices L_t(6016)>=2 (final/min 2) and U_t != reverse(V_t); hence every N_t(Q) is nonpalindromic and its symmetric pair word contains central coefficient 18.
Exact 20k control: exterior width final 10,148; overflow gamma0=11,738, gamma1=8,262; symmetric 9-wall trims=9,854.
Independent decimal digit-vector and base-1e9 limb bigint replays for Q=6016 agree on all checks and final full-number checksum 788241103; the existing independent Q=7000,7001,8000 replays agree as well.
One source-level ordinary-integer random control checks 10,000 two-wall transfer instances; a PAPER derivation of transfer soundness is in the report.
Source, data and one-command reproduction: calculation/new_structures/agent-N23/ and bash calculation/new_structures/agent-N23/reproduce_parametric.sh.
Exact scope and proof: reports/AgentN23ParametricDecimal20kBand.md.
This is a UNIFORM FINITE-HORIZON certificate for a family of decimal seeds, not an infinite Lychrel proof, not Lean-verified, and makes no claim about 196.
