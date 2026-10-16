import SparseNumbers

/-!
Agent #122. The original total countermap, exact predecessor preservation,
and its finite first-hit chains. The map below is not the actual RAA map
outside B. Classical choice selects a unique sparse label; it is not an oracle
for an unproved arithmetic claim.
-/
namespace Agent122.Countermodel

open Lychrel196 DecimalDigits DecimalQuantitativeMass

/-- Membership in a finite (but arbitrarily long) labeled chain. -/
def IsNode (ell : Nat → Nat) (n : Nat) : Prop :=
  ∃ p : Nat × Nat, 3 ≤ p.1 ∧ p.2 ≤ ell p.1 ∧ n = node p.1 p.2

/-- The historical countermap. Zero is included only to make a total Nat map;
the all-seed termination and growth statements below concern positive inputs. -/
noncomputable def F (ell : Nat → Nat) (n : Nat) : Nat := by
  classical
  exact if B n then step n else
    if h : IsNode ell n then
      let p := Classical.choose h
      if p.2 < ell p.1 then node p.1 (p.2+1) else terminal p.1 (ell p.1)
    else if decimalLength n = 1 then 19
    else if decimalLength n = 2 then 109
    else node (decimalLength n) 0

noncomputable def run (ell : Nat → Nat) (n : Nat) : Nat → Nat
  | 0 => n
  | t+1 => F ell (run ell n t)

/-- Here first-hit safety includes the initial index zero. -/
def FirstHit (ell : Nat → Nat) (n tau : Nat) : Prop :=
  Palindrome (run ell n tau) ∧ ∀ t, t < tau → ¬ Palindrome (run ell n t)

/-- A positive-time palindrome hit; an initially palindromic seed still must
have a later hit to satisfy this predicate. -/
def Terminates (ell : Nat → Nat) (n : Nat) : Prop :=
  ∃ t, 0 < t ∧ Palindrome (run ell n t)

theorem node_isNode (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    IsNode ell (node a j) := ⟨(a,j), ha, hj, rfl⟩

theorem F_of_B (ell : Nat → Nat) (n : Nat) (h : B n) : F ell n = step n := by
  classical
  simp [F, h]

theorem F_node (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    F ell (node a j) =
      if j < ell a then node a (j+1) else terminal a (ell a) := by
  classical
  have hnode := node_isNode ell a j ha hj
  have hx := Classical.choose_spec hnode
  have hinj := node_injective a j (Classical.choose hnode).1 (Classical.choose hnode).2
    ha hx.1 hx.2.2
  have heq : Classical.choose hnode = (a,j) := Prod.ext hinj.1.symm hinj.2.symm
  simp only [F, if_neg (node_safe a j ha).2, dif_pos hnode, heq]

theorem F_terminal (ell : Nat → Nat) (a : Nat) (ha : 3 ≤ a) :
    F ell (terminal a (ell a)) = step (terminal a (ell a)) := by
  exact F_of_B ell _ (terminal_properties a (ell a) ha).2.2

theorem F_generic (ell : Nat → Nat) (n : Nat) (hb : ¬ B n) (hn : ¬ IsNode ell n) :
    F ell n = if decimalLength n = 1 then 19
      else if decimalLength n = 2 then 109 else node (decimalLength n) 0 := by
  classical
  simp [F, hb, hn]

theorem decimalLength_positive (n : Nat) (hn : 0 < n) : 0 < decimalLength n := by
  obtain ⟨d,L,hc⟩ := canonical_exists n hn
  rw [decimalLength_of_canonical n d L hc]
  exact hc.1

theorem not_node_of_short_width (ell : Nat → Nat) (n : Nat) (hn : decimalLength n < 4) :
    ¬ IsNode ell n := by
  rintro ⟨⟨a,j⟩, ha, hj, heq⟩
  rw [heq, node_width a j ha] at hn
  omega

theorem nineteen_safe : ¬ Palindrome 19 ∧ ¬ B 19 := by decide

theorem one_hundred_nine_safe : ¬ Palindrome 109 ∧ ¬ B 109 := by decide

theorem F_nineteen (ell : Nat → Nat) : F ell 19 = 109 := by
  have h : decimalLength 19 = 2 := by simp [decimalLength]
  rw [F_generic ell 19 nineteen_safe.2
    (not_node_of_short_width ell 19 (by omega))]
  simp [h]

theorem F_one_hundred_nine (ell : Nat → Nat) : F ell 109 = node 3 0 := by
  have h : decimalLength 109 = 3 := by simp [decimalLength]
  rw [F_generic ell 109 one_hundred_nine_safe.2
    (not_node_of_short_width ell 109 (by omega))]
  simp [h]

/-- Exact predecessor preservation for every Nat, with the actual decimal
palindrome predicate and actual reverse-and-add predecessor set. -/
theorem F_exact_predecessors (ell : Nat → Nat) (n : Nat) :
    Palindrome (F ell n) ↔ B n := by
  classical
  by_cases hb : B n
  · rw [F_of_B ell n hb]
    exact Iff.rfl
  · have hp : 0 < n := by
      by_cases hz : n = 0
      · subst n
        exact False.elim (hb (by decide))
      · omega
    have hnP : ¬ Palindrome (F ell n) := by
      by_cases hn : IsNode ell n
      · obtain ⟨⟨a,j⟩,ha,hj,heq⟩ := hn
        rw [heq, F_node ell a j ha hj]
        split
        · exact (node_safe a (j+1) ha).1
        · exact (terminal_properties a (ell a) ha).2.1
      · rw [F_generic ell n hb hn]
        split
        · exact nineteen_safe.1
        · split
          · exact one_hundred_nine_safe.1
          · have hpos := decimalLength_positive n hp
            exact (node_safe (decimalLength n) 0 (by omega)).1
    exact ⟨fun h => False.elim (hnP h), fun h => False.elim (hb h)⟩

theorem F_positive (ell : Nat → Nat) (n : Nat) (hn : 0 < n) : 0 < F ell n := by
  classical
  by_cases hb : B n
  · rw [F_of_B ell n hb]
    unfold step
    omega
  · by_cases hc : IsNode ell n
    · obtain ⟨⟨a,j⟩,ha,hj,heq⟩ := hc
      rw [heq, F_node ell a j ha hj]
      split
      · exact node_positive _ _
      · exact (terminal_properties a (ell a) ha).1
    · rw [F_generic ell n hb hc]
      split
      · decide
      · split
        · decide
        · exact node_positive _ _

theorem run_succ_left (ell : Nat → Nat) (n t : Nat) :
    run ell n (t+1) = run ell (F ell n) t := by
  induction t with
  | zero => rfl
  | succ t ih =>
    change F ell (run ell n (t+1)) = F ell (run ell (F ell n) t)
    exact congrArg (F ell) ih

theorem run_add (ell : Nat → Nat) (n s t : Nat) :
    run ell n (s+t) = run ell (run ell n s) t := by
  induction t with
  | zero => simp [run]
  | succ t ih =>
    change F ell (run ell n (s+t)) = F ell (run ell (run ell n s) t)
    exact congrArg (F ell) ih

theorem run_positive (ell : Nat → Nat) (n t : Nat) (hn : 0 < n) :
    0 < run ell n t := by
  induction t with
  | zero => exact hn
  | succ t ih => exact F_positive ell _ ih

theorem run_node (ell : Nat → Nat) (a j t : Nat) (ha : 3 ≤ a)
    (ht : j+t ≤ ell a) : run ell (node a j) t = node a (j+t) := by
  induction t with
  | zero => simp [run]
  | succ t ih =>
    rw [run, ih (by omega), F_node ell a (j+t) ha (by omega)]
    rw [if_pos (by omega : j+t < ell a)]
    congr 1

theorem run_terminal_at (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    run ell (node a j) (ell a-j+1) = terminal a (ell a) := by
  rw [run, run_node ell a j (ell a-j) ha (by omega)]
  have heq : j+(ell a-j) = ell a := by omega
  rw [heq, F_node ell a (ell a) ha (by omega), if_neg (by omega)]

theorem run_palindrome_at (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    run ell (node a j) (ell a-j+2) = step (terminal a (ell a)) := by
  rw [show ell a-j+2 = (ell a-j+1)+1 by omega, run,
    run_terminal_at ell a j ha hj, F_terminal ell a ha]

/-- Exact, not just bounded, first hit from every finite chain position. -/
theorem node_first_hit (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    FirstHit ell (node a j) (ell a-j+2) := by
  constructor
  · rw [run_palindrome_at ell a j ha hj]
    exact (terminal_properties a (ell a) ha).2.2
  · intro t ht
    by_cases he : t ≤ ell a-j
    · rw [run_node ell a j t ha (by omega)]
      exact (node_safe a (j+t) ha).1
    · have heq : t = ell a-j+1 := by omega
      rw [heq, run_terminal_at ell a j ha hj]
      exact (terminal_properties a (ell a) ha).2.1

theorem node_terminates (ell : Nat → Nat) (a j : Nat) (ha : 3 ≤ a) (hj : j ≤ ell a) :
    Terminates ell (node a j) := by
  exact ⟨ell a-j+2, by omega, (node_first_hit ell a j ha hj).1⟩

theorem terminates_of_next (ell : Nat → Nat) (n : Nat) (h : Terminates ell (F ell n)) :
    Terminates ell n := by
  obtain ⟨t,ht,hp⟩ := h
  refine ⟨t+1, by omega, ?_⟩
  rwa [run_succ_left]

theorem small_terminates (ell : Nat → Nat) : Terminates ell 19 ∧ Terminates ell 109 := by
  have h109 : Terminates ell 109 := by
    apply terminates_of_next
    rw [F_one_hundred_nine]
    exact node_terminates ell 3 0 (by decide) (by omega)
  constructor
  · apply terminates_of_next
    rwa [F_nineteen]
  · exact h109

/-- All positive finite seeds terminate under the countermap, even though
no uniform finite first-hit bound is asserted. -/
theorem every_positive_seed_terminates (ell : Nat → Nat) (n : Nat) (hn : 0 < n) :
    Terminates ell n := by
  classical
  by_cases hb : B n
  · refine ⟨1, by decide, ?_⟩
    change Palindrome (F ell n)
    rw [F_of_B ell n hb]
    exact hb
  · by_cases hc : IsNode ell n
    · obtain ⟨⟨a,j⟩,ha,hj,heq⟩ := hc
      rw [heq]
      exact node_terminates ell a j ha hj
    · apply terminates_of_next
      rw [F_generic ell n hb hc]
      split
      · exact (small_terminates ell).1
      · split
        · exact (small_terminates ell).2
        · have hp := decimalLength_positive n hn
          exact node_terminates ell (decimalLength n) 0 (by omega) (by omega)

/-- One fixed completely terminating map has arbitrarily large exact finite
first-hit times. The map, not the horizon, is fixed before the quantifier R. -/
theorem fixed_map_unbounded_first_hits (R : Nat) :
    ∃ n tau, 0 < n ∧ R < tau ∧ FirstHit (fun a => a) n tau := by
  refine ⟨node (R+3) 0, R+5, node_positive _ _, by omega, ?_⟩
  have h := node_first_hit (fun a => a) (R+3) 0 (by omega) (by omega)
  simpa using h

/-- This is an actual decimal countermodel to that collection of supporting
properties, not a Lychrel seed for the true reverse-and-add update. -/
theorem terminating_countermodel_exists :
    ∃ ell : Nat → Nat,
      (∀ n, B n → F ell n = step n) ∧
      (∀ n, Palindrome (F ell n) ↔ B n) ∧
      (∀ n, 0 < n → Terminates ell n) ∧
      (∀ R, ∃ n tau, 0 < n ∧ R < tau ∧ FirstHit ell n tau) := by
  refine ⟨fun a => a, ?_, ?_, ?_, ?_⟩
  · exact F_of_B _
  · exact F_exact_predecessors _
  · exact every_positive_seed_terminates _
  · exact fixed_map_unbounded_first_hits

end Agent122.Countermodel
