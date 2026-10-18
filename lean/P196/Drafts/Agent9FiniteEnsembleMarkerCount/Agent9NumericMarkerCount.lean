import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9MarkerEnumeration
import P196.Agent101DigitSplit.Agent101NumericFibers

/-!
Exact ordinary-integer form of equation (3) in the original finite-horizon
density note. Membership uses the actual decimal digits `n / 10^i % 10`.
The numeral interfaces are imported unchanged through the preserved
Lychrel196Research compatibility import of LychrelDigitSums.
-/

namespace P196.Agent9.Ensemble

open Agent101 DecimalDigits

def markerCount (L r : Nat) : Nat := (L / 2 - 1) / r
def freePairs (L r : Nat) : Nat := L / 2 - 1 - markerCount L r * r

theorem markerCount_mul_le (L r : Nat) : markerCount L r * r ≤ L / 2 - 1 :=
  Nat.div_mul_le_self _ _

theorem pairs_decomposition (L r : Nat) :
    markerCount L r * r + freePairs L r = L / 2 - 1 := by
  have h := markerCount_mul_le L r
  unfold freePairs
  omega

theorem width_decomposition (L r : Nat) (hL : 2 ≤ L) :
    2 * (markerCount L r * r + freePairs L r + 1) + L % 2 = L := by
  rw [pairs_decomposition]
  omega

/-- Every selected digit is among the non-leading free positions. -/
theorem selected_digits_le (L r : Nat) (hL : 0 < L) :
    2 * r * markerCount L r ≤ L - 1 := by
  have h := Nat.mul_le_mul_left 2 (markerCount_mul_le L r)
  have he : 2 * r * markerCount L r = 2 * (markerCount L r * r) := by
    simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  rw [he]
  omega

theorem free_exponent (L r : Nat) (hL : 2 ≤ L) :
    L - 1 - 2 * r * markerCount L r = 2 * freePairs L r + L % 2 + 1 := by
  have h := width_decomposition L r hL
  have he : 2 * r * markerCount L r = 2 * (markerCount L r * r) := by
    simp [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  rw [he]
  omega

theorem selected_block_bound (L r j : Nat) (hL : 0 < L) (hr : 0 < r)
    (hj : j < markerCount L r) : 1 + j * r + r ≤ L := by
  have hm := markerCount_mul_le L r
  have hjr := Nat.mul_le_mul_right r (show j + 1 ≤ markerCount L r by omega)
  rw [Nat.succ_mul] at hjr
  omega

theorem selected_position_geometry (L r j i : Nat) (hL : 0 < L) (hr : 0 < r)
    (hj : j < markerCount L r) (hi : i < r) :
    0 < 1 + j * r + i ∧ 1 + j * r + i < L / 2 ∧
      (L - 1) / 2 < L - 1 - (1 + j * r + i) ∧
      L - 1 - (1 + j * r + i) < L - 1 := by
  have hm := markerCount_mul_le L r
  have hjr := Nat.mul_le_mul_right r (show j + 1 ≤ markerCount L r by omega)
  rw [Nat.succ_mul] at hjr
  omega

def oneDigitWords : List (List Nat) := (List.range' 1 9).map (fun a => [a])

theorem mem_oneDigitWords (ds : List Nat) :
    ds ∈ oneDigitWords ↔ canonicalDigits ds ∧ ds.length = 1 := by
  constructor
  · intro hd
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hd
    have ha' := List.mem_range'_1.mp ha
    refine ⟨⟨?_, ?_⟩, rfl⟩
    · intro b hb
      have he : b = a := by simpa using hb
      subst b
      omega
    · simp only [List.getLastD_cons, List.getLastD_nil]
      omega
  · rintro ⟨hc, hlen⟩
    cases ds with
    | nil => simp at hlen
    | cons a ds =>
      have ht : ds = [] := List.length_eq_zero_iff.mp (by simpa using hlen)
      subst ds
      apply List.mem_map.mpr
      refine ⟨a, List.mem_range'_1.mpr ?_, rfl⟩
      have hb := hc.1 a (by simp)
      have hp := hc.2
      simp only [List.getLastD_cons, List.getLastD_nil] at hp
      omega

theorem oneDigitWords_nodup : oneDigitWords.Nodup := by decide
theorem length_oneDigitWords : oneDigitWords.length = 9 := by decide

def unmarkedDigits (L r : Nat) : List (List Nat) :=
  if L = 1 then oneDigitWords
  else markerWords r (markerCount L r) (freePairs L r) (L % 2)

theorem mem_unmarkedDigits (L r : Nat) (hL : 0 < L) (ds : List Nat) :
    ds ∈ unmarkedDigits L r ↔ canonicalDigits ds ∧ ds.length = L ∧
      ∀ j, j < markerCount L r → ¬ WordMarker ds (1 + j * r) r := by
  by_cases h1 : L = 1
  · subst L
    simp [unmarkedDigits, mem_oneDigitWords, markerCount]
  · rw [unmarkedDigits, if_neg h1, mem_markerWords,
      width_decomposition L r (by omega)]

theorem unmarkedDigits_nodup (L r : Nat) : (unmarkedDigits L r).Nodup := by
  unfold unmarkedDigits
  split
  · exact oneDigitWords_nodup
  · exact markerWords_nodup _ _ _ _

theorem length_unmarkedDigits (L r : Nat) (hL : 0 < L) :
    (unmarkedDigits L r).length =
      9 * 10 ^ (L - 1 - 2 * r * markerCount L r) *
        (10 ^ (2 * r) - 1) ^ markerCount L r := by
  by_cases h1 : L = 1
  · subst L
    simp [unmarkedDigits, markerCount, length_oneDigitWords]
  · rw [unmarkedDigits, if_neg h1, length_markerWords,
      free_exponent L r (by omega)]
    have hp : 100 ^ freePairs L r = 10 ^ (2 * freePairs L r) := by
      rw [Nat.pow_mul]
    rw [hp, show 90 = 9 * 10 by decide]
    simp only [Nat.pow_add, Nat.pow_one, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

def numericDigit (n i : Nat) : Nat := n / 10 ^ i % 10

/-- A positional bridge from the unchanged bounded-value interface to
ordinary quotient/remainder decimal digits. -/
theorem numericDigit_value (d : Nat → Nat) (L i : Nat)
    (hd : ∀ j, j < L → d j ≤ 9) (hi : i < L) :
    numericDigit (value d L) i = d i := by
  induction L generalizing d i with
  | zero => omega
  | succ L ih =>
    have h0 := hd 0 (by omega)
    have hs : ∀ j, j < L → d (j + 1) ≤ 9 := by
      intro j hj
      exact hd (j + 1) (by omega)
    cases i with
    | zero =>
      unfold numericDigit
      rw [Nat.pow_zero, Nat.div_one, value_shift]
      omega
    | succ i =>
      have hv : value d (L + 1) / 10 = value (fun j => d (j + 1)) L := by
        rw [value_shift]
        omega
      unfold numericDigit
      rw [Nat.pow_succ', ← Nat.div_div_eq_div_mul, hv]
      exact ih (fun j => d (j + 1)) i hs (by omega)

theorem canonical_numericDigit (n : Nat) (d : Nat → Nat) (L i : Nat)
    (hc : Canonical n d L) (hi : i < L) : numericDigit n i = d i := by
  rw [← hc.2.2.2]
  exact numericDigit_value d L i hc.2.1 hi

/-- An actual ordinary-integer all-nine marker, with no representation witness. -/
def NumericMarker (n L a r : Nat) : Prop :=
  ∀ i, i < r → numericDigit n (a + i) = 9 ∧
    numericDigit n (L - 1 - (a + i)) = 9

theorem numericMarker_natValue_iff (ds : List Nat) (a r : Nat)
    (hd : digitsBounded ds) (har : a + r ≤ ds.length) :
    NumericMarker (natValue ds) ds.length a r ↔ WordMarker ds a r := by
  have hb := (bounded_digitFn_iff ds).mpr hd
  have he (i : Nat) (hi : i < ds.length) :
      numericDigit (natValue ds) i = ds[i]?.getD 0 :=
    numericDigit_value (digitFn ds) ds.length i hb hi
  constructor
  · intro h i hi
    have hl : a + i < ds.length := by omega
    simpa only [he (a + i) hl, he (ds.length - 1 - (a + i)) (by omega)] using h i hi
  · intro h i hi
    have hl : a + i < ds.length := by omega
    simpa only [he (a + i) hl, he (ds.length - 1 - (a + i)) (by omega)] using h i hi

/-- Complete finite enumeration of ordinary integers in the marker complement. -/
def unmarkedSeeds (L r : Nat) : List Nat := (unmarkedDigits L r).map natValue

theorem unmarkedSeeds_nodup (L r : Nat) (hL : 0 < L) :
    (unmarkedSeeds L r).Nodup := by
  apply nodup_map_natValue _ ?_ (unmarkedDigits_nodup L r)
  exact fun ds hd => ((mem_unmarkedDigits L r hL ds).mp hd).1

/-- Full ordinary-integer semantics: exactly the canonical decimal interval
and absence of every selected all-nine block in the actual decimal digits. -/
theorem mem_unmarkedSeeds (L r n : Nat) (hL : 0 < L) (hr : 0 < r) :
    n ∈ unmarkedSeeds L r ↔ decimalWidth n L ∧
      ∀ j, j < markerCount L r → ¬ NumericMarker n L (1 + j * r) r := by
  constructor
  · intro hn
    obtain ⟨ds, hd, rfl⟩ := List.mem_map.mp hn
    obtain ⟨hc, hlen, hmarks⟩ := (mem_unmarkedDigits L r hL ds).mp hd
    refine ⟨?_, ?_⟩
    · simpa only [hlen] using canonical_decimalWidth _ _ _ ((canonicalDigits_iff ds).mp hc)
    · intro j hj hm
      apply hmarks j hj
      apply (numericMarker_natValue_iff ds (1 + j * r) r hc.1 ?_).mp
      · simpa only [hlen] using hm
      · simpa only [hlen] using selected_block_bound L r j hL hr hj
  · rintro ⟨hw, hmarks⟩
    obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical n L).mp hw
    obtain ⟨ds, hlen, hd, hv, _⟩ := canonical_to_list n d L hc
    apply List.mem_map.mpr
    refine ⟨ds, (mem_unmarkedDigits L r hL ds).mpr ⟨hd, hlen, ?_⟩, hv⟩
    intro j hj hm
    apply hmarks j hj
    have he := (numericMarker_natValue_iff ds (1 + j * r) r hd.1
      (by simpa only [hlen] using selected_block_bound L r j hL hr hj)).mpr hm
    simpa only [hlen, hv] using he

/-- Equation (3), counting every ordinary numeral once. -/
theorem length_unmarkedSeeds (L r : Nat) (hL : 0 < L) :
    (unmarkedSeeds L r).length =
      9 * 10 ^ (L - 1 - 2 * r * markerCount L r) *
        (10 ^ (2 * r) - 1) ^ markerCount L r := by
  rw [unmarkedSeeds, List.length_map, length_unmarkedDigits L r hL]

end P196.Agent9.Ensemble
