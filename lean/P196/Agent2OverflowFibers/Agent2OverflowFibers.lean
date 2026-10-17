import P196.Agent2OverflowFibers.Agent2OverflowBound
import P196.Agent2OverflowFibers.Agent2OverflowImage

/-!
Agent #2: exact sharp overflow inverse-fiber maximum for the repository's
actual pair-word transition, at every input width at least two.
The witnesses have a nonpalindromic next normalization.  This is a finite
one-step counting theorem, not an infinite-orbit or Lychrel-existence result.
-/

namespace P196.Agent2.OverflowFibers

set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

theorem sharpFamily_membership (odd : Bool) (n : Nat) (q : List Nat)
    (hq : q ∈ sharpFamily odd n) :
    ActualOverflowFiber (2 * n + 2 + if odd then 1 else 0)
      (sharpTarget (2 * n + if odd then 1 else 0)) q := by
  obtain ⟨bs, hbs, rfl⟩ := List.mem_map.mp hq
  have hlen := binaryWords_member_length n bs hbs
  simpa only [hlen] using sharpWord_actualOverflowFiber odd bs

/-- The canonical complete fiber of the explicit target attains the upper
bound. Both parity choices are derived from L; there is no width premise
other than L >= 2. -/
theorem actualOverflowPreimages_sharp (L : Nat) (hL : 2 ≤ L) :
    (actualOverflowPreimages L (sharpTarget (L - 2))).length =
      2 ^ (L / 2 - 1) := by
  let odd : Bool := decide (L % 2 = 1)
  let n : Nat := L / 2 - 1
  have hwidth : 2 * n + 2 + (if odd then 1 else 0) = L := by
    dsimp only [n, odd]
    by_cases hodd : L % 2 = 1 <;> simp [hodd] <;> omega
  have htarget : 2 * n + (if odd then 1 else 0) = L - 2 := by omega
  have hsubset : ∀ q ∈ sharpFamily odd n,
      q ∈ actualOverflowPreimages L (sharpTarget (L - 2)) := by
    intro q hq
    apply (actualOverflowPreimages_membership L (sharpTarget (L - 2)) q).mpr
    have h := sharpFamily_membership odd n q hq
    simpa only [hwidth, htarget] using h
  have hlower := nodup_subset_length_le (sharpFamily odd n)
    (actualOverflowPreimages L (sharpTarget (L - 2)))
    (sharpFamily_nodup odd n) hsubset
  rw [sharpFamily_length] at hlower
  have hupper := actualOverflowPreimages_bound L (sharpTarget (L - 2)) hL
  exact Nat.le_antisymm hupper hlower

/-- Full exact maximum: all complete fibers are bounded, and an explicit
target attains that value while not producing a palindrome next. -/
theorem actual_overflow_sharp_maximum (L : Nat) (hL : 2 ≤ L) :
    (∀ target : List Nat,
      (actualOverflowPreimages L target).Nodup ∧
      (actualOverflowPreimages L target).length ≤ 2 ^ (L / 2 - 1)) ∧
    ∃ target : List Nat,
      (actualOverflowPreimages L target).length = 2 ^ (L / 2 - 1) ∧
      Agent8.normalize target 0 ≠ (Agent8.normalize target 0).reverse := by
  constructor
  · intro target
    exact ⟨actualOverflowPreimages_nodup L target,
      actualOverflowPreimages_bound L target hL⟩
  · exact ⟨sharpTarget (L - 2), actualOverflowPreimages_sharp L hL,
      sharpTarget_not_palindrome (L - 2)⟩

#print axioms sharpFamily_membership
#print axioms actualOverflowPreimages_sharp
#print axioms actual_overflow_sharp_maximum

end P196.Agent2.OverflowFibers
