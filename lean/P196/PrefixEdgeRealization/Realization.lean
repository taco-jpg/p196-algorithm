import P196.PrefixEdgeRealization.Compatibility
import P196.Agent107FoldedTransducer.Agent107TransducerInput
import P196.Agent104P620Witness.PalindromeBridge

/-!
# Actual integer realizations of individual prefix edges

A prefix of length k is completed to a symmetric word of width 2*k+1.
Its center coefficient is 0 or 18, forcing the selected high inner carry
independently of the low incoming carry. Existing finite-word realization
and actual projection theorems then supply an ordinary integer step.

Each edge has its own witness. This does not provide a common integer
realizing a multi-edge path or cycle, a fixed-seed reachability claim,
or a palindrome-avoidance conclusion.
-/

set_option autoImplicit false

namespace PrefixEdgeRealization

open DecimalDigits FoldedDecimal SevenColumnProjection

private theorem wordPrefix_congr (q r : Nat → Nat) (k : Nat)
    (h : ∀ i, i < k → q i = r i) : wordPrefix q k = wordPrefix r k := by
  rw [wordPrefix_eq_range_map, wordPrefix_eq_range_map]
  exact List.map_congr_left (fun i hi => h i (List.mem_range.mp hi))

private theorem wordPrefix_getD (s : List Nat) :
    wordPrefix (fun i => s.getD i 0) s.length = s := by
  rw [wordPrefix_eq_range_map]
  apply List.ext_getElem
  · simp
  · intro i hleft hright
    simp [hright]

/-- The existing mirror constructor preserves the prefix and adds an even
center. Only its finite width will be used in the realization theorem. -/
private def completion (s : List Nat) (b : Nat) : Nat → Nat :=
  Agent107.FoldedTransducer.symmetrize (2 * s.length + 1)
    (fun i => if i = s.length then 18 * b else s.getD i 0)

private theorem completion_entry (s : List Nat) (b i : Nat)
    (hi : i < s.length) : completion s b i = s.getD i 0 := by
  unfold completion
  rw [Agent107.FoldedTransducer.symmetrize_pair _ _ i (by omega)]
  simp [Nat.ne_of_lt hi]

private theorem completion_center (s : List Nat) (b : Nat) :
    completion s b s.length = 18 * b := by
  have hhalf : (2 * s.length + 1) / 2 = s.length := by omega
  have hc := Agent107.FoldedTransducer.symmetrize_center (2 * s.length + 1)
    (fun i => if i = s.length then 18 * b else s.getD i 0) (by omega)
  rw [hhalf] at hc
  simpa [completion] using hc

private theorem completion_admissible (s : List Nat) (b : Nat)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (hb : b ≤ 1) :
    Admissible (2 * s.length + 1) (completion s b) := by
  have hk : 0 < s.length := by
    cases s with
    | nil => simp at hpos
    | cons a s => simp
  have hhead : s.getD 0 0 = s.headD 0 := by cases s <;> rfl
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · rw [completion_entry s b 0 hk, hhead]
    exact hpos
  · intro i hi
    unfold completion
    rw [Agent107.FoldedTransducer.symmetrize_eq_min]
    let j := min i (2 * s.length + 1 - 1 - i)
    have hj : j ≤ s.length := by dsimp [j]; omega
    change (if j = s.length then 18 * b else s.getD j 0) ≤ 18
    by_cases he : j = s.length
    · rw [if_pos he]
      omega
    · rw [if_neg he]
      have hjlt : j < s.length := by omega
      have hvalue : s[j] < 19 := hs s[j] (List.getElem_mem hjlt)
      have hget : s.getD j 0 = s[j] := by simp [hjlt]
      rw [hget]
      omega
  · exact Agent107.FoldedTransducer.symmetrize_symmetric _ _
  · intro i hi he
    have hic : i = s.length := by omega
    rw [hic, completion_center]
    omega

private theorem completion_prefix (s : List Nat) (b : Nat) :
    wordPrefix (completion s b) s.length = s := by
  exact (wordPrefix_congr _ _ _ (completion_entry s b)).trans (wordPrefix_getD s)

private theorem completion_carry (s : List Nat) (b : Nat)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (hb : b ≤ 1) :
    carry (completion s b) (2 * s.length + 1 - s.length) = b := by
  have ha := completion_admissible s b hs hpos hb
  have hc := carry_bounded (completion s b) (2 * s.length + 1)
    ha.2.2.1 s.length (by omega)
  have hi : 2 * s.length + 1 - s.length = s.length + 1 := by omega
  rw [hi, carry, completion_center]
  omega

/-- Every valid prefix and prescribed carry bit has an actual positive
integer witness with source width exactly twice the prefix length plus one.
Both digit representations are canonical, and the carry is the source's
actual computed high inner carry. -/
theorem forwardPrefix_realizable (s : List Nat) (b : Nat)
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (hb : b ≤ 1) :
    let L := 2 * s.length + 1
    ∃ (n : Nat) (d d' : Nat → Nat),
      let q := columnSum d L
      let W := nextWidth q L
      0 < n ∧ Canonical n d L ∧
      wordPrefix q s.length = s ∧
      carry q (L - s.length) = b ∧
      Canonical (Lychrel196.step n) d' W ∧
      wordPrefix (columnSum d' W) s.length = forwardPrefix s b := by
  let L := 2 * s.length + 1
  let Q := completion s b
  have ha : Admissible L Q := completion_admissible s b hs hpos hb
  obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable Q L
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  let q := columnSum d L
  have hkL : s.length ≤ L := by dsimp [L]; omega
  have hpref : wordPrefix q s.length = s :=
    (wordPrefix_congr q Q s.length (fun i hi => hrep i (by omega))).trans
      (completion_prefix s b)
  have hc : carry q (L - s.length) = b :=
    (carry_congr_upto q Q L hrep (L - s.length) (by omega)).trans
      (completion_carry s b hs hpos hb)
  obtain ⟨d', hnext, hnextrep⟩ :=
    representation_next n d q L hcan (fun _ _ => rfl)
  have hqa : Admissible L q := NormalizationBridge.canonical_admissible n d L hcan
  have hkW : s.length ≤ nextWidth q L := by
    unfold nextWidth
    split <;> omega
  have hf := actual_forwardPrefix q L s.length hqa hkL
  rw [hpref, hc] at hf
  refine ⟨n, d, d', hn, hcan, hpref, hc, hnext, ?_⟩
  exact (wordPrefix_congr _ _ s.length
    (fun i hi => hnextrep i (by omega))).trans hf.symm

/-- The full executable inverse is exactly existential actual one-step
prefix realizability at source width 2*k+1. The nonempty guard excludes the
empty-prefix numeric witness, which is absent from the inverse relation. -/
theorem mem_prefixPredecessors_iff_realizable (s p : List Nat) :
    s ∈ SevenColumn.prefixPredecessors p ↔
      0 < s.length ∧
      (let L := 2 * s.length + 1
       ∃ (n : Nat) (d d' : Nat → Nat),
         let q := columnSum d L
         let W := nextWidth q L
         0 < n ∧ Canonical n d L ∧
         wordPrefix q s.length = s ∧
         Canonical (Lychrel196.step n) d' W ∧
         wordPrefix (columnSum d' W) s.length = p) := by
  constructor
  · intro h
    obtain ⟨hs, hpos, b, hb, hf⟩ :=
      (mem_prefixPredecessors_iff_forwardAdmitted s p).mp h
    have hk : 0 < s.length := by
      cases s with
      | nil => simp at hpos
      | cons a s => simp
    obtain ⟨n, d, d', hn, hcan, hpref, hc, hnext, hout⟩ :=
      forwardPrefix_realizable s b hs hpos hb
    exact ⟨hk, n, d, d', hn, hcan, hpref, hnext, hout.trans hf⟩
  · rintro ⟨hk, n, d, d', hn, hcan, hpref, hnext, hout⟩
    let L := 2 * s.length + 1
    let q := columnSum d L
    let W := nextWidth q L
    have hsource : Canonical n d L := hcan
    have htarget : Canonical (Lychrel196.step n) d' W := hnext
    have ha : Admissible L q :=
      NormalizationBridge.canonical_admissible n d L hsource
    have hkL : s.length ≤ L := by dsimp [L]; omega
    have hkW : s.length ≤ W := by
      dsimp [W, nextWidth]
      split <;> omega
    obtain ⟨e, he, hrep⟩ :=
      representation_next n d q L hsource (fun _ _ => rfl)
    have hdigits : ∀ i, i < W → e i = d' i :=
      (SevenColumnKernel.PalindromeBridge.canonical_unique he htarget).2
    have hcolumns : ∀ i, i < W → columnSum d' W i = nextColumns q L i := by
      intro i hi
      calc
        columnSum d' W i = columnSum e W i := by
          simp only [columnSum, reflected]
          rw [← hdigits i hi, ← hdigits (W - 1 - i) (by omega)]
        _ = nextColumns q L i := hrep i hi
    have hpnext : wordPrefix (nextColumns q L) s.length = p :=
      (wordPrefix_congr _ _ s.length
        (fun i hi => (hcolumns i (by omega)).symm)).trans hout
    have hmem := actual_mem_prefixPredecessors q L s.length ha hk hkL
    rw [hpref, hpnext] at hmem
    exact hmem

#print axioms forwardPrefix_realizable
#print axioms mem_prefixPredecessors_iff_realizable

end PrefixEdgeRealization
