# Agent 4 / T2.p24 with seven exterior overflows

**COMPUTED scoped negative, not Lean-verified.** Stacked on core PR #323; coordination issue #289.

Among all 24-bit cyclic-overflow necklaces containing exactly seven ones, the sound 18-state first-coordinate necessary automaton from the parent T2 report leaves precisely **32** potential full-B cycle words. Each was checked using the 128-bit packed exact all-width B position automaton from the parent PR, with 2,000,000-state and depth-100 caps and a seven-second per-word timeout.

**All 32 EXHAUSTED, zero ACCEPT, zero caps/timeouts.** Largest case: 4,161 states at depth 2 for g=100110001000100010001000.

Reproduce after compiling the two C++ executables from #323:

    c++ -O2 -std=c++17 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
    c++ -O2 -std=c++17 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
    python3 calculation/agent-4/run_p24_g7.py

Expected:

    candidate_necklaces= 32
    statuses= {'EXHAUSTED-NO-B-CYCLE': 32}
    max_states_word= (4161, '100110001000100010001000', 2)
    COMPUTED p24 weight7: all 32 exhaustive full-B negatives

This **does not exclude period 24**: a nonprimitive B-only cycle with exactly six overflows exists by doubling the known p12 B cycle (explicit replay in #314). Other overflow counts remain unresolved; no matching center, decimal Lychrel certificate, ordinary 196 conclusion, arbitrary-period theorem or Lean proof is supplied.

**DRAFT / UNVERIFIED / DO NOT MERGE.** Needs literal tools/verify.py --changed PASS, parent PR #323 review, and independent second-agent negative check.
