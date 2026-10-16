import ModularAutonomy
import ResiduePalindromes

/-! A restricted arithmetic-invariant obstruction. A constructed palindrome
shares a sufficiently late actual orbit state's exact width and residue;
the theorem does not say that the orbit reaches that palindrome. -/

namespace Agent105.ResidueTrap

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  Agent105.ResiduePalindromes

/-- An even-width, eleven-divisible actual state occurs within this
explicit window, beyond any prescribed width. -/
theorem large_even_dvd11_state (n B : Nat) (hn : 0 < n) :
    ∃ t d L, 6 + 4 * B ≤ t ∧ t ≤ 11 + 4 * B ∧
      Canonical (orbit n t) d L ∧ B ≤ L ∧ L % 2 = 0 ∧ 11 ∣ orbit n t := by
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  let start := 6 + 4 * B
  obtain ⟨e, W, he, hg, _⟩ := DecimalWidthGrowth.numeric_width_bounds n d L start hc
  have ha := NormalizationBridge.canonical_admissible (orbit n start) e W he
  obtain ⟨k, hk, hev⟩ := AstraModular.exists_even_width_by_five (columnSum e W) W ha
  obtain ⟨f, hf, _⟩ := iterPairs_representation (orbit n start) e
    (columnSum e W) W k he (fun _ _ => rfl)
  have hw := DecimalWidthGrowth.width_lower_bound (columnSum e W) W k ha
  have hL := hc.1
  have hbound : B ≤ (iterPairs (columnSum e W) W k).1 := by
    dsimp [start] at hg
    omega
  rw [← LychrelCertificates.orbit_add] at hf
  refine ⟨start + k, f, (iterPairs (columnSum e W) W k).1,
    by dsimp [start]; omega, by dsimp [start]; omega,
    hf, hbound, hev, ?_⟩
  apply Nat.dvd_of_mod_eq_zero
  exact AstraModular.orbit_mod11_eq_zero_of_six_le n (start + k) hn
    (by dsimp [start]; omega)

/-- Quantitative matching with a positive ordinary palindrome. The input
state and palindrome have the same exact width and residue modulo M. -/
theorem orbit_matches_palindrome_of_dvd99 (M n B : Nat)
    (hM : M ∣ 99) (hn : 0 < n) :
    ∃ t p d e L, 6 + 4 * B ≤ t ∧ t ≤ 11 + 4 * B ∧ B ≤ L ∧
      Canonical (orbit n t) d L ∧ Canonical p e L ∧
      0 < p ∧ Palindrome p ∧ orbit n t % M = p % M := by
  obtain ⟨t, d, L, ht0, ht1, hc, hB, he, h11⟩ := large_even_dvd11_state n B hn
  obtain ⟨p, e, hp, hpc, hpal, hr⟩ := matching_even_palindrome (orbit n t) L hc.1 he h11
  refine ⟨t, p, d, e, L, ht0, ht1, hB, hc, hpc, hp, hpal, ?_⟩
  have hm := congrArg (fun x => x % M) hr
  simpa only [Nat.mod_mod_of_dvd _ hM] using hm.symm

/-- Beyond B, membership is constant on each exact-width residue class.
The allowed residue classes may vary arbitrarily with the exact width. -/
def SaturatedAbove (S : Nat → Prop) (M B : Nat) : Prop :=
  ∀ L, B ≤ L → ∀ n m (d e : Nat → Nat),
    Canonical n d L → Canonical m e L →
    n % M = m % M → (S n ↔ S m)

/-- No positive nonempty forward-closed palindrome-free set can be
eventually saturated by exact width and a divisor-of-99 residue. -/
theorem closed_saturated_contains_palindrome (M : Nat) (S : Nat → Prop)
    (hM : M ∣ 99) (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n → S n → S (step n))
    (hsat : ∃ B, SaturatedAbove S M B) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  obtain ⟨n, hn, hs⟩ := hne
  obtain ⟨B, hB⟩ := hsat
  obtain ⟨t, p, d, e, L, _, _, hLB, hc, hpc, hp, hpal, hr⟩ :=
    orbit_matches_palindrome_of_dvd99 M n B hM hn
  have hmem : ∀ k, S (orbit n k) := by
    intro k
    induction k with
    | zero => exact hs
    | succ k ih => exact hclosed (orbit n k) (orbit_positive n hn k) ih
  exact ⟨p, hp, (hB L hLB (orbit n t) p d e hc hpc hr).mp (hmem t), hpal⟩

/-- Reuse Agent #108's classification: every modulus admitting an eventual
residue-only step update has the preceding invariant-class obstruction. -/
theorem autonomous_closed_saturated_contains_palindrome
    (M : Nat) (S : Nat → Prop) (hM : 0 < M)
    (haut : ModularAutonomy.EventualStepResidueDet M)
    (hne : ∃ n, 0 < n ∧ S n)
    (hclosed : ∀ n, 0 < n → S n → S (step n))
    (hsat : ∃ B, SaturatedAbove S M B) :
    ∃ p, 0 < p ∧ S p ∧ Palindrome p := by
  exact closed_saturated_contains_palindrome M S
    ((ModularAutonomy.eventual_step_residue_determinism_iff M hM).mp haut)
    hne hclosed hsat

#print axioms large_even_dvd11_state
#print axioms orbit_matches_palindrome_of_dvd99
#print axioms closed_saturated_contains_palindrome
#print axioms autonomous_closed_saturated_contains_palindrome

end Agent105.ResidueTrap
