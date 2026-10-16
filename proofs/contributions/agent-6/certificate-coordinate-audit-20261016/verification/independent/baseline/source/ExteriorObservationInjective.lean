import ExteriorFactorizationProof

/-!
Agent #115. The observation `(c, zValue, ρ)` determines a canonical exterior
word. Together with `Agent115.ExteriorFactorization.target` this makes the exact
exterior map conjugate to the induced map on observations.

Elementary argument: for two equal-length words with coefficients at most 18,
equal little-endian values force equal outermost coefficients modulo 10, and
equal big-endian values exclude a difference of 10 because a tail of length `m`
has big-endian value below `2 * 10^m`. Induct.
-/

namespace Agent115.ExteriorFactorization

open P196.Agent7.Finite

theorem highValue_cons (x : Nat) (xs : List Nat) :
    highValue (x :: xs) = x * 10 ^ xs.length + highValue xs := by
  show List.foldl (fun acc b => 10 * acc + b) (10 * 0 + x) xs = _
  rw [foldl_high]
  simp

theorem highValue_lt (l : List Nat) (hl : ∀ x ∈ l, x ≤ 18) :
    highValue l + 2 ≤ 2 * 10 ^ l.length := by
  induction l with
  | nil => simp [highValue]
  | cons x xs ih =>
    rw [highValue_cons, List.length_cons, Nat.pow_succ]
    have hx := hl x List.mem_cons_self
    have h := ih (fun y hy => hl y (List.mem_cons_of_mem x hy))
    have hm : x * 10 ^ xs.length ≤ 18 * 10 ^ xs.length := Nat.mul_le_mul_right _ hx
    omega

/-- Equal length, coefficients at most 18, equal little- and big-endian values
force equal words. -/
theorem eq_of_values (a b : List Nat) (hl : a.length = b.length)
    (ha : ∀ x ∈ a, x ≤ 18) (hb : ∀ x ∈ b, x ≤ 18)
    (hlow : lowValue a = lowValue b) (hhigh : highValue a = highValue b) : a = b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons _ _ => simp at hl
  | cons x xs ih =>
    cases b with
    | nil => simp at hl
    | cons y ys =>
      have hl' : xs.length = ys.length := by simpa using hl
      have hx := ha x List.mem_cons_self
      have hy := hb y List.mem_cons_self
      have hxs : ∀ z ∈ xs, z ≤ 18 := fun z hz => ha z (List.mem_cons_of_mem x hz)
      have hys : ∀ z ∈ ys, z ≤ 18 := fun z hz => hb z (List.mem_cons_of_mem y hz)
      simp only [lowValue] at hlow
      rw [highValue_cons, highValue_cons, hl'] at hhigh
      have bx := highValue_lt xs hxs
      have byy := highValue_lt ys hys
      rw [hl'] at bx
      generalize 10 ^ ys.length = P at hhigh bx byy
      have hxy : x = y := by
        have : x = y ∨ x = y + 10 ∨ y = x + 10 := by omega
        rcases this with h | h | h
        · exact h
        · subst h
          rw [Nat.add_mul] at hhigh
          omega
        · subst h
          rw [Nat.add_mul] at hhigh
          omega
      subst hxy
      have hlow' : lowValue xs = lowValue ys := by omega
      have hhigh' : highValue xs = highValue ys := by omega
      rw [ih ys hl' hxs hys hlow' hhigh']

/-- One-sided padding step for injectivity. -/
theorem canonical_eq_le (c : Nat) (B₁ B₂ : List Nat) (hc : nonneutralPhase c)
    (h₁ : ∀ x ∈ B₁, x ≤ 18) (h₂ : ∀ x ∈ B₂, x ≤ 18)
    (hlast : B₂.getLast? ≠ some c) (hle : B₁.length ≤ B₂.length)
    (hz : zValue c B₁ = zValue c B₂)
    (hr : rhoNum c B₁ * 10 ^ B₂.length = rhoNum c B₂ * 10 ^ B₁.length) : B₁ = B₂ := by
  have hc18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  obtain ⟨m, hm⟩ : ∃ m, B₂.length = B₁.length + m := ⟨B₂.length - B₁.length, by omega⟩
  have hl : (B₁ ++ List.replicate m c).length = B₂.length := by simp [hm]
  have hpad : B₁ ++ List.replicate m c = B₂ := by
    apply eq_of_values _ _ hl
    · intro x hx
      rcases List.mem_append.mp hx with h | h
      · exact h₁ x h
      · rw [List.eq_of_mem_replicate h]; exact hc18
    · exact h₂
    · apply lowValue_of_zValue c _ _ hl
      rw [zValue_append_replicate, hz]
    · have hr' : rhoNum c (B₁ ++ List.replicate m c) = rhoNum c B₂ := by
        rw [rhoNum_append_replicate]
        rw [hm, Nat.pow_add] at hr
        apply Nat.eq_of_mul_eq_mul_right (Nat.pow_pos (by decide : 0 < 10) : 0 < 10 ^ B₁.length)
        rw [← hr, Nat.mul_comm (10 ^ m) (rhoNum c B₁), Nat.mul_assoc,
          Nat.mul_comm (10 ^ m) (10 ^ B₁.length)]
      unfold rhoNum at hr'
      omega
  cases m with
  | zero => simpa using hpad
  | succ m =>
    exfalso
    apply hlast
    rw [← hpad, List.replicate_succ', ← List.append_assoc, List.getLast?_append]
    simp

theorem last_ne_of_valid (c : Nat) (B : List Nat) (hv : validOuter { c := c, B := B } = true) :
    B.getLast? ≠ some c := by
  simp only [validOuter, Bool.and_eq_true] at hv
  obtain ⟨-, hl⟩ := hv
  intro h
  rw [h] at hl
  simp at hl

/-- **Injectivity.** A canonical exterior state is determined by its phase, its
centered value `zValue` and its real value `ρ`. -/
theorem observation_injective (c : Nat) (B₁ B₂ : List Nat) (hc : nonneutralPhase c)
    (hv₁ : validOuter { c := c, B := B₁ } = true) (hv₂ : validOuter { c := c, B := B₂ } = true)
    (hz : zValue c B₁ = zValue c B₂)
    (hr : rhoNum c B₁ * 10 ^ B₂.length = rhoNum c B₂ * 10 ^ B₁.length) : B₁ = B₂ := by
  have h₁ := entries_le_of_valid c B₁ hv₁
  have h₂ := entries_le_of_valid c B₂ hv₂
  rcases Nat.le_total B₁.length B₂.length with h | h
  · exact canonical_eq_le c B₁ B₂ hc h₁ h₂ (last_ne_of_valid c B₂ hv₂) h hz hr
  · exact (canonical_eq_le c B₂ B₁ hc h₂ h₁ (last_ne_of_valid c B₁ hv₁) h hz.symm hr.symm).symm

end Agent115.ExteriorFactorization
