import ActualHighReturn

-- Explicit assignments verify the intended quantifiers and assumptions.
example (n R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R → Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (2 * j))) :
    R ≤ 3 := Agent105.ActualHighReturn.numeric_high_returns_le_three n R hn hH

example (n start R : Nat) (hn : 0 < n)
    (hH : ∀ j, j ≤ R →
      Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) :
    R ≤ 3 := Agent105.ActualHighReturn.numeric_high_returns_after_le_three n start R hn hH

example (n start : Nat) (hn : 0 < n) :
    ¬ (∀ j, Agent105.NumericHigh.NumericHigh (Lychrel196.orbit n (start + 2 * j))) :=
  Agent105.ActualHighReturn.no_perpetual_high_returns n start hn

set_option pp.universes true in
#check Agent105.ActualHighReturn.numeric_high_returns_le_three
set_option pp.universes true in
#check Agent105.ActualHighReturn.numeric_high_returns_after_le_three
#print Agent105.NumericHigh.NumericHigh
#print HighCarryReduction.HighCarryWord
#print DecimalDigits.Canonical
#print DecimalDigits.columnSum
#print DecimalDigits.reflected
#print Lychrel196.orbit
#print Lychrel196.step
#print Lychrel196.reverse10
