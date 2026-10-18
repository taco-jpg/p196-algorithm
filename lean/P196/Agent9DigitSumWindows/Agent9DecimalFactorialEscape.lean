import P196.Agent9DigitSumWindows.Agent9FactorialRecurrence
import P196.Agent9DigitSumWindows.SharpUniformDecimal

/-!
Decimal instance of strengthening_notes.txt, section 5, equation (9).
All profile dynamics, the integer orbit, 和 the sharp escape theorem are
the unchanged existing declarations. The closed bound is intentionally coarse.
-/

namespace P196.Agent9.FactorialEscape

/-- The manuscript factorial bound for the existing exact decimal recurrence.
The additional `M=0` case uses its existing value zero separately. -/
theorem sharpEscapeBound_factorial (M : Nat) :
    DecimalProfile.sharpEscapeBound M ≤ 20 ^ (M - 1) * factorial M := by
  cases M with
  | zero => simp [DecimalProfile.sharpEscapeBound_zero]
  | succ i =>
    have hrec : ∀ j, DecimalProfile.sharpEscapeBound (j + 2) =
        5 * ((j + 2) + (j + 1) *
          (2 * DecimalProfile.sharpEscapeBound (j + 1) + 1)) := fun _ => rfl
    simpa using recurrence_factorial_bound 5 (by decide)
      DecimalProfile.sharpEscapeBound DecimalProfile.sharpEscapeBound_one
      hrec (i + 1) (by omega)

/-- Applying the mass-index bound at the unchanged digit-sum index `2*B`.
For `B=0`, the closed expression is one while the exact horizon is zero. -/
theorem sharpDigitSumEscapeBound_factorial (B : Nat) :
    DecimalUniformEscape.sharpDigitSumEscapeBound B ≤
      20 ^ (2 * B - 1) * factorial (2 * B) :=
  sharpEscapeBound_factorial (2 * B)

/-- Actual ordinary-decimal escape in every inclusive time window, for every
positive seed 和 all natural thresholds/start times, including zero. -/
theorem digitSum_uniform_window_factorial (n : Nat) (hn : 0 < n) (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
      B < DecimalMass.digitSum (Lychrel196.orbit n t) := by
  obtain ⟨t, hlo, hhi, hp⟩ :=
    DecimalUniformEscape.digitSum_uniform_window_sharp n hn B s
  exact ⟨t, hlo, Nat.le_trans hhi
    (Nat.add_le_add_left (sharpDigitSumEscapeBound_factorial B) s), hp⟩

/-- The same finite window for the ordinary orbit of 196. -/
theorem digitSum_uniform_window_196_factorial (B s : Nat) :
    ∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
      B < DecimalMass.digitSum (Lychrel196.orbit 196 t) :=
  digitSum_uniform_window_factorial 196 (by decide) B s

#print axioms sharpEscapeBound_factorial
#print axioms sharpDigitSumEscapeBound_factorial
#print axioms digitSum_uniform_window_factorial
#print axioms digitSum_uniform_window_196_factorial

end P196.Agent9.FactorialEscape
