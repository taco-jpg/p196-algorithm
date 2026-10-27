import P196.Agent104NeutralJointWidth.Edges
import P196.Agent104NeutralJointWidth.FiniteCycle

/-!
# A complete finite Boolean decision under joint raw width caps

The explicit search is intentionally a simple finite specification. It is
not a performance claim and does not verify an external optimized solver.
Short-cycle extraction existentially changes the driver and initial state.
-/

namespace Agent104.NeutralJointWidth

open Agent120.Neutral

def JointRealizable (b M W : Nat) : Prop :=
  ∃ es B C, cycleOK b es B C = true ∧ JointCaps M W es

def ShortNormalized (b M W : Nat) : Prop :=
  ∃ es B C, cycleOK b es B C = true ∧ NormalizedEdges b M W es ∧
    0 < es.length ∧ es.length ≤ stateBound b M W

/-- Finite exhaustive specification, always using the original cycle checker. -/
def normalizedSearch (b M W : Nat) : Bool :=
  (List.range (stateBound b M W + 1)).any fun n =>
    (listsOf (edgeAlphabet b M W) n).any fun es =>
      (states b M W).any fun s => cycleOK b es s.1 s.2

theorem normalizedSearch_sound {b M W : Nat}
    (h : normalizedSearch b M W = true) : JointRealizable b M W := by
  obtain ⟨n, hn, hs⟩ := List.any_eq_true.mp h
  obtain ⟨es, hes, hss⟩ := List.any_eq_true.mp hs
  obtain ⟨s, hs, hc⟩ := List.any_eq_true.mp hss
  have hem := ((mem_listsOf _ _ _).mp hes).2
  have hnorm : NormalizedEdges b M W es :=
    fun E hE => edgeAlphabet_normalized (hem E hE)
  exact ⟨es, s.1, s.2, hc, normalizedEdges_caps hnorm⟩

/-- Every normalized checked witness below the explicit cutoff is enumerated. -/
theorem normalizedSearch_complete {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hn : NormalizedEdges b M W es)
    (hlen : es.length ≤ stateBound b M W) : normalizedSearch b M W = true := by
  have he := cycle_mem_edgeAlphabet hc hn
  have hs := cycle_start_mem hc (cycle_source_states hc hn)
  apply List.any_eq_true.mpr
  refine ⟨es.length, List.mem_range.mpr (by omega), ?_⟩
  apply List.any_eq_true.mpr
  refine ⟨es, (mem_listsOf _ _ _).mpr ⟨rfl, he⟩, ?_⟩
  exact List.any_eq_true.mpr ⟨(B, C), hs, hc⟩

/-- The cutoff is existential over drivers and initial states, not a fixed-driver
period-descent statement. Every chosen subcycle still passes unchanged cycleOK. -/
theorem joint_iff_short_normalized (b M W : Nat) (hW : 2 ≤ W) :
    JointRealizable b M W ↔ ShortNormalized b M W := by
  constructor
  · rintro ⟨es, B, C, hc, hcap⟩
    obtain ⟨ns, BN, CN, hnc, hnorm, hsame⟩ :=
      cycle_normalized_representative hc hcap hW
    have hstates := cycle_source_states hnc hnorm
    obtain ⟨ss, BS, CS, hsc, hsnorm, hss, hpos, hlen⟩ :=
      cycleOK_exists_bounded (NormalizedEdge b M W) (states b M W)
        hnc hnorm hstates
    exact ⟨ss, BS, CS, hsc, hsnorm, hpos, by simpa [states_length] using hlen⟩
  · rintro ⟨es, B, C, hc, hnorm, hpos, hlen⟩
    exact ⟨es, B, C, hc, normalizedEdges_caps hnorm⟩

/-- A fully explicit finite Boolean decision for every raw joint width bound. -/
theorem normalizedSearch_iff (b M W : Nat) (hW : 2 ≤ W) :
    normalizedSearch b M W = true ↔ JointRealizable b M W := by
  constructor
  · exact normalizedSearch_sound
  · intro h
    obtain ⟨es, B, C, hc, hn, hp, hl⟩ := (joint_iff_short_normalized b M W hW).mp h
    exact normalizedSearch_complete hc hn hl

theorem normalizedSearch_false_iff (b M W : Nat) (hW : 2 ≤ W) :
    normalizedSearch b M W = false ↔ ¬ JointRealizable b M W := by
  rw [← normalizedSearch_iff b M W hW]
  cases normalizedSearch b M W <;> simp

/-- The decision procedure is defined from the finite Boolean search; the
classical reasoning in the cutoff proof does not implement the search. -/
def jointDecidable (b M W : Nat) (hW : 2 ≤ W) : Decidable (JointRealizable b M W) :=
  if h : normalizedSearch b M W = true then
    isTrue ((normalizedSearch_iff b M W hW).mp h)
  else
    isFalse (fun hc => h ((normalizedSearch_iff b M W hW).mpr hc))

end Agent104.NeutralJointWidth

#print axioms Agent104.NeutralJointWidth.normalizedSearch_sound
#print axioms Agent104.NeutralJointWidth.normalizedSearch_complete
#print axioms Agent104.NeutralJointWidth.joint_iff_short_normalized
#print axioms Agent104.NeutralJointWidth.normalizedSearch_iff
#print axioms Agent104.NeutralJointWidth.normalizedSearch_false_iff
#print axioms Agent104.NeutralJointWidth.jointDecidable
