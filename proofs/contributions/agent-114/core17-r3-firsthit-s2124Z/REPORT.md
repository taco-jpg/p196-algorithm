# Agent #114 / session s2124Z: core (1,7), r=3 finite first hit

**Status:** Two independent finite arithmetic paths PASS. The Lean 4.19.0 source is an **UNCOMPILED WIP**, with no formal axiom audit or independent Lean rebuild. No infinite-time claim.

## Exact problem

Reuse `DelayedOverlapGate.initial 3 1 1 7` and `L=13`, with the original `FoldedDecimal.Canonical n d 13` and exactly the thirteen finite `columnSum d 13 i` equalities. Show (eventually in Lean) `DecimalDelayBridge.FirstPositiveHit n 11` for **every** such canonical ordinary decimal integer. The original `Lychrel196.step/orbit/Palindrome` semantics are unchanged.

This rechecks a **historical observation**, not a new discovery: the original `renewal_pass/tails/STATUS.md` (blob `00f3e3fed54ee8f3823038b10289523d2a2f1aa8`) records `(1,7), r=3` as first hitting a palindrome at time 11. All other remaining `(1,7)` spacers are outside this task. The concurrent Agent #114 / PR #104 owns core `(1,6)` for r=1..4, and our scope is disjoint.

## Exact finite data

Low-to-high symmetric coefficients:

```
[1,1,0,0,1,8,14,8,1,0,0,1,1]
```

All 13-digit canonical integer realizations have one ordered digit split in the outermost pair, then 2,1,1,2,9 choices in the other half-column pairs. Their middle digit is forced to 7. Thus the number of distinct **integers** (not infinite digit functions) is exactly `1*2*1*1*2*9 = 36`.

One explicit representative is `1000007810010`; the positive orbit is independent of the selected digit split, since the original `FoldedDecimal.step_eq_word_value` states that each seed's first output equals the numerical value of the same fixed mirrored pair word.

| t | ordinary integer | palindrome |
|---:|---:|:---:|
| 0 | 1000007810010 | no |
| 1 | 1100194810011 | no |
| 2 | 2200379720022 | no |
| 3 | 4400659450044 | no |
| 4 | 8801209010088 | no |
| 5 | 17601318031176 | no |
| 6 | 84714399341847 | no |
| 7 | 159528798683595 | no |
| 8 | 754915696509546 | no |
| 9 | 1400821393029003 | no |
| 10 | 4410025324309044 | no |
| 11 | **8819059559509188** | **yes** |

Two independent computations were **actually executed**, including all 36 seed splittings and all eleven transitions. One is a standard-library Python verifier implementing (A) direct integer reverse/add and (B) the literal normalized pair-word carry recurrence, comparing every output. Another is a standalone Node.js BigInt verifier that reconstructs the 36 inputs independently, checks every positive orbit and compares the saved artifact. Both succeeded with exit code 0. The Python record is exactly regenerable byte-for-byte.

Reproduce in the directory containing the scripts:

```
python3 -B verify_core17_r3.py --check finite_evidence.json
node independent_replay.mjs finite_evidence.json
```

Author evidence SHA-256:

- `verify_core17_r3.py`: `41cad76b5608f49207ade3b08e4ca517552b5e4e214f4eeb0a11219ca1008d1c`
- `independent_replay.mjs`: `602cc257b59bee693a5044d1c74d7877b9d7c87db05d4ccac711ba42e09c1d01`
- `finite_evidence.json`: `5b1972eb1992861425d5761c5c2a87c74524d06ed74826a5611a80814ec0a3c1`, 10,811 bytes.
- `Agent114Core17R3FirstHit.wip.lean`: `a6a36c5960d87570b3195e4bf436e543f7bb0e469209253c13ea2ca855e30370`.

## Formal obligation and trust boundary

The uncompiled candidate file imports the original `DelayedOverlapGate` and proposes:

- `Agent114.Core17R3.universal_first_hit_11`: every original canonical realization has `FirstPositiveHit n 11`.
- `Agent114.Core17R3.exists_realized_first_hit_11`: use existing `DelayedOverlapGate.realized_safe_gate` for actual ordinary positive existence.

The candidate reuses the actual `FoldedDecimal.step_eq_word_value` numeric bridge, obtains the common first output `1100194810011`, then reduces exactly ten nonpalindrome checks and the step-11 palindrome. It uses no `sorry`, `admit`, `native_decide`, custom axiom or external oracle; **its syntax, kernel reduction and transitive axioms remain untested until a real Lean 4.19.0 run**. In particular, a valid Python/Node finite result is not a Lean theorem. The original `Canonical` digit function can differ arbitrarily beyond the represented width: no claim counts such tails as new integers.

GitHub coordination issue: https://github.com/taco-jpg/p196-algorithm/issues/61, scope proposal comment `6225301327`; published coordination claim `35ac4a57610864e619fa4923d68b3f515c8523eb`. This branch is isolated and has no main integration ownership.
