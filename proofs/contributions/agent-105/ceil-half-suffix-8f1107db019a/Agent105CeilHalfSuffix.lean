import GrowingSuffix

/-!
WIP target for the odd-center boundary of exact decimal palindrome suffix
realization. This file states the intended universal property and begins
the symmetry extension; it does not claim a complete proof.
-/

namespace Agent105.CeilHalfSuffix

open Lychrel196 DecimalDigits ExactLengthResidues

/-- Every nonzero-units integer admits an exact-width positive canonical
palindrome with the same residue modulo 10^k. -/
def UniversalSuffixRealization (k L : Nat) : Prop :=
  ∀ n : Nat, ¬ 10 ∣ n →
    ∃ P : Nat, ∃ e : Nat → Nat, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧
      P % (10 ^ k) = n % (10 ^ k)

/-- Candidate sharp range: a prescribed suffix can occupy at most the
low half plus the one shared odd center digit. -/
def CeilHalfRange (k L : Nat) : Prop :=
  0 < k ∧ 2 * k ≤ L + 1

/-- The mirrored outer-digit function remains symmetric when the two
prescribed blocks meet at the unique center position. -/
theorem outerDigits_symmetric_ceil (d : Nat → Nat) (k L i : Nat)
    (hL : 2 * k ≤ L + 1) (hi : i < L) :
    outerDigits d k L i = outerDigits d k L (L - 1 - i) := by
  have hinv : L - 1 - (L - 1 - i) = i := by omega
  simp only [outerDigits, hinv]
  by_cases ha : i < k
  · by_cases hb : L - 1 - i < k
    · have hcenter : i = L - 1 - i := by omega
      simp only [if_pos ha, if_pos hb]
      exact congrArg d hcenter
    · simp only [if_pos ha, if_neg hb]
  · by_cases hb : L - 1 - i < k
    · simp only [if_neg ha, if_pos hb]
    · simp only [if_neg ha, if_neg hb]


/-- Canonicality of the mirrored outer digits also holds at the one-center
overlap boundary. The only case not covered by k<L is the one-digit word. -/
theorem outerDigits_canonical_ceil (d : Nat → Nat) (k L : Nat)
    (hk : 0 < k) (hL : 2 * k ≤ L + 1)
    (hd : ∀ i, i < k → d i ≤ 9) (hd0 : 0 < d 0) :
    Canonical (value (outerDigits d k L) L) (outerDigits d k L) L := by
  by_cases hLone : L = 1
  · subst L
    have hkone : k = 1 := by omega
    subst k
    refine ⟨by decide, ?_, ?_, rfl⟩
    · intro i hi
      have hi0 : i = 0 := by omega
      subst i
      simpa [outerDigits] using hd 0 (by omega)
    · simpa [outerDigits] using hd0
  · have hkL : k < L := by omega
    refine ⟨by omega, ?_, ?_, rfl⟩
    · intro i hi
      by_cases ha : i < k
      · simpa [outerDigits, ha] using hd i ha
      · by_cases hb : L - 1 - i < k
        · simpa [outerDigits, ha, hb] using hd (L - 1 - i) hb
        · simp [outerDigits, ha, hb]
    · have ha : ¬ L - 1 < k := by omega
      have hb : L - 1 - (L - 1) = 0 := by omega
      rw [outerDigits, if_neg ha, hb, if_pos (by omega : 0 < k)]
    exact hd0

/-- The exact-width outer-digit construction is an ordinary integer
palindrome at the full low-half boundary, including the odd center. -/
theorem outerValue_palindrome_ceil (A k L : Nat) (hk : 0 < k)
    (hL : 2 * k ≤ L + 1) (hA0 : A % 10 ≠ 0) :
    Palindrome (value (outerDigits (paddedDigits A) k L) L) := by
  have hc := outerDigits_canonical_ceil (paddedDigits A) k L hk hL
    (fun i _ => paddedDigits_bound A i)
    (by simpa [paddedDigits] using Nat.pos_of_ne_zero hA0)
  apply (palindrome_value_iff (outerDigits (paddedDigits A) k L) L
    hc.2.1 (Or.inr hc.2.2.1)).mpr
  intro i hi
  exact outerDigits_symmetric_ceil (paddedDigits A) k L i hL hi

/-- WIP strengthening of Agent111's suffix realization: the single shared
center digit is permitted. The proof reuses the original low-modulus lemma
and the generalized outer-digit construction above. -/
theorem palindrome_with_given_suffix_ceil (n k L : Nat)
    (hk : 0 < k) (hL : 2 * k ≤ L + 1) (hunit : ¬ 10 ∣ n) :
    ∃ P e, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧
      P % (10 ^ k) = n % (10 ^ k) := by
  let A := n % (10 ^ k)
  let ds := outerDigits (paddedDigits A) k L
  let P := value ds L
  have hA : A < 10 ^ k := Nat.mod_lt n (Nat.pow_pos (by decide))
  have hten : 10 ∣ 10 ^ k := ten_dvd_pow k (by omega)
  have hA0 : A % 10 ≠ 0 := by
    change n % (10 ^ k) % 10 ≠ 0
    rw [Nat.mod_mod_of_dvd n hten]
    intro hz
    exact hunit (Nat.dvd_of_mod_eq_zero hz)
  have hkL : k ≤ L := by omega
  have hc : Canonical P ds L := by
    simpa [P, ds] using outerDigits_canonical_ceil (paddedDigits A) k L
      hk hL (fun i _ => paddedDigits_bound A i)
      (by simpa [paddedDigits] using Nat.pos_of_ne_zero hA0)
  have hp : Palindrome P := by
    simpa [P, ds] using outerValue_palindrome_ceil A k L hk hL hA0
  have hPpos : 0 < P := by
    rw [← hc.2.2.2]
    exact value_positive ds L hc.1 hc.2.2.1
  have hlow : LowerPositions k L ([] : List Nat) := by
    intro i hi
    simp at hi
  have hmod := realizedDigits_mod_outer (paddedDigits A) k L (10 ^ k) []
    hkL (⟨1, by simp⟩) hlow
  rw [paddedDigits_value A k hA] at hmod
  have hres : P % (10 ^ k) = A := by
    simpa [P, ds, realizedDigits, pairDigits, selectedDigit,
      Nat.mod_eq_of_lt hA] using hmod
  refine ⟨P, ds, hPpos, hc, hp, ?_⟩
  simpa [A, Nat.mod_eq_of_lt hA] using hres


/-- A width-k digit vector with decimal digits represents a value below
10^k. This helper is needed to recover individual low digits from a residue. -/
theorem value_lt_pow10 (d : Nat → Nat) (k : Nat)
    (hd : ∀ i, i < k → d i ≤ 9) :
    value d k < 10 ^ k := by
  induction k generalizing d with
  | zero => simp [value]
  | succ k ih =>
    rw [value_shift]
    have h0 : d 0 ≤ 9 := hd 0 (by omega)
    have ht : value (fun i => d (i + 1)) k < 10 ^ k :=
      ih (fun i => d (i + 1)) (fun i hi => hd (i + 1) (by omega))
    simp only [Nat.pow_succ]
    omega

/-- If a canonical L-digit value agrees with n modulo 10^k and k≤L,
then its first k low-to-high digits are exactly the digits of n. -/
theorem lowDigits_eq_of_mod_eq (P n k L : Nat) (e : Nat → Nat)
    (hcan : Canonical P e L) (hkL : k ≤ L) (hn : n < 10 ^ k)
    (hmod : P % (10 ^ k) = n) :
    ∀ i, i < k → e i = paddedDigits n i := by
  have hlow : ∀ i, i < k → e i = truncateDigits e k i := by
    intro i hi
    simp [truncateDigits, hi]
  have hmodE := value_mod_eq_of_low_eq e (truncateDigits e k) k L
    (10 ^ k) (⟨1, by simp⟩) hlow
  rw [truncateDigits_value e k L hkL] at hmodE
  rw [hcan.2.2.2] at hmodE
  rw [hmod] at hmodE
  have hbound : value e k < 10 ^ k :=
    value_lt_pow10 e k (fun i hi => hcan.2.1 i (by omega))
  rw [Nat.mod_eq_of_lt hbound] at hmodE
  have hval : value e k = value (paddedDigits n) k := by
    calc
      value e k = n := hmodE.symm
      _ = value (paddedDigits n) k := (paddedDigits_value n k hn).symm
  have hdigits := value_injective e (paddedDigits n) k
    (fun i hi => hcan.2.1 i (by omega))
    (fun i hi => paddedDigits_bound n i) hval
  exact hdigits

/-- Converse obstruction target. When the suffix is longer than the low
half plus center, exhibit one nonzero-units input that no exact-width
palindrome can realize. This remains unproved. -/
def ConverseObstruction (k L : Nat) : Prop :=
  2 * k > L + 1 →
    ∃ n : Nat, ¬ 10 ∣ n ∧
      ∀ P : Nat, ∀ e : Nat → Nat, Canonical P e L → Palindrome P →
        P % (10 ^ k) ≠ n % (10 ^ k)

/-- Candidate witness used in the converse: n=1+2*10^(k-1). For k≤L,
the forced mirrored positions L-k and k-1 disagree; for k>L,
the witness itself is too large to be an exact-L-digit canonical P.
This explanation is not yet a Lean proof. -/
def ProposedConverseWitness (k : Nat) : Nat :=
  1 + 2 * 10 ^ (k - 1)

/-- Unproved research target. This is deliberately a proposition definition,
not an accepted theorem. A counterexample must be preserved if the proposed
converse is false under the exact original Canonical/Palindrome semantics. -/
def UniversalSuffixRealizationIffCeilHalf : Prop :=
  ∀ k L : Nat, 0 < k →
    (UniversalSuffixRealization k L ↔ 2 * k ≤ L + 1)

end Agent105.CeilHalfSuffix
