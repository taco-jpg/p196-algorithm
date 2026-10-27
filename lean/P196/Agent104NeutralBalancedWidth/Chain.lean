import P196.Agent104NeutralBalancedWidth.Step
import P196.Agent119NeutralLengthAccounting.Main

/-!
# Balanced center widths along exact checked chains

Each occurrence of a center is padded by the same width-dependent function,
so seams and endpoints are preserved. Closed-chain acceptance and total gain
reuse Agent119's verified length accounting.
-/

namespace Agent104.NeutralBalancedWidth

open Agent120.Neutral

def SourceCap (W : Nat) (es : List Edge) : Prop :=
  ∀ E ∈ es, E.C.length ≤ W

def InterfaceCap (W : Nat) (es : List Edge) : Prop :=
  ∀ E ∈ es, E.C.length ≤ W ∧ E.C2.length ≤ W

def balanceEdges (b W : Nat) (es : List Edge) : List Edge :=
  es.map (balanceEdge b W)

private theorem chain_start_bound {b W : Nat} {es : List Edge}
    {B C : List Nat} (hc : chainOK b es B C = true)
    (hs : SourceCap W es) (hend : (endC es C).length ≤ W) : C.length ≤ W := by
  cases es with
  | nil => exact hend
  | cons E es =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, hC⟩, _⟩, _⟩ := hc
      simpa [hC] using hs E List.mem_cons_self

private theorem chain_target_bounds {b W : Nat} {es : List Edge}
    {B C : List Nat} (hc : chainOK b es B C = true)
    (hs : SourceCap W es) (hend : (endC es C).length ≤ W) :
    ∀ E ∈ es, E.C2.length ≤ W := by
  induction es generalizing B C with
  | nil => simp
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, _⟩, ht⟩ := hc
      have hs' : SourceCap W es := fun F hF => hs F (List.mem_cons_of_mem E hF)
      have hh : E.C2.length ≤ W := chain_start_bound ht hs' hend
      have hi := ih ht hs' hend
      intro F hF
      rcases List.mem_cons.mp hF with hF | hF
      · simpa [hF] using hh
      · exact hi F hF

/-- On a closed checked cycle, bounding source phases also bounds all targets. -/
theorem cycle_interface_cap {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : SourceCap W es) : InterfaceCap W es := by
  obtain ⟨hne, hch, _, hC⟩ :=
    (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  have hstart : C.length ≤ W := by
    cases es with
    | nil => exact False.elim (hne rfl)
    | cons E es =>
        simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hch
        obtain ⟨⟨⟨_, heC⟩, _⟩, _⟩ := hch
        simpa [heC] using hs E List.mem_cons_self
  have ht := chain_target_bounds hch hs (by simpa [hC] using hstart)
  exact fun E hE => ⟨hs E hE, ht E hE⟩

theorem balanceEdges_length (b W : Nat) (es : List Edge) :
    (balanceEdges b W es).length = es.length := by simp [balanceEdges]

theorem balanceEdges_fields (b W : Nat) (es : List Edge) :
    (balanceEdges b W es).map (fun E => (E.B, E.B2, E.u)) =
      es.map (fun E => (E.B, E.B2, E.u)) := by
  simp [balanceEdges, balanceEdge, List.map_map]

theorem balanceEdges_endB (b W : Nat) (es : List Edge) (B : List Nat) :
    endB (balanceEdges b W es) B = endB es B := by
  induction es generalizing B with
  | nil => rfl
  | cons E es ih => simpa only [balanceEdges, List.map_cons, endB, balanceEdge] using ih E.B2

theorem balanceEdges_endC (b W : Nat) (es : List Edge) (C : List Nat) :
    endC (balanceEdges b W es) (balanceCenter b W C) =
      balanceCenter b W (endC es C) := by
  induction es generalizing C with
  | nil => rfl
  | cons E es ih => simpa only [balanceEdges, List.map_cons, endC, balanceEdge] using ih E.C2

theorem balanceEdges_chainOK {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hb : InterfaceCap W es) :
    chainOK b (balanceEdges b W es) B (balanceCenter b W C) = true := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, ht⟩ := hc
      subst hB
      subst hC
      have hE := hb E List.mem_cons_self
      have he' := edgeOK_balance he hE.1 hE.2
      have hb' : InterfaceCap W es := fun F hF => hb F (List.mem_cons_of_mem E hF)
      have hi := ih ht hb'
      simpa only [balanceEdges, List.map_cons, chainOK, balanceEdge,
        decide_true, Bool.true_and, Bool.and_eq_true] using And.intro he' hi

theorem balanceEdges_streams {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    (balanceEdges b W es).map (fun E => (e1 b E.B, gam b E.B E.C)) =
      es.map (fun E => (e1 b E.B, gam b E.B E.C)) := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      have hg := balanceEdge_gam (W := W) he
      change gam b E.B (balanceCenter b W E.C) = gam b E.B E.C at hg
      have hi := ih ht
      simpa only [balanceEdges, List.map_cons, balanceEdge, hg] using
        congrArg (List.cons (e1 b E.B, gam b E.B E.C)) hi

theorem balanceEdges_sumGam {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    sumGam b (balanceEdges b W es) = sumGam b es := by
  induction es generalizing B C with
  | nil => rfl
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, ht⟩ := hc
      have hg := balanceEdge_gam (W := W) he
      have hi := ih ht
      simpa only [balanceEdges, List.map_cons, sumGam, hg] using
        congrArg (Nat.add (gam b E.B E.C)) hi

/-- A bounded certificate has an accepted representative at the balanced widths. -/
theorem cycleOK_balance {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : SourceCap W es) :
    cycleOK b (balanceEdges b W es) B (balanceCenter b W C) = true := by
  have hb := cycle_interface_cap hc hs
  obtain ⟨hne, hch, hB, hC⟩ :=
    (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  apply (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain _ _ _ _).mpr
  refine ⟨?_, balanceEdges_chainOK hch hb, ?_, ?_⟩
  · simpa [balanceEdges] using hne
  · simpa [hB] using balanceEdges_endB b W es B
  · simpa [hC] using balanceEdges_endC b W es C

theorem cycle_balance_gain {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : SourceCap W es) :
    sumGain (balanceEdges b W es) = sumGain es := by
  have hn := cycleOK_balance hc hs
  have ho := Agent119.NeutralLengthAccounting.cycleOK_totals hc
  have ht := Agent119.NeutralLengthAccounting.cycleOK_totals hn
  have hch := (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain b es B C).mp hc
  have hg := balanceEdges_sumGam (W := W) hch.2.1
  omega

end Agent104.NeutralBalancedWidth

#print axioms Agent104.NeutralBalancedWidth.cycle_interface_cap
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_length
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_fields
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_endB
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_endC
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_chainOK
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_streams
#print axioms Agent104.NeutralBalancedWidth.balanceEdges_sumGam
#print axioms Agent104.NeutralBalancedWidth.cycleOK_balance
#print axioms Agent104.NeutralBalancedWidth.cycle_balance_gain
