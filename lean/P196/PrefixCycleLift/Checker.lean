import P196.Agent104P620Witness.ActualPrefix

/-!
# One-column extensions of finite prefix traces

The retained rows run in forward time. An extension assigns one additional
pair coefficient to each row, and each edge uses one of the two possible
boundary carries in the unchanged `SevenColumnProjection.forwardPrefix`.
An empty checked reachable set excludes every such extension. Actual
admissible words supply these coefficients and carries, including overflow.
-/

namespace PrefixCycleLift

open SevenColumnProjection DecimalDigits FoldedDecimal

abbrev Word := List Nat

/-- Possible additional coefficients after one forward edge. -/
def advance (p q : Word) (xs : List Nat) : List Nat :=
  (List.range 19).filter (fun y =>
    xs.any (fun x =>
      (List.range 2).any (fun e =>
        decide (forwardPrefix (p ++ [x]) e = q ++ [y]))))

/-- Exact semantics of the small executable one-column transition. -/
theorem mem_advance_iff (p q : Word) (xs : List Nat) (y : Nat) :
    y ∈ advance p q xs ↔
      y < 19 ∧ ∃ x, x ∈ xs ∧ ForwardAdmitted (p ++ [x]) (q ++ [y]) := by
  simp only [advance, List.mem_filter, List.mem_range, List.any_eq_true,
    decide_eq_true_eq, ForwardAdmitted]
  constructor
  · rintro ⟨hy, x, hx, e, he, hedge⟩
    exact ⟨hy, x, hx, e, by omega, hedge⟩
  · rintro ⟨hy, x, hx, e, he, hedge⟩
    exact ⟨hy, x, hx, e, by omega, hedge⟩

/-- Propagate a candidate set through a forward trace of retained rows. -/
def run : List Word → List Nat → List Nat
  | p :: q :: rest, xs => run (q :: rest) (advance p q xs)
  | _, xs => xs

/-- A consistent one-column extension of a finite forward trace. -/
inductive Lift : List Word → Nat → Nat → Prop
  | nil (x : Nat) : Lift [] x x
  | single (p : Word) (x : Nat) : Lift [p] x x
  | step {p q : Word} {rest : List Word} {x y z : Nat}
      (edge : ForwardAdmitted (p ++ [x]) (q ++ [y]))
      (bound : y < 19)
      (tail : Lift (q :: rest) y z) : Lift (p :: q :: rest) x z

/-- Every consistent extension survives the executable reachable-set scan. -/
theorem lift_survives {rows : List Word} {x z : Nat}
    (h : Lift rows x z) (xs : List Nat) (hx : x ∈ xs) :
    z ∈ run rows xs := by
  induction h generalizing xs with
  | nil x => exact hx
  | single p x => exact hx
  | @step p q rest x y z hedge hy htail ih =>
      change z ∈ run (q :: rest) (advance p q xs)
      exact ih (advance p q xs)
        ((mem_advance_iff p q xs y).mpr ⟨hy, x, hx, hedge⟩)

/-- A kernel-checked empty final set rules out every bounded initial lift. -/
theorem checked_no_lift {rows : List Word}
    (checked : run rows (List.range 19) = []) {x z : Nat}
    (hx : x < 19) : ¬ Lift rows x z := by
  intro h
  have hz := lift_survives h (List.range 19) (List.mem_range.mpr hx)
  rw [checked] at hz
  exact List.not_mem_nil hz

/-- One more retained pair coefficient is literally a list append. -/
theorem wordPrefix_succ (q : Nat → Nat) (k : Nat) :
    wordPrefix q (k + 1) = wordPrefix q k ++ [q k] := by
  simp only [wordPrefix_eq_range_map, List.range_succ, List.map_append,
    List.map_cons, List.map_nil]

/-- The actual whole-word map supplies a one-column lift. The exact high
inner carry is used by `actual_forward_admitted`; no fixed width or
disjointness of reflected windows is assumed. -/
theorem actual_lift_edge (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : k + 1 ≤ L) :
    ForwardAdmitted (wordPrefix q k ++ [q k])
      (wordPrefix (nextColumns q L) k ++ [nextColumns q L k]) := by
  have h := actual_forward_admitted q L (k + 1) ha hk
  rw [wordPrefix_succ, wordPrefix_succ] at h
  exact h

end PrefixCycleLift
