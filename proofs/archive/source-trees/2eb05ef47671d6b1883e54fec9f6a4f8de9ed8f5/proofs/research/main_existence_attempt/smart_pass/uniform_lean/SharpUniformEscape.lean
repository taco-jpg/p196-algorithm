import UniformEscape
import SharpProfileBounds

/-!
The manuscript's exact decimal recurrence for uniform mass escape.
The definitions and all dynamics remain those of the checked concrete
half-line profile development.
-/

namespace DecimalProfile

open DecimalDigits DecimalMass DecimalZeroGap DecimalUnboundedMass

/-- The exact manuscript horizon, written in its equivalent width form. -/
def sharpEscapeBound : Nat → Nat
  | 0 => 0
  | 1 => 1
  | M + 2 => 5 * ((M + 2) + (M + 1) * (2 * sharpEscapeBound (M + 1) + 1))

theorem sharpEscapeBound_zero : sharpEscapeBound 0 = 0 := rfl

theorem sharpEscapeBound_one : sharpEscapeBound 1 = 1 := rfl

/-- This is exactly `E(M)=5*(2*(M-1)*E(M-1)+2*M-1)` for `M≥2`. -/
theorem sharpEscapeBound_recurrence (M : Nat) :
    sharpEscapeBound (M + 2) =
      5 * (2 * (M + 1) * sharpEscapeBound (M + 1) + 2 * (M + 2) - 1) := by
  rw [sharpEscapeBound]
  congr 1
  simp only [Nat.mul_add, Nat.mul_one, Nat.mul_left_comm (M + 1) 2,
    ← Nat.mul_assoc]
  omega

theorem sharpEscapeBound_eq (M : Nat) (hM : 2 ≤ M) :
    sharpEscapeBound M =
      5 * (2 * (M - 1) * sharpEscapeBound (M - 1) + 2 * M - 1) := by
  have hindex : M - 2 + 2 = M := by omega
  have hprev : M - 2 + 1 = M - 1 := by omega
  have hh := sharpEscapeBound_recurrence (M - 2)
  simpa only [hindex, hprev] using hh

theorem sharpEscapeBound_ge (M : Nat) : M ≤ sharpEscapeBound M := by
  cases M with
  | zero => exact Nat.le_refl _
  | succ M =>
    cases M with
    | zero => exact Nat.le_refl _
    | succ M =>
      change M + 2 ≤ 5 * ((M + 2) + (M + 1) *
        (2 * sharpEscapeBound (M + 1) + 1))
      omega

theorem sharpEscapeBound_le_succ (M : Nat) :
    sharpEscapeBound M ≤ sharpEscapeBound (M + 1) := by
  cases M with
  | zero => decide
  | succ M =>
    have hm := Nat.mul_le_mul_right (2 * sharpEscapeBound (M + 1) + 1)
      (show 1 ≤ M + 1 by omega)
    simp only [Nat.one_mul] at hm
    change sharpEscapeBound (M + 1) ≤
      5 * ((M + 2) + (M + 1) * (2 * sharpEscapeBound (M + 1) + 1))
    omega

/-- A valid profile of mass at most one has exactly one occupied column. -/
theorem mass_one_width (s : State) (hv : Valid s.1 s.2)
    (hm : mass s ≤ 1) : s.1 = 1 := by
  have hL := hv.1
  by_cases heq : s.1 = 1
  · exact heq
  have hLtwo : 2 ≤ s.1 := by omega
  have hprefix := wordSum_mono_length s.2 1 (s.1 - 1) (by omega)
  simp only [wordSum, Nat.zero_add] at hprefix
  have hsplit : wordSum s.2 s.1 = wordSum s.2 (s.1 - 1) + s.2 (s.1 - 1) := by
    have hindex : s.1 - 1 + 1 = s.1 := by omega
    have hh : wordSum s.2 (s.1 - 1 + 1) =
        wordSum s.2 (s.1 - 1) + s.2 (s.1 - 1) := rfl
    simpa only [hindex] using hh
  have hzero := hv.2.1
  have hlast := hv.2.2.2.2
  change wordSum s.2 s.1 ≤ 1 at hm
  omega

/-- The single unit coefficient becomes two at the next actual step. -/
theorem mass_one_next (s : State) (hv : Valid s.1 s.2)
    (hm : mass s ≤ 1) : mass (iter s 1) = 2 := by
  obtain ⟨L, q⟩ := s
  have hL : L = 1 := mass_one_width (L, q) hv hm
  subst L
  have hpos := hv.2.1
  change 0 < q 0 at hpos
  have hmass : q 0 ≤ 1 := by simpa [mass, wordSum] using hm
  have hq0 : q 0 = 1 := by omega
  have hf : carry q 1 = 0 := by simp [carry, hq0]
  have hb : backCarry q 1 0 = 0 := by simp [backCarry, reflect, carry, hq0]
  have hlen : nextLen q 1 = 1 := by simp [nextLen, hf, hb]
  simp [iter, step, mass, hlen, wordSum, phi, hb, output, carry,
    backOutput, reflect, hq0]

/-- The sharp gap budget propagates through every bounded-mass prefix. -/
theorem sharp_bounded_prefix_zeroBound (s : State) (hv : Valid s.1 s.2)
    (M K N : Nat) (hKsmall : 2 ≤ K) (hKmass : M + 1 ≤ K)
    (hzero : ZeroBound s.2 s.1 K)
    (hm : ∀ t, t ≤ N → mass (iter s t) ≤ M) :
    ∀ t, t ≤ N → ZeroBound (iter s t).2 (iter s t).1 K := by
  intro t
  induction t with
  | zero =>
    intro _
    exact hzero
  | succ t ih =>
    intro ht
    exact zeroBound_phi_sharp (iter s t).2 (iter s t).1 M K
      (iter_valid s t hv) (hm t (by omega)) (ih (by omega)) hKsmall hKmass

/-- Positive endpoints give the manuscript's sharp finite-width bound. -/
theorem sharp_bounded_prefix_width (s : State) (hv : Valid s.1 s.2)
    (M K N : Nat) (hKsmall : 2 ≤ K) (hKmass : M + 1 ≤ K)
    (hzero : ZeroBound s.2 s.1 K)
    (hm : ∀ t, t ≤ N → mass (iter s t) ≤ M) :
    ∀ t, t ≤ N → (iter s t).1 ≤ M + (M - 1) * K := by
  intro t ht
  exact length_le_mass_zero_runs_sharp (iter s t).2 (iter s t).1 M K
    (iter_valid s t hv) (hm t ht)
    (sharp_bounded_prefix_zeroBound s hv M K N hKsmall hKmass hzero hm t ht)

/-- Uniform escape with exactly the decimal horizon stated in the
manuscript: `E(1)=1` and `E(M)=5*(2*(M-1)*E(M-1)+2*M-1)`. -/
theorem sharp_uniform_escape (s : State) (hv : Valid s.1 s.2) (M : Nat) :
    ∃ t, t ≤ sharpEscapeBound M ∧ M < mass (iter s t) := by
  induction M generalizing s with
  | zero =>
    exact ⟨0, Nat.le_refl 0, mass_positive s hv⟩
  | succ M ih =>
    cases M with
    | zero =>
      by_cases hm : mass s ≤ 1
      · refine ⟨1, Nat.le_refl 1, ?_⟩
        rw [mass_one_next s hv hm]
        decide
      · refine ⟨0, by decide, ?_⟩
        change 1 < mass s
        omega
    | succ M =>
      apply Classical.byContradiction
      intro hnone
      have hm : ∀ t, t ≤ sharpEscapeBound (M + 2) →
          mass (iter s t) ≤ M + 2 := by
        intro t ht
        by_cases hgt : M + 2 < mass (iter s t)
        · exact False.elim (hnone ⟨t, ht, hgt⟩)
        · omega
      let T := sharpEscapeBound (M + 1)
      let K := 2 * T + 1
      let H := (M + 2) + (M + 1) * K
      have hT : M + 1 ≤ T := sharpEscapeBound_ge (M + 1)
      have hKsmall : 2 ≤ K := by dsimp [K]; omega
      have hKmass : (M + 2) + 1 ≤ K := by dsimp [K]; omega
      have htime : sharpEscapeBound (M + 2) = 5 * H := rfl
      by_cases hz : ZeroBound s.2 s.1 K
      · have hwidth := sharp_bounded_prefix_width s hv (M + 2) K
          (sharpEscapeBound (M + 2)) hKsmall hKmass hz hm
          (sharpEscapeBound (M + 2)) (Nat.le_refl _)
        have hclock := iter_width_clock s (sharpEscapeBound (M + 2)) hv
        have hL := hv.1
        have hH : 0 < H := by dsimp [H]; omega
        change (iter s (sharpEscapeBound (M + 2))).1 ≤ H at hwidth
        omega
      · obtain ⟨A, D, p, v, hp, heq, hvz, hvnon, hgap⟩ :=
          long_gap_split s.1 s.2 T hv hz
        have hisolate := isolated_mass s.2 p v s.1 A D T hv hp heq hvz hvnon hgap
        obtain ⟨t, ht, hgt⟩ := ih (A, p) hp
        have hpart := hisolate t ht
        change mass (iter (A, p) t) + 1 ≤ mass (iter s t) at hpart
        have hwhole := hm t (Nat.le_trans ht (sharpEscapeBound_le_succ (M + 1)))
        omega

#print axioms sharpEscapeBound_eq
#print axioms sharp_uniform_escape

end DecimalProfile
