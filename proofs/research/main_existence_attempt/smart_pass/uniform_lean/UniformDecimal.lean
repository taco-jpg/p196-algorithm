import UniformEscape
import DecimalEmbedding

/-!
Uniform waiting time for actual positive decimal reverse-and-add orbits.
The recurrence is intentionally coarse and independent of the initial
integer, its decimal width, and the starting time of the observation.
This theorem does not assert palindrome avoidance.
-/

namespace DecimalUniformEscape

open DecimalDigits DecimalMass Lychrel196

/-- A uniform digit-sum escape horizon, depending only on the threshold. -/
def digitSumEscapeBound (B : Nat) : Nat := DecimalProfile.escapeBound (2 * B)

/-- Every positive decimal input exceeds a digit-sum ceiling by the same
threshold-dependent deadline. The input need not start below the ceiling. -/
theorem digitSum_uniform_escape (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, t ≤ digitSumEscapeBound B ∧ B < digitSum (orbit n t) := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have ha := NormalizationBridge.canonical_admissible n d L hc
  have hv := DecimalProfile.NumericBridge.pad_valid (columnSum d L) L ha
  obtain ⟨t, ht, hm⟩ := DecimalProfile.uniform_escape
    (DecimalProfile.NumericBridge.embed (L, columnSum d L)) hv (2 * B)
  rw [DecimalProfile.NumericBridge.mass_numeric_iter n d L t hc] at hm
  exact ⟨t, ht, by omega⟩

/-- The same deadline applies to every time window, independently of
the orbit's initial value and the selected starting time. -/
theorem digitSum_uniform_window (n : Nat) (hn : 0 < n) (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + digitSumEscapeBound B ∧
      B < digitSum (orbit n t) := by
  obtain ⟨j, hj, hgt⟩ := digitSum_uniform_escape
    (orbit n s) (orbit_positive n hn s) B
  refine ⟨s + j, by omega, by omega, ?_⟩
  simpa only [LychrelCertificates.orbit_add] using hgt

/-- The uniform theorem applies to 196 but makes no palindrome claim. -/
theorem digitSum_uniform_window_196 (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + digitSumEscapeBound B ∧
      B < digitSum (orbit 196 t) :=
  digitSum_uniform_window 196 (by decide) B s

#print axioms digitSum_uniform_escape
#print axioms digitSum_uniform_window
#print axioms digitSum_uniform_window_196

end DecimalUniformEscape
