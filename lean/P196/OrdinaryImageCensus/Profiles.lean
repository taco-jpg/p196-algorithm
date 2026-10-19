import P196.SymmetricCarryCensus.Counts
import P196.Agent101DigitSplit.Agent101NumericFibers
import P196.Drafts.Misc.Agent221FiniteSeedBridge

/-!
# Numerical values of coefficient words with a fixed terminal carry

The original admissible coefficient enumeration gives every ordinary source
profile. At a fixed source width, numerical evaluation is injective even when
the coefficients require carries. Filtering by the terminal carry therefore
counts distinct ordinary outputs and partitions the original profile count.
-/

set_option autoImplicit false

namespace OrdinaryImageCensus

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent124.PrefixK SevenColumn.ShortBoundary SymmetricCarryCensus

/-- Distinct ordinary output values from width-L source profiles whose
terminal carry is c. -/
def carryValues (L c : Nat) : List Nat :=
  ((symWords L).filter (fun w => carry (wordFun w) L == c)).map natValue

private theorem symWords_value_injective {L : Nat} {a b : List Nat}
    (ha : a ∈ symWords L) (hb : b ∈ symWords L)
    (hv : natValue a = natValue b) : a = b := by
  obtain ⟨hla, hqa⟩ := (mem_symWords_iff L a).mp ha
  obtain ⟨hlb, hqb⟩ := (mem_symWords_iff L b).mp hb
  have hvalue : value (wordFun a) L = value (wordFun b) L := by
    change value (wordFun a) a.length = value (wordFun b) b.length at hv
    simpa only [hla, hlb] using hv
  have hcols := ReverseAddInverse.symmetric_value_injective
    (wordFun a) (wordFun b) L hqa.2.2.1 hqb.2.2.1
    hqa.2.2.2.1 hqb.2.2.2.1 hvalue
  calc
    a = wordOf (wordFun a) L := by
      rw [← hla]
      exact (wordOf_wordFun a).symm
    _ = wordOf (wordFun b) L := wordOf_congr _ _ L hcols
    _ = b := by
      rw [← hlb]
      exact wordOf_wordFun b

/-- Different admissible profiles of one source width have different values. -/
theorem carryValues_nodup (L c : Nat) : (carryValues L c).Nodup := by
  unfold carryValues
  apply nodup_map_of_injOn _ _ (List.Pairwise.filter _ (symWords_nodup L))
  intro a ha b hb hv
  exact symWords_value_injective
    (List.mem_filter.mp ha).1 (List.mem_filter.mp hb).1 hv

/-- Membership is exactly ordinary reverse-and-add at the specified source
width and terminal carry. -/
theorem mem_carryValues (L c Y : Nat) :
    Y ∈ carryValues L c ↔
      ∃ n d, Canonical n d L ∧ step n = Y ∧
        carry (columnSum d L) L = c := by
  unfold carryValues
  constructor
  · intro hY
    obtain ⟨w, hw, hvalue⟩ := List.mem_map.mp hY
    obtain ⟨hw, hc⟩ := List.mem_filter.mp hw
    have hcarry : carry (wordFun w) L = c := by
      simpa only [beq_iff_eq] using hc
    obtain ⟨hlen, ha⟩ := (mem_symWords_iff L w).mp hw
    obtain ⟨n, d, _, hn, hrep, hstep⟩ :=
      Agent221FiniteSeedBridge.realizable_step_value (wordFun w) L
        ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
    refine ⟨n, d, hn, ?_, ?_⟩
    · calc
        step n = value (wordFun w) L := hstep
        _ = natValue w := by rw [← hlen]; rfl
        _ = Y := hvalue
    · exact (carry_congr_upto (columnSum d L) (wordFun w) L hrep L
        (Nat.le_refl L)).trans hcarry
  · rintro ⟨n, d, hn, hstep, hcarry⟩
    let q := columnSum d L
    have ha : Admissible L q :=
      NormalizationBridge.canonical_admissible n d L hn
    have hrep : ∀ i, i < L → wordFun (wordOf q L) i = q i :=
      wordOf_get q L
    refine List.mem_map.mpr ⟨wordOf q L,
      List.mem_filter.mpr ⟨wordOf_mem_symWords q L ha, ?_⟩, ?_⟩
    · have hc : carry (wordFun (wordOf q L)) L = c :=
        (carry_congr_upto (wordFun (wordOf q L)) q L hrep L
          (Nat.le_refl L)).trans hcarry
      simpa only [beq_iff_eq] using hc
    · calc
        natValue (wordOf q L) = value q L := by
          unfold natValue
          rw [wordOf_length]
          exact value_congr _ _ L hrep
        _ = step n := (step_eq_word_value n d q L hn (fun _ _ => rfl)).symm
        _ = Y := hstep

/-- The numerical list retains exactly the original carry-filtered count. -/
theorem carryValues_length (L c : Nat) :
    (carryValues L c).length =
      (symWords L).countP (fun w => carry (wordFun w) L == c) := by
  simp only [carryValues, List.length_map, List.countP_eq_length_filter]

/-- Terminal carries zero and one partition every admissible source profile. -/
theorem carryValues_partition (L : Nat) :
    (carryValues L 0).length + (carryValues L 1).length = wordCount L := by
  rw [carryValues_length, carryValues_length, ← symWords_length]
  have hsplit := List.length_eq_countP_add_countP
    (fun w : List Nat => carry (wordFun w) L == 0) (l := symWords L)
  have hcomplement :
      (symWords L).countP (fun w => ¬ (carry (wordFun w) L == 0)) =
        (symWords L).countP (fun w => carry (wordFun w) L == 1) := by
    apply List.countP_congr
    intro w hw
    have ha := ((mem_symWords_iff L w).mp hw).2
    have hb := carry_bounded (wordFun w) L ha.2.2.1 L (Nat.le_refl L)
    have hcases : carry (wordFun w) L = 0 ∨ carry (wordFun w) L = 1 := by
      omega
    rcases hcases with hzero | hone
    · simp [hzero]
    · simp [hone]
  rw [hcomplement] at hsplit
  exact hsplit.symm

end OrdinaryImageCensus

#print axioms OrdinaryImageCensus.carryValues
#print axioms OrdinaryImageCensus.carryValues_nodup
#print axioms OrdinaryImageCensus.mem_carryValues
#print axioms OrdinaryImageCensus.carryValues_length
#print axioms OrdinaryImageCensus.carryValues_partition
