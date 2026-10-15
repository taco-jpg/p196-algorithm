import HighBaseNormalization

namespace Agent11HighBase
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd

theorem shifted_symmetric (b : Int) (q : List Int) (hs : q.reverse=q) :
    (shifted b q).reverse = shifted b q := by
  simp only [shifted, ← List.map_reverse, hs]

theorem symmetric_dropLast (a : Int) (q : List Int) (hs : (a::q).reverse=a::q) :
    (a::q).dropLast=q.reverse := by
  have ht : (a::q).dropLast.reverse=q := by
    rw [← List.tail_reverse, hs]
    rfl
  simpa only [List.reverse_reverse] using congrArg List.reverse ht

/-- Pairing the true overflow digit list gives both positive endpoints. -/
theorem framed_pairs (a : Int) (q : List Int) :
    pairs ((a-1)::q ++ [1]) =
      a :: List.zipWith (· + ·) q q.reverse ++ [a] := by
  unfold pairs
  simp only [List.cons_append]
  rw [List.reverse_cons, List.reverse_append]
  simp only [List.reverse_cons, List.reverse_nil, List.nil_append, List.singleton_append, List.append_assoc,
    List.cons_append, List.zipWith_cons_cons]
  rw [List.zipWith_append (by simp : q.length=q.reverse.length)]
  simp only [List.zipWith_cons_cons, List.zipWith_nil_left, List.append_nil,
    List.cons.injEq]
  constructor
  · omega
  · congr 1
    congr 1
    omega

theorem adjacent_shifted (b : Int) (q : List Int) :
    adjacent (shifted b q) = (adjacent q).map (fun s => s-2*b+2) := by
  simp only [adjacent, shifted, ← List.map_dropLast, ← List.map_tail,
    List.zipWith_map, List.map_zipWith]
  congr 1
  funext a c
  omega

/-- Source equation (8), uniformly for all finite widths including one. -/
theorem next_pairs_formula (b a : Int) (q : List Int) (hb : 2 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2)
    (hs : (a::q).reverse=a::q) :
    nextPairs b (a::q) =
      (a-b+1) :: ((adjacent (a::q)).map (fun s => s-2*b+2)) ++ [a-b+1] := by
  have hshift := shifted_symmetric b (a::q) hs
  change ((a-b+1)::shifted b q).reverse=(a-b+1)::shifted b q at hshift
  have hdrop := symmetric_dropLast (a-b+1) (shifted b q) hshift
  have hadj : adjacent (shifted b (a::q)) =
      List.zipWith (· + ·) (shifted b q) (shifted b q).reverse := by
    change List.zipWith (· + ·) ((a-b+1)::shifted b q).dropLast (shifted b q) = _
    rw [hdrop, List.zipWith_comm]
    simp only [Int.add_comm]
  unfold nextPairs
  rw [high_first_digits b a q hb ha hq]
  have he : a-b=(a-b+1)-1 := by omega
  have hp := framed_pairs (a-b+1) (shifted b q)
  simp only [show (a-b+1)-1=a-b by omega] at hp
  rw [hp, ← hadj, adjacent_shifted]

/-- List formulation of adjacency is exactly the recursively listed consecutive sums. -/
theorem adjacent_cons_cons (a c : Int) (q : List Int) :
    adjacent (a::c::q) = (a+c) :: adjacent (c::q) := by
  cases q with
  | nil => rfl
  | cons d q => rfl

/-- Universal indexed version of the source adjacency condition. -/
theorem adjacent_bound_iff (q : List Int) (limit : Int) :
    (∀ s ∈ adjacent q, s ≤ limit) ↔
    (∀ i : Nat, ∀ h : i+1<q.length, q[i] + q[i+1] ≤ limit) := by
  induction q with
  | nil => simp [adjacent]
  | cons a q ih =>
      cases q with
      | nil => simp [adjacent]
      | cons c q =>
        rw [adjacent_cons_cons]
        constructor
        · intro hs i hi
          cases i with
          | zero => exact hs (a+c) (by simp)
          | succ i =>
              have ht : ∀ s ∈ adjacent (c::q), s ≤ limit := by
                intro s hm; exact hs s (by simp [hm])
              exact (ih.mp ht) i (by simpa using hi)
        · intro hs s hm
          rcases List.mem_cons.mp hm with rfl | hm
          · exact hs 0 (by simp)
          · apply (ih.mpr ?_) s hm
            intro i hi
            exact hs (i+1) (by simpa using hi)

end Agent11HighBase
