# AgentX01TwoBankNearNeutralRelay
**COMPUTED:** A new 6-step decimal two-band resource relay with folded pairword H_0(k)=[9]++14^k++[5,5]++4^k++[13]; full pairword H_0++reverse(H_0), realized by an explicit positive decimal seed.
For k=30,80,200,1000, exact six-step pairword evolution has (14,4) bulk lengths (k,k)->(k-1,k), versus N19's original 8/16 example (k,k)->(k-5,k-2). One reservoir loses only one cell; the other loses zero.
The improvement is NOT a renewable cycle: by step 12, the two widths are (k-6,k-3), and their centre/exteriors have changed; k=200 loses its left macroscopic 14 run by step 480.
Independent Python arbitrary-precision integer reverse-and-add checks the *entire pairword* and nonpalindromicity at every t through 90,240,500,500 steps respectively; each trajectory retains at least one odd pair coefficient.
Reproduce: python3 calculation/new_structures/agent-X01/relay_six.py. Data: calculation/new_structures/agent-X01/relay_six.json.
Scope and limits: reports/AgentX01TwoBankNearNeutralRelay.md. Not an infinite Lychrel certificate, no Lean proof, and no all-k universal assertion.
