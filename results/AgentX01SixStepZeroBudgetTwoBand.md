# AgentX01SixStepZeroBudgetTwoBand
**COMPUTED:** New decimal six-edge ZERO-DEFECT-BUDGET joint for two distinct absorbing pair bands. Folded LSD-first P0(k)=[9]++14^k++[5,5,5]++4^k++[13], with full pairword H++reverse(H) and an explicit positive decimal realization.
At k=30,80,200,1000, both canonical bulk lengths return exactly (k,k)->(k,k) after 6 genuine reverse-add steps, with no palindrome in ANY checked state. This improves the previous X01 two-cell joint's (-1,0) loss and N19's (-5,-2).
COMPUTED 19^3 three-cell junction enumeration at k=50 (fixed x=14,y=4 and exterior 9/13): 6744 phase-valid bridges; 4 preserve both full band lengths after six steps: 555, 55(14), 5(14)5, 5(14)(14).
**Not a certificate:** at t=12, lengths=(k-5,k-3); the exterior/junction do not return even though the two bulk lengths do at t=6.
Independent Python BIGINT arithmetic checks the entire pairword, odd witnesses and palindrome test through 90/240/500/500 steps for k=30/80/200/1000.
Reproduce: python3 calculation/new_structures/agent-X01/scan_3core.py && python3 calculation/new_structures/agent-X01/relay3.py.
Data/code: calculation/new_structures/agent-X01/relay3.json and the two Python scripts; report: reports/AgentX01SixStepZeroBudgetTwoBand.md. No Lean verification or infinite Lychrel claim.
