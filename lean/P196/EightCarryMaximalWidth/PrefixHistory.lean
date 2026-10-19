import P196.Agent104P620Witness.ActualPrefix
import P196.Agent10EightCarry.DifferenceObservability

/-!
Agent #10: synchronized complete-carry observations on arbitrary finite prefixes.
The accepted generic `actual_forwardPrefix` theorem supplies every transition.
Only list lookup and the connection between finite carry signatures and actual
observed coordinates are established here. Reflected prefixes may overlap.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace EightCarryMaximalWidth.PrefixHistory

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open CarryObservabilityActual DifferenceObservability SevenColumnProjection

/-- The low incoming carries, including the initial zero and the carry after
the last prefix coefficient. -/
def lowSignature (s : List Nat) : List Nat :=
  (List.range (s.length + 1)).map
    (carry (fun i => s.getD i 0))

/-- The high carries from exterior to interior. The first is the terminal
overflow carry and the last is the supplied common interior carry. -/
def highSignature (s : List Nat) (e : Nat) : List Nat :=
  (List.range (s.length + 1)).map
    (fun i => (highDigits (s.drop i) e).1)

/-- All low and all reflected high coordinates must coincide. -/
def compatible (s r : List Nat) (e : Nat) : Bool :=
  decide (lowSignature s = lowSignature r) &&
    decide (highSignature s e = highSignature r e)

/-- Positive exterior coefficient and the ordinary pair-coefficient bounds. -/
def valid : List Nat → Bool
  | [] => false
  | a :: s => decide (1 ≤ a ∧ a ≤ 18) && s.all (fun x => decide (x ≤ 18))

/-- A bounded-depth synchronized history. Both possible common interior carry
bits are explored; each successor is checked to remain a valid prefix. -/
def survives : Nat → List Nat → List Nat → Bool
  | 0, _, _ => true
  | n + 1, s, r =>
      let branch := fun e =>
        compatible s r e &&
          valid (forwardPrefix s e) && valid (forwardPrefix r e) &&
          survives n (forwardPrefix s e) (forwardPrefix r e)
      branch 0 || branch 1

theorem segment_getD (q : Nat → Nat) (start n i : Nat) (hi : i < n) :
    (segment q start n).getD i 0 = q (start + i) := by
  induction n generalizing start i with
  | zero => omega
  | succ n ih =>
      cases i with
      | zero => rfl
      | succ i =>
          simp only [segment, List.getD_cons_succ]
          simpa only [Nat.add_assoc, Nat.add_comm 1 i] using
            ih (start + 1) i (by omega)

theorem prefix_getD (q : Nat → Nat) (k i : Nat) (hi : i < k) :
    (wordPrefix q k).getD i 0 = q i := by
  simpa only [wordPrefix, Nat.zero_add] using segment_getD q 0 k i hi

theorem drop_segment (q : Nat → Nat) (start n i : Nat) (hi : i ≤ n) :
    (segment q start n).drop i = segment q (start + i) (n - i) := by
  induction i generalizing start n with
  | zero => simp only [List.drop_zero, Nat.add_zero, Nat.sub_zero]
  | succ i ih =>
      cases n with
      | zero => omega
      | succ n =>
          simpa only [segment, List.drop_succ_cons, Nat.succ_sub_succ_eq_sub,
            Nat.add_assoc, Nat.add_comm 1 i] using ih (start + 1) n (by omega)

theorem prefix_low_carry (q : Nat → Nat) (k i : Nat) (hi : i ≤ k) :
    carry (fun j => (wordPrefix q k).getD j 0) i = carry q i := by
  exact carry_congr_upto _ q k (fun j hj => prefix_getD q k j hj) i hi

theorem prefix_high_carry (q : Nat → Nat) (L k i : Nat)
    (hs : ∀ j, j < L → q j = q (L - 1 - j)) (hk : k ≤ L) (hi : i ≤ k) :
    (highDigits ((wordPrefix q k).drop i) (carry q (L - k))).1 =
      carry q (L - i) := by
  unfold wordPrefix
  rw [drop_segment q 0 k i hi]
  simp only [Nat.zero_add]
  have h := highDigits_segment q L i (k - i) hs (by omega)
  have he : i + (k - i) = k := by omega
  rw [he] at h
  exact congrArg Prod.fst h

theorem lowSignature_prefix (q : Nat → Nat) (k : Nat) :
    lowSignature (wordPrefix q k) =
      (List.range (k + 1)).map (carry q) := by
  simp only [lowSignature, prefix_length]
  apply List.map_congr_left
  intro i hi
  have hib : i < k + 1 := List.mem_range.mp hi
  exact prefix_low_carry q k i (by omega)

theorem highSignature_prefix (q : Nat → Nat) (L k : Nat)
    (hs : ∀ j, j < L → q j = q (L - 1 - j)) (hk : k ≤ L) :
    highSignature (wordPrefix q k) (carry q (L - k)) =
      (List.range (k + 1)).map (fun i => carry q (L - i)) := by
  simp only [highSignature, prefix_length]
  apply List.map_congr_left
  intro i hi
  have hib : i < k + 1 := List.mem_range.mp hi
  exact prefix_high_carry q L k i hs hk (by omega)

theorem actual_compatible (q r : Nat → Nat) (L k : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hk : k ≤ L)
    (hc : ∀ i, i ≤ L → carry q i = carry r i) :
    compatible (wordPrefix q k) (wordPrefix r k) (carry q (L - k)) = true := by
  have he : carry q (L - k) = carry r (L - k) := hc _ (by omega)
  have hl : lowSignature (wordPrefix q k) = lowSignature (wordPrefix r k) := by
    rw [lowSignature_prefix, lowSignature_prefix]
    apply List.map_congr_left
    intro i hi
    have hib : i < k + 1 := List.mem_range.mp hi
    exact hc i (by omega)
  have hh : highSignature (wordPrefix q k) (carry q (L - k)) =
      highSignature (wordPrefix r k) (carry q (L - k)) := by
    rw [highSignature_prefix q L k hq.2.2.2.1 hk, he,
      highSignature_prefix r L k hr.2.2.2.1 hk]
    apply List.map_congr_left
    intro i _
    exact hc (L - i) (by omega)
  simp only [compatible, hl, hh, decide_true, Bool.and_self]

theorem segment_all_bounded (q : Nat → Nat) (start n : Nat)
    (hq : ∀ i, i < n → q (start + i) ≤ 18) :
    (segment q start n).all (fun x => decide (x ≤ 18)) = true := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih =>
      simp only [segment, List.all_cons, Bool.and_eq_true, decide_eq_true_eq]
      refine ⟨?_, ?_⟩
      · simpa only [Nat.add_zero] using hq 0 (by omega)
      · apply ih (start + 1)
        intro i hi
        have h := hq (i + 1) (by omega)
        simpa only [Nat.add_assoc, Nat.add_comm 1 i] using h

theorem valid_prefix (q : Nat → Nat) (L k : Nat)
    (hq : Admissible L q) (hk0 : 0 < k) (hk : k ≤ L) :
    valid (wordPrefix q k) = true := by
  cases k with
  | zero => omega
  | succ k =>
      simp only [wordPrefix, segment, valid, Bool.and_eq_true, decide_eq_true_eq]
      refine ⟨⟨?_, hq.2.2.1 0 hq.1⟩, ?_⟩
      · have h := hq.2.1
        omega
      · apply segment_all_bounded q 1 k
        intro i hi
        exact hq.2.2.1 (1 + i) (by omega)

theorem survives_step_of (n : Nat) (s r : List Nat) (e : Nat) (he : e ≤ 1)
    (hc : compatible s r e = true)
    (hs : valid (forwardPrefix s e) = true)
    (hr : valid (forwardPrefix r e) = true)
    (hn : survives n (forwardPrefix s e) (forwardPrefix r e) = true) :
    survives (n + 1) s r = true := by
  have hb : e = 0 ∨ e = 1 := by omega
  rcases hb with hb | hb
  · subst e
    simp [survives, hc, hs, hr, hn]
  · subst e
    simp [survives, hc, hs, hr, hn]

theorem survives_of_trajectory (s r : Nat → List Nat) (bits : Nat → Nat) (K : Nat)
    (hb : ∀ t, t < K → bits t ≤ 1)
    (hv : ∀ t, t ≤ K → valid (s t) = true ∧ valid (r t) = true)
    (hc : ∀ t, t < K → compatible (s t) (r t) (bits t) = true)
    (hs : ∀ t, t < K → s (t + 1) = forwardPrefix (s t) (bits t))
    (hr : ∀ t, t < K → r (t + 1) = forwardPrefix (r t) (bits t)) :
    survives K (s 0) (r 0) = true := by
  induction K generalizing s r bits with
  | zero => rfl
  | succ K ih =>
      apply survives_step_of K (s 0) (r 0) (bits 0) (hb 0 (by omega)) (hc 0 (by omega))
      · rw [← hs 0 (by omega)]
        exact (hv 1 (by omega)).1
      · rw [← hr 0 (by omega)]
        exact (hv 1 (by omega)).2
      · rw [← hs 0 (by omega), ← hr 0 (by omega)]
        exact ih (fun t => s (t + 1)) (fun t => r (t + 1))
          (fun t => bits (t + 1))
          (by intro t ht; exact hb (t + 1) (by omega))
          (by intro t ht; exact hv (t + 1) (by omega))
          (by intro t ht; exact hc (t + 1) (by omega))
          (by intro t ht; exact hs (t + 1) (by omega))
          (by intro t ht; exact hr (t + 1) (by omega))

/-- Complete equal actual carry histories survive the executable prefix
checker at every positive prefix length contained in the initial width. -/
theorem actual_history_survives (q r : Nat → Nat) (L k K : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hk0 : 0 < k) (hk : k ≤ L)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    survives K (wordPrefix q k) (wordPrefix r k) = true := by
  let statesQ : Nat → List Nat := fun t => wordPrefix (iterPairs q L t).2 k
  let statesR : Nat → List Nat := fun t => wordPrefix (iterPairs r L t).2 k
  let bits : Nat → Nat := fun t =>
    carry (iterPairs q L t).2 ((iterPairs q L t).1 - k)
  have hw : ∀ t, t ≤ K → (iterPairs q L t).1 = (iterPairs r L t).1 := by
    intro t ht
    exact matched_widths q r L t (fun j hj => hc j (by omega))
  have hwq : ∀ t, k ≤ (iterPairs q L t).1 := by
    intro t
    exact Nat.le_trans hk (iterPairs_width_ge_initial q L t)
  have hwr : ∀ t, k ≤ (iterPairs r L t).1 := by
    intro t
    exact Nat.le_trans hk (iterPairs_width_ge_initial r L t)
  have hbits : ∀ t, t < K → bits t =
      carry (iterPairs r L t).2 ((iterPairs r L t).1 - k) := by
    intro t ht
    dsimp only [bits]
    rw [← hw t (by omega)]
    exact hc t ht _ (by omega)
  apply survives_of_trajectory statesQ statesR bits K
  · intro t _
    exact carry_bounded _ _ (iterPairs_admissible q L t hq).2.2.1 _ (by omega)
  · intro t _
    exact ⟨valid_prefix _ _ k (iterPairs_admissible q L t hq) hk0 (hwq t),
      valid_prefix _ _ k (iterPairs_admissible r L t hr) hk0 (hwr t)⟩
  · intro t ht
    have har : Admissible (iterPairs q L t).1 (iterPairs r L t).2 := by
      rw [hw t (by omega)]
      exact iterPairs_admissible r L t hr
    exact actual_compatible _ _ _ k (iterPairs_admissible q L t hq) har
      (hwq t) (hc t ht)
  · intro t _
    exact (actual_forwardPrefix _ _ k (iterPairs_admissible q L t hq) (hwq t)).symm
  · intro t ht
    dsimp only [statesR]
    rw [hbits t ht]
    exact (actual_forwardPrefix _ _ k (iterPairs_admissible r L t hr) (hwr t)).symm

#print axioms prefix_low_carry
#print axioms prefix_high_carry
#print axioms actual_compatible
#print axioms valid_prefix
#print axioms survives_of_trajectory
#print axioms actual_history_survives

end EightCarryMaximalWidth.PrefixHistory
