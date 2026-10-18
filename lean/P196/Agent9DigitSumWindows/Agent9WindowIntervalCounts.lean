import Std

/-!
Finite counting from a uniformly bounded waiting time.
Intervals are half-open: `List.range' s N` lists exactly the times in `[s,s+N)`.
The proof counts complete disjoint blocks; it does not assert a density limit.
-/

namespace P196.Agent9.IntervalCounts

/-- Number of times satisfying `P` in the half-open interval `[s,s+N)`. -/
def intervalCount (P : Nat → Prop) [DecidablePred P] (s N : Nat) : Nat :=
  ((List.range' s N).filter (fun t => decide (P t))).length

/-- Adjacent half-open intervals concatenate without a duplicated endpoint. -/
theorem intervalCount_append (P : Nat → Prop) [DecidablePred P]
    (s N M : Nat) :
    intervalCount P s (N + M) =
      intervalCount P s N + intervalCount P (s + N) M := by
  unfold intervalCount
  rw [← List.range'_append_1, List.filter_append, List.length_append]

/-- Appending a remainder can only increase the count. -/
theorem intervalCount_mono_length (P : Nat → Prop) [DecidablePred P]
    (s N M : Nat) (hNM : N ≤ M) :
    intervalCount P s N ≤ intervalCount P s M := by
  have he : M = N + (M - N) := by omega
  rw [he, intervalCount_append]
  exact Nat.le_add_right _ _

/-- A witness strictly before the right endpoint contributes at least one. -/
theorem intervalCount_positive_of_witness (P : Nat → Prop) [DecidablePred P]
    (s H : Nat) (hw : ∃ t, s ≤ t ∧ t < s + H ∧ P t) :
    1 ≤ intervalCount P s H := by
  obtain ⟨t, hlo, hhi, hp⟩ := hw
  have hm : t ∈ (List.range' s H).filter (fun u => decide (P u)) := by
    simp only [List.mem_filter, List.mem_range'_1, decide_eq_true_eq]
    exact ⟨⟨hlo, hhi⟩, hp⟩
  exact List.length_pos_of_mem hm

/-- Every complete block contributes, with no choice of global witness sequence. -/
theorem window_property_complete_blocks (P : Nat → Prop) [DecidablePred P]
    (H : Nat) (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t)
    (s J : Nat) :
    J ≤ intervalCount P s (J * H) := by
  induction J with
  | zero => simp [intervalCount]
  | succ J ih =>
    have hlast := intervalCount_positive_of_witness P (s + J * H) H
      (hw (s + J * H))
    rw [Nat.succ_mul, intervalCount_append]
    omega

/-- Exact finite consequence of a positive uniform window length.
The right side counts all qualifying times in `[s,s+N)`, including `s=0` or `N=0`. -/
theorem window_property_interval_count (P : Nat → Prop) [DecidablePred P]
    (H : Nat) (hH : 0 < H)
    (hw : ∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t)
    (s N : Nat) :
    N / H ≤ ((List.range' s N).filter (fun t => decide (P t))).length := by
  have hprefix : (N / H) * H ≤ N :=
    (Nat.le_div_iff_mul_le hH).mp (Nat.le_refl (N / H))
  exact Nat.le_trans (window_property_complete_blocks P H hw s (N / H))
    (intervalCount_mono_length P s ((N / H) * H) N hprefix)

#print axioms intervalCount_append
#print axioms intervalCount_mono_length
#print axioms intervalCount_positive_of_witness
#print axioms window_property_complete_blocks
#print axioms window_property_interval_count

end P196.Agent9.IntervalCounts
