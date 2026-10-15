import ReturnCertificate
import LychrelDigitSums

/-!
The actual exterior coefficient of a return certificate follows the decimal
carry transition, even when the exterior is empty or trimming is nonmaximal.
The finite outer-column potentials give an unconditional carry budget for an
accepted closed certificate whose initial exterior is canonical.
-/

namespace Agent110.CarryBudget

open Agent109 Agent109.Cert

def exterior (s : State) : Nat := s.B.head?.getD s.c

/-- Exact one-column decimal update, with the incoming carry displayed. -/
def OuterStep (a b γ : Nat) : Prop :=
  ∃ e, e ≤ 1 ∧ γ = (a + e) / 10 ∧
    b = if γ = 0 then 2 * a + e else a % 10 + 1

theorem exterior_le (s : State) (hc : Phase s.c) (hB : Bounded s.B) :
    exterior s ≤ 18 := by
  cases he : s.B with
  | nil => simp [exterior, he]; exact Nat.le_trans hc.2.1 (by decide)
  | cons b bs =>
    have hb := hB b (by simp [he])
    simpa [exterior, he] using hb

theorem exterior_pos (s : State) (hc : Phase s.c)
    (hp : ∀ b, s.B.head? = some b → 0 < b) : 0 < exterior s := by
  cases he : s.B with
  | nil => simpa [exterior, he] using hc.1
  | cons b bs => simpa [exterior, he] using hp b (by simp [he])

theorem trimmed_head (w B : Word) (c j a : Nat)
    (hw : w.head? = some a) (ht : w = B ++ List.replicate j c) :
    B.head?.getD c = a := by
  cases B with
  | cons b bs => simp_all
  | nil =>
    cases j with
    | zero => simp_all
    | succ j => simp_all [List.replicate_succ]

theorem raw_exterior_step (c : Nat) (B A C : Word)
    (hc : Phase c) (hB : Bounded B) :
    ∃ b, (Br c B A C).head? = some b ∧
      OuterStep (B.head?.getD c) b (data c B A C).γ := by
  cases B with
  | nil =>
    have hc1 := hc.1
    have hc2 := hc.2.1
    have hc9 := hc.2.2
    by_cases hk : 10 ≤ c
    · refine ⟨c - 10 + 1, ?_, ?_⟩
      · simp [Br, data, norm, u0, kOf, hk, zipAdd]
      · refine ⟨1, by omega, ?_, ?_⟩
        · simp [data, norm, kOf, hk]; omega
        · simp [data, norm, kOf, hk]; omega
    · refine ⟨2 * c, ?_, ?_⟩
      · simp [Br, data, norm, u0, kOf, hk, zipAdd, tOf]; omega
      · refine ⟨0, by omega, ?_, ?_⟩
        · simp [data, norm, kOf, hk]; omega
        · simp [data, norm, kOf, hk]
  | cons a as =>
    let e := (norm as.reverse (kOf c)).2
    have he : e ≤ 1 := by
      apply norm_carry_le
      · apply bounded_reverse
        intro x hx; exact hB x (by simp [hx])
      · unfold kOf; split <;> omega
    have hg : (data c (a :: as) A C).γ = (a + e) / 10 := by
      simp [data, List.reverse_cons, norm_append, norm, e]
    have hr : (data c (a :: as) A C).DRB.reverse =
        (a + e) % 10 :: (norm as.reverse (kOf c)).1.reverse := by
      simp [data, List.reverse_cons, norm_append, norm, e]
    by_cases hγ : (data c (a :: as) A C).γ = 0
    · have ha : a + e < 10 := by omega
      refine ⟨2 * a + e, ?_, ?_⟩
      · simp only [Br, if_pos hγ, hr]
        simp [data, norm, zipAdd]
        omega
      · exact ⟨e, he, hg, by simp [hγ]⟩
    · refine ⟨a % 10 + 1, ?_, ?_⟩
      · simp only [Br, if_neg hγ]
        simp [data, norm, zipAdd]
      · exact ⟨e, he, hg, by simp [hγ]⟩

/-- The certificate's arbitrary suffix trimming preserves the actual outer
coefficient; maximal trimming is not an assumption. -/
theorem local_outer_step (s s' : State) (L L' : Link)
    (hl : LocalOK s s' L L') : OuterStep (exterior s) (exterior s') (gam s) := by
  obtain ⟨b, hb, hs⟩ := raw_exterior_step s.c s.B s.A s.C hl.1 hl.2.1
  have ht := trimmed_head (Br s.c s.B s.A s.C) s'.B s'.c L.j b hb hl.2.2.2.2.2.1
  simpa [exterior, gam, ht] using hs

theorem outer_step_positive (a b γ : Nat) (ha : 0 < a) (hs : OuterStep a b γ) :
    0 < b := by
  obtain ⟨e, he, hγ, hb⟩ := hs
  split at hb <;> omega

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
/-- The two previously defined exact-column potentials, checked on all legal
outer coefficients and both internal carry bits. -/
theorem outer_potential_table : ∀ a : Fin 19, ∀ e : Fin 2, 0 < a.val →
    let γ := (a.val + e.val) / 10
    let b := if γ = 0 then 2 * a.val + e.val else a.val % 10 + 1
    DecimalWidthGrowth.lowerPotential b + 1 ≤
        DecimalWidthGrowth.lowerPotential a.val + 4 * γ ∧
      CarryHistory.outerPotential b + 1 + 2 * γ ≤
        CarryHistory.outerPotential a.val + 2 := by decide

theorem outer_potential_step (a b γ : Nat) (ha : 0 < a) (ha18 : a ≤ 18)
    (hs : OuterStep a b γ) :
    DecimalWidthGrowth.lowerPotential b + 1 ≤
        DecimalWidthGrowth.lowerPotential a + 4 * γ ∧
      CarryHistory.outerPotential b + 1 + 2 * γ ≤
        CarryHistory.outerPotential a + 2 := by
  obtain ⟨e, he, hγ, hb⟩ := hs
  have ht := outer_potential_table ⟨a, by omega⟩ ⟨e, by omega⟩ ha
  simpa only [hγ, hb] using ht

def count (g : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => count g n + g n

def carryCount (cert : Certificate) : Nat := count (fun i => gam (cert.st i)) cert.P

theorem exterior_positive_along (cert : Certificate) (hv : Valid cert)
    (h0 : 0 < exterior (cert.st 0)) :
    ∀ i, i ≤ cert.P → 0 < exterior (cert.st (i % cert.P)) := by
  intro i
  induction i with
  | zero => intro _; simpa using h0
  | succ i ih =>
    intro hi
    have hiP : i < cert.P := by omega
    have hprev := ih (by omega)
    rw [Nat.mod_eq_of_lt hiP] at hprev
    have hs := local_outer_step _ _ _ _ (hv.2 i hiP)
    exact outer_step_positive _ _ _ hprev hs

/-- Telescope both finite potentials around the actual certificate exterior.
The only initial assumption is positivity of its canonical exterior. -/
theorem certificate_carry_budget_of_positive (cert : Certificate) (hv : Valid cert)
    (h0 : 0 < exterior (cert.st 0)) :
    0 < carryCount cert ∧ 2 * carryCount cert ≤ cert.P ∧
      cert.P ≤ 4 * carryCount cert := by
  let a := fun i => exterior (cert.st (i % cert.P))
  let g := fun i => gam (cert.st i)
  have hs : ∀ i, i < cert.P →
      DecimalWidthGrowth.lowerPotential (a (i + 1)) + 1 ≤
          DecimalWidthGrowth.lowerPotential (a i) + 4 * g i ∧
        CarryHistory.outerPotential (a (i + 1)) + 1 + 2 * g i ≤
          CarryHistory.outerPotential (a i) + 2 := by
    intro i hi
    have hl := hv.2 i hi
    have hp := exterior_positive_along cert hv h0 i (by omega)
    have hb := exterior_le (cert.st i) hl.1 hl.2.1
    have hstep := local_outer_step _ _ _ _ hl
    simp only [Nat.mod_eq_of_lt hi] at hp
    simpa only [a, g, Nat.mod_eq_of_lt hi] using
      outer_potential_step _ _ _ hp hb hstep
  have ht : ∀ n, n ≤ cert.P →
      DecimalWidthGrowth.lowerPotential (a n) + n ≤
          DecimalWidthGrowth.lowerPotential (a 0) + 4 * count g n ∧
        CarryHistory.outerPotential (a n) + n + 2 * count g n ≤
          CarryHistory.outerPotential (a 0) + 2 * n := by
    intro n
    induction n with
    | zero => intro _; simp [count]
    | succ n ih =>
      intro hn
      have hp := ih (by omega)
      have hn := hs n (by omega)
      simp only [count]
      omega
  have h := ht cert.P (by omega)
  have hc : a cert.P = a 0 := by simp [a]
  rw [hc] at h
  change 0 < count g cert.P ∧ 2 * count g cert.P ≤ cert.P ∧
    cert.P ≤ 4 * count g cert.P
  have hP := hv.1
  omega

/-- Admissibility supplies precisely the canonical initial exterior needed by
the actual decimal transition, and no orbit growth hypothesis is assumed. -/
theorem certificate_carry_budget (cert : Certificate) (hv : Valid cert)
    (H M : Word) (ha : Admissible0 cert H M) :
    0 < carryCount cert ∧ 2 * carryCount cert ≤ cert.P ∧
      cert.P ≤ 4 * carryCount cert := by
  apply certificate_carry_budget_of_positive cert hv
  exact exterior_pos _ (hv.2 0 hv.1).1 ha.2.2.2

end Agent110.CarryBudget

#print axioms Agent110.CarryBudget.exterior_le
#print axioms Agent110.CarryBudget.exterior_pos
#print axioms Agent110.CarryBudget.trimmed_head
#print axioms Agent110.CarryBudget.raw_exterior_step
#print axioms Agent110.CarryBudget.local_outer_step
#print axioms Agent110.CarryBudget.outer_step_positive
#print axioms Agent110.CarryBudget.outer_potential_table
#print axioms Agent110.CarryBudget.outer_potential_step
#print axioms Agent110.CarryBudget.exterior_positive_along
#print axioms Agent110.CarryBudget.certificate_carry_budget_of_positive
#print axioms Agent110.CarryBudget.certificate_carry_budget
