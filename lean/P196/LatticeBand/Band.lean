import P196.Drafts.Agent120NeutralBandCalibration.A120Template

/-!
# Periodic bands

`rp W q` is `q` copies of the period block `W`; `band W l` is the first `l` entries of the
periodic word `W W W ...` (phase 0).  These are the only objects of the lattice format; the
facts below are elementary list/arithmetic lemmas (no reverse-and-add yet).
-/

namespace LatticeBand

open Agent120.Neutral

/-- `q` copies of the block `W`. -/
def rp (W : List Nat) : Nat → List Nat
  | 0 => []
  | q + 1 => W ++ rp W q

/-- The first `l` entries of the periodic word `W W W ...`. -/
def band (W : List Nat) (l : Nat) : List Nat :=
  rp W (l / W.length) ++ W.take (l % W.length)

@[simp] theorem rp_zero (W : List Nat) : rp W 0 = [] := rfl
@[simp] theorem rp_succ (W : List Nat) (q : Nat) : rp W (q + 1) = W ++ rp W q := rfl

theorem length_rp (W : List Nat) : ∀ q, (rp W q).length = W.length * q
  | 0 => by simp
  | q + 1 => by
      simp only [rp_succ, List.length_append, length_rp W q]
      rw [Nat.mul_succ]; omega

theorem rp_succ' (W : List Nat) : ∀ q, rp W (q + 1) = rp W q ++ W
  | 0 => by simp
  | q + 1 => by
      have ih := rp_succ' W q
      calc rp W (q + 1 + 1) = W ++ rp W (q + 1) := rfl
        _ = W ++ (rp W q ++ W) := by rw [ih]
        _ = (W ++ rp W q) ++ W := by rw [List.append_assoc]
        _ = rp W (q + 1) ++ W := rfl

theorem reverse_rp (W : List Nat) : ∀ q, (rp W q).reverse = rp W.reverse q
  | 0 => rfl
  | q + 1 => by
      rw [rp_succ', List.reverse_append, reverse_rp W q, rp_succ]

theorem getElem_rp (W : List Nat) (hW : W ≠ []) :
    ∀ (q i : Nat) (h : i < (rp W q).length), (rp W q)[i] = W[i % W.length]'(
      Nat.mod_lt _ (List.length_pos_iff.mpr hW))
  | 0, i, h => by simp at h
  | q + 1, i, h => by
      have hm : 0 < W.length := List.length_pos_iff.mpr hW
      by_cases hi : i < W.length
      · simp only [rp_succ]
        rw [List.getElem_append_left (by simpa using hi)]
        simp [Nat.mod_eq_of_lt hi]
      · simp only [rp_succ] at h ⊢
        rw [List.getElem_append_right (by omega)]
        have h' : i - W.length < (rp W q).length := by
          simp only [List.length_append] at h; omega
        rw [getElem_rp W hW q (i - W.length) h']
        congr 1
        rw [show i = (i - W.length) + W.length by omega, Nat.add_mod_right]
        simp

theorem length_band (W : List Nat) (hW : W ≠ []) (l : Nat) : (band W l).length = l := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  have h1 := Nat.mod_lt l hm
  simp only [band, List.length_append, length_rp, List.length_take]
  have h2 := Nat.div_add_mod l W.length
  rw [Nat.min_eq_left (by omega)]
  omega

theorem band_add_period (W : List Nat) (hW : W ≠ []) (l : Nat) :
    band W (W.length + l) = W ++ band W l := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  unfold band
  rw [Nat.add_div_left _ hm, Nat.add_mod_left, rp_succ, List.append_assoc]

theorem band_eq_rp (W : List Nat) (hW : W ≠ []) (q ρ : Nat) (hρ : ρ < W.length) :
    band W (W.length * q + ρ) = rp W q ++ W.take ρ := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  unfold band
  rw [Nat.mul_add_div hm, Nat.mul_add_mod, Nat.div_eq_of_lt hρ, Nat.mod_eq_of_lt hρ]
  simp

theorem getElem_band (W : List Nat) (hW : W ≠ []) (l i : Nat) (h : i < (band W l).length) :
    (band W l)[i] = W[i % W.length]'(Nat.mod_lt _ (List.length_pos_iff.mpr hW)) := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  have hl := length_band W hW l
  have hi : i < l := by omega
  obtain ⟨q, ρ, hρ, rfl⟩ : ∃ q ρ, ρ < W.length ∧ l = W.length * q + ρ :=
    ⟨l / W.length, l % W.length, Nat.mod_lt _ hm, (Nat.div_add_mod l W.length).symm⟩
  simp only [band_eq_rp W hW q ρ hρ] at h ⊢
  by_cases hiq : i < (rp W q).length
  · rw [List.getElem_append_left hiq, getElem_rp W hW q i hiq]
  · rw [List.getElem_append_right (by omega)]
    have hlen := length_rp W q
    have hlt : i - (rp W q).length < ρ := by
      have : (rp W q ++ W.take ρ).length = W.length * q + ρ := by simpa [band_eq_rp W hW q ρ hρ] using hl
      simp only [List.length_append] at this
      omega
    rw [List.getElem_take]
    have : i = W.length * q + (i - (rp W q).length) := by omega
    congr 1
    rw [this, Nat.mul_add_mod]
    rw [Nat.mod_eq_of_lt (by omega)]
    omega

end LatticeBand
