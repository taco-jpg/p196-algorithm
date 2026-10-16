import Cap3Bounds
import OuterBridge
import Compat

/-!
The cap-three finite certificate interpreted on the repository's genuine
ordinary decimal reverse-and-add orbit.  Exit means growth of the specified
maximally trimmed exterior coordinate, not a palindrome hit or departure from
every possible template representation.
-/
namespace Agent116.ActualCap3

open Agent109 Agent109.Outer P196.Agent7.Finite
set_option maxHeartbeats 0

/-- With both bands initially at least 18, a valid even-phase exterior of
length at most three grows beyond three within nine actual additions. -/
theorem lychrel_cap3_exit (n : Nat) (p : Fin 8) (B A C : Word) (g h : Nat)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hlen : B.length ≤ 3)
    (hvalid : validOuter ⟨2 * (p.val + 1), B⟩ = true)
    (hg : 18 ≤ g) (hh : 18 ≤ h)
    (hn : pairWord n = Agent8.template (2 * (p.val + 1)) B A C g h) :
    ∃ i, i ≤ 9 ∧ ∃ c' B' A' C' G H, 3 < B'.length ∧
      B' = (outerIterate i ⟨2 * (p.val + 1), B⟩).B ∧
      pairWord (Lychrel196.orbit n i) = Agent8.template c' B' A' C' G H := by
  have hc : Phase (2 * (p.val + 1)) := by
    have := p.isLt
    unfold Phase
    omega
  obtain ⟨i, hi, hex⟩ :=
    P196.Agent116.Cap3.cap3_exit_witness p B hlen hB hvalid
  obtain ⟨A', C', G, H, _, _, _, _, _, _, hrep⟩ :=
    actual_outer_orbit n _ B A C g h hc hB hA hC hn i (by omega) (by omega)
  refine ⟨i, hi, (outerIterate i ⟨2 * (p.val + 1), B⟩).c,
    (outerIterate i ⟨2 * (p.val + 1), B⟩).B, A', C', G, H, hex, rfl, ?_⟩
  rw [Compat.orbit_eq, outerIterate_eq]
  exact hrep

end Agent116.ActualCap3

#print axioms Agent116.ActualCap3.lychrel_cap3_exit
