import OuterBounds

/-! A scope fixture: bounded phase-valid words need not satisfy validOuter.
The selected invalid-head word exits cap2 at time six; it is not a cycle or
a complete return certificate. -/
namespace Agent116.Review
open P196.Agent7.Finite

def zeroHead : Outer := ⟨2, [0]⟩

theorem zeroHead_invalid : validOuter zeroHead = false := by decide

theorem zeroHead_six_exit : (outerIterate 6 zeroHead).B = [6, 15, 1] := by decide

theorem zeroHead_five_confined : staysSmall 5 zeroHead = true := by decide

end Agent116.Review

#print axioms Agent116.Review.zeroHead_invalid
#print axioms Agent116.Review.zeroHead_six_exit
#print axioms Agent116.Review.zeroHead_five_confined
