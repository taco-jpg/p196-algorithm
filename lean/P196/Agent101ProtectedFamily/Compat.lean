import P196.Agent2SaturatedProfile.TemplateStep
import P196.Foundations.LychrelDigitSums
import P196.Foundations.PeriodObstructions

/-!
Agent #109 compatibility layer: the verbatim copies in `TemplateStep.lean`
coincide with Agent #8's `PeriodObstructions.lean` and with the accepted
`Lychrel196` semantics of `LychrelDigitSums.lean`; the main bridge theorems are
restated with the original constants.
-/

namespace Agent109.Compat

open Agent109

theorem zipAdd_eq (a b : Word) : Agent8.zipAdd a b = Agent109.zipAdd a b := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons x xs ih =>
    cases b with
    | nil => rfl
    | cons y ys => simp [Agent8.zipAdd, Agent109.zipAdd, ih]

theorem pair_eq (w : Word) : Agent8.pair w = Agent109.pair w := by
  simp [Agent8.pair, Agent109.pair, zipAdd_eq]

theorem normalize_eq (w : Word) (e : Nat) :
    Agent8.normalize w e = Agent109.normalize w e := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [Agent8.normalize, Agent109.normalize, ih]

theorem stepWord_eq (w : Word) : Agent8.stepWord w = Agent109.stepWord w := by
  simp [Agent8.stepWord, Agent109.stepWord, pair_eq, normalize_eq]

theorem template_eq (c : Nat) (B A C : Word) (g h : Nat) :
    Agent8.template c B A C g h = Agent109.template c B A C g h := rfl

theorem orbit_word_eq (w : Word) (k : Nat) : Agent8.orbit w k = Agent109.orbitWord w k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [Agent8.orbit, Agent109.orbitWord, ih, stepWord_eq]

theorem reverseFuel_eq (f n acc : Nat) :
    Lychrel196.reverseFuel f n acc = Agent109.reverseFuel f n acc := by
  induction f generalizing n acc with
  | zero => rfl
  | succ f ih => simp [Lychrel196.reverseFuel, Agent109.reverseFuel, ih]

theorem reverse10_eq (n : Nat) : Lychrel196.reverse10 n = Agent109.reverse10 n := by
  simp [Lychrel196.reverse10, Agent109.reverse10, reverseFuel_eq]

theorem step_eq (n : Nat) : Lychrel196.step n = Agent109.step n := by
  simp [Lychrel196.step, Agent109.step, reverse10_eq]

theorem palindrome_eq (n : Nat) : Lychrel196.Palindrome n ↔ Agent109.Palindrome n := by
  simp [Lychrel196.Palindrome, Agent109.Palindrome, reverse10_eq]

theorem orbit_eq (n k : Nat) : Lychrel196.orbit n k = Agent109.orbit n k := by
  induction k with
  | zero => rfl
  | succ k ih => simp [Lychrel196.orbit, Agent109.orbit, ih, step_eq]

/-! ## Restated bridge theorems with the original constants -/

/-- The mirrored pair word of the accepted `Lychrel196.step n` is
`Agent8.stepWord` of the pair word of `n`, for every natural `n`. -/
theorem pairWord_step (n : Nat) :
    pairWord (Lychrel196.step n) = Agent8.stepWord (pairWord n) := by
  rw [step_eq, stepWord_eq, Agent109.pairWord_step]

/-- `Agent8.orbit` on pair words is the accepted integer orbit. -/
theorem pairWord_orbit (n k : Nat) :
    pairWord (Lychrel196.orbit n k) = Agent8.orbit (pairWord n) k := by
  rw [orbit_eq, orbit_word_eq, Agent109.pairWord_orbit]

/-- Identity (8) with Agent #8's `stepWord` and `template`. -/
theorem stepWord_template (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    Agent8.stepWord (Agent8.template c B A C (g + 2) (h + 2)) =
      Agent8.template (tOf c + tOf c) (Br c B A C) (Ar c B A C) (Cr c B A C)
        (g + (data c B A C).γ) (h + (data c B A C).γ) := by
  rw [stepWord_eq, template_eq, template_eq, Agent109.stepWord_template c B A C g h hc hB hA hC]

/-- An ordinary integer whose pair word is a template steps, under the accepted
`Lychrel196.step`, to an integer whose pair word is the returned template. -/
theorem actual_template_step (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = Agent8.template c B A C (g + 2) (h + 2)) :
    pairWord (Lychrel196.step n) =
      Agent8.template (tOf c + tOf c) (Br c B A C) (Ar c B A C) (Cr c B A C)
        (g + (data c B A C).γ) (h + (data c B A C).γ) := by
  rw [step_eq]; exact Agent109.actual_template_step n c B A C g h hc hB hA hC hn

/-- **Exact word-level form of the decimal Lychrel property.** `n` is Lychrel in
the accepted sense iff `n` is not a palindrome and, at every time `k`, the
normalized word of Agent #8's orbit of `pairWord n` is not a list palindrome. -/
theorem isLychrel_iff (n : Nat) :
    Lychrel196.IsLychrel n ↔
      ¬ Lychrel196.Palindrome n ∧
        ∀ k, (Agent8.normalize (Agent8.orbit (pairWord n) k) 0).reverse ≠
          Agent8.normalize (Agent8.orbit (pairWord n) k) 0 := by
  have key : ∀ k, Lychrel196.Palindrome (Lychrel196.orbit n (k + 1)) ↔
      (Agent8.normalize (Agent8.orbit (pairWord n) k) 0).reverse =
        Agent8.normalize (Agent8.orbit (pairWord n) k) 0 := by
    intro k
    rw [palindrome_eq, orbit_eq, Agent109.orbit, step_palindrome_iff,
      Agent109.pairWord_orbit, orbit_word_eq, normalize_eq]
  constructor
  · intro h
    exact ⟨h 0, fun k hk => h (k + 1) ((key k).mpr hk)⟩
  · rintro ⟨h0, hk⟩ k
    cases k with
    | zero => exact h0
    | succ k => exact fun hp => hk k ((key k).mp hp)

end Agent109.Compat

#print axioms Agent109.Compat.pairWord_step
#print axioms Agent109.Compat.pairWord_orbit
#print axioms Agent109.Compat.stepWord_template
#print axioms Agent109.Compat.actual_template_step
#print axioms Agent109.Compat.isLychrel_iff
