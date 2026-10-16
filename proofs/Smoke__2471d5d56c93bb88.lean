import Std
theorem runtimeSmoke : 196 + 691 = 887 := by decide
theorem runtimeOmega (a b : Nat) : a + b = b + a := by omega
#print axioms runtimeSmoke
#print axioms runtimeOmega
