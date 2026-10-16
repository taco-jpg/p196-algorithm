import Lychrel196Research
namespace CarryNormalizationSharpness
open DecimalDigits FoldedDecimal Lychrel196
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

/-- The complete five-digit carry trace is 0,0,0,1,1,1. -/
def slowCarry (i : Nat) : Nat := if i<3 then 0 else 1

/-- This carry trace forces only five possible first reverse-and-add values. -/
theorem five_first_values (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 5)
    (hc : ∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) :
    step n=100099 ∨ step n=100299 ∨ step n=100499 ∨
      step n=100699 ∨ step n=100899 := by
  let q := columnSum d 5
  have c1 : carry q 1=0 := hc 1 (by decide)
  have c2 : carry q 2=0 := hc 2 (by decide)
  have c3 : carry q 3=1 := hc 3 (by decide)
  have c4 : carry q 4=1 := hc 4 (by decide)
  have c5 : carry q 5=1 := hc 5 (by decide)
  have q4 : q 4=q 0 := by simp [q,columnSum,reflected,Nat.add_comm]
  have q3 : q 3=q 1 := by simp [q,columnSum,reflected,Nat.add_comm]
  have q2 : q 2=2*d 2 := by simp [q,columnSum,reflected]; omega
  have e1 : (q 0+0)/10=0 := c1
  have e2 : (q 1+carry q 1)/10=0 := c2
  have e3 : (q 2+carry q 2)/10=1 := c3
  have e4 : (q 3+carry q 3)/10=1 := c4
  have e5 : (q 4+carry q 4)/10=1 := c5
  rw [c1] at e2
  rw [c2,q2] at e3
  rw [c3,q3] at e4
  rw [c4,q4] at e5
  have q0 : q 0=9 := by omega
  have q1 : q 1=9 := by omega
  have dc : d 2≤9 := hcan.2.1 2 (by decide)
  have sv := step_eq_word_value n d q 5 hcan (fun _ _ => rfl)
  have sn : step n=99099+200*d 2 := by
    rw [sv]
    simp only [value]
    rw [q4,q3,q2,q1,q0]
    omega
  omega

theorem five_values_checked :
    noPalindromeFor 3 100099=true ∧ noPalindromeFor 3 100299=true ∧
    noPalindromeFor 3 100499=true ∧ noPalindromeFor 3 100699=true ∧
    noPalindromeFor 3 100899=true := by decide

/-- Every positive five-digit integer with this carry trace avoids a palindrome
for its first three positive-time reverse-and-add iterates. -/
theorem slow_carry_requires_at_least_four (n : Nat) (d : Nat → Nat)
    (hcan : Canonical n d 5)
    (hc : ∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) :
    ∀ k, 0<k → k≤3 → ¬ Palindrome (orbit n k) := by
  have hv := five_first_values n d hcan hc
  have hf : noPalindromeFor 3 (step n)=true := by
    rcases hv with h|h|h|h|h <;> rw [h]
    · exact five_values_checked.1
    · exact five_values_checked.2.1
    · exact five_values_checked.2.2.1
    · exact five_values_checked.2.2.2.1
    · exact five_values_checked.2.2.2.2
  intro k hk hmax
  have hn := noPalindromeFor_sound 3 (step n) hf (k-1) (by omega)
  rw [orbit_from_step] at hn
  have he : k-1+1=k := by omega
  simpa only [he] using hn

def witnessDigit (i : Nat) : Nat := if i=2 then 5 else if 3≤i then 9 else 0

theorem witness_canonical : Canonical 99500 witnessDigit 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold witnessDigit
  split
  · omega
  · split <;> omega

 theorem witness_carries : ∀ i, i≤5 → carry (columnSum witnessDigit 5) i=slowCarry i := by
  intro i hi
  have he : i=0 ∨ i=1 ∨ i=2 ∨ i=3 ∨ i=4 ∨ i=5 := by omega
  rcases he with rfl|rfl|rfl|rfl|rfl|rfl <;> decide

theorem witness_reaches_at_four :
    orbit 99500 1=100099 ∧ orbit 99500 2=1090100 ∧
    orbit 99500 3=1101001 ∧ orbit 99500 4=2102012 ∧
    Palindrome (orbit 99500 4) := by decide

theorem four_is_optimal :
    (∃ n d, 0<n ∧ Canonical n d 5 ∧
      (∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) ∧
      Palindrome (orbit n 4)) ∧
    (∀ n d, Canonical n d 5 →
      (∀ i, i≤5 → carry (columnSum d 5) i=slowCarry i) →
      ∀ k, 0<k → k≤3 → ¬ Palindrome (orbit n k)) := by
  exact ⟨⟨99500,witnessDigit,by decide,witness_canonical,witness_carries,
    witness_reaches_at_four.2.2.2.2⟩,slow_carry_requires_at_least_four⟩

#print axioms five_first_values
#print axioms slow_carry_requires_at_least_four
#print axioms four_is_optimal
end CarryNormalizationSharpness
