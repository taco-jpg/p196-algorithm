import P196.Agent5EvenBaseAbsorption.GeneralMomentAbsorption

namespace P196.Agent5.General.Filter
open Moment

theorem moment_empty (c : Int) : moment c [] = c := by
  simp [moment, altSum, wordSign, lengthSign]

theorem nonempty_of_zero_moment (m c : Int) (B : Word)
    (hc : 0<c ∧ c<2*(m+2)) (hz : moment c B % (2*(m+2))=0) : B≠[] := by
  intro hempty
  rw [hempty, moment_empty] at hz
  have h := Int.emod_eq_of_lt (by omega : 0≤c) hc.2
  omega

theorem decimal_last_column_iff (r x : Int) (P : Word) :
    moment (2*r) (P++[x])%22=0 ↔
      (x-r+wordSign P*altSum P)%11=0 := by
  simp only [moment, altSum_append, wordSign_append, altSum, Int.sub_zero,
    show wordSign [x] = -1 from rfl]
  rcases wordSign_bit P with h | h <;>
    simp only [h, Int.one_mul, Int.neg_one_mul, Int.neg_mul, Int.mul_neg,
      Int.mul_one, Int.neg_neg] <;> omega

theorem decimal_singleton_filter (r x : Int) (hr : 1≤r ∧ r≤8)
    (hx : 1≤x ∧ x≤18) (hz : moment (2*r) [x]%22=0) : x=r ∨ x=r+11 := by
  simp only [moment, altSum, Int.sub_zero, show wordSign [x] = -1 from rfl,
    Int.neg_one_mul] at hz
  omega

theorem individual_gains_divisible_nine (G dg dh : Int)
    (hG : G%18=0) (hw : G=2*(dg+dh)) (hd : (dg-dh)%9=0) :
    dg%9=0 ∧ dh%9=0 := by omega

theorem guarded_six_phase_gain_consequences (P G dg dh : Int)
    (hG : G%18=0) (hw : G=2*(dg+dh)) (hd : (dg-dh)%9=0)
    (hp : 2*G≤P) (hpos : 0<G) (hg : 0≤dg) (hh : 0≤dh) :
    dg%9=0 ∧ dh%9=0 ∧ (dg=0 ∨ 9≤dg) ∧ (dh=0 ∨ 9≤dh) ∧ 9≤dg+dh ∧ 36≤P := by
  have hi := individual_gains_divisible_nine G dg dh hG hw hd
  omega

theorem both_gaps_grow_period_at_least_72 (P G dg dh : Int)
    (hG : G%18=0) (hw : G=2*(dg+dh)) (hd : (dg-dh)%9=0)
    (hp : 2*G≤P) (hg : 0<dg) (hh : 0<dh) : 72≤P := by
  have hi := individual_gains_divisible_nine G dg dh hG hw hd
  omega

theorem period_below_72_forces_stationary_gap (P G dg dh : Int)
    (hG : G%18=0) (hw : G=2*(dg+dh)) (hd : (dg-dh)%9=0)
    (hp : 2*G≤P) (hpos : 0<G) (hg : 0≤dg) (hh : 0≤dh) (hshort : P<72) :
    G=18 ∧ ((dg=0 ∧ dh=9) ∨ (dg=9 ∧ dh=0)) := by
  have hi := individual_gains_divisible_nine G dg dh hG hw hd
  omega

theorem modulus44_counterexample :
    exteriorOverflow 9 2 [9,10]=1 ∧ nextExterior 9 2 [9,10]=[10,0,3] ∧
    moment 2 [9,10]=0 ∧ moment 4 [10,0,3]=22 := by decide

#print axioms modulus44_counterexample
#print axioms both_gaps_grow_period_at_least_72
#print axioms period_below_72_forces_stationary_gap
#print axioms moment_empty
#print axioms nonempty_of_zero_moment
#print axioms decimal_last_column_iff
#print axioms decimal_singleton_filter
#print axioms individual_gains_divisible_nine
#print axioms guarded_six_phase_gain_consequences

end P196.Agent5.General.Filter
