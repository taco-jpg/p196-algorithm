import OuterBridge
import Compat

/-! Agent #109: `actual_cap2_exit` restated with the accepted `Lychrel196.orbit`. -/

namespace Agent109.OuterCompat
open Agent109 Agent109.Outer

theorem lychrel_cap2_exit (n : Nat) (p : Fin 8) (B A C : Word) (g h : Nat)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hlen : B.length ≤ 2)
    (hvalid : P196.Agent7.Finite.validOuter ⟨2 * (p.val + 1), B⟩ = true)
    (hg : 14 ≤ g) (hh : 14 ≤ h)
    (hn : pairWord n = Agent8.template (2 * (p.val + 1)) B A C g h) :
    ∃ i, i ≤ 7 ∧ ∃ c' B' A' C' G H, 2 < B'.length ∧
      B' = (P196.Agent7.Finite.outerIterate i ⟨2 * (p.val + 1), B⟩).B ∧
      pairWord (Lychrel196.orbit n i) = Agent8.template c' B' A' C' G H := by
  obtain ⟨i, hi, c', B', A', C', G, H, h1, h2, h3⟩ :=
    actual_cap2_exit n p B A C g h hB hA hC hlen hvalid hg hh hn
  exact ⟨i, hi, c', B', A', C', G, H, h1, h2, by rw [Compat.orbit_eq]; exact h3⟩

end Agent109.OuterCompat

#print axioms Agent109.OuterCompat.lychrel_cap2_exit
