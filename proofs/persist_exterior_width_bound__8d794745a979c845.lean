import Std

/-!
Generic width bookkeeping for a neutral-band return construction.
The concrete finite-time carry certificates establishing these hypotheses
are not formalized in this file. No decimal infinite-orbit claim is made.
-/
namespace NeutralWidthBound

def bonus (emissions : Nat) : Nat := if emissions = 1 then 2 else 0

def potential (width emissions : Nat → Nat) (t : Nat) : Nat :=
  width t + bonus (emissions t)

theorem potential_step (width emissions : Nat → Nat)
    (balance : ∀ t, width (t+1) + 2 * emissions t = width t + 4)
    (positive : ∀ t, 1 ≤ emissions t)
    (not_two : ∀ t, emissions t ≠ 2)
    (no_consecutive_one : ∀ t, emissions t = 1 → emissions (t+1) ≠ 1)
    (t : Nat) : potential width emissions (t+1) ≤ potential width emissions t := by
  have hb := balance t
  have hp := positive t
  have hn := not_two t
  by_cases h : emissions t = 1
  · have hnext := no_consecutive_one t h
    simp only [potential, bonus, h, hnext, if_true, if_false]
    omega
  · by_cases hnext : emissions (t+1) = 1
    · simp only [potential, bonus, h, hnext, if_true, if_false]
      omega
    · simp only [potential, bonus, h, hnext, if_true, if_false]
      omega

/-- Isolated one-pair emissions increase width by two; every other allowed
emission decreases it by at least two. Hence width never exceeds its initial
value by more than two, however many return blocks are performed. -/
theorem width_bounded (width emissions : Nat → Nat)
    (balance : ∀ t, width (t+1) + 2 * emissions t = width t + 4)
    (positive : ∀ t, 1 ≤ emissions t)
    (not_two : ∀ t, emissions t ≠ 2)
    (no_consecutive_one : ∀ t, emissions t = 1 → emissions (t+1) ≠ 1) :
    ∀ t, width t ≤ width 0 + 2 := by
  have mono : ∀ t, potential width emissions t ≤ potential width emissions 0 := by
    intro t
    induction t with
    | zero => exact Nat.le_refl _
    | succ t ih =>
      exact Nat.le_trans (potential_step width emissions balance positive not_two
        no_consecutive_one t) ih
  intro t
  have hm := mono t
  have ht : width t ≤ potential width emissions t := by
    unfold potential
    omega
  have h0 : potential width emissions 0 ≤ width 0 + 2 := by
    unfold potential bonus
    split <;> omega
  omega

/-- Padding a variable-width center to a common width makes each neutral
annulus grow by exactly two per return. The equations avoid natural-number
subtraction and thus state the needed nonnegative padding explicitly. -/
theorem padded_annulus_increment
    (w w' padding padding' common m m' padded padded' emitted : Nat)
    (hwidth : w' + 2 * emitted = w + 4)
    (hpad : w + 2 * padding = common)
    (hpad' : w' + 2 * padding' = common)
    (hgrow : m' = m + emitted)
    (houter : padded + padding = m)
    (houter' : padded' + padding' = m') : padded' = padded + 2 := by
  omega

#print axioms potential_step
#print axioms width_bounded
#print axioms padded_annulus_increment

/-- Strict compensation potential. The tag records whether the canonical
center begins with14; the arithmetic hypotheses remain abstract. -/
def strictPotential (width : Nat → Nat) (tag : Nat → Bool) (t : Nat) : Nat :=
  width t + if tag t then 0 else 3

theorem strict_potential_step (width emissions : Nat → Nat) (tag : Nat → Bool)
    (balance : ∀ t, width (t+1) + 2 * emissions t = width t + 4)
    (positive : ∀ t, 1 ≤ emissions t)
    (not_two : ∀ t, emissions t ≠ 2)
    (tagged_emits_four : ∀ t, tag t = true → 4 ≤ emissions t)
    (one_tags_next : ∀ t, emissions t = 1 → tag (t+1) = true)
    (t : Nat) :
    strictPotential width tag (t+1) + 1 ≤ strictPotential width tag t := by
  have hb := balance t
  have hp := positive t
  have hn := not_two t
  cases ht : tag t with
  | true =>
    have hfour := tagged_emits_four t ht
    cases ht' : tag (t+1) <;> simp only [strictPotential, ht, ht', Bool.false_eq_true,
      if_false, if_true] <;> omega
  | false =>
    by_cases hone : emissions t = 1
    · have ht' := one_tags_next t hone
      simp only [strictPotential, ht, ht', Bool.false_eq_true, if_false, if_true]
      omega
    · cases ht' : tag (t+1) <;> simp only [strictPotential, ht, ht', Bool.false_eq_true,
        if_false, if_true] <;> omega

/-- An infinite sequence satisfying the verified compensation hypotheses
would give an infinite strictly descending sequence of natural potentials. -/
theorem no_infinite_compensated_return (width emissions : Nat → Nat) (tag : Nat → Bool)
    (balance : ∀ t, width (t+1) + 2 * emissions t = width t + 4)
    (positive : ∀ t, 1 ≤ emissions t)
    (not_two : ∀ t, emissions t ≠ 2)
    (tagged_emits_four : ∀ t, tag t = true → 4 ≤ emissions t)
    (one_tags_next : ∀ t, emissions t = 1 → tag (t+1) = true) : False := by
  have desc : ∀ t, strictPotential width tag t + t ≤ strictPotential width tag 0 := by
    intro t
    induction t with
    | zero => omega
    | succ t ih =>
      have hs := strict_potential_step width emissions tag balance positive not_two
        tagged_emits_four one_tags_next t
      omega
  have impossible := desc (strictPotential width tag 0 + 1)
  omega

/-- A finite run with a unit decrease at every transition has at most its
initial potential many transitions. -/
theorem finite_descent_bound (value : Nat → Nat) (depth : Nat)
    (hstep : ∀ t, t < depth → value (t+1) + 1 ≤ value t) : depth ≤ value 0 := by
  have bound : ∀ t, t ≤ depth → value t + t ≤ value 0 := by
    intro t
    induction t with
    | zero => intro _; omega
    | succ t ih =>
      intro ht
      have hp := ih (by omega)
      have hs := hstep t (by omega)
      omega
  have h := bound depth (Nat.le_refl depth)
  omega

#print axioms finite_descent_bound
#print axioms strict_potential_step
#print axioms no_infinite_compensated_return

end NeutralWidthBound
