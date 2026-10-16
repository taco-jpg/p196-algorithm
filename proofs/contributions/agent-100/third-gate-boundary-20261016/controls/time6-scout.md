**PRECLAIM_SCOUT / FINITE.** Archived source analysis and nine-spacer ordinary-integer diagnostics. Not an ownership claim, not a Lean theorem, and not part of the Lean build. See README.md for reproduction and exact scope.

# Source scout: old (1,1,6) family, third proposed repair

Status: read-only source scout and finite diagnostics. No new theorem is claimed, no Lean implementation started, and no ownership is reserved. This inspects the already written argument in renewal_pass/constructive/STATUS.md, blob d684dc1865a3e59e1c699ad1ec28a4dbec0a74e2, section4. Agent2's claimed all-r>=5 first-positive-hit11 tail remains separate.

Let A0=component r 1 1 6 and Q0=Phi1 A0, with their **actual** finite pair words A_t,Q_t. The existing/new time4 formulas give A4=16·0^(r-1)·(1,1,2,2,1,1)·0^(r-1)·16 and Q4=Phi1 A4. Put L=2r+6.

The source's outer14-vs15 claim agrees with independent ordinary-integer diagnostics for r=1,2,3,4,5,6,10,30,100. In all those cases A has widths L through time4 and L+1 at times5,6; Q has widths L+1 through time4 and L+2 at times5,6. Thus Phi1 A6 and Q6 have equal physical widths; their index0 coefficients differ by1.

|Spacer|A4 first two|Q4 first two|A5 first two|Q5 first two|A6 outer|Q6 outer|
|---|---|---|---|---|---|---|
|r=1|(16,1)|(16,17)|(7,8)|(7,15)|14|15|
|r=2|(16,0)|(16,16)|(7,7)|(7,14)|14|15|
|r>=3, tested listed values|(16,0)|(16,16)|(7,7)|(7,14)|14|15|

The actual index0 difference is the shortest useful proposed certificate. It never accesses the arbitrary tail of a total `Nat -> Nat` pair function. No full time6 word formula is needed to refute the proposed overlap.

## Minimal local obligation suggested by the written proof

Use z=1 for r=1 and z=0 for r>=2. For an admissible bounded symmetric word with prefix (16,z), z<=1, the first normalization overflows; the next pair prefix is (7,7+z). For the whole prefix (16,16+z), the first normalization also overflows and gives (7,14+z). At the next step both outer7 coefficients forbid overflow, while the penultimate7+z resets the incoming carry to0 and the penultimate14+z forces it to1. The corresponding outer sums are14 and15.

This proposed local proof requires no assumption about deeper columns beyond admissibility/bounded carries and symmetry. It can reuse the unchanged LychrelDigitSums interfaces `OverflowNormalizationNine.outer_large_overflow`, `NormalizationBridge.outer_small_no_overflow`, `FoldedDecimal.next_column_overflow_outer`, `FoldedDecimal.next_column_overflow_interior`, `FoldedDecimal.next_column_no_overflow`, `carry_bounded`, and `NormalizationBridge.admissible_next`. Exact namespace qualification should be checked during implementation; the proposed arithmetic itself has not been Lean-checked here.

The r=1 boundary must retain z=1. Substituting the r>=2 prefix formula there gives the wrong time5 second coefficient (7 instead of8 for A,14 instead of15 for Q), although the final outer obstruction happens to remain14/15.

The finite scout also sees different deeper defects: for r1, Q6-Phi1 A6 starts (1,-19,-19,1); for the tested r>=2 it starts (1,-20,1). Neither full-defect identity is needed or proposed as a new accepted theorem. The source's time6 result is failure of this third reuse only, not exclusion of later returns or a first-hit theorem.
