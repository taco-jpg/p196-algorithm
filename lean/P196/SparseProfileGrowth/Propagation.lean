import P196.Agent9DigitSumWindows.ProfileIsolation
import P196.Drafts.Agent106RunBirths.OverflowBirths

/-!
Nonzero columns of the original padded profile dynamics have an old nonzero
column at distance at most one. Iteration retains an initial nonzero origin
at distance at most the elapsed time. The profile need not be symmetric.
-/

set_option autoImplicit false

namespace SparseProfileGrowth

open DecimalDigits DecimalProfile

private theorem positive_before_tail (q : Nat → Nat) (L i : Nat)
    (htail : ∀ j, L ≤ j → q j = 0) (hi : 0 < q i) : i < L := by
  by_cases h : i < L
  · exact h
  · have hz := htail i (by omega)
    omega

/-- Every positive next column has a positive old column among its three
neighboring positions. The origin lies inside the old finite support. -/
theorem phi_positive_origin (q : Nat → Nat) (L i : Nat)
    (hv : Valid L q) (hi : 0 < phi q L i) :
    ∃ j, j < L ∧ 0 < q j ∧ j ≤ i + 1 ∧ i ≤ j + 1 := by
  have hL := hv.1
  have hq := hv.2.2.1
  have htail := hv.2.2.2.1
  by_cases hi0 : i = 0
  · subst i
    exact ⟨0, hL, hv.2.1, by omega, by omega⟩
  have hiw : i < nextLen q L := by
    by_cases h : i < nextLen q L
    · exact h
    · have hz := phi_tail q L hv i (by omega)
      omega
  by_cases hiL : i < L
  · by_cases hzero : q i = 0
    · by_cases hprev : q (i - 1) = 0
      · have hpred : i - 1 + 1 = i := by omega
        have hforward :
            carry q i = (q (i - 1) + carry q (i - 1)) / 10 := by
          simpa only [hpred] using
            (show carry q (i - 1 + 1) =
              (q (i - 1) + carry q (i - 1)) / 10 from rfl)
        by_cases hback : backCarry q L 0 = 0
        · by_cases hnext : q (i + 1) = 0
          · have hfc := carry_le_one q hq (i - 1)
            have hcarry : carry q i = 0 := by
              rw [hprev] at hforward
              omega
            have hbc : backCarry q L (i + 1) = 0 := by
              by_cases hinext : i + 1 < L
              · have he := backward_carry_step q L (i + 1) hinext
                have hb := backCarry_bounded q L (i + 1 + 1) hq
                rw [hnext] at he
                omega
              · exact backCarry_tail q L (i + 1) (by omega)
            have hf : output q i = 0 := by
              simp only [output, hzero, hcarry, Nat.zero_add, Nat.zero_mod]
            have hb : backOutput q L i = 0 := by
              simp only [backward_digit_formula q L i hiL, hzero, hbc,
                Nat.zero_add, Nat.zero_mod]
            have hz : phi q L i = 0 := by
              simp only [phi, hback, if_true, hf, hb, Nat.zero_add]
            omega
          · exact ⟨i + 1, positive_before_tail q L (i + 1) htail (by omega),
              by omega, by omega, by omega⟩
        · have hbackward := backward_carry_step q L i hiL
          have hsum :
              (q i + carry q i) % 10 +
                (q (i - 1) + backCarry q L i) % 10 = 0 := by
            apply (RunBirths.Overflow.adjacent_residues_zero_iff
              (q (i - 1)) (q i) (carry q (i - 1)) (carry q i)
              (backCarry q L i) (backCarry q L (i + 1))
              (hq (i - 1)) (hq i) (carry_le_one q hq (i - 1))
              (backCarry_bounded q L (i + 1) hq) hforward hbackward).mpr
            exact Or.inl ⟨hprev, hzero⟩
          have hb : backOutput q L (i - 1) =
              (q (i - 1) + backCarry q L i) % 10 := by
            simpa only [hpred] using
              backward_digit_formula q L (i - 1) (by omega)
          have hz : phi q L i = 0 := by
            simpa only [phi, hback, if_false, hi0, output, hb] using hsum
          omega
      · exact ⟨i - 1, by omega, by omega, by omega, by omega⟩
    · exact ⟨i, hiL, by omega, by omega, by omega⟩
  · have hn := (nextLen_bounds q L).2
    have he : i = L := by omega
    subst i
    exact ⟨L - 1, by omega, hv.2.2.2.2, by omega, by omega⟩

/-- Every positive column after `t` steps has a positive initial origin at
distance at most `t`, with the initial finite-width boundary retained. -/
theorem iter_positive_origin (s : State) (t i : Nat)
    (hv : Valid s.1 s.2) (hi : 0 < (iter s t).2 i) :
    ∃ j, j < s.1 ∧ 0 < s.2 j ∧ j ≤ i + t ∧ i ≤ j + t := by
  induction t generalizing i with
  | zero =>
    change 0 < s.2 i at hi
    exact ⟨i, positive_before_tail s.2 s.1 i hv.2.2.2.1 hi,
      hi, by omega, by omega⟩
  | succ t ih =>
    change 0 < phi (iter s t).2 (iter s t).1 i at hi
    obtain ⟨k, _, hk, hki, hik⟩ := phi_positive_origin
      (iter s t).2 (iter s t).1 i (iter_valid s t hv) hi
    obtain ⟨j, hj, hpos, hjk, hkj⟩ := ih k hk
    exact ⟨j, hj, hpos, by omega, by omega⟩

#print axioms phi_positive_origin
#print axioms iter_positive_origin

end SparseProfileGrowth
