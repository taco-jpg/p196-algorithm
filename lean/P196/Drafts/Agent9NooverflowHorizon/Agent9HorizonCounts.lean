import P196.Drafts.Agent9NooverflowHorizon.Agent9HorizonDefinitions

namespace P196.Agent9.NoOverflowHorizon

open InverseFibers

set_option maxHeartbeats 4000000

theorem targetHalf_length (m k : Nat) :
    (targetHalf m k).length = m + k + 1 := by
  simp [targetHalf, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

theorem mirror_length (xs : List Nat) : (mirror xs).length = 2 * xs.length := by
  simp [mirror, Nat.two_mul]

/-- An eighteen target column keeps precisely the total accepted at an even
center. Other states may be deleted; no preservation of the full vector is used. -/
theorem advance_eighteen_U (v : Counts) : (advance 18 v).U = v.U := by
  rw [advance_formula]
  rfl

theorem run_eighteens_U (k : Nat) (v : Counts) :
    (run (List.replicate k 18) v).U = v.U := by
  induction k generalizing v with
  | zero => rfl
  | succ k ih =>
    simp only [List.replicate_succ, run]
    rw [ih, advance_eighteen_U]

/-- Any finite central eighteen reservoir preserves the exact even fiber count. -/
theorem append_eighteens_count (ss : List Symbol) (k : Nat) :
    inverseCount (ss ++ List.replicate k 18) = inverseCount ss := by
  unfold inverseCount
  rw [run_append, run_eighteens_U]

theorem canonical_eleven_all (ss : List Symbol) :
    canonicalPreimages (11 :: ss) = preimages (11 :: ss) 0 := by
  apply List.filter_eq_self.mpr
  intro xs hx
  exact decide_eq_true (leading_eleven_positive ss xs hx)

/-- Exact cardinality, including the empty-fiber boundary m=0. -/
theorem protected_fiber_cardinality (m k : Nat) :
    (inputWords m k).length = fib m := by
  simp only [inputWords, fullPreimages, List.length_map]
  rw [targetHalf, canonical_eleven_all, preimages_length]
  have h := append_eighteens_count (11 :: List.replicate m 9) k
  simpa only [List.cons_append, leading_eleven_exact] using h

theorem protected_fiber_nodup (m k : Nat) : (inputWords m k).Nodup :=
  fullPreimages_nodup (targetHalf m k)

theorem mirror_of_symmetric_even (q : List Nat) (n : Nat)
    (hlen : q.length = 2 * n) (hsym : q.reverse = q) :
    mirror (q.take n) = q := by
  have hr : (q.take n).reverse = q.drop n := by
    rw [List.reverse_take, hsym, hlen]
    congr 1
    omega
  simp only [mirror, hr, List.take_append_drop]

/-- Intrinsic complete-word fiber: symmetry, real width, canonical coefficient
range, positive exterior, exact zero final carry, and the original transition. -/
def FullActualFiber (m k : Nat) (q : List Nat) : Prop :=
  q.length = 2 * (m + k + 1) ∧ q.reverse = q ∧
  (∀ x ∈ q, x < 19) ∧ 0 < q.headD 0 ∧
  (scan q 0).2 = 0 ∧ Agent8.stepWord q = targetWord m k

/-- Completeness uses symmetry and the even width, rather than assuming that
an arbitrary fiber element already has a chosen half-word representation. -/
theorem protected_fiber_membership (m k : Nat) (q : List Nat) :
    q ∈ inputWords m k ↔ FullActualFiber m k q := by
  rw [inputWords, fullPreimages_membership]
  constructor
  · rintro ⟨xs, ⟨hlen, hb, hc, hs⟩, hp, rfl⟩
    refine ⟨?_, ?_, ?_, ?_, hc, hs⟩
    · rw [mirror_length, hlen, targetHalf_length]
    · simp [mirror]
    · intro x hx
      simp only [mirror, List.mem_append, List.mem_reverse] at hx
      exact hb x (hx.elim id id)
    · cases xs with
      | nil => simp at hp
      | cons x xs => simpa [mirror] using hp
  · rintro ⟨hlen, hsym, hb, hp, hc, hs⟩
    let xs := q.take (m + k + 1)
    have hm : mirror xs = q := mirror_of_symmetric_even q _ hlen hsym
    refine ⟨xs, ⟨?_, ?_, ?_, ?_⟩, ?_, hm⟩
    · simp only [xs, List.length_take, hlen, targetHalf_length]
      omega
    · intro x hx
      exact hb x (List.mem_of_mem_take hx)
    · simpa only [hm] using hc
    · simpa only [hm, targetWord] using hs
    · cases q with
      | nil => simp at hp
      | cons x qs => simp [xs, List.take_succ_cons] at *; assumption

/-- Exact complete fiber result. Its same-width global maximum is a separate
theorem: appending the reservoir adds width but preserves this family's count. -/
theorem protected_fiber_exact (m k : Nat) :
    (inputWords m k).Nodup ∧ (inputWords m k).length = fib m ∧
    ∀ q, q ∈ inputWords m k ↔ FullActualFiber m k q :=
  ⟨protected_fiber_nodup m k, protected_fiber_cardinality m k,
    protected_fiber_membership m k⟩

theorem protected_fiber_nonempty (m k : Nat) (hm : 0 < m) :
    ∃ q, q ∈ inputWords m k := by
  have hf : 0 < fib m := by
    have h := fib_succ_positive (m - 1)
    have he : m - 1 + 1 = m := by omega
    rw [he] at h
    omega
  have hl : (inputWords m k).length ≠ 0 := by
    rw [protected_fiber_cardinality]
    omega
  cases he : inputWords m k with
  | nil => simp [he] at hl
  | cons q qs => exact ⟨q, by simp [he]⟩

#print axioms protected_fiber_exact
#print axioms protected_fiber_nonempty

end P196.Agent9.NoOverflowHorizon
