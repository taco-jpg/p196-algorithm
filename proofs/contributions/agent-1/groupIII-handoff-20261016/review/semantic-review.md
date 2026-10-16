# Independent second-handoff review: scoped PASS

Reviewer: `/root/research_status/numeric_bridge_review`, acting as an Agent #1 specialist. The reviewer edited only this `review/` directory, performed no Git writes, and did not edit either author's Lean source. Findings were supplied to the parent for attributed coordination relay. This is same-session specialist review, not external peer approval.

The frozen implementation correctly covers the written fixed Group III `(p,u,v)=(1,10,6)` second repair. No semantic gap or unresolved correctness issue was found. Independent fresh compilation and the complete transitive axiom audit passed.

## Frozen identities and executed checks

| Module | SHA-256 |
|---|---|
| `Agent1GroupIIIHandoff` | `190778311fe86b4c48ae617b2946d78876b13772c6dfeee8cba4f2a7cc0ba1a4` |
| `Agent1GroupIIIHandoffNumeric` | `14abe8bbdc4320c3ec72d97eacb403c481b154d8baf8f1dac041d3af79cc13c4` |

The reviewer executed `independent_build.py clean-001` after the author freeze. The runner verified these two exact hashes and pinned every one of the eight preexisting modules to the preceding accepted independent source snapshot. All original SHA-256/Git blob identities and the exact ten-module import closure matched.

All ten modules were rebuilt in a previously nonexistent source/object directory with official Lean 4.19.0, commit `6caaee842e94`, using `--trust=0 -j1 -DElab.async=false`. No author build or previous project objects were used. The installed official Lean/Std library was used. Every compile and the audit exited zero; source bytes and compiler identities were checked again at completion.

The complete module-origin audit checked **2,547 theorem constants**, including dependencies and generated auxiliaries. It also checked the printed types and literal `#print axioms` output of **all 43 new public exports: 36 core and seven numeric theorems**. Every logical axiom dependency is in `{propext, Classical.choice, Quot.sound}`. The five fixed `r=1` boundary theorems have no axiom dependencies. Fourteen compiler-generated unsafe implementation declarations are separately recorded from unchanged dependencies; none originates in either new module or occurs in theorem logical axiom sets. Forbidden proof-bypass/custom-axiom tokens were rejected by source scanning.

Evidence is retained in `clean-001/report.json`, `clean-001/logs/IndependentAudit.log`, the immutable `clean-001/source/` files, and `clean-001/FILES.json`. The audit/scanner follow the retained repository verifier's method; this was an independently executed clean build, not a claim to independently designed audit infrastructure. The 2,547 count is not a count of new mathematical results.

## Semantic findings on the compiled snapshot

The written source is constructive `STATUS.md`, section 3, original Git blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`, particularly lines 121, 125–139. References below are to the frozen files in `clean-001/source/`.

1. **Exact words and continuation.** `Agent1GroupIIIHandoff.lean:17–20` defines `afterTwo = sixWord r 4 2 1 7`, `componentThree = sixWord r 8 4 2 14`, and `componentFour = sixWord r 16 8 5 9`. Thus the returned component is exactly `16 · 0^(r-1) · (8,5,9,9,5,8) · 0^(r-1) · 16`, width `2r+6`. These are pair-sum coefficients, not individual decimal digits. `first_domain` and `first_return_component` at lines 30–35 connect the actual initial `(1,10,6)` family to the already-proved first gate. None of the six central columns is dropped or renamed into a four-column gate.

2. **Actual carries, complete columns, and width.** Lines 37–116 prove the four local recursive carry profiles, terminal no-overflow results, and complete next-column identities. The nonzero incoming carries are:

   | Input word | Incoming carry equals one exactly at |
   |---|---|
   | `afterTwo` | nowhere |
   | `wholeTwo` | `r+4` |
   | `componentThree` | `r+3,r+4` |
   | `wholeThree`, for `r>=2` | `r+3,r+5` |

   These agree with the written normalized center `(4,2,4,5,3,4)` and its paired center `(8,5,9,9,5,8)`. `wholeThree` adds exterior and core contributions, so the adjacent supports at `r=1` are not accidentally overwritten. The later whole normalization correctly requires `r>=2`.

3. **No tail or fixed-width surrogate.** `continue_no_overflow` at lines 119–128 uses finite-prefix agreement and the original `no_overflow_next_congr` to continue the actual `iterPairs` state. The time-three/time-four results at lines 130–159 and width results at 161–183 concern the original changing-width dynamics. `finiteComponent` at 186–188 zero-extends at the actual current component width; `OverlapAt` at 190–195 requires the actual width relation and equality throughout the actual whole width. Consequently both departures and both repairs use one consistent finite-word meaning, without assumptions on arbitrary function tails.

4. **Genuine repairs and exact threshold.** `time_three_departure` at 219–231 exhibits the central mismatch `8` versus `28`. The time-one failure and time-two repair reuse the first gate with the same finite-word convention. `two_genuine_repairs` at 385–388 combines failure at times 1/3 and restoration at times 2/4 for every `r>=2`. `component_time_four` holds even for `r=1`; the whole return requires `r>=2`.

5. **The shortest case is an actual kernel-checked boundary.** Lines 274–328 evaluate original `iterPairs` at `r=1`, prove actual component/whole widths eight/nine, and establish the complete signed defect `(1,-20,1,0,0,0,1,-20,1)` over `Int`. The nine list entries are only accessed under `i<9`; there is no out-of-range default issue. These are Lean theorems proved by kernel `decide`, not Python observations. `time_four_overlap_iff` at 332–345 combines that real boundary exclusion with the all-`r>=2` result to prove, for every `r>=1`, `OverlapAt r 4 ↔ 2<=r`.

6. **All ordinary integer realizations.** `Agent1GroupIIIHandoffNumeric.lean:13–41` uses the unchanged original `Canonical`, `columnSum`, `orbit`, and `iterPairs_representation`. The hypotheses require only finite initial pair-word agreement. Canonical leading positivity excludes zero/leading-zero padding, while allowing trailing zeros and irrelevant out-of-width digit values. The canonical time-four representation has width `2r+7` and the complete pair word `shiftOne (componentFour r)`. There is no assumed symbolic-to-numeric lift.

7. **Numeric sharpness and safety indices.** `numeric_time_four_iff` at 44–61 also proves the exact threshold for the canonical ordinary output. Its `r=1` exclusion uses coefficient `24` at index one of the proposed overlap, contradicting the original canonical pair bound `<=18`; it does not misclassify an arbitrary padded representation. `numeric_four_step_safety` at 63–84 reuses first-gate safety at outputs one/two and tests the predecessor words at times two/three to exclude palindromes at outputs three/four. The seed itself is not assumed nonpalindromic.

8. **Bundled conclusion and nonemptiness.** `numeric_safe_handoff` at 86–92 supplies the requested all-realizations safety-through-four and exact time-four return. `realized_safe_handoff` at 95–102 reuses the first-gate positive realization theorem for every permitted spacer. Its existence obligation is discharged, not a premise. Printed theorem types in `IndependentAudit.log:178–219` confirm the numeric sharpness and these complete exported conclusions.

The normalized-digit defect in the written proof route is not claimed as a separately exported new Lean theorem; the implemented return is proved directly through the full actual carry/column identities. No first-palindrome-time classification, time-six obstruction, infinite recurrence, persistent exterior reset, Lychrel existence, or complete-196-orbit claim is supplied. No time-six calculation was performed by this reviewer.

## Separate finite diagnostics

`finite_controls.py`, `finite-controls.log`, and `finite-controls-result.json` retain successful independent integer controls for `r=1..32,64,128`: **34 spacers and 102 canonical realization checks**, whose three choices per spacer need not be distinct. They check actual component/whole iterates through time four, widths, the normalized digit row and core digit defect, exact carry locations, both departures/repairs, and all four positive ordinary outputs.

The `r=1` actual time-four component is `[16,8,5,9,9,5,8,16]`; the whole word is `[17,4,14,14,18,14,14,4,17]`. Their difference after zero-extended overlap is exactly the stated nine-column defect. These script checks remain **finite diagnostic evidence**; the all-spacer result is supported by the independently compiled Lean proof.

`semantic-review-source-only.md` is retained as the earlier unverified checkpoint. This final report completes its verification status without changing that historical record.
