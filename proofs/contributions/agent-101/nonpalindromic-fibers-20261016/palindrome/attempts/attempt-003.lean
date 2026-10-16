import Agent101NumericFibers

/-!
Initial palindromes in complete decimal digit-profile fibers. These results
use the actual natural-number reversal and permit arbitrary profiles; an
unrealizable profile contributes no source integer.
-/

namespace Agent101

open DecimalDigits

/-- Actual palindromicity is reflection symmetry of a canonical digit list. -/
theorem palindrome_natValue_iff_reverse (ds : List Nat) (hd : canonicalDigits ds) :
    Lychrel196.Palindrome (natValue ds) ↔ ds.reverse = ds := by
  have hc := (canonicalDigits_iff ds).mp hd
  change Lychrel196.Palindrome (value (digitFn ds) ds.length) ↔ _
  rw [palindrome_value_iff _ _ hc.2.1 (Or.inr hc.2.2.1)]
  constructor
  · intro h
    apply List.ext_getElem (by simp)
    intro i hi hj
    have hk : ds.length - 1 - i < ds.length := by omega
    have hs := h i hj
    rw [digitFn_getElem ds i hj, digitFn_getElem ds _ hk] at hs
    simpa only [List.getElem_reverse] using hs.symm
  · intro h i hi
    exact digitFn_symmetric_of_reverse ds h i hi

/-- A symmetric original digit list has twice each digit as its column sum. -/
theorem digitPairSums_of_reverse_eq (ds : List Nat) (hs : ds.reverse = ds) :
    digitPairSums ds = ds.map (fun d => d + d) := by
  unfold digitPairSums
  rw [hs]
  clear hs
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    simp only [List.zipWith_cons_cons, List.map_cons, ih]
    rfl

theorem even_digitPairSums_of_reverse_eq (ds : List Nat) (hs : ds.reverse = ds) :
    ∀ s ∈ digitPairSums ds, s % 2 = 0 := by
  rw [digitPairSums_of_reverse_eq ds hs]
  intro s hm
  obtain ⟨d, _, rfl⟩ := List.mem_map.mp hm
  omega

/-- Halving the prescribed sums recovers every digit of a palindromic source. -/
theorem half_digitPairSums_of_reverse_eq (ds : List Nat) (hs : ds.reverse = ds) :
    (digitPairSums ds).map (fun s => s / 2) = ds := by
  rw [digitPairSums_of_reverse_eq ds hs, List.map_map]
  clear hs
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    simp only [List.map_cons, ih, Function.comp_apply]
    congr 1
    omega

end Agent101
