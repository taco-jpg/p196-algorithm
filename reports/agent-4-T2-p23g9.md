# Agent 4 / T2.p23 with nine exterior overflows

**COMPUTED finite negative. NOT LEAN-VERIFIED.** Coordination: #289. This report is stacked on the first-coordinate and full-B automaton source PR #323.

In base 10, exactly 35,530 binary cyclic necklaces have period 23 and nine overflow bits. The sound width-independent 18-state low-digit necessary filter from parent PR #323 leaves precisely **731** stream candidates. The corrected 128-bit exact full-width B position automaton from that PR was run for each surviving word, under a two-million-state cap, depth cap 100, and five-second per-word timeout. **All 731 searches EXHAUSTED** with no ACCEPT, CAPPED, TIMEOUT or NOT_RUN. Largest visited graph: **43,897 states**, depth **6**, g=`10101000101010010110000`. Local batch wall time was 2.738 seconds (run-to-run timings vary). Keys for this scope require 2*23+4*9=82 bits, safely within 128-bit guard.

Freshly recompiled positive controls on the same C++ source reproduce p11 ACCEPT (e=10100110011, depth29) and p12 ACCEPT (e=100101011010, depth53). The independently implemented first-coordinate regression has 130,320 full-B projection checks and all necklaces through p9, zero mismatches.

Reproduce from repository root after building the parent PR's two executables:

    c++ -std=c++17 -O2 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
    c++ -std=c++17 -O2 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
    python3 calculation/agent-4/run_p23_g9.py

Expected result:

    p23 weight9 candidate_necklaces= 731
    status_counts= {'EXHAUSTED-NO-B-CYCLE': 731}
    max_states_word= (43897, '10101000101010010110000', 6)
    ALL_EXHAUSTED= True

This excludes **only** p23/Σg=9 exterior B returns, with unrestricted B widths in the existing exact position automaton. Other overflow weights, C returns, decimal Lychrel existence and any global no-go are not established. This result awaits a genuinely independent second agent's reproduction; no new Lean module and no `python3 tools/verify.py --changed` PASS is asserted.

**DRAFT / UNVERIFIED / DO NOT MERGE.**
