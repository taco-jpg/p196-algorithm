import PrefixInverse

namespace SevenColumn

/-- Solve the no-overflow equation for the source sum after guessing the
next low carry. Final guards reject every spurious truncated-division result. -/
def noCandidate (v x y b z : Nat) : Nat :=
  (v + 10 * (b + y) - x - z) / 2

/-- Solve the shifted overflow equation after guessing the next low carry. -/
def overflowCandidate (v prev x y b z : Nat) : Nat :=
  (v + 10 * y - prev - z) + 10 * b - x

/-- Four choices per column, rather than 38 source/carry choices. -/
def fastNoOverflowPred : List Nat → Nat → Nat → List (List Nat)
  | [], _, _ => [[]]
  | v :: p, x, y => (List.range 2).flatMap fun b =>
      (List.range 2).flatMap fun z =>
        let a := noCandidate v x y b z
        if a < 19 ∧ carry a x = b ∧ carry a z = y ∧
            v = lowDigit a x + lowDigit a z then
          (fastNoOverflowPred p b z).map (a :: ·)
        else []

def fastOverflowTailPred : List Nat → Nat → Nat → Nat → List (List Nat)
  | [], a, _, y => if (List.range 2).any (fun z => carry a z == y) then [[]] else []
  | v :: p, prev, x, y => (List.range 2).flatMap fun b =>
      (List.range 2).flatMap fun z =>
        let a := overflowCandidate v prev x y b z
        if a < 19 ∧ carry a x = b ∧ carry prev z = y ∧
            v = lowDigit a x + lowDigit prev z then
          (fastOverflowTailPred p a b z).map (a :: ·)
        else []

def fastOverflowPred : List Nat → List (List Nat)
  | [] => []
  | v :: p => if 0 < v ∧ v ≤ 10 then
      let a := overflowFirst v
      (fastOverflowTailPred p a (carry a 0) 1).map (a :: ·)
    else []

def fastPrefixPredecessors (p : List Nat) : List (List Nat) :=
  (fastNoOverflowPred p 0 0).filter (fun s => 0 < s.headD 0) ++ fastOverflowPred p

theorem carry_lt_two {a x : Nat} (ha : a < 19) (hx : x < 2) :
    carry a x < 2 := by
  unfold carry
  omega

theorem noCandidate_eq {v a x y z : Nat}
    (hy : carry a z = y) (hv : v = lowDigit a x + lowDigit a z) :
    noCandidate v x y (carry a x) z = a := by
  unfold noCandidate carry lowDigit at *
  omega

theorem overflowCandidate_eq {v a prev x y z : Nat}
    (hy : carry prev z = y) (hv : v = lowDigit a x + lowDigit prev z) :
    overflowCandidate v prev x y (carry a x) z = a := by
  unfold overflowCandidate carry lowDigit at *
  omega

theorem NoOverflow.mem_fastNoOverflowPred {p s : List Nat} {x y : Nat}
    (h : NoOverflow p s x y) (hx : x < 2) : s ∈ fastNoOverflowPred p x y := by
  induction h with
  | nil => simp [fastNoOverflowPred]
  | @cons p s v a x y z ha hz hy hv tail ih =>
      have hb := carry_lt_two ha hx
      have he := noCandidate_eq hy hv
      simp only [fastNoOverflowPred, List.mem_flatMap, List.mem_range]
      exact ⟨carry a x, hb, z, hz, by rw [he]; simp [ha, hy, hv, ih hb]⟩

theorem OverflowTail.mem_fastOverflowTailPred {p s : List Nat} {a x y : Nat}
    (h : OverflowTail p s a x y) (hx : x < 2) :
    s ∈ fastOverflowTailPred p a x y := by
  induction h with
  | @nil a x y terminal =>
      rcases terminal with ⟨z, hz, hy⟩
      have hh : (List.range 2).any (fun z => carry a z == y) = true := by
        simp only [List.any_eq_true, List.mem_range, beq_iff_eq]
        exact ⟨z, hz, hy⟩
      simp [fastOverflowTailPred, hh]
  | @cons p s v a prev x y z ha hz hy hv tail ih =>
      have hb := carry_lt_two ha hx
      have he := overflowCandidate_eq hy hv
      simp only [fastOverflowTailPred, List.mem_flatMap, List.mem_range]
      exact ⟨carry a x, hb, z, hz, by rw [he]; simp [ha, hy, hv, ih hb]⟩

theorem longCompatible_mem_fastPrefixPredecessors {p s : List Nat}
    (h : LongCompatible p s) : s ∈ fastPrefixPredecessors p := by
  cases h with
  | @noOverflow p s a positive equations =>
      apply List.mem_append_left
      simp only [List.mem_filter, List.headD_cons, decide_eq_true_eq]
      exact ⟨equations.mem_fastNoOverflowPred (by decide), positive⟩
  | @overflow p s v a positive ha outer equations =>
      rcases equations.outer_carry with ⟨z, hz, hy⟩
      rcases overflowFirst_eq ha hz hy outer with ⟨hv, heq⟩
      have hx := carry_lt_two ha (show 0 < 2 by decide)
      have hvpos : 0 < v := by omega
      apply List.mem_append_right
      simp [fastOverflowPred, hvpos, hv, heq, equations.mem_fastOverflowTailPred hx]

theorem fastNoOverflowPred_mem {p s : List Nat} {x y : Nat}
    (h : s ∈ fastNoOverflowPred p x y) : NoOverflow p s x y := by
  induction p generalizing s x y with
  | nil =>
      simp only [fastNoOverflowPred, List.mem_singleton] at h
      subst s
      exact .nil x y
  | cons v p ih =>
      simp only [fastNoOverflowPred, List.mem_flatMap, List.mem_range] at h
      obtain ⟨b, hb, z, hz, h⟩ := h
      split at h
      next hc =>
        obtain ⟨ss, hss, hs⟩ := List.mem_map.mp h
        subst s
        apply NoOverflow.cons hc.1 hz hc.2.2.1 hc.2.2.2
        rw [hc.2.1]
        exact ih hss
      next => simp at h

theorem fastOverflowTailPred_mem {p s : List Nat} {a x y : Nat}
    (h : s ∈ fastOverflowTailPred p a x y) : OverflowTail p s a x y := by
  induction p generalizing s a x y with
  | nil =>
      simp only [fastOverflowTailPred] at h
      split at h
      next hc =>
        simp only [List.mem_singleton] at h
        subst s
        apply OverflowTail.nil
        simpa only [List.any_eq_true, List.mem_range, beq_iff_eq] using hc
      next => simp at h
  | cons v p ih =>
      simp only [fastOverflowTailPred, List.mem_flatMap, List.mem_range] at h
      obtain ⟨b, hb, z, hz, h⟩ := h
      split at h
      next hc =>
        obtain ⟨ss, hss, hs⟩ := List.mem_map.mp h
        subst s
        apply OverflowTail.cons hc.1 hz hc.2.2.1 hc.2.2.2
        rw [hc.2.1]
        exact ih hss
      next => simp at h

theorem mem_fastPrefixPredecessors_iff {p s : List Nat} :
    s ∈ fastPrefixPredecessors p ↔ LongCompatible p s := by
  constructor
  · intro h
    rcases List.mem_append.mp h with h | h
    · obtain ⟨heq, hpos⟩ := List.mem_filter.mp h
      cases s with
      | nil => simp at hpos
      | cons a ss =>
          have hapos : 0 < a := by simpa using hpos
          exact .noOverflow hapos (fastNoOverflowPred_mem heq)
    · cases p with
      | nil => simp [fastOverflowPred] at h
      | cons v p =>
          simp only [fastOverflowPred] at h
          split at h
          next hc =>
            obtain ⟨ss, hss, hs⟩ := List.mem_map.mp h
            subst s
            obtain ⟨ha, halt, hv⟩ := overflowFirst_properties hc.1 hc.2
            exact .overflow ha halt hv (fastOverflowTailPred_mem hss)
          next => simp at h
  · exact longCompatible_mem_fastPrefixPredecessors

/-- Extensional equality of the simple and four-choice inverse algorithms. -/
theorem fastPrefixPredecessors_mem_iff {p s : List Nat} :
    s ∈ fastPrefixPredecessors p ↔ s ∈ prefixPredecessors p := by
  rw [mem_fastPrefixPredecessors_iff, mem_prefixPredecessors_iff]

#print axioms mem_fastPrefixPredecessors_iff
#print axioms fastPrefixPredecessors_mem_iff

end SevenColumn
