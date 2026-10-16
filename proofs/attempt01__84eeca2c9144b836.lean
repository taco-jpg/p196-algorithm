import ReturnCertificate

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
      · simp [Br, hγ, hr, data, norm, zipAdd]
        omega
      · exact ⟨e, he, hg, by simp [hγ]⟩
    · refine ⟨a % 10 + 1, ?_, ?_⟩
      · simp [Br, hγ, data, norm, zipAdd]
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

end Agent110.CarryBudget

#print axioms Agent110.CarryBudget.exterior_le
#print axioms Agent110.CarryBudget.exterior_pos
#print axioms Agent110.CarryBudget.trimmed_head
#print axioms Agent110.CarryBudget.raw_exterior_step
#print axioms Agent110.CarryBudget.local_outer_step
#print axioms Agent110.CarryBudget.outer_step_positive
