# Agent 2 / T2.p21.k7: exhaustive all-width B-cycles for one period and overflow count

Status: **COMPUTED** (plus the established PAPER PROOF of first-head necessary overapproximation). Not LEAN-VERIFIED; no decimal Lychrel certificate. Coordination issue #289. Distinct from period-16 Draft PR #309; Agent 4's period 21–24 claim is restricted to six overflows, not these seven.

## Statement

In decimal base, no neutral-band exterior B-cycle exists with exactly P=21 steps and exactly k=7 overflow steps, under the exact positional B automaton of calculation/neutral_band/structure/bauto.cpp, for any exterior B width. The result does not restrict any other (P,k), does not rule out a center C-cycle independently, and does not settle the existence of a decimal Lychrel number.

## Method, completeness, results

The necessary first-head graph allows x=1,...,18 and an arbitrary incoming reverse carry h∈{0,1}. The recurrence is x'=2x+h when g=0 and x+h<10; x'=(x mod10)+1 when g=1 and x+h>=10. Every actual B-cycle projects to a path in this enlarged graph. Cyclic time shifts of g give equivalent existence questions, so considering the lexicographically smallest rotation of each binary overflow word suffices.

For P=21, k=7 there are exactly **5,538** distinct cyclic binary words (necklaces), of which **145** support a cyclic first-head path. All 145 were passed into the existing width-unbounded exact position automaton with 100,000-state cap per word. Every case **EXHAUSTED**, none reached the cap, and none yielded ACCEPT. The largest exact C++ state set has 36,029 states (word g=000100011000100100011); the largest depth observed is 10. A separately authored pure-Python positional BFS independently exhausts that hardest word at precisely 36,029 states and depth 10, zero accepts.

In a B positional automaton, each level chooses a column for all 21 time indices, tracking normalizing carries and overflow-partner digits. A finite exhaustive set of reachable positional boundary states without the accepting neutral boundary means that no finite exterior length can realize the fixed g stream. Because the head filter does not reject any realizable B-cycle and all survivors are exhausted, the scoped negative is complete in this model.

## Reproduction

Compile the unchanged repository B automaton in a repository checkout:

    g++ -O2 -std=c++17 calculation/neutral_band/structure/bauto.cpp -o /tmp/p196-bauto
    python3 calculation/agent-2/p21_weight7.py --bauto /tmp/p196-bauto --cap 100000 --timeout 20

Expected summary:

    P=21 weight=7 necklaces 5538 first-head survivors 145
    EXACT B RESULT {'EXHAUSTED': 145, 'ACCEPT': 0, 'UNDECIDED': 0}

Independent hardest-case Python check (from the separate scoped period-16 research PR #309, or its review-only issue #294):

    python3 calculation/agent-2/bauto_py.py 000100011000100100011
    # RESULT EXHAUSTED depth 10 states 36029 accepted 0

The p21_weight7.py runner uses only the standard library, the existing upstream exact C++ program and explicit subprocess limits; a cap/time limit produces UNDECIDED and terminates with nonzero status, never a false negative. Positive p11/p12 control streams were reproduced by the separate independently implemented B solver in #294.

This result is COMPUTED and externally needs an independent second-agent full-scope reproduction before being treated as reviewed. No Lean theorem was added; full project python3 tools/verify.py --changed was not run. **UNVERIFIED / DO NOT MERGE.**
