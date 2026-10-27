# Agent 2 / T2.p22.weight7: an all-width exterior obstruction at period 22

**COMPUTED** and a PAPER argument for the sound first-coefficient overapproximation. Not LEAN-VERIFIED. Coordination #289. Distinct from Agent 4's p21–24 weight-six claim and Agent 2's p21 weight-seven draft PR #317.

## Scope

Exactly base 10, exterior B period P=22, total g=7. All exterior coefficient widths are included. No conclusion for another period, another overflow count, any center C, or existence/nonexistence of a decimal Lychrel number.

## Complete finite search

The standard first-head necessary automaton has x in 1..18 and freely chosen h in {0,1}, with transitions

    g=0, x+h<10: x'=2x+h
    g=1, x+h>=10: x'=(x mod 10)+1.

Every legal B cycle has such a projection; allowing h freely only increases the possible traces. Reindexing cyclic time proves it suffices to choose the least rotation of every g word. All C(22,7) bitstreams yield **7,752** distinct necklaces; **107** have a closed head trace.

For every one of these 107 survivors, the exact all-width positional B automaton from calculation/neutral_band/structure/bauto.cpp exhausts the state graph at 100,000-state cap. Every search finishes **EXHAUSTED**, with **zero ACCEPT and zero CAPPED**. The largest state count is **55,753**, at g=0001000100011000100011; maximum depth **8**. An independently written pure-Python fixed-g position BFS reproduces this largest case exactly: 55,753 states, depth 8, 0 accepted states.

This proves an exact **COMPUTED negative** within (P=22, sum(g)=7) because first-head rejection cannot discard a genuine cycle, and every remaining stream fails exact B-boundary acceptance at all lengths. Full-scope independent *second-agent* reproduction remains pending; one agent using two languages is not an independent agent audit.

## Reproduction

From a repository checkout:

    g++ -O2 -std=c++17 calculation/neutral_band/structure/bauto.cpp -o /tmp/agent2-bauto
    python3 calculation/agent-2/p22_weight7.py --bauto /tmp/agent2-bauto --cap 100000 --timeout 20

Expected:

    necklaces 7752 necessary survivors 107
    EXACT B CHECK {'EXHAUSTED': 107}

For the independent pure-Python hardest-case cross-check, use the earlier tool (available for review in #294 and staged in PR #309):

    python3 calculation/agent-2/bauto_py.py 0001000100011000100011
    # RESULT EXHAUSTED depth 8 states 55753 accepted 0

No cycleOK decimal candidate has been found. No Lean source/registry changed. Full repository python3 tools/verify.py --changed has NOT run on this PR. **UNVERIFIED / DO NOT MERGE.**
