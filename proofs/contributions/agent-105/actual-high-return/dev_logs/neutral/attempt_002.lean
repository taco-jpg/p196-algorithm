import LychrelDigitSums

/-!
The actual decimal normalization of a symmetric word with exterior nine
cannot overflow and still have all next pair coefficients at least nine.
No canonical-realizability or central parity premise is needed.
-/

namespace Agent105.NeutralExterior

open DecimalDigits FoldedDecimal

theorem carry_neutral_segment (q : Nat → Nat) (a n : Nat)
    (hc : carry q a ≤ 1)
    (hn : ∀ i, i < n → q (a + i) = 9) :
    carry q (a + n) = carry q a := by
  revert hn
  induction n with
  | zero => intro _; simp
  | succ n ih =>
    intro hn
    have hp := ih (fun i hi => hn i (by omega))
    have hq := hn n (by omega)
    have he : a + (n + 1) = (a + n) + 1 := by omega
    rw [he, carry, hq, hp]
    omega

theorem first_non_neutral (q : Nat → Nat) (L : Nat)
    (hex : ∃ i, i < L ∧ q i ≠ 9) :
    ∃ j, j < L ∧ q j ≠ 9 ∧ ∀ i, i < j → q i = 9 := by
  classical
  induction L with
  | zero => obtain ⟨i, hi, _⟩ := hex; omega
  | succ L ih =>
    by_cases he : ∃ i, i < L ∧ q i ≠ 9
    · obtain ⟨j, hj, hq, hp⟩ := ih he
      exact ⟨j, by omega, hq, hp⟩
    · have hp : ∀ i, i < L → q i = 9 := by
        intro i hi
        apply Classical.byContradiction
        intro hn
        exact he ⟨i, hi, hn⟩
      have hq : q L ≠ 9 := by
        obtain ⟨i, hi, hni⟩ := hex
        have hEq : i = L := by
          apply Classical.byContradiction
          intro hne
          exact hni (hp i (by omega))
        simpa [hEq] using hni
      exact ⟨L, by omega, hq, hp⟩

/-- Reflection uses the actual output width `L+1`. The witness pairs the
first non-nine source column with a neutral column whose incoming carry is
one. This holds even for symmetric words with an unrealizable odd center. -/
theorem neutral_overflow_has_low_pair (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hout : q 0 = 9) (hover : carry q L = 1) :
    ∃ i, i < nextWidth q L ∧ nextColumns q L i ≤ 8 := by
  classical
  have hbits := carry_bounded q L hb
  have hex : ∃ i, i < L ∧ q i ≠ 9 := by
    apply Classical.byContradiction
    intro hnone
    have hall : ∀ i, i < L → q i = 9 := by
      intro i hi
      apply Classical.byContradiction
      intro hn
      exact hnone ⟨i, hi, hn⟩
    have hz := carry_neutral_segment q 0 L (by simp [carry])
      (by simpa using hall)
    simp only [Nat.zero_add, carry] at hz
    omega
  obtain ⟨j, hj, hjn, hpre⟩ := first_non_neutral q L hex
  have hjpos : 0 < j := by
    apply Classical.byContradiction
    intro hz
    have he : j = 0 := by omega
    exact hjn (by simpa [he] using hout)
  have hcj : carry q j = 0 := by
    have hz := carry_neutral_segment q 0 j (by simp [carry])
      (by simpa using hpre)
    simpa only [Nat.zero_add, carry] using hz
  let k := L - j
  have hkpos : 0 < k := by dsimp [k]; omega
  have hkL : k < L := by dsimp [k]; omega
  have htail : ∀ i, i < L - k → q (k + i) = 9 := by
    intro i hi
    have hki : k + i < L := by omega
    rw [hs (k + i) hki]
    apply hpre
    dsimp [k] at *
    omega
  have hck : carry q k = 1 := by
    have hh := carry_neutral_segment q k (L - k) (hbits k (by omega)) htail
    have he : k + (L - k) = L := by omega
    rw [he, hover] at hh
    exact hh.symm
  have hmir : k - 1 = L - 1 - j := by dsimp [k]; omega
  have hqmir : q (k - 1) = q j := by
    rw [hmir]
    exact (hs j hj).symm
  have hrec : carry q k = (q (k - 1) + carry q (k - 1)) / 10 := by
    have he : k = (k - 1) + 1 := by omega
    exact (congrArg (carry q) he).trans (by rfl)
  have hqjhigh : 10 ≤ q j := by
    have hbit := hbits (k - 1) (by omega)
    rw [hck, hqmir] at hrec
    omega
  have hqk : q k = 9 := by
    rw [hs k hkL]
    apply hpre
    dsimp [k]
    omega
  have hdj : output q j ≤ 8 := by
    have hbj := hb j hj
    simp only [output, hcj, Nat.add_zero]
    omega
  have hdk : output q k = 0 := by simp [output, hqk, hck]
  have href : L + 1 - 1 - j = k := by dsimp [k]; omega
  refine ⟨j, ?_, ?_⟩
  · simp only [nextWidth, hover, Nat.one_ne_zero, if_false]
    omega
  · simp only [nextColumns, hover, Nat.one_ne_zero, if_false, columnSum,
      reflected, href, extended, hj, hkL, if_true, hdk, Nat.add_zero]
    exact hdj

/-- For a symmetric bounded word with exterior at most nine, a successor
whose every pair coefficient is at least nine forces no overflow. -/
theorem low_outer_high_next_no_overflow (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hout : q 0 ≤ 9)
    (hhigh : ∀ i, i < nextWidth q L → 9 ≤ nextColumns q L i) :
    carry q L = 0 := by
  have hbits := carry_bounded q L hb
  by_cases hzero : carry q L = 0
  · exact hzero
  have hover : carry q L = 1 := by have := hbits L (Nat.le_refl L); omega
  have houter : q 0 = 9 := by
    have hlast : q (L - 1) = q 0 := by simpa using (hs 0 hL).symm
    have hcprev := hbits (L - 1) (by omega)
    have he : L = (L - 1) + 1 := by omega
    have hrec : carry q L = (q (L - 1) + carry q (L - 1)) / 10 := by
      exact (congrArg (carry q) he).trans (by rfl)
    rw [hover, hlast] at hrec
    omega
  obtain ⟨i, hi, hlow⟩ := neutral_overflow_has_low_pair q L hL hb hs houter hover
  have hh := hhigh i hi
  omega

end Agent105.NeutralExterior
