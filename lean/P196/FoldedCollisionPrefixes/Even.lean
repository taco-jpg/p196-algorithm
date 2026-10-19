import P196.FoldedCollisionPrefixes.Prefixes

/-!
# Even shorter widths and doubled midpoint reflection

A finite prefix with k edges reconstructs a full trace of shorter width
2*k+2. The middle edge joins the final retained state to its reflection.
Its coefficient parity is exactly the remaining center condition for the
longer word. Extraction and reflection are inverse on the active interval.
-/

set_option autoImplicit false

namespace FoldedCollisionPrefixes

open CrossWidthCollisionStates CrossWidthCollisionPaths

private theorem even_reflection (k : Nat) (p : Prefix k)
    {i : Nat} (hi : 1 ≤ i) (hiL : i ≤ 2 * k + 2) :
    evenTrace k p (2 * k + 2 + 1 - i) =
      CrossWidthCollisionPaths.flip (evenTrace k p i) := by
  by_cases hleft : i ≤ k + 1
  · have hmirror : ¬ (2 * k + 2 + 1 - i ≤ k + 1) := by omega
    have hindex : 2 * k + 2 - (2 * k + 2 + 1 - i) = i - 1 := by omega
    simp only [evenTrace, if_pos hleft, if_neg hmirror, hindex]
  · have hmirror : 2 * k + 2 + 1 - i ≤ k + 1 := by omega
    have hindex : 2 * k + 2 + 1 - i - 1 = 2 * k + 2 - i := by omega
    simp only [evenTrace, if_neg hleft, if_pos hmirror, hindex,
      flip_involution]

private theorem even_center_word (k : Nat) (p : Prefix k) :
    longWord (2 * k + 2) (evenTrace k p) (k + 1) =
      (prefixAt p k).x + (prefixAt p k).u + 9 -
        10 * (prefixAt p k).v := by
  have hinner : ¬ (k + 1 = 0 ∨ k + 1 = 2 * k + 2) := by omega
  have hmid := evenTrace_prefix k p (i := k) (Nat.le_refl k)
  have hnext : evenTrace k p (k + 1 + 1) =
      CrossWidthCollisionPaths.flip (prefixAt p k) := by
    have hright : ¬ (k + 1 + 1 ≤ k + 1) := by omega
    have hindex : 2 * k + 2 - (k + 1 + 1) = k := by omega
    simp only [evenTrace, if_neg hright, hindex]
  simp only [longWord, if_neg hinner, hmid, hnext,
    CrossWidthCollisionPaths.flip]

private theorem even_closed (k : Nat) (p : Prefix k)
    (hw : Walk k p)
    (ht : Edge (prefixAt p k)
      (CrossWidthCollisionPaths.flip (prefixAt p k))) :
    Closed (2 * k + 2) (evenTrace k p) := by
  refine ⟨by omega, ?_, ?_, ?_, ?_⟩
  · exact (evenTrace_prefix k p (i := 0) (by omega)).trans hw.1
  · have hright : ¬ (2 * k + 2 ≤ k + 1) := by omega
    simp only [evenTrace, if_neg hright, Nat.sub_self, hw.1, flip_initial]
  · intro i hi hiL
    by_cases hbefore : i < k + 1
    · have hs : i ≤ k + 1 := by omega
      have ht' : i + 1 ≤ k + 1 := by omega
      have hprev : i - 1 < k := by omega
      have hindex : i - 1 + 1 = i := by omega
      simp only [evenTrace, if_pos hs, if_pos ht', Nat.add_sub_cancel]
      simpa only [hindex] using hw.2 (i - 1) hprev
    · by_cases hmid : i = k + 1
      · subst i
        have hright : ¬ (k + 1 + 1 ≤ k + 1) := by omega
        have hindex : 2 * k + 2 - (k + 1 + 1) = k := by omega
        simpa only [evenTrace, Nat.le_refl, if_true, if_neg hright,
          Nat.add_sub_cancel, hindex] using ht
      · have hs : ¬ (i ≤ k + 1) := by omega
        have ht' : ¬ (i + 1 ≤ k + 1) := by omega
        have hprev : 2 * k + 2 - (i + 1) < k := by omega
        have hindex : 2 * k + 2 - (i + 1) + 1 = 2 * k + 2 - i := by omega
        have he := hw.2 (2 * k + 2 - (i + 1)) hprev
        have hre := (edge_flip_iff _ _).mp he
        simp only [evenTrace, if_neg hs, if_neg ht']
        simpa only [hindex] using hre
  · intro i hi hiL
    exact even_reflection k p hi hiL

/-- Extracting the retained half and reflecting it recovers every active
state of a closed trace of even shorter width. -/
theorem evenTrace_take {k : Nat} {f : Nat → State}
    (h : Closed (2 * k + 2) f) :
    ∀ i, 1 ≤ i → i ≤ 2 * k + 2 →
      evenTrace k (takePrefix k f) i = f i := by
  intro i hi hiL
  by_cases hleft : i ≤ k + 1
  · have hindex : i - 1 ≤ k := by omega
    simp only [evenTrace, if_pos hleft, prefixAt_take k f hindex,
      Nat.sub_add_cancel hi]
  · have hindex : 2 * k + 2 - i ≤ k := by omega
    have hmirror : f (2 * k + 2 - i + 1) =
        CrossWidthCollisionPaths.flip (f i) := by
      have he : 2 * k + 2 + 1 - i = 2 * k + 2 - i + 1 := by omega
      simpa only [he] using h.reflection i hi hiL
    simp only [evenTrace, if_neg hleft, prefixAt_take k f hindex,
      hmirror, flip_involution]

/-- The retained half of every valid even-width trace satisfies the
finite walk and the doubled midpoint terminal condition. -/
theorem evenAccepted_take {k : Nat} {f : Nat → State}
    (h : Valid (2 * k + 2) f) :
    EvenAccepted k (takePrefix k f) := by
  refine ⟨⟨?_, ?_⟩, ?_⟩
  · rw [prefixAt_take k f (i := 0) (by omega)]
    exact h.toClosed.first
  · intro i hi
    rw [prefixAt_take k f (i := i) (by omega),
      prefixAt_take k f (i := i + 1) (by omega)]
    exact h.toClosed.edge (i + 1) (by omega) (by omega)
  · rw [prefixAt_take k f (i := k) (Nat.le_refl k)]
    have hnext : f (k + 1 + 1) =
        CrossWidthCollisionPaths.flip (f (k + 1)) := by
      have hindex : 2 * k + 2 + 1 - (k + 1) = k + 1 + 1 := by omega
      simpa only [hindex] using
        h.toClosed.reflection (k + 1) (by omega) (by omega)
    constructor
    · simpa only [hnext] using
        h.toClosed.edge (k + 1) (by omega) (by omega)
    · have hm := h.long_center (k + 1) (by omega) (by omega)
      have hinner : ¬ (k + 1 = 0 ∨ k + 1 = 2 * k + 2) := by omega
      simpa only [longWord, if_neg hinner, hnext,
        CrossWidthCollisionPaths.flip] using hm

/-- Even acceptance is exactly validity of the reconstructed full trace.
The shorter word has no central position; the longer word's central
parity is supplied by the even terminal predicate. -/
theorem even_valid_iff (k : Nat) (p : Prefix k) :
    EvenAccepted k p ↔ Valid (2 * k + 2) (evenTrace k p) := by
  constructor
  · intro h
    refine ⟨even_closed k p h.1 h.2.1, ?_, ?_⟩
    · intro i hi hcenter
      omega
    · intro i hi hcenter
      have hindex : i = k + 1 := by omega
      subst i
      simpa only [even_center_word k p] using h.2.2
  · intro h
    have ht := evenAccepted_take h
    simpa only [takePrefix_evenTrace] using ht

end FoldedCollisionPrefixes

#print axioms FoldedCollisionPrefixes.even_valid_iff
#print axioms FoldedCollisionPrefixes.evenTrace_take
#print axioms FoldedCollisionPrefixes.evenAccepted_take
