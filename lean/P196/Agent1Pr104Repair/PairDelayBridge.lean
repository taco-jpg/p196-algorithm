import P196.Agent1Pr104Repair.DecimalDelayBridge

/-!
The exact symbolic safe-image recurrence from the finite-ancestry study.
Admissibility and numeric realization are discharged, including changing
width and equality only on the finite represented prefix.
-/

namespace PairDelayBridge

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DecimalSafeRuns DecimalDelayBridge

abbrev State := Nat × (Nat → Nat)

def next (s : State) : State := (nextWidth s.2 s.1, nextColumns s.2 s.1)
def Valid (s : State) : Prop := Admissible s.1 s.2
def Bad (s : State) : Prop := BadWord s.1 s.2
def S (r : Nat) : State → Prop := SafeImageDynamics.image next Valid Bad r
def K (r : Nat) : State → Prop := SafeImageDynamics.kernel next Valid Bad r

theorem next_valid (s : State) (hs : Valid s) : Valid (next s) :=
  NormalizationBridge.admissible_next s.2 s.1 hs

theorem kernel_descending (r : Nat) : ∀ s, K (r + 1) s → K r s :=
  SafeImageDynamics.kernel_descending next Valid Bad next_valid r

theorem iter_eq_iterPairs (s : State) (r : Nat) :
    SafeImageDynamics.iter next s r = iterPairs s.2 s.1 r := by
  induction r with
  | zero => exact (Prod.eta s).symm
  | succ r ih =>
    change next (SafeImageDynamics.iter next s r) = next (iterPairs s.2 s.1 r)
    exact congrArg next ih

theorem palindrome_iff_bad (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i) :
    Palindrome (step n) ↔ BadWord L q := by
  have he : Palindrome (step n) ↔ BadWord L (columnSum d L) := by
    rw [← hc.2.2.2]
    exact step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1
  rw [he]
  constructor
  · rintro (hlo | ⟨houter, hhi⟩)
    · exact Or.inl (fun i hi => by rw [← hr i hi]; exact hlo i hi)
    · exact Or.inr ⟨by rw [← hr 0 hc.1]; exact houter,
        fun i hi => by rw [← hr i hi]; exact hhi i hi⟩
  · rintro (hlo | ⟨houter, hhi⟩)
    · exact Or.inl (fun i hi => by rw [hr i hi]; exact hlo i hi)
    · exact Or.inr ⟨by rw [hr 0 hc.1]; exact houter,
        fun i hi => by rw [hr i hi]; exact hhi i hi⟩

theorem bad_iter_iff_positive_palindrome (n : Nat) (d q : Nat → Nat) (L r : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i) :
    Bad (SafeImageDynamics.iter next (L, q) r) ↔ Palindrome (orbit n (r + 1)) := by
  rw [iter_eq_iterPairs]
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L r hc hr
  exact (palindrome_iff_bad _ e _ _ he hrep).symm

theorem firstBad_iff_positive_hit (n : Nat) (d q : Nat → Nat) (L r : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i) :
    SafeImageDynamics.FirstBad next Bad (L, q) r ↔ FirstPositiveHit n (r + 1) := by
  constructor
  · rintro ⟨hb, hs⟩
    refine ⟨by omega, (bad_iter_iff_positive_palindrome n d q L r hc hr).mp hb, ?_⟩
    intro k hk0 hkr hpal
    apply hs (k - 1) (by omega)
    apply (bad_iter_iff_positive_palindrome n d q L (k - 1) hc hr).mpr
    simpa only [Nat.sub_add_cancel hk0] using hpal
  · rintro ⟨_, hb, hs⟩
    refine ⟨(bad_iter_iff_positive_palindrome n d q L r hc hr).mpr hb, ?_⟩
    intro k hk hbad
    exact hs (k + 1) (by omega) (by omega)
      ((bad_iter_iff_positive_palindrome n d q L k hc hr).mp hbad)

/-- Exact safe-ancestry/first-positive-hit equivalence for admissible pair
words, with their actual changing widths and the two palindrome patterns. -/
theorem S_intersects_bad_iff (r : Nat) :
    (∃ s, S r s ∧ Bad s) ↔ ∃ n, 0 < n ∧ FirstPositiveHit n (r + 1) := by
  constructor
  · intro h
    obtain ⟨⟨L, q⟩, ha, hf⟩ := (SafeImageDynamics.image_bad_iff next Valid Bad r).mp h
    obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable q L
      ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
    exact ⟨n, hn, (firstBad_iff_positive_hit n d q L r hc hr).mp hf⟩
  · rintro ⟨n, hn, hf⟩
    obtain ⟨d, L, hc⟩ := canonical_exists n hn
    have ha := NormalizationBridge.canonical_admissible n d L hc
    apply (SafeImageDynamics.image_bad_iff next Valid Bad r).mpr
    exact ⟨(L, columnSum d L), ha,
      (firstBad_iff_positive_hit n d (columnSum d L) L r hc (fun _ _ => rfl)).mpr hf⟩

theorem cutoff_iff_finiteDelayBound (r : Nat) :
    (∀ s, S r s → ¬ Bad s) ↔ FiniteDelayBound r := by
  have he : (∃ s, S r s ∧ Bad s) ↔
      ∃ n, DecimalDelayBridge.S r n ∧ DecimalDelayBridge.Bad n :=
    (S_intersects_bad_iff r).trans (DecimalDelayBridge.S_intersects_bad_iff r).symm
  constructor
  · intro hcut
    apply (DecimalDelayBridge.cutoff_iff_finiteDelayBound r).mp
    intro n hn hb
    obtain ⟨s, hs, hbad⟩ := he.mpr ⟨n, hn, hb⟩
    exact hcut s hs hbad
  · intro hbound s hs hb
    obtain ⟨n, hn, hbad⟩ := he.mp ⟨s, hs, hb⟩
    exact (DecimalDelayBridge.cutoff_iff_finiteDelayBound r).mpr hbound n hn hbad

theorem K_closed_iff_finiteDelayBound (r : Nat) :
    (∀ s, K r s → K r (next s)) ↔ FiniteDelayBound (r + 1) :=
  (SafeImageDynamics.kernel_closed_iff next Valid Bad next_valid r).trans
    (cutoff_iff_finiteDelayBound (r + 1))

theorem unbounded_iff_all_safe_images_meet_bad :
    UnboundedFiniteDelays ↔ ∀ r, ∃ s, S r s ∧ Bad s := by
  rw [unbounded_iff_every_positive_delay]
  constructor
  · intro h r
    exact (S_intersects_bad_iff r).mpr (h (r + 1) (by omega))
  · intro h d hd
    have he : d - 1 + 1 = d := by omega
    simpa only [he] using (S_intersects_bad_iff (d - 1)).mp (h (d - 1))

theorem candidate_lychrel_of_pair_cutoff (r : Nat)
    (hcut : ∀ s, S r s → ¬ Bad s) : IsLychrel (candidate r) :=
  candidate_lychrel_of_finiteDelayBound r ((cutoff_iff_finiteDelayBound r).mp hcut)

theorem candidate_lychrel_of_pair_kernel_closed (r : Nat)
    (hclosed : ∀ s, K r s → K r (next s)) : IsLychrel (candidate (r + 1)) :=
  candidate_lychrel_of_finiteDelayBound (r + 1)
    ((K_closed_iff_finiteDelayBound r).mp hclosed)

/-- Every finite ancestry depth has safe members, unconditionally. -/
theorem kernel_nonempty (r : Nat) : ∃ s, K r s := by
  let L := 2 * r + 1
  let d : Nat → Nat := fun _ => 9
  let q : Nat → Nat := fun _ => 18
  have hc : Canonical (nines L) d L := nines_canonical L (by dsimp [L]; omega)
  have hr : ∀ i, i < L → columnSum d L i = q i := by intro i hi; rfl
  have ha : Valid (L, q) :=
    NormalizationBridge.admissible_congr _ _ _
      (NormalizationBridge.canonical_admissible _ _ _ hc) hr
  have hs : ∀ k, k ≤ r → ¬ Bad (SafeImageDynamics.iter next (L, q) k) := by
    intro k hk hb
    exact nines_safe_prefix r k hk
      ((bad_iter_iff_positive_palindrome (nines L) d q L k hc hr).mp hb)
  refine ⟨SafeImageDynamics.iter next (L, q) r, ?_, hs r (Nat.le_refl _)⟩
  apply (SafeImageDynamics.image_iff next Valid Bad _ r).mpr
  exact ⟨(L, q), ha, rfl, fun k hk => hs k (by omega)⟩

/-- In contrast to changing finite-depth witnesses, a fixed finite target
has bounded backward depth. This is the exact recurrence S_r. -/
theorem image_depth_le (s : State) (r : Nat) (hs : S r s) : r ≤ 4 * s.1 := by
  obtain ⟨x, hx, he, _⟩ := (SafeImageDynamics.image_iff next Valid Bad s r).mp hs
  rw [iter_eq_iterPairs] at he
  have hw : (iterPairs x.2 x.1 r).1 = s.1 := congrArg Prod.fst he
  have hg := DecimalWidthGrowth.width_lower_bound x.2 x.1 r hx
  have hpos := hx.1
  rw [hw] at hg
  omega

theorem safe_image_intersection_empty (s : State) : ¬ ∀ r, S r s := by
  intro hs
  have := image_depth_le s (4 * s.1 + 1) (hs _)
  omega

theorem kernel_intersection_empty : ¬ ∃ s, ∀ r, K r s := by
  rintro ⟨s, hs⟩
  exact safe_image_intersection_empty s (fun r => (hs r).1)

/-- The quantifier order cannot be swapped: these exact descending safe
languages are all nonempty, while no finite target belongs to all depths. -/
theorem nonempty_depths_empty_intersection :
    (∀ r, ∃ s, K r s) ∧ ¬ (∃ s, ∀ r, K r s) :=
  ⟨kernel_nonempty, kernel_intersection_empty⟩

#print axioms S_intersects_bad_iff
#print axioms cutoff_iff_finiteDelayBound
#print axioms K_closed_iff_finiteDelayBound
#print axioms unbounded_iff_all_safe_images_meet_bad
#print axioms candidate_lychrel_of_pair_cutoff
#print axioms candidate_lychrel_of_pair_kernel_closed
#print axioms kernel_nonempty
#print axioms kernel_descending
#print axioms image_depth_le
#print axioms nonempty_depths_empty_intersection

end PairDelayBridge
