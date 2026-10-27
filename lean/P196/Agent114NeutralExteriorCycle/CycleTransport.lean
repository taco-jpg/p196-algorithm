import P196.Agent114NeutralExteriorPadding.EdgeTransport

/-!
# Agent 114: phase-dependent exterior padding of complete certificates

`PadChain` records the natural-number balance at each edge and requires the
target padding of one edge to be the source padding of the next.  The unchanged
chain checker is preserved in both directions.  Equal initial/final padding
also preserves the unchanged cycle checker, including its total gain test.
No existence of a decimal certificate is asserted.
-/

namespace Agent114.NeutralExteriorCycle

open Agent120.Neutral Agent114.NeutralExteriorPadding

/-- A consistent sequence of exterior padding offsets and replacement trims. -/
inductive PadChain (b : Nat) : Nat → Nat → List Edge → List Edge → Prop
  | nil (a : Nat) : PadChain b a a [] []
  | cons {a a' z : Nat} {e : Edge} {es fs : List Edge}
      (w : Nat) (hcount : a + e.u = w + a')
      (rest : PadChain b a' z es fs) :
      PadChain b a z (e :: es) (padEdge b a a' w e :: fs)

theorem suffixPad_eq_iff (b a : Nat) (X Y : List Nat) :
    suffixPad b a X = suffixPad b a Y ↔ X = Y := by
  unfold suffixPad
  exact List.append_left_inj _

namespace PadChain

variable {b a z : Nat} {es fs : List Edge}

theorem length_eq (hp : PadChain b a z es fs) : fs.length = es.length := by
  induction hp with
  | nil => rfl
  | cons w hcount rest ih => simpa only [List.length_cons] using congrArg Nat.succ ih

theorem nil_iff (hp : PadChain b a z es fs) : fs = [] ↔ es = [] := by
  rw [← List.length_eq_zero_iff, ← List.length_eq_zero_iff, hp.length_eq]

theorem not_nil_iff (hp : PadChain b a z es fs) : fs ≠ [] ↔ es ≠ [] :=
  not_congr hp.nil_iff

/-- The final exterior has the final recorded padding, even for empty chains. -/
theorem endB_eq (hp : PadChain b a z es fs) (B : List Nat) :
    endB fs (suffixPad b a B) = suffixPad b z (endB es B) := by
  induction hp generalizing B with
  | nil => rfl
  | @cons a a' z e es fs w hcount rest ih =>
      exact ih e.B2

theorem endC_eq (hp : PadChain b a z es fs) (C : List Nat) :
    endC fs C = endC es C := by
  induction hp generalizing C with
  | nil => rfl
  | @cons a a' z e es fs w hcount rest ih =>
      exact ih e.C2

/-- Exact checker equivalence, without assuming either chain is accepted. -/
theorem chainOK_iff (hp : PadChain b a z es fs) (B C : List Nat) :
    chainOK b fs (suffixPad b a B) C = true ↔ chainOK b es B C = true := by
  induction hp generalizing B C with
  | nil => rfl
  | @cons a a' z e es fs w hcount rest ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq]
      change
        (((suffixPad b a e.B = suffixPad b a B ∧ e.C = C) ∧
          edgeOK b (padEdge b a a' w e) = true) ∧
          chainOK b fs (suffixPad b a' e.B2) e.C2 = true) ↔
        (((e.B = B ∧ e.C = C) ∧ edgeOK b e = true) ∧
          chainOK b es e.B2 e.C2 = true)
      rw [suffixPad_eq_iff, edgeOK_suffixPad_iff a a' w hcount, ih]

/-- Natural-number telescoping retains the boundary offsets explicitly. -/
theorem gain_balance (hp : PadChain b a z es fs) :
    a + sumGain es = sumGain fs + z := by
  induction hp with
  | nil => simp [sumGain]
  | @cons a a' z e es fs w hcount rest ih =>
      change a + (e.u + e.v + sumGain es) = w + e.v + sumGain fs + z
      omega

theorem sumGain_eq {a : Nat} (hp : PadChain b a a es fs) :
    sumGain fs = sumGain es := by
  have h := hp.gain_balance
  omega

/-- Overflow totals agree on accepted chains; every edge uses the actual carry. -/
theorem sumGam_eq (hp : PadChain b a z es fs) (B C : List Nat)
    (hc : chainOK b es B C = true) :
    sumGam b fs = sumGam b es := by
  induction hp generalizing B C with
  | nil => rfl
  | @cons a a' z e es fs w hcount rest ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, hr⟩ := hc
      have h := (edgeOK_sound he).1
      change gam b (suffixPad b a e.B) e.C + sumGam b fs =
        gam b e.B e.C + sumGam b es
      rw [gam_suffixPad h a, ih e.B2 e.C2 hr]

/-- Both interface carry streams and the overflow stream are preserved. -/
theorem streams_eq (hp : PadChain b a z es fs) (B C : List Nat)
    (hc : chainOK b es B C = true) :
    fs.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) =
      es.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) := by
  induction hp generalizing B C with
  | nil => rfl
  | @cons a a' z e es fs w hcount rest ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, _⟩, he⟩, hr⟩ := hc
      have h := (edgeOK_sound he).1
      change
        (e1 b (suffixPad b a e.B), e2 b (suffixPad b a e.B) e.C,
          gam b (suffixPad b a e.B) e.C) ::
          fs.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C)) =
        (e1 b e.B, e2 b e.B e.C, gam b e.B e.C) ::
          es.map (fun e => (e1 b e.B, e2 b e.B e.C, gam b e.B e.C))
      rw [e1_suffixPad h a, e2_suffixPad h a, gam_suffixPad h a, ih e.B2 e.C2 hr]

/-- Closed padding offsets preserve exactly the original Boolean cycle test. -/
theorem cycleOK_iff {a : Nat} (hp : PadChain b a a es fs) (B C : List Nat) :
    cycleOK b fs (suffixPad b a B) C = true ↔ cycleOK b es B C = true := by
  by_cases hc : chainOK b es B C = true
  · simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq]
    rw [hp.not_nil_iff, hp.chainOK_iff B C, hp.endB_eq B, hp.endC_eq C,
      suffixPad_eq_iff, hp.sumGam_eq B C hc, hp.sumGain_eq]
  · have hf : chainOK b fs (suffixPad b a B) C ≠ true := by
      intro h
      exact hc ((hp.chainOK_iff B C).1 h)
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq]
    simp [hc, hf]

end PadChain

end Agent114.NeutralExteriorCycle

#print axioms Agent114.NeutralExteriorCycle.PadChain.length_eq
#print axioms Agent114.NeutralExteriorCycle.PadChain.endB_eq
#print axioms Agent114.NeutralExteriorCycle.PadChain.endC_eq
#print axioms Agent114.NeutralExteriorCycle.PadChain.chainOK_iff
#print axioms Agent114.NeutralExteriorCycle.PadChain.gain_balance
#print axioms Agent114.NeutralExteriorCycle.PadChain.sumGam_eq
#print axioms Agent114.NeutralExteriorCycle.PadChain.streams_eq
#print axioms Agent114.NeutralExteriorCycle.PadChain.cycleOK_iff
