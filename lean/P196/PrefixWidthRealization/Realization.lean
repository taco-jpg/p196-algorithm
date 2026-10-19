import P196.PrefixEdgeRealization.Realization

/-!
# Exact prefix realization at a prescribed source width

An observed coefficient prefix can overlap its reflected copy. The overlap
must agree, an observed center must be even, and a boundary lying within
the observed prefix has its computed carry fixed. These finite conditions
are sufficient: the existing mirror constructor fills any unobserved
middle with 0 or 18, and the existing realization and projection theorems
produce one ordinary integer step at exactly the requested source width.
-/

set_option autoImplicit false

namespace PrefixWidthRealization

open DecimalDigits FoldedDecimal SevenColumnProjection

/-- Explicit overlap, center, and inner-carry conditions. Source bounds,
positive head, nonempty prefix, and the width bound are separate premises
of the numeric realization theorem. -/
def Fits (s : List Nat) (L b : Nat) : Prop :=
  (∀ i, i < s.length → L - 1 - i < s.length →
    s.getD i 0 = s.getD (L - 1 - i) 0) ∧
  (∀ i, i < s.length → 2 * i + 1 = L →
    s.getD i 0 % 2 = 0) ∧
  (L ≤ 2 * s.length →
    carry (fun i => s.getD i 0) (L - s.length) = b)

private theorem prefix_entries_iff (q : Nat → Nat) (s : List Nat) :
    wordPrefix q s.length = s ↔
      ∀ i, i < s.length → q i = s.getD i 0 := by
  rw [wordPrefix_eq_range_map]
  constructor
  · intro h i hi
    have he := congrArg (fun xs : List Nat => xs.getD i 0) h
    simpa only [List.getD_eq_getElem?_getD, List.getElem?_map,
      List.getElem?_range hi, Option.map_some', Option.getD_some] using he
  · intro h
    apply List.ext_getElem
    · simp
    · intro i hleft hright
      simpa [hright] using h i hright

private def completion (s : List Nat) (L b : Nat) : Nat → Nat :=
  Agent107.FoldedTransducer.symmetrize L
    (fun i => if i < s.length then s.getD i 0 else 18 * b)

private theorem completion_entry (s : List Nat) (L b : Nat)
    (hfit : Fits s L b) (i : Nat) (hi : i < s.length) :
    completion s L b i = s.getD i 0 := by
  unfold completion Agent107.FoldedTransducer.symmetrize
  by_cases hlow : i ≤ L - 1 - i
  · simp only [hlow, if_true, hi]
  · have href : L - 1 - i < s.length := by omega
    simp only [hlow, if_false, href, if_true]
    exact (hfit.1 i hi href).symm

private theorem completion_admissible (s : List Nat) (L b : Nat)
    (hk : 0 < s.length) (hwidth : s.length ≤ L)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0)
    (hb : b ≤ 1) (hfit : Fits s L b) :
    Admissible L (completion s L b) := by
  have hhead : s.getD 0 0 = s.headD 0 := by cases s <;> rfl
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · rw [completion_entry s L b hfit 0 hk, hhead]
    exact hpos
  · intro i hi
    unfold completion
    rw [Agent107.FoldedTransducer.symmetrize_eq_min]
    let j := min i (L - 1 - i)
    change (if j < s.length then s.getD j 0 else 18 * b) ≤ 18
    by_cases hj : j < s.length
    · rw [if_pos hj]
      have hvalue : s[j] < 19 := hs s[j] (List.getElem_mem hj)
      have hget : s.getD j 0 = s[j] := by simp [hj]
      rw [hget]
      omega
    · rw [if_neg hj]
      omega
  · exact Agent107.FoldedTransducer.symmetrize_symmetric _ _
  · intro i hi he
    unfold completion
    rw [Agent107.FoldedTransducer.symmetrize_eq_min]
    have hmin : min i (L - 1 - i) = i := by omega
    rw [hmin]
    by_cases hik : i < s.length
    · rw [if_pos hik]
      exact hfit.2.1 i hik (by omega)
    · rw [if_neg hik]
      omega

private theorem completion_carry (s : List Nat) (L b : Nat)
    (hk : 0 < s.length) (hwidth : s.length ≤ L)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0)
    (hb : b ≤ 1) (hfit : Fits s L b) :
    carry (completion s L b) (L - s.length) = b := by
  by_cases hshort : L ≤ 2 * s.length
  · exact (carry_congr_upto (completion s L b) (fun i => s.getD i 0)
      s.length (completion_entry s L b hfit) (L - s.length) (by omega)).trans
        (hfit.2.2 hshort)
  · have ha := completion_admissible s L b hk hwidth hs hpos hb hfit
    have hc := carry_bounded (completion s L b) L ha.2.2.1
      (L - s.length - 1) (by omega)
    have hmiddle : completion s L b (L - s.length - 1) = 18 * b := by
      unfold completion
      rw [Agent107.FoldedTransducer.symmetrize_eq_min]
      have hmin : min (L - s.length - 1)
          (L - 1 - (L - s.length - 1)) = s.length := by omega
      rw [hmin]
      simp
    have hindex : L - s.length = (L - s.length - 1) + 1 := by omega
    rw [hindex, carry, hmiddle]
    omega

private theorem fits_of_admissible_prefix (q : Nat → Nat) (s : List Nat)
    (L b : Nat) (ha : Admissible L q) (hwidth : s.length ≤ L)
    (hp : wordPrefix q s.length = s) (hc : carry q (L - s.length) = b) :
    Fits s L b := by
  have he := (prefix_entries_iff q s).mp hp
  refine ⟨?_, ?_, ?_⟩
  · intro i hi href
    rw [← he i hi, ← he (L - 1 - i) href]
    exact ha.2.2.2.1 i (by omega)
  · intro i hi hcenter
    rw [← he i hi]
    exact ha.2.2.2.2 i (by omega) (by omega)
  · intro hshort
    exact (carry_congr_upto q (fun i => s.getD i 0) s.length he
      (L - s.length) (by omega)).symm.trans hc

/-- Exact realization at every prescribed width, including overlapping
reflected prefixes. The actual high inner carry and both canonical digit
representations are retained. All observed positions lie within their
respective canonical widths. -/
theorem fits_iff_realizable (s : List Nat) (L b : Nat)
    (hk : 0 < s.length) (hwidth : s.length ≤ L)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0)
    (hb : b ≤ 1) :
    Fits s L b ↔
      ∃ (n : Nat) (d d' : Nat → Nat),
        let q := columnSum d L
        let W := nextWidth q L
        0 < n ∧ Canonical n d L ∧
        wordPrefix q s.length = s ∧
        carry q (L - s.length) = b ∧
        Canonical (Lychrel196.step n) d' W ∧
        wordPrefix (columnSum d' W) s.length = forwardPrefix s b := by
  constructor
  · intro hfit
    let Q := completion s L b
    have ha : Admissible L Q :=
      completion_admissible s L b hk hwidth hs hpos hb hfit
    obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable Q L
      ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
    let q := columnSum d L
    have hpref : wordPrefix q s.length = s := by
      apply (prefix_entries_iff q s).mpr
      intro i hi
      exact (hrep i (by omega)).trans (completion_entry s L b hfit i hi)
    have hbit : carry q (L - s.length) = b :=
      (carry_congr_upto q Q L hrep (L - s.length) (by omega)).trans
        (completion_carry s L b hk hwidth hs hpos hb hfit)
    obtain ⟨d', hnext, hnextrep⟩ :=
      representation_next n d q L hcan (fun _ _ => rfl)
    have hqa : Admissible L q :=
      NormalizationBridge.canonical_admissible n d L hcan
    have hkW : s.length ≤ nextWidth q L := by
      unfold nextWidth
      split <;> omega
    have hf := actual_forwardPrefix q L s.length hqa hwidth
    rw [hpref, hbit] at hf
    have hnextprefix : wordPrefix (columnSum d' (nextWidth q L)) s.length =
        wordPrefix (nextColumns q L) s.length := by
      rw [wordPrefix_eq_range_map, wordPrefix_eq_range_map]
      exact List.map_congr_left
        (fun i hi => hnextrep i (by have := List.mem_range.mp hi; omega))
    exact ⟨n, d, d', hn, hcan, hpref, hbit, hnext, hnextprefix.trans hf.symm⟩
  · rintro ⟨n, d, d', hn, hcan, hpref, hbit, hnext, hout⟩
    exact fits_of_admissible_prefix (columnSum d L) s L b
      (NormalizationBridge.canonical_admissible n d L hcan) hwidth hpref hbit

#print axioms fits_iff_realizable

end PrefixWidthRealization
