import Agent9WindowIntervalCounts
import SharpUniformDecimal

/-!
Finite ordinary-decimal consequence of the existing exact uniform escape theorem.
Written source: strengthening_notes.txt, section 6, original source commit
2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob 7103ee939d82740b970dd23fb91e9db50db4ea54.
The original integer orbit continues after palindromes. This result counts
excursions above a fixed threshold; it asserts no pointwise convergence.
-/

namespace P196.Agent9.IntervalCounts

/-- Every half-open finite interval contains at least one digit-sum excursion
per complete window of length `sharpDigitSumEscapeBound B + 1`.
All natural `B`, `s`, 和 `N` are included, including zero. -/
theorem digitSum_interval_count (n : Nat) (hn : 0 < n) (B s N : Nat) :
    N / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) ≤
      ((List.range' s N).filter
        (fun t => decide (B < DecimalMass.digitSum (Lychrel196.orbit n t)))).length := by
  refine window_property_interval_count
    (fun t => B < DecimalMass.digitSum (Lychrel196.orbit n t))
    (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) (by omega) ?_ s N
  intro a
  obtain ⟨t, hlo, hhi, hp⟩ :=
    DecimalUniformEscape.digitSum_uniform_window_sharp n hn B a
  exact ⟨t, hlo, by omega, hp⟩

/-- The same unconditional finite count for the ordinary orbit of 196. -/
theorem digitSum_interval_count_196 (B s N : Nat) :
    N / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) ≤
      ((List.range' s N).filter
        (fun t => decide (B < DecimalMass.digitSum (Lychrel196.orbit 196 t)))).length :=
  digitSum_interval_count 196 (by decide) B s N

#print axioms digitSum_interval_count
#print axioms digitSum_interval_count_196

end P196.Agent9.IntervalCounts
