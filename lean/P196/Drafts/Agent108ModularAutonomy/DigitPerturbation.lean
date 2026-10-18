import P196.Drafts.Agent108ModularAutonomy.AutonomyDefs

/-! Exact-width digit perturbations for ordinary decimal reversal. -/
namespace ModularAutonomy

open Lychrel196 DecimalDigits

def incrementUnits (d : Nat → Nat) (i : Nat) : Nat :=
  if i = 0 then d 0 + 1 else d i

theorem canonical_units (n L : Nat) (d : Nat → Nat)
    (hc : Canonical n d L) : n % 10 = d 0 := by
  obtain ⟨k, hL⟩ := Nat.exists_eq_succ_of_ne_zero (by have := hc.1; omega : L ≠ 0)
  subst L
  have hv := value_shift d k
  have hb := hc.2.1 0 (by omega)
  rw [hc.2.2.2] at hv
  omega

theorem incrementUnits_value (d : Nat → Nat) (L : Nat) (hL : 0 < L) :
    value (incrementUnits d) L = value d L + 1 := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : L ≠ 0)
  rw [value_shift, value_shift]
  have htail : value (fun i => incrementUnits d (i + 1)) k =
      value (fun i => d (i + 1)) k := by
    apply value_congr
    intro i _
    simp [incrementUnits]
  rw [htail]
  simp [incrementUnits, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

theorem canonical_incrementUnits (n L : Nat) (d : Nat → Nat)
    (hc : Canonical n d L) (hu : n % 10 ≤ 8) :
    Canonical (n + 1) (incrementUnits d) L := by
  have hd0 : d 0 ≤ 8 := by rw [canonical_units n L d hc] at hu; exact hu
  refine ⟨hc.1, ?_, ?_, ?_⟩
  · intro i hi
    by_cases hz : i = 0
    · simp [incrementUnits, hz]; omega
    · simpa [incrementUnits, hz] using hc.2.1 i hi
  · by_cases hz : L - 1 = 0
    · simp [incrementUnits, hz]
    · simpa [incrementUnits, hz] using hc.2.2.1
  · rw [incrementUnits_value d L hc.1, hc.2.2.2]

theorem reverse10_succ_of_units_le_eight (n L : Nat) (d : Nat → Nat)
    (hc : Canonical n d L) (hu : n % 10 ≤ 8) :
    reverse10 (n + 1) = reverse10 n + 10 ^ (L - 1) := by
  have he := canonical_incrementUnits n L d hc hu
  rw [← he.2.2.2, reverse10_value _ _ he.2.1 (Or.inr he.2.2.1)]
  rw [← hc.2.2.2, reverse10_value _ _ hc.2.1 (Or.inr hc.2.2.1)]
  obtain ⟨k, hL⟩ := Nat.exists_eq_succ_of_ne_zero (by have := hc.1; omega : L ≠ 0)
  subst L
  rw [reflected_value_shift, reflected_value_shift]
  have htail : value (reflected (fun i => incrementUnits d (i + 1)) k) k =
      value (reflected (fun i => d (i + 1)) k) k := by
    apply value_congr
    intro i _
    simp [reflected, incrementUnits]
  rw [htail]
  simp [incrementUnits, Nat.add_mul, Nat.add_assoc]

def digitSpike (j a i : Nat) : Nat := if i = j then a else 0

theorem value_digitSpike (j a L : Nat) :
    value (digitSpike j a) L = if j < L then a * 10 ^ j else 0 := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    rw [value, ih]
    by_cases hj : j < L
    · have hn : L ≠ j := by omega
      simp [digitSpike, hj, hn, show j < L + 1 by omega]
    · by_cases he : j = L
      · subst j; simp [digitSpike]
      · have hn : L ≠ j := by omega
        have hnot : ¬ j < L + 1 := by omega
        simp [digitSpike, hj, hn, hnot]

theorem reflected_digitSpike_value (j a L : Nat) (hj : j < L) :
    value (reflected (digitSpike j a) L) L = a * 10 ^ (L - 1 - j) := by
  have he : value (reflected (digitSpike j a) L) L =
      value (digitSpike (L - 1 - j) a) L := by
    apply value_congr
    intro i hi
    have hind : (L - 1 - i = j) ↔ (i = L - 1 - j) := by omega
    simp only [reflected, digitSpike, hind]
  rw [he, value_digitSpike]
  simp [show L - 1 - j < L by omega]

def twoDigits (L k a i : Nat) : Nat :=
  digitSpike (L - 1) 1 i + digitSpike k a i

theorem twoDigits_canonical (L k a : Nat) (hL : 0 < L)
    (hk : k < L - 1) (ha : a ≤ 9) :
    Canonical (10 ^ (L - 1) + a * 10 ^ k) (twoDigits L k a) L := by
  refine ⟨hL, ?_, ?_, ?_⟩
  · intro i _
    by_cases ht : i = L - 1
    · have hn : i ≠ k := by omega
      simp [twoDigits, digitSpike, ht, show L - 1 ≠ k by omega]
    · by_cases hb : i = k
      · simpa [twoDigits, digitSpike, ht, hb, show k ≠ L - 1 by omega] using ha
      · simp [twoDigits, digitSpike, ht, hb]
  · simp [twoDigits, digitSpike, show L - 1 ≠ k by omega]
  · change value (fun i => digitSpike (L - 1) 1 i + digitSpike k a i) L = _
    rw [value_add, value_digitSpike, value_digitSpike]
    simp [show L - 1 < L by omega, show k < L by omega]

theorem reverse10_twoDigits (L k a : Nat) (hL : 0 < L)
    (hk : k < L - 1) (ha : a ≤ 9) :
    reverse10 (10 ^ (L - 1) + a * 10 ^ k) = 1 + a * 10 ^ (L - 1 - k) := by
  have hc := twoDigits_canonical L k a hL hk ha
  rw [← hc.2.2.2, reverse10_value _ _ hc.2.1 (Or.inr hc.2.2.1)]
  change value (fun i => reflected (digitSpike (L - 1) 1) L i +
      reflected (digitSpike k a) L i) L = _
  rw [value_add, reflected_digitSpike_value _ _ _ (by omega),
    reflected_digitSpike_value _ _ _ (by omega)]
  simp

theorem single_nine_canonical (L : Nat) (hL : 3 ≤ L) :
    Canonical (10 ^ (L - 1) + 9) (twoDigits L 0 9) L := by
  simpa using twoDigits_canonical L 0 9 (by omega) (by omega) (by decide)

theorem single_nine_successor_canonical (L : Nat) (hL : 3 ≤ L) :
    Canonical (10 ^ (L - 1) + 10) (twoDigits L 1 1) L := by
  simpa using twoDigits_canonical L 1 1 (by omega) (by omega) (by decide)

theorem single_nine_reverse_increment (L : Nat) (hL : 3 ≤ L) :
    reverse10 (10 ^ (L - 1) + 10) + 9 * 10 ^ (L - 1) =
      reverse10 (10 ^ (L - 1) + 9) + 10 ^ (L - 2) := by
  have hfirst := reverse10_twoDigits L 0 9 (by omega) (by omega) (by decide)
  have hnext := reverse10_twoDigits L 1 1 (by omega) (by omega) (by decide)
  simp only [Nat.pow_zero, Nat.mul_one, Nat.sub_zero] at hfirst
  simp only [Nat.pow_one, Nat.one_mul] at hnext
  have hind : L - 1 - 1 = L - 2 := by omega
  rw [hind] at hnext
  rw [hfirst, hnext]
  omega

end ModularAutonomy
