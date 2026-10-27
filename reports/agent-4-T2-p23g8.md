# Agent 4: exact p23 eight-overflow exterior B-cycle census

**COMPUTED, not Lean-verified.** Coordination #289, foundational parent PR #323.

For base 10, period p=23 with exactly 8 overflow bits, the necessary low-digit automaton of parent #323 admits **463** rotation-inequivalent binary words. The exact full B position automaton in that parent was run on each word with 2-million-state, 100-depth caps and a seven-second per-word timeout.

All **463/463 EXHAUSTED** with zero ACCEPT, caps or timeouts. The largest graph visited 252,273 states, depth 8, for g=10101001010001000110000. The actual bounded batch terminated below the overall 45-second limit.

Reproduction after building both C++ executables from #323:

    c++ -O2 -std=c++17 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
    c++ -O2 -std=c++17 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
    python3 calculation/agent-4/run_p23_g8.py

Expected:

    candidate_necklaces= 463
    status_counts= {'EXHAUSTED-NO-B-CYCLE': 463}
    max_states_word= (252273, '10101001010001000110000', 8)
    COMPUTED p23 weight8: all 463 B-position searches exhausted

This is an exact finite COMPUTED negative for this period/weight, not all p23, not arbitrary periods, and not proof of a decimal Lychrel number. Existing B cycles at other periods and center nonexistence remain separate questions. Another agent's independent negative reproduction is pending.

**DRAFT / UNVERIFIED / DO NOT MERGE.** Current PR has no Lean modules, no verified tool/Lean build, and depends on foundational #323.
