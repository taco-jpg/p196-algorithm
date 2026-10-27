import P196.Agent114NeutralUniformExterior.UniformChain
import P196.Agent104NeutralBalancedWidth.Main

/-!
# Joint bounded-width representatives for the unchanged neutral checker

Compose the verified uniform exterior construction with the verified balanced
center construction. Source bounds suffice on a closed chain, including for
an empty exterior. The resulting cycle keeps its listed length and total gain.
No finite search, period cutoff, or decimal certificate is asserted here.
-/

namespace Agent104.NeutralJointWidth

open Agent120.Neutral Agent114.NeutralUniformExterior Agent104.NeutralBalancedWidth

/-- Both source interfaces obey their declared width ceilings. -/
def JointCaps (M W : Nat) (es : List Edge) : Prop :=
  ∀ E ∈ es, E.B.length ≤ M ∧ E.C.length ≤ W

/-- The two fixed-width representations determine both trim fields. -/
def NormalizedEdge (b M W : Nat) (E : Edge) : Prop :=
  E.B.length = M ∧
  (E.C.length = W - 1 ∨ E.C.length = W) ∧
  E.u = gam b E.B E.C ∧
  E.v = if gam b E.B E.C = 1 ∧ E.C.length = W then 1 else 0

def NormalizedEdges (b M W : Nat) (es : List Edge) : Prop :=
  ∀ E ∈ es, NormalizedEdge b M W E

/-- First pad every exterior to M, then balance the centers below W. -/
def jointEdges (b M W : Nat) (es : List Edge) : List Edge :=
  balanceEdges b W (uniformEdges b M es)

private theorem chain_exterior_property {b : Nat} {es : List Edge}
    {B C : List Nat} (P : List Nat → Prop)
    (hc : chainOK b es B C = true) (hs : ∀ E ∈ es, P E.B)
    (hend : P (endB es B)) : P B ∧ ∀ E ∈ es, P E.B2 := by
  induction es generalizing B C with
  | nil => exact ⟨hend, by simp⟩
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, _⟩, _⟩, ht⟩ := hc
      have hh : P B := by simpa [hB] using hs E List.mem_cons_self
      have hi := ih ht (fun F hF => hs F (List.mem_cons_of_mem E hF)) hend
      refine ⟨hh, ?_⟩
      intro F hF
      rcases List.mem_cons.mp hF with hF | hF
      · simpa [hF] using hi.1
      · exact hi.2 F hF

/-- Closure turns the source-only exterior cap into all required interfaces. -/
theorem jointCaps_widthBound {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : JointCaps M W es) :
    WidthBound M es B := by
  obtain ⟨hne, hch, hB, _⟩ :=
    (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  have hstart : B.length ≤ M := by
    cases es with
    | nil => exact False.elim (hne rfl)
    | cons E es =>
        simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hch
        obtain ⟨⟨⟨heB, _⟩, _⟩, _⟩ := hch
        simpa [heB] using (hs E List.mem_cons_self).1
  have ht := (chain_exterior_property (fun L => L.length ≤ M) hch
    (fun E hE => (hs E hE).1) (by simpa [hB] using hstart)).2
  exact ⟨hstart, fun E hE => ⟨(hs E hE).1, ht E hE⟩⟩

private theorem uniform_sourceCap (b M W : Nat) (es : List Edge)
    (hs : JointCaps M W es) : SourceCap W (uniformEdges b M es) := by
  intro F hF
  obtain ⟨E, hE, rfl⟩ := List.mem_map.mp hF
  exact (hs E hE).2

private theorem chain_checked_edges {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) : ∀ E ∈ es, edgeOK b E = true := by
  induction es generalizing B C with
  | nil => simp
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      intro F hF
      rcases List.mem_cons.mp hF with hF | hF
      · simpa [hF] using he
      · exact ih ht F hF

theorem jointEdges_length (b M W : Nat) (es : List Edge) :
    (jointEdges b M W es).length = es.length := by
  rw [jointEdges, balanceEdges_length, uniformEdges_length]

/-- Both successive representation changes preserve original checker acceptance. -/
theorem jointEdges_cycleOK {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : JointCaps M W es) :
    cycleOK b (jointEdges b M W es) (padWidth b M B)
      (balanceCenter b W C) = true := by
  exact cycleOK_balance (uniform_cycleOK hc (jointCaps_widthBound hc hs))
    (uniform_sourceCap b M W es hs)

/-- The composed representative has uniform exteriors and the forced two-width
center profile, with both trims computed from its actual source. -/
theorem jointEdges_normalized {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : JointCaps M W es) (hW : 2 ≤ W) :
    NormalizedEdges b M W (jointEdges b M W es) := by
  have hb := jointCaps_widthBound hc hs
  have hu := uniform_cycleOK hc hb
  have hw := uniform_widths b M es B hb
  have hp := balanceEdges_balanced hu (uniform_sourceCap b M W es hs) hW
  have hj := jointEdges_cycleOK hc hs
  have hch := (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain
    b (jointEdges b M W es) (padWidth b M B) (balanceCenter b W C)).mp hj
  intro F hF
  have he := chain_checked_edges hch.2.1 F hF
  have hprofile := hp F hF
  change F ∈ (uniformEdges b M es).map (balanceEdge b W) at hF
  obtain ⟨E, hE, rfl⟩ := List.mem_map.mp hF
  have hwidth := hw.2 E hE
  refine ⟨hwidth.1, hprofile.2.1, ?_, hprofile.2.2.2⟩
  exact equal_width_trim he (hwidth.1.trans hwidth.2.symm)

theorem jointEdges_gain {b M W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : JointCaps M W es) :
    sumGain (jointEdges b M W es) = sumGain es := by
  have hb := jointCaps_widthBound hc hs
  exact (cycle_balance_gain (uniform_cycleOK hc hb)
    (uniform_sourceCap b M W es hs)).trans (uniform_cycle_gain hc hb)

/-- A constructive normalized certificate of the same listed length. -/
theorem cycle_normalized_representative {b M W : Nat} {es : List Edge}
    {B C : List Nat} (hc : cycleOK b es B C = true) (hs : JointCaps M W es)
    (hW : 2 ≤ W) :
    ∃ es' B' C', cycleOK b es' B' C' = true ∧
      NormalizedEdges b M W es' ∧ es'.length = es.length := by
  exact ⟨jointEdges b M W es, padWidth b M B, balanceCenter b W C,
    jointEdges_cycleOK hc hs, jointEdges_normalized hc hs hW,
    jointEdges_length b M W es⟩

theorem normalizedEdges_caps {b M W : Nat} {es : List Edge}
    (hn : NormalizedEdges b M W es) : JointCaps M W es := by
  intro E hE
  obtain ⟨hB, hC, _, _⟩ := hn E hE
  constructor <;> omega

/-- Joint width-bounded existence is exactly normalized-cycle existence. -/
theorem bounded_cycle_exists_iff_normalized (b M W : Nat) (hW : 2 ≤ W) :
    (∃ es B C, cycleOK b es B C = true ∧ JointCaps M W es) ↔
      ∃ es B C, cycleOK b es B C = true ∧ NormalizedEdges b M W es := by
  constructor
  · rintro ⟨es, B, C, hc, hs⟩
    obtain ⟨es', B', C', hc', hn, _⟩ := cycle_normalized_representative hc hs hW
    exact ⟨es', B', C', hc', hn⟩
  · rintro ⟨es, B, C, hc, hn⟩
    exact ⟨es, B, C, hc, normalizedEdges_caps hn⟩

end Agent104.NeutralJointWidth

#print axioms Agent104.NeutralJointWidth.jointCaps_widthBound
#print axioms Agent104.NeutralJointWidth.jointEdges_length
#print axioms Agent104.NeutralJointWidth.jointEdges_cycleOK
#print axioms Agent104.NeutralJointWidth.jointEdges_normalized
#print axioms Agent104.NeutralJointWidth.jointEdges_gain
#print axioms Agent104.NeutralJointWidth.cycle_normalized_representative
#print axioms Agent104.NeutralJointWidth.normalizedEdges_caps
#print axioms Agent104.NeutralJointWidth.bounded_cycle_exists_iff_normalized
