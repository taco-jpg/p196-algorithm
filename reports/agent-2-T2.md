# Agent 2 / T2: width-unbounded exterior B obstruction at period 16

**Status:** PAPER PROOF and COMPUTED, **not LEAN-VERIFIED**. Research coordination #289, full review source #294.

## Exact scope and result

Any base-10 exterior B-cycle with P time steps and k overflow steps must have P <= 4k (PAPER PROOF), and equality forces overflow stream (1000)^k up to rotation. This is independent of exterior width and center.

For P=16, all possible g streams except the alternating eight-overflow word g=0101010101010101 are excluded by the first-head necessary automaton together with exhaustive exact B positional enumerations. That remaining word is **UNDECIDED**, having exceeded 250,000, 1,000,000 and 4,000,000 states; a Studio request in #289 asks for a higher capped run.

Nothing here supplies a decimal certificate or claims a cycleOK 10 witness.

## Proof of the P <= 4k bound (PAPER PROOF)

Use x=B[0], or x=9 when B is empty, which is the neutral-padding convention for this exterior dynamics. In a legal edge let h be the last reverse-normalization incoming carry (h=0 or 1). The exact first-coefficient transition satisfies

* no overflow g=0: x+h<10 and x'=2x+h;
* overflow g=1: x+h>=10 and x'=(x mod 10)+1.

After an overflow 1<=x<=10. Allowing h to be chosen freely yields a *necessary overapproximation*, so rejection by this graph is sound. A segment starting just after an overflow, taking zero or more g=0 steps and then one g=1 step, has length ell satisfying

    ell <= 4 + [x=1] - [y=1]

where y is the following post-overflow value. This follows by finite direct enumeration of x=1..10 and the two carry choices, recorded by calculation/agent-2/four_overflow.py.

For k cyclic overflow segments, the potential terms telescope, giving P <= 4k. When equality holds, only the tight-edge recurrent vertex x=1 survives. Its unique cyclic tight segment has length four, hence precisely three g=0 steps followed by one g=1, i.e. (1000)^k up to rotation. These are necessary conditions only, not a construction.

## Exhaustive P=16 results (COMPUTED)

| sum(g) | Binary necklaces | Necessary head survivors | Exact B conclusion |
| --- | ---: | ---: | --- |
| 0–3 | various | irrelevant | impossible by P<=4k |
| 4 | 116 | 1 | EXHAUSTED, 0 accepts; 13,170 maximum states |
| 5 | 273 | 14 | all EXHAUSTED, 0 accepts; max 1,885 |
| 6 | 504 | 54 | all EXHAUSTED, 0 accepts; max 144,899 |
| 7 | 715 | 25 | all EXHAUSTED, 0 accepts; max 80,865 |
| 8 | 810 | 1 | alternating word only: CAPPED, UNDECIDED |
| 9–16 | various | 0 | no first-head-compatible cyclic stream |

The necessary-head enumeration covers every binary word via cyclic rotation. The subsequent position automaton is the all-width column-transfer model documented in calculation/neutral_band/structure/bauto.cpp: its states hold the forward and reverse carry masks L,H and overflow-partner digits Y. It accepts only when the eventual neutral boundary constraints L_t+H_t=1 and Y_t=9 L_t hold. A completely exhausted state graph with zero accepting boundaries is a COMPUTED all-width negative for the given g.

Two independent languages/implementations written by Agent 2 agreed on every nontrivial p16 search, including the 144,899-state and 80,865-state cases. More importantly, **Agent 4 independently implemented the positional B automaton and replicated weights 5–7**, with the same maximal state counts, as described in #289 and review issues #298 and #300. This is independent second-agent corroboration for those bounded negatives, not Lean verification.

Positive controls on the same positional model reproduce the known p=11 (one e stream) and p=12 (three e streams) base-10 exterior cycles from the neutral-band README.

## Reproduction

Standard library Python; execution of every finite instance terminates or raises if it fails its 300-second limit. In repo root:

    python3 calculation/agent-2/four_overflow.py
    python3 calculation/agent-2/p16_census.py
    python3 calculation/agent-2/p16_census.py 4 5 6 7 --check
    python3 calculation/agent-2/bauto_py.py 1000100010001000

The all-width Python enumerator is independently derived from the coefficient/carry recurrence, not an import of the existing C++ source. The --check mode intentionally does not claim the k=8 negative: any unfinished/capped run remains UNDECIDED. All local sample controls and exhaustive k=4..7 runs had zero accepts.

No Lean theorem file changed; no cycleOK certificate discovered; python3 tools/verify.py --changed has **not** been executed on this PR in a full repo checkout. **UNVERIFIED / DO NOT MERGE** pending project verification and reviewer sign-off.
