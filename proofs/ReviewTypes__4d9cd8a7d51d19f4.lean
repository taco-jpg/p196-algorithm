import TwoDigitMain

/-! Independent reviewer probe (not part of the package). -/

#check @Agent113.TwoDigit.ancestry_bound_65
#check @Agent113.TwoDigit.no_196_thirteen
#check @Agent113.TwoDigit.no_196_thirteen_arith
#check @Agent113.TwoDigit.startsTwo_iff
#print Agent113.TwoDigit.PalindromeStartsTwo
#print Agent113.TwoDigit.StartsTwo
#print Agent113.TwoDigit.SharpAt
#print Lychrel196.orbit
#print Lychrel196.step
#print Lychrel196.reverse10
#print Lychrel196.reverseFuel
#print Lychrel196.Palindrome
#print DecimalDigits.Canonical

/-- ancestry_bound_65 restated by hand with no package definitions: if a
palindrome `P` (in the base-library sense `reverse10 P = P`) satisfies
`P / 10^k = 65` for some `k`, then no positive `A` reaches it in more than
six reverse-and-add steps. -/
example : ∀ A P t k : Nat, 0 < A → Lychrel196.reverse10 P = P → P / 10 ^ k = 65 →
    Lychrel196.orbit A t = P → t ≤ 6 := by
  intro A P t k hA hpal hk hrun
  exact Agent113.TwoDigit.ancestry_bound_65 A P t hA
    ⟨hpal, (Agent113.TwoDigit.startsTwo_iff 6 5 P).mpr
      ⟨by decide, by decide, by decide, k, by omega⟩⟩ hrun

/-- The requested direct restatement: the type of ancestry_bound_65 is
literally this. -/
example : ∀ A P t : Nat, 0 < A → Agent113.TwoDigit.PalindromeStartsTwo 6 5 P →
    Lychrel196.orbit A t = P → t ≤ 6 := by
  exact Agent113.TwoDigit.ancestry_bound_65

/-- Non-vacuity of the hypothesis family: the sharp witness satisfies it. -/
example : Agent113.TwoDigit.PalindromeStartsTwo 6 5 (Lychrel196.orbit 1203290 6) :=
  Agent113.TwoDigit.sharp_65.1

/-- Concrete values of orbit 196 and the 65-witness, kernel-evaluated. -/
example : Lychrel196.orbit 196 6 = 94039 ∧ Lychrel196.orbit 1203290 6 = 65477456 := by
  decide

/-- The 196 corollary restated in plain arithmetic form for t = every time. -/
example : ∀ t k : Nat, Lychrel196.reverse10 (Lychrel196.orbit 196 t) = Lychrel196.orbit 196 t →
    Lychrel196.orbit 196 t / 10 ^ k ≠ 65 := by
  intro t k hpal h
  exact Agent113.TwoDigit.no_196_thirteen_arith t k hpal (by simp [h])

#print axioms Agent113.TwoDigit.ancestry_bound_65
#print axioms Agent113.TwoDigit.no_196_thirteen
#print axioms Agent113.TwoDigit.no_196_thirteen_arith
