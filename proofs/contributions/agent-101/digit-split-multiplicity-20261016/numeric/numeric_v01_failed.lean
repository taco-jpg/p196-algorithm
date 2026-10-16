import Lychrel196Research
import Agent101SplitEnumeration

/-!
Agent #101: transport finite canonical digit-list enumeration to ordinary
positive natural numbers under the unchanged decimal reverse-and-add map.
All list digits are least-significant first. Infinite tails of digit
functions are never counted.
-/

namespace Agent101

open DecimalDigits

/-- Finite least-significant-first digits, extended by zero outside the list. -/
def digitFn (ds : List Nat) (i : Nat) : Nat := ds[i]?.getD 0

/-- Decimal numerical evaluation of a finite digit list. -/
def natValue (ds : List Nat) : Nat := value (digitFn ds) ds.length

theorem digitFn_getElem (ds : List Nat) (i : Nat) (hi : i < ds.length) :
    digitFn ds i = ds[i] := by
  simp [digitFn, List.getElem?_eq_getElem hi]

theorem digitFn_last (ds : List Nat) :
    digitFn ds (ds.length - 1) = ds.getLastD 0 := by
  simp [digitFn, List.getLastD_eq_getLast?, List.getLast?_eq_getElem?]

theorem bounded_digitFn_iff (ds : List Nat) :
    (∀ i, i < ds.length → digitFn ds i ≤ 9) ↔ digitsBounded ds := by
  constructor
  · intro h d hd
    obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp hd
    simpa [digitFn_getElem ds i hi] using h i hi
  · intro h i hi
    rw [digitFn_getElem ds i hi]
    exact h _ (List.getElem_mem hi)

theorem canonicalDigits_nonempty (ds : List Nat) (hd : canonicalDigits ds) :
    0 < ds.length := by
  cases ds with
  | nil => simpa [canonicalDigits] using hd.2
  | cons a ds => simp

theorem canonicalDigits_iff (ds : List Nat) :
    canonicalDigits ds ↔ Canonical (natValue ds) (digitFn ds) ds.length := by
  constructor
  · intro hd
    exact ⟨canonicalDigits_nonempty ds hd, (bounded_digitFn_iff ds).mpr hd.1,
      by simpa [digitFn_last] using hd.2, rfl⟩
  · intro hd
    exact ⟨(bounded_digitFn_iff ds).mp hd.2.1,
      by simpa [digitFn_last] using hd.2.2.1⟩

theorem natValue_injective_same_length (a b : List Nat)
    (ha : digitsBounded a) (hb : digitsBounded b)
    (hlen : a.length = b.length) (hv : natValue a = natValue b) : a = b := by
  have hb' : ∀ i, i < a.length → digitFn b i ≤ 9 := by
    simpa [hlen] using (bounded_digitFn_iff b).mpr hb
  have hv' : value (digitFn a) a.length = value (digitFn b) a.length := by
    simpa [natValue, hlen] using hv
  have heq := value_injective (digitFn a) (digitFn b) a.length
    ((bounded_digitFn_iff a).mpr ha) hb' hv'
  apply List.ext_getElem hlen
  intro i hi hj
  simpa [digitFn_getElem a i hi, digitFn_getElem b i hj] using heq i hi

theorem length_digitPairSums (ds : List Nat) :
    (digitPairSums ds).length = ds.length := by
  simp [digitPairSums]

theorem digitFn_digitPairSums (ds : List Nat) (i : Nat) (hi : i < ds.length) :
    digitFn (digitPairSums ds) i = columnSum (digitFn ds) ds.length i := by
  have hj : ds.length - 1 - i < ds.length := by omega
  simp only [digitFn, digitPairSums, List.getElem?_zipWith,
    List.getElem?_reverse hi, List.getElem?_eq_getElem hi,
    List.getElem?_eq_getElem hj, Option.getD_some, columnSum, reflected]

theorem canonical_list_exists (n : Nat) (hn : 0 < n) :
    ∃ ds, canonicalDigits ds ∧ natValue ds = n := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  let ds := List.ofFn (fun i : Fin L => d i)
  have hlen : ds.length = L := List.length_ofFn
  have heq : ∀ i, i < L → digitFn ds i = d i := by
    intro i hi
    simp [digitFn, ds, List.getElem?_ofFn, hi]
  have hv : natValue ds = n := by
    unfold natValue
    rw [hlen, value_congr (digitFn ds) d L heq]
    exact hc.2.2.2
  refine ⟨ds, (canonicalDigits_iff ds).mpr ?_, hv⟩
  rw [hv, hlen]
  refine ⟨hc.1, ?_, ?_, ?_⟩
  · intro i hi
    rw [heq i hi]
    exact hc.2.1 i hi
  · rw [heq (L - 1) (by omega)]
    exact hc.2.2.1
  · rw [value_congr (digitFn ds) d L heq]
    exact hc.2.2.2

theorem step_natValue (ds : List Nat) (hd : canonicalDigits ds) :
    Lychrel196.step (natValue ds) = natValue (digitPairSums ds) := by
  unfold natValue
  rw [length_digitPairSums]
  apply FoldedDecimal.step_eq_word_value _ _ _ _ ((canonicalDigits_iff ds).mp hd)
  intro i hi
  exact (digitFn_digitPairSums ds i hi).symm

theorem same_width_step_eq_iff_digitPairSums (a b : List Nat)
    (ha : canonicalDigits a) (hb : canonicalDigits b)
    (hlen : a.length = b.length) :
    Lychrel196.step (natValue a) = Lychrel196.step (natValue b) ↔
      digitPairSums a = digitPairSums b := by
  have hb' : Canonical (natValue b) (digitFn b) a.length := by
    simpa [hlen] using (canonicalDigits_iff b).mp hb
  rw [ReverseAddInverse.same_width_step_eq_iff_pair_sums _ _ _ _ _
    ((canonicalDigits_iff a).mp ha) hb']
  constructor
  · intro heq
    apply List.ext_getElem (by simpa [length_digitPairSums] using hlen)
    intro i hi hj
    have hi' : i < a.length := by simpa [length_digitPairSums] using hi
    have hj' : i < b.length := by omega
    have h := heq i hi'
    rw [← digitFn_digitPairSums a i hi', hlen,
      ← digitFn_digitPairSums b i hj'] at h
    simpa [digitFn_getElem _ i hi, digitFn_getElem _ i hj] using h
  · intro heq i hi
    rw [← digitFn_digitPairSums a i hi, heq, hlen,
      digitFn_digitPairSums b i (by omega)]

#print axioms digitFn_getElem
#print axioms digitFn_last
#print axioms bounded_digitFn_iff
#print axioms canonicalDigits_nonempty
#print axioms canonicalDigits_iff
#print axioms natValue_injective_same_length
#print axioms length_digitPairSums
#print axioms digitFn_digitPairSums
#print axioms canonical_list_exists
#print axioms step_natValue
#print axioms same_width_step_eq_iff_digitPairSums

end Agent101
