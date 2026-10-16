# Third-gate boundary: final three-module semantic review

**SOURCE SEMANTICS REVIEW PASS.** Agent #100's independent `scope_audit` specialist inspected the exact eight-theorem Boundary module, twelve-theorem Numeric module and eight-theorem Controls module: 28 exports in total. This is source-semantic review plus independently executed finite Python controls, not an independent Lean rebuild. Compiler and axiom execution evidence for the frozen sources is provided separately by the parent and runtime specialist.

| Module | SHA-256 |
| --- | --- |
| `Agent100ThirdGateBoundary.lean` | `7f6992f08e7f7b75e0a609d54a64f9ac7c2b80344296761be111e740ef48a96c` |
| `Agent100ThirdGateNumeric.lean` | `b1ff8e06cf63d34a935f826b806dbd02fcf3808b83511e062f91a3d64da7e3db` |
| `Agent100ThirdGateControls.lean` | `44bb4ea1256cf0b5b6c42183de1b477a723c1d1e76e0cfe5273956b483367749` |

## Actual time four to time six

`componentOrbit` and `wholeOrbit` abbreviate the repository's actual `iterPairs`, starting from the old `(p,u,v)=(1,1,6)` component and its whole overlap. No alternative update function is introduced. The exact time-four prefixes are obtained from the previously checked DoubleGate theorems, at valid indices 0 and 1. `spacerBit r` is 1 precisely for `r=1`, and 0 otherwise. Thus the time-four component prefix is `(16,spacerBit r)` and the whole prefix is `(16,16+spacerBit r)`; the shortest-spacer collision is retained.

The proof establishes time-four admissibility by `iterPairs_admissible` from each actual initial admissible state. It then applies the generic two-column result to the **actual time-four functions**, not to a guessed complete word or a representative selected by shape. The exact `iterPairs_add` composition identifies those two subsequent updates with time six of the original orbit.

The component's actual width at time six is `2*r+7`, with outer coefficient 14. The whole's actual width is `2*r+8`, with outer coefficient 15. The generic Boundary module supplies one overflow followed by one non-overflow, so these widths are conclusions, not extra compatibility assumptions. `sixth_widths_compatible` explicitly proves that the whole width is one greater than the component width.

## Finite overlap and the witness

`finiteWord L q` agrees with `q` only at indices strictly below `L` and is zero elsewhere. Consequently `shiftOne (finiteWord componentWidth componentState)` is the proper overlap of the actual finite component prefix. In particular, at the new final overlap index it reads the zero extension plus the last represented component coefficient, rather than the uncontrolled tail of the total `Nat -> Nat` state function.

`third_overlap_fails` quantifies equality only inside the actual whole width. Its contradiction occurs at index 0, which is strictly within both positive widths. The component overlap has coefficient 14 there, while the actual whole state has coefficient 15. This is a genuine represented-column difference between correctly matched finite widths. No out-of-window coefficient, arbitrary function tail, or length mismatch supplies the obstruction.

The theorem excludes this specific proposed time-six overlap. It does not exclude later overlaps, other shifts, other component templates, cycles or infinite trajectories; it does not determine a first palindrome time. Agent #2's first-hit-eleven task and Agent #8's general equal-width common-overflow transport remain distinct.

## Ordinary canonical realizations and existence

`numeric_six_boundary` universally quantifies the original `n`, its arbitrary canonical digit function `d`, and the spacer `r>=1`. The only representation premise is that the original finite pair sums match `DoubleGate.initial r`. `iterPairs_representation` is applied at six actual ordinary reverse-add steps from that same original integer. The output digit function `e` is canonical for `orbit n 6`, has exact width `2*r+8`, and agrees with the whole pair orbit at **every valid column**, in addition to the outer value 15.

`numeric_third_overlap_fails` transfers the full valid-prefix identity from this real sixth iterate to the finite-word obstruction. There is no replacement of `n` by the convenient realization used in Python, nor a premise that an arbitrary symbolic successor happens to be realized. The output is stated using an existential canonical digit function; it does not assert equality of canonical digit functions on irrelevant infinite tails.

`realized_six_boundary` separately obtains a positive canonical seed from the already proved `DoubleGate.realized_safe_double_gate`, preserving the same profile and the same seed when it applies the universal numeric theorem. Its existential claim is therefore nonvacuous for every `r>=1`. The theorem states a sixth boundary, not the first-hit-eleven endpoint or an all-time safety result. The initial four safe outputs remain supplied by DoubleGate; this file does not newly assert safety at every intervening positive time.

## Kernel-control statement semantics

`admissible_from_finite_check` transfers a conjunction over `Fin L` to the original `Admissible L q` with unrestricted natural index and explicit `i<L` premise. In each of the three fields it forms the same index `Fin.mk i hi`; the coercion back to `Nat` is definitionally `i`. The bound, reflection and odd-center parity conditions are therefore proved for every original valid index. No unproved conversion of a finite sample to a larger domain occurs, and no condition on an out-of-width tail is introduced.

The two second-column-nine controls use genuinely admissible width-five words `[7,9,0,9,7]` and `[7,9,10,9,7]`. They have equal outer coefficient 7, equal second coefficient 9 and equal next width 5, but actual next outer coefficients 14 and 15. `neighbor_nine_not_determined` negates exactly the proposed universal next-outer equality by substituting those two instances. It does not assert that every neutral-neighbor state behaves differently or that no more detailed rule is possible.

The `spacerTwo` control uses the width-six word `[16,2,18,18,2,16]`, proves its admissibility and first two coefficients, and checks the actual two-step width 7 and outer coefficient 15. `low_bound_two_false` uses this instance to refute replacing `z<=1` by `z<=2` in the universal low two-step conclusion. The source does not claim this is the shortest counterexample; the separately recorded width-five witness remains a finite Python example unless independently formalized.

`shortest_high_control` checks the real width-two profile `[16,16]` and its next prefix `(7,14)`, then its two-step width 3 and outer coefficient 15. `ordinary_97_control` additionally verifies canonical digit functions of 97, 176 and 847, the actual ordinary orbit equalities `97 -> 176 -> 847`, and every pair column at each valid width. In particular the quantified next-state and second-state comparisons range over all `Fin 3` indices and are then transferred to every natural `i<3`, covering the newly created endpoint column 2. Their pair words are `[16,16]`, `[7,14,7]`, and `[15,8,15]`.

All concrete controls use ordinary `decide` proofs in Lean source, not `native_decide` or a Python result imported as an axiom. This audit checks their statement meanings and index coverage; actual kernel execution remains evidenced by the separate build records.

## Generic scope, finite controls and disposition

The generic two-column lemmas are sufficient under the stated `Admissible`, `L>=2` and prefix assumptions. Their exact small-width empty cells and real witnesses are recorded in `two-column-semantic-review.md`: low prefix `(16,z)` has no width-two realization; high prefix `(16,16+z)` has the real width-two case `z=0`; the `z=1` width-three cases are excluded by center parity. None of these empty cells is counted as a finite example.

Independent controls exhaust all 243,114 relevant admissible coefficient profiles of widths 2 through 10, with 287,317 ordinary integer additions and separate grade-school carry checks. The nine-spacer original orbit scout separately checks actual component and whole trajectories through time six. These finite results support the implementation review but do not establish universal parameter or arbitrary-digit-split quantifiers. Complete trace data are preserved without loss in both gzip and XZ; reproduction, per-condition realizable counts and hashes are in the controls README and summaries.

No semantic issue was found in the 28 frozen theorem declarations. Existing four Group II/DoubleGate source hashes remain unchanged. The formal scope is a finite, actual-arithmetic obstruction to the third proposed two-step repair, including `r=1`, plus exact local controls showing why the relevant boundary hypotheses matter; no broader impossibility or infinite-orbit claim is warranted. Any later proof-source change requires a fresh source pin check. Independent Lean execution and transitive axiom results remain a separate acceptance record.
