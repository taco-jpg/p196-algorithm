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

theorem digitFn_half_map (qs : List Nat) (i : Nat) (hi : i < qs.length) :
    digitFn (qs.map (fun s => s / 2)) i = digitFn qs i / 2 := by
  rw [digitFn_getElem _ _ (by simpa using hi), List.getElem_map,
    digitFn_getElem qs i hi]

theorem digitPairSums_bounded (ds : List Nat) (hd : digitsBounded ds) :
    ∀ s ∈ digitPairSums ds, s ≤ 18 := by
  intro s hs
  obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp hs
  have hi' : i < ds.length := by simpa only [length_digitPairSums] using hi
  have hj : ds.length - 1 - i < ds.length := by omega
  have hb := bounded_digitFn ds 9 hd
  have h1 := hb i hi'
  have h2 := hb (ds.length - 1 - i) hj
  have heq := digitFn_digitPairSums ds i hi'
  rw [digitFn_getElem _ _ hi] at heq
  simp only [columnSum, reflected] at heq
  omega

/-- Averaging mirrored digits preserves a positive high digit when all sums
are even. The original digits need not themselves form a palindrome. -/
theorem canonical_half_pairSums (ds : List Nat) (hd : canonicalDigits ds)
    (he : ∀ s ∈ digitPairSums ds, s % 2 = 0) :
    canonicalDigits ((digitPairSums ds).map (fun s => s / 2)) := by
  constructor
  · intro d hm
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hm
    have hb := digitPairSums_bounded ds hd.1 s hs
    omega
  · have hL := canonicalDigits_nonempty ds hd
    have hi : ds.length - 1 < ds.length := by omega
    have hiq : ds.length - 1 < (digitPairSums ds).length := by
      simpa only [length_digitPairSums] using hi
    have heven : digitFn (digitPairSums ds) (ds.length - 1) % 2 = 0 := by
      apply he
      rw [digitFn_getElem _ _ hiq]
      exact List.getElem_mem hiq
    have hlast : digitFn (digitPairSums ds) (ds.length - 1) =
        ds.getLastD 0 + digitFn ds 0 := by
      rw [digitFn_digitPairSums ds _ hi]
      simp only [columnSum, reflected, Nat.sub_self, digitFn_last]
    rw [← digitFn_last]
    simp only [List.length_map, length_digitPairSums]
    rw [digitFn_half_map _ _ hiq]
    have hp := hd.2
    omega

theorem digitPairSums_half_of_reverse_even (qs : List Nat)
    (hr : qs.reverse = qs) (he : ∀ s ∈ qs, s % 2 = 0) :
    digitPairSums (qs.map (fun s => s / 2)) = qs := by
  have hrev : (qs.map (fun s => s / 2)).reverse = qs.map (fun s => s / 2) := by
    simpa only [List.map_reverse] using
      congrArg (fun xs : List Nat => xs.map (fun s => s / 2)) hr
  rw [digitPairSums_of_reverse_eq _ hrev, List.map_map]
  clear hr hrev
  induction qs with
  | nil => rfl
  | cons s qs ih =>
    have hs := he s (by simp)
    have ht : ∀ t ∈ qs, t % 2 = 0 := fun t ht => he t (by simp [ht])
    simp only [List.map_cons, Function.comp_apply, ih ht]
    congr 1
    omega

/-- Positive exact multiplicity supplies an original realization, which
certifies that the halved even profile is a canonical decimal digit list. -/
theorem canonical_half_coefficientWord (h : List Nat) (c : Option Nat)
    (hp : 0 < profileCount h c)
    (he : ∀ s ∈ coefficientWord h c, s % 2 = 0) :
    canonicalDigits ((coefficientWord h c).map (fun s => s / 2)) := by
  have hpos : 0 < (canonicalWords h c).length := by
    rw [length_canonicalWords]
    exact hp
  cases hw : canonicalWords h c with
  | nil => simp [hw] at hpos
  | cons ds words =>
    have hm : ds ∈ canonicalWords h c := by simp [hw]
    have hc := (mem_canonicalWords h c ds).mp hm
    rw [← hc.2] at he ⊢
    exact canonical_half_pairSums ds hc.1 he

/-- The explicit halved profile is an actual palindromic member whenever
the profile has a realization and every coefficient is even. -/
theorem half_coefficientWord_mem_numericFiber (h : List Nat) (c : Option Nat)
    (hp : 0 < profileCount h c)
    (he : ∀ s ∈ coefficientWord h c, s % 2 = 0) :
    natValue ((coefficientWord h c).map (fun s => s / 2)) ∈ numericFiber h c ∧
      Lychrel196.Palindrome (natValue ((coefficientWord h c).map (fun s => s / 2))) := by
  have hc := canonical_half_coefficientWord h c hp he
  have hr : ((coefficientWord h c).map (fun s => s / 2)).reverse =
      (coefficientWord h c).map (fun s => s / 2) := by
    simpa only [List.map_reverse] using
      congrArg (fun xs : List Nat => xs.map (fun s => s / 2)) (coefficientWord_reverse h c)
  have hq := digitPairSums_half_of_reverse_even (coefficientWord h c)
    (coefficientWord_reverse h c) he
  constructor
  · exact (mem_numericFiber_digits h c _).mpr ⟨_, hc, hq, rfl⟩
  · exact (palindrome_natValue_iff_reverse _ hc).mpr hr

end Agent101
