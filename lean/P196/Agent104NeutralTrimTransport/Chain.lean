import P196.Agent104NeutralTrimTransport.Structure

/-!
Whole-chain transport from a local padding law. The generic interface below
is a hypothesis, not a new axiom: the concrete neutral-padding instance is
supplied separately from Agent119's local covariance theorem.
-/

namespace Agent104.NeutralTrimTransport

open Agent120.Neutral

/-- Exactly the local facts needed by the complete-cycle construction. -/
structure PaddingLaws (b : Nat) (pad : Nat → List Nat → List Nat) : Prop where
  edge_transport : ∀ {E : Edge}, edgeOK b E = true →
    ∀ {a a' w : Nat}, a + E.v = w + a' →
      edgeOK b { E with C := pad a E.C, C2 := pad a' E.C2, v := w } = true
  gam_preserved : ∀ {B C : List Nat}, Hyp b B C → ∀ a : Nat,
    gam b B (pad a C) = gam b B C

/-- The additive offsets match at every seam of the checked chain. -/
theorem retime_chainOK {b : Nat} {pad : Nat → List Nat → List Nat}
    (laws : PaddingLaws b pad) (q : Nat) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hl : es.length = ws.length)
    (hc : chainOK b es B C = true) :
    chainOK b (retime pad q es ws) B (pad (q + ws.sum) C) = true := by
  induction es generalizing q ws B C with
  | nil =>
      cases ws with
      | nil => rfl
      | cons w ws => simp at hl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨⟨⟨hB, hC⟩, he⟩, hes⟩ := hc
          subst hB
          subst hC
          have he' := laws.edge_transport he
            (a := q + w + ws.sum) (a' := q + E.v + ws.sum) (w := w) (by omega)
          have hi := ih (q + E.v) ws E.B2 E.C2 ht hes
          simpa only [retime, chainOK, List.sum_cons, Nat.add_assoc,
            decide_true, Bool.true_and, Bool.and_eq_true] using And.intro he' hi

/-- Padding changes neither the lower carry nor the overflow at any phase. -/
theorem retime_streams {b : Nat} {pad : Nat → List Nat → List Nat}
    (laws : PaddingLaws b pad) (q : Nat) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hl : es.length = ws.length)
    (hc : chainOK b es B C = true) :
    (retime pad q es ws).map (fun E => (e1 b E.B, gam b E.B E.C)) =
      es.map (fun E => (e1 b E.B, gam b E.B E.C)) := by
  induction es generalizing q ws B C with
  | nil =>
      cases ws with
      | nil => rfl
      | cons w ws => simp at hl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨⟨⟨_, _⟩, he⟩, hes⟩ := hc
          have hg := laws.gam_preserved (edgeOK_sound he).1 (q + w + ws.sum)
          have hi := ih (q + E.v) ws E.B2 E.C2 ht hes
          simpa only [retime, List.map_cons, hg] using congrArg
            (List.cons (e1 b E.B, gam b E.B E.C)) hi

theorem retime_sumGam {b : Nat} {pad : Nat → List Nat → List Nat}
    (laws : PaddingLaws b pad) (q : Nat) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hl : es.length = ws.length)
    (hc : chainOK b es B C = true) :
    sumGam b (retime pad q es ws) = sumGam b es := by
  induction es generalizing q ws B C with
  | nil =>
      cases ws with
      | nil => rfl
      | cons w ws => simp at hl
  | cons E es ih =>
      cases ws with
      | nil => simp at hl
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hl
          simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
          obtain ⟨⟨⟨_, _⟩, he⟩, hes⟩ := hc
          have hg := laws.gam_preserved (edgeOK_sound he).1 (q + w + ws.sum)
          have hi := ih (q + E.v) ws E.B2 E.C2 ht hes
          simpa only [retime, sumGam, hg] using congrArg
            (Nat.add (gam b E.B E.C)) hi

/-- Equal trim totals close the padded chain and preserve the gain test. -/
theorem cycleOK_retime_of_laws {b : Nat} {pad : Nat → List Nat → List Nat}
    (laws : PaddingLaws b pad) (es : List Edge) (ws : List Nat)
    (B C : List Nat) (hc : cycleOK b es B C = true)
    (hl : es.length = ws.length) (hs : ws.sum = sumV es) :
    cycleOK b (retime pad 0 es ws) B (pad ws.sum C) = true := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hc ⊢
  obtain ⟨⟨⟨⟨hne, hch⟩, hB⟩, hC⟩, hgain⟩ := hc
  have hlen := retime_length pad 0 es ws hl
  have hne' : retime pad 0 es ws ≠ [] := by
    intro he
    have hz : es.length = 0 := by simpa [he] using hlen.symm
    exact hne (List.length_eq_zero_iff.mp hz)
  have hch' := retime_chainOK laws 0 es ws B C hl hch
  have hB' := retime_endB pad 0 es ws B hl
  have hC' := retime_endC pad 0 es ws C hl
  have hg := retime_sumGam laws 0 es ws B C hl hch
  have hu := retime_sumGain pad 0 es ws hl
  refine ⟨⟨⟨⟨hne', ?_⟩, ?_⟩, ?_⟩, ?_⟩
  · simpa using hch'
  · simpa [hB] using hB'
  · simpa [hs, hC] using hC'
  · omega

end Agent104.NeutralTrimTransport

#print axioms Agent104.NeutralTrimTransport.retime_chainOK
#print axioms Agent104.NeutralTrimTransport.retime_streams
#print axioms Agent104.NeutralTrimTransport.retime_sumGam
#print axioms Agent104.NeutralTrimTransport.cycleOK_retime_of_laws
