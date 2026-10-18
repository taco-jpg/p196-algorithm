import P196.Foundations.LychrelDigitSums
import P196.Agent104P620Witness.PrefixInverse
import P196.Agent104P620Witness.ActualPrefix
import P196.Agent104P620Witness.PalindromeBridge

/-!
# The eight `dd 0^(2r) dd` families never occur in the orbit of 196

Agent #119, task `agent119-eight-families-lean`.

Written source: `proofs/chat-6acee928/originals/p196_all_palindromes_and_eight_families.md`,
section 3 (written proof and Python checks only).  For `d ∈ {1,2,3,4,6,7,8,9}` and every
`r`, the palindrome `fam d r = 11 * d * (10^(2r+2) + 1)` (decimal `dd 0^(2r) dd`) is never
equal to `Lychrel196.orbit 196 t`.  The family `d = 5` is not treated.

This file: basic arithmetic of the family, the residue invariants of the 196 orbit
(never divisible by 3; divisible by 11 from time 3) and size bounds.
-/

namespace Agent119.EightFamilies

open DecimalDigits FoldedDecimal Lychrel196

/-- The palindrome `dd 0^(2r) dd`. -/
def fam (d r : Nat) : Nat := 11 * d * (10 ^ (2 * r + 2) + 1)

/-- Its decimal digits, indexed from the units end. -/
def famDigit (d r i : Nat) : Nat :=
  if i = 0 ∨ i = 1 ∨ i = 2 * r + 2 ∨ i = 2 * r + 3 then d else 0

theorem famDigit_zero (d r : Nat) : famDigit d r 0 = d := by simp [famDigit]
theorem famDigit_one (d r : Nat) : famDigit d r 1 = d := by simp [famDigit]
theorem famDigit_mid (d r i : Nat) (h2 : 2 ≤ i) (hi : i ≤ 2 * r + 1) :
    famDigit d r i = 0 := by
  unfold famDigit
  split <;> omega
theorem famDigit_hi1 (d r : Nat) : famDigit d r (2 * r + 2) = d := by simp [famDigit]
theorem famDigit_hi0 (d r : Nat) : famDigit d r (2 * r + 3) = d := by simp [famDigit]

theorem mul_sparse_aux (x y Q : Nat) : Q * (x + 10 * y) = x * Q + y * (Q * 10) := by
  rw [Nat.mul_add, Nat.mul_comm Q x, Nat.mul_comm 10 y, ← Nat.mul_assoc, Nat.mul_comm Q y,
    Nat.mul_assoc]

/-- Value of a digit function whose positions `2 .. 2r+1` vanish. -/
theorem value_sparse (f : Nat → Nat) (r : Nat)
    (hz : ∀ i, 2 ≤ i → i ≤ 2 * r + 1 → f i = 0) :
    value f (2 * r + 4) =
      f 0 + 10 * f 1 + 10 ^ (2 * r + 2) * (f (2 * r + 2) + 10 * f (2 * r + 3)) := by
  have hmid : ∀ k, 2 ≤ k → k ≤ 2 * r + 2 → value f k = f 0 + 10 * f 1 := by
    intro k hk2 hk
    induction k with
    | zero => omega
    | succ k ih =>
      by_cases h1 : k = 1
      · subst h1
        simp [value]
        omega
      · have hk' : 2 ≤ k := by omega
        rw [value, ih hk' (by omega), hz k hk' (by omega)]
        simp
  have h2 : value f (2 * r + 2) = f 0 + 10 * f 1 := hmid _ (by omega) (Nat.le_refl _)
  have hv : value f (2 * r + 4) =
      value f (2 * r + 2) + f (2 * r + 2) * 10 ^ (2 * r + 2) +
        f (2 * r + 3) * 10 ^ (2 * r + 3) := rfl
  rw [hv, h2, mul_sparse_aux, show 10 ^ (2 * r + 3) = 10 ^ (2 * r + 2) * 10 from Nat.pow_succ ..]
  omega

theorem fam_value (d r : Nat) : value (famDigit d r) (2 * r + 4) = fam d r := by
  rw [value_sparse (famDigit d r) r (fun i h1 h2 => famDigit_mid d r i h1 h2)]
  rw [famDigit_zero, famDigit_one, famDigit_hi1, famDigit_hi0]
  unfold fam
  rw [show d + 10 * d = 11 * d by omega, Nat.mul_comm (10 ^ (2 * r + 2)) (11 * d), Nat.mul_add,
    Nat.mul_one]
  omega

theorem fam_canonical (d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9) :
    Canonical (fam d r) (famDigit d r) (2 * r + 4) := by
  refine ⟨by omega, ?_, ?_, fam_value d r⟩
  · intro i _
    unfold famDigit
    split <;> omega
  · have h : 2 * r + 4 - 1 = 2 * r + 3 := by omega
    rw [h, famDigit_hi0]
    omega

/-! ## Residue invariants and size of the 196 orbit -/

theorem step_mod3 (n : Nat) : step n % 3 = (2 * n) % 3 := by
  have h := step_mod9 n
  have h1 : step n % 3 = step n % 9 % 3 := (Nat.mod_mod_of_dvd _ (by decide)).symm
  have h2 : (2 * n) % 3 = (2 * n) % 9 % 3 := (Nat.mod_mod_of_dvd _ (by decide)).symm
  rw [h1, h2, h]

/-- The orbit of 196 never contains a multiple of 3. -/
theorem orbit196_not_dvd3 (t : Nat) : orbit 196 t % 3 ≠ 0 := by
  have h : ∀ t, orbit 196 t % 3 = 1 ∨ orbit 196 t % 3 = 2 := by
    intro t
    induction t with
    | zero => decide
    | succ t ih =>
      show step (orbit 196 t) % 3 = 1 ∨ step (orbit 196 t) % 3 = 2
      rw [step_mod3]
      omega
  have := h t
  omega

theorem fam_dvd3 (d r : Nat) (hd : d % 3 = 0) : fam d r % 3 = 0 := by
  unfold fam
  rw [Nat.mul_mod, show 11 * d % 3 = 0 by omega, Nat.zero_mul, Nat.zero_mod]

theorem orbit196_three : orbit 196 3 = 7436 := by decide

/-- Divisibility by 11 from time 3 on. -/
theorem orbit196_dvd11 (t : Nat) (ht : 3 ≤ t) : 11 ∣ orbit 196 t := by
  have h : t = 3 + (t - 3) := by omega
  rw [h, LychrelCertificates.orbit_add, orbit196_three]
  exact AstraModular.orbit_preserves_dvd11 7436 (t - 3) (by decide)

theorem step_ge (n : Nat) : n ≤ step n := Nat.le_add_right n _

theorem orbit_mono (n a b : Nat) (h : a ≤ b) : orbit n a ≤ orbit n b := by
  have hb : b = a + (b - a) := by omega
  rw [hb, LychrelCertificates.orbit_add]
  generalize b - a = k
  induction k with
  | zero => exact Nat.le_refl _
  | succ k ih => exact Nat.le_trans ih (step_ge _)

theorem orbit196_five : orbit 196 5 = 52514 := by decide

theorem fam_zero (d : Nat) : fam d 0 = 1111 * d := by
  unfold fam
  omega

theorem fam_ge (d r : Nat) (hd : 1 ≤ d) (hr : 1 ≤ r) : 110011 ≤ fam d r := by
  unfold fam
  have hp : 10 ^ 4 ≤ 10 ^ (2 * r + 2) := Nat.pow_le_pow_right (by decide) (by omega)
  have : 10 ^ 4 = 10000 := by decide
  have h1 : 11 * 1 * (10000 + 1) ≤ 11 * d * (10 ^ (2 * r + 2) + 1) :=
    Nat.mul_le_mul (Nat.mul_le_mul_left 11 hd) (by omega)
  omega

/-- Small times and the width-four members are excluded by direct computation and size. -/
theorem early_or_short (d r t : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9)
    (h : orbit 196 t = fam d r) : 5 ≤ t ∧ 1 ≤ r := by
  by_cases ht : 5 ≤ t
  · refine ⟨ht, ?_⟩
    by_cases hr : r = 0
    · subst hr
      have hm := orbit_mono 196 5 t ht
      rw [orbit196_five, h, fam_zero] at hm
      omega
    · omega
  · exfalso
    by_cases hr : r = 0
    · subst hr
      rw [fam_zero] at h
      have h0 : orbit 196 0 = 196 := rfl
      have h1 : orbit 196 1 = 887 := by decide
      have h2 : orbit 196 2 = 1675 := by decide
      have h3 : orbit 196 3 = 7436 := by decide
      have h4 : orbit 196 4 = 13783 := by decide
      have : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 := by omega
      rcases this with rfl | rfl | rfl | rfl | rfl <;> omega
    · have hge := fam_ge d r hd1 (by omega)
      have hle : orbit 196 t ≤ orbit 196 4 := orbit_mono 196 t 4 (by omega)
      have h4 : orbit 196 4 = 13783 := by decide
      omega

#print axioms fam_canonical
#print axioms orbit196_not_dvd3
#print axioms orbit196_dvd11
#print axioms early_or_short

/-! ## Exact pair states of the 196 orbit -/

open OverflowCarryNormalization NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumnKernel.PalindromeBridge

/-- Canonical digits of 196, units first. -/
def d196 (i : Nat) : Nat := if i = 0 then 6 else if i = 1 then 9 else 1

theorem canonical196 : Canonical 196 d196 3 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i _
  unfold d196
  split
  · omega
  · split <;> omega

def q196 : Nat → Nat := columnSum d196 3

/-- The exact (width, pair-sum word) state of `orbit 196 t`. -/
def V (t : Nat) : Nat × (Nat → Nat) := iterPairs q196 3 t

theorem V_adm (t : Nat) : Admissible (V t).1 (V t).2 :=
  iterPairs_admissible q196 3 t (canonical_admissible 196 d196 3 canonical196)

theorem V_rep (t : Nat) : ∃ e, Canonical (orbit 196 t) e (V t).1 ∧
    ∀ i, i < (V t).1 → columnSum e (V t).1 i = (V t).2 i :=
  iterPairs_representation 196 d196 q196 3 t canonical196 (fun _ _ => rfl)

theorem V_succ (t : Nat) :
    V (t + 1) = (nextWidth (V t).2 (V t).1, nextColumns (V t).2 (V t).1) := rfl

theorem V_succ_fst (t : Nat) : (V (t + 1)).1 = nextWidth (V t).2 (V t).1 := rfl
theorem V_succ_snd (t : Nat) : (V (t + 1)).2 = nextColumns (V t).2 (V t).1 := rfl

-- Keep elaboration and `omega` from unfolding the orbit state.
attribute [irreducible] V

theorem value_lt_pow (e : Nat → Nat) (L : Nat) (h : ∀ i, i < L → e i ≤ 9) :
    value e L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have h1 := ih (fun i hi => h i (by omega))
    have h2 := h L (by omega)
    have h3 : e L * 10 ^ L ≤ 9 * 10 ^ L := Nat.mul_le_mul_right _ h2
    show value e L + e L * 10 ^ L < 10 ^ (L + 1)
    rw [Nat.pow_succ]
    omega

theorem V_width (t k : Nat) (hk : 10 ^ k ≤ orbit 196 t) : k + 1 ≤ (V t).1 := by
  obtain ⟨e, he, _⟩ := V_rep t
  have hv := value_lt_pow e (V t).1 he.2.1
  rw [he.2.2.2] at hv
  apply Nat.succ_le_of_lt
  apply Nat.lt_of_not_le
  intro hle
  have : 10 ^ (V t).1 ≤ 10 ^ k := Nat.pow_le_pow_right (by decide) hle
  omega

theorem V_width3 (t : Nat) : 3 ≤ (V t).1 := by
  have hm := orbit_mono 196 0 t (Nat.zero_le _)
  have h0 : orbit 196 0 = 196 := rfl
  have := V_width t 2 (by rw [show (10 : Nat) ^ 2 = 100 from rfl]; omega)
  omega

theorem V_width4 (t : Nat) (ht : 2 ≤ t) : 4 ≤ (V t).1 := by
  have hm := orbit_mono 196 2 t ht
  have h2 : orbit 196 2 = 1675 := by decide
  have := V_width t 3 (by rw [show (10 : Nat) ^ 3 = 1000 from rfl]; omega)
  omega

theorem canonical_congr {n : Nat} {d e : Nat → Nat} {L : Nat}
    (hc : Canonical n d L) (h : ∀ i, i < L → d i = e i) : Canonical n e L := by
  obtain ⟨hL, hd, hlead, hv⟩ := hc
  refine ⟨hL, fun i hi => (h i hi) ▸ hd i hi, ?_, ?_⟩
  · rw [← h (L - 1) (by omega)]
    exact hlead
  · rw [← value_congr d e L h]
    exact hv

theorem V_carry_le (t : Nat) : carry (V t).2 (V t).1 ≤ 1 :=
  carry_bounded (V t).2 (V t).1 (V_adm t).2.2.1 (V t).1 (Nat.le_refl _)

theorem next_digits_no_overflow (t : Nat) (hc : carry (V t).2 (V t).1 = 0) :
    Canonical (orbit 196 (t + 1)) (output (V t).2) (V t).1 := by
  obtain ⟨e, he, hr⟩ := V_rep t
  have hcar := carry_congr_upto (columnSum e (V t).1) (V t).2 (V t).1 hr (V t).1 (Nat.le_refl _)
  have h := canonical_next_no_overflow (orbit 196 t) e (V t).1 he (by rw [hcar]; exact hc)
  exact canonical_congr h (output_congr_upto _ _ _ hr)

theorem next_digits_overflow (t : Nat) (hc : carry (V t).2 (V t).1 = 1) :
    Canonical (orbit 196 (t + 1)) (extended (V t).2 (V t).1) ((V t).1 + 1) := by
  obtain ⟨e, he, hr⟩ := V_rep t
  have hcar := carry_congr_upto (columnSum e (V t).1) (V t).2 (V t).1 hr (V t).1 (Nat.le_refl _)
  have h := canonical_next_overflow (orbit 196 t) e (V t).1 he (by rw [hcar]; exact hc)
  exact canonical_congr h (fun i _ => extended_congr_upto _ _ _ hr i)

/-- Agent #104's projection theorem along the 196 orbit. -/
theorem V_prefix_pred (t k : Nat) (hk0 : 0 < k) (hk : k ≤ (V t).1) :
    wordPrefix (V t).2 k ∈ SevenColumn.prefixPredecessors (wordPrefix (V (t + 1)).2 k) := by
  rw [V_succ_snd]
  exact actual_mem_prefixPredecessors (V t).2 (V t).1 k (V_adm t) hk0 hk

theorem wordPrefix_two (q : Nat → Nat) : wordPrefix q 2 = [q 0, q 1] := rfl
theorem wordPrefix_three (q : Nat → Nat) : wordPrefix q 3 = [q 0, q 1, q 2] := rfl
theorem wordPrefix_four (q : Nat → Nat) : wordPrefix q 4 = [q 0, q 1, q 2, q 3] := rfl

/-- `fam d r` is a palindrome (its canonical digits are symmetric). -/
theorem fam_palindrome (d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9) : Palindrome (fam d r) := by
  have hc := fam_canonical d r hd1 hd9
  rw [← hc.2.2.2]
  apply (palindrome_value_iff (famDigit d r) (2 * r + 4) hc.2.1 (Or.inr hc.2.2.1)).mpr
  intro i hi
  unfold famDigit
  split <;> split <;> omega

/-! ## The final step into `fam d r` -/

/-- An overflowing final step forces `d = 1` and the source prefix `[11, 0, 0]`. -/
theorem last_step_overflow (s d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9) (hr : 1 ≤ r)
    (h : orbit 196 (s + 1) = fam d r) (hc : carry (V s).2 (V s).1 = 1) :
    d = 1 ∧ wordPrefix (V s).2 3 = [11, 0, 0] := by
  have hcan := next_digits_overflow s hc
  rw [h] at hcan
  obtain ⟨hw, hdig⟩ := canonical_unique hcan (fam_canonical d r hd1 hd9)
  have hL : (V s).1 = 2 * r + 3 := by omega
  have htop := hdig (V s).1 (by omega)
  simp only [extended, Nat.lt_irrefl, if_false, hc] at htop
  rw [hL, famDigit_hi0] at htop
  have hd : d = 1 := htop.symm
  subst hd
  refine ⟨rfl, ?_⟩
  -- the overflow palindrome criterion on the actual source digits
  obtain ⟨e, he, hr'⟩ := V_rep s
  have hcar := carry_congr_upto (columnSum e (V s).1) (V s).2 (V s).1 hr' (V s).1 (Nat.le_refl _)
  have hpal : Palindrome (step (value e (V s).1)) := by
    rw [he.2.2.2]
    show Palindrome (orbit 196 (s + 1))
    rw [h]
    exact fam_palindrome 1 r (by decide) (by decide)
  obtain ⟨h0, hvals⟩ := (step_palindrome_iff_overflow e (V s).1 he.1 he.2.1 he.2.2.1
    (by rw [hcar]; exact hc)).mp hpal
  have q0 : (V s).2 0 = 11 := by rw [← hr' 0 (by omega)]; exact h0
  have qv : ∀ i, i < (V s).1 → (V s).2 i = 0 ∨ (V s).2 i = 11 := by
    intro i hi
    rw [← hr' i hi]
    exact hvals i hi
  have hb := carry_bounded (V s).2 (V s).1 (V_adm s).2.2.1
  have c1 := hb 1 (by omega)
  have c2 := hb 2 (by omega)
  have c3 := hb 3 (by omega)
  have e0 : output (V s).2 0 + 10 * carry (V s).2 1 = (V s).2 0 + carry (V s).2 0 :=
    column_equation (V s).2 0
  have e1 : output (V s).2 1 + 10 * carry (V s).2 2 = (V s).2 1 + carry (V s).2 1 :=
    column_equation (V s).2 1
  have e2 : output (V s).2 2 + 10 * carry (V s).2 3 = (V s).2 2 + carry (V s).2 2 :=
    column_equation (V s).2 2
  have o0 : output (V s).2 0 = 1 := by
    have := hdig 0 (by omega)
    simp only [extended, show 0 < (V s).1 by omega, if_true, famDigit_zero] at this
    exact this
  have o1 : output (V s).2 1 = 1 := by
    have := hdig 1 (by omega)
    simp only [extended, show 1 < (V s).1 by omega, if_true, famDigit_one] at this
    exact this
  have o2 : output (V s).2 2 = 0 := by
    have := hdig 2 (by omega)
    simp only [extended, show 2 < (V s).1 by omega, if_true,
      famDigit_mid 1 r 2 (by omega) (by omega)] at this
    exact this
  have cz : carry (V s).2 0 = 0 := rfl
  have qv1 := qv 1 (by omega)
  have qv2 := qv 2 (by omega)
  have hq1 : (V s).2 1 = 0 := by omega
  have hq2 : (V s).2 2 = 0 := by omega
  rw [wordPrefix_three, q0, hq1, hq2]

/-- A non-overflowing final step: same width, and the source pair word equals the
target digits. -/
theorem last_step_no_overflow (s d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9)
    (h : orbit 196 (s + 1) = fam d r) (hc : carry (V s).2 (V s).1 = 0) :
    (V s).1 = 2 * r + 4 ∧ ∀ i, i < 2 * r + 4 → (V s).2 i = famDigit d r i := by
  have hcan := next_digits_no_overflow s hc
  rw [h] at hcan
  obtain ⟨hw, hdig⟩ := canonical_unique hcan (fam_canonical d r hd1 hd9)
  refine ⟨hw, ?_⟩
  have hp : Palindrome (value (output (V s).2) (V s).1) := by
    rw [hcan.2.2.2]
    exact fam_palindrome d r hd1 hd9
  have hsym := (palindrome_value_iff (output (V s).2) (V s).1 hcan.2.1
    (Or.inr hcan.2.2.1)).mp hp
  obtain ⟨_, hpair⟩ := DecimalCarry.no_overflow_palindrome_has_no_carries (V s).1 (V s).2
    (carry (V s).2) (output (V s).2) (V_adm s).1 (V_adm s).2.2.2.1 hsym
    (fun i _ => column_equation (V s).2 i) rfl hc
  intro i hi
  exact (hpair i (by omega)).trans (hdig i (by omega))

#print axioms last_step_overflow
#print axioms last_step_no_overflow

/-! ## The step before the last one -/

theorem pow_hundred_mod11 (k : Nat) : 100 ^ k % 11 = 1 := by
  induction k with
  | zero => decide
  | succ k ih => rw [Nat.pow_succ, Nat.mul_mod, ih]

theorem pow_two_r_mod11 (r : Nat) : 10 ^ (2 * r + 2) % 11 = 1 := by
  rw [show 2 * r + 2 = 2 * (r + 1) by omega, Nat.pow_mul]
  exact pow_hundred_mod11 (r + 1)

/-- Residue of a sparse width-`2r+4` numeral modulo 11. -/
theorem value_sparse_mod11 (f : Nat → Nat) (r : Nat)
    (hz : ∀ i, 2 ≤ i → i ≤ 2 * r + 1 → f i = 0) :
    value f (2 * r + 4) % 11 =
      (f 0 + 10 * f 1 + f (2 * r + 2) + 10 * f (2 * r + 3)) % 11 := by
  rw [value_sparse f r hz, Nat.add_mod, Nat.mul_mod, pow_two_r_mod11, Nat.one_mul,
    Nat.mod_mod, ← Nat.add_mod]
  omega

/-- An overflow onto the penultimate term (whose pair word is the digit word of
`fam d r`) is possible only for `d = 2`, and then that term is `fam 1 r`. -/
theorem middle_overflow (s d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9) (hr : 1 ≤ r) (hs : 3 ≤ s)
    (hW : (V (s + 1)).1 = 2 * r + 4)
    (hq : ∀ i, i < 2 * r + 4 → (V (s + 1)).2 i = famDigit d r i)
    (hc : carry (V s).2 (V s).1 = 1) :
    d = 2 ∧ orbit 196 (s + 1) = fam 1 r := by
  have hcanM := next_digits_overflow s hc
  obtain ⟨e, he, hrep⟩ := V_rep (s + 1)
  obtain ⟨hwid, hdig⟩ := canonical_unique hcanM he
  have hLx : (V s).1 = 2 * r + 3 := by omega
  rw [hW] at he hrep
  -- digit facts of the penultimate term `e`
  have hpair : ∀ i, i < 2 * r + 4 → e i + e (2 * r + 4 - 1 - i) = famDigit d r i := by
    intro i hi
    rw [← hq i hi, ← hrep i hi]
    rfl
  have etop : e (2 * r + 3) = 1 := by
    have := hdig (2 * r + 3) (by omega)
    rw [← this]
    simp only [extended, hLx, Nat.lt_irrefl, if_false]
    rw [← hLx]
    exact hc
  have ebound := he.2.1
  have p0 := hpair 0 (by omega)
  have p1 := hpair 1 (by omega)
  rw [famDigit_zero, show 2 * r + 4 - 1 - 0 = 2 * r + 3 by omega] at p0
  rw [famDigit_one, show 2 * r + 4 - 1 - 1 = 2 * r + 2 by omega] at p1
  have einterior : ∀ i, 2 ≤ i → i ≤ 2 * r + 1 → e i = 0 := by
    intro i h2 hi
    have := hpair i (by omega)
    rw [famDigit_mid d r i h2 hi] at this
    omega
  -- divisibility by 11 of the penultimate term
  have h11 := orbit196_dvd11 (s + 1) (by omega)
  rw [← he.2.2.2] at h11
  have hmod := value_sparse_mod11 e r einterior
  have hm0 : value e (2 * r + 4) % 11 = 0 := Nat.mod_eq_zero_of_dvd h11
  have b0 := ebound 0 (by omega)
  have b1 := ebound 1 (by omega)
  have b2 := ebound (2 * r + 2) (by omega)
  have hm1 : e 1 = d - 1 := by omega
  have hm2 : e (2 * r + 2) = 1 := by omega
  -- column equations of the source pair word
  have hout : ∀ i, i < 2 * r + 3 → output (V s).2 i = e i := by
    intro i hi
    have := hdig i (by omega)
    simp only [extended, show i < (V s).1 by omega, if_true] at this
    exact this
  have hb := carry_bounded (V s).2 (V s).1 (V_adm s).2.2.1
  have hsym := (V_adm s).2.2.2.1
  have q0top : (V s).2 (2 * r + 2) = (V s).2 0 := by
    have := hsym 0 (by omega)
    rw [hLx, show 2 * r + 3 - 1 - 0 = 2 * r + 2 by omega] at this
    exact this.symm
  have col0 : output (V s).2 0 + 10 * carry (V s).2 1 = (V s).2 0 + carry (V s).2 0 :=
    column_equation (V s).2 0
  have coltop : output (V s).2 (2 * r + 2) + 10 * carry (V s).2 (2 * r + 3) =
      (V s).2 (2 * r + 2) + carry (V s).2 (2 * r + 2) := column_equation (V s).2 (2 * r + 2)
  have ctop : carry (V s).2 (2 * r + 3) = 1 := by rw [← hLx]; exact hc
  have c1 := hb 1 (by omega)
  have c2 := hb (2 * r + 2) (by omega)
  have cz : carry (V s).2 0 = 0 := rfl
  rw [hout 0 (by omega)] at col0
  rw [hout (2 * r + 2) (by omega), q0top, ctop] at coltop
  have hd2 : d ≤ 2 := by omega
  have hc1 : carry (V s).2 1 = 1 := by omega
  by_cases hd : d = 2
  · subst hd
    refine ⟨rfl, ?_⟩
    rw [← he.2.2.2]
    rw [show fam 1 r = value (famDigit 1 r) (2 * r + 4) from (fam_value 1 r).symm]
    apply value_congr
    intro i hi
    unfold famDigit
    split
    · rename_i hcase
      rcases hcase with h | h | h | h <;> subst h <;> omega
    · rename_i hcase
      exact einterior i (by omega) (by omega)
  · exfalso
    have hd1' : d = 1 := by
      clear hcanM he hrep hdig hpair hout hq hsym hb einterior hmod h11
      omega
    subst hd1'
    -- every column 1 .. 2r+1 has output digit 0 and incoming carry 1
    have hzero : ∀ i, 1 ≤ i → i ≤ 2 * r + 1 → output (V s).2 i = 0 := by
      intro i h1 hi
      rw [hout i (by omega)]
      by_cases hi1 : i = 1
      · subst hi1; omega
      · exact einterior i (by omega) hi
    have hcarry : ∀ k, k ≤ 2 * r → carry (V s).2 (k + 1) = 1 := by
      intro k hk
      induction k with
      | zero => exact hc1
      | succ k ih =>
        show carry (V s).2 (k + 2) = 1
        have ihk := ih (by omega)
        have col : output (V s).2 (k + 1) + 10 * carry (V s).2 (k + 2) =
            (V s).2 (k + 1) + carry (V s).2 (k + 1) := column_equation (V s).2 (k + 1)
        rw [hzero (k + 1) (by omega) (by omega), ihk] at col
        have := hb (k + 2) (by omega)
        omega
    have col : output (V s).2 (r + 1) + 10 * carry (V s).2 (r + 2) =
        (V s).2 (r + 1) + carry (V s).2 (r + 1) := column_equation (V s).2 (r + 1)
    rw [hzero (r + 1) (by omega) (by omega), hcarry (r + 1) (by omega),
      hcarry r (by omega)] at col
    have hcenter := (V_adm s).2.2.2.2 (r + 1) (by omega) (by omega)
    omega

#print axioms middle_overflow

/-- Without overflow the penultimate term has outer pair sum at least two, so the
digit word of `fam 1 r` (outer pair sum one) cannot be its pair word. -/
theorem middle_no_overflow_one (s : Nat)
    (hq0 : (V (s + 1)).2 0 = 1)
    (hc : carry (V s).2 (V s).1 = 0) : False := by
  have hcanM := next_digits_no_overflow s hc
  obtain ⟨e, he, hrep⟩ := V_rep (s + 1)
  obtain ⟨hwid, hdig⟩ := canonical_unique hcanM he
  have hW1 : (V (s + 1)).1 = (V s).1 := by rw [V_succ_fst]; simp [nextWidth, hc]
  have hL := (V_adm s).1
  have hpos := (V_adm s).2.1
  have hsym0 : (V s).2 0 = (V s).2 ((V s).1 - 1 - 0) := (V_adm s).2.2.2.1 0 hL
  have hb := carry_bounded (V s).2 (V s).1 (V_adm s).2.2.1
  have cL1 := hb ((V s).1 - 1) (by omega)
  have c1 := hb 1 (by omega)
  have colTop : output (V s).2 ((V s).1 - 1) + 10 * carry (V s).2 ((V s).1 - 1 + 1) =
      (V s).2 ((V s).1 - 1) + carry (V s).2 ((V s).1 - 1) := column_equation _ _
  rw [show (V s).1 - 1 + 1 = (V s).1 by omega, hc] at colTop
  have col0 : output (V s).2 0 + 10 * carry (V s).2 1 = (V s).2 0 + carry (V s).2 0 :=
    column_equation _ _
  have cz : carry (V s).2 0 = 0 := rfl
  have oTop := output_bounded (V s).2 ((V s).1 - 1)
  have o0 := output_bounded (V s).2 0
  -- the outer pair sum of the penultimate term
  have hpair0 : e 0 + e ((V s).1 - 1) = 1 := by
    have := hrep 0 (by omega)
    rw [hq0, hW1] at this
    simpa [columnSum, reflected] using this
  have he0 : e 0 = output (V s).2 0 := (hdig 0 hL).symm
  have heTop : e ((V s).1 - 1) = output (V s).2 ((V s).1 - 1) := (hdig _ (by omega)).symm
  rw [he0, heTop] at hpair0
  rw [Nat.sub_zero] at hsym0
  clear hcanM he hrep hdig
  omega

/-- Two non-overflowing additions onto an all-even target from carry state `(0,0)`:
the source is exactly half the target. -/
theorem noOverflow_half : ∀ {p s : List Nat} {x y : Nat},
    SevenColumn.NoOverflow p s x y → x = 0 → y = 0 →
      (∀ v ∈ p, v % 2 = 0 ∧ v ≤ 8) → s = p.map (· / 2) := by
  intro p s x y h
  induction h with
  | nil => intro _ _ _; rfl
  | @cons p s v a x y z ha hz hy hv tail ih =>
    intro hx hy0 hp
    subst hx
    subst hy0
    have hve := hp v List.mem_cons_self
    simp only [SevenColumn.carry, SevenColumn.lowDigit] at hy hv
    have hz0 : z = 0 := by omega
    have ha2 : a = v / 2 := by omega
    have hrest := ih (by simp only [SevenColumn.carry]; omega) hz0
      (fun w hw => hp w (List.mem_cons_of_mem _ hw))
    rw [hrest, ha2]
    rfl

theorem segment_mem {q : Nat → Nat} {start n v : Nat}
    (h : v ∈ segment q start n) : ∃ i, start ≤ i ∧ i < start + n ∧ q i = v := by
  rw [segment_eq_range_map] at h
  obtain ⟨i, hi, rfl⟩ := List.mem_map.mp h
  rw [List.mem_range'] at hi
  obtain ⟨k, hk, rfl⟩ := hi
  exact ⟨start + 1 * k, by omega, by omega, rfl⟩

/-- Even `d`, no overflow onto the penultimate term: that term is `fam (d/2) r`. -/
theorem middle_no_overflow_even (s d r : Nat) (hd1 : 1 ≤ d) (hd9 : d ≤ 9)
    (heven : d % 2 = 0)
    (hW : (V (s + 1)).1 = 2 * r + 4)
    (hq : ∀ i, i < 2 * r + 4 → (V (s + 1)).2 i = famDigit d r i)
    (hc : carry (V s).2 (V s).1 = 0) :
    orbit 196 (s + 1) = fam (d / 2) r := by
  have hW1 : (V (s + 1)).1 = (V s).1 := by rw [V_succ_fst]; simp [nextWidth, hc]
  have hLx : (V s).1 = 2 * r + 4 := by omega
  have hno := actual_noOverflow (V s).2 (V s).1 0 (V s).1 (V_adm s) (by omega) hc
  rw [Nat.sub_zero, hc, ← V_succ_snd] at hno
  have hhalf := noOverflow_half hno rfl rfl (by
    intro v hv
    obtain ⟨i, _, hi, rfl⟩ := segment_mem hv
    rw [hq i (by omega)]
    unfold famDigit
    split <;> omega)
  have hqi : ∀ i, i < 2 * r + 4 → (V s).2 i = famDigit d r i / 2 := by
    intro i hi
    have h1 := congrArg (fun l => l[i]?) hhalf
    simp only [segment_eq_range_map, List.map_map] at h1
    rw [List.getElem?_map, List.getElem?_map, List.getElem?_range' (by omega)] at h1
    simp only [Nat.zero_add, Option.map_some', Function.comp_apply, Nat.one_mul] at h1
    rw [hq i hi] at h1
    exact Option.some.inj h1
  have hsmall : ∀ i, i < 2 * r + 4 → (V s).2 i ≤ 4 := by
    intro i hi
    rw [hqi i hi]
    unfold famDigit
    split <;> omega
  have hcz : ∀ i, i ≤ 2 * r + 4 → carry (V s).2 i = 0 := by
    intro i
    induction i with
    | zero => intro _; rfl
    | succ i ih =>
      intro hi
      show ((V s).2 i + carry (V s).2 i) / 10 = 0
      rw [ih (by omega)]
      have := hsmall i (by omega)
      omega
  have hcan := next_digits_no_overflow s hc
  rw [← hcan.2.2.2, hLx, ← fam_value (d / 2) r]
  apply value_congr
  intro i hi
  show ((V s).2 i + carry (V s).2 i) % 10 = famDigit (d / 2) r i
  rw [hcz i (by omega), hqi i hi]
  unfold famDigit
  split <;> omega

#print axioms middle_no_overflow_one
#print axioms middle_no_overflow_even

/-! ## Short backward chains with no predecessor -/

theorem pred_11_0_0 : SevenColumn.prefixPredecessors [11, 0, 0] = [] := by decide

theorem pred_1_16 : SevenColumn.prefixPredecessors [1, 16] = [] := by decide

theorem noOverflowPred_7700 : SevenColumn.noOverflowPred [7, 7, 0, 0] 0 0 = [[3, 13, 9, 9]] := by
  decide

theorem pred_3_13_9_9 :
    ∀ w ∈ SevenColumn.prefixPredecessors [3, 13, 9, 9], w.take 2 = [1, 16] := by decide

/-- An overflow onto a palindrome of the class `d = 1`: the source prefix `[11,0,0]`
has no predecessor at all. -/
theorem no_pred_11_0_0 (s : Nat) (hs : 1 ≤ s) (h : wordPrefix (V s).2 3 = [11, 0, 0]) :
    False := by
  obtain ⟨s1, rfl⟩ : ∃ s1, s = s1 + 1 := ⟨s - 1, by omega⟩
  have hP := V_prefix_pred s1 3 (by decide) (V_width3 s1)
  rw [h, pred_11_0_0] at hP
  simp at hP

/-- `d = 7`, last two additions without overflow: three steps back the outer pair
sums would be `(1,16)`, which no addition produces. -/
theorem seven_chain (s r : Nat) (hr : 1 ≤ r) (hs : 3 ≤ s)
    (hW : (V (s + 1)).1 = 2 * r + 4)
    (hq : ∀ i, i < 2 * r + 4 → (V (s + 1)).2 i = famDigit 7 r i)
    (hc : carry (V s).2 (V s).1 = 0) : False := by
  have hW1 : (V (s + 1)).1 = (V s).1 := by rw [V_succ_fst]; simp [nextWidth, hc]
  have hno := actual_noOverflow (V s).2 (V s).1 0 4 (V_adm s) (by omega) hc
  rw [Nat.sub_zero, hc, ← V_succ_snd] at hno
  have htarget : segment (V (s + 1)).2 0 4 = [7, 7, 0, 0] := by
    show [(V (s + 1)).2 0, (V (s + 1)).2 1, (V (s + 1)).2 2, (V (s + 1)).2 3] = [7, 7, 0, 0]
    rw [hq 0 (by omega), hq 1 (by omega), hq 2 (by omega), hq 3 (by omega), famDigit_zero,
      famDigit_one, famDigit_mid 7 r 2 (by omega) (by omega),
      famDigit_mid 7 r 3 (by omega) (by omega)]
  rw [htarget, show carry (V s).2 0 = 0 from rfl] at hno
  have hmem := SevenColumn.NoOverflow.mem_noOverflowPred hno
  rw [noOverflowPred_7700, List.mem_singleton] at hmem
  obtain ⟨s1, rfl⟩ : ∃ s1, s = s1 + 1 := ⟨s - 1, by omega⟩
  have hY := V_prefix_pred s1 4 (by decide) (V_width4 s1 (by omega))
  have hX : wordPrefix (V (s1 + 1)).2 4 = [3, 13, 9, 9] := hmem
  rw [hX] at hY
  have hY2 : wordPrefix (V s1).2 2 = [1, 16] := by
    have := pred_3_13_9_9 _ hY
    rw [wordPrefix_four] at this
    rw [wordPrefix_two]
    simpa using this
  obtain ⟨s2, rfl⟩ : ∃ s2, s1 = s2 + 1 := ⟨s1 - 1, by omega⟩
  have hZ := V_prefix_pred s2 2 (by decide) (by have := V_width3 s2; omega)
  rw [hY2, pred_1_16] at hZ
  simp at hZ

/-! ## Reduction and the eight families -/

/-- If `fam d r` (with `r ≥ 1`) occurs at time `s+1 ≥ 5` for `d ∈ {1,2,4,7,8}`, then `d`
is even and `fam (d/2) r` occurs at time `s`. -/
theorem reduce (s d r : Nat) (hd : d = 1 ∨ d = 2 ∨ d = 4 ∨ d = 7 ∨ d = 8) (hr : 1 ≤ r)
    (hs : 4 ≤ s) (h : orbit 196 (s + 1) = fam d r) :
    d % 2 = 0 ∧ orbit 196 s = fam (d / 2) r := by
  have hd1 : 1 ≤ d := by omega
  have hd9 : d ≤ 9 := by omega
  rcases Nat.lt_or_ge (carry (V s).2 (V s).1) 1 with hc | hc
  · have hc0 : carry (V s).2 (V s).1 = 0 := by omega
    obtain ⟨hW, hq⟩ := last_step_no_overflow s d r hd1 hd9 h hc0
    obtain ⟨s1, rfl⟩ : ∃ s1, s = s1 + 1 := ⟨s - 1, by omega⟩
    rcases Nat.lt_or_ge (carry (V s1).2 (V s1).1) 1 with hc' | hc'
    · have hc0' : carry (V s1).2 (V s1).1 = 0 := by omega
      rcases hd with rfl | rfl | rfl | rfl | rfl
      · exact (middle_no_overflow_one s1 (by rw [hq 0 (by omega), famDigit_zero]) hc0').elim
      · exact ⟨rfl, middle_no_overflow_even s1 2 r (by decide) (by decide) rfl hW hq hc0'⟩
      · exact ⟨rfl, middle_no_overflow_even s1 4 r (by decide) (by decide) rfl hW hq hc0'⟩
      · exact (seven_chain s1 r hr (by omega) hW hq hc0').elim
      · exact ⟨rfl, middle_no_overflow_even s1 8 r (by decide) (by decide) rfl hW hq hc0'⟩
    · have hc1 : carry (V s1).2 (V s1).1 = 1 := by have := V_carry_le s1; omega
      obtain ⟨h2, hm⟩ := middle_overflow s1 d r hd1 hd9 hr (by omega) hW hq hc1
      subst h2
      exact ⟨rfl, hm⟩
  · have hc1 : carry (V s).2 (V s).1 = 1 := by have := V_carry_le s; omega
    obtain ⟨rfl, hpre⟩ := last_step_overflow s d r hd1 hd9 hr h hc1
    exact (no_pred_11_0_0 s (by omega) hpre).elim

theorem no_fam_one (t r : Nat) : orbit 196 t ≠ fam 1 r := by
  intro h
  obtain ⟨ht, hr⟩ := early_or_short 1 r t (by decide) (by decide) h
  obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
  have := (reduce s 1 r (Or.inl rfl) hr (by omega) h).1
  omega

theorem no_fam_two (t r : Nat) : orbit 196 t ≠ fam 2 r := by
  intro h
  obtain ⟨ht, hr⟩ := early_or_short 2 r t (by decide) (by decide) h
  obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
  exact no_fam_one s r (reduce s 2 r (by decide) hr (by omega) h).2

theorem no_fam_four (t r : Nat) : orbit 196 t ≠ fam 4 r := by
  intro h
  obtain ⟨ht, hr⟩ := early_or_short 4 r t (by decide) (by decide) h
  obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
  exact no_fam_two s r (reduce s 4 r (by decide) hr (by omega) h).2

theorem no_fam_eight (t r : Nat) : orbit 196 t ≠ fam 8 r := by
  intro h
  obtain ⟨ht, hr⟩ := early_or_short 8 r t (by decide) (by decide) h
  obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
  exact no_fam_four s r (reduce s 8 r (by decide) hr (by omega) h).2

theorem no_fam_seven (t r : Nat) : orbit 196 t ≠ fam 7 r := by
  intro h
  obtain ⟨ht, hr⟩ := early_or_short 7 r t (by decide) (by decide) h
  obtain ⟨s, rfl⟩ : ∃ s, t = s + 1 := ⟨t - 1, by omega⟩
  have := (reduce s 7 r (by decide) hr (by omega) h).1
  omega

theorem no_fam_mul3 (d t r : Nat) (hd : d % 3 = 0) : orbit 196 t ≠ fam d r := by
  intro h
  have h3 := orbit196_not_dvd3 t
  rw [h, fam_dvd3 d r hd] at h3
  exact h3 rfl

/-- **Main theorem.** For every `d ∈ {1,2,3,4,6,7,8,9}`, every `r` and every time `t`,
the orbit of 196 is not the palindrome `dd 0^(2r) dd = 11 * d * (10^(2r+2) + 1)`. -/
theorem orbit196_ne_fam (d r t : Nat)
    (hd : d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 ∨ d = 6 ∨ d = 7 ∨ d = 8 ∨ d = 9) :
    orbit 196 t ≠ fam d r := by
  rcases hd with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact no_fam_one t r
  · exact no_fam_two t r
  · exact no_fam_mul3 3 t r rfl
  · exact no_fam_four t r
  · exact no_fam_mul3 6 t r rfl
  · exact no_fam_seven t r
  · exact no_fam_eight t r
  · exact no_fam_mul3 9 t r rfl

/-- Digit form: no member of the 196 orbit has the canonical decimal digits
`d d 0^(2r) d d` (units first: `d, d, 0, …, 0, d, d`) for an allowed `d`. -/
theorem orbit196_digits_ne_fam (t d r : Nat)
    (hd : d = 1 ∨ d = 2 ∨ d = 3 ∨ d = 4 ∨ d = 6 ∨ d = 7 ∨ d = 8 ∨ d = 9)
    (e : Nat → Nat) (hcan : Canonical (orbit 196 t) e (2 * r + 4)) :
    ¬ ∀ i, i < 2 * r + 4 → e i = famDigit d r i := by
  intro he
  apply orbit196_ne_fam d r t hd
  rw [← hcan.2.2.2, ← fam_value d r]
  exact value_congr _ _ _ he

#print axioms no_pred_11_0_0
#print axioms seven_chain
#print axioms reduce
#print axioms orbit196_ne_fam
#print axioms orbit196_digits_ne_fam

end Agent119.EightFamilies
