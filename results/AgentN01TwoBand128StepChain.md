# AgentN01TwoBand128StepChain
**COMPUTED:** a decimal, period-20/period-48 locked two-band family has an exact 128-step nonpalindromic reverse-and-add chain for EVERY k>=12, not only sampled lengths.
The two-band pairword shape is preserved in all 129 states, with source integer N_k=val_10(P_k) from the earlier AgentN01LockedTwoBandDiagonal result.
Each of 128 temporal edges is certified with the full 80-state two-ended carry matrices and synchronized parameter powers (joint preperiod 1 and period 1).
Independent ordinary Python-bigint reverse-and-add at k=20 confirms every template, every addition and palindrome avoidance.
The fixed junction width is 616; the finite centre suffix grows from 80 to 112, so this is NOT a temporal cycle and NOT a decimal Lychrel proof.
Reproduce: `python3 calculation/new_structures/agent-N01/chain128.py`.
Files: calculation/new_structures/agent-N01/chain128.py, calculation/new_structures/agent-N01/chain128_expected.json, reports/AgentN01TwoBand128StepChain.md.
