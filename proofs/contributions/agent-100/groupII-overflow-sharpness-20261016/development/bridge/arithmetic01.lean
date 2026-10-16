import Agent100GroupIIOverflowProfiles
example (v:Nat) (h: 5 ≤ v ∧ v ≤ 6) : (2*(2*v)+2)%10 = (2*v+1)%10 + (2*v+1)%10 := by omega
example (v:Nat) (h: 5 ≤ v ∧ v ≤ 6) : (2*(2*v)+2)%10 = (2*v+1)%10 + (2*v+1)%10 := by simp only [Nat.mul_assoc]; omega
