import P196.CrossWidthTargetCensus.Enumeration

/-!
# Paired finite families of ordinary common targets

The accepted even prefixes enumerate both parity families. Appending their
unique terminal extension gives exactly the accepted odd prefixes. The
existing target correspondence and value injectivity turn these lists into
duplicate-free lists of ordinary common outputs at adjacent source widths.
-/

set_option autoImplicit false

namespace CrossWidthTargetCensus

open FoldedCollisionPrefixes

/-- The complete odd-prefix family, obtained by the unique extension of
each accepted even prefix. -/
def oddPrefixes (k : Nat) : List (Prefix (k + 1)) :=
  (evenPrefixes k).map extendEven

/-- All ordinary outputs shared by sources of widths 2*k+2 and 2*k+3. -/
def evenTargets (k : Nat) : List Nat :=
  (evenPrefixes k).map (evenValue k)

/-- All ordinary outputs shared by sources of widths 2*k+3 and 2*k+4. -/
def oddTargets (k : Nat) : List Nat :=
  (oddPrefixes k).map (oddValue k)

/-- Terminal extension enumerates every accepted odd prefix exactly as
specified by its finite walk and terminal condition. -/
theorem mem_oddPrefixes (k : Nat) (p : Prefix (k + 1)) :
    p ∈ oddPrefixes k ↔ OddAccepted k p := by
  unfold oddPrefixes
  constructor
  · intro hp
    obtain ⟨q, hq, rfl⟩ := List.mem_map.mp hp
    exact extendEven_accepted ((mem_evenPrefixes k q).mp hq)
  · intro hp
    exact List.mem_map.mpr ⟨truncatePrefix p,
      (mem_evenPrefixes k (truncatePrefix p)).mpr (truncatePrefix_accepted hp),
      extendEven_truncate hp⟩

/-- The extended prefix list has no repeated finite tuples. -/
theorem oddPrefixes_nodup (k : Nat) : (oddPrefixes k).Nodup := by
  change ((evenPrefixes k).map extendEven).Pairwise (fun p q => p ≠ q)
  rw [List.pairwise_map]
  exact (evenPrefixes_nodup k).imp fun hne heq =>
    hne (extendEven_injective heq)

/-- The even family contains exactly the common ordinary targets at the
specified pair of adjacent source widths. -/
theorem mem_evenTargets (k Y : Nat) :
    Y ∈ evenTargets k ↔ CommonTarget (2 * k + 2) Y := by
  unfold evenTargets
  constructor
  · intro hY
    obtain ⟨p, hp, hv⟩ := List.mem_map.mp hY
    exact (even_targets_iff k Y).mpr ⟨p, (mem_evenPrefixes k p).mp hp, hv⟩
  · intro hY
    obtain ⟨p, hp, hv⟩ := (even_targets_iff k Y).mp hY
    exact List.mem_map.mpr ⟨p, (mem_evenPrefixes k p).mpr hp, hv⟩

/-- The odd family contains exactly the common ordinary targets at the
next pair of adjacent source widths. -/
theorem mem_oddTargets (k Y : Nat) :
    Y ∈ oddTargets k ↔ CommonTarget (2 * k + 3) Y := by
  unfold oddTargets
  constructor
  · intro hY
    obtain ⟨p, hp, hv⟩ := List.mem_map.mp hY
    exact (odd_targets_iff k Y).mpr ⟨p, (mem_oddPrefixes k p).mp hp, hv⟩
  · intro hY
    obtain ⟨p, hp, hv⟩ := (odd_targets_iff k Y).mp hY
    exact List.mem_map.mpr ⟨p, (mem_oddPrefixes k p).mpr hp, hv⟩

/-- Distinct accepted even tuples have distinct ordinary target values. -/
theorem evenTargets_nodup (k : Nat) : (evenTargets k).Nodup := by
  change ((evenPrefixes k).map (evenValue k)).Pairwise (fun a b => a ≠ b)
  rw [List.pairwise_map]
  apply List.Pairwise.imp_of_mem (p := evenPrefixes_nodup k)
  intro p q hp hq hne hvalue
  exact hne ((even_value_eq_iff ((mem_evenPrefixes k p).mp hp)
    ((mem_evenPrefixes k q).mp hq)).mp hvalue)

/-- Distinct accepted odd tuples have distinct ordinary target values. -/
theorem oddTargets_nodup (k : Nat) : (oddTargets k).Nodup := by
  change ((oddPrefixes k).map (oddValue k)).Pairwise (fun a b => a ≠ b)
  rw [List.pairwise_map]
  apply List.Pairwise.imp_of_mem (p := oddPrefixes_nodup k)
  intro p q hp hq hne hvalue
  exact hne ((odd_value_eq_iff ((mem_oddPrefixes k p).mp hp)
    ((mem_oddPrefixes k q).mp hq)).mp hvalue)

/-- The two neighboring parity families contain equally many distinct
ordinary targets, since both are maps of the same even-prefix list. -/
theorem paired_target_lengths (k : Nat) :
    (evenTargets k).length = (oddTargets k).length := by
  simp only [evenTargets, oddTargets, oddPrefixes, List.length_map]

end CrossWidthTargetCensus

#print axioms CrossWidthTargetCensus.oddPrefixes
#print axioms CrossWidthTargetCensus.evenTargets
#print axioms CrossWidthTargetCensus.oddTargets
#print axioms CrossWidthTargetCensus.mem_oddPrefixes
#print axioms CrossWidthTargetCensus.oddPrefixes_nodup
#print axioms CrossWidthTargetCensus.mem_evenTargets
#print axioms CrossWidthTargetCensus.mem_oddTargets
#print axioms CrossWidthTargetCensus.evenTargets_nodup
#print axioms CrossWidthTargetCensus.oddTargets_nodup
#print axioms CrossWidthTargetCensus.paired_target_lengths
