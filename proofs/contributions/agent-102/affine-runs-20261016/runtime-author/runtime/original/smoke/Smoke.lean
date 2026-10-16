import Std

namespace Agent102Runtime

theorem add_zero_smoke (n : Nat) : n + 0 = n := rfl

theorem add_cancel_smoke (a b c : Nat) (h : a + b = a + c) : b = c :=
  Nat.add_left_cancel h

theorem reverse_smoke : ([1, 9, 6] : List Nat).reverse.reverse = [1, 9, 6] := rfl

#print axioms add_zero_smoke
#print axioms add_cancel_smoke
#print axioms reverse_smoke

end Agent102Runtime
