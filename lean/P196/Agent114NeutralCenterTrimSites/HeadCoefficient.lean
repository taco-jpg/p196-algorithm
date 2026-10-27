import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Agent 114: exact center-head coefficients and the credited trim thresholds

These all-base formulas concern the unchanged A120 transition.  The overflow
head equivalence does not assume source symmetry.  For the nonoverflow trim
thresholds the head is explicitly assumed to equal the last coefficient;
no stronger symmetry hypothesis is needed in this module.
-/

namespace Agent114.NeutralCenterTrimSites

open Agent120.Neutral

private theorem normalized_head (b : Nat) (C : List Nat) (e c : Nat)
    (hh : C.head? = some c) :
    (norm b C e).1.head? = some ((c + e) % b) := by
  cases C with
  | nil => simp at hh
  | cons d Q =>
      have hd : d = c := by simpa using hh
      subst d
      simp [norm_cons]

/-- Exact raw center head in the overflow branch. -/
theorem nextC_head_overflow (b : Nat) (B Q : List Nat) (c : Nat)
    (hg : gam b B (c :: Q) = 1) :
    (nextC b B (c :: Q)).head? =
      some ((c + e1 b B) % b + yd b B (c :: Q)) := by
  simp [nextC, hg, DC, norm_cons]

/-- Exact raw center head without overflow when the source head and last
coefficient are both `c`.  The prefix normalization supplies the actual
carry entering that last coefficient. -/
theorem nextC_head_nooverflow (b : Nat) (B P : List Nat) (c : Nat)
    (hh : (P ++ [c]).head? = some c) (hg : gam b B (P ++ [c]) = 0) :
    (nextC b B (P ++ [c])).head? =
      some ((c + e1 b B) % b + (c + (norm b P (e1 b B)).2) % b) := by
  have hd : (DC b B (P ++ [c])).head? = some ((c + e1 b B) % b) :=
    normalized_head b (P ++ [c]) (e1 b B) c hh
  have hl : (DC b B (P ++ [c])).getLast? =
      some ((c + (norm b P (e1 b B)).2) % b) := by
    simp [DC, norm_append, norm_cons]
  rw [nextC, if_pos hg, List.head?_zipWith, hd, List.head?_reverse, hl]

private theorem overflow_head_arithmetic (b c e f : Nat)
    (hb2 : 2 ≤ b) (hc : c ≤ 2 * (b - 1))
    (he : e ≤ 1) (hf : f ≤ 1) (hflip : e ≠ f) :
    (c + e) % b + (b - 1) * (1 - f) = b - 1 ↔ c = b - 1 := by
  have hb : 0 < b := by omega
  have small (q : Nat) (hq : q < 2) : q = 0 ∨ q = 1 := by omega
  rcases (by omega : (e = 0 ∧ f = 1) ∨ (e = 1 ∧ f = 0)) with
    ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · simp only [Nat.add_zero, Nat.sub_self, Nat.mul_zero]
    constructor
    · intro h
      have hq : c / b < 2 := (Nat.div_lt_iff_lt_mul hb).2 (by omega)
      have hd := Nat.mod_add_div c b
      rcases small _ hq with hq0 | hq1
      · rw [h, hq0] at hd
        simp only [Nat.mul_zero, Nat.add_zero] at hd
        omega
      · rw [h, hq1] at hd
        simp only [Nat.mul_one] at hd
        omega
    · intro h
      subst c
      exact Nat.mod_eq_of_lt (by omega)
  · simp only [Nat.sub_zero, Nat.mul_one]
    constructor
    · intro h
      have hm : (c + 1) % b = 0 := by omega
      have hq : (c + 1) / b < 2 :=
        (Nat.div_lt_iff_lt_mul hb).2 (by omega)
      have hd := Nat.mod_add_div (c + 1) b
      rcases small _ hq with hq0 | hq1
      · rw [hm, hq0] at hd
        simp only [Nat.mul_zero, Nat.add_zero] at hd
        omega
      · rw [hm, hq1] at hd
        simp only [Nat.mul_one, Nat.zero_add] at hd
        omega
    · intro h
      subst c
      have hb1 : b - 1 + 1 = b := by omega
      simp [hb1]

/-- On overflow, the raw center starts with a neutral coefficient exactly
when its source does.  A source with empty center cannot satisfy `Hyp`. -/
theorem overflow_head_neutral_iff {b : Nat} {B C : List Nat}
    (h : Hyp b B C) (hg : gam b B C = 1) :
    (nextC b B C).head? = some (b - 1) ↔ C.head? = some (b - 1) := by
  cases C with
  | nil =>
      have hf := h.flip
      simp [e2] at hf
  | cons c Q =>
      have hc : c ≤ 2 * (b - 1) := h.boundC c (by simp)
      rw [nextC_head_overflow b B Q c hg]
      simpa only [List.head?_cons, Option.some.injEq, yd] using
        overflow_head_arithmetic b c (e1 b B) (e2 b B (c :: Q))
          h.base hc h.e1_le h.e2_le h.flip

/-- A nonneutral source with the same first and last coefficient can produce
a neutral raw head without overflow only at the two exact center thresholds. -/
theorem nooverflow_head_thresholds {b : Nat} {B P : List Nat} {c : Nat}
    (h : Hyp b B (P ++ [c])) (hh : (P ++ [c]).head? = some c)
    (hn : c ≠ b - 1) (hg : gam b B (P ++ [c]) = 0)
    (hhead : (nextC b B (P ++ [c])).head? = some (b - 1)) :
    (e1 b B = 0 ∧ 2 * c + (norm b P (e1 b B)).2 = 3 * b - 1) ∨
      (e1 b B = 1 ∧ 2 * c + (norm b P (e1 b B)).2 = b - 2) := by
  let t := (norm b P (e1 b B)).2
  have hb2 := h.base
  have hb : 0 < b := by omega
  have hc : c ≤ 2 * (b - 1) := h.boundC c (by simp)
  have hP : ∀ x ∈ P, x ≤ 2 * (b - 1) := by
    intro x hx
    exact h.boundC x (List.mem_append_left _ hx)
  have ht : t ≤ 1 := norm_carry_le_one b hb P (e1 b B) hP h.e1_le
  have h1 := h.e1_le
  have h2 := h.e2_le
  have hflip := h.flip
  have hecarry : (c + t) / b = e2 b B (P ++ [c]) := by
    simp [e2, norm_append, norm_cons, t]
  rw [nextC_head_nooverflow b B P c hh hg] at hhead
  have hs := Option.some.inj hhead
  change (c + e1 b B) % b + (c + t) % b = b - 1 at hs
  rcases (by omega : e1 b B = 0 ∨ e1 b B = 1) with he0 | he1
  · have hf : e2 b B (P ++ [c]) = 1 := by omega
    have hm := Nat.mod_add_div (c + t) b
    rw [hecarry, hf, Nat.mul_one] at hm
    have hcge : b ≤ c := by omega
    have hmc : c % b = c - b := by
      rw [Nat.mod_eq_sub_mod hcge, Nat.mod_eq_of_lt (by omega : c - b < b)]
    rw [he0, Nat.add_zero, hmc] at hs
    exact Or.inl ⟨he0, by change 2 * c + t = 3 * b - 1; omega⟩
  · have hf : e2 b B (P ++ [c]) = 0 := by omega
    have hm := Nat.mod_add_div (c + t) b
    rw [hecarry, hf, Nat.mul_zero, Nat.add_zero] at hm
    have hct : c + t < b := by
      have hm_lt := Nat.mod_lt (c + t) hb
      omega
    have hcr : c + 1 < b := by omega
    rw [he1, Nat.mod_eq_of_lt hcr, hm] at hs
    exact Or.inr ⟨he1, by change 2 * c + t = b - 2; omega⟩

end Agent114.NeutralCenterTrimSites

#print axioms Agent114.NeutralCenterTrimSites.nextC_head_overflow
#print axioms Agent114.NeutralCenterTrimSites.nextC_head_nooverflow
#print axioms Agent114.NeutralCenterTrimSites.overflow_head_neutral_iff
#print axioms Agent114.NeutralCenterTrimSites.nooverflow_head_thresholds
