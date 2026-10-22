import P196.Agent124ForwardInvariant.Agent124Forward

/-!
# Forward walks: what the forward-invariant method can NOT exclude (sprint agent 01)

`Agent124.Forward.no_196_outside` excludes a palindrome prefix from the orbit of
196 by exhibiting a finite set of width-`k` words that contains the projection
of `orbit 196 100`, is closed under both inner-carry choices of
`forwardPrefix`, and misses the possible last-predecessor projections of that
prefix.

This module proves the converse obstruction for explicit prefixes: a list of
inner carries `es` (a *forward walk*) leading from the projection of
`orbit 196 100` to a word `w` of decimal digits that begins with `pre`.  Every
forward-closed code set containing the projection then contains `w`, and `w`
is one of the initial words `initialWordsL k pre`.  So no forward-closed set at
width `k` built from time 100 can exclude `pre`.

Scope: this is a statement about the abstraction only.  It says nothing about
whether a palindrome with prefix `pre` occurs in the orbit of 196, and it
concerns the time-100 start and the stated width only.
-/

namespace Sprint.Agent01

open SevenColumnProjection Agent124.CodeCert Agent124.Forward Agent124.PrefixK
open Agent124.PrefixL

/-- Iterate `forwardPrefix` along a list of inner carries. -/
def walk (s : List Nat) : List Nat → List Nat
  | [] => s
  | e :: es => walk (forwardPrefix s e) es

/-- The current word has width `k`, entries below 19, and the carry is a bit. -/
def stepOK (k : Nat) (s : List Nat) (e : Nat) : Bool :=
  Nat.beq s.length k && s.all (fun x => Nat.blt x 19) && Nat.ble e 1

/-- Every step of the walk is a legal abstract step. -/
def walkOK (k : Nat) (s : List Nat) : List Nat → Bool
  | [] => true
  | e :: es => stepOK k s e && walkOK k (forwardPrefix s e) es

theorem mem_walk {t : CodeTree} {k : Nat} (hk : k ≤ 32)
    (closed : t.All (fun c _ => fwdOK t k c = true)) :
    ∀ (es s : List Nat), walkOK k s es = true → Mem t s → Mem t (walk s es)
  | [], _, _, hs => hs
  | e :: es, s, h, hs => by
      simp only [walkOK, stepOK, Bool.and_eq_true, Nat.beq_eq, List.all_eq_true,
        Nat.blt_eq, Nat.ble_eq] at h
      obtain ⟨⟨⟨hl, hb⟩, he⟩, hrest⟩ := h
      exact mem_walk hk closed es _ hrest (mem_forward hk closed hb hl hs he)

/-- A full-width digit word beginning with `pre` is an initial word for `pre`. -/
theorem mem_initialWordsL_of {k : Nat} {pre w : List Nat} (hl : w.length = k)
    (hp : pre.isPrefixOf w = true) (hd : ∀ x ∈ w, x ≤ 9) :
    w ∈ initialWordsL k pre := by
  obtain ⟨tail, rfl⟩ := List.isPrefixOf_iff_prefix.mp hp
  unfold initialWordsL
  rw [List.mem_filter]
  constructor
  · rw [List.mem_flatMap]
    refine ⟨tail.length, ?_, ?_⟩
    · rw [List.mem_range]
      simp only [List.length_append] at hl
      omega
    · rw [List.mem_map]
      exact ⟨tail, mem_digitLists _ tail rfl (fun x hx => hd x (by simp [hx])), rfl⟩
  · unfold initialOK
    simp [hl]

/-- The walk ends at a full-width digit word beginning with `pre`. -/
def targetOK (k : Nat) (pre w : List Nat) : Bool :=
  Nat.beq w.length k && pre.isPrefixOf w && w.all (fun x => Nat.ble x 9)

/-- One entry `(pre, es)`: the walk `es` from `s0` is legal and reaches `pre`. -/
def entryOK (k : Nat) (s0 : List Nat) (e : List Nat × List Nat) : Bool :=
  walkOK k s0 e.2 && targetOK k e.1 (walk s0 e.2)

/-- Obstruction endpoint: for every checked entry, every forward-closed code set
of width `k` that contains the width-`k` projection of `orbit 196 100` contains
an initial word of the prefix `e.1`. -/
theorem forward_cannot_exclude {k : Nat} {s0 : List Nat} (hk : k ≤ 32)
    (hs0 : wordPrefix q100 k = s0)
    (entries : List (List Nat × List Nat))
    (h : entries.all (entryOK k s0) = true) :
    ∀ e ∈ entries, ∃ w ∈ initialWordsL k e.1, ∀ t : CodeTree,
      t.All (fun c _ => fwdOK t k c = true) → Mem t (wordPrefix q100 k) → Mem t w := by
  intro e he
  have hc := List.all_eq_true.mp h e he
  simp only [entryOK, targetOK, Bool.and_eq_true, Nat.beq_eq, List.all_eq_true,
    Nat.ble_eq] at hc
  obtain ⟨hw, ⟨hl, hp⟩, hd⟩ := hc
  refine ⟨walk s0 e.2, mem_initialWordsL_of hl hp hd, ?_⟩
  intro t closed hinit
  rw [hs0] at hinit
  exact mem_walk hk closed e.2 s0 hw hinit

end Sprint.Agent01

#print axioms Sprint.Agent01.mem_walk
#print axioms Sprint.Agent01.mem_initialWordsL_of
#print axioms Sprint.Agent01.forward_cannot_exclude
