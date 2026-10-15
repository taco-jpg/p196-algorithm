import OuterBounds

/-! A scope fixture: dropping the positive-head condition admits a bounded
six-cycle in the exterior map. It is not a complete return certificate. -/
namespace Agent116.Review
open P196.Agent7.Finite

def zeroHead : Outer := ⟨2, [0]⟩

theorem zeroHead_invalid : validOuter zeroHead = false := by decide

theorem zeroHead_six_cycle : outerIterate 6 zeroHead = zeroHead := by decide

theorem zeroHead_seven_confined : staysSmall 7 zeroHead = true := by decide

end Agent116.Review

#print axioms Agent116.Review.zeroHead_invalid
#print axioms Agent116.Review.zeroHead_six_cycle
#print axioms Agent116.Review.zeroHead_seven_confined
