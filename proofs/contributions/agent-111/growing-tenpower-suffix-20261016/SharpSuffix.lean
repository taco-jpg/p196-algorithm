import GrowingSuffix

/-! Ordinary decimal palindrome realization with a prescribed low-order half.
The modulus 10^k is allowed up to k=floor(L/2), without the 4-digit
padding required by general arbitrary-modulus residue saturation. -/

namespace Agent111.GrowingSuffix

open Lychrel196 DecimalDigits ExactLengthResidues

/-- Every positive-width decimal residue whose units digit is nonzero can
be completed to an ordinary positive palindrome of exact width L, whenever
2*k<=L. We reuse the *checked* original constructive realization with
empty inner digit pools, not a search over finite examples. -/
theorem palindrome_with_given_suffix (n k L : Nat)
    (hk : 0 < k) (hL : 2 * k <= L) (hunit : ¬ 10 ∣ n) :
    ∃ P e, 0 < P ∧ Canonical P e L ∧ Palindrome P ∧
      P % (10 ^ k) = n % (10 ^ k) := by
  let A := n % (10 ^ k)
  have hA : A < 10 ^ k := Nat.mod_lt n (Nat.pow_pos (by decide))
  have hten : 10 ∣ 10 ^ k := ten_dvd_pow k (by omega)
  have hA0 : A % 10 ≠ 0 := by
    change n % (10 ^ k) % 10 ≠ 0
    rw [Nat.mod_mod_of_dvd n hten]
    intro hzero
    exact hunit (Nat.dvd_of_mod_eq_zero hzero)
  have hlow : LowerPositions k L ([] : List Nat) := by
    intro i hi
    simp at hi
  obtain ⟨P, e, hc, hp, hmod, _⟩ :=
    two_pool_realization A k L (10 ^ k) 1 0 0 ([] : List Nat) ([] : List Nat)
      hk hL hA hA0 (⟨1, by simp⟩) (by simp) hlow (by simp) (by simp)
  have hPpos : 0 < P := by
    rw [← hc.2.2.2]
    exact value_positive e L hc.1 hc.2.2.1
  refine ⟨P, e, hPpos, hc, hp, ?_⟩
  simpa only [A, Nat.mod_mod] using hmod

/-- Every eventually exact-width, trailing-k(L)-digit saturated, nonempty
positive reverse-add forward-closed set has a positive palindrome, even if
k(L) grows without any uniform bound, provided 2*k(L)<=L. -/
theorem variable_half_suffix_closed_set_contains_palindrome
    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)
    (hwidth : ∀ L, B <= L -> 0 < k L ∧ 2*(k L) <= L)
    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),
      Canonical n d L -> Canonical m e L ->
      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  obtain ⟨n, hn, hnS⟩ := hne
  obtain ⟨t, d, L, _, _, hc, hL, _, h10⟩ :=
    AstraModular.large_width_compatible_state n (max B 6) hn
  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL
  have hk : 0 < k L := (hwidth L hLB).1
  have hbound : 2 * (k L) <= L := (hwidth L hLB).2
  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=
    palindrome_with_given_suffix (orbit n t) (k L) L hk hbound h10
  have hmem : ∀ j, S (orbit n j) := by
    intro j
    induction j with
    | zero => exact hnS
    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih
  refine ⟨p, hp, ?_, hpal⟩
  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)

/-- The entire low half may be retained: at every exact width L>=6,
S depends only on L and n mod 10^(floor(L/2)). This unbounded modulus
is strictly stronger than the previous (L-4)/2 exponent. -/
theorem exact_half_suffix_closed_set_contains_palindrome
    (S : Nat -> Prop)
    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),
      Canonical n d L -> Canonical m e L ->
      n % (10 ^ (L / 2)) = m % (10 ^ (L / 2)) -> (S n ↔ S m))
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  apply variable_half_suffix_closed_set_contains_palindrome
    S (fun L => L / 2) 6
  · intro L hL
    constructor <;> omega
  · exact hsat
  · exact hne
  · exact hclosed

end Agent111.GrowingSuffix

#print axioms Agent111.GrowingSuffix.palindrome_with_given_suffix
#print axioms Agent111.GrowingSuffix.variable_half_suffix_closed_set_contains_palindrome
#print axioms Agent111.GrowingSuffix.exact_half_suffix_closed_set_contains_palindrome
