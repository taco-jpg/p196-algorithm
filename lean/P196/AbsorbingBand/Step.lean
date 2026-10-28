import P196.AbsorbingBand.Absorb

/-!
# Absorbing-band templates: exact one-step dynamics

With `L = DB ++ [x]` and `R = (y :: DR)` (no overflow) or `R = DR ++ [1]` (overflow), the digit word of
the template value is `L ++ y^m ++ R` with `m = l + gam - 2`, its mirrored digit sums are again an
absorbing template with band value `y + y` and block `zipWith (+) L (reverse R)`, and the value is not a
palindrome as soon as `L ≠ reverse R`.  All statements hold for every band length `l` with
`2 ≤ l + gam`.
-/

namespace AbsorbingBand

open Agent120.Neutral

/-- Left interface word of the digit word. -/
def Lw (b : Nat) (B : List Nat) (c : Nat) : List Nat := DB b B ++ [xa b B c]

/-- Right interface word of the digit word. -/
def Rw (b : Nat) (B : List Nat) (c : Nat) : List Nat :=
  if gama b B c = 0 then ya b c :: DRa b B c else DRa b B c ++ [1]

/-- Next block (before moving band-valued coefficients into the band). -/
def nextBa (b : Nat) (B : List Nat) (c : Nat) : List Nat :=
  List.zipWith (· + ·) (Lw b B c) (Rw b B c).reverse

/-- Next band value. -/
def cnext (b c : Nat) : Nat := ya b c + ya b c

/-- Digit word of the template value, unified over the overflow cases. -/
def dW (b : Nat) (B : List Nat) (c l : Nat) : List Nat :=
  Lw b B c ++ (List.replicate (l + gama b B c - 2) (ya b c) ++ Rw b B c)

section
variable {b : Nat} {B : List Nat} {c : Nat}

theorem length_Lw : (Lw b B c).length = B.length + 1 := by
  simp [Lw, length_DB]

theorem length_Rw : (Rw b B c).length = B.length + 1 := by
  unfold Rw; split <;> simp [length_DRa]

/-- The exact digit word of the template value, for every band length with `2 ≤ l + gam`. -/
theorem digits_ltmpl_unified (h : LHyp b B c) (l : Nat) (hl : 2 ≤ l + gama b B c) :
    digits b (val b (ltmpl B c l)) = dW b B c l := by
  have hg := h.gam_le
  obtain ⟨m, rfl⟩ : ∃ m, l = m + 1 := ⟨l - 1, by omega⟩
  rw [digits_ltmpl h m]
  rcases (by omega : gama b B c = 0 ∨ gama b B c = 1) with h0 | h1
  · obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
    have hm : m' + 1 + 1 + gama b B c - 2 = m' := by omega
    simp only [h0, if_true]
    unfold dW
    rw [hm]
    unfold outW Lw Rw
    simp only [h0, if_true, List.replicate_succ', List.append_assoc, List.singleton_append,
      List.cons_append, List.nil_append]
  · have hm : m + 1 + gama b B c - 2 = m := by omega
    simp only [h1, Nat.one_ne_zero, if_false]
    unfold dW
    rw [hm]
    unfold outW Lw Rw
    simp only [h1, Nat.one_ne_zero, if_false, List.append_assoc, List.singleton_append,
      List.cons_append, List.nil_append]

theorem zipWith_add_reverse_swap' (u w : List Nat) (hl : u.length = w.length) :
    List.zipWith (· + ·) w.reverse u.reverse = (List.zipWith (· + ·) u w).reverse :=
  zipWith_add_reverse_swap u w hl

/-- Mirrored digit sums of a sandwich `L ++ y^m ++ R` form an absorbing template. -/
theorem pairs_sandwich_ltmpl (L R : List Nat) (m y : Nat) (hl : L.length = R.length) :
    pairs (L ++ (List.replicate m y ++ R)) =
      ltmpl (List.zipWith (· + ·) L R.reverse) (y + y) m := by
  have l1 : L.length = R.reverse.length := by simp [hl]
  have l2 : (List.replicate m y).length = (List.replicate m y).length := rfl
  have hsw := zipWith_add_reverse_swap' L R.reverse l1
  rw [List.reverse_reverse] at hsw
  unfold pairs ltmpl
  rw [List.reverse_append, List.reverse_append, List.reverse_replicate, List.append_assoc,
    List.zipWith_append l1, List.zipWith_append l2]
  simp only [List.zipWith_replicate, Nat.min_self]
  rw [hsw]

/-- Exact next coefficient word. -/
theorem pairs_dW (_h : LHyp b B c) (l : Nat) :
    pairs (dW b B c l) =
      ltmpl (nextBa b B c) (cnext b c) (l + gama b B c - 2) := by
  unfold dW
  exact pairs_sandwich_ltmpl (Lw b B c) (Rw b B c) _ (ya b c) (by rw [length_Lw, length_Rw])

/-- One ordinary base-`b` reverse-and-add step maps the template value to the next one. -/
theorem step_ltmpl (h : LHyp b B c) (l : Nat) (hl : 2 ≤ l + gama b B c) :
    step b (val b (ltmpl B c l)) =
      val b (ltmpl (nextBa b B c) (cnext b c) (l + gama b B c - 2)) := by
  rw [step_eq_val_pairs b h.base, digits_ltmpl_unified h l hl, pairs_dW h l]

/-- The template value is not a palindrome as soon as `L ≠ reverse R`. -/
theorem not_isPal_ltmpl (h : LHyp b B c) (l : Nat) (hl : 2 ≤ l + gama b B c)
    (hnp : Lw b B c ≠ (Rw b B c).reverse) : ¬ IsPal b (val b (ltmpl B c l)) := by
  unfold IsPal
  rw [digits_ltmpl_unified h l hl]
  unfold dW
  intro hpal
  rw [List.reverse_append, List.reverse_append, List.reverse_replicate, List.append_assoc]
    at hpal
  have hl' : (Lw b B c).length = (Rw b B c).reverse.length := by
    rw [List.length_reverse, length_Lw, length_Rw]
  exact hnp (List.append_inj hpal hl').1

end

/-- Moving band-valued coefficients from the block into the band. -/
theorem ltmpl_trim (B2 : List Nat) (c u j : Nat) :
    ltmpl (B2 ++ List.replicate u c) c j = ltmpl B2 c (u + j + u) := by
  unfold ltmpl
  rw [← List.replicate_append_replicate, ← List.replicate_append_replicate]
  simp only [List.reverse_append, List.reverse_replicate, List.append_assoc]

end AbsorbingBand

#print axioms AbsorbingBand.digits_ltmpl_unified
#print axioms AbsorbingBand.step_ltmpl
#print axioms AbsorbingBand.not_isPal_ltmpl
#print axioms AbsorbingBand.ltmpl_trim
