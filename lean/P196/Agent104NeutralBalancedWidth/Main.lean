import P196.Agent104NeutralBalancedWidth.Chain

/-!
# Balanced representatives preserve bounded certificate existence

Within a fixed center-width ceiling W >= 2, every accepted certificate has a
representative whose centers have widths W-1 or W and whose binary trims are
forced by overflow and width. The initial exterior, full exterior edge data
and carry/overflow streams stay fixed. Centers and their trims are existential.
This is an existence equivalence, not a rejection test for an arbitrary source.
-/

namespace Agent104.NeutralBalancedWidth

open Agent120.Neutral

/-- Positive centers at the two adjacent widths, with their forced binary trims. -/
def BalancedPhases (b W : Nat) (es : List Edge) : Prop :=
  ∀ E ∈ es,
    0 < E.C.length ∧
    (E.C.length = W - 1 ∨ E.C.length = W) ∧
    E.v ≤ 1 ∧
    E.v = if gam b E.B E.C = 1 ∧ E.C.length = W then 1 else 0

private theorem chain_edgeOK {b : Nat} {es : List Edge} {B C : List Nat}
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

/-- Balancing a bounded accepted cycle satisfies every local profile rule. -/
theorem balanceEdges_balanced {b W : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) (hs : SourceCap W es) (hW : 2 ≤ W) :
    BalancedPhases b W (balanceEdges b W es) := by
  have hb := cycle_interface_cap hc hs
  have hch := (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain
    b es B C).mp hc
  intro F hF
  change F ∈ es.map (balanceEdge b W) at hF
  obtain ⟨E, hE, rfl⟩ := List.mem_map.mp hF
  have he := chain_edgeOK hch.2.1 E hE
  have hcap := hb E hE
  have hlen := balanceCenter_lengths b W E.C hcap.1
  have hpos : 0 < (balanceCenter b W E.C).length := by
    have hh := balanceCenter_length_bounds b W E.C hcap.1
    omega
  have hv := balanceTrim_le_one he hcap.1 hcap.2
  have hr := balanceTrim_exact he hcap.1 hcap.2
  have hg := balanceEdge_gam (W := W) he
  change gam b E.B (balanceCenter b W E.C) = gam b E.B E.C at hg
  refine ⟨hpos, hlen, hv, ?_⟩
  simpa only [balanceEdge, hg] using hr

/-- The balanced local profile already implies the original source-width cap. -/
theorem balanced_sourceCap {b W : Nat} {es : List Edge}
    (hb : BalancedPhases b W es) : SourceCap W es := by
  intro E hE
  have hw := (hb E hE).2.1
  omega

/-- An accepted certificate below a fixed center-width ceiling, retaining exact
exterior data and the lower-carry/overflow stream. Center trims are unrestricted. -/
def BoundedRealizable (b W : Nat) (B : List Nat)
    (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) : Prop :=
  ∃ (es : List Edge) (C : List Nat),
    cycleOK b es B C = true ∧
    es.map (fun E => (E.B, E.B2, E.u)) = exterior ∧
    es.map (fun E => (e1 b E.B, gam b E.B E.C)) = streams ∧
    SourceCap W es

/-- An accepted certificate with the same fixed data and the balanced local
profile. The center words and binary trim choices remain existential. -/
def BalancedRealizable (b W : Nat) (B : List Nat)
    (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) : Prop :=
  ∃ (es : List Edge) (C : List Nat),
    cycleOK b es B C = true ∧
    es.map (fun E => (E.B, E.B2, E.u)) = exterior ∧
    es.map (fun E => (e1 b E.B, gam b E.B E.C)) = streams ∧
    BalancedPhases b W es

/-- At fixed exterior data and streams, the two-width profile is a complete
existential normal form within the same width ceiling. -/
theorem bounded_iff_balanced (b W : Nat) (B : List Nat)
    (exterior : List (List Nat × List Nat × Nat))
    (streams : List (Nat × Nat)) (hW : 2 ≤ W) :
    BoundedRealizable b W B exterior streams ↔
      BalancedRealizable b W B exterior streams := by
  constructor
  · rintro ⟨es, C, hc, hext, hstreams, hs⟩
    have hch := (Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain
      b es B C).mp hc
    refine ⟨balanceEdges b W es, balanceCenter b W C,
      cycleOK_balance hc hs, ?_, ?_, balanceEdges_balanced hc hs hW⟩
    · exact (balanceEdges_fields b W es).trans hext
    · exact (balanceEdges_streams (W := W) hch.2.1).trans hstreams
  · rintro ⟨es, C, hc, hext, hstreams, hb⟩
    exact ⟨es, C, hc, hext, hstreams, balanced_sourceCap hb⟩

end Agent104.NeutralBalancedWidth

#print axioms Agent104.NeutralBalancedWidth.balanceEdges_balanced
#print axioms Agent104.NeutralBalancedWidth.balanced_sourceCap
#print axioms Agent104.NeutralBalancedWidth.bounded_iff_balanced
