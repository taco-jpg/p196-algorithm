import P196.Agent114NeutralUniformExterior.UniformEdge
import P196.Agent114NeutralExteriorCycle.CycleTransport

/-!
# Uniform exterior widths for complete checked chains

Every exterior interface bounded by `M` is padded to exactly `M`.  The
replacement exterior trim is the actual overflow bit.  Existing exact
padding transport preserves chain and cycle acceptance, streams and gain.
The center interfaces and their trims remain unchanged.
-/

namespace Agent114.NeutralUniformExterior

open Agent120.Neutral Agent114.NeutralExteriorPadding Agent114.NeutralExteriorCycle

/-- Pad every edge to the same exterior width without changing its position. -/
def uniformEdges (b M : Nat) (es : List Edge) : List Edge :=
  es.map (uniformEdge b M)

/-- All exterior interfaces, including the given starting word, fit the cap. -/
def WidthBound (M : Nat) (es : List Edge) (B : List Nat) : Prop :=
  B.length ≤ M ∧ ∀ e ∈ es, e.B.length ≤ M ∧ e.B2.length ≤ M

/-- All exterior interfaces, including the given starting word, have one width. -/
def UniformWidth (M : Nat) (es : List Edge) (B : List Nat) : Prop :=
  B.length = M ∧ ∀ e ∈ es, e.B.length = M ∧ e.B2.length = M

theorem uniformEdges_length (b M : Nat) (es : List Edge) :
    (uniformEdges b M es).length = es.length := by
  simp [uniformEdges]

theorem uniformEdges_centers (b M : Nat) (es : List Edge) :
    (uniformEdges b M es).map (fun e => (e.C, e.C2, e.v)) =
      es.map (fun e => (e.C, e.C2, e.v)) := by
  induction es with
  | nil => rfl
  | cons e es ih =>
      simpa only [uniformEdges, List.map_cons, uniformEdge, padEdge] using
        congrArg (List.cons (e.C, e.C2, e.v)) ih

/-- The width deficits are a compatible exterior-padding plan. -/
theorem uniform_chain_plan (b M : Nat) (es : List Edge) (B C : List Nat)
    (hc : chainOK b es B C = true) (hb : WidthBound M es B) :
    PadChain b (M - B.length) (M - (endB es B).length) es (uniformEdges b M es) := by
  induction es generalizing B C with
  | nil => exact PadChain.nil (M - B.length)
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hr⟩ := hc
      have hE := hb.2 E (by simp)
      have ht : WidthBound M es E.B2 := by
        refine ⟨hE.2, ?_⟩
        intro e he'
        exact hb.2 e (by simp [he'])
      subst B
      subst C
      exact PadChain.cons (gam b E.B E.C) (uniformEdge_balance he hE.1 hE.2)
        (ih E.B2 E.C2 hr ht)

/-- Every accepted bounded chain has an accepted uniform-width representative. -/
theorem uniform_chainOK {b M : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hb : WidthBound M es B) :
    chainOK b (uniformEdges b M es) (padWidth b M B) C = true := by
  exact ((uniform_chain_plan b M es B C hc hb).chainOK_iff B C).2 hc

/-- Width padding preserves both interface carries and every overflow bit. -/
theorem uniform_chain_streams {b M : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hb : WidthBound M es B) :
    (uniformEdges b M es).map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) =
      es.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) := by
  exact (uniform_chain_plan b M es B C hc hb).streams_eq B C hc

/-- The original complete cycle checker accepts the padded representative. -/
theorem uniform_cycleOK {b M : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) (hb : WidthBound M es B) :
    cycleOK b (uniformEdges b M es) (padWidth b M B) C = true := by
  have hs := hcert
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hs
  obtain ⟨⟨⟨⟨_, hc⟩, hB⟩, _⟩, _⟩ := hs
  have hp := uniform_chain_plan b M es B C hc hb
  rw [hB] at hp
  exact (hp.cycleOK_iff B C).2 hcert

theorem uniform_cycle_gain {b M : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) (hb : WidthBound M es B) :
    sumGain (uniformEdges b M es) = sumGain es := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨_, hc⟩, hB⟩, _⟩, _⟩ := hcert
  have hp := uniform_chain_plan b M es B C hc hb
  rw [hB] at hp
  exact hp.sumGain_eq

/-- Width padding reaches exactly the requested common cap at every interface. -/
theorem uniform_widths (b M : Nat) (es : List Edge) (B : List Nat)
    (hb : WidthBound M es B) :
    UniformWidth M (uniformEdges b M es) (padWidth b M B) := by
  refine ⟨?_, ?_⟩
  · exact padWidth_length b M B hb.1
  · intro e he
    obtain ⟨E, hE, rfl⟩ := List.mem_map.mp he
    exact uniformEdge_widths b M E (hb.2 E hE).1 (hb.2 E hE).2

/-- Each replacement trim equals the overflow computed at its padded source.
No width bound is needed for this field/carry identity itself. -/
theorem uniformEdges_trims {b M : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    ∀ e ∈ uniformEdges b M es, e.u = gam b e.B e.C := by
  induction es generalizing B C with
  | nil => simp [uniformEdges]
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, hr⟩ := hc
      intro e he'
      simp only [uniformEdges, List.map_cons, List.mem_cons] at he'
      rcases he' with rfl | he'
      · exact uniformEdge_trim_eq_gam he
      · exact ih (B := E.B2) (C := E.C2) hr e he'

end Agent114.NeutralUniformExterior

#print axioms Agent114.NeutralUniformExterior.uniform_chain_plan
#print axioms Agent114.NeutralUniformExterior.uniform_cycleOK
#print axioms Agent114.NeutralUniformExterior.uniform_cycle_gain
#print axioms Agent114.NeutralUniformExterior.uniform_chain_streams
#print axioms Agent114.NeutralUniformExterior.uniform_widths
#print axioms Agent114.NeutralUniformExterior.uniformEdges_trims
