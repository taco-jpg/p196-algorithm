# AgentN14ClockLift
**COMPUTED.** Exact rooted base-10, primitive overflow period 72, width-five temporal carry strip; independently checked 72/72 ordinary-integer single-step outer-column updates.
**COMPUTED.** Its freely driven sixth column becomes impossible at step 10 (exact 19-state propagation); a genuine integer seed 110102959969697 tracks its first five columns for t=0..9 and deviates at t=10.
**COMPUTED.** Independent ordinary decimal digit-vector replay of this seed: steps 0..20000 nonpalindromic, final length 8279 digits. **Not a certificate:** claimed column periodicity stops at t=10.
**COMPUTED control.** A non-rooted decimal cut with g=01, L=(1,0), H=(1,1), Y=(-1,8) has minimum clock lift 2, witnessed by new-column coefficients (17,16,14,9); this does NOT imply root reachability.
**UNDECIDED:** decimal Lychrel existence, a coherent central seam, and any permanently valid width-five candidate.
Reproduce with \`python3 calculation/new_structures/agent-N14/generate.py\`, \`python3 calculation/new_structures/agent-N14/independent_check.py\`, \`python3 calculation/new_structures/agent-N14/transfer.py\`, and \`g++ -O3 -std=c++17 calculation/new_structures/agent-N14/replay20k.cpp -o /tmp/n14-replay && /tmp/n14-replay 110102959969697 20000\`.
Soundness statement, precise limitations, and lifting proof: \`reports/AgentN14ClockLift.md\`.
