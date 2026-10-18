import P196.Agent9DigitSumWindows.SharpUniformEscape
import P196.Agent9DigitSumWindows.DecimalEmbedding

/-!
The manuscript's exact decimal uniform digit-sum escape bound, for ordinary
positive integers and every starting time. This does not prove palindrome
avoidance: the numeric orbit continues after a palindrome.
-/

namespace DecimalUniformEscape

open DecimalDigits DecimalMass Lychrel196

/-- The manuscript horizon E(2B), independent of the initial integer. -/
def sharpDigitSumEscapeBound (B : Nat) : Nat :=
  DecimalProfile.sharpEscapeBound (2 * B)

/-- Every positive decimal input exceeds a digit-sum ceiling within E(2B). -/
theorem digitSum_uniform_escape_sharp (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ sharpDigitSumEscapeBound B ∧ B < digitSum (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have ha := NormalizationBridge.canonical_admissible n d L hc
  have hv := DecimalProfile.NumericBridge.pad_valid (columnSum d L) L ha
  obtain ⟨t, ht, hm⟩ := DecimalProfile.sharp_uniform_escape
    (DecimalProfile.NumericBridge.embed (L, columnSum d L)) hv (2 * B)
  rw [DecimalProfile.NumericBridge.mass_numeric_iter n d L t hc] at hm
  exact ⟨t, ht, by omega⟩

/-- The sharp horizon applies to every time window of every positive orbit. -/
theorem digitSum_uniform_window_sharp (n : Nat) (hn : 0 < n) (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + sharpDigitSumEscapeBound B ∧
      B < digitSum (orbit n t) := by
  obtain ⟨j, hj, hgt⟩ := digitSum_uniform_escape_sharp
    (orbit n s) (orbit_positive n hn s) B
  refine ⟨s + j, by omega, by omega, ?_⟩
  simpa only [LychrelCertificates.orbit_add] using hgt

/-- Application to 196, without a claim of palindrome avoidance. -/
theorem digitSum_uniform_window_196_sharp (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + sharpDigitSumEscapeBound B ∧
      B < digitSum (orbit 196 t) :=
  digitSum_uniform_window_sharp 196 (by decide) B s

#print axioms digitSum_uniform_escape_sharp
#print axioms digitSum_uniform_window_sharp
#print axioms digitSum_uniform_window_196_sharp

end DecimalUniformEscape
