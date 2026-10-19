import P196.CrossWidthTargetCensus.Tuples

/-!
# Pairing accepted collision prefixes at adjacent parities

Every accepted prefix belongs to the productive state catalogue because
its reflected completion is a closed collision trace. The existing
terminal extension therefore appends exactly one odd terminal to each
even accepted prefix. Truncation gives the inverse correspondence.
-/

set_option autoImplicit false

namespace CrossWidthTargetCensus

open CrossWidthCollisionStates CrossWidthCollisionPaths FoldedCollisionPrefixes

/-- Every retained state of an even accepted prefix is productive. -/
theorem evenAccepted_productive {k : Nat} {p : Prefix k}
    (h : EvenAccepted k p) (i : Fin (k + 1)) : p i ∈ productive := by
  have hc := ((even_valid_iff k p).mp h).toClosed
  have hm := closed_walk_mem_productive (L := 2 * k + 2) (evenTrace k p)
    (by omega) hc.first hc.last hc.edge
    (i := i.val + 1) (by omega) (by have := i.isLt; omega)
  have he : evenTrace k p (i.val + 1) = p i :=
    (evenTrace_prefix k p (i := i.val) (by have := i.isLt; omega)).trans
      (prefixAt_fin p i)
  rw [he] at hm
  exact hm

/-- Every retained state of an odd accepted prefix is productive. -/
theorem oddAccepted_productive {k : Nat} {p : Prefix (k + 1)}
    (h : OddAccepted k p) (i : Fin (k + 2)) : p i ∈ productive := by
  have hc := ((odd_valid_iff k p).mp h).toClosed
  have hm := closed_walk_mem_productive (L := 2 * k + 3) (oddTrace k p)
    (by omega) hc.first hc.last hc.edge
    (i := i.val + 1) (by omega) (by have := i.isLt; omega)
  have he : oddTrace k p (i.val + 1) = p i :=
    (oddTrace_prefix k p (i := i.val) (by have := i.isLt; omega)).trans
      (prefixAt_fin p i)
  rw [he] at hm
  exact hm

/-- Append the explicit terminal extension to a finite prefix. -/
def extendEven {k : Nat} (p : Prefix k) : Prefix (k + 1) :=
  appendPrefix p (terminalExtension (prefixAt p k))

/-- Truncation recovers the original tuple without an acceptance premise. -/
theorem truncatePrefix_extendEven {k : Nat} (p : Prefix k) :
    truncatePrefix (extendEven p) = p :=
  truncatePrefix_append p (terminalExtension (prefixAt p k))

/-- The terminal extension turns every even accepted prefix into an
odd accepted prefix with one additional edge. -/
theorem extendEven_accepted {k : Nat} {p : Prefix k}
    (h : EvenAccepted k p) : OddAccepted k (extendEven p) := by
  have hs : prefixAt p k ∈ productive := by
    have he : prefixAt p k = p (Fin.last k) := prefixAt_fin p (Fin.last k)
    rw [he]
    exact evenAccepted_productive h (Fin.last k)
  have ht := (productive_terminal_extension_iff
    (t := terminalExtension (prefixAt p k)) hs).mpr ⟨h.2, rfl⟩
  constructor
  · exact (walk_append_iff p _).mpr ⟨h.1, ht.1⟩
  · simpa only [extendEven, prefixAt_append_last] using ht.2

private theorem odd_terminal_extension {k : Nat} {p : Prefix (k + 1)}
    (h : OddAccepted k p) :
    EvenTerminal (prefixAt p k) ∧
      prefixAt p (k + 1) = terminalExtension (prefixAt p k) := by
  have hs : prefixAt p k ∈ productive := by
    let i : Fin (k + 2) := ⟨k, by omega⟩
    have he : prefixAt p k = p i := prefixAt_fin p i
    rw [he]
    exact oddAccepted_productive h i
  exact (productive_terminal_extension_iff hs).mp
    ⟨h.1.2 k (by omega), h.2⟩

/-- Removing the final state of an odd accepted prefix leaves an even
accepted prefix. Productive membership justifies the terminal converse. -/
theorem truncatePrefix_accepted {k : Nat} {p : Prefix (k + 1)}
    (h : OddAccepted k p) : EvenAccepted k (truncatePrefix p) := by
  have hw : Walk (k + 1)
      (appendPrefix (truncatePrefix p) (prefixAt p (k + 1))) := by
    rw [appendPrefix_truncate]
    exact h.1
  constructor
  · exact ((walk_append_iff (truncatePrefix p) (prefixAt p (k + 1))).mp hw).1
  · rw [prefixAt_truncate p (Nat.le_refl k)]
    exact (odd_terminal_extension h).1

/-- The final state of an odd accepted prefix is exactly the explicit
extension of its penultimate state, so extension reverses truncation. -/
theorem extendEven_truncate {k : Nat} {p : Prefix (k + 1)}
    (h : OddAccepted k p) : extendEven (truncatePrefix p) = p := by
  unfold extendEven
  rw [prefixAt_truncate p (Nat.le_refl k), ← (odd_terminal_extension h).2]
  exact appendPrefix_truncate p

/-- Appending the terminal extension cannot identify distinct tuples. -/
theorem extendEven_injective {k : Nat} {p q : Prefix k}
    (h : extendEven p = extendEven q) : p = q := by
  have ht := congrArg (fun r : Prefix (k + 1) => truncatePrefix r) h
  simpa only [truncatePrefix_extendEven] using ht

end CrossWidthTargetCensus

#print axioms CrossWidthTargetCensus.evenAccepted_productive
#print axioms CrossWidthTargetCensus.oddAccepted_productive
#print axioms CrossWidthTargetCensus.extendEven
#print axioms CrossWidthTargetCensus.truncatePrefix_extendEven
#print axioms CrossWidthTargetCensus.extendEven_accepted
#print axioms CrossWidthTargetCensus.truncatePrefix_accepted
#print axioms CrossWidthTargetCensus.extendEven_truncate
#print axioms CrossWidthTargetCensus.extendEven_injective
