import P196.Drafts.Agent3ThreeLayerPrefix.ActualDepth
import P196.Drafts.Agent3ThreeLayerPrefix.SharpHistoryFamily

/-!
Sharpness of the two incoming layers for a finite-horizon subfamily.
The exact depth is relative to the original bounded, equal-half-width,
zero-carry ActualFiber relation. Numeric conclusions concern ordinary
positive finite integers and a prescribed finite horizon.
-/

namespace P196.Agent3.ThreeLayer

open Agent8 Lychrel196
open P196.Agent9.InverseFibers
open P196.Agent3.OverflowHorizon P196.Agent3.TwoHistory

/-- Two actual incoming layers exist and no three such layers exist.
Every edge is the unchanged original `ActualFiber` relation. -/
def ExactlyTwoZeroCarryLayers (ss : List Symbol) : Prop :=
  (∃ a b : List Symbol,
    ActualFiber ss (a.map Fin.val) ∧ ActualFiber a (b.map Fin.val)) ∧
  ¬ (∃ a b : List Symbol, ∃ c : List Nat,
    ActualFiber ss (a.map Fin.val) ∧ ActualFiber a (b.map Fin.val) ∧
    ActualFiber b c)

theorem historyTarget_exact_depth (free : List Bool) (k : Nat) :
    ExactlyTwoZeroCarryLayers (historyTarget (depthBits free) k) := by
  refine ⟨history_has_two_actual_layers (depthBits free) k, ?_⟩
  rintro ⟨a, b, c, h⟩
  exact no_three_actual_histories free k a b c h

theorem historyTarget_mirror (xs : List Bool) (k : Nat) :
    mirror ((historyTarget xs k).map Fin.val) = historyWord2 xs k := by
  rw [historyTarget_values]
  rfl

theorem sharp_protected_exact_depth (m k : Nat) (w : Word)
    (hw : w ∈ sharpHistoryFamily2 m k) :
    ∃ ss : List Symbol, mirror (ss.map Fin.val) = w ∧
      ExactlyTwoZeroCarryLayers ss := by
  obtain ⟨xs, _, rfl⟩ := (mem_sharpHistoryFamily2_iff w m k).mp hw
  exact ⟨historyTarget (depthBits xs) k, historyTarget_mirror _ k,
    historyTarget_exact_depth xs k⟩

/-- The equal-width premise is stated in full-word form as `2*ys.length`.
The candidate predecessor is the literal mirrored half `ys`. -/
theorem sharp_initial_no_zero_predecessor (m k : Nat) (w : Word)
    (hw : w ∈ sharpHistoryFamily0 m k) (ys : List Nat)
    (hlen : 2 * ys.length = w.length)
    (hb : ∀ y ∈ ys, y < 19)
    (hc : terminalCarry (mirror ys) 0 = 0) :
    stepWord (mirror ys) ≠ w := by
  obtain ⟨xs, _, rfl⟩ := (mem_sharpHistoryFamily0_iff w m k).mp hw
  have hh : (historyWord0 (depthBits xs) k).length =
      2 * (historyHalf0 (depthBits xs) k).length := by
    simp only [historyWord0, mirror, List.length_append, List.length_reverse]
    omega
  have hy : ys.length = (historyHalf0 (depthBits xs) k).length := by
    change 2 * ys.length = (historyWord0 (depthBits xs) k).length at hlen
    omega
  exact historyWord0_no_zero_predecessor xs k ys hy hb hc

theorem sharp_initial_canonical_chain (m k : Nat) (hk : 0 < k)
    (w : Word) (hw : w ∈ sharpHistoryFamily0 m k) :
    ∃ v q : Word,
      CanonicalPair v ∧ CanonicalPair q ∧
      v.length = w.length ∧ q.length = w.length ∧
      q ∈ sharpHistoryFamily2 m k ∧
      stepWord w = v ∧ stepWord v = q ∧
      terminalCarry w 0 = 0 ∧ terminalCarry v 0 = 0 ∧
      terminalCarry q 0 = 1 ∧ stepWord q = target (m + 9) k := by
  obtain ⟨xs, hlen, rfl⟩ := (mem_sharpHistoryFamily0_iff w m k).mp hw
  have hl : ([true, true, false] ++ xs).length + 6 = m + 9 := by
    simp only [List.length_append, List.length_cons, List.length_nil, hlen]
    omega
  refine ⟨historyWord1 ([true, true, false] ++ xs) k,
    historyWord2 ([true, true, false] ++ xs) k,
    historyWord1_canonical _ k, historyWord2_canonical _ k, ?_, ?_, ?_,
    historyWord0_step _ k, historyWord1_step _ k,
    historyWord0_final_carry _ k, historyWord1_final_carry _ k,
    historyWord2_final_carry _ k, ?_⟩
  · rw [historyWord1_length, historyWord0_length]
  · rw [historyWord2_length, historyWord0_length]
  · exact (mem_sharpHistoryFamily2_iff _ m k).mpr ⟨xs, hlen, rfl⟩
  · simpa only [hl] using historyWord2_step ([true, true, false] ++ xs) k hk

/-- The exact finite family has two zero-carry incoming layers and no
third in the original ActualFiber domain. Every ordinary realization
of every listed initial word has the stated finite safety and common value. -/
theorem finite_horizon_exact_two_history_family (m k : Nat) (hk : 0 < k) :
    (sharpHistoryFamily0 m k).length = 2 ^ m ∧
    (sharpHistoryFamily0 m k).Nodup ∧
    (sharpHistoryFamily2 m k).length = 2 ^ m ∧
    (sharpHistoryFamily2 m k).Nodup ∧
    (sharpHistoryFamily0 m k).map (fun w => stepWord (stepWord w)) =
      sharpHistoryFamily2 m k ∧
    (∀ w ∈ sharpHistoryFamily2 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 10) ∧ w.length % 2 = 0 ∧
      ∃ ss : List Symbol, mirror (ss.map Fin.val) = w ∧
        ExactlyTwoZeroCarryLayers ss) ∧
    (∀ w ∈ sharpHistoryFamily0 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 10) ∧ w.length % 2 = 0 ∧
      (∃ n, 0 < n ∧ IntegerRealizes n w) ∧
      (∀ n, IntegerRealizes n w →
        0 < n ∧ (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
        orbit n 4 = digitValue (target (m + 9) k)) ∧
      (∀ ys : List Nat, 2 * ys.length = w.length →
        (∀ y ∈ ys, y < 19) → terminalCarry (mirror ys) 0 = 0 →
        stepWord (mirror ys) ≠ w)) := by
  refine ⟨sharpHistoryFamily0_length m k, sharpHistoryFamily0_nodup m k,
    sharpHistoryFamily2_length m k, sharpHistoryFamily2_nodup m k,
    sharpHistoryFamilies_two_step m k, ?_, ?_⟩
  · intro w hw
    have hp := sharpHistoryFamily2_member_properties m k w hw
    exact ⟨hp.1, hp.2.1, hp.2.2, sharp_protected_exact_depth m k w hw⟩
  · intro w hw
    have hp := sharpHistoryFamily0_member_properties m k w hw
    exact ⟨hp.1, hp.2.1, hp.2.2, sharp_initial_integer_exists m k w hw,
      sharp_initial_integer_package m k hk w hw,
      sharp_initial_no_zero_predecessor m k w hw⟩

end P196.Agent3.ThreeLayer
