import TwoDigitCert10
import TwoDigitCert20
import TwoDigitCert32
import TwoDigitCert40
import TwoDigitCert41
import TwoDigitCert60
import TwoDigitCert64
import TwoDigitCert65
import TwoDigitCert76
import TwoDigitCert80
import TwoDigitCert81
import TwoDigitCert82
import TwoDigitCert83

/-!
# Agent #113: thirteen two-digit palindrome prefixes, endpoints

Kernel formalization of the written "thirteen prefix theorem"
(`proofs/chat-6acee928/originals/p196_thirteen_prefix_theorem.md`).

For each prefix `ab` and bound `h` in

  10:1, 20:2, 32:2, 40:3, 41:3, 60:3, 64:3, 76:3, 80:4, 81:4, 82:4, 83:4, 65:6

every palindrome `P` whose decimal numeral begins with the digits `a, b`
satisfies: for every positive `A` and every `t`, `orbit A t = P` implies
`t ≤ h` (`ancestry_bound_ab`, in the certificate modules). Width and interior
digits are arbitrary; intermediate palindromes are allowed.

This module adds

* `startsTwo_iff`: the canonical-numeral prefix predicate equals the plain
  arithmetic statement `∃ k, P / 10 ^ k = 10 * a + b` (with `1 ≤ a ≤ 9`,
  `b ≤ 9`), so the endpoints can be read without the digit machinery;
* `no_196_thirteen`: no state `orbit 196 t`, at any time `t`, is a palindrome
  beginning with any of the thirteen prefixes;
* `sharp_*`: each bound is attained at a first palindrome (the written
  witnesses), so the thirteen bounds are exact.

This is a restricted-family exclusion. It does not prove that 196 is a
Lychrel number, and it says nothing about palindromes with other prefixes.
-/

namespace Agent113.TwoDigit

open DecimalDigits Lychrel196

/-! ## Arithmetic reading of the prefix predicate -/

theorem value_lt (d : Nat → Nat) (L : Nat) (hd : ∀ i, i < L → d i ≤ 9) :
    value d L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have h1 := ih (fun i hi => hd i (by omega))
    have h2 := hd L (by omega)
    simp only [value, Nat.pow_succ]
    have h3 : d L * 10 ^ L ≤ 9 * 10 ^ L := Nat.mul_le_mul_right _ h2
    omega

theorem value_digitAt (n L : Nat) : value (digitAt n) L = n % 10 ^ L := by
  induction L with
  | zero => simp [value, Nat.mod_one]
  | succ L ih =>
    simp only [value, ih, digitAt, Nat.mod_pow_succ]
    rw [Nat.mul_comm]

theorem startsTwo_iff (a b P : Nat) :
    StartsTwo a b P ↔ 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9 ∧ ∃ k, P / 10 ^ k = 10 * a + b := by
  constructor
  · rintro ⟨e, W, hcan, hW, hea, heb⟩
    have hdig := canonical_digitAt hcan
    have hlt : P < 10 ^ W := by
      rw [← hcan.2.2.2]; exact value_lt e W hcan.2.1
    have ha1 : 1 ≤ a := by rw [← hea]; exact hcan.2.2.1
    have ha9 : a ≤ 9 := by rw [← hea]; exact hcan.2.1 _ (by omega)
    have hb9 : b ≤ 9 := by rw [← heb]; exact hcan.2.1 _ (by omega)
    refine ⟨ha1, ha9, hb9, W - 2, ?_⟩
    have hda := hdig (W - 1) (by omega)
    have hdb := hdig (W - 2) (by omega)
    simp only [digitAt] at hda hdb
    rw [hea] at hda
    rw [heb] at hdb
    have hpow1 : 10 ^ (W - 1) = 10 ^ (W - 2) * 10 := by
      rw [← Nat.pow_succ]; congr 1; omega
    have hpow2 : 10 ^ W = 10 ^ (W - 2) * (10 * 10) := by
      rw [← Nat.mul_assoc, ← Nat.pow_succ, ← Nat.pow_succ]; congr 1; omega
    have hq1 : P / 10 ^ (W - 1) = P / 10 ^ (W - 2) / 10 := by
      rw [hpow1, Nat.div_div_eq_div_mul]
    have hq2 : P / 10 ^ (W - 2) / 10 / 10 = 0 := by
      rw [Nat.div_div_eq_div_mul, Nat.div_div_eq_div_mul, ← hpow2]
      exact Nat.div_eq_of_lt hlt
    rw [hq1] at hda
    omega
  · rintro ⟨ha1, ha9, hb9, k, hk⟩
    have hpos : 0 < 10 ^ k := Nat.pow_pos (by decide)
    have hlt : P < 10 ^ (k + 2) := by
      have : P / 10 ^ k < 100 := by omega
      rw [Nat.div_lt_iff_lt_mul hpos] at this
      rw [Nat.pow_add]
      omega
    have hk1 : P / 10 ^ (k + 1) = a := by
      rw [Nat.pow_succ, ← Nat.div_div_eq_div_mul, hk]
      omega
    refine ⟨digitAt P, k + 2, ⟨by omega, ?_, ?_, ?_⟩, by omega, ?_, ?_⟩
    · intro i _; simp only [digitAt]; omega
    · show 0 < P / 10 ^ (k + 2 - 1) % 10
      rw [show k + 2 - 1 = k + 1 by omega, hk1]
      omega
    · rw [value_digitAt]; exact Nat.mod_eq_of_lt hlt
    · show P / 10 ^ (k + 2 - 1) % 10 = a
      rw [show k + 2 - 1 = k + 1 by omega, hk1]
      omega
    · show P / 10 ^ (k + 2 - 2) % 10 = b
      rw [show k + 2 - 2 = k by omega, hk]
      omega

/-! ## The 196 corollaries -/

theorem no_196 (a b h : Nat) (hh : h ≤ 100)
    (hbound : ∀ A P t, 0 < A → PalindromeStartsTwo a b P → orbit A t = P → t ≤ h) :
    ∀ t, ¬ PalindromeStartsTwo a b (orbit 196 t) :=
  SevenColumnKernel.PalindromeBridge.no_196_target_of_ancestry_bound
    (PalindromeStartsTwo a b) h hh (fun _ hP => hP.1) hbound

/-- The thirteen prefixes, as `(a, b)` digit pairs. -/
def thirteenPrefixes : List (Nat × Nat) :=
  [(1, 0), (2, 0), (3, 2), (4, 0), (4, 1), (6, 0), (6, 4), (6, 5), (7, 6),
   (8, 0), (8, 1), (8, 2), (8, 3)]

/-- The orbit of 196 never contains, at any time, a palindrome whose decimal
numeral begins with one of the thirteen prefixes. -/
theorem no_196_thirteen :
    ∀ t, ∀ ab ∈ thirteenPrefixes, ¬ PalindromeStartsTwo ab.1 ab.2 (orbit 196 t) := by
  intro t ab hab
  simp only [thirteenPrefixes, List.mem_cons, List.mem_nil_iff, or_false] at hab
  rcases hab with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl
  · exact no_196 1 0 1 (by decide) ancestry_bound_10 t
  · exact no_196 2 0 2 (by decide) ancestry_bound_20 t
  · exact no_196 3 2 2 (by decide) ancestry_bound_32 t
  · exact no_196 4 0 3 (by decide) ancestry_bound_40 t
  · exact no_196 4 1 3 (by decide) ancestry_bound_41 t
  · exact no_196 6 0 3 (by decide) ancestry_bound_60 t
  · exact no_196 6 4 3 (by decide) ancestry_bound_64 t
  · exact no_196 6 5 6 (by decide) ancestry_bound_65 t
  · exact no_196 7 6 3 (by decide) ancestry_bound_76 t
  · exact no_196 8 0 4 (by decide) ancestry_bound_80 t
  · exact no_196 8 1 4 (by decide) ancestry_bound_81 t
  · exact no_196 8 2 4 (by decide) ancestry_bound_82 t
  · exact no_196 8 3 4 (by decide) ancestry_bound_83 t

/-- Arithmetic form: for every time `t` and every `k`, if `orbit 196 t` is
a palindrome then `orbit 196 t / 10 ^ k` is not one of the thirteen
two-digit numbers. -/
theorem no_196_thirteen_arith (t k : Nat) (hpal : Palindrome (orbit 196 t)) :
    orbit 196 t / 10 ^ k ∉ [10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83] := by
  intro hmem
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hmem
  have go : ∀ a b, (a, b) ∈ thirteenPrefixes → 1 ≤ a → a ≤ 9 → b ≤ 9 →
      orbit 196 t / 10 ^ k = 10 * a + b → False := fun a b hab h1 h2 h3 hk =>
    no_196_thirteen t (a, b) hab ⟨hpal, (startsTwo_iff a b _).mpr ⟨h1, h2, h3, k, hk⟩⟩
  rcases hmem with h | h | h | h | h | h | h | h | h | h | h | h | h
  · exact go 1 0 (by decide) (by decide) (by decide) (by decide) h
  · exact go 2 0 (by decide) (by decide) (by decide) (by decide) h
  · exact go 3 2 (by decide) (by decide) (by decide) (by decide) h
  · exact go 4 0 (by decide) (by decide) (by decide) (by decide) h
  · exact go 4 1 (by decide) (by decide) (by decide) (by decide) h
  · exact go 6 0 (by decide) (by decide) (by decide) (by decide) h
  · exact go 6 4 (by decide) (by decide) (by decide) (by decide) h
  · exact go 6 5 (by decide) (by decide) (by decide) (by decide) h
  · exact go 7 6 (by decide) (by decide) (by decide) (by decide) h
  · exact go 8 0 (by decide) (by decide) (by decide) (by decide) h
  · exact go 8 1 (by decide) (by decide) (by decide) (by decide) h
  · exact go 8 2 (by decide) (by decide) (by decide) (by decide) h
  · exact go 8 3 (by decide) (by decide) (by decide) (by decide) h

/-! ## Sharpness: every bound is attained at a first palindrome -/

/-- `orbit R h` is a palindrome beginning with `a, b`, and no earlier state
is a palindrome. -/
def SharpAt (a b R h k : Nat) : Prop :=
  PalindromeStartsTwo a b (orbit R h) ∧ (∀ j, j < h → ¬ Palindrome (orbit R j)) ∧
    orbit R h / 10 ^ k = 10 * a + b

theorem sharp_of_checks (a b R h k : Nat)
    (ha : 1 ≤ a ∧ a ≤ 9 ∧ b ≤ 9)
    (hk : orbit R h / 10 ^ k = 10 * a + b) (hpal : Palindrome (orbit R h))
    (hfirst : ∀ j, j < h → ¬ Palindrome (orbit R j)) : SharpAt a b R h k :=
  ⟨⟨hpal, (startsTwo_iff a b _).mpr ⟨ha.1, ha.2.1, ha.2.2, k, hk⟩⟩, hfirst, hk⟩

theorem sharp_10 : SharpAt 1 0 100 1 1 :=
  sharp_of_checks 1 0 100 1 1 (by decide) (by decide) (by decide) (by decide)
theorem sharp_20 : SharpAt 2 0 1005000 2 5 :=
  sharp_of_checks 2 0 1005000 2 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_32 : SharpAt 3 2 12090 2 3 :=
  sharp_of_checks 3 2 12090 2 3 (by decide) (by decide) (by decide) (by decide)
theorem sharp_40 : SharpAt 4 0 1008000 3 5 :=
  sharp_of_checks 4 0 1008000 3 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_41 : SharpAt 4 1 1008400 3 5 :=
  sharp_of_checks 4 1 1008400 3 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_60 : SharpAt 6 0 1103090 3 5 :=
  sharp_of_checks 6 0 1103090 3 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_64 : SharpAt 6 4 1203090 3 5 :=
  sharp_of_checks 6 4 1203090 3 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_65 : SharpAt 6 5 1203290 6 6 :=
  sharp_of_checks 6 5 1203290 6 6 (by decide) (by decide) (by decide) (by decide)
theorem sharp_76 : SharpAt 7 6 17590 3 3 :=
  sharp_of_checks 7 6 17590 3 3 (by decide) (by decide) (by decide) (by decide)
theorem sharp_80 : SharpAt 8 0 1009000 4 5 :=
  sharp_of_checks 8 0 1009000 4 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_81 : SharpAt 8 1 1009200 4 5 :=
  sharp_of_checks 8 1 1009200 4 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_82 : SharpAt 8 2 1006500 4 5 :=
  sharp_of_checks 8 2 1006500 4 5 (by decide) (by decide) (by decide) (by decide)
theorem sharp_83 : SharpAt 8 3 1009400 4 5 :=
  sharp_of_checks 8 3 1009400 4 5 (by decide) (by decide) (by decide) (by decide)

#print axioms startsTwo_iff
#print axioms no_196_thirteen
#print axioms no_196_thirteen_arith
#print axioms sharp_10
#print axioms sharp_20
#print axioms sharp_32
#print axioms sharp_40
#print axioms sharp_41
#print axioms sharp_60
#print axioms sharp_64
#print axioms sharp_65
#print axioms sharp_76
#print axioms sharp_80
#print axioms sharp_81
#print axioms sharp_82
#print axioms sharp_83

end Agent113.TwoDigit
