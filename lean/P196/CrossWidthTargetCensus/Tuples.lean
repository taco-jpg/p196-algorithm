import P196.FoldedCollisionPrefixes.Targets

/-!
# Extending and truncating finite collision walks

The finite tuple representation has an injective one-state extension.
Truncation recovers the preceding tuple, and the walk condition separates
into its old edges and the newly appended final edge.
-/

set_option autoImplicit false

namespace CrossWidthTargetCensus

open CrossWidthCollisionStates FoldedCollisionPrefixes

/-- Add one state after the last entry of a finite prefix. -/
def appendPrefix {k : Nat} (p : Prefix k) (s : State) : Prefix (k + 1) :=
  fun i => if h : i.val < k + 1 then p ⟨i.val, h⟩ else s

/-- Remove the last entry of a nonempty extension. -/
def truncatePrefix {k : Nat} (p : Prefix (k + 1)) : Prefix k :=
  fun i => p i.castSucc

/-- Extension preserves every old tuple entry. -/
theorem appendPrefix_castSucc {k : Nat} (p : Prefix k) (s : State)
    (i : Fin (k + 1)) : appendPrefix p s i.castSucc = p i := by
  change (if h : i.val < k + 1 then p ⟨i.val, h⟩ else s) = p i
  rw [dif_pos i.isLt]

/-- The new last entry is exactly the appended state. -/
theorem appendPrefix_last {k : Nat} (p : Prefix k) (s : State) :
    appendPrefix p s (Fin.last (k + 1)) = s := by
  change (if h : k + 1 < k + 1 then p ⟨k + 1, h⟩ else s) = s
  rw [dif_neg (Nat.lt_irrefl (k + 1))]

/-- Truncation is a left inverse of finite tuple extension. -/
theorem truncatePrefix_append {k : Nat} (p : Prefix k) (s : State) :
    truncatePrefix (appendPrefix p s) = p := by
  funext i
  exact appendPrefix_castSucc p s i

/-- Every extended tuple is recovered from its truncation and last state. -/
theorem appendPrefix_truncate {k : Nat} (p : Prefix (k + 1)) :
    appendPrefix (truncatePrefix p) (prefixAt p (k + 1)) = p := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · rw [appendPrefix_last]
    exact prefixAt_fin p (Fin.last (k + 1))
  · rw [appendPrefix_castSucc]
    rfl

/-- Tuple extension is jointly injective in the preceding tuple and state. -/
theorem appendPrefix_eq_iff {k : Nat} (p q : Prefix k) (s t : State) :
    appendPrefix p s = appendPrefix q t ↔ p = q ∧ s = t := by
  constructor
  · intro h
    constructor
    · have ht := congrArg (fun r : Prefix (k + 1) => truncatePrefix r) h
      simpa only [truncatePrefix_append] using ht
    · have hl := congrArg (fun r : Prefix (k + 1) => r (Fin.last (k + 1))) h
      simpa only [appendPrefix_last] using hl
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Saturated access before the extension still reads the original tuple. -/
theorem prefixAt_append {k : Nat} (p : Prefix k) (s : State)
    {i : Nat} (hi : i ≤ k) :
    prefixAt (appendPrefix p s) i = prefixAt p i := by
  let j : Fin (k + 1) := ⟨i, by omega⟩
  calc
    prefixAt (appendPrefix p s) i = appendPrefix p s j.castSucc :=
      prefixAt_fin (appendPrefix p s) j.castSucc
    _ = p j := appendPrefix_castSucc p s j
    _ = prefixAt p i := (prefixAt_fin p j).symm

/-- Saturated access at the new final index reads the appended state. -/
theorem prefixAt_append_last {k : Nat} (p : Prefix k) (s : State) :
    prefixAt (appendPrefix p s) (k + 1) = s := by
  exact (prefixAt_fin (appendPrefix p s) (Fin.last (k + 1))).trans
    (appendPrefix_last p s)

/-- Truncation preserves access to every entry that remains in range. -/
theorem prefixAt_truncate {k : Nat} (p : Prefix (k + 1))
    {i : Nat} (hi : i ≤ k) :
    prefixAt (truncatePrefix p) i = prefixAt p i := by
  let j : Fin (k + 1) := ⟨i, by omega⟩
  calc
    prefixAt (truncatePrefix p) i = truncatePrefix p j :=
      prefixAt_fin (truncatePrefix p) j
    _ = p j.castSucc := rfl
    _ = prefixAt p i := (prefixAt_fin p j.castSucc).symm

/-- Extending a walk requires exactly one additional edge. -/
theorem walk_append_iff {k : Nat} (p : Prefix k) (s : State) :
    Walk (k + 1) (appendPrefix p s) ↔
      Walk k p ∧ Edge (prefixAt p k) s := by
  constructor
  · rintro ⟨hfirst, hedges⟩
    constructor
    · constructor
      · simpa only [prefixAt_append p s (Nat.zero_le k)] using hfirst
      · intro i hi
        have he := hedges i (by omega)
        simpa only [prefixAt_append p s (by omega : i ≤ k),
          prefixAt_append p s (by omega : i + 1 ≤ k)] using he
    · have he := hedges k (by omega)
      simpa only [prefixAt_append p s (Nat.le_refl k),
        prefixAt_append_last p s] using he
  · rintro ⟨⟨hfirst, hedges⟩, hlast⟩
    constructor
    · simpa only [prefixAt_append p s (Nat.zero_le k)] using hfirst
    · intro i hi
      by_cases hik : i < k
      · simpa only [prefixAt_append p s (by omega : i ≤ k),
          prefixAt_append p s (by omega : i + 1 ≤ k)] using hedges i hik
      · have hieq : i = k := by omega
        subst i
        simpa only [prefixAt_append p s (Nat.le_refl k),
          prefixAt_append_last p s] using hlast

end CrossWidthTargetCensus

#print axioms CrossWidthTargetCensus.appendPrefix
#print axioms CrossWidthTargetCensus.truncatePrefix
#print axioms CrossWidthTargetCensus.appendPrefix_castSucc
#print axioms CrossWidthTargetCensus.appendPrefix_last
#print axioms CrossWidthTargetCensus.truncatePrefix_append
#print axioms CrossWidthTargetCensus.appendPrefix_truncate
#print axioms CrossWidthTargetCensus.appendPrefix_eq_iff
#print axioms CrossWidthTargetCensus.prefixAt_append
#print axioms CrossWidthTargetCensus.prefixAt_append_last
#print axioms CrossWidthTargetCensus.prefixAt_truncate
#print axioms CrossWidthTargetCensus.walk_append_iff
