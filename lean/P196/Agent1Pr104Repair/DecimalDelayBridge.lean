import P196.Agent1Pr104Repair.SafeDelay
import P196.Agent1Pr104Repair.DecimalSafeRuns

/-!
Exact decimal delay/cutoff equivalences and an explicit conditional witness.
No bound on all finite terminating delays is supplied or assumed globally.
-/

namespace DecimalDelayBridge

open Lychrel196 DecimalDigits DecimalSafeRuns

def Bad (n : Nat) : Prop := Palindrome (step n)

/-- Least positive palindrome time. The initial value may be palindromic. -/
def FirstPositiveHit (n d : Nat) : Prop :=
  0 < d ∧ Palindrome (orbit n d) ∧
    ∀ k, 0 < k → k < d → ¬ Palindrome (orbit n k)

def FiniteDelayBound (D : Nat) : Prop :=
  ∀ n d, 0 < n → FirstPositiveHit n d → d ≤ D

def S (r : Nat) : Nat → Prop :=
  SafeImageDynamics.image step (fun n => 0 < n) Bad r

def K (r : Nat) : Nat → Prop :=
  SafeImageDynamics.kernel step (fun n => 0 < n) Bad r

theorem step_positive (n : Nat) (hn : 0 < n) : 0 < step n := by
  unfold step
  omega

theorem iter_eq_orbit (n k : Nat) : SafeImageDynamics.iter step n k = orbit n k := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg step ih

theorem orbit_step (n k : Nat) : orbit (step n) k = orbit n (k + 1) := by
  have he := LychrelCertificates.orbit_add n 1 k
  simpa only [orbit, Nat.add_comm] using he.symm

theorem bad_iter_iff (n r : Nat) :
    Bad (SafeImageDynamics.iter step n r) ↔ Palindrome (orbit n (r + 1)) := by
  rw [iter_eq_orbit]
  rfl

theorem firstBad_iff_positive_hit (n r : Nat) :
    SafeImageDynamics.FirstBad step Bad n r ↔ FirstPositiveHit n (r + 1) := by
  constructor
  · rintro ⟨hb, hs⟩
    refine ⟨by omega, (bad_iter_iff n r).mp hb, ?_⟩
    intro k hk0 hkr hpal
    have hk : k - 1 < r := by omega
    apply hs (k - 1) hk
    apply (bad_iter_iff n (k - 1)).mpr
    simpa only [Nat.sub_add_cancel hk0] using hpal
  · rintro ⟨_, hb, hs⟩
    refine ⟨(bad_iter_iff n r).mpr hb, ?_⟩
    intro k hk hbad
    exact hs (k + 1) (by omega) (by omega) ((bad_iter_iff n k).mp hbad)

/-- This is the exact safe-ancestry/first-positive-hit equivalence, with
the target untested by ancestry and tested by the final intersection. -/
theorem S_intersects_bad_iff (r : Nat) :
    (∃ n, S r n ∧ Bad n) ↔ ∃ n, 0 < n ∧ FirstPositiveHit n (r + 1) := by
  constructor
  · intro h
    obtain ⟨n, hn, hf⟩ := (SafeImageDynamics.image_bad_iff step
      (fun n => 0 < n) Bad r).mp h
    exact ⟨n, hn, (firstBad_iff_positive_hit n r).mp hf⟩
  · rintro ⟨n, hn, hf⟩
    exact (SafeImageDynamics.image_bad_iff step (fun n => 0 < n) Bad r).mpr
      ⟨n, hn, (firstBad_iff_positive_hit n r).mpr hf⟩

theorem finiteDelayBound_iff (D : Nat) :
    FiniteDelayBound D ↔ ∀ n r, 0 < n →
      SafeImageDynamics.FirstBad step Bad n r → r < D := by
  constructor
  · intro hb n r hn hf
    have hd := hb n (r + 1) hn ((firstBad_iff_positive_hit n r).mp hf)
    omega
  · intro hb n d hn hf
    have hp := hf.1
    have he : d - 1 + 1 = d := by omega
    have hf' : FirstPositiveHit n (d - 1 + 1) := by simpa only [he] using hf
    have hd := hb n (d - 1) hn ((firstBad_iff_positive_hit n (d - 1)).mpr hf')
    omega

theorem cutoff_iff_finiteDelayBound (r : Nat) :
    (∀ n, S r n → ¬ Bad n) ↔ FiniteDelayBound r :=
  (SafeImageDynamics.cutoff_iff_finite_bound step (fun n => 0 < n) Bad
    step_positive r).trans (finiteDelayBound_iff r).symm

/-- K_r is closed exactly when every finite positive first hit is ≤r+1. -/
theorem K_closed_iff_finiteDelayBound (r : Nat) :
    (∀ n, K r n → K r (step n)) ↔ FiniteDelayBound (r + 1) :=
  (SafeImageDynamics.kernel_closed_iff step (fun n => 0 < n) Bad
    step_positive r).trans (cutoff_iff_finiteDelayBound (r + 1))

theorem firstPositiveHit_suffix (n a d : Nat) (hd : 0 < d)
    (hf : FirstPositiveHit n (a + d)) : FirstPositiveHit (orbit n a) d := by
  refine ⟨hd, ?_, ?_⟩
  · rw [← LychrelCertificates.orbit_add]
    exact hf.2.1
  · intro k hk0 hkd
    rw [← LychrelCertificates.orbit_add]
    exact hf.2.2 (a + k) (by omega) (by omega)

theorem positive_delays_downward (n d k : Nat) (hn : 0 < n)
    (hf : FirstPositiveHit n d) (hk : 0 < k) (hkd : k ≤ d) :
    ∃ m, 0 < m ∧ FirstPositiveHit m k := by
  refine ⟨orbit n (d - k), orbit_positive n hn _, ?_⟩
  apply firstPositiveHit_suffix n (d - k) k hk
  simpa only [Nat.sub_add_cancel hkd] using hf

def UnboundedFiniteDelays : Prop :=
  ∀ R, ∃ n d, 0 < n ∧ FirstPositiveHit n d ∧ R < d

theorem unbounded_iff_every_positive_delay :
    UnboundedFiniteDelays ↔ ∀ d, 0 < d → ∃ n, 0 < n ∧ FirstPositiveHit n d := by
  constructor
  · intro h d hd
    obtain ⟨n, e, hn, hf, he⟩ := h d
    exact positive_delays_downward n e d hn hf hd (by omega)
  · intro h R
    obtain ⟨n, hn, hf⟩ := h (R + 1) (by omega)
    exact ⟨n, R + 1, hn, hf, by omega⟩

theorem unbounded_iff_all_safe_images_meet_bad :
    UnboundedFiniteDelays ↔ ∀ r, ∃ n, S r n ∧ Bad n := by
  rw [unbounded_iff_every_positive_delay]
  constructor
  · intro h r
    exact (S_intersects_bad_iff r).mpr (h (r + 1) (by omega))
  · intro h d hd
    have he : d - 1 + 1 = d := by omega
    simpa only [he] using (S_intersects_bad_iff (d - 1)).mp (h (d - 1))

theorem nines_add_one (L : Nat) : nines L + 1 = 10 ^ L := by
  induction L with
  | zero => rfl
  | succ L ih =>
    change nines L + 9 * 10 ^ L + 1 = 10 ^ (L + 1)
    rw [Nat.pow_succ]
    omega

theorem nines_palindrome (L : Nat) : Palindrome (nines L) := by
  exact reverse10_value (fun _ => 9) L (by intro i hi; exact Nat.le_refl 9)
    (Or.inr (by exact Nat.zero_lt_succ 8))

/-- An explicit ordinary integer, with no infinite digit object involved. -/
def candidate (D : Nat) : Nat := 2 * (10 ^ (2 * D + 1) - 1)

theorem candidate_eq_step_nines (D : Nat) : candidate D = step (nines (2 * D + 1)) := by
  have hn := nines_add_one (2 * D + 1)
  have hp := nines_palindrome (2 * D + 1)
  change reverse10 (nines (2 * D + 1)) = nines (2 * D + 1) at hp
  unfold candidate step
  rw [hp]
  omega

theorem candidate_positive (D : Nat) : 0 < candidate D := by
  rw [candidate_eq_step_nines]
  exact step_positive _ (nines_positive _ (by omega))

/-- An explicit finite safe segment including the candidate's initial state. -/
theorem candidate_safe_prefix (D k : Nat) (hk : k ≤ D) :
    ¬ Palindrome (orbit (candidate D) k) := by
  rw [candidate_eq_step_nines, orbit_step]
  exact nines_safe_prefix D k hk

/-- If all finite positive first hits are bounded by D, this specific
finite decimal integer is Lychrel. The finite safe prefix is proved above. -/
theorem candidate_lychrel_of_finiteDelayBound (D : Nat) (hbound : FiniteDelayBound D) :
    IsLychrel (candidate D) := by
  have hn : 0 < nines (2 * D + 1) := nines_positive _ (by omega)
  have hs : SafeImageDynamics.SafePrefix step Bad (nines (2 * D + 1)) D := by
    intro k hk hb
    exact nines_safe_prefix D k (by omega) ((bad_iter_iff _ k).mp hb)
  have ha := SafeImageDynamics.avoids_of_finite_bound step (fun n => 0 < n) Bad D
    ((finiteDelayBound_iff D).mp hbound) _ hn hs
  intro k
  rw [candidate_eq_step_nines, orbit_step]
  intro hp
  exact ha k ((bad_iter_iff _ k).mpr hp)

theorem candidate_lychrel_of_cutoff (r : Nat) (hcut : ∀ n, S r n → ¬ Bad n) :
    IsLychrel (candidate r) :=
  candidate_lychrel_of_finiteDelayBound r ((cutoff_iff_finiteDelayBound r).mp hcut)

theorem candidate_lychrel_of_kernel_closed (r : Nat)
    (hclosed : ∀ n, K r n → K r (step n)) : IsLychrel (candidate (r + 1)) :=
  candidate_lychrel_of_finiteDelayBound (r + 1)
    ((K_closed_iff_finiteDelayBound r).mp hclosed)

/-- A genuine unconditional dichotomy. It does not select either branch. -/
theorem existence_or_unbounded_finite_delays :
    DecimalLychrelExistence ∨ UnboundedFiniteDelays := by
  classical
  by_cases hb : ∃ D, FiniteDelayBound D
  · obtain ⟨D, hD⟩ := hb
    exact Or.inl ⟨candidate D, candidate_lychrel_of_finiteDelayBound D hD⟩
  · right
    intro R
    apply Classical.byContradiction
    intro hn
    apply hb
    refine ⟨R, ?_⟩
    intro n d hpos hf
    have hnot : ¬ R < d := by intro h; exact hn ⟨n, d, hpos, hf, h⟩
    omega

theorem no_existence_implies_every_positive_delay (hno : ¬ DecimalLychrelExistence) :
    ∀ d, 0 < d → ∃ n, 0 < n ∧ FirstPositiveHit n d := by
  rcases existence_or_unbounded_finite_delays with he | hu
  · exact False.elim (hno he)
  · exact unbounded_iff_every_positive_delay.mp hu

#print axioms S_intersects_bad_iff
#print axioms cutoff_iff_finiteDelayBound
#print axioms K_closed_iff_finiteDelayBound
#print axioms positive_delays_downward
#print axioms unbounded_iff_every_positive_delay
#print axioms unbounded_iff_all_safe_images_meet_bad
#print axioms candidate_eq_step_nines
#print axioms candidate_safe_prefix
#print axioms candidate_lychrel_of_finiteDelayBound
#print axioms candidate_lychrel_of_cutoff
#print axioms candidate_lychrel_of_kernel_closed
#print axioms existence_or_unbounded_finite_delays
#print axioms no_existence_implies_every_positive_delay

end DecimalDelayBridge
