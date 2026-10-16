import RhoCycleLemmas

/-!
Agent #34: exact arithmetic and empty-exterior controls for the README repair.
These checks do not prove stepNumeratorTarget, a telescope, or cycleOverflowTarget.
-/
namespace Agent34.PR107.ReadmeControl

open P196.Agent7.Finite Agent115.ExteriorFactorization Agent115.RhoCycle

theorem one_quotient_remainder (x D : Nat) (h : x / D = 1) :
    D + x % D = x := by
  have hdiv := Nat.mod_add_div x D
  simpa [h, Nat.add_comm] using hdiv

theorem gamma_empty_phase_ten :
    gamma { c := 10, B := [] } = 1 := by decide

theorem raw_high_empty_phase_ten :
    highValue (rawSucc 10 []) = 1 := by decide

theorem prior_formula_fails_on_empty_phase_ten :
    highValue (rawSucc 10 []) ≠ 2 := by decide

#print axioms one_quotient_remainder
#print axioms gamma_empty_phase_ten
#print axioms raw_high_empty_phase_ten
#print axioms prior_formula_fails_on_empty_phase_ten

#eval rawSucc 10 []
#eval outerNext { c := 10, B := [] }

end Agent34.PR107.ReadmeControl
