import Saturation

/-!
Agent #111: unbounded width-dependent decimal suffix congruence obstruction.

For any sufficiently long exact decimal width L, allow a modulus 10^(k L)
that can grow exponentially with L, but with k L <= (L-4)/2.
The original decimal orbit and exact-length saturation proofs are imported
unchanged. This does not prove that any particular orbit hits a palindrome.
-/

namespace Agent111.GrowingSuffix

open Lychrel196 DecimalDigits ExactLengthResidues

/-- At any specified width L with 1 <= k and 2*k+4 <= L, every residue
compatible with a true palindrome has a same-width palindrome modulo 10^k.
This specializes the *existing* arbitrary-modulus theorem at u=10^k,
q=1, r=1; no unproved arithmetic assumption remains. -/
theorem powerTen_saturation (k : Nat) (hk : 1 <= k) :
    SaturationAbove (10 ^ k) (2*k+4) := by
  apply saturation_of_split (10 ^ k) k (10 ^ k) 1 1 hk
  · exact Nat.pow_pos (by decide)
  · decide
  · simp
  · exact ⟨1, by simp⟩
  · simp
  · decide
  · simp

/-- If the suffix modulus is a power of ten with exponent at most almost
half the available width, forward closure forces *some member of the set*
to be an ordinary decimal palindrome. The orbit used to transfer membership
is not claimed to contain that palindrome. -/
theorem variable_powerTen_closed_set_contains_palindrome
    (S : Nat -> Prop) (k : Nat -> Nat) (B : Nat)
    (hwidth : ∀ L, B <= L -> 1 <= k L ∧ 2*(k L)+4 <= L)
    (hsat : ∀ L, B <= L -> ∀ n m (d e : Nat -> Nat),
      Canonical n d L -> Canonical m e L ->
      n % (10 ^ (k L)) = m % (10 ^ (k L)) -> (S n ↔ S m))
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  obtain ⟨n, hn, hnS⟩ := hne
  obtain ⟨t, d, L, _, _, hc, hL, h11, h10⟩ :=
    AstraModular.large_width_compatible_state n (max B 6) hn
  have hLB : B <= L := Nat.le_trans (Nat.le_max_left B 6) hL
  have hk : 1 <= k L := (hwidth L hLB).1
  have hbound : 2*(k L)+4 <= L := (hwidth L hLB).2
  have hcompatible : Compatible (10 ^ (k L)) L (orbit n t) := by
    constructor
    · intro h
      exact h10 h.2
    · intro _
      exact Nat.dvd_trans (Nat.gcd_dvd_right (10 ^ (k L)) 11) h11
  obtain ⟨p, e, hp, hpc, hpal, hcong⟩ :=
    (powerTen_saturation (k L) hk) L hbound (orbit n t) hcompatible
  have hmem : ∀ j, S (orbit n j) := by
    intro j
    induction j with
    | zero => exact hnS
    | succ j ih => exact hclosed (orbit n j) (orbit_positive n hn j) ih
  refine ⟨p, hp, ?_, hpal⟩
  exact (hsat L hLB (orbit n t) p d e hc hpc hcong.symm).mp (hmem t)

/-- An explicit unbounded schedule: at width L>=6, membership depends
only on the last floor((L-4)/2) decimal digits, plus the exact width.
No fixed modulus can replace this schedule for all large L. -/
theorem half_width_suffix_closed_set_contains_palindrome
    (S : Nat -> Prop)
    (hsat : ∀ L, 6 <= L -> ∀ n m (d e : Nat -> Nat),
      Canonical n d L -> Canonical m e L ->
      n % (10 ^ ((L - 4) / 2)) = m % (10 ^ ((L - 4) / 2)) ->
      (S n ↔ S m))
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n -> S n -> S (step n)) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  apply variable_powerTen_closed_set_contains_palindrome
    S (fun L => (L - 4) / 2) 6
  · intro L hL
    constructor <;> omega
  · exact hsat
  · exact hne
  · exact hclosed

end Agent111.GrowingSuffix

#print axioms Agent111.GrowingSuffix.powerTen_saturation
#print axioms Agent111.GrowingSuffix.variable_powerTen_closed_set_contains_palindrome
#print axioms Agent111.GrowingSuffix.half_width_suffix_closed_set_contains_palindrome
