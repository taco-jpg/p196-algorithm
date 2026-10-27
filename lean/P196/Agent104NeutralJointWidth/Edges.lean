import P196.Agent104NeutralJointWidth.NormalForm
import P196.Agent104NeutralJointWidth.FiniteStates

/-!
# A finite alphabet of normalized checker edges

Each pair of finite interface states determines the only possible normalized
trim fields. Acceptance remains the original edgeOK test. Closed-chain seams
place every source and target of a normalized certificate inside this alphabet.
-/

namespace Agent104.NeutralJointWidth

open Agent120.Neutral

/-- The candidate edge between two states, with the forced normalized trims. -/
def edgeFrom (b W : Nat) (s t : State) : Edge where
  B := s.1
  C := s.2
  B2 := t.1
  C2 := t.2
  u := gam b s.1 s.2
  v := if gam b s.1 s.2 = 1 ∧ s.2.length = W then 1 else 0

/-- All candidate normalized edges; the original checker filters acceptance. -/
def edgeAlphabet (b M W : Nat) : List Edge :=
  (states b M W).flatMap fun s => (states b M W).map (edgeFrom b W s)

theorem mem_edgeAlphabet (b M W : Nat) (E : Edge) :
    E ∈ edgeAlphabet b M W ↔
      ∃ s ∈ states b M W, ∃ t ∈ states b M W, edgeFrom b W s t = E := by
  simp only [edgeAlphabet, List.mem_flatMap, List.mem_map]

theorem edgeAlphabet_normalized {b M W : Nat} {E : Edge}
    (hE : E ∈ edgeAlphabet b M W) : NormalizedEdge b M W E := by
  obtain ⟨s, hs, t, _, rfl⟩ := (mem_edgeAlphabet b M W E).mp hE
  have hh := (mem_states b M W s.1 s.2).mp hs
  exact ⟨hh.1, hh.2.1, rfl, rfl⟩

theorem edgeAlphabet_source {b M W : Nat} {E : Edge}
    (hE : E ∈ edgeAlphabet b M W) : (E.B, E.C) ∈ states b M W := by
  obtain ⟨s, hs, t, _, rfl⟩ := (mem_edgeAlphabet b M W E).mp hE
  exact hs

theorem edgeAlphabet_target {b M W : Nat} {E : Edge}
    (hE : E ∈ edgeAlphabet b M W) : (E.B2, E.C2) ∈ states b M W := by
  obtain ⟨s, _, t, ht, rfl⟩ := (mem_edgeAlphabet b M W E).mp hE
  exact ht

/-- Source, target, and normalized fields recover exactly the listed candidate. -/
theorem edge_mem_alphabet {b M W : Nat} {E : Edge}
    (hs : (E.B, E.C) ∈ states b M W)
    (ht : (E.B2, E.C2) ∈ states b M W) (hn : NormalizedEdge b M W E) :
    E ∈ edgeAlphabet b M W := by
  apply (mem_edgeAlphabet b M W E).mpr
  refine ⟨(E.B, E.C), hs, (E.B2, E.C2), ht, ?_⟩
  obtain ⟨_, _, hu, hv⟩ := hn
  cases E
  simp_all only [edgeFrom]

private theorem chain_source_states {b M W : Nat} {es : List Edge}
    {B C : List Nat} (hc : chainOK b es B C = true)
    (hn : NormalizedEdges b M W es) :
    ∀ E ∈ es, (E.B, E.C) ∈ states b M W := by
  induction es generalizing B C with
  | nil => simp
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      have hE := hn E List.mem_cons_self
      have hn' : NormalizedEdges b M W es :=
        fun F hF => hn F (List.mem_cons_of_mem E hF)
      intro F hF
      rcases List.mem_cons.mp hF with hF | hF
      · subst F
        exact hyp_mem_states (edgeOK_sound he).1 hE.1 hE.2.1
      · exact ih ht hn' F hF

/-- Actual Hyp bounds supply the finite coefficient alphabet at each source. -/
theorem cycle_source_states {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hn : NormalizedEdges b M W es) :
    ∀ E ∈ es, (E.B, E.C) ∈ states b M W := by
  have hch := (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain
    b es B C).mp hc
  exact chain_source_states hch.2.1 hn

/-- In a nonempty checked cycle, the declared start is one of its sources. -/
theorem cycle_start_mem {b : Nat} {es : List Edge} {B C : List Nat}
    {carrier : List State} (hc : cycleOK b es B C = true)
    (hs : ∀ E ∈ es, (E.B, E.C) ∈ carrier) : (B, C) ∈ carrier := by
  obtain ⟨hne, hch, _, _⟩ :=
    (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  cases es with
  | nil => exact False.elim (hne rfl)
  | cons E es =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hch
      obtain ⟨⟨⟨hB, hC⟩, _⟩, _⟩ := hch
      simpa [hB, hC] using hs E List.mem_cons_self

private theorem chain_interfaces_mem {b : Nat} {es : List Edge}
    {B C : List Nat} {carrier : List State} (hc : chainOK b es B C = true)
    (hs : ∀ E ∈ es, (E.B, E.C) ∈ carrier)
    (hend : (endB es B, endC es C) ∈ carrier) :
    (B, C) ∈ carrier ∧ ∀ E ∈ es, (E.B2, E.C2) ∈ carrier := by
  induction es generalizing B C with
  | nil => exact ⟨hend, by simp⟩
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, _⟩, ht⟩ := hc
      have hstart : (B, C) ∈ carrier := by
        simpa [hB, hC] using hs E List.mem_cons_self
      have hi := ih ht (fun F hF => hs F (List.mem_cons_of_mem E hF)) hend
      refine ⟨hstart, ?_⟩
      intro F hF
      rcases List.mem_cons.mp hF with hF | hF
      · simpa [hF] using hi.1
      · exact hi.2 F hF

/-- Every target is another source, using the actual final-to-initial seam. -/
theorem cycle_target_mem {b : Nat} {es : List Edge} {B C : List Nat}
    {carrier : List State} (hc : cycleOK b es B C = true)
    (hs : ∀ E ∈ es, (E.B, E.C) ∈ carrier) :
    ∀ E ∈ es, (E.B2, E.C2) ∈ carrier := by
  obtain ⟨_, hch, hB, hC⟩ :=
    (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  have hend : (endB es B, endC es C) ∈ carrier := by
    simpa [hB, hC] using cycle_start_mem hc hs
  exact (chain_interfaces_mem hch hs hend).2

/-- Every edge of an accepted normalized cycle belongs to the finite alphabet. -/
theorem cycle_mem_edgeAlphabet {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hn : NormalizedEdges b M W es) :
    ∀ E ∈ es, E ∈ edgeAlphabet b M W := by
  have hs := cycle_source_states hc hn
  have ht := cycle_target_mem hc hs
  exact fun E hE => edge_mem_alphabet (hs E hE) (ht E hE) (hn E hE)

/-- Normalized accepted edges with the same source have the same full output.
The finite alphabet may contain rejected alternatives, but acceptance is partial
and single-valued. -/
theorem normalized_edge_deterministic {b M W : Nat} {E F : Edge}
    (he : edgeOK b E = true) (hf : edgeOK b F = true)
    (hE : NormalizedEdge b M W E) (hF : NormalizedEdge b M W F)
    (hB : E.B = F.B) (hC : E.C = F.C) : E = F := by
  have hu : E.u = F.u := by rw [hE.2.2.1, hF.2.2.1, hB, hC]
  have hv : E.v = F.v := by rw [hE.2.2.2, hF.2.2.2, hB, hC]
  have heqB := (edgeOK_sound he).2.1
  have heqC := (edgeOK_sound he).2.2
  rw [hB, hC, hu] at heqB
  rw [hB, hC, hv] at heqC
  have hB2 := List.append_cancel_right (heqB.symm.trans (edgeOK_sound hf).2.1)
  have hC2 := List.append_cancel_right
    (List.append_cancel_left (heqC.symm.trans (edgeOK_sound hf).2.2))
  cases E
  cases F
  simp_all

end Agent104.NeutralJointWidth

#print axioms Agent104.NeutralJointWidth.mem_edgeAlphabet
#print axioms Agent104.NeutralJointWidth.edgeAlphabet_normalized
#print axioms Agent104.NeutralJointWidth.edgeAlphabet_source
#print axioms Agent104.NeutralJointWidth.edgeAlphabet_target
#print axioms Agent104.NeutralJointWidth.edge_mem_alphabet
#print axioms Agent104.NeutralJointWidth.cycle_source_states
#print axioms Agent104.NeutralJointWidth.cycle_start_mem
#print axioms Agent104.NeutralJointWidth.cycle_target_mem
#print axioms Agent104.NeutralJointWidth.cycle_mem_edgeAlphabet
#print axioms Agent104.NeutralJointWidth.normalized_edge_deterministic
