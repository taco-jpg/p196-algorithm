import P196.Drafts.Misc.Agent100GroupIISafety

/-!
已有第一组 (p,u,v)=(1,1,6) 修复与第二组 (4,5,5) 的有限组合。
结论只覆盖两个延迟修复和四次正时间非回文输出。
-/

namespace Agent100.DoubleGate

set_option maxHeartbeats 2000000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

abbrev initial (r : Nat) : Nat → Nat := DelayedOverlapGate.initial r 1 1 6
abbrev atFour (r : Nat) : Nat → Nat := GroupII.returned r 4 5 5

theorem first_domain (r : Nat) (hr : 1 ≤ r) :
    DelayedOverlapGate.Domain r 1 1 6 := by
  unfold DelayedOverlapGate.Domain
  omega

theorem second_domain (r : Nat) (hr : 1 ≤ r) : GroupII.Domain r 4 5 5 := by
  unfold GroupII.Domain
  omega

/-- 旧六核域的不闭合并未排除这个新的七核域。 -/
theorem handoff_word (r i : Nat) :
    DelayedOverlapGate.returned r 1 1 6 i = DelayedOverlapGate.initial r 4 5 5 i := by
  rfl

theorem iterPairs_add (q : Nat → Nat) (L a b : Nat) :
    iterPairs q L (a + b) =
      iterPairs (iterPairs q L a).2 (iterPairs q L a).1 b := by
  induction b with
  | zero => exact (Prod.eta _).symm
  | succ b ih =>
      rw [Nat.add_succ]
      exact congrArg (fun s : Nat × (Nat → Nat) =>
        (nextWidth s.2 s.1, nextColumns s.2 s.1)) ih

/-- 有限已表示前缀足以拼接下一段，不对函数的无关无限尾部作假设。 -/
theorem two_steps_from_matching (q s m t : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hs : carry s L = 0) (hm : carry m L = 0)
    (he : ∀ i, i < L → q i = s i)
    (hsm : ∀ i, i < L → nextColumns s L i = m i)
    (hmt : ∀ i, i < L → nextColumns m L i = t i) :
    (iterPairs q L 2).1 = L ∧
      ∀ i, i < L → (iterPairs q L 2).2 i = t i := by
  have hq := (carry_congr_upto q s L he L (Nat.le_refl _)).trans hs
  have hcongr := DelayedOverlapGate.no_overflow_next_congr q s L hL hs he
  exact DelayedOverlapGate.two_steps_of_explicit_columns q m t L hL hq hm
    (fun i hi => (hcongr.2 i hi).trans (hsm i hi)) hmt

theorem component_four_return (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 4).1 =
        2 * r + 6 ∧
      ∀ i, i < 2 * r + 6 →
        (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 4).2 i =
          GroupII.returnedComponent r 4 5 5 i := by
  have hf := DelayedOverlapGate.component_two_step_return r 1 1 6 (first_domain r hr)
  have he : ∀ i, i < 2 * r + 6 →
      (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).2 i =
        DelayedOverlapGate.component r 4 5 5 i := hf.2
  rw [iterPairs_add _ _ 2 2, hf.1]
  exact two_steps_from_matching _ _ _ _ _ (by omega)
    (GroupII.component_no_overflow r 4 5 5 (second_domain r hr))
    (GroupII.component_double_no_overflow r 4 5 5 (second_domain r hr)) he
    (GroupII.component_next r 4 5 5 (second_domain r hr))
    (GroupII.component_double_next r 4 5 5 (second_domain r hr))

theorem whole_handoff (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (initial r) (2 * r + 7) 2).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (iterPairs (initial r) (2 * r + 7) 2).2 i =
        DelayedOverlapGate.initial r 4 5 5 i := by
  have hf := DelayedOverlapGate.whole_two_step_return r 1 1 6 (first_domain r hr)
  refine ⟨hf.1, ?_⟩
  intro i hi
  exact (hf.2 i hi).trans (DelayedOverlapGate.initial_is_overlap r 4 5 5 hr i).symm

theorem whole_four_return (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (initial r) (2 * r + 7) 4).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (iterPairs (initial r) (2 * r + 7) 4).2 i =
        atFour r i := by
  have hf := whole_handoff r hr
  rw [iterPairs_add _ _ 2 2, hf.1]
  exact two_steps_from_matching _ _ _ _ _ (by omega)
    (GroupII.initial_no_overflow r 4 5 5 (second_domain r hr))
    (GroupII.middle_no_overflow r 4 5 5 (second_domain r hr)) hf.2
    (GroupII.initial_next r 4 5 5 (second_domain r hr))
    (GroupII.middle_next r 4 5 5 (second_domain r hr))

theorem whole_three (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (initial r) (2 * r + 7) 3).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (iterPairs (initial r) (2 * r + 7) 3).2 i =
        GroupII.middle r 4 5 5 i := by
  have hf := whole_handoff r hr
  have hc := DelayedOverlapGate.no_overflow_next_congr
    (iterPairs (initial r) (2 * r + 7) 2).2
    (DelayedOverlapGate.initial r 4 5 5) (2 * r + 7) (by omega)
    (GroupII.initial_no_overflow r 4 5 5 (second_domain r hr)) hf.2
  change nextWidth (iterPairs (initial r) (2 * r + 7) 2).2
      (iterPairs (initial r) (2 * r + 7) 2).1 = 2 * r + 7 ∧
    ∀ i, i < 2 * r + 7 →
      nextColumns (iterPairs (initial r) (2 * r + 7) 2).2
        (iterPairs (initial r) (2 * r + 7) 2).1 i = GroupII.middle r 4 5 5 i
  rw [hf.1]
  exact ⟨hc.1, fun i hi => (hc.2 i hi).trans
    (GroupII.initial_next r 4 5 5 (second_domain r hr) i hi)⟩

theorem component_three (r : Nat) (hr : 1 ≤ r) :
    (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 3).1 =
        2 * r + 6 ∧
      ∀ i, i < 2 * r + 6 →
        (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 3).2 i =
          DelayedOverlapGate.component r 8 10 10 i := by
  have hf := DelayedOverlapGate.component_two_step_return r 1 1 6 (first_domain r hr)
  have he : ∀ i, i < 2 * r + 6 →
      (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).2 i =
        DelayedOverlapGate.component r 4 5 5 i := hf.2
  have hc := DelayedOverlapGate.no_overflow_next_congr
    (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).2
    (DelayedOverlapGate.component r 4 5 5) (2 * r + 6) (by omega)
    (GroupII.component_no_overflow r 4 5 5 (second_domain r hr)) he
  change nextWidth (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).2
      (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).1 = 2 * r + 6 ∧
    ∀ i, i < 2 * r + 6 →
      nextColumns (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).2
        (iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) 2).1 i =
          DelayedOverlapGate.component r 8 10 10 i
  rw [hf.1]
  exact ⟨hc.1, fun i hi => (hc.2 i hi).trans
    (GroupII.component_next r 4 5 5 (second_domain r hr) i hi)⟩

/-- 第二次修复之前确实再次偏离重叠；差异发生在列 r+1。 -/
theorem time_three_overlap_fails (r : Nat) (hr : 1 ≤ r) :
    ¬ ∀ i, i < 2 * r + 7 → (iterPairs (initial r) (2 * r + 7) 3).2 i =
      DelayedOverlapGate.shiftOne (DelayedOverlapGate.component r 8 10 10) i := by
  intro he
  have hx := he (r + 1) (by omega)
  rw [(whole_three r hr).2 (r + 1) (by omega),
    ← DelayedOverlapGate.initial_is_overlap r 8 10 10 hr (r + 1)] at hx
  simp only [GroupII.middle, DelayedOverlapGate.initial, DelayedOverlapGate.fiveWord,
    true_or, if_true] at hx
  repeat (first | omega | split at hx)

theorem numeric_handoff (n : Nat) (d : Nat → Nat) (r : Nat) (hr : 1 ≤ r)
    (hc : Canonical n d (2 * r + 7))
    (hq : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 →
        columnSum e (2 * r + 7) i = DelayedOverlapGate.initial r 4 5 5 i := by
  obtain ⟨e, he, hrep⟩ := DelayedOverlapGate.numeric_return n d r 1 1 6
    (first_domain r hr) hc hq
  exact ⟨e, he, fun i hi => (hrep i hi).trans (handoff_word r i)⟩

theorem numeric_four_return (n : Nat) (d : Nat → Nat) (r : Nat) (hr : 1 ≤ r)
    (hc : Canonical n d (2 * r + 7))
    (hq : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r i) :
    ∃ e, Canonical (orbit n 4) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = atFour r i := by
  obtain ⟨e, he, hrep⟩ := numeric_handoff n d r hr hc hq
  have hout := GroupII.numeric_return (orbit n 2) e r 4 5 5
    (second_domain r hr) he hrep
  simpa only [← LychrelCertificates.orbit_add] using hout

/-- 无论如何拆分初始 pair sums，四个普通十进制输出都安全。 -/
theorem numeric_four_step_safety (n : Nat) (d : Nat → Nat) (r : Nat) (hr : 1 ≤ r)
    (hc : Canonical n d (2 * r + 7))
    (hq : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r i) :
    ∀ k, 1 ≤ k → k ≤ 4 → ¬ Palindrome (orbit n k) := by
  have hfirst := DelayedOverlapGate.numeric_two_step_safety n d r 1 1 6
    (first_domain r hr) hc hq
  obtain ⟨e, he, hrep⟩ := numeric_handoff n d r hr hc hq
  have hsecond := GroupII.numeric_two_step_safety (orbit n 2) e r 4 5 5
    (second_domain r hr) he hrep
  have hthree : ¬ Palindrome (orbit n 3) := by
    simpa only [← LychrelCertificates.orbit_add] using hsecond.1
  have hfour : ¬ Palindrome (orbit n 4) := by
    simpa only [← LychrelCertificates.orbit_add] using hsecond.2
  intro k hk0 hk4
  have hk : k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by omega
  rcases hk with rfl | rfl | rfl | rfl
  · exact hfirst.1
  · exact hfirst.2
  · exact hthree
  · exact hfour

theorem realized_safe_double_gate (r : Nat) (hr : 1 ≤ r) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r i) ∧
      (∀ k, 1 ≤ k → k ≤ 4 → ¬ Palindrome (orbit n k)) ∧
      (∃ e, Canonical (orbit n 4) e (2 * r + 7) ∧
        ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = atFour r i) := by
  have ha := DelayedOverlapGate.initial_admissible r 1 1 6 (first_domain r hr)
  obtain ⟨n, d, hn, hc, hrep⟩ := valid_word_realizable (initial r) (2 * r + 7)
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  exact ⟨n, d, hn, hc, hrep, numeric_four_step_safety n d r hr hc hrep,
    numeric_four_return n d r hr hc hrep⟩

end Agent100.DoubleGate

#print axioms Agent100.DoubleGate.first_domain
#print axioms Agent100.DoubleGate.second_domain
#print axioms Agent100.DoubleGate.handoff_word
#print axioms Agent100.DoubleGate.iterPairs_add
#print axioms Agent100.DoubleGate.two_steps_from_matching
#print axioms Agent100.DoubleGate.component_four_return
#print axioms Agent100.DoubleGate.whole_handoff
#print axioms Agent100.DoubleGate.whole_four_return
#print axioms Agent100.DoubleGate.whole_three
#print axioms Agent100.DoubleGate.component_three
#print axioms Agent100.DoubleGate.time_three_overlap_fails
#print axioms Agent100.DoubleGate.numeric_handoff
#print axioms Agent100.DoubleGate.numeric_four_return
#print axioms Agent100.DoubleGate.numeric_four_step_safety
#print axioms Agent100.DoubleGate.realized_safe_double_gate
