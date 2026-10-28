import P196.LatticeBand.Digits

/-!
# Mirrored digit sums of a lattice digit word

For a digit word `D = L ++ rp Y j ++ R` with `|L| = |R| + d`, `0 ≤ d ≤ |Y|` and `j ≥ 1`, the mirrored
digit sums `pairs D` are

  `H ++ band (gen Y d) (|Y|·j - d) ++ reverse H`,

where `H` (of length `|L|`) does not depend on `j`.  So a periodic digit word produces again a
periodic coefficient word, with the new period block `gen Y d` (the "lattice update").
-/

namespace LatticeBand

open Agent120.Neutral

theorem pairs_reverse (D : List Nat) : (pairs D).reverse = pairs D := by
  have h := zipWith_add_reverse_swap D D.reverse (by simp)
  rw [List.reverse_reverse] at h
  unfold pairs
  exact h.symm

theorem length_pairs (D : List Nat) : (pairs D).length = D.length := by
  simp [pairs]

theorem getElem?_pairs (D : List Nat) (i : Nat) (hi : i < D.length) :
    (pairs D)[i]? = some (D[i]?.getD 0 + D[D.length - 1 - i]?.getD 0) := by
  unfold pairs
  rw [List.getElem?_zipWith', List.getElem?_reverse hi]
  have h1 : D[i]? = some D[i] := List.getElem?_eq_getElem hi
  have h2 : D[D.length - 1 - i]? = some D[D.length - 1 - i] :=
    List.getElem?_eq_getElem (by omega)
  rw [h1, h2]
  simp

theorem mod_rev_helper (m j a : Nat) (hm : 0 < m) (ha : a < m * j) :
    (m * j - 1 - a) % m = m - 1 - a % m := by
  have hr := Nat.mod_lt a hm
  have hc := Nat.div_add_mod a m
  obtain ⟨k, hk⟩ : ∃ k, j = a / m + 1 + k := by
    have : a / m < j := by
      rw [Nat.div_lt_iff_lt_mul hm]; rw [Nat.mul_comm]; exact ha
    exact ⟨j - (a / m + 1), by omega⟩
  have e : m * j - 1 - a = (m - 1 - a % m) + m * k := by
    rw [hk, Nat.mul_add, Nat.mul_add, Nat.mul_one]
    have : m * (a / m) + a % m = a := hc
    omega
  rw [e, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]

/-- The new period block. -/
def gen (Y : List Nat) (d : Nat) : List Nat :=
  (List.range Y.length).map (fun s => Y[s]?.getD 0 + Y.reverse[(s + d) % Y.length]?.getD 0)

theorem length_gen (Y : List Nat) (d : Nat) : (gen Y d).length = Y.length := by
  simp [gen]

/-- Outer part of the mirrored digit sums (independent of `j`). -/
def Hh (L R Y : List Nat) : List Nat :=
  List.zipWith (· + ·) (L.take R.length) R.reverse ++
    List.zipWith (· + ·) (L.drop R.length) Y.reverse


/-- Value at an index, default `0`. -/
def gv (l : List Nat) (i : Nat) : Nat := l[i]?.getD 0

theorem getElem?_eq_some_gv (l : List Nat) (i : Nat) (h : i < l.length) :
    l[i]? = some (gv l i) := by
  unfold gv; rw [List.getElem?_eq_getElem h]; rfl

theorem gv_append_left (l l' : List Nat) (i : Nat) (h : i < l.length) :
    gv (l ++ l') i = gv l i := by
  unfold gv; rw [List.getElem?_append_left h]

theorem gv_append_right (l l' : List Nat) (i : Nat) (h : l.length ≤ i) :
    gv (l ++ l') i = gv l' (i - l.length) := by
  unfold gv; rw [List.getElem?_append_right h]

theorem gv_rp (Y : List Nat) (hY : Y ≠ []) (q i : Nat) (h : i < Y.length * q) :
    gv (rp Y q) i = gv Y (i % Y.length) := by
  have hm : 0 < Y.length := List.length_pos_iff.mpr hY
  have h1 : i < (rp Y q).length := by rw [length_rp]; exact h
  rw [getElem?_eq_some_gv _ _ h1 |> fun e => show gv (rp Y q) i = (rp Y q)[i] from by
        unfold gv; rw [List.getElem?_eq_getElem h1]; rfl]
  rw [getElem_rp Y hY q i h1]
  unfold gv; rw [List.getElem?_eq_getElem (Nat.mod_lt _ hm)]; rfl

theorem gv_reverse (l : List Nat) (i : Nat) (h : i < l.length) :
    gv l.reverse i = gv l (l.length - 1 - i) := by
  unfold gv; rw [List.getElem?_reverse h]

theorem getElem?_pairs_gv (D : List Nat) (i : Nat) (hi : i < D.length) :
    (pairs D)[i]? = some (gv D i + gv D (D.length - 1 - i)) :=
  getElem?_pairs D i hi


theorem length_Hh (L R Y : List Nat) (hr : R.length ≤ L.length) (hd : L.length - R.length ≤ Y.length) :
    (Hh L R Y).length = L.length := by
  simp only [Hh, List.length_append, List.length_zipWith, List.length_take, List.length_reverse,
    List.length_drop]
  omega

theorem Hh_A (L R Y : List Nat) (i : Nat) (hi : i < R.length) (hr : R.length ≤ L.length) :
    (Hh L R Y)[i]? = some (gv L i + gv R (R.length - 1 - i)) := by
  have hA : i < (List.zipWith (· + ·) (L.take R.length) R.reverse).length := by
    simp only [List.length_zipWith, List.length_take, List.length_reverse]; omega
  unfold Hh
  rw [List.getElem?_append_left hA, List.getElem?_zipWith', List.getElem?_take_of_lt hi,
    List.getElem?_reverse hi, getElem?_eq_some_gv L i (by omega),
    getElem?_eq_some_gv R _ (by omega)]
  simp

theorem Hh_B (L R Y : List Nat) (i : Nat) (hi1 : R.length ≤ i) (hi2 : i < L.length)
    (hd : L.length - R.length ≤ Y.length) :
    (Hh L R Y)[i]? = some (gv L i + gv Y (Y.length - 1 - (i - R.length))) := by
  have hA : (List.zipWith (· + ·) (L.take R.length) R.reverse).length = R.length := by
    simp only [List.length_zipWith, List.length_take, List.length_reverse]; omega
  unfold Hh
  rw [List.getElem?_append_right (by omega), hA, List.getElem?_zipWith', List.getElem?_drop,
    List.getElem?_reverse (by omega), getElem?_eq_some_gv L _ (by omega),
    getElem?_eq_some_gv Y _ (by omega)]
  have : R.length + (i - R.length) = i := by omega
  rw [this]
  simp

section region
variable (Y L R : List Nat) (j : Nat)

theorem gvD_L (i : Nat) (h : i < L.length) : gv (L ++ (rp Y j ++ R)) i = gv L i :=
  gv_append_left _ _ _ h

theorem gvD_Y (hY : Y ≠ []) (i : Nat) (h1 : L.length ≤ i) (h2 : i < L.length + Y.length * j) :
    gv (L ++ (rp Y j ++ R)) i = gv Y ((i - L.length) % Y.length) := by
  rw [gv_append_right _ _ _ h1, gv_append_left _ _ _ (by rw [length_rp]; omega),
    gv_rp Y hY j _ (by omega)]

theorem gvD_R (i : Nat) (h : L.length + Y.length * j ≤ i) :
    gv (L ++ (rp Y j ++ R)) i = gv R (i - L.length - Y.length * j) := by
  rw [gv_append_right _ _ _ (by omega), gv_append_right _ _ _ (by rw [length_rp]; omega),
    length_rp]

end region


theorem gv_band (W : List Nat) (hW : W ≠ []) (l i : Nat) (h : i < l) :
    gv (band W l) i = gv W (i % W.length) := by
  have hm : 0 < W.length := List.length_pos_iff.mpr hW
  have h1 : i < (band W l).length := by rw [length_band W hW]; exact h
  unfold gv
  rw [List.getElem?_eq_getElem h1, getElem_band W hW l i h1,
    List.getElem?_eq_getElem (Nat.mod_lt _ hm)]

theorem gv_gen (Y : List Nat) (d s : Nat) (hs : s < Y.length) :
    gv (gen Y d) s = gv Y s + gv Y.reverse ((s + d) % Y.length) := by
  unfold gen gv
  rw [List.getElem?_map, List.getElem?_range hs]
  simp

theorem pairs_take_H (Y L R : List Nat) (j d : Nat) (hY : Y ≠ []) (hj : 1 ≤ j)
    (hd : d ≤ Y.length) (hLR : L.length = R.length + d) :
    (pairs (L ++ (rp Y j ++ R))).take L.length = Hh L R Y := by
  have hm : 0 < Y.length := List.length_pos_iff.mpr hY
  have hNj : Y.length ≤ Y.length * j := Nat.le_mul_of_pos_right _ hj
  have hlenD : (L ++ (rp Y j ++ R)).length = L.length + Y.length * j + R.length := by
    simp [length_rp]; omega
  have hH := length_Hh L R Y (by omega) (by omega)
  apply List.ext_getElem?
  intro i
  rw [List.getElem?_take]
  by_cases hi : i < L.length
  · rw [if_pos hi, getElem?_pairs_gv _ _ (by omega)]
    by_cases hir : i < R.length
    · rw [Hh_A L R Y i hir (by omega), gvD_L Y L R j i hi, gvD_R Y L R j _ (by omega)]
      have hk : (L ++ (rp Y j ++ R)).length - 1 - i - L.length - Y.length * j
          = R.length - 1 - i := by omega
      rw [hk]
    · rw [Hh_B L R Y i (by omega) hi (by omega), gvD_L Y L R j i hi,
        gvD_Y Y L R j hY _ (by omega) (by omega)]
      have hk : ((L ++ (rp Y j ++ R)).length - 1 - i - L.length) % Y.length
          = Y.length - 1 - (i - R.length) := by
        have e : (L ++ (rp Y j ++ R)).length - 1 - i - L.length
            = Y.length * j - 1 - (i - R.length) := by omega
        rw [e, mod_rev_helper Y.length j _ hm (by omega),
          Nat.mod_eq_of_lt (by omega : i - R.length < Y.length)]
      rw [hk]
  · rw [if_neg hi, List.getElem?_eq_none (by omega)]

theorem pairs_drop_M (Y L R : List Nat) (j d : Nat) (hY : Y ≠ []) (hj : 1 ≤ j)
    (hLR : L.length = R.length + d) :
    ((pairs (L ++ (rp Y j ++ R))).drop L.length).take (Y.length * j - d) =
      band (gen Y d) (Y.length * j - d) := by
  have hm : 0 < Y.length := List.length_pos_iff.mpr hY
  have hNj : Y.length ≤ Y.length * j := Nat.le_mul_of_pos_right _ hj
  have hlenD : (L ++ (rp Y j ++ R)).length = L.length + Y.length * j + R.length := by
    simp [length_rp]; omega
  have hG : gen Y d ≠ [] := by
    intro h; have := length_gen Y d; rw [h] at this; simp at this; omega
  apply List.ext_getElem?
  intro i
  rw [List.getElem?_take]
  by_cases hi : i < Y.length * j - d
  · rw [if_pos hi, List.getElem?_drop, getElem?_pairs_gv _ _ (by omega),
      getElem?_eq_some_gv (band _ _) i (by rw [length_band _ hG]; exact hi), gv_band _ hG _ _ hi,
      length_gen, gv_gen Y d _ (Nat.mod_lt _ hm), gvD_Y Y L R j hY _ (by omega) (by omega),
      gvD_Y Y L R j hY _ (by omega) (by omega)]
    have e1 : (L.length + i - L.length) % Y.length = i % Y.length := by
      rw [Nat.add_sub_cancel_left]
    have e2 : ((L ++ (rp Y j ++ R)).length - 1 - (L.length + i) - L.length) % Y.length
        = Y.length - 1 - (i + d) % Y.length := by
      have e : (L ++ (rp Y j ++ R)).length - 1 - (L.length + i) - L.length
          = Y.length * j - 1 - (i + d) := by omega
      rw [e, mod_rev_helper Y.length j _ hm (by omega)]
    have e3 : (i % Y.length + d) % Y.length = (i + d) % Y.length := Nat.mod_add_mod _ _ _
    rw [e1, e2, e3, gv_reverse Y _ (Nat.mod_lt _ hm)]
  · rw [if_neg hi]
    symm
    apply List.getElem?_eq_none
    rw [length_band _ hG]; omega


/-- The mirrored digit sums of a periodic digit word: outer part, periodic band, mirrored outer part. -/
theorem pairs_lattice (Y L R : List Nat) (j d : Nat) (hY : Y ≠ []) (hj : 1 ≤ j)
    (hd : d ≤ Y.length) (hLR : L.length = R.length + d) :
    pairs (L ++ (rp Y j ++ R)) =
      Hh L R Y ++ (band (gen Y d) (Y.length * j - d) ++ (Hh L R Y).reverse) := by
  have hm : 0 < Y.length := List.length_pos_iff.mpr hY
  have hNj : Y.length ≤ Y.length * j := Nat.le_mul_of_pos_right _ hj
  have hlenD : (L ++ (rp Y j ++ R)).length = L.length + Y.length * j + R.length := by
    simp [length_rp]; omega
  have hG : gen Y d ≠ [] := by
    intro h; have := length_gen Y d; rw [h] at this; simp at this; omega
  have hH := length_Hh L R Y (by omega) (by omega)
  have hM : (band (gen Y d) (Y.length * j - d)).length = Y.length * j - d :=
    length_band _ hG _
  have h1 := pairs_take_H Y L R j d hY hj hd hLR
  have h2 := pairs_drop_M Y L R j d hY hj hLR
  have hpal := pairs_reverse (L ++ (rp Y j ++ R))
  have hlenP : (pairs (L ++ (rp Y j ++ R))).length = L.length + Y.length * j + R.length := by
    rw [length_pairs, hlenD]
  generalize pairs (L ++ (rp Y j ++ R)) = P at *
  generalize hMdef : band (gen Y d) (Y.length * j - d) = M at *
  generalize hHdef : Hh L R Y = H at *
  have hsplit : P = H ++ (M ++ (P.drop L.length).drop (Y.length * j - d)) := by
    calc P = P.take L.length ++ P.drop L.length := (List.take_append_drop _ _).symm
      _ = H ++ ((P.drop L.length).take (Y.length * j - d) ++
            (P.drop L.length).drop (Y.length * j - d)) := by
          rw [h1, List.take_append_drop]
      _ = H ++ (M ++ (P.drop L.length).drop (Y.length * j - d)) := by rw [h2]
  generalize hE : (P.drop L.length).drop (Y.length * j - d) = E at *
  have hEl : E.length = H.length := by
    have := congrArg List.length hsplit
    simp only [List.length_append] at this
    omega
  have hrev : P.reverse = E.reverse ++ (M.reverse ++ H.reverse) := by
    rw [hsplit]; simp
  have hinj := List.append_inj (hrev.symm.trans hpal |>.trans hsplit)
    (by simp [hEl])
  have hEH : E = H.reverse := by
    have := hinj.1
    rw [← this, List.reverse_reverse]
  rw [hEH] at hsplit
  exact hsplit

end LatticeBand
