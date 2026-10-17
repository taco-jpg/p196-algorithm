import Agent1PeriodicSafety

/-!
Interpretation of the exact periodic state test for every original canonical
integer realization. The complete arithmetic criterion is reused unchanged.
This classifies the next output, not the represented input or all future times.
-/
namespace Agent1.Periodic
open Agent8

/-- Every original canonical realization has the same next-output safety
flag as its stored periodic tuple. The digit and pair correspondence premises
retain every in-range position and the original canonical width. -/
theorem safePeriodic_iff_next_not_palindrome (B H w : Word) (k n : Nat)
    (d : Nat → Nat) (hk : 0 < k) (hw : w ≠ [])
    (hc : DecimalDigits.Canonical n d (periodicWord B H w k).length)
    (hrep : ∀ i, i < (periodicWord B H w k).length →
      DecimalDigits.columnSum d (periodicWord B H w k).length i =
        ((periodicWord B H w k)[i]?).getD 0) :
    safePeriodic B H w = true ↔ ¬ Lychrel196.Palindrome (Lychrel196.step n) := by
  rw [safePeriodic_iff_not_bad B H w k hk hw]
  apply not_congr
  have hcriterion := DecimalDigits.step_palindrome_iff d _ hc.1 hc.2.1 hc.2.2.1
  rw [hc.2.2.2] at hcriterion
  rw [hcriterion]
  unfold FoldedDecimal.BadWord
  simp only [hrep 0 hc.1]
  constructor
  · rintro (h | ⟨hout, h⟩)
    · exact Or.inl (fun i hi => by rw [hrep i hi]; exact h i hi)
    · exact Or.inr ⟨hout, fun i hi => by rw [hrep i hi]; exact h i hi⟩
  · rintro (h | ⟨hout, h⟩)
    · exact Or.inl (fun i hi => by rw [← hrep i hi]; exact h i hi)
    · exact Or.inr ⟨hout, fun i hi => by rw [← hrep i hi]; exact h i hi⟩

end Agent1.Periodic
#print axioms Agent1.Periodic.safePeriodic_iff_next_not_palindrome
