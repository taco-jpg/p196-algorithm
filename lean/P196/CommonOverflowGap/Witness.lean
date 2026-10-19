import P196.CommonOverflowGap.Numeric
import P196.Agent8CommonOverflowDefect.Agent8DefectWitness

/-!
The existing canonical common-overflow witness instantiates the new gap
law.  Its digits, carries, antisymmetry, and numerical outputs are reused
without recertifying their finite calculations.
-/

namespace P196.CommonOverflowGap

open P196.Agent8.CommonOverflowDefect.Witness

/-- The first gap is 49,995; the second gap has the opposite sign and
magnitude 449,955.  The scale is derived from the universal theorem. -/
theorem witness_reversed_gap :
    Lychrel196.step 99010 < Lychrel196.step 99505 ∧
      Lychrel196.step (Lychrel196.step 99505) <
        Lychrel196.step (Lychrel196.step 99010) ∧
      Lychrel196.step (Lychrel196.step 99010) -
        Lychrel196.step (Lychrel196.step 99505) = 449955 := by
  have hfirst := actual_first_values
  have horder : Lychrel196.step 99010 < Lychrel196.step 99505 := by omega
  have hreverse := (numeric_overflow_order_reversal
    99505 99010 leftDigits rightDigits leftWord rightWord 5
    left_canonical right_canonical (fun _ _ => rfl) (fun _ _ => rfl)
    terminal_carries.1 terminal_carries.2 antisymmetric).mpr horder
  have hgap := numeric_overflow_natural_gap
    99505 99010 leftDigits rightDigits leftWord rightWord 5
    left_canonical right_canonical (fun _ _ => rfl) (fun _ _ => rfl)
    terminal_carries.1 terminal_carries.2 antisymmetric
  exact ⟨horder, hreverse, by omega⟩

end P196.CommonOverflowGap
