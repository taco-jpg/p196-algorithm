import GeneralMomentAbsorption

/-!
Agent #5: discharge orbit-wide coefficient assumptions from initial validity.
SOURCE_PRESENT / BUILD_NOT_RUN. This source has not been checked by Lean here.
The imported definitions are unchanged. No integer-orbit bridge is asserted.
-/

namespace P196.Agent5.General.InitialValidity

/-- Positive interior bulk phase, excluding the neutral coefficient. -/
def Phase (m c : Int) : Prop := 0 < c ∧ c < 2 * m ∧ c ≠ m

def Bounded (m : Int) (B : Word) : Prop :=
  ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m

structure State where
  c : Int
  B : Word
  deriving DecidableEq, Repr

def Valid (m : Int) (s : State) : Prop := Phase m s.c ∧ Bounded m s.B

def step (m : Int) (s : State) : State :=
  ⟨nextPhase m s.c, nextExterior m s.c s.B⟩

def orbit (m : Int) (s : State) : Nat → State
  | 0 => s
  | n + 1 => step m (orbit m s n)

theorem band_digit_bounds (m c : Int) (hc : Phase m c) :
    1 ≤ c - m * bulkCarry m c ∧ c - m * bulkCarry m c < m := by
  rcases hc with ⟨hc0, hc2, hcne⟩
  unfold bulkCarry
  split <;> simp only [Int.mul_one, Int.mul_zero, Int.sub_zero] <;> omega

theorem phase_step (m c : Int) (hodd : ∃ r : Int, m = 2 * r + 1)
    (hc : Phase m c) : Phase m (nextPhase m c) := by
  have ht := band_digit_bounds m c hc
  rcases hodd with ⟨r, hr⟩
  unfold Phase nextPhase
  omega

theorem boundary_digit_bounds (m c e : Int) (hc : Phase m c)
    (he : 0 ≤ e ∧ e ≤ 1) :
    0 ≤ c + e - (m + 1) * bulkCarry m c ∧
      c + e - (m + 1) * bulkCarry m c ≤ m := by
  rcases hc with ⟨hc0, hc2, hcne⟩
  unfold bulkCarry
  split <;> simp only [Int.mul_one, Int.mul_zero, Int.sub_zero] <;> omega

/-- Modulo normalization produces digits even for unrestricted input integers. -/
theorem normalize_digits_bounded (m : Int) (B : Word) (e : Int) (hm : 1 ≤ m) :
    ∀ x ∈ (normalize m B e).1, 0 ≤ x ∧ x ≤ m := by
  induction B generalizing e with
  | nil => simp [normalize]
  | cons b bs ih =>
    intro x hx
    simp only [normalize, List.mem_cons] at hx
    rcases hx with hx | hx
    · subst x
      have h0 := Int.emod_nonneg (b + e) (show m + 1 ≠ 0 by omega)
      have hlt := Int.emod_lt_of_pos (b + e) (show 0 < m + 1 by omega)
      omega
    · exact ih ((b + e) / (m + 1)) x hx

theorem zip_add_bounded (m : Int) (a b : Word)
    (ha : ∀ x ∈ a, 0 ≤ x ∧ x ≤ m)
    (hb : ∀ x ∈ b, 0 ≤ x ∧ x ≤ m) :
    Bounded m (List.zipWith (· + ·) a b) := by
  induction a generalizing b with
  | nil => simp [Bounded]
  | cons x xs ih =>
    cases b with
    | nil => simp [Bounded]
    | cons y ys =>
      have hx := ha x (by simp)
      have hy := hb y (by simp)
      have hxs : ∀ z ∈ xs, 0 ≤ z ∧ z ≤ m := by
        intro z hz
        exact ha z (by simp [hz])
      have hys : ∀ z ∈ ys, 0 ≤ z ∧ z ≤ m := by
        intro z hz
        exact hb z (by simp [hz])
      intro z hz
      simp only [List.zipWith_cons_cons, List.mem_cons] at hz
      rcases hz with hz | hz
      · subst z
        omega
      · exact ih ys hxs hys z hz

theorem append_digit_bounded (m : Int) (w : Word) (e : Int)
    (hw : ∀ x ∈ w, 0 ≤ x ∧ x ≤ m) (he : 0 ≤ e ∧ e ≤ m) :
    ∀ x ∈ w ++ [e], 0 ≤ x ∧ x ≤ m := by
  intro x hx
  simp only [List.mem_append, List.mem_singleton] at hx
  rcases hx with hx | hx
  · exact hw x hx
  · simpa [hx] using he

theorem rawExterior_bounded (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hc : Phase m c) (hB : Bounded m B) : Bounded m (rawExterior m c B) := by
  have hl := normalize_digits_bounded m B 0 hm
  have hh := normalize_digits_bounded m B.reverse (bulkCarry m c) hm
  have he := normalize_carry_bit m B 0 hm hB (by omega)
  have hu := boundary_digit_bounds m c (normalize m B 0).2 hc he
  have ht := band_digit_bounds m c hc
  have hlo := append_digit_bounded m (normalize m B 0).1
    (c + (normalize m B 0).2 - (m + 1) * bulkCarry m c) hl hu
  have hrev : ∀ x ∈ (normalize m B.reverse (bulkCarry m c)).1.reverse,
      0 ≤ x ∧ x ≤ m := by
    intro x hx
    exact hh x (by simpa using hx)
  have hno := append_digit_bounded m
    (normalize m B.reverse (bulkCarry m c)).1.reverse
    (c - m * bulkCarry m c) hrev (by omega)
  have hyes : ∀ x ∈ 1 :: (normalize m B.reverse (bulkCarry m c)).1.reverse,
      0 ≤ x ∧ x ≤ m := by
    intro x hx
    simp only [List.mem_cons] at hx
    rcases hx with hx | hx
    · subst x
      omega
    · exact hrev x hx
  unfold rawExterior
  split
  · exact zip_add_bounded m _ _ hlo hno
  · exact zip_add_bounded m _ _ hlo hyes

theorem stripSuffix_bounded (m c : Int) (B : Word) (hB : Bounded m B) :
    Bounded m (stripSuffix c B).1 := by
  intro x hx
  apply hB x
  rw [Moment.stripSuffix_decomposition c B]
  exact List.mem_append.mpr (Or.inl hx)

theorem nextExterior_bounded (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hc : Phase m c) (hB : Bounded m B) : Bounded m (nextExterior m c B) := by
  exact stripSuffix_bounded m (nextPhase m c) (rawExterior m c B)
    (rawExterior_bounded m c B hm hc hB)

theorem valid_step (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s) :
    Valid m (step m s) := by
  exact ⟨phase_step m s.c hodd hs.1,
    nextExterior_bounded m s.c s.B hm hs.1 hs.2⟩

/-- No coefficient-bound hypothesis about later states occurs in this contract. -/
theorem valid_orbit (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s) (n : Nat) :
    Valid m (orbit m s n) := by
  induction n with
  | zero => exact hs
  | succ n ih => exact valid_step m (orbit m s n) hm hodd ih

theorem overflow_bit_orbit (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s) (n : Nat) :
    exteriorOverflow m (orbit m s n).c (orbit m s n).B = 0 ∨
      exteriorOverflow m (orbit m s n).c (orbit m s n).B = 1 := by
  exact exterior_overflow_bit m _ _ hm (valid_orbit m s hm hodd hs n).2

theorem orbit_add (m : Int) (s : State) (a b : Nat) :
    orbit m s (a + b) = orbit m (orbit m s a) b := by
  induction b with
  | zero => simp [orbit]
  | succ b ih => simp [Nat.add_succ, orbit, ih]

def residue (m : Int) (s : State) : Int :=
  Moment.moment s.c s.B % (2 * (m + 2))

/-- Absorption persistence with only initial-state bounds. -/
theorem residue_zero_orbit (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hz : residue m s = 0) (n : Nat) : residue m (orbit m s n) = 0 := by
  induction n with
  | zero => exact hz
  | succ n ih =>
    have hB := (valid_orbit m s hm hodd hs n).2
    have h := Moment.moment_zero_preserved m (orbit m s n).c
      (orbit m s n).B hm hB ih
    simpa only [orbit, step, residue] using h

/-- One computed overflow supplies the initial zero automatically. -/
theorem residue_zero_after_overflow (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s) (j n : Nat)
    (hg : exteriorOverflow m (orbit m s j).c (orbit m s j).B = 1) :
    residue m (orbit m s (j + 1 + n)) = 0 := by
  have hv := valid_orbit m s hm hodd hs (j + 1)
  have hreset := Moment.moment_step_overflow m (orbit m s j).c (orbit m s j).B hg
  have hz : residue m (orbit m s (j + 1)) = 0 := by
    simpa only [orbit, step, residue] using hreset
  rw [orbit_add]
  exact residue_zero_orbit m (orbit m s (j + 1)) hm hodd hv hz n

theorem decimal_valid_orbit (s : State) (hs : Valid 9 s) (n : Nat) :
    Valid 9 (orbit 9 s n) :=
  valid_orbit 9 s (by decide) ⟨4, by decide⟩ hs n

theorem decimal_residue_after_overflow (s : State) (hs : Valid 9 s) (j n : Nat)
    (hg : exteriorOverflow 9 (orbit 9 s j).c (orbit 9 s j).B = 1) :
    Moment.moment (orbit 9 s (j + 1 + n)).c
      (orbit 9 s (j + 1 + n)).B % 22 = 0 := by
  exact residue_zero_after_overflow 9 s (by decide) ⟨4, by decide⟩ hs j n hg

/-- The neutral phase cannot simply be added to the invariant domain. -/
theorem neutral_counterexample :
    nextExterior 9 9 [1, 18] = [3, 16, 19] := by decide

theorem neutral_not_bounded : ¬ Bounded 9 (nextExterior 9 9 [1, 18]) := by
  intro h
  have hx := h 19 (by decide)
  omega

/-- In an odd base the phase can land exactly on the excluded neutral value. -/
theorem odd_base_phase_counterexample : Phase 2 1 ∧ ¬ Phase 2 (nextPhase 2 1) := by decide

end P196.Agent5.General.InitialValidity
