# Agent 4 / T2.p23, seven overflows: all-width B-cycle census

**COMPUTED scoped negative, not Lean-verified.** Parent source PR #323, coordination issue #289. No decimal Lychrel certificate is claimed.

The sound 18-state first-coordinate necessary graph in the parent T2 report filters 10,659 rotation-inequivalent binary overflow words (period p=23, precisely seven ones) to **64**.

The exact all-width B position automaton checks each of these 64 survivors with a 2,000,000-state and depth-100 cap. **All 64 EXHAUSTED**, zero ACCEPT, CAPPED or TIMEOUT. Maximum 62,497 states, depth 9, for g=11100010001000100010000. At p=23 with seven overflows, 2*p+4*sum(g)=74, within the 128-bit key guard.

**Reproduction (after building C++ executables from #323):**

    c++ -std=c++17 -O2 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
    c++ -std=c++17 -O2 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
    python3 calculation/agent-4/run_p23_g7.py

Expected output:

    candidate_necklaces=64
    status_counts= {'EXHAUSTED-NO-B-CYCLE': 64}
    max_states_word= (62497, '11100010001000100010000', 9)
    COMPUTED p23 weight7: all 64 full-B searches exhausted

This excludes only the precise p23 seven-overflow B-cycle scope, not p23 at other weights, other periods, centers, base-10 neutral certificates, or decimal Lychrel existence. Established p11/p12 B-cycle positive controls pass the exact solver in the parent PR.

**UNVERIFIED / DO NOT MERGE.** No Lean result, no verification-script PASS and no second-agent independent negative reproduction claimed. This PR is stacked onto #323 and requires its source programs.
