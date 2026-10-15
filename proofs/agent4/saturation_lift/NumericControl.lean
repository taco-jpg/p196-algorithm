import ActualWordStrip

/-! A real integer witness for the width-one, one-pair endpoint.
It reaches a palindrome on the third update, so it is not a Lychrel witness. -/
namespace P196.Agent4.TemporalStrip.NumericControl
open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196
open P196.Agent4.TemporalStrip.ActualWord

def digits (i : Nat) : Nat := if i<3 then 0 else if i<7 then 6 else 0

theorem canonical_control : Canonical 6666000 digits 7 := by
  refine ⟨by decide,?_,by decide,by decide⟩
  intro i hi
  unfold digits
  split <;> (try split) <;> omega

theorem one_pair_clock : Alternates (columnSum digits 7) 7 1 := by
  intro j hj
  have h : j=0 := by omega
  subst j
  constructor <;> decide

theorem one_pair_band : Band (columnSum digits 7) 7 1 1 6 12 := by
  intro j hj
  have h : j=0 := by omega
  subst j
  repeat constructor <;> decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem exact_numeric_control :
    orbit 6666000 1=6672666 ∧ orbit 6666000 2=13335432 ∧
    orbit 6666000 3=36788763 ∧
    ¬ Palindrome 6672666 ∧ ¬ Palindrome 13335432 ∧ Palindrome 36788763 := by
  decide +kernel

theorem width_one_bound_attained :
    Canonical 6666000 digits 7 ∧
    Alternates (columnSum digits 7) 7 1 ∧ Band (columnSum digits 7) 7 1 1 6 12 ∧
    (1:Nat)=2*1-1 :=
  ⟨canonical_control,one_pair_clock,one_pair_band,rfl⟩

#print axioms canonical_control
#print axioms one_pair_clock
#print axioms one_pair_band
#print axioms exact_numeric_control
#print axioms width_one_bound_attained
end P196.Agent4.TemporalStrip.NumericControl
