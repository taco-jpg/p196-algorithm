import P196.LatticeBand.Pairs

/-!
# One reverse-and-add step on a lattice template

For `l = |W|·(q+1) + ρ` with `q ≥ 1` the digit word of `val (tm B W l)` is `Lw ++ rp Y q ++ Rw`
(`Digits.lean`), so its mirrored digit sums are `Hh ++ band (gen Y d) ++ reverse Hh` (`Pairs.lean`)
with `d = |W| - ρ - gm`.  When the outer part is `B2 ++ W2`, the new period block is `W2 = gen Y d`
and `W2` is symmetric with respect to the shift `d`, the result is again a template, of band length
`l + gm`.  Every hypothesis on `(B2, W2)` is a finite check on lists of fixed length.
-/

namespace LatticeBand

open Agent120.Neutral

/-- Extending a band by one period on the right appends the reversed block, if the band is symmetric. -/
theorem band_append_rev (W : List Nat) (hW : W ≠ []) (x : Nat)
    (hsym : ∀ s, s < W.length → gv W ((x + s) % W.length) = gv W (W.length - 1 - s)) :
    band W (x + W.length) = band W x ++ W.reverse := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  have hlx := length_band W hW x
  have hlx2 := length_band W hW (x + W.length)
  apply List.ext_getElem?
  intro i
  by_cases hi : i < x
  · rw [List.getElem?_append_left (by omega),
      getElem?_eq_some_gv _ _ (by omega), getElem?_eq_some_gv _ _ (by omega),
      gv_band W hW _ _ (by omega), gv_band W hW _ _ hi]
  · by_cases hi2 : i < x + W.length
    · rw [List.getElem?_append_right (by omega), hlx,
        getElem?_eq_some_gv _ _ (by omega), getElem?_eq_some_gv _ _ (by simp; omega),
        gv_band W hW _ _ hi2, gv_reverse W _ (by omega)]
      have := hsym (i - x) (by omega)
      rw [show x + (i - x) = i by omega] at this
      rw [this]
    · rw [List.getElem?_eq_none (by omega), List.getElem?_eq_none (by simp; omega)]

/-- Symmetry of the band under reflection (the band is its own mirror image). -/
theorem band_symm (W : List Nat) (hW : W ≠ []) (x : Nat)
    (hsym : ∀ s, s < W.length → gv W ((x + s) % W.length) = gv W (W.length - 1 - s)) :
    band W (W.length + (x + W.length)) = W ++ (band W x ++ W.reverse) := by
  rw [band_add_period W hW, band_append_rev W hW x hsym]


/-- Shift of the mirror alignment: `d = |W| - ρ - gm`. -/
def dd (b : Nat) (B W : List Nat) (ρ cs : Nat) : Nat := W.length - ρ - gm b B W ρ cs

section
variable {b : Nat} {B W : List Nat} {cs : Nat}

theorem length_Rw' (h : LHyp b B W cs) (ρ : Nat) (hρ : ρ < W.length) :
    (Rw b B W ρ cs).length = ρ + B.length + gm b B W ρ cs := by
  have hg := h.gm_le ρ
  unfold Rw
  simp only [List.length_append, length_Zb, length_DRb]
  rcases (by omega : gm b B W ρ cs = 0 ∨ gm b B W ρ cs = 1) with h0 | h1
  · simp [h0]; omega
  · simp [h1]; omega

theorem Yb_ne (h : LHyp b B W cs) : Yb b W cs ≠ [] := by
  intro he
  have := length_Yb (b := b) (W := W) (cs := cs)
  rw [he] at this
  have := List.length_pos_iff.mpr h.wne
  simp_all

/-- Mirrored digit sums of the template digit word. -/
theorem pairs_tm (h : LHyp b B W cs) (q ρ : Nat) (hρ : ρ < W.length) (hq : 1 ≤ q) :
    pairs (digits b (val b (tm B W (W.length * (q + 1) + ρ)))) =
      Hh (Lw b B W) (Rw b B W ρ cs) (Yb b W cs) ++
        (band (gen (Yb b W cs) (dd b B W ρ cs)) (W.length * q - dd b B W ρ cs) ++
          (Hh (Lw b B W) (Rw b B W ρ cs) (Yb b W cs)).reverse) := by
  have hg := h.gm_le ρ
  have hlr := length_Rw' h ρ hρ
  have hll := length_Lw (b := b) (B := B) (W := W)
  rw [digits_tm h q ρ hρ]
  have := pairs_lattice (Yb b W cs) (Lw b B W) (Rw b B W ρ cs) q (dd b B W ρ cs) (Yb_ne h) hq
    (by rw [length_Yb]; unfold dd; omega) (by unfold dd; omega)
  rw [this, length_Yb]

/-- One step of reverse-and-add maps the template to the next template. -/
theorem step_tm (h : LHyp b B W cs) (q ρ : Nat) (hρ : ρ < W.length) (hq : 1 ≤ q)
    (B2 W2 : List Nat)
    (hH : Hh (Lw b B W) (Rw b B W ρ cs) (Yb b W cs) = B2 ++ W2)
    (hG : gen (Yb b W cs) (dd b B W ρ cs) = W2)
    (hsym : ∀ s, s < W.length →
      gv W2 ((s + W.length - dd b B W ρ cs) % W.length) = gv W2 (W.length - 1 - s)) :
    step b (val b (tm B W (W.length * (q + 1) + ρ))) =
      val b (tm B2 W2 (W.length * (q + 1) + ρ + gm b B W ρ cs)) := by
  have hb := h.base
  have hg := h.gm_le ρ
  have hm : 0 < W.length := List.length_pos_iff.mpr h.wne
  have hW2len : W2.length = W.length := by
    rw [← hG, length_gen, length_Yb]
  have hW2 : W2 ≠ [] := by
    intro he; rw [he] at hW2len; simp at hW2len; omega
  rw [step_eq_val_pairs b hb, pairs_tm h q ρ hρ hq, hH, hG]
  congr 1
  have hd : dd b B W ρ cs ≤ W.length := by unfold dd; omega
  have hmq : W.length ≤ W.length * q := Nat.le_mul_of_pos_right _ hq
  have hx : W.length * q - dd b B W ρ cs = W.length * (q - 1) + (W.length - dd b B W ρ cs) := by
    have : W.length * q = W.length * (q - 1) + W.length := by
      rw [← Nat.mul_succ]; congr 1; omega
    omega
  have hl : W2.length + (W.length * q - dd b B W ρ cs + W2.length) =
      W.length * (q + 1) + ρ + gm b B W ρ cs := by
    rw [hW2len, Nat.mul_succ]; unfold dd at *; omega
  have hsym' : ∀ s, s < W2.length →
      gv W2 ((W.length * q - dd b B W ρ cs + s) % W2.length) = gv W2 (W2.length - 1 - s) := by
    intro s hs
    rw [hW2len] at hs ⊢
    have e : (W.length * q - dd b B W ρ cs + s) % W.length
        = (s + W.length - dd b B W ρ cs) % W.length := by
      rw [hx, show W.length * (q - 1) + (W.length - dd b B W ρ cs) + s
        = (s + W.length - dd b B W ρ cs) + W.length * (q - 1) by omega,
        Nat.add_mul_mod_self_left]
    rw [e]
    exact hsym s hs
  have hb2 := band_symm W2 hW2 (W.length * q - dd b B W ρ cs) hsym'
  unfold tm
  rw [← hl, hb2]
  simp [List.append_assoc]

/-- The template value is not a palindrome as soon as the left end is not the mirror of the right end. -/
theorem not_isPal_tm (h : LHyp b B W cs) (q ρ : Nat) (hρ : ρ < W.length)
    (hnp : (Lw b B W).take (Rw b B W ρ cs).length ≠ (Rw b B W ρ cs).reverse) :
    ¬ IsPal b (val b (tm B W (W.length * (q + 1) + ρ))) := by
  unfold IsPal
  rw [digits_tm h q ρ hρ]
  intro hpal
  have hg := h.gm_le ρ
  have hlr := length_Rw' h ρ hρ
  have hll := length_Lw (b := b) (B := B) (W := W)
  have hle : (Rw b B W ρ cs).length ≤ (Lw b B W).length := by omega
  apply hnp
  have e : (Lw b B W ++ (rp (Yb b W cs) q ++ Rw b B W ρ cs)).reverse =
      ((Rw b B W ρ cs).reverse ++ (rp (Yb b W cs) q).reverse) ++ (Lw b B W).reverse := by
    simp [List.reverse_append, List.append_assoc]
  have h1 := congrArg (List.take (Rw b B W ρ cs).length) hpal
  rw [e, List.take_append_of_le_length hle,
    List.take_append_of_le_length (show (Rw b B W ρ cs).length ≤
      ((Rw b B W ρ cs).reverse ++ (rp (Yb b W cs) q).reverse).length by simp),
    List.take_left' (by simp)] at h1
  exact h1

end

end LatticeBand
