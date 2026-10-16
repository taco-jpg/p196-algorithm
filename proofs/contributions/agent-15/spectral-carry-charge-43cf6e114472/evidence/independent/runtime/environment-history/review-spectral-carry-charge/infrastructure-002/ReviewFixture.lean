import Std

namespace ReviewFixture
private def hidden : Nat := 7
def visible : Nat := hidden
theorem visible_eq : visible = 7 := rfl
structure Sample where
  val : Nat
theorem sample_refl (x : Sample) : x.val = x.val := rfl
end ReviewFixture
