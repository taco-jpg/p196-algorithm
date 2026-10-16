# Group III second handoff — source checkpoint

Reviewer: `/root/research_status/numeric_bridge_review`, Agent #1 specialist. No author-source edits, Git writes, or new mathematical source were performed. Independent compilation awaits the author's frozen handoff; this document is source inspection and finite diagnostics only.

No semantic gap was found in the current statements relative to the written fixed `(p,u,v)=(1,10,6)` target in constructive `STATUS.md`, section 3 (original blob `d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2`). This task excludes time-six work and infinite recurrence.

- `afterTwo = sixWord r 4 2 1 7` is exactly the first Group III returned component. The original first-gate theorem is reused, with its original parameter domain established by `first_domain`; no column is discarded from this six-column component.
- `componentThree = sixWord r 8 4 2 14` and `componentFour = sixWord r 16 8 5 9` match the written updates. The normalized center of the former is `(4,2,4,5,3,4)` and its paired center is `(8,5,9,9,5,8)`.
- For `r>=2`, incoming carries on the next two component words occur nowhere, then at `r+3,r+4`. The whole-word incoming carries occur at `r+4`, then at `r+3,r+5`. These are the actual recursive decimal carries, and all four relevant terminal carries vanish.
- The first overlap from the returned component is named `wholeTwo`. `wholeThree` adds exterior and central contributions. Its additive definition covers `r=1`; the later whole normalization lemmas correctly require `r>=2`, where the zero separator prevents exterior carry interaction.
- `continue_no_overflow` transports only finite-prefix agreement from the actual `iterPairs` state. The time-three/time-four theorems preserve actual component/whole widths and complete column words, without assumptions on function tails.
- `finiteComponent` truncates at the actual current component width. `OverlapAt` requires both the actual width relation and equality of the whole finite word with the overlap of that zero extension. It therefore expresses the stated finite-word relation even when widths could change.
- First- and third-step departures and second-/fourth-step returns use this same definition. The third departure has a concrete center mismatch `8` versus `28`.
- At `r=1`, the boundary theorems evaluate the original actual iterates, preserve widths eight/nine, and subtract over `Int`. The complete signed defect is `(1,-20,1,0,0,0,1,-20,1)`. `time_four_overlap_iff` combines this real boundary exclusion with the all-`r>=2` return; it does not substitute a formal predicted component for an unchecked actual one.
- Numeric statements retain the original `Canonical` predicate and finite initial pair-word agreement for arbitrary ordinary integer realizations. `iterPairs_representation` supplies the actual time-three/time-four canonical representations and true widths. Leading-zero padding and zero seeds are excluded by `Canonical`; arbitrary out-of-width tails remain irrelevant.
- Four-step safety uses the first-gate result for outputs one/two and `palindrome_iff_bad` on the words at times two/three for outputs three/four. This checks the positive outputs with no off-by-one change and makes no assertion about the initial seed's palindromicity.
- `numeric_time_four_iff` has a sound additional `r=1` exclusion: the target overlap's index-one coefficient is `24`, while a canonical pair-word coefficient is at most `18`. `numeric_safe_handoff` bundles the full all-realizations four-step conclusion. `realized_safe_handoff` reuses the first-gate positive realization theorem, so nonemptiness is discharged.

Independent executable controls in `finite_controls.py` passed for `r=1..32,64,128` (34 spacers, 102 canonical realization checks; choices need not be distinct). They check all actual component/whole words through time four, widths, genuine departures/returns, the normalized digit row, central digit defect, and the four positive integer outputs. The `r=1` actual time-four words are:

```text
component: 16,8,5,9,9,5,8,16
whole:     17,4,14,14,18,14,14,4,17
defect:    1,-20,1,0,0,0,1,-20,1
```

These controls are finite diagnostics only. They do not replace fresh Lean compilation and the complete transitive axiom audit of the frozen sources. No time-six calculation was run in this review.
