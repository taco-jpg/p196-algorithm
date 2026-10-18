import P196.Drafts.Agent100GroupIIOverlap.Agent100GroupIIDynamics

/-!
第二组延迟重叠修复的普通十进制语义。安全性指两次正时间输出；
不要求初始整数本身非回文，也不把有限修复解释成无限递归。
-/

namespace Agent100.GroupII

set_option maxHeartbeats 2000000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem initial_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 7) (DelayedOverlapGate.initial r p u v) := by
  unfold Domain at h
  exact DelayedOverlapGate.fiveWord_admissible r p u (u + v) (2 * v)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem middle_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 7) (middle r p u v) := by
  unfold Domain at h
  exact DelayedOverlapGate.fiveWord_admissible r (2 * p) (2 * u + 1)
    (2 * (u + v) - 19) (4 * v - 18)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem initial_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2 * r + 7) (DelayedOverlapGate.initial r p u v) := by
  have hc : DelayedOverlapGate.initial r p u v (r + 3) = 2 * v :=
    DelayedOverlapGate.fiveWord_center r p u (u + v) (2 * v) h.1
  have ho : DelayedOverlapGate.initial r p u v 0 = p :=
    DelayedOverlapGate.fiveWord_zero _ _ _ _ _
  unfold Domain at h
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r + 3) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

theorem middle_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2 * r + 7) (middle r p u v) := by
  have hc : middle r p u v (r + 1) = 2 * u + 1 := by
    have hr := h.1
    simp only [middle, DelayedOverlapGate.fiveWord, true_or, if_true]
    repeat (first | omega | split)
  have ho : middle r p u v 0 = 2 * p :=
    DelayedOverlapGate.fiveWord_zero _ _ _ _ _
  unfold Domain at h
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r + 1) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

/-- 每个普通整数实现的一次真实输出具有已算出的中间 pair word。 -/
theorem numeric_middle (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r p u v i) :
    ∃ e, Canonical (orbit n 1) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = middle r p u v i := by
  have hw : nextWidth (DelayedOverlapGate.initial r p u v) (2 * r + 7) =
      2 * r + 7 := by
    simp only [nextWidth, initial_no_overflow r p u v h, if_true]
  obtain ⟨e, he, hrep⟩ := representation_next n d
    (DelayedOverlapGate.initial r p u v) (2 * r + 7) hc hr
  rw [hw] at he hrep
  exact ⟨e, he, fun i hi => (hrep i hi).trans (initial_next r p u v h i hi)⟩

/-- 第二次真实输出是完整 returned word；最短间隔的加法也包含在内。 -/
theorem numeric_return (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = returned r p u v i := by
  obtain ⟨e, he, hrep⟩ := numeric_middle n d r p u v h hc hr
  have hw : nextWidth (middle r p u v) (2 * r + 7) = 2 * r + 7 := by
    simp only [nextWidth, middle_no_overflow r p u v h, if_true]
  obtain ⟨f, hf, hfrep⟩ := representation_next (orbit n 1) e
    (middle r p u v) (2 * r + 7) he hrep
  rw [hw] at hf hfrep
  exact ⟨f, hf, fun i hi => (hfrep i hi).trans (middle_next r p u v h i hi)⟩

theorem numeric_two_step_safety (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r p u v i) :
    ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) := by
  constructor
  · intro hp
    exact initial_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad n d
        (DelayedOverlapGate.initial r p u v) (2 * r + 7) hc hr).mp hp)
  · obtain ⟨e, he, hrep⟩ := numeric_middle n d r p u v h hc hr
    intro hp
    exact middle_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad (orbit n 1) e (middle r p u v)
        (2 * r + 7) he hrep).mp hp)

/-- 给定域中的每个参数，都有真正的有限正整数实现；实现前提已解除。 -/
theorem realized_safe_gate (r p u v : Nat) (h : Domain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 →
        columnSum d (2 * r + 7) i = DelayedOverlapGate.initial r p u v i) ∧
      ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) ∧
      (∃ e, Canonical (orbit n 2) e (2 * r + 7) ∧
        ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = returned r p u v i) := by
  have ha := initial_admissible r p u v h
  obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable
    (DelayedOverlapGate.initial r p u v) (2 * r + 7)
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  have hs := numeric_two_step_safety n d r p u v h hc hr
  exact ⟨n, d, hn, hc, hr, hs.1, hs.2, numeric_return n d r p u v h hc hr⟩

#print axioms initial_admissible
#print axioms middle_admissible
#print axioms initial_not_bad
#print axioms middle_not_bad
#print axioms numeric_middle
#print axioms numeric_return
#print axioms numeric_two_step_safety
#print axioms realized_safe_gate

end Agent100.GroupII
