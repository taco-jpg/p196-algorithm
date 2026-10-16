import Lychrel196Research

set_option autoImplicit false

/-!
Agent #423: exact ordinary-decimal residue transport.
The first three 99-absorption endpoints repair Agent #315's written contract.
Later results derive width-independent residue dynamics after the existing
six-step divisibility-by-11 theorem. This is periodicity of residues, NOT
periodicity, termination, or palindrome avoidance of the integer orbit.
-/
namespace Agent423.TemporalResidues

open Lychrel196 DecimalDigits AstraModular

/-- Every divisor of 99 gives a forward-invariant divisibility class. -/
theorem step_preserves_divisor99 (M n : Nat) (hM : M ∣ 99) (hn : M ∣ n) :
    M ∣ step n := by
  by_cases hz : n = 0
  · subst n
    simpa [step, reverse10, reverseFuel] using (Nat.dvd_zero M)
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := step_mod_of_dvd99 M n d L hM hc
    have hm := Nat.mod_eq_zero_of_dvd hn
    apply Nat.dvd_of_mod_eq_zero
    simpa [Nat.mul_mod, hm] using hr

theorem step_preserves_dvd99 (n : Nat) (h : 99 ∣ n) : 99 ∣ step n :=
  step_preserves_divisor99 99 n (by decide) h

theorem orbit_preserves_divisor99 (M n k : Nat) (hM : M ∣ 99) (hn : M ∣ n) :
    M ∣ orbit n k := by
  induction k with
  | zero => exact hn
  | succ k ih => exact step_preserves_divisor99 M (orbit n k) hM ih

theorem orbit_preserves_dvd99 (n k : Nat) (h : 99 ∣ n) : 99 ∣ orbit n k :=
  orbit_preserves_divisor99 99 n k (by decide) h

theorem orbit_dvd99_of_dvd99_at (n t k : Nat) (h : 99 ∣ orbit n t) :
    99 ∣ orbit n (t + k) := by
  have hp := orbit_preserves_dvd99 (orbit n t) k h
  simpa only [← LychrelCertificates.orbit_add] using hp

/-- Width parity ceases to affect the modulo-99 transition once 11 divides
an actual integer state. This premise is not a symbolic-model assumption. -/
theorem step_mod99_of_dvd11 (n : Nat) (hn : 11 ∣ n) :
    step n % 99 = (2 * n) % 99 := by
  by_cases hz : n = 0
  · subst n
    decide
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := step_mod99 n d L hc
    obtain ⟨a, ha⟩ := hn
    by_cases he : L % 2 = 0
    · simp only [if_pos he] at hr
      omega
    · simpa only [if_neg he] using hr

/-- Closed residue formula on the actual 11-divisible class. -/
theorem orbit_mod99_pow_of_dvd11 (n k : Nat) (hn : 11 ∣ n) :
    orbit n k % 99 = (2 ^ k * n) % 99 := by
  induction k with
  | zero => simp [orbit]
  | succ k ih =>
      change step (orbit n k) % 99 = _
      rw [step_mod99_of_dvd11 (orbit n k) (AstraModular.orbit_preserves_dvd11 n k hn)]
      calc
        (2 * orbit n k) % 99 = (2 * (orbit n k % 99)) % 99 := by omega
        _ = (2 * ((2 ^ k * n) % 99)) % 99 := by rw [ih]
        _ = (2 * (2 ^ k * n)) % 99 := by omega
        _ = (2 ^ (k + 1) * n) % 99 := by
          rw [Nat.pow_succ]
          simp only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

/-- Six-step periodicity is only a residue statement. -/
theorem orbit_six_mod99_of_dvd11 (n : Nat) (hn : 11 ∣ n) :
    orbit n 6 % 99 = n % 99 := by
  have hr := orbit_mod99_pow_of_dvd11 n 6 hn
  change orbit n 6 % 99 = (64 * n) % 99 at hr
  obtain ⟨a, ha⟩ := hn
  omega

/-- All positive actual decimal trajectories have a six-periodic modulo-99
suffix from time six; no bound on the integer trajectory is inferred. -/
theorem orbit_mod99_period_six (n t : Nat) (hn : 0 < n) (ht : 6 ≤ t) :
    orbit n (t + 6) % 99 = orbit n t % 99 := by
  have hd : 11 ∣ orbit n t := Nat.dvd_of_mod_eq_zero
    (AstraModular.orbit_mod11_eq_zero_of_six_le n t hn ht)
  have hr := orbit_six_mod99_of_dvd11 (orbit n t) hd
  simpa only [← LychrelCertificates.orbit_add] using hr

/-- Exact initial phase for the eventual residue cycle of 196. -/
theorem orbit196_six_mod99 : orbit 196 6 % 99 = 88 := by decide

theorem orbit196_mod99_after_six (k : Nat) :
    orbit 196 (6 + k) % 99 = (2 ^ k * 88) % 99 := by
  have hr := orbit_mod99_pow_of_dvd11 (orbit 196 6) k
    (AstraModular.orbit_six_dvd11 196 (by decide))
  rw [← LychrelCertificates.orbit_add] at hr
  calc
    orbit 196 (6 + k) % 99 = (2 ^ k * orbit 196 6) % 99 := hr
    _ = (2 ^ k * 88) % 99 := by
      simp only [Nat.mul_mod, orbit196_six_mod99, Nat.mod_mod]


/-- A periodic function on natural times is determined by its first p values.
This arithmetic reduction does not require a finiteness assumption on values. -/
theorem periodic_reduce {β : Type} (f : Nat → β) (p : Nat) (hp : 0 < p)
    (hperiod : ∀ k, f (k + p) = f k) (k : Nat) : f k = f (k % p) := by
  induction k using Nat.strongRecOn with
  | ind k ih =>
      by_cases hk : k < p
      · rw [Nat.mod_eq_of_lt hk]
      · have hlt : k - p < k := by omega
        have he : k - p + p = k := by omega
        have hm : (k - p) % p = k % p := by
          have hh := congrArg (fun x => x % p) he
          simpa only [Nat.add_mod, Nat.mod_self, Nat.add_zero, Nat.mod_mod] using hh
        calc
          f k = f (k - p) := by simpa only [he] using hperiod (k - p)
          _ = f ((k - p) % p) := ih (k - p) hlt
          _ = f (k % p) := by rw [hm]

def phase196 (k : Nat) : Nat :=
  if k % 6 = 0 then 88 else if k % 6 = 1 then 77 else
  if k % 6 = 2 then 55 else if k % 6 = 3 then 11 else
  if k % 6 = 4 then 22 else 44

/-- Complete residue table of the actual 196 orbit from time six. -/
theorem orbit196_mod99_table (k : Nat) :
    orbit 196 (6 + k) % 99 = phase196 k := by
  have hp : ∀ j, orbit 196 (6 + (j + 6)) % 99 = orbit 196 (6 + j) % 99 := by
    intro j
    simpa only [Nat.add_assoc] using
      orbit_mod99_period_six 196 (6 + j) (by decide) (by omega)
  have hr := periodic_reduce (fun j => orbit 196 (6 + j) % 99) 6 (by decide) hp k
  rw [hr, orbit196_mod99_after_six]
  have hb : k % 6 = 0 ∨ k % 6 = 1 ∨ k % 6 = 2 ∨
      k % 6 = 3 ∨ k % 6 = 4 ∨ k % 6 = 5 := by omega
  rcases hb with h | h | h | h | h | h <;> simp [phase196, h]

/-- The displayed six residues are pairwise distinct by phase. -/
theorem phase196_injective (a b : Nat) (ha : a < 6) (hb : b < 6)
    (he : phase196 a = phase196 b) : a = b := by
  have hA : a = 0 ∨ a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 := by omega
  have hB : b = 0 ∨ b = 1 ∨ b = 2 ∨ b = 3 ∨ b = 4 ∨ b = 5 := by omega
  rcases hA with rfl | rfl | rfl | rfl | rfl | rfl <;>
    rcases hB with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp_all [phase196]

/-- Therefore the minimal positive period of this residue suffix is six:
any period P valid from time six must be divisible by six. -/
theorem any_period_of_196_suffix_multiple_six (P : Nat)
    (hperiod : ∀ k, orbit 196 (6 + (k + P)) % 99 = orbit 196 (6 + k) % 99) :
    6 ∣ P := by
  have h := hperiod 0
  simp only [Nat.zero_add, orbit196_mod99_table] at h
  have he : phase196 (P % 6) = phase196 0 := by
    simpa only [phase196, Nat.mod_mod] using h
  have hz := phase196_injective (P % 6) 0 (Nat.mod_lt _ (by decide)) (by decide) he
  exact Nat.dvd_of_mod_eq_zero hz

theorem step_mod3 (n : Nat) : step n % 3 = (2 * n) % 3 := by
  have hr := congrArg (fun x => x % 3) (Lychrel196.step_mod9 n)
  simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 9)] using hr

theorem orbit_mod3_nonzero (n k : Nat) (hn : n % 3 ≠ 0) :
    orbit n k % 3 ≠ 0 := by
  induction k with
  | zero => exact hn
  | succ k ih =>
      change step (orbit n k) % 3 ≠ 0
      have hr := step_mod3 (orbit n k)
      omega

theorem orbit196_mod3_nonzero (k : Nat) : orbit 196 k % 3 ≠ 0 :=
  orbit_mod3_nonzero 196 k (by decide)

/-- The 99-divisible invariant class is never entered by the actual 196 orbit.
This does not exclude palindromes in its nonzero residue classes. -/
theorem orbit196_never_dvd99 (k : Nat) : ¬ 99 ∣ orbit 196 k := by
  intro h
  have ht : 3 ∣ orbit 196 k := Nat.dvd_trans (by decide : 3 ∣ 99) h
  exact orbit196_mod3_nonzero k (Nat.mod_eq_zero_of_dvd ht)


/-- Each residue phase has an actual positive decimal-palindrome representative.
Therefore the residue cycle alone cannot prove palindrome avoidance. -/
theorem phase_has_palindrome_representative (k : Nat) :
    ∃ p : Nat, 0 < p ∧ Palindrome p ∧ p % 99 = orbit 196 (6 + k) % 99 := by
  rw [orbit196_mod99_table]
  have hb : k % 6 = 0 ∨ k % 6 = 1 ∨ k % 6 = 2 ∨
      k % 6 = 3 ∨ k % 6 = 4 ∨ k % 6 = 5 := by omega
  rcases hb with h | h | h | h | h | h
  · refine ⟨88, by decide, by decide, ?_⟩; simp [phase196, h]
  · refine ⟨77, by decide, by decide, ?_⟩; simp [phase196, h]
  · refine ⟨55, by decide, by decide, ?_⟩; simp [phase196, h]
  · refine ⟨11, by decide, by decide, ?_⟩; simp [phase196, h]
  · refine ⟨22, by decide, by decide, ?_⟩; simp [phase196, h]
  · refine ⟨44, by decide, by decide, ?_⟩; simp [phase196, h]

/-- No predicate depending only on residue modulo 99 can both contain this
entire suffix and exclude every decimal palindrome. Width restrictions or
additional state would be separate hypotheses, not covered by this theorem. -/
theorem no_mod99_only_palindrome_exclusion (R : Nat → Prop)
    (contains : ∀ k, R (orbit 196 (6 + k) % 99))
    (excludes : ∀ p, R (p % 99) → ¬ Palindrome p) : False := by
  obtain ⟨p, _, hp, he⟩ := phase_has_palindrome_representative 0
  have hr : R (p % 99) := by rw [he]; exact contains 0
  exact excludes p hr hp

#print axioms step_preserves_divisor99
#print axioms step_preserves_dvd99
#print axioms orbit_preserves_divisor99
#print axioms orbit_preserves_dvd99
#print axioms orbit_dvd99_of_dvd99_at
#print axioms step_mod99_of_dvd11
#print axioms orbit_mod99_pow_of_dvd11
#print axioms orbit_six_mod99_of_dvd11
#print axioms orbit_mod99_period_six
#print axioms orbit196_six_mod99
#print axioms orbit196_mod99_after_six

#print axioms periodic_reduce
#print axioms orbit196_mod99_table
#print axioms phase196_injective
#print axioms any_period_of_196_suffix_multiple_six
#print axioms step_mod3
#print axioms orbit_mod3_nonzero
#print axioms orbit196_mod3_nonzero
#print axioms orbit196_never_dvd99

#print axioms phase_has_palindrome_representative
#print axioms no_mod99_only_palindrome_exclusion

end Agent423.TemporalResidues
