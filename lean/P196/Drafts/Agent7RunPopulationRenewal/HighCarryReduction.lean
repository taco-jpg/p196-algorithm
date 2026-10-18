import P196.Foundations.LychrelDigitSums

/-! Exact adjacent-sum reduction for decimal pair coefficients 9 through 18.
All carries after the first column are one. The next actual pair word has
low endpoints, and the second output is palindromic exactly when every
adjacent original coefficient sum is at most 27. -/

namespace HighCarryReduction

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196

def HighCarryWord (q : Nat → Nat) (L : Nat) : Prop :=
  (∀ i, i < L → 9 ≤ q i ∧ q i ≤ 18) ∧ 10 ≤ q 0

theorem carry_one (q : Nat → Nat) (L : Nat) (hq : HighCarryWord q L) :
    ∀ i, 0 < i → i ≤ L → carry q i = 1 := by
  intro i
  induction i with
  | zero => intro hi _; omega
  | succ i ih =>
    intro _ hi
    have hqi := hq.1 i (by omega)
    by_cases hz : i = 0
    · subst i
      have hfirst := hq.2
      simp only [carry, Nat.add_zero]
      omega
    · have hc := ih (by omega) (by omega)
      simp only [carry, hc]
      omega

theorem output_zero (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L) : output q 0 = q 0 - 10 := by
  have hfirst := hq.2
  have hb := hq.1 0 hL
  simp only [output, carry, Nat.add_zero]
  omega

theorem output_internal (q : Nat → Nat) (L i : Nat)
    (hq : HighCarryWord q L) (hipos : 0 < i) (hi : i < L) :
    output q i = q i - 9 := by
  have hc := carry_one q L hq i hipos (by omega)
  have hb := hq.1 i hi
  simp only [output, hc]
  omega

theorem nextWidth_eq (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L) : nextWidth q L = L + 1 := by
  simp [nextWidth, carry_one q L hq L hL (Nat.le_refl L)]

theorem nextColumns_zero (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L) : nextColumns q L 0 = q 0 - 9 := by
  have hc := carry_one q L hq L hL (Nat.le_refl L)
  have ho := output_zero q L hL hq
  have hfirst := hq.2
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected,
    Nat.add_sub_cancel, Nat.sub_zero, extended, hL, Nat.lt_irrefl, if_true, if_false]
  omega

theorem nextColumns_last (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L) : nextColumns q L L = q 0 - 9 := by
  have hc := carry_one q L hq L hL (Nat.le_refl L)
  have ho := output_zero q L hL hq
  have hfirst := hq.2
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected,
    Nat.add_sub_cancel, Nat.sub_self, extended, hL, Nat.lt_irrefl, if_true, if_false]
  omega

theorem nextColumns_internal (q : Nat → Nat) (L i : Nat)
    (hq : HighCarryWord q L)
    (hsym : ∀ j, j < L → q j = q (L - 1 - j))
    (hipos : 0 < i) (hi : i < L) :
    nextColumns q L i = q (i - 1) + q i - 18 := by
  have hL : 0 < L := by omega
  have hc := carry_one q L hq L hL (Nat.le_refl L)
  have hmpos : 0 < L - i := by omega
  have hm : L - i < L := by omega
  have ha := output_internal q L i hq hipos hi
  have hb := output_internal q L (L - i) hq hmpos hm
  have hindex : L - 1 - (i - 1) = L - i := by omega
  have hmirror := hsym (i - 1) (by omega)
  rw [hindex] at hmirror
  rw [← hmirror] at hb
  have hqa := hq.1 i hi
  have hqb := hq.1 (i - 1) (by omega)
  simp only [nextColumns, hc, Nat.one_ne_zero, if_false, columnSum, reflected,
    Nat.add_sub_cancel, extended, hi, hm, if_true]
  omega

theorem nextColumns_low_iff_adjacent (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L)
    (hsym : ∀ j, j < L → q j = q (L - 1 - j)) :
    (∀ i, i < nextWidth q L → nextColumns q L i ≤ 9) ↔
      ∀ i, 0 < i → i < L → q (i - 1) + q i ≤ 27 := by
  rw [nextWidth_eq q L hL hq]
  constructor
  · intro hlow i hipos hi
    have h := hlow i (by omega)
    rw [nextColumns_internal q L i hq hsym hipos hi] at h
    have ha := hq.1 i hi
    have hb := hq.1 (i - 1) (by omega)
    omega
  · intro hadj i hi
    by_cases hzero : i = 0
    · subst i
      rw [nextColumns_zero q L hL hq]
      have hb := hq.1 0 hL
      omega
    · by_cases hlast : i = L
      · subst i
        rw [nextColumns_last q L hL hq]
        have hb := hq.1 0 hL
        omega
      · have hipos : 0 < i := by omega
        have hiL : i < L := by omega
        rw [nextColumns_internal q L i hq hsym hipos hiL]
        have h := hadj i hipos hiL
        omega

/-- A low outer pair coefficient excludes the special overflow-palindrome
class, leaving exactly the all-small class. -/
theorem numeric_palindrome_iff_low_outer (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (houter : q 0 ≤ 9) :
    Palindrome (step n) ↔ ∀ i, i < L → q i ≤ 9 := by
  constructor
  · intro hp
    have hp' : Palindrome (step (value d L)) := by simpa only [hc.2.2.2] using hp
    rcases (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp'
      with hsmall | ⟨heleven, _⟩
    · intro i hi
      simpa only [hrep i hi] using hsmall i hi
    · rw [hrep 0 hc.1] at heleven
      omega
  · intro hsmall
    have hp : Palindrome (step (value d L)) := by
      apply (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mpr
      exact Or.inl (fun i hi => by simpa only [hrep i hi] using hsmall i hi)
    simpa only [hc.2.2.2] using hp

/-- Exact ordinary-integer second-output criterion; adjacency is vacuous
at width one, which correctly gives a palindrome at the second output. -/
theorem numeric_second_palindrome_iff_adjacent (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hq : HighCarryWord q L) :
    Palindrome (orbit n 2) ↔ ∀ i, 0 < i → i < L → q (i - 1) + q i ≤ 27 := by
  have had := NormalizationBridge.admissible_congr L (columnSum d L) q
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  obtain ⟨e, he, her⟩ := iterPairs_representation n d q L 1 hc hrep
  change Canonical (orbit n 1) e (nextWidth q L) at he
  change ∀ i, i < nextWidth q L → columnSum e (nextWidth q L) i = nextColumns q L i at her
  have hout : nextColumns q L 0 ≤ 9 := by
    rw [nextColumns_zero q L hc.1 hq]
    have hb := hq.1 0 hc.1
    omega
  have hp := numeric_palindrome_iff_low_outer (orbit n 1) e (nextColumns q L)
    (nextWidth q L) he her hout
  exact hp.trans (nextColumns_low_iff_adjacent q L hc.1 hq had.2.2.2.1)

theorem numeric_large_adjacent_safe_second (n : Nat) (d q : Nat → Nat) (L i : Nat)
    (hc : Canonical n d L) (hrep : ∀ j, j < L → columnSum d L j = q j)
    (hq : HighCarryWord q L) (hipos : 0 < i) (hi : i < L)
    (hlarge : 28 ≤ q (i - 1) + q i) : ¬ Palindrome (orbit n 2) := by
  intro hp
  have h := (numeric_second_palindrome_iff_adjacent n d q L hc hrep hq).mp hp i hipos hi
  omega

theorem threshold_controls :
    step 974 = 1453 ∧ orbit 974 2 = 4994 ∧ Palindrome (orbit 974 2) ∧
    step 77 = 154 ∧ orbit 77 2 = 605 ∧ ¬ Palindrome (orbit 77 2) := by decide

theorem singleton_control :
    step 9 = 18 ∧ orbit 9 2 = 99 ∧ Palindrome (orbit 9 2) := by decide

end HighCarryReduction
