# AgentN25FirewallRecharge
Label: COMPUTED.
Claim: Three protected decimal zero sectors exhibit measurable *paired* boundary replenishment credits, not just passive worst-case erosion.
Scope: Seed `1789 0^40001 3141 0^40001 5926 0^40001 5358`, times `0..20000`. This is NOT an infinite Lychrel certificate.
Exact paper identity: maximal reflection-matched zero width `w_t=g-2t+G_t+E_t`, with `E_t` nondecreasing; increment `r_t=w_{t+1}-w_t+2-gamma_t >=0`.
Computed at t=20000: `G=8227`, `E_outer=19753`, `E_centre=19804`; actual matched widths 27981 and 28032, instead of the 8228 passive bound. Neither matched wall grows in an individual step.
Replenishment rates per step ~0.988 and ~0.990; needed average to avoid contraction ~1.589, so regeneration is insufficient in this seed.
Positive mechanism: boundary normalization prevents nearly 20,000 worst-case zero-cell losses on each joint pair, but the wall still contracts ~0.6 positions/step.
Reproduce: `python3 calculation/new_structures/agent-N25/run_recharge.py` (full independent 20k replay plus Python big-integer witness).
Code and data: `calculation/new_structures/agent-N25/{safe_scan.cpp,regen_check.py,run_recharge.py,recharge.json}`; first N25 result contains two independent arithmetic kernels.
Derivation and constructive next-step criterion: `reports/AgentN25FirewallRecharge.md`.
