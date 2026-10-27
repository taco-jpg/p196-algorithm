import P196.PrefixCycleLift.Checker

/-!
An exact finite refinement of closed decimal prefix traces, adding one
coefficient at a time. The unchanged `PrefixCycleLift.advance` supplies
the local arithmetic and its existing completeness theorem. No product
of independent phase marginals replaces a correlated temporal trace.
-/

namespace P196.ManagerShortTwoRun

open SevenColumnProjection PrefixCycleLift

abbrev Rows := List (List Nat)

def rowsAt (s : Nat → List Nat) (t : Nat) : Nat → Rows
  | 0 => [s t]
  | n + 1 => s t :: rowsAt s (t + 1) n

@[simp] theorem rowsAt_head (s : Nat → List Nat) (t n : Nat) :
    (rowsAt s t n).headD [] = s t := by cases n <;> rfl

@[simp] theorem rowsAt_last (s : Nat → List Nat) (t n : Nat) (fallback : List Nat) :
    (rowsAt s t n).getLastD fallback = s (t + n) := by
  induction n generalizing t fallback with
  | zero => simp [rowsAt]
  | succ n ih =>
    rw [rowsAt, List.getLastD_cons]
    simpa only [Nat.add_assoc, Nat.add_comm 1 n] using ih (t + 1) (s t)

def headGamma (a b : Nat) : Nat :=
  if 10 ≤ a ∨ (a = 9 ∧ b = 10) then 1 else 0

def traceGain : Rows → Nat
  | p :: q :: rest => headGamma (p.headD 0) (q.headD 0) + traceGain (q :: rest)
  | _ => 0

def extendFrom : Rows → Nat → List Rows
  | [], _ => [[]]
  | [p], x => [[p ++ [x]]]
  | p :: q :: rest, x =>
      (PrefixCycleLift.advance p q [x]).flatMap fun y =>
        (extendFrom (q :: rest) y).map fun tail => (p ++ [x]) :: tail

def extendCycles (rows : Rows) : List Rows :=
  (List.range 19).flatMap fun x =>
    (extendFrom rows x).filter fun out =>
      decide (out.headD [] = out.getLastD []) && decide (0 < (out.headD []).headD 0)

def candidates (P G : Nat) : Nat → List Rows
  | 0 => [List.replicate (P + 1) []]
  | k + 1 => ((candidates P G k).flatMap extendCycles).filter fun rows =>
      decide (traceGain rows = G)

/-- All correlated next coefficients of an admitted trace occur in the
enumerator. No terminal equality is used until the cycle filter. -/
theorem extendFrom_complete (s : Nat → List Nat) (c : Nat → Nat) (t n : Nat)
    (hb : ∀ i, i ≤ n → c (t + i) < 19)
    (he : ∀ i, i < n → ForwardAdmitted
      (s (t + i) ++ [c (t + i)]) (s (t + i + 1) ++ [c (t + i + 1)])) :
    rowsAt (fun j => s j ++ [c j]) t n ∈ extendFrom (rowsAt s t n) (c t) := by
  induction n generalizing t with
  | zero => simp [rowsAt, extendFrom]
  | succ n ih =>
    have hy : c (t + 1) ∈ PrefixCycleLift.advance (s t) (s (t + 1)) [c t] := by
      apply (mem_advance_iff _ _ _ _).mpr
      refine ⟨hb 1 (by omega), c t, by simp, ?_⟩
      simpa only [Nat.add_zero] using he 0 (by omega)
    have ht := ih (t + 1)
      (by intro i hi; simpa only [Nat.add_assoc, Nat.add_comm i 1] using hb (i + 1) (by omega))
      (by intro i hi; simpa only [Nat.add_assoc, Nat.add_comm i 1] using he (i + 1) (by omega))
    cases n with
    | zero =>
      simp only [rowsAt, extendFrom, List.mem_flatMap, List.mem_map]
      exact ⟨c (t + 1), hy, [s (t + 1) ++ [c (t + 1)]], by simp [extendFrom], rfl⟩
    | succ n =>
      simp only [rowsAt, extendFrom, List.mem_flatMap, List.mem_map]
      refine ⟨c (t + 1), hy, rowsAt (fun j => s j ++ [c j]) (t + 1) (n + 1), ?_, rfl⟩
      exact ht

theorem extendCycles_complete (s : Nat → List Nat) (c : Nat → Nat) (P : Nat)
    (hb : ∀ i, i ≤ P → c i < 19)
    (he : ∀ i, i < P → ForwardAdmitted (s i ++ [c i]) (s (i + 1) ++ [c (i + 1)]))
    (hc : s P ++ [c P] = s 0 ++ [c 0])
    (hp : 0 < (s 0 ++ [c 0]).headD 0) :
    rowsAt (fun j => s j ++ [c j]) 0 P ∈ extendCycles (rowsAt s 0 P) := by
  unfold extendCycles
  apply List.mem_flatMap.mpr
  refine ⟨c 0, List.mem_range.mpr (hb 0 (by omega)), ?_⟩
  apply List.mem_filter.mpr
  refine ⟨extendFrom_complete s c 0 P (by simpa using hb) (by simpa using he), ?_⟩
  simp only [Bool.and_eq_true, decide_eq_true_eq, rowsAt_head, rowsAt_last,
    Nat.zero_add]
  exact ⟨hc.symm, hp⟩

theorem traceGain_rowsAt_congr (s r : Nat → List Nat) (t n : Nat)
    (h : ∀ j, (s j).headD 0 = (r j).headD 0) :
    traceGain (rowsAt s t n) = traceGain (rowsAt r t n) := by
  induction n generalizing t with
  | zero => rfl
  | succ n ih =>
    cases n with
    | zero => simp only [rowsAt, traceGain, h, Nat.add_zero]
    | succ n =>
      simpa only [rowsAt, traceGain, h] using congrArg
        (fun z => headGamma ((r t).headD 0) ((r (t + 1)).headD 0) + z) (ih (t + 1))

theorem prefix_eq_of_pointwise (q r : Nat → Nat) (k : Nat)
    (h : ∀ i, i < k → q i = r i) : wordPrefix q k = wordPrefix r k := by
  rw [wordPrefix_eq_range_map, wordPrefix_eq_range_map]
  apply List.map_congr_left
  intro i hi
  exact h i (List.mem_range.mp hi)

/-- Complete finite coverage of every bounded, positive, closed prefix path
with the indicated head-derived overflow sum. -/
theorem candidates_complete (q : Nat → Nat → Nat) (P G k : Nat)
    (hb : ∀ t, t ≤ P → ∀ i, i < k → q t i < 19)
    (hp : 0 < q 0 0)
    (he : ∀ j, j ≤ k → ∀ t, t < P →
      ForwardAdmitted (wordPrefix (q t) j) (wordPrefix (q (t + 1)) j))
    (hc : ∀ i, i < k → q P i = q 0 i)
    (hg : traceGain (rowsAt (fun t => [q t 0]) 0 P) = G) :
    rowsAt (fun t => wordPrefix (q t) k) 0 P ∈ candidates P G k := by
  induction k with
  | zero =>
    have hzero (t n : Nat) : rowsAt (fun j => wordPrefix (q j) 0) t n =
        List.replicate (n + 1) [] := by
      induction n generalizing t with
      | zero => rfl
      | succ n ih =>
        change [] :: rowsAt (fun j => wordPrefix (q j) 0) (t + 1) n =
          [] :: List.replicate (n + 1) []
        rw [ih]
    simp [candidates, hzero]
  | succ k ih =>
    have old := ih (by intro t ht i hi; exact hb t ht i (by omega))
      (by intro j hj; exact he j (by omega)) (by intro i hi; exact hc i (by omega))
    have hrow : (fun t => wordPrefix (q t) (k + 1)) =
        (fun t => wordPrefix (q t) k ++ [q t k]) := by
      funext t
      exact wordPrefix_succ (q t) k
    have ext := extendCycles_complete (fun t => wordPrefix (q t) k) (fun t => q t k) P
      (by intro t ht; exact hb t ht k (by omega))
      (by intro t ht; simpa only [← wordPrefix_succ] using he (k + 1) (by omega) t ht)
      (by rw [← wordPrefix_succ, ← wordPrefix_succ]; exact prefix_eq_of_pointwise _ _ _ hc)
      (by rw [← wordPrefix_succ]; simpa only [wordPrefix, segment, List.headD_cons] using hp)
    rw [← hrow] at ext
    apply List.mem_filter.mpr
    constructor
    · exact List.mem_flatMap.mpr ⟨rowsAt (fun t => wordPrefix (q t) k) 0 P, old, ext⟩
    · apply decide_eq_true
      rw [traceGain_rowsAt_congr (fun t => wordPrefix (q t) (k + 1))
        (fun t => [q t 0]) 0 P]
      · exact hg
      · intro t
        rfl

#print axioms extendFrom_complete
#print axioms extendCycles_complete
#print axioms candidates_complete

end P196.ManagerShortTwoRun
