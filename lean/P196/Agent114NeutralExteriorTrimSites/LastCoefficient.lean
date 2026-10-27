import P196.Drafts.Agent120NeutralBandCalibration.A120Template
import P196.Drafts.Agent110TwoStepReturn.ZipTail

/-!
# Agent 114: terminal exterior coefficients at the unchanged A120 transition

These are the exact all-base terminal formulas used in Agent 7's paper trim
gates.  The proofs reuse the existing generic terminal zip lemma and the A120
normalizer.  Empty exteriors are included in the overflow boundary equivalence.
No center symmetry, certificate instance, or decimal obstruction is asserted.
-/

namespace Agent114.NeutralExteriorTrimSites

open Agent120.Neutral

private theorem DB_snoc (b : Nat) (P : List Nat) (z : Nat) :
    DB b (P ++ [z]) =
      (norm b P 0).1 ++ [(z + (norm b P 0).2) % b] := by
  simp [DB, norm_append, norm_cons]

private theorem DR_reverse_snoc (b : Nat) (P C : List Nat) (z : Nat) :
    (DR b (P ++ [z]) C).reverse =
      (norm b P.reverse ((z + e2 b (P ++ [z]) C) / b)).1.reverse ++
        [(z + e2 b (P ++ [z]) C) % b] := by
  simp [DR, List.reverse_append, norm_cons]

/-- Exact final exterior coefficient in the nonoverflow branch. -/
theorem nextB_last_nooverflow (b : Nat) (P C : List Nat) (z : Nat)
    (hg : gam b (P ++ [z]) C = 0) :
    (nextB b (P ++ [z]) C).getLast? =
      some ((z + (norm b P 0).2) % b + (z + e2 b (P ++ [z]) C) % b) := by
  rw [nextB, if_pos hg, DB_snoc, DR_reverse_snoc]
  exact Agent110.TwoStepZip.zipWith_add_terminal _ _ _ _ (by simp [norm_length])

/-- Exact final exterior coefficient in the overflow branch. -/
theorem nextB_last_overflow (b : Nat) (P C : List Nat) (z : Nat)
    (hg : gam b (P ++ [z]) C = 1) :
    (nextB b (P ++ [z]) C).getLast? =
      some (xd b (P ++ [z]) + (z + e2 b (P ++ [z]) C) % b) := by
  rw [nextB, if_neg (by omega : gam b (P ++ [z]) C ≠ 0), DR_reverse_snoc]
  simpa only [List.cons_append] using
    Agent110.TwoStepZip.zipWith_add_terminal
      (DB b (P ++ [z]))
      (1 :: (norm b P.reverse ((z + e2 b (P ++ [z]) C) / b)).1.reverse)
      (xd b (P ++ [z])) ((z + e2 b (P ++ [z]) C) % b)
      (by simp [length_DB, norm_length])

private theorem overflow_digit_neutral_iff (b z e f : Nat)
    (hb2 : 2 ≤ b) (hz : z ≤ 2 * (b - 1))
    (he : e ≤ 1) (hf : f ≤ 1) (hflip : e ≠ f) :
    (b - 1) * (1 - e) + (z + f) % b = b - 1 ↔ z = b - 1 := by
  have hb : 0 < b := by omega
  have small (q : Nat) (hq : q < 2) : q = 0 ∨ q = 1 := by omega
  rcases (by omega : (e = 0 ∧ f = 1) ∨ (e = 1 ∧ f = 0)) with
    ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · simp only [Nat.sub_zero, Nat.mul_one]
    constructor
    · intro h
      have hm : (z + 1) % b = 0 := by omega
      have hq : (z + 1) / b < 2 :=
        (Nat.div_lt_iff_lt_mul hb).2 (by omega)
      have hd := Nat.mod_add_div (z + 1) b
      rcases small _ hq with hq0 | hq1
      · rw [hm, hq0] at hd
        simp only [Nat.mul_zero, Nat.add_zero] at hd
        omega
      · rw [hm, hq1] at hd
        simp only [Nat.mul_one, Nat.zero_add] at hd
        omega
    · intro h
      subst z
      have hb1 : b - 1 + 1 = b := by omega
      simp [hb1]
  · simp only [Nat.sub_self, Nat.mul_zero, Nat.zero_add, Nat.add_zero]
    constructor
    · intro h
      have hq : z / b < 2 := (Nat.div_lt_iff_lt_mul hb).2 (by omega)
      have hd := Nat.mod_add_div z b
      rcases small _ hq with hq0 | hq1
      · rw [h, hq0] at hd
        simp only [Nat.mul_zero, Nat.add_zero] at hd
        omega
      · rw [h, hq1] at hd
        simp only [Nat.mul_one] at hd
        omega
    · intro h
      subst z
      exact Nat.mod_eq_of_lt (by omega)

/-- Overflow has a neutral final coefficient exactly when its source does.
The optional-last formulation also covers an empty exterior. -/
theorem overflow_last_neutral_iff {b : Nat} {B C : List Nat}
    (h : Hyp b B C) (hg : gam b B C = 1) :
    (nextB b B C).getLast? = some (b - 1) ↔ B.getLast? = some (b - 1) := by
  cases hr : B.reverse with
  | nil =>
      have hB : B = [] := List.reverse_eq_nil_iff.mp hr
      subst B
      simp [nextB, hg, DB, DR, xd, e1]
  | cons z Q =>
      have hB : B = Q.reverse ++ [z] := by
        simpa using congrArg List.reverse hr
      rw [hB] at h hg ⊢
      have hz : z ≤ 2 * (b - 1) := h.boundB z (by simp)
      rw [nextB_last_overflow b Q.reverse C z hg]
      simpa only [List.getLast?_append, List.getLast?_singleton, Option.some_or,
        Option.some.injEq, xd] using
        overflow_digit_neutral_iff b z (e1 b (Q.reverse ++ [z]))
          (e2 b (Q.reverse ++ [z]) C) h.base hz h.e1_le h.e2_le h.flip

/-- A nonneutral source endpoint can create a neutral raw endpoint without
overflow only at the two exact coefficient/carry thresholds. -/
theorem nooverflow_last_thresholds {b : Nat} {P C : List Nat} {z : Nat}
    (h : Hyp b (P ++ [z]) C) (hn : z ≠ b - 1)
    (hg : gam b (P ++ [z]) C = 0)
    (hlast : (nextB b (P ++ [z]) C).getLast? = some (b - 1)) :
    (e1 b (P ++ [z]) = 0 ∧ 2 * z + (norm b P 0).2 = b - 2) ∨
      (e1 b (P ++ [z]) = 1 ∧ 2 * z + (norm b P 0).2 = 3 * b - 1) := by
  let t := (norm b P 0).2
  have hb2 := h.base
  have hb : 0 < b := by omega
  have hz : z ≤ 2 * (b - 1) := h.boundB z (by simp)
  have hP : ∀ x ∈ P, x ≤ 2 * (b - 1) := by
    intro x hx
    exact h.boundB x (List.mem_append_left _ hx)
  have ht : t ≤ 1 := norm_carry_le_one b hb P 0 hP (by omega)
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hflip := h.flip
  have hecarry : (z + t) / b = e1 b (P ++ [z]) := by
    simp [e1, norm_append, norm_cons, t]
  rw [nextB_last_nooverflow b P C z hg] at hlast
  have hs := Option.some.inj hlast
  change (z + t) % b + (z + e2 b (P ++ [z]) C) % b = b - 1 at hs
  rcases (by omega : e1 b (P ++ [z]) = 0 ∨ e1 b (P ++ [z]) = 1) with he0 | he1
  · have hf : e2 b (P ++ [z]) C = 1 := by omega
    have hm := Nat.mod_add_div (z + t) b
    rw [hecarry, he0, Nat.mul_zero, Nat.add_zero] at hm
    have hzt : z + t < b := by
      have hm_lt := Nat.mod_lt (z + t) hb
      omega
    have hzr : z + 1 < b := by omega
    rw [hf, hm, Nat.mod_eq_of_lt hzr] at hs
    exact Or.inl ⟨he0, by change 2 * z + t = b - 2; omega⟩
  · have hf : e2 b (P ++ [z]) C = 0 := by omega
    have hm := Nat.mod_add_div (z + t) b
    rw [hecarry, he1, Nat.mul_one] at hm
    have hzge : b ≤ z := by omega
    have hmz : z % b = z - b := by
      rw [Nat.mod_eq_sub_mod hzge, Nat.mod_eq_of_lt (by omega : z - b < b)]
    rw [hf, Nat.add_zero, hmz] at hs
    exact Or.inr ⟨he1, by change 2 * z + t = 3 * b - 1; omega⟩

end Agent114.NeutralExteriorTrimSites

#print axioms Agent114.NeutralExteriorTrimSites.nextB_last_nooverflow
#print axioms Agent114.NeutralExteriorTrimSites.nextB_last_overflow
#print axioms Agent114.NeutralExteriorTrimSites.overflow_last_neutral_iff
#print axioms Agent114.NeutralExteriorTrimSites.nooverflow_last_thresholds
