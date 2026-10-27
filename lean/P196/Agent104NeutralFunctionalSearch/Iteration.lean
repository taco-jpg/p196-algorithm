import P196.Agent104NeutralFunctionalSearch.Successor

/-!
# Positive return detection along the exact normalized successor

The Boolean iteration accepts only after at least one successful edge. Every
successful return constructs a nonempty chain accepted by the original checker.
Conversely, an accepted normalized cycle is detected within its listed length;
an earlier return may stop the iteration before that entire list is traversed.
-/

namespace Agent104.NeutralFunctionalSearch

open Agent120.Neutral Agent104.NeutralJointWidth
open Agent119.NeutralLengthAccounting

/-- Test for a positive-length return to `start`, using at most `fuel` edges. -/
def returns (b M W : Nat) (start current : State) : Nat → Bool
  | 0 => false
  | fuel + 1 =>
      match successor b M W current with
      | none => false
      | some next => if next = start then true else returns b M W start next fuel

private theorem successful_edge {b M W : Nat} {s t : State}
    (h : successor b M W s = some t) :
    edgeOK b (edgeFrom b W s t) = true ∧
      NormalizedEdge b M W (edgeFrom b W s t) := by
  exact ⟨successor_edgeOK h, successor_normalized h⟩

/-- Successful iteration reconstructs the actual nonempty checked chain. -/
theorem returns_chain_sound {b M W fuel : Nat} {start current : State}
    (h : returns b M W start current fuel = true) :
    ∃ es, es ≠ [] ∧ es.length ≤ fuel ∧
      chainOK b es current.1 current.2 = true ∧
      endB es current.1 = start.1 ∧ endC es current.2 = start.2 ∧
      NormalizedEdges b M W es := by
  induction fuel generalizing current with
  | zero => simp [returns] at h
  | succ fuel ih =>
      cases hstep : successor b M W current with
      | none => simp [returns, hstep] at h
      | some next =>
          obtain ⟨he, hn⟩ := successful_edge hstep
          by_cases hclose : next = start
          · refine ⟨[edgeFrom b W current next], by simp, by simp, ?_, ?_, ?_, ?_⟩
            · simpa only [chainOK, edgeFrom, decide_true, Bool.true_and,
                Bool.and_true] using he
            · simpa only [endB, edgeFrom] using congrArg Prod.fst hclose
            · simpa only [endC, edgeFrom] using congrArg Prod.snd hclose
            · intro E hE
              have heq := List.mem_singleton.mp hE
              simpa [heq] using hn
          · have ht : returns b M W start next fuel = true := by
              simpa only [returns, hstep, if_neg hclose] using h
            obtain ⟨es, hne, hlen, hc, hB, hC, hnorm⟩ := ih ht
            refine ⟨edgeFrom b W current next :: es, by simp, ?_, ?_, ?_, ?_, ?_⟩
            · simp only [List.length_cons]
              omega
            · simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq]
              exact ⟨⟨⟨rfl, rfl⟩, he⟩, hc⟩
            · exact hB
            · exact hC
            · intro E hE
              rcases List.mem_cons.mp hE with hE | hE
              · simpa [hE] using hn
              · exact hnorm E hE

/-- A detected return gives an accepted normalized cycle under the same fuel. -/
theorem returns_cycle_sound {b M W fuel : Nat} {s : State}
    (h : returns b M W s s fuel = true) :
    ∃ es, cycleOK b es s.1 s.2 = true ∧ NormalizedEdges b M W es ∧
      0 < es.length ∧ es.length ≤ fuel := by
  obtain ⟨es, hne, hlen, hc, hB, hC, hn⟩ := returns_chain_sound h
  exact ⟨es, (cycleOK_iff_closed_chain b es s.1 s.2).mpr ⟨hne, hc, hB, hC⟩,
    hn, List.length_pos_iff.mpr hne, hlen⟩

private theorem successor_of_alphabet_edge {b M W : Nat} {E : Edge}
    (hm : E ∈ edgeAlphabet b M W) (he : edgeOK b E = true) :
    successor b M W (E.B, E.C) = some (E.B2, E.C2) := by
  obtain ⟨s, hs, t, ht, rfl⟩ := (mem_edgeAlphabet b M W E).mp hm
  exact (successor_eq_some_iff b M W s t).mpr ⟨hs, ht, he⟩

private theorem returns_chain_complete {b M W : Nat} (es : List Edge)
    (start current : State) (fuel : Nat) (hne : es ≠ [])
    (hc : chainOK b es current.1 current.2 = true)
    (hB : endB es current.1 = start.1) (hC : endC es current.2 = start.2)
    (hm : ∀ E ∈ es, E ∈ edgeAlphabet b M W) (hlen : es.length ≤ fuel) :
    returns b M W start current fuel = true := by
  induction es generalizing current fuel with
  | nil => exact False.elim (hne rfl)
  | cons E es ih =>
      cases fuel with
      | zero => simp at hlen
      | succ fuel =>
          simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨⟨⟨hsB, hsC⟩, he⟩, ht⟩ := hc
          have hcurrent : current = (E.B, E.C) := Prod.ext hsB.symm hsC.symm
          have hstep := successor_of_alphabet_edge (hm E List.mem_cons_self) he
          by_cases hclose : (E.B2, E.C2) = start
          · simp only [returns, hcurrent, hstep, if_pos hclose]
          · have htail : es ≠ [] := by
              intro hn
              subst es
              simp only [endB, endC] at hB hC
              exact hclose (Prod.ext hB hC)
            have hh := ih (E.B2, E.C2) fuel htail ht hB hC
              (fun F hF => hm F (List.mem_cons_of_mem E hF)) (by
                simp only [List.length_cons] at hlen
                omega)
            simpa only [returns, hcurrent, hstep, if_neg hclose] using hh

/-- Every accepted normalized cycle is detected within its listed length. -/
theorem returns_cycle_complete {b M W fuel : Nat} {es : List Edge}
    {B C : List Nat} (hc : cycleOK b es B C = true)
    (hn : NormalizedEdges b M W es) (hlen : es.length ≤ fuel) :
    returns b M W (B, C) (B, C) fuel = true := by
  obtain ⟨hne, hch, hB, hC⟩ := (cycleOK_iff_closed_chain b es B C).mp hc
  exact returns_chain_complete es (B, C) (B, C) fuel hne hch hB hC
    (cycle_mem_edgeAlphabet hc hn) hlen

end Agent104.NeutralFunctionalSearch

#print axioms Agent104.NeutralFunctionalSearch.returns_chain_sound
#print axioms Agent104.NeutralFunctionalSearch.returns_cycle_sound
#print axioms Agent104.NeutralFunctionalSearch.returns_cycle_complete
