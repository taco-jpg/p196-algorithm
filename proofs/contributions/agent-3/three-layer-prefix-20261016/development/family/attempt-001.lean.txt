import TwoHistoryTheorem

/-!
An exact subfamily obtained by fixing the first three free choices to
true, true, false. The resulting protected target starts 14,14,14,5.
This module reuses the checked two-history construction for enumeration
and ordinary finite-horizon safety. The ancestry exclusion is separate.
-/

namespace P196.Agent3.ThreeLayer

open Agent8 Lychrel196
open P196.Agent3.OverflowHorizon P196.Agent3.TwoHistory

def sharpHistoryFamily0 (m k : Nat) : List Word :=
  (allBits m).map (fun xs => historyWord0 ([true, true, false] ++ xs) k)

def sharpHistoryFamily2 (m k : Nat) : List Word :=
  (allBits m).map (fun xs => historyWord2 ([true, true, false] ++ xs) k)

theorem sharpWord0_injective (k : Nat) (xs ys : List Bool)
    (h : historyWord0 ([true, true, false] ++ xs) k =
      historyWord0 ([true, true, false] ++ ys) k) : xs = ys := by
  have hp := historyWord0_injective k _ _ h
  simpa using hp

theorem sharpWord2_injective (k : Nat) (xs ys : List Bool)
    (h : historyWord2 ([true, true, false] ++ xs) k =
      historyWord2 ([true, true, false] ++ ys) k) : xs = ys := by
  have hp := historyWord2_injective k _ _ h
  simpa using hp

theorem sharpHistoryFamily0_length (m k : Nat) :
    (sharpHistoryFamily0 m k).length = 2 ^ m := by
  simp only [sharpHistoryFamily0, List.length_map, allBits_length]

theorem sharpHistoryFamily2_length (m k : Nat) :
    (sharpHistoryFamily2 m k).length = 2 ^ m := by
  simp only [sharpHistoryFamily2, List.length_map, allBits_length]

theorem sharpHistoryFamily0_nodup (m k : Nat) :
    (sharpHistoryFamily0 m k).Nodup := by
  exact List.Pairwise.map (fun xs => historyWord0 ([true, true, false] ++ xs) k)
    (fun xs ys hne heq => hne (sharpWord0_injective k xs ys heq))
    (allBits_nodup m)

theorem sharpHistoryFamily2_nodup (m k : Nat) :
    (sharpHistoryFamily2 m k).Nodup := by
  exact List.Pairwise.map (fun xs => historyWord2 ([true, true, false] ++ xs) k)
    (fun xs ys hne heq => hne (sharpWord2_injective k xs ys heq))
    (allBits_nodup m)

theorem mem_sharpHistoryFamily0_iff (w : Word) (m k : Nat) :
    w ∈ sharpHistoryFamily0 m k ↔ ∃ xs : List Bool,
      xs.length = m ∧ historyWord0 ([true, true, false] ++ xs) k = w := by
  simp only [sharpHistoryFamily0, List.mem_map, mem_allBits_iff]

theorem mem_sharpHistoryFamily2_iff (w : Word) (m k : Nat) :
    w ∈ sharpHistoryFamily2 m k ↔ ∃ xs : List Bool,
      xs.length = m ∧ historyWord2 ([true, true, false] ++ xs) k = w := by
  simp only [sharpHistoryFamily2, List.mem_map, mem_allBits_iff]

theorem sharpHistoryFamily0_member_properties (m k : Nat) (w : Word)
    (hw : w ∈ sharpHistoryFamily0 m k) :
    CanonicalPair w ∧ w.length = 2 * (m + k + 10) ∧ w.length % 2 = 0 := by
  obtain ⟨xs, hlen, rfl⟩ := (mem_sharpHistoryFamily0_iff w m k).mp hw
  refine ⟨historyWord0_canonical _ k, ?_, historyWord0_even _ k⟩
  rw [historyWord0_length]
  simp only [List.length_append, List.length_cons, List.length_nil, hlen]
  omega

theorem sharpHistoryFamily2_member_properties (m k : Nat) (w : Word)
    (hw : w ∈ sharpHistoryFamily2 m k) :
    CanonicalPair w ∧ w.length = 2 * (m + k + 10) ∧ w.length % 2 = 0 := by
  obtain ⟨xs, hlen, rfl⟩ := (mem_sharpHistoryFamily2_iff w m k).mp hw
  refine ⟨historyWord2_canonical _ k, ?_, historyWord2_even _ k⟩
  rw [historyWord2_length]
  simp only [List.length_append, List.length_cons, List.length_nil, hlen]
  omega

theorem sharpHistoryFamilies_two_step (m k : Nat) :
    (sharpHistoryFamily0 m k).map (fun w => stepWord (stepWord w)) =
      sharpHistoryFamily2 m k := by
  simp only [sharpHistoryFamily0, sharpHistoryFamily2, List.map_map,
    Function.comp_def, historyWord0_step, historyWord1_step]

theorem sharp_initial_integer_exists (m k : Nat) (w : Word)
    (hw : w ∈ sharpHistoryFamily0 m k) :
    ∃ n, 0 < n ∧ IntegerRealizes n w := by
  have hp := sharpHistoryFamily0_member_properties m k w hw
  exact even_canonical_realizable w hp.1 hp.2.2

theorem sharp_initial_integer_package (m k : Nat) (hk : 0 < k)
    (w : Word) (hw : w ∈ sharpHistoryFamily0 m k)
    (n : Nat) (hr : IntegerRealizes n w) :
    0 < n ∧ (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
      orbit n 4 = digitValue (target (m + 9) k) := by
  obtain ⟨xs, hlen, rfl⟩ := (mem_sharpHistoryFamily0_iff w m k).mp hw
  have hl : ([true, true, false] ++ xs).length + 6 = m + 9 := by
    simp only [List.length_append, List.length_cons, List.length_nil, hlen]
    omega
  simpa only [hl] using
    history_integer_realization_package ([true, true, false] ++ xs) k hk n hr

/-- The inherited count and safety assertions, before adding the independently
proved obstruction to a third zero-carry incoming layer. -/
theorem sharp_finite_horizon_family (m k : Nat) (hk : 0 < k) :
    (sharpHistoryFamily0 m k).length = 2 ^ m ∧
    (sharpHistoryFamily0 m k).Nodup ∧
    (sharpHistoryFamily2 m k).length = 2 ^ m ∧
    (sharpHistoryFamily2 m k).Nodup ∧
    (sharpHistoryFamily0 m k).map (fun w => stepWord (stepWord w)) =
      sharpHistoryFamily2 m k ∧
    ∀ w ∈ sharpHistoryFamily0 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 10) ∧ w.length % 2 = 0 ∧
      (∃ n, 0 < n ∧ IntegerRealizes n w) ∧
      (∀ n, IntegerRealizes n w →
        0 < n ∧ (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
        orbit n 4 = digitValue (target (m + 9) k)) := by
  refine ⟨sharpHistoryFamily0_length m k, sharpHistoryFamily0_nodup m k,
    sharpHistoryFamily2_length m k, sharpHistoryFamily2_nodup m k,
    sharpHistoryFamilies_two_step m k, ?_⟩
  intro w hw
  have hp := sharpHistoryFamily0_member_properties m k w hw
  exact ⟨hp.1, hp.2.1, hp.2.2, sharp_initial_integer_exists m k w hw,
    sharp_initial_integer_package m k hk w hw⟩

end P196.Agent3.ThreeLayer
