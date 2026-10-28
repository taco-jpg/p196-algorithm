import P196.LatticeBand.Step
import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Certificates for lattice templates

A *state* is `(B, W, ρ)`; it stands for every template `tm B W l` with `2|W| ≤ l` and `l mod |W| = ρ`.
An edge `(B, W, ρ) → (B2, W2)` is checked by evaluating the exact transition of `Step.lean`; the new
band length is `l + gm` (so the phase becomes `(ρ + gm) mod |W|`).  Band lengths never decrease, so
no gain condition is needed: a checked closed cycle certifies every `l ≥ 2|W|` with `l mod |W| = ρ`.
-/

namespace LatticeBand

open Agent120.Neutral

/-- One transition. -/
structure LEdge where
  B : List Nat
  W : List Nat
  ρ : Nat
  B2 : List Nat
  W2 : List Nat
  deriving DecidableEq, Repr

/-- Absorbing carry of the block of an edge. -/
def lcs (b : Nat) (E : LEdge) : Nat := (norm b E.W 0).2

/-- Overflow of an edge. -/
def lgam (b : Nat) (E : LEdge) : Nat := gm b E.B E.W E.ρ (lcs b E)

/-- Executable check of one edge. -/
def ledgeOK (b : Nat) (E : LEdge) : Bool :=
  decide (2 ≤ b) && decide (E.B ≠ []) && decide (E.B.head? ≠ some 0) &&
    E.B.all (fun v => decide (v ≤ 2 * (b - 1))) && E.W.all (fun v => decide (v ≤ 2 * (b - 1))) &&
    decide (E.W ≠ []) && decide ((norm b E.W 1).2 = lcs b E) && decide (E.ρ < E.W.length) &&
    decide (Hh (Lw b E.B E.W) (Rw b E.B E.W E.ρ (lcs b E)) (Yb b E.W (lcs b E)) = E.B2 ++ E.W2) &&
    decide (gen (Yb b E.W (lcs b E)) (dd b E.B E.W E.ρ (lcs b E)) = E.W2) &&
    (List.range E.W.length).all (fun s =>
      decide (gv E.W2 ((s + E.W.length - dd b E.B E.W E.ρ (lcs b E)) % E.W.length) =
        gv E.W2 (E.W.length - 1 - s))) &&
    decide ((Lw b E.B E.W).take (Rw b E.B E.W E.ρ (lcs b E)).length ≠
      (Rw b E.B E.W E.ρ (lcs b E)).reverse)

theorem ledgeOK_sound {b : Nat} {E : LEdge} (h : ledgeOK b E = true) :
    LHyp b E.B E.W (lcs b E) ∧ E.ρ < E.W.length ∧
      Hh (Lw b E.B E.W) (Rw b E.B E.W E.ρ (lcs b E)) (Yb b E.W (lcs b E)) = E.B2 ++ E.W2 ∧
      gen (Yb b E.W (lcs b E)) (dd b E.B E.W E.ρ (lcs b E)) = E.W2 ∧
      (∀ s, s < E.W.length →
        gv E.W2 ((s + E.W.length - dd b E.B E.W E.ρ (lcs b E)) % E.W.length) =
          gv E.W2 (E.W.length - 1 - s)) ∧
      (Lw b E.B E.W).take (Rw b E.B E.W E.ρ (lcs b E)).length ≠
        (Rw b E.B E.W E.ρ (lcs b E)).reverse := by
  simp only [ledgeOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    List.mem_range] at h
  obtain ⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨⟨hb, hne⟩, hext⟩, hB⟩, hW⟩, hWne⟩, habs1⟩, hρ⟩, hH⟩, hG⟩, hsym⟩, hnp⟩ := h
  exact ⟨⟨hb, hB, hW, hne, hext, hWne, rfl, habs1⟩, hρ, hH, hG, hsym, hnp⟩

/-- One checked edge: exact step, palindrome freedom, and the new block length. -/
theorem ledge_step {b : Nat} {E : LEdge} (h : ledgeOK b E = true) (l : Nat)
    (hl : 2 * E.W.length ≤ l) (hρ : l % E.W.length = E.ρ) :
    ¬ IsPal b (val b (tm E.B E.W l)) ∧
      step b (val b (tm E.B E.W l)) = val b (tm E.B2 E.W2 (l + lgam b E)) ∧
      E.W2.length = E.W.length := by
  obtain ⟨hyp, hρlt, hH, hG, hsym, hnp⟩ := ledgeOK_sound h
  have hm : 0 < E.W.length := List.length_pos_iff.mpr hyp.wne
  obtain ⟨q, hq, rfl⟩ : ∃ q, 1 ≤ q ∧ l = E.W.length * (q + 1) + E.ρ := by
    refine ⟨l / E.W.length - 1, ?_, ?_⟩
    · have : 2 ≤ l / E.W.length := (Nat.le_div_iff_mul_le hm).mpr (by omega)
      omega
    · have h1 := Nat.div_add_mod l E.W.length
      rw [hρ] at h1
      have : 2 ≤ l / E.W.length := (Nat.le_div_iff_mul_le hm).mpr (by omega)
      rw [show l / E.W.length - 1 + 1 = l / E.W.length by omega]
      omega
  refine ⟨not_isPal_tm hyp q E.ρ hρlt hnp, ?_, ?_⟩
  · exact step_tm hyp q E.ρ hρlt hq E.B2 E.W2 hH hG hsym
  · rw [← hG, length_gen, length_Yb]

/-- Chained edges starting at a given state. -/
def lchainOK (b : Nat) : List LEdge → List Nat → List Nat → Nat → Bool
  | [], _, _, _ => true
  | e :: es, B, W, ρ =>
      decide (e.B = B) && decide (e.W = W) && decide (e.ρ = ρ) && ledgeOK b e &&
        lchainOK b es e.B2 e.W2 ((e.ρ + lgam b e) % e.W.length)

/-- Final block of a chain. -/
def endB : List LEdge → List Nat → List Nat
  | [], B => B
  | e :: es, _ => endB es e.B2

/-- Final period word of a chain. -/
def endW : List LEdge → List Nat → List Nat
  | [], W => W
  | e :: es, _ => endW es e.W2

/-- Total overflow along a chain. -/
def sumGamL (b : Nat) : List LEdge → Nat
  | [] => 0
  | e :: es => lgam b e + sumGamL b es

/-- Running a checked chain: palindrome freedom and the exact final template. -/
theorem lchain_run (b : Nat) :
    ∀ (es : List LEdge) (B W : List Nat) (ρ l : Nat), lchainOK b es B W ρ = true →
      2 * W.length ≤ l → l % W.length = ρ →
      (∀ k, k < es.length → ¬ IsPal b (orbit b (val b (tm B W l)) k)) ∧
      orbit b (val b (tm B W l)) es.length =
        val b (tm (endB es B) (endW es W) (l + sumGamL b es)) ∧
      (endW es W).length = W.length
  | [], B, W, ρ, l, _, _, _ => by
      refine ⟨fun k hk => by simp at hk, ?_, rfl⟩
      simp [orbit, endB, endW, sumGamL]
  | e :: es, B, W, ρ, l, hc, hl, hρ => by
      simp only [lchainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨⟨hB, hW⟩, hr⟩, he⟩, hes⟩ := hc
      subst hB; subst hW; subst hr
      obtain ⟨hnp, hstep, hlen⟩ := ledge_step he l hl hρ
      have hl2 : 2 * e.W2.length ≤ l + lgam b e := by omega
      have hρ2 : (l + lgam b e) % e.W2.length = (e.ρ + lgam b e) % e.W.length := by
        rw [hlen, Nat.add_mod, hρ, Nat.add_mod_mod]
      obtain ⟨ihp, ihe, ihl⟩ := lchain_run b es e.B2 e.W2 _ (l + lgam b e) hes hl2 hρ2
      refine ⟨?_, ?_, ?_⟩
      · intro k hk
        cases k with
        | zero => simpa [orbit] using hnp
        | succ k =>
            have hk' : k < es.length := by simpa using hk
            have := ihp k hk'
            rwa [show k + 1 = 1 + k by omega, orbit_add,
              show orbit b (val b (tm e.B e.W l)) 1 = step b (val b (tm e.B e.W l)) from rfl,
              hstep]
      · have hlen' : (e :: es).length = 1 + es.length := by simp <;> omega
        rw [hlen', orbit_add,
          show orbit b (val b (tm e.B e.W l)) 1 = step b (val b (tm e.B e.W l)) from rfl,
          hstep, ihe]
        simp only [endB, endW, sumGamL]
        rw [Nat.add_assoc]
      · simp only [endW]; rw [ihl, hlen]

/-- Executable check of a cycle certificate based at the state `(B, W, ρ)`. -/
def lcycleOK (b : Nat) (es : List LEdge) (B W : List Nat) (ρ : Nat) : Bool :=
  decide (es ≠ []) && lchainOK b es B W ρ && decide (endB es B = B) && decide (endW es W = W) &&
    decide ((ρ + sumGamL b es) % W.length = ρ)

/-- A checked cycle certifies every template value of its state. -/
theorem lychrel_of_lcycle (b : Nat) (es : List LEdge) (B W : List Nat) (ρ : Nat)
    (hcert : lcycleOK b es B W ρ = true) (l : Nat) (hl : 2 * W.length ≤ l)
    (hρ : l % W.length = ρ) : Lychrel b (val b (tm B W l)) := by
  simp only [lcycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨hne, hch⟩, hB⟩, hW⟩, hgain⟩ := hcert
  have hlen : 0 < es.length := List.length_pos_iff.mpr hne
  have rounds : ∀ n : Nat, ∃ G, 2 * W.length ≤ G ∧ G % W.length = ρ ∧
      orbit b (val b (tm B W l)) (n * es.length) = val b (tm B W G) := by
    intro n
    induction n with
    | zero => exact ⟨l, hl, hρ, by simp [orbit]⟩
    | succ n ih =>
        obtain ⟨G, hG, hGρ, hEq⟩ := ih
        obtain ⟨_, hrun, _⟩ := lchain_run b es B W ρ G hch hG hGρ
        refine ⟨G + sumGamL b es, by omega, ?_, ?_⟩
        · rw [Nat.add_mod, hGρ, Nat.add_mod_mod]; exact hgain
        · rw [Nat.succ_mul, orbit_add, hEq, hrun, hB, hW]
  intro t
  have hdiv := Nat.div_add_mod t es.length
  obtain ⟨G, hG, hGρ, hEq⟩ := rounds (t / es.length)
  have hr : t % es.length < es.length := Nat.mod_lt _ hlen
  obtain ⟨hnp, _⟩ := lchain_run b es B W ρ G hch hG hGρ
  have := hnp (t % es.length) hr
  rw [← hdiv, Nat.mul_comm, orbit_add, hEq]
  exact this

end LatticeBand

#print axioms LatticeBand.ledge_step
#print axioms LatticeBand.lchain_run
#print axioms LatticeBand.lychrel_of_lcycle
