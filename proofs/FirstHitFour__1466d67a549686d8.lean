import DelayedOverlapGate

/-!
Agent #12. Exact first positive hit four for every spacer length in the three
written tail families (2,5), (2,6), (3,5). No finite-range replacement is used.
Source: renewal_pass/tails/STATUS.md, the three first-hit-four timing rows.
The explicit decimal endpoint-string formulas are separate source claims.
-/
namespace P196.Agent12.FirstHitFour

set_option maxHeartbeats 4000000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate DecimalDelayBridge

/-- Exactly the three source core pairs; it is not defined by their hit time. -/
def Core (u v : Nat) : Prop :=
  (u = 2 ∧ v = 5) ∨ (u = 2 ∧ v = 6) ∨ (u = 3 ∧ v = 5)

theorem core_domain (r u v : Nat) (hr : 1 ≤ r) (h : Core u v) :
    Domain r 1 u v := by
  rcases h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
    unfold Domain <;> omega

/-- Outgoing carries for the returned word, indexed as incoming column carries.
The r=1 boundary is included without requiring a positive gap beyond the flank. -/
def tailCarry (r u v i : Nat) : Nat :=
  if i = r + 3 ∨ i = r + 5 ∨ i = r + 6 then 1
  else if i = r + 2 ∧ u = 3 then 1
  else if i = r + 4 ∧ v = 6 then 1
  else 0

theorem returned_carry (r u v : Nat) (hr : 1 ≤ r) (h : Core u v) :
    ∀ i, i ≤ 2*r+7 → carry (returned r 1 u v) i = tailCarry r u v i := by
  apply carry_certificate _ _ _
  · simp only [tailCarry]
    repeat (first | omega | split)
  · intro i hi
    rcases h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
      simp [returned, fiveWord, tailCarry] <;>
      repeat (first | omega | split)

theorem returned_no_overflow (r u v : Nat) (hr : 1 ≤ r) (h : Core u v) :
    carry (returned r 1 u v) (2*r+7) = 0 := by
  rw [returned_carry r u v hr h _ (Nat.le_refl _)]
  simp only [tailCarry]
  repeat (first | omega | split)

/-- After the third true normalization, every mirrored digit-pair sum is low. -/
theorem third_pairs_low (r u v : Nat) (hr : 1 ≤ r) (h : Core u v) :
    ∀ i, i < 2*r+7 → nextColumns (returned r 1 u v) (2*r+7) i ≤ 9 := by
  intro i hi
  simp only [nextColumns, returned_no_overflow r u v hr h, if_true,
    columnSum, reflected, output]
  rw [returned_carry r u v hr h i (by omega),
    returned_carry r u v hr h (2*r+7-1-i) (by omega)]
  rcases h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
    simp [returned, fiveWord, tailCarry] <;>
    repeat (first | omega | split)

/-- The fourth iterate is actually palindromic for every canonical realization. -/
theorem numeric_fourth_palindrome (n : Nat) (d : Nat → Nat) (r u v : Nat)
    (hr : 1 ≤ r) (h : Core u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = initial r 1 u v i) :
    Palindrome (orbit n 4) := by
  have hd := core_domain r u v hr h
  obtain ⟨e, he, herep⟩ := numeric_return n d r 1 u v hd hc hrep
  obtain ⟨f, hf, hfrep⟩ := representation_next (orbit n 2) e (returned r 1 u v)
    (2*r+7) he herep
  have hw : nextWidth (returned r 1 u v) (2*r+7) = 2*r+7 := by
    simp only [nextWidth, returned_no_overflow r u v hr h, if_true]
  rw [hw] at hf hfrep
  apply (PairDelayBridge.palindrome_iff_bad (orbit n 3) f
    (nextColumns (returned r 1 u v) (2*r+7)) (2*r+7) hf hfrep).mpr
  exact Or.inl (third_pairs_low r u v hr h)

/-- Exact first positive time, not merely a fourth-step hit. -/
theorem numeric_first_hit_four (n : Nat) (d : Nat → Nat) (r u v : Nat)
    (hr : 1 ≤ r) (h : Core u v) (hc : Canonical n d (2*r+7))
    (hrep : ∀ i, i < 2*r+7 → columnSum d (2*r+7) i = initial r 1 u v i) :
    FirstPositiveHit n 4 := by
  have hd := core_domain r u v hr h
  have hs := numeric_two_step_safety n d r 1 u v hd hc hrep
  have h3 : ¬ Palindrome (orbit n 3) := by
    intro hp
    have he := (numeric_third_palindrome_iff n d r 1 u v hd hc hrep).mp hp
    rcases h with ⟨hu, hv⟩ | ⟨hu, hv⟩ | ⟨hu, hv⟩ <;> omega
  refine ⟨by decide, numeric_fourth_palindrome n d r u v hr h hc hrep, ?_⟩
  intro k hk0 hk4
  have cases : k = 1 ∨ k = 2 ∨ k = 3 := by omega
  rcases cases with rfl | rfl | rfl
  · exact hs.1
  · exact hs.2
  · exact h3

/-- Each all-r theorem has an ordinary positive decimal realization. -/
theorem realized_first_hit_four (r u v : Nat) (hr : 1 ≤ r) (h : Core u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2*r+7) ∧
      (∀ i, i < 2*r+7 → columnSum d (2*r+7) i = initial r 1 u v i) ∧
      FirstPositiveHit n 4 := by
  obtain ⟨n, d, hn, hc, hrep, _⟩ := realized_safe_gate r 1 u v (core_domain r u v hr h)
  exact ⟨n, d, hn, hc, hrep, numeric_first_hit_four n d r u v hr h hc hrep⟩

end P196.Agent12.FirstHitFour
