import P196.Drafts.Agent114Cap4KernelActualExit.CapCore
import P196.Agent6CertificateCoordinateAudit.OuterBridge

namespace Agent114.Exterior
open P196.Agent7.Finite
open Agent109
open Agent109.Outer

set_option maxHeartbeats 0

/-- A finite exterior certificate transfers to the actual ordinary integer orbit.
The certificate premise is explicit. No infinite-time assertion is made. -/
theorem actual_exit_of_check (cap bound n c : Nat) (B A C : Word) (g h : Nat)
    (hc : Phase c) (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hg : 2 * bound ≤ g) (hh : 2 * bound ≤ h)
    (hn : pairWord n = template c B A C g h)
    (hcheck : escapes cap bound ⟨c, B⟩ = true) :
    ∃ i, i ≤ bound ∧ ∃ A' C' G H,
      cap < (outerIterate i ⟨c, B⟩).B.length ∧
      Phase (outerIterate i ⟨c, B⟩).c ∧
      Bounded (outerIterate i ⟨c, B⟩).B ∧ Bounded A' ∧ Bounded C' ∧
      g ≤ G + 2 * i ∧ h ≤ H + 2 * i ∧
      pairWord (orbit n i) =
        template (outerIterate i ⟨c, B⟩).c (outerIterate i ⟨c, B⟩).B A' C' G H := by
  obtain ⟨i, hi, he⟩ := escapes_sound cap bound ⟨c, B⟩ hcheck
  obtain ⟨A', C', G, H, hphase, hbound, hA', hC', hG, hH, hrep⟩ :=
    actual_outer_orbit n c B A C g h hc hB hA hC hn i
      (by omega) (by omega)
  refine ⟨i, hi, A', C', G, H, he, ?_⟩
  simpa only [outerIterate_eq] using
    And.intro hphase (And.intro hbound (And.intro hA'
      (And.intro hC' (And.intro hG (And.intro hH hrep)))))

#print axioms actual_exit_of_check
end Agent114.Exterior
