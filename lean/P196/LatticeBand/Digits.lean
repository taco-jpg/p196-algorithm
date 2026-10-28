import P196.LatticeBand.Band

/-!
# Exact digit word of a lattice template

Template: `tm B W l = B ++ (band W l ++ reverse B)`.  The period block `W` is *absorbing*: its
outgoing carry is the same constant `cs` for incoming carry `0` and `1`.  Hence in a run
`W^(q+1)` only the first copy sees the carry coming out of `B`; later copies see `cs`.
For `l = |W|·(q+1) + ρ` (`ρ < |W|`) the digit word of the value is

  `Lw ++ rp Y q ++ Rw`,   `Lw = DB ++ X1`,   `Rw = Z ++ DR (++ [1] on overflow)`.

Nothing here is specific to a base or to 196.
-/

namespace LatticeBand

open Agent120.Neutral

/-- Template coefficient word. -/
def tm (B W : List Nat) (l : Nat) : List Nat := B ++ (band W l ++ B.reverse)

/-- Digits of the canonical value of a list whose normalization carries out `γ ≤ 1`. -/
theorem digits_of_norm (b : Nat) (hb : 2 ≤ b) (T D : List Nat) (γ : Nat)
    (hn : norm b T 0 = (D, γ)) (hγ : γ ≤ 1) (hlast : γ = 0 → D.getLast? ≠ some 0) :
    digits b (val b T) = if γ = 0 then D else D ++ [1] := by
  have hv := norm_val b T 0
  rw [hn] at hv
  simp only [Nat.add_zero] at hv
  have hlen : D.length = T.length := by
    have := norm_length b T 0
    rw [hn] at this; exact this
  have hlt : ∀ d ∈ D, d < b := by
    have := norm_digit_lt b (by omega) T 0
    rw [hn] at this; exact this
  have hvT : val b T = val b D + b ^ D.length * γ := by rw [hlen]; omega
  rcases (by omega : γ = 0 ∨ γ = 1) with h0 | h1
  · subst h0
    simp only [Nat.mul_zero, Nat.add_zero, if_true] at hvT ⊢
    rw [hvT]
    exact digits_val b hb D ⟨hlt, hlast rfl⟩
  · subst h1
    simp only [Nat.mul_one, Nat.one_ne_zero, if_false] at hvT ⊢
    have : val b (D ++ [1]) = val b D + b ^ D.length := by rw [val_append]; simp
    rw [hvT, ← this]
    apply digits_val b hb
    refine ⟨?_, by simp⟩
    intro d hd
    simp only [List.mem_append, List.mem_singleton] at hd
    rcases hd with hd | rfl
    · exact hlt d hd
    · omega

/-- A run of absorbing blocks entered with the fixed carry reproduces itself. -/
theorem norm_rp_fix {b : Nat} {W : List Nat} {cs : Nat} (hfix : (norm b W cs).2 = cs) :
    ∀ q, norm b (rp W q) cs = (rp (norm b W cs).1 q, cs)
  | 0 => rfl
  | q + 1 => by
      rw [rp_succ, norm_append, hfix, norm_rp_fix hfix q, rp_succ]

/-- An absorbing run swallows its incoming carry (only the first copy sees it). -/
theorem norm_rp_absorb {b : Nat} {W : List Nat} {cs e : Nat} (he : (norm b W e).2 = cs)
    (hfix : (norm b W cs).2 = cs) (q : Nat) :
    norm b (rp W (q + 1)) e = ((norm b W e).1 ++ rp (norm b W cs).1 q, cs) := by
  rw [rp_succ, norm_append, he, norm_rp_fix hfix q]

/-- Hypotheses of the one-step theorem. -/
structure LHyp (b : Nat) (B W : List Nat) (cs : Nat) : Prop where
  base : 2 ≤ b
  boundB : ∀ v ∈ B, v ≤ 2 * (b - 1)
  boundW : ∀ v ∈ W, v ≤ 2 * (b - 1)
  ne : B ≠ []
  ext : B.head? ≠ some 0
  wne : W ≠ []
  abs0 : (norm b W 0).2 = cs
  abs1 : (norm b W 1).2 = cs

/-- First copy of the block, entered with the carry out of `B`. -/
def X1 (b : Nat) (B W : List Nat) : List Nat := (norm b W (e1 b B)).1
/-- Steady digits of one block (entered with the absorbing carry). -/
def Yb (b : Nat) (W : List Nat) (cs : Nat) : List Nat := (norm b W cs).1
/-- Partial last block. -/
def Zb (b : Nat) (W : List Nat) (ρ cs : Nat) : List Nat := (norm b (W.take ρ) cs).1
/-- Carry leaving the partial block. -/
def cc (b : Nat) (W : List Nat) (ρ cs : Nat) : Nat := (norm b (W.take ρ) cs).2
/-- Upper copy of `B`. -/
def DRb (b : Nat) (B W : List Nat) (ρ cs : Nat) : List Nat := (norm b B.reverse (cc b W ρ cs)).1
/-- Overflow: `1` iff the value gains a digit. -/
def gm (b : Nat) (B W : List Nat) (ρ cs : Nat) : Nat := (norm b B.reverse (cc b W ρ cs)).2

/-- Left end of the digit word. -/
def Lw (b : Nat) (B W : List Nat) : List Nat := DB b B ++ X1 b B W
/-- Right end of the digit word. -/
def Rw (b : Nat) (B W : List Nat) (ρ cs : Nat) : List Nat :=
  Zb b W ρ cs ++ (DRb b B W ρ cs ++ (if gm b B W ρ cs = 0 then [] else [1]))

section
variable {b : Nat} {B W : List Nat} {cs : Nat}

theorem LHyp.cs_le (h : LHyp b B W cs) : cs ≤ 1 := by
  have := norm_carry_le_one b (by have := h.base; omega) W 0 h.boundW (by omega)
  rw [h.abs0] at this; exact this

theorem LHyp.e1_le (h : LHyp b B W cs) : e1 b B ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B 0 h.boundB (by omega)

theorem LHyp.cc_le (h : LHyp b B W cs) (ρ : Nat) : cc b W ρ cs ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) (W.take ρ) cs
    (fun v hv => h.boundW v (List.mem_of_mem_take hv)) h.cs_le

theorem LHyp.gm_le (h : LHyp b B W cs) (ρ : Nat) : gm b B W ρ cs ≤ 1 :=
  norm_carry_le_one b (by have := h.base; omega) B.reverse _
    (fun v hv => h.boundB v (List.mem_reverse.mp hv)) (h.cc_le ρ)

theorem length_X1 : (X1 b B W).length = W.length := norm_length b W _
theorem length_Yb : (Yb b W cs).length = W.length := norm_length b W _
theorem length_Zb (ρ : Nat) : (Zb b W ρ cs).length = min ρ W.length := by
  simp [Zb, norm_length]
theorem length_DRb (ρ : Nat) : (DRb b B W ρ cs).length = B.length := by
  simp [DRb, norm_length]

theorem length_Lw : (Lw b B W).length = B.length + W.length := by
  simp [Lw, X1, DB, norm_length]

/-- Exact digit word of the template value, band length `|W|·(q+1) + ρ`. -/
theorem digits_tm (h : LHyp b B W cs) (q ρ : Nat) (hρ : ρ < W.length) :
    digits b (val b (tm B W (W.length * (q + 1) + ρ))) =
      Lw b B W ++ (rp (Yb b W cs) q ++ Rw b B W ρ cs) := by
  have hb := h.base
  have hband := band_eq_rp W h.wne (q + 1) ρ hρ
  have habs : (norm b W (e1 b B)).2 = cs := by
    rcases (by have := h.e1_le; omega : e1 b B = 0 ∨ e1 b B = 1) with h0 | h1
    · rw [h0]; exact h.abs0
    · rw [h1]; exact h.abs1
  have hfix : (norm b W cs).2 = cs := by
    rcases (by have := h.cs_le; omega : cs = 0 ∨ cs = 1) with h0 | h1
    · subst h0; exact h.abs0
    · subst h1; exact h.abs1
  have hnorm : norm b (tm B W (W.length * (q + 1) + ρ)) 0 =
      (Lw b B W ++ (rp (Yb b W cs) q ++ (Zb b W ρ cs ++ DRb b B W ρ cs)), gm b B W ρ cs) := by
    unfold tm
    rw [hband, norm_append, norm_append, norm_append]
    rw [show (norm b B 0).2 = e1 b B from rfl, norm_rp_absorb habs hfix q]
    simp only [Lw, X1, Yb, Zb, DRb, gm, cc, DB, List.append_assoc]
  have hlast : gm b B W ρ cs = 0 →
      (Lw b B W ++ (rp (Yb b W cs) q ++ (Zb b W ρ cs ++ DRb b B W ρ cs))).getLast? ≠ some 0 := by
    intro h0
    obtain ⟨a, ha⟩ : ∃ a, B.head? = some a := by
      cases B with
      | nil => exact absurd rfl h.ne
      | cons x xs => exact ⟨x, rfl⟩
    have ha0 : a ≠ 0 := by intro h'; subst h'; exact h.ext ha
    have hra : B.reverse.getLast? = some a := by rw [List.getLast?_reverse]; exact ha
    obtain ⟨d, hd, had⟩ := norm_getLast?_ge b (by omega) B.reverse (cc b W ρ cs) a hra h0
    have hDR : (DRb b B W ρ cs).getLast? = some d := hd
    simp only [List.getLast?_append, hDR, Option.some_or]
    intro hd0
    simp only [Option.some.injEq] at hd0
    omega
  have hdig := digits_of_norm b hb _ _ _ hnorm (h.gm_le ρ) hlast
  rw [hdig]
  unfold Rw
  rcases (by have := h.gm_le ρ; omega : gm b B W ρ cs = 0 ∨ gm b B W ρ cs = 1) with h0 | h1
  · simp [h0]
  · simp [h1, List.append_assoc]

end

end LatticeBand
