/- Agent #104 finite-list partition of the frozen 620 instance.
Agent #124's original semantic checker and enumerations are unchanged. -/
import Agent104Prefix620RowsAll
import Agent104Prefix620ShortAll
import Agent104Prefix620InitialAll

namespace Agent104.Prefix620
open Agent124.CodeCert Agent124.PrefixK Agent124.PrefixR
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Leading decimal digits 620 in the exact canonical numeral. -/
abbrev Starts620 (P : Nat) : Prop := Starts3 6 2 0 P

/-- Decimal palindromes whose leading three digits are 620. -/
abbrev PalindromeStarts620 (P : Nat) : Prop := PalStarts3 6 2 0 P

/-- Expose the numeric meaning of the target predicate. -/
theorem palindromeStarts620_iff (P : Nat) :
    PalindromeStarts620 P ↔ Lychrel196.Palindrome P ∧
      ∃ e W, DecimalDigits.Canonical P e W ∧ 3 ≤ W ∧
        e (W - 1) = 6 ∧ e (W - 2) = 2 ∧ e (W - 3) = 0 := Iff.rfl

/-- Any positive seed reaches a 620-prefix palindrome only within 12 additions.
This is the certified upper bound; no optimality claim is made. -/
theorem ancestry_bound12 :
    ∀ A P t, 0 < A → PalindromeStarts620 P → Lychrel196.orbit A t = P → t ≤ 12 :=
  ancestry_bound_of_R 7 6 2 0 11 (by decide +kernel) (by decide +kernel)
    (R ranks) allRows short initialBounded

/-- No iterate from 196 is a decimal palindrome beginning 620. -/
theorem no_196_620_palindrome :
    ∀ t, ¬ PalindromeStarts620 (Lychrel196.orbit 196 t) :=
  no_196_of_R 7 6 2 0 11 (by decide +kernel) (by decide +kernel) (by decide +kernel)
    (R ranks) allRows short initialBounded

#print axioms palindromeStarts620_iff
#print axioms ancestry_bound12
#print axioms no_196_620_palindrome

end Agent104.Prefix620
