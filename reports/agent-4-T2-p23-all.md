# Agent 4: complete period-23 exterior B census in base 10

**Status: PAPER PROOF (necessary projection) + COMPUTED (exhaustive finite census).**
**NOT LEAN-VERIFIED / NO DECIMAL CERTIFICATE.** Coordination issue #289, T2.
Dependencies: first-coordinate necessary filter and exact 128-bit full-width B position automaton in the agent-4 core source PR #323; previous component reports in PRs #327 (p23/g7), #331 (p23/g8), #333 (p23/g9), and review issue #314 (p23/g6).

## Scope and mathematical reduction

In the existing Agent120 one-neutral-band checker, accepted edges satisfy e2=1-e1. The exterior B evolves autonomously and yields an overflow bit g each step. For the first coefficient x of B, allowing effective x=9 when B is empty, there exists a carry c in {0,1} such that

- g=0: x+c<10 and x'=2*x+c;
- g=1: x+c>=10 and x'=(x mod 10)+1.

The proof that every actual B return produces a closed word in this 18-vertex over-approximation (including arbitrary legal trailing-9 trims) is in the parent report `reports/agent-4-T2.md`. The converse is false: a surviving overflow stream requires further exact full-width B checks.

There are exactly **364,724** binary necklaces at temporal period 23 (23 is prime); the 18-state prefilter permits exactly **1,502**. All counts here are rotation-equivalence classes, not labelled unquotiented sequences.

| Overflow weight Σg | Pass necessary filter | Exact full-B solver result |
|---:|---:|---|
| 6 | 1 | EXHAUSTED / 0 ACCEPT |
| 7 | 64 | EXHAUSTED / 0 ACCEPT |
| 8 | 463 | EXHAUSTED / 0 ACCEPT |
| 9 | 731 | EXHAUSTED / 0 ACCEPT |
| 10 | 239 | EXHAUSTED / 0 ACCEPT |
| 11 | 4 | EXHAUSTED / 0 ACCEPT |
| all other weights | 0 | rejected by necessary projection |

The exact fixed-g positional automaton, specialized from the existing repository's B automaton, ranges over *all* B lengths via its interface state (L,H,Y), so an exhausted fixed-g graph rules out all B returns for that stream, not merely a small initial-width census. The packed state has 2*23+4*Σg<=90 bits for all remaining streams and is stored in 128 bits with a guard.

**Exceptional hard word:** `g=10101010101001001110000` (weight 10) was initially TIMEOUT after five seconds. At 2M cap it was CAPPED after 2,029,417 states/depth 24. A subsequent 10,000,000-state isolated run reached an actual **EXHAUSTED-NO-B-CYCLE** terminal output at **8,455,917** visited states/depth **65**. Both initial limits were correctly labelled UNDECIDED until that terminal output, not negative evidence. The other 1,501 streams exhausted under 2M states each.

## Reproduction

Recompile and first run positive controls from the *current* parent source:

    c++ -std=c++17 -O2 calculation/agent-4/low_digit_automaton.cpp -o calculation/agent-4/low_digit_automaton
    c++ -std=c++17 -O2 calculation/agent-4/fixed_g_B_probe.cpp -o calculation/agent-4/fixed_g_B_probe
    python3 calculation/agent-4/test_low_digit.py
    calculation/agent-4/fixed_g_B_probe 11100010000 2000000 110
    calculation/agent-4/fixed_g_B_probe 100010001000 2000000 110
    python3 calculation/agent-4/run_p23_all.py

The first regression previously compared 130,320 full-B projected updates with independent arithmetic (zero mismatches); documented p11 and p12 positive exterior cycles are accepted at depth 29 and 53, respectively.

Expected all-p23 terminal conditions:

    period=23 initial_binary_necklaces=364724
    necessary_survivors= 1502 weight_counts= {6: 1, 7: 64, 8: 463, 9: 731, 10: 239, 11: 4}
    status_counts= {'EXHAUSTED-NO-B-CYCLE': 1502}
    largest= (8455917, '10101010101001001110000', 65)
    COMPLETE_COMPUTED_P23_NO_B= True

The runner uses 10M states and 90s per-word timeout for the exceptional word, 2M states/5s for all others, and a global 130s guard. Any timeout, bad exit status, depth/state cap, non-executed word, or accepting stream makes the runner print a non-negative-inference status and exit nonzero. The whole batch must finish for the claimed exact computed negative.

## Exactly what is and is not established

**COMPUTED:** the p=23 exhaustive finite automaton census has no exterior B-cycle at any width. Consequently no base-10 one-neutral-band `cycleOK` certificate with 23 exterior edges exists *within the established exact checker model*. This is NOT an all-period impossibility theorem and says nothing about base10 full orbit 196 specifically.

A full decimal existence proof still needs the matching center, complete certificate edges, Python mirror replay, Lean theorem `cycleOK 10 ... = true := by decide`, and `verify.py --changed`. None are provided here. The p23 negative requires an *independent second agent's algorithmic corroboration*, since all present p23 subsets share one author's B solver. There are no new Lean modules; no repo-wide verification PASS claimed.

**DRAFT / UNVERIFIED / DO NOT MERGE**, stacked on core #323 and separate from its mathematical proof source. No RESULTS.md, README.md or other agents' files edited.
