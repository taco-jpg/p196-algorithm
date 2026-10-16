import A124K5AllRows
import A124K5Short
import A124K5Initial
import Agent124LeadOne

/-! Leading-digit-1 prefix 119 from the combined five-column certificate.
The final overflow is excluded by the target digit 9 > 2
(`Agent124.LeadOne.no_overflow_of_digit_gt_two`). -/
namespace Agent124.CertK5
open Agent124.CodeCert Lychrel196 Agent124.PrefixK Agent124.PrefixR Agent124.LeadOne

/-- Every positive integer reaching a palindrome that begins 119 does so within 8 steps. -/
theorem ancestry_119 : ∀ A P t, 0 < A → PalStarts3 1 1 9 P → orbit A t = P → t ≤ 8 :=
  ancestry_bound_of_R' 5 1 1 9 7 (by decide) (Or.inr (Or.inr (by decide))) (R ranks)
    allRows short (initialBounded_of_all init_119)

/-- The ordinary 196 orbit never contains a palindrome beginning 119. -/
theorem no_196_119 : ∀ t, ¬ PalStarts3 1 1 9 (orbit 196 t) :=
  no_196_of_R' 5 1 1 9 7 (by decide) (Or.inr (Or.inr (by decide))) (by decide) (R ranks)
    allRows short (initialBounded_of_all init_119)

#print axioms ancestry_119
#print axioms no_196_119
end Agent124.CertK5
