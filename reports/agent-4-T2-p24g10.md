# Agent 4 / T2: base-10 period 24, ten overflows (PARTIAL)

**COMPUTED / PARTIALLY EXHAUSTED. NOT LEAN-VERIFIED.** Coordination: #289. Depends on parent PR #323's necessary first-digit graph and exact 128-bit fixed-g exterior B positional automaton. Unlike the complete period-23 census in PR #342, this p24 weight10 search has **TWO UNRESOLVED** streams. Do not report a complete negative.

There are exactly 81,752 rotation-inequivalent binary overflow words of period 24 containing ten ones. The PAPER-proven necessary 18-state first-digit overapproximation leaves **685**. A fixed-g exact all-width B position automaton with a two-million-state cap and five-second per-stream timeout gave:

- 683 streams EXHAUSTED-NO-B-CYCLE, with no accepting exterior interface.
- g=101010100111000110001000: TIMEOUT at 5 seconds, then CAPPED-UNDECIDED at 10,741,237 visited states / depth 20 (ten-million-state cap), wall 57.42 seconds, 801,232 KB maximum RSS.
- g=101010101001001010100100: TIMEOUT at 5 seconds, then CAPPED-UNDECIDED at 10,531,201 visited states / depth 20, wall 59.07 seconds, 788,640 KB maximum RSS.

The 685-word batch completed in 20.79 seconds. The packed positional key uses 2*24+4*10=88 bits, within the 128-bit storage guard.

**Reproduce from a working tree containing parent PR #323:**

    c++ -std=c++17 -O2 calculation/agent-4/low_digit_automaton.cpp -o calculation/agent-4/low_digit_automaton
    c++ -std=c++17 -O2 calculation/agent-4/fixed_g_B_probe.cpp -o calculation/agent-4/fixed_g_B_probe
    python3 calculation/agent-4/run_p24_g10.py
    calculation/agent-4/fixed_g_B_probe 101010100111000110001000 10000000 120
    calculation/agent-4/fixed_g_B_probe 101010101001001010100100 10000000 120

The Python batch exits nonzero while the two words are unresolved. The isolated 10M cap commands return code 3 / CAPPED. The unchanged solver separately ACCEPTs known period-11 g=11100010000 and period-12 g=100010001000 B cycles as positive controls.

**STUDIO REQUEST already posted to issue #289:** two SERIAL 40-million-state jobs with per-job ceilings of 20 minutes and 8 GB resident RAM, requiring exact terminal statuses, depth/states, elapsed time and peak RSS. No claim that these Studio jobs have executed.

**Not established:** neither full p24/weight10 B nonexistence nor decimal Lychrel existence; no matching center C-cycle, global one-band impossibility, Lean proof or full repository verification. The p24 weight6 known nonprimitive repeated p12 B-only return is unaffected. Independent second-agent review of the 683 bounded negative cases is still needed.

**DRAFT / UNVERIFIED / DO NOT MERGE.** Preserve UNDECIDED on the two capped words.
