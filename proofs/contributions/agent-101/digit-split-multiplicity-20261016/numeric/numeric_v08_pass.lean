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

theorem numeric_length_digitPairSums (ds : List Nat) :
    (digitPairSums ds).length = ds.length := by
  simp [digitPairSums]

theorem digitFn_digitPairSums (ds : List Nat) (i : Nat) (hi : i < ds.length) :
    digitFn (digitPairSums ds) i = columnSum (digitFn ds) ds.length i := by
  have hj : ds.length - 1 - i < ds.length := by omega
  simp only [digitFn, digitPairSums, List.getElem?_zipWith,
    List.getElem?_reverse hi, List.getElem?_eq_getElem hi,
    List.getElem?_eq_getElem hj, Option.getD_some, columnSum, reflected]
  rfl

theorem canonical_list_exists (n : Nat) (hn : 0 < n) :
    ∃ ds, canonicalDigits ds ∧ natValue ds = n := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hL := hc.1
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
  rw [numeric_length_digitPairSums]
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
    apply List.ext_getElem (by simpa [numeric_length_digitPairSums] using hlen)
    intro i hi hj
    have hi' : i < a.length := by simpa [numeric_length_digitPairSums] using hi
    have hj' : i < b.length := by omega
    have h := heq i hi'
    rw [← digitFn_digitPairSums a i hi', hlen,
      ← digitFn_digitPairSums b i hj'] at h
    simpa [digitFn_getElem _ i hi, digitFn_getElem _ i hj] using h
  · intro heq i hi
    rw [← digitFn_digitPairSums a i hi, heq, hlen,
      digitFn_digitPairSums b i (by omega)]

/-- Preserve a specified width when replacing an infinite digit function by
its finite list of relevant digits. No condition is imposed on its tail. -/
theorem canonical_to_list (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    ∃ ds, ds.length = L ∧ canonicalDigits ds ∧ natValue ds = n ∧
      ∀ i, i < L → digitFn ds i = d i := by
  let ds := List.ofFn (fun i : Fin L => d i)
  have hlen : ds.length = L := List.length_ofFn
  have heq : ∀ i, i < L → digitFn ds i = d i := by
    intro i hi
    simp [digitFn, ds, List.getElem?_ofFn, hi]
  have hv : natValue ds = n := by
    unfold natValue
    rw [hlen, value_congr (digitFn ds) d L heq]
    exact hc.2.2.2
  refine ⟨ds, hlen, (canonicalDigits_iff ds).mpr ?_, hv, heq⟩
  rw [hv, hlen]
  refine ⟨hc.1, ?_, ?_, ?_⟩
  · intro i hi
    rw [heq i hi]
    exact hc.2.1 i hi
  · rw [heq (L - 1) (Nat.sub_lt hc.1 (by decide))]
    exact hc.2.2.1
  · rw [value_congr (digitFn ds) d L heq]
    exact hc.2.2.2

theorem natValue_positive (ds : List Nat) (hd : canonicalDigits ds) :
    0 < natValue ds := by
  have hc := (canonicalDigits_iff ds).mp hd
  exact value_positive _ _ hc.1 hc.2.2.1

theorem coefficientWord_reverse (h : List Nat) (c : Option Nat) :
    (coefficientWord h c).reverse = coefficientWord h c := by
  cases c <;> simp [coefficientWord, List.reverse_append, List.append_assoc]

theorem digitFn_symmetric_of_reverse (qs : List Nat) (hs : qs.reverse = qs)
    (i : Nat) (hi : i < qs.length) :
    digitFn qs i = digitFn qs (qs.length - 1 - i) := by
  have heq := List.getElem?_reverse (l := qs) hi
  rw [hs] at heq
  exact congrArg (fun x : Option Nat => x.getD 0) heq

theorem bounded_digitFn (qs : List Nat) (B : Nat)
    (hB : ∀ s ∈ qs, s ≤ B) : ∀ i, i < qs.length → digitFn qs i ≤ B := by
  intro i hi
  rw [digitFn_getElem qs i hi]
  exact hB _ (List.getElem_mem hi)

/-- The symmetric coefficient profile is recoverable from its numeric value,
even when coefficients exceed a single decimal digit and carries occur. -/
theorem step_eq_profile_iff (ds h : List Nat) (c : Option Nat)
    (hd : canonicalDigits ds)
    (hlen : ds.length = (coefficientWord h c).length)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
    Lychrel196.step (natValue ds) = natValue (coefficientWord h c) ↔
      digitPairSums ds = coefficientWord h c := by
  constructor
  · intro hv
    have hc := (canonicalDigits_iff ds).mp hd
    have hstep := FoldedDecimal.step_eq_word_value _ _ _ _ hc (fun _ _ => rfl)
    have heqv : value (columnSum (digitFn ds) ds.length) ds.length =
        value (digitFn (coefficientWord h c)) ds.length := by
      rw [hstep] at hv
      simpa only [natValue, ← hlen] using hv
    have heq := ReverseAddInverse.symmetric_value_injective
      (columnSum (digitFn ds) ds.length) (digitFn (coefficientWord h c)) ds.length
      (columnSum_bounded _ _ hc.2.1)
      (by simpa [hlen] using bounded_digitFn _ 18 hq)
      (columnSum_symmetric _ _)
      (by simpa [hlen] using digitFn_symmetric_of_reverse _ (coefficientWord_reverse h c))
      heqv
    apply List.ext_getElem (by simpa [numeric_length_digitPairSums] using hlen)
    intro i hi hj
    have hi' : i < ds.length := by simpa [numeric_length_digitPairSums] using hi
    have hx := heq i hi'
    rw [← digitFn_digitPairSums ds i hi'] at hx
    simpa [digitFn_getElem _ i hi, digitFn_getElem _ i hj] using hx
  · intro hp
    rw [step_natValue ds hd, hp]

/-- Ordinary positive integers with exactly `L` decimal digits. -/
def decimalWidth (n L : Nat) : Prop :=
  0 < L ∧ 10 ^ (L - 1) ≤ n ∧ n < 10 ^ L

theorem bounded_value_lt_pow (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9) : value d L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have ht := ih (fun i hi => hd i (by omega))
    have hm := Nat.mul_le_mul_right (10 ^ L) (hd L (by omega))
    simp only [value, Nat.pow_succ]
    omega

theorem canonical_decimalWidth (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) : decimalWidth n L := by
  refine ⟨hc.1, ?_, ?_⟩
  · obtain ⟨K, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hc.1)
    have hlead : 1 ≤ d K := by simpa using hc.2.2.1
    have hm := Nat.mul_le_mul_right (10 ^ K) hlead
    have hv := hc.2.2.2
    simp only [value, Nat.succ_sub_one, Nat.one_mul] at hm hv ⊢
    omega
  · rw [← hc.2.2.2]
    exact bounded_value_lt_pow d L hc.2.1

theorem decimalWidth_unique (n L K : Nat)
    (hL : decimalWidth n L) (hK : decimalWidth n K) : L = K := by
  have hLl := hL.2.1
  have hLu := hL.2.2
  have hKl := hK.2.1
  have hKu := hK.2.2
  by_cases heq : L = K
  · exact heq
  have hne := heq
  rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
  · have hh := Nat.pow_le_pow_right (by decide : 0 < 10)
      (show L ≤ K - 1 by omega)
    omega
  · have hh := Nat.pow_le_pow_right (by decide : 0 < 10)
      (show K ≤ L - 1 by omega)
    omega

theorem decimalWidth_iff_canonical (n L : Nat) :
    decimalWidth n L ↔ ∃ d, Canonical n d L := by
  constructor
  · intro hw
    have hp : 0 < n := Nat.lt_of_lt_of_le (Nat.pow_pos (by decide)) hw.2.1
    obtain ⟨d, K, hc⟩ := canonical_exists n hp
    have heq := decimalWidth_unique n L K hw (canonical_decimalWidth n d K hc)
    exact ⟨d, heq.symm ▸ hc⟩
  · rintro ⟨d, hc⟩
    exact canonical_decimalWidth n d L hc

theorem coefficientWord_bounded (h : List Nat) (c : Option Nat)
    (hh : ∀ s ∈ h, s ≤ 18) (hc : ∀ s ∈ c.toList, s ≤ 18) :
    ∀ s ∈ coefficientWord h c, s ≤ 18 := by
  intro s hs
  simp only [coefficientWord, List.mem_append, List.mem_reverse] at hs
  rcases hs with (hs | hs) | hs
  · exact hh s hs
  · exact hc s hs
  · exact hh s hs

/-- Canonical finite decimal lists have distinct numeric values, without
having to assume their lengths agree beforehand. -/
theorem natValue_injective_canonical (a b : List Nat)
    (ha : canonicalDigits a) (hb : canonicalDigits b)
    (hv : natValue a = natValue b) : a = b := by
  have hwa := canonical_decimalWidth _ _ _ ((canonicalDigits_iff a).mp ha)
  have hwb := canonical_decimalWidth _ _ _ ((canonicalDigits_iff b).mp hb)
  rw [← hv] at hwb
  exact natValue_injective_same_length a b ha.1 hb.1
    (decimalWidth_unique _ _ _ hwa hwb) hv

theorem nodup_map_natValue (words : List (List Nat))
    (hc : ∀ ds ∈ words, canonicalDigits ds) (hn : words.Nodup) :
    (words.map natValue).Nodup := by
  rw [List.Nodup, List.pairwise_map]
  apply List.Pairwise.imp_of_mem (p := hn)
  intro a b ha hb hne heq
  exact hne (natValue_injective_canonical a b (hc a ha) (hc b hb) heq)

/-- Complete finite list of ordinary natural-number predecessors at this
profile's width. Its elements are numbers, not digit functions. -/
def numericFiber (h : List Nat) (c : Option Nat) : List Nat :=
  (canonicalWords h c).map natValue

theorem mem_numericFiber_digits (h : List Nat) (c : Option Nat) (n : Nat) :
    n ∈ numericFiber h c ↔ ∃ ds, canonicalDigits ds ∧
      digitPairSums ds = coefficientWord h c ∧ natValue ds = n := by
  simp only [numericFiber, List.mem_map, mem_canonicalWords]
  constructor
  · rintro ⟨ds, ⟨hc, hp⟩, hv⟩
    exact ⟨ds, hc, hp, hv⟩
  · rintro ⟨ds, hc, hp, hv⟩
    exact ⟨ds, ⟨hc, hp⟩, hv⟩

theorem mem_numericFiber_canonical (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
    n ∈ numericFiber h c ↔
      (∃ d, Canonical n d (coefficientWord h c).length) ∧
      Lychrel196.step n = natValue (coefficientWord h c) := by
  rw [mem_numericFiber_digits]
  constructor
  · rintro ⟨ds, hc, hp, hv⟩
    have hlen : ds.length = (coefficientWord h c).length := by
      rw [← hp, numeric_length_digitPairSums]
    refine ⟨⟨digitFn ds, ?_⟩, ?_⟩
    · simpa [← hlen, ← hv] using (canonicalDigits_iff ds).mp hc
    · rw [← hv, step_natValue ds hc, hp]
  · rintro ⟨⟨d, hc⟩, hs⟩
    obtain ⟨ds, hlen, hd, hv, _⟩ := canonical_to_list n d _ hc
    refine ⟨ds, hd, ?_, hv⟩
    apply (step_eq_profile_iff ds h c hd hlen hq).mp
    simpa [hv] using hs

/-- Exact ordinary-integer inverse fiber at the prescribed decimal width.
The right side contains no digit-function or digit-list witness. It also
covers inadmissible profiles, whose complete inverse fiber is empty. -/
theorem mem_numericFiber (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
    n ∈ numericFiber h c ↔
      decimalWidth n (coefficientWord h c).length ∧
      Lychrel196.step n = natValue (coefficientWord h c) := by
  rw [mem_numericFiber_canonical h c n hq, decimalWidth_iff_canonical]

theorem numericFiber_nodup (h : List Nat) (c : Option Nat) :
    (numericFiber h c).Nodup := by
  apply nodup_map_natValue
  · intro ds hd
    exact ((mem_canonicalWords h c ds).mp hd).1
  · exact canonicalWords_nodup h c

theorem length_numericFiber (h : List Nat) (c : Option Nat) :
    (numericFiber h c).length = profileCount h c := by
  simp only [numericFiber, List.length_map, length_canonicalWords]

theorem length_numericFiber_cons (s : Nat) (h : List Nat) (c : Option Nat) :
    (numericFiber (s :: h) c).length =
      pairCount true s * centerCount c * natProduct (h.map (pairCount false)) := by
  rw [length_numericFiber]
  rfl

theorem length_numericFiber_cons_le (s : Nat) (h : List Nat) (c : Option Nat) :
    (numericFiber (s :: h) c).length ≤ 9 * 10 ^ h.length := by
  rw [length_numericFiber]
  exact profileCount_cons_le s h c

#print axioms digitFn_getElem
#print axioms digitFn_last
#print axioms bounded_digitFn_iff
#print axioms canonicalDigits_nonempty
#print axioms canonicalDigits_iff
#print axioms natValue_injective_same_length
#print axioms numeric_length_digitPairSums
#print axioms digitFn_digitPairSums
#print axioms canonical_list_exists
#print axioms step_natValue
#print axioms same_width_step_eq_iff_digitPairSums
#print axioms canonical_to_list
#print axioms natValue_positive
#print axioms coefficientWord_reverse
#print axioms digitFn_symmetric_of_reverse
#print axioms bounded_digitFn
#print axioms step_eq_profile_iff
#print axioms bounded_value_lt_pow
#print axioms canonical_decimalWidth
#print axioms decimalWidth_unique
#print axioms decimalWidth_iff_canonical
#print axioms coefficientWord_bounded
#print axioms natValue_injective_canonical
#print axioms nodup_map_natValue
#print axioms digitFn
#print axioms natValue
#print axioms decimalWidth
#print axioms numericFiber
#print axioms mem_numericFiber_digits
#print axioms mem_numericFiber_canonical
#print axioms mem_numericFiber
#print axioms numericFiber_nodup
#print axioms length_numericFiber
#print axioms length_numericFiber_cons
#print axioms length_numericFiber_cons_le

end Agent101
