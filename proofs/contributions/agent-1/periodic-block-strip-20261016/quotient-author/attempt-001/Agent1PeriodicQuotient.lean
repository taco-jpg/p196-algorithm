import Agent1PeriodicGuardFacts

/-!
Exact whole-period absorption for the spatial quotient. The period word,
normalizer and actual pair map are the original definitions. This module
asserts neither safety preservation nor a return cycle.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Absorb complete exterior periods and mirrored center periods into the
two repeated bands. All exponents are natural numbers, including zero. -/
theorem periodicWord_absorb (B H w : Word) (u v k : Nat) :
    periodicWord (B ++ pow w u)
      (pow w v ++ H ++ pow w.reverse v) w k =
    periodicWord B H w (k + u + v) := by
  have hl : pow w u ++ pow w k ++ pow w v = pow w (k+u+v) := by
    rw [← pow_append, ← pow_append, Nat.add_comm u k]
  have hr : pow w.reverse v ++ pow w.reverse k ++ pow w.reverse u =
      pow w.reverse (k+u+v) := by
    rw [← pow_append, ← pow_append]
    congr 1
    omega
  simp only [periodicWord, List.reverse_append, pow_reverse]
  simp only [List.append_assoc] at hl hr ⊢
  rw [← hl, ← hr]
  simp only [List.append_assoc]

/-- Exact length, including zero exponents and noncanonical coefficient lists. -/
theorem periodicWord_length (B H w : Word) (k : Nat) :
    (periodicWord B H w k).length = 2*B.length + H.length + 2*(k*w.length) := by
  simp only [periodicWord, List.length_append, List.length_reverse, pow_length]
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_absorb
#print axioms Agent1.Periodic.periodicWord_length
