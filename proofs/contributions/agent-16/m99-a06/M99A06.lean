import ExteriorArithmetic

namespace P196.Agent16.M99A06

open P196.Agent6

/-- Exact one-step interface hypothesis for an ordinary decimal state and the
exterior quotient. The paired-word shape is explicit; no global semiconjugacy
is assumed. -/
def ActualExteriorStep (D : Word) (s t : Exterior) : Prop :=
  ∃ B W c g,
    s = ⟨c, B⟩ ∧ t = advance s ∧
    DecimalDigits D ∧ PositiveLast D ∧
    Nonneutral c ∧ Coefficients B ∧ Coefficients W ∧
    paired D = surrounded B c g W

/-- The actual decimal reverse-add output projects to the next exterior state
under exactly the hypotheses used by the existing one-step bridge. -/
theorem actual_exterior_step_projection (D : Word) (s t : Exterior)
    (h : ActualExteriorStep D s t) :
    ∃ B W c g,
      s = ⟨c, B⟩ ∧
      t.word = trim (2 * digitPhase c)
        ((paired (reverseAddDigits D)).take (B.length + 1)) := by
  rcases h with ⟨B,W,c,g,hs,ht,hD,hp,hc,hB,hW,hshape⟩
  refine ⟨B,W,c,g,hs,?_,?_,?_,?_,?_,?_,?_⟩
  · rw [ht, hs]
    exact (ordinary_reverse_add_exterior D B W c g hD hp hc hB hW hshape).2.2.2.symm
  · exact hD
  · exact hp
  · exact hc
  · exact hB
  · exact hW
  · exact hshape

/-- A finite actual decimal walk lifts to the exterior map when every step
supplies its exact interface shape. This is deliberately conditional: it does
not assert that arbitrary decimal orbits admit the interface. -/
theorem actual_exterior_walk
    (D : Nat → Word) (s : Nat → Exterior) (N : Nat)
    (hstep : ∀ i, i < N → s (i+1) = advance (s i)) :
    s N = iterate N (s 0) := by
  induction N with
  | zero => rfl
  | succ N ih =>
      rw [ih (fun i hi => hstep i (by omega))]
      simpa [iterate] using hstep N (by omega)

/-- Exterior residue/mod-22 closure is not by itself a full-interface result:
the missing bridge is the explicit per-step interface premise represented by
ActualExteriorStep. -/
theorem exterior_closure_requires_interface :
    ∀ (D : Nat → Word) (s : Nat → Exterior) (N : Nat),
      (∀ i, i < N → ActualExteriorStep (D i) (s i) (s (i+1))) →
      s N = iterate N (s 0) := by
  intro D s N h
  apply actual_exterior_walk D s N
  intro i hi
  rcases h i hi with ⟨B,W,c,g,hs,ht,hD,hp,hc,hB,hW,hshape⟩
  exact ht

#print axioms actual_exterior_step_projection
#print axioms actual_exterior_walk
#print axioms exterior_closure_requires_interface

end P196.M99A06
