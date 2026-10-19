import P196.CrossWidthTargetCensus.Pairing
import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9FiniteProducts

/-!
# Executable enumeration of accepted finite collision prefixes

Each level appends one productive state to an already retained walk and
checks the new final edge. The fixed catalogue and the injective tuple
constructor make every level duplicate-free. Filtering the final even
terminal condition gives exactly the accepted prefixes, because validity
of their reflected traces already forces every state into the catalogue.
-/

set_option autoImplicit false

namespace CrossWidthTargetCensus

open CrossWidthCollisionStates FoldedCollisionPrefixes

/-- All walks of k edges through the productive catalogue, beginning at
the forced initial state. Only the newly added edge is tested at each level. -/
def walkPrefixes : (k : Nat) → List (Prefix k)
  | 0 => [fun _ => initial]
  | k + 1 =>
      ((walkPrefixes k).flatMap fun p => productive.map (appendPrefix p)).filter
        (fun q => decide (Edge (prefixAt q k) (prefixAt q (k + 1))))

private theorem append_productive {k : Nat} (p : Prefix k) (s : State)
    (hp : ∀ i : Fin (k + 1), p i ∈ productive) (hs : s ∈ productive) :
    ∀ i : Fin (k + 1 + 1), appendPrefix p s i ∈ productive := by
  intro i
  rw [← prefixAt_fin (appendPrefix p s) i]
  by_cases hi : i.val ≤ k
  · rw [prefixAt_append p s hi]
    exact hp _
  · have hlast : i.val = k + 1 := by have := i.isLt; omega
    rw [hlast, prefixAt_append_last p s]
    exact hs

/-- The generated tuples are exactly the walks whose retained states all
belong to the productive catalogue. -/
theorem mem_walkPrefixes (k : Nat) (p : Prefix k) :
    p ∈ walkPrefixes k ↔
      Walk k p ∧ ∀ i : Fin (k + 1), p i ∈ productive := by
  induction k with
  | zero =>
    constructor
    · intro hp
      have heq : p = (fun _ => initial) := by
        simpa only [walkPrefixes, List.mem_singleton] using hp
      subst p
      refine ⟨⟨rfl, ?_⟩, ?_⟩
      · intro i hi
        omega
      · intro i
        change initial ∈ productive
        decide +kernel
    · rintro ⟨hw, _⟩
      have heq : p = (fun _ => initial) := by
        funext i
        have hi : i = (0 : Fin 1) := by
          apply Fin.ext
          have := i.isLt
          omega
        rw [hi]
        exact hw.1
      simpa only [walkPrefixes, List.mem_singleton] using heq
  | succ k ih =>
    constructor
    · intro hp
      rw [walkPrefixes] at hp
      obtain ⟨hm, he⟩ := List.mem_filter.mp hp
      obtain ⟨q, hq, hm⟩ := List.mem_flatMap.mp hm
      obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hm
      obtain ⟨hw, hc⟩ := (ih q).mp hq
      have hedge : Edge (prefixAt (appendPrefix q s) k)
          (prefixAt (appendPrefix q s) (k + 1)) := of_decide_eq_true he
      rw [prefixAt_append q s (Nat.le_refl k),
        prefixAt_append_last q s] at hedge
      exact ⟨(walk_append_iff q s).mpr ⟨hw, hedge⟩,
        append_productive q s hc hs⟩
    · rintro ⟨hw, hc⟩
      have hrestore := appendPrefix_truncate p
      have hwalk : Walk k (truncatePrefix p) :=
        ((walk_append_iff (truncatePrefix p) (prefixAt p (k + 1))).mp
          (by simpa only [hrestore] using hw)).1
      have hcatalogue : ∀ i : Fin (k + 1), truncatePrefix p i ∈ productive := by
        intro i
        exact hc i.castSucc
      have hlast : prefixAt p (k + 1) ∈ productive := hc _
      rw [walkPrefixes]
      apply List.mem_filter.mpr
      constructor
      · apply List.mem_flatMap.mpr
        exact ⟨truncatePrefix p, (ih _).mpr ⟨hwalk, hcatalogue⟩,
          List.mem_map.mpr ⟨prefixAt p (k + 1), hlast, hrestore⟩⟩
      · exact decide_eq_true (hw.2 k (Nat.lt_succ_self k))

/-- No generated walk occurs twice. This uses the existing generic
duplicate-free product theorem and joint injectivity of tuple extension. -/
theorem walkPrefixes_nodup (k : Nat) : (walkPrefixes k).Nodup := by
  induction k with
  | zero => simp [walkPrefixes]
  | succ k ih =>
    rw [walkPrefixes]
    apply List.Pairwise.filter
    exact P196.Agent9.Ensemble.nodup_flatMap_map
      (walkPrefixes k) productive appendPrefix ih productive_nodup
      (fun p _ q _ s _ t _ he => (appendPrefix_eq_iff p q s t).mp he)

/-- The accepted prefixes for even shorter source width 2*k+2. -/
def evenPrefixes (k : Nat) : List (Prefix k) :=
  (walkPrefixes k).filter (fun p => decide (EvenTerminal (prefixAt p k)))

/-- The executable filter has exactly the previously established even
acceptance semantics, with no additional catalogue hypothesis. -/
theorem mem_evenPrefixes (k : Nat) (p : Prefix k) :
    p ∈ evenPrefixes k ↔ EvenAccepted k p := by
  rw [evenPrefixes, List.mem_filter, mem_walkPrefixes]
  constructor
  · rintro ⟨⟨hw, _⟩, ht⟩
    exact ⟨hw, of_decide_eq_true ht⟩
  · intro h
    exact ⟨⟨h.1, evenAccepted_productive h⟩, decide_eq_true h.2⟩

/-- Every even accepted finite tuple is listed once. -/
theorem evenPrefixes_nodup (k : Nat) : (evenPrefixes k).Nodup := by
  exact List.Pairwise.filter _ (walkPrefixes_nodup k)

end CrossWidthTargetCensus

#print axioms CrossWidthTargetCensus.walkPrefixes
#print axioms CrossWidthTargetCensus.mem_walkPrefixes
#print axioms CrossWidthTargetCensus.walkPrefixes_nodup
#print axioms CrossWidthTargetCensus.evenPrefixes
#print axioms CrossWidthTargetCensus.mem_evenPrefixes
#print axioms CrossWidthTargetCensus.evenPrefixes_nodup
