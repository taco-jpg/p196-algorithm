import P196.Agent124ForwardInvariant.Agent124Forward
import P196.Agent117RemainingCycles.PrefixCycle

/-!
# Sprint agent 02: limits of the forward invariant (generic part)

`Agent124.Forward` excludes a `k`-digit palindrome prefix from the 196 orbit when it lies
outside a code-keyed set that is closed under both carry choices of
`SevenColumnProjection.forwardPrefix` and contains the projection of `orbit 196 100`.

This file gives the generic interface for the opposite direction, for code-keyed data that is
checked by kernel reduction elsewhere:

* `reach_from` / `reach_to`: a parent tree (breadth-first tree from a root code `W0`) and a
  next tree (breadth-first tree towards `W0`) show that every forward-closed predicate that
  contains one listed word contains every listed word;
* `no_rank_of_from`: if every listed word has a listed forward predecessor, then no partial rank
  function closed under the complete long inverse (`Agent124.PrefixR.RowsClosed`) gives any
  listed word a rank.

Nothing here is a statement about palindromes in the 196 orbit; these are limits of the two
finite-prefix methods.
-/

namespace Sprint.Agent02

open Agent124.CodeCert SevenColumnProjection SevenColumn SevenColumn.Certificate
open Agent124.PrefixR

/-- A predicate on words closed under both boundary carries of the prefix map at width `k`. -/
def ClosedK (k : Nat) (P : List Nat → Prop) : Prop :=
  ∀ w, P w → w.length = k → (∀ x ∈ w, x < 19) → ∀ e, e < 2 → P (forwardPrefix w e)

/-- Shift separating the depth from the packed `(code, carry)` pair in tree values. -/
def SH : Nat := 1099511627776

/-- Node check of a breadth-first parent tree rooted at `W0`. The value `v` packs
`depth * SH + parent * 2 + carry`; the node word is `forwardPrefix (parent word) carry`. -/
def fromOK (k : Nat) (fromT : CodeTree) (W0 c v : Nat) : Bool :=
  Nat.beq (decode c).length k && (decode c).all (fun a => decide (a < 19)) &&
    (Nat.beq c W0 ||
      ((match lookupC fromT ((v % SH) / 2) with
        | some vp => Nat.blt (vp / SH) (v / SH)
        | none => false) &&
        Agent117.edgeOK (decode c) (decode ((v % SH) / 2)) (v % 2)))

/-- Node check of a breadth-first tree towards `W0`. The value packs
`depth * SH + next * 2 + carry`; `forwardPrefix (node word) carry` is the next word. -/
def toOK (k : Nat) (toT : CodeTree) (W0 c v : Nat) : Bool :=
  Nat.beq (decode c).length k && (decode c).all (fun a => decide (a < 19)) &&
    (Nat.beq c W0 ||
      ((match lookupC toT ((v % SH) / 2) with
        | some vn => Nat.blt (vn / SH) (v / SH)
        | none => false) &&
        decide (v % 2 < 2) && (forwardPrefix (decode c) (v % 2) == decode ((v % SH) / 2))))

/-- Boolean check of every node of a subtree. -/
def allNodes (f : Nat → Nat → Bool) : CodeTree → Bool
  | .empty => true
  | .node c v l r => allNodes f l && f c v && allNodes f r

theorem allNodes_sound {f : Nat → Nat → Bool} :
    ∀ {t : CodeTree}, allNodes f t = true → t.All (fun c v => f c v = true)
  | .empty, _ => trivial
  | .node c v l r, h => by
      simp only [allNodes, Bool.and_eq_true] at h
      exact ⟨allNodes_sound h.1.1, h.1.2, allNodes_sound h.2⟩

theorem edgeOK_forward {p s : List Nat} {e : Nat} (h : Agent117.edgeOK p s e = true) :
    forwardPrefix s e = p ∧ e < 2 ∧ (∀ a ∈ s, a < 19) := by
  unfold Agent117.edgeOK at h
  simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at h
  exact ⟨h.2, h.1.1.1, h.1.1.2⟩

theorem all_lt19 {w : List Nat} (h : w.all (fun a => decide (a < 19)) = true) :
    ∀ a ∈ w, a < 19 := by
  intro a ha
  simpa using List.all_eq_true.mp h a ha

/-- Every listed word is forward reachable from `W0` inside any closed predicate. -/
theorem reach_from {k : Nat} {fromT : CodeTree} {W0 : Nat}
    (hT : fromT.All (fun c v => fromOK k fromT W0 c v = true))
    {P : List Nat → Prop} (hP : ClosedK k P) (h0 : P (decode W0)) :
    ∀ c v, lookupC fromT c = some v → P (decode c) := by
  suffices H : ∀ d, ∀ c v, lookupC fromT c = some v → v / SH = d → P (decode c) by
    intro c v hv
    exact H _ c v hv rfl
  intro d
  induction d using Nat.strongRecOn with
  | _ d ih =>
    intro c v hv hd
    have hok := lookupC_all hT hv
    unfold fromOK at hok
    simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq] at hok
    obtain ⟨⟨_, _⟩, hcase⟩ := hok
    rcases hcase with hc | ⟨hlook, hedge⟩
    · subst hc
      exact h0
    · split at hlook
      · rename_i vp hvp
        have hlt : vp / SH < d := by
          have := Nat.blt_eq.mp hlook
          omega
        have hpar := ih (vp / SH) hlt _ vp hvp rfl
        have hpok := lookupC_all hT hvp
        unfold fromOK at hpok
        simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq] at hpok
        obtain ⟨⟨hplen, hpb⟩, _⟩ := hpok
        obtain ⟨hfw, he, _⟩ := edgeOK_forward hedge
        rw [← hfw]
        exact hP _ hpar hplen (all_lt19 hpb) _ he
      · contradiction

/-- From every listed word, `W0` is forward reachable inside any closed predicate. -/
theorem reach_to {k : Nat} {toT : CodeTree} {W0 : Nat}
    (hT : toT.All (fun c v => toOK k toT W0 c v = true))
    {P : List Nat → Prop} (hP : ClosedK k P) :
    ∀ c v, lookupC toT c = some v → P (decode c) → P (decode W0) := by
  suffices H : ∀ d, ∀ c v, lookupC toT c = some v → v / SH = d → P (decode c) →
      P (decode W0) by
    intro c v hv
    exact H _ c v hv rfl
  intro d
  induction d using Nat.strongRecOn with
  | _ d ih =>
    intro c v hv hd hc
    have hok := lookupC_all hT hv
    unfold toOK at hok
    simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq, decide_eq_true_eq,
      beq_iff_eq] at hok
    obtain ⟨⟨hlen, hb⟩, hcase⟩ := hok
    rcases hcase with hw | ⟨⟨hlook, he⟩, hfw⟩
    · subst hw
      exact hc
    · split at hlook
      · rename_i vn hvn
        have hlt : vn / SH < d := by
          have := Nat.blt_eq.mp hlook
          omega
        have hnext : P (decode ((v % SH) / 2)) := by
          rw [← hfw]
          exact hP _ hc hlen (all_lt19 hb) _ he
        exact ih (vn / SH) hlt _ vn hvn rfl hnext
      · contradiction

/-- Every listed word has a listed predecessor (its parent, or `U0` for the root), so no rank
function closed under the complete long inverse ranks any listed word. -/
theorem no_rank_of_from {k : Nat} {fromT : CodeTree} {W0 U0 E0 : Nat}
    (hT : fromT.All (fun c v => fromOK k fromT W0 c v = true))
    (hU0 : (lookupC fromT U0).isSome = true)
    (hE0 : Agent117.edgeOK (decode W0) (decode U0) E0 = true)
    (hW0 : (decode W0).length = k ∧ ∀ a ∈ decode W0, a < 19)
    (Rk : List Nat → Option Nat) (rows : RowsClosed k Rk) :
    ∀ c v, lookupC fromT c = some v → Rk (decode c) = none := by
  suffices H : ∀ r, ∀ c v, lookupC fromT c = some v → Rk (decode c) = some r → False by
    intro c v hv
    cases hr : Rk (decode c) with
    | none => rfl
    | some r => exact (H r c v hv hr).elim
  intro r
  induction r using Nat.strongRecOn with
  | _ r ih =>
    intro c v hv hr
    have hok := lookupC_all hT hv
    unfold fromOK at hok
    simp only [Bool.and_eq_true, Bool.or_eq_true, Nat.beq_eq] at hok
    obtain ⟨⟨hlen, hb⟩, hcase⟩ := hok
    -- a listed predecessor `u` of `c`, with the forward edge as an inverse edge
    have step : ∀ u e, (lookupC fromT u).isSome = true →
        Agent117.edgeOK (decode c) (decode u) e = true → False := by
      intro u e hu hedge
      have hback := Agent117.edgeOK_sound hedge
      have hmem : decode u ∈ longPred k (decode c) := by
        simp only [longPred, hlen, if_true]
        exact hback
      obtain ⟨s, hs, hsr⟩ := rows (decode c) r (all_lt19 hb) hr (decode u) hmem
      obtain ⟨vu, hvu⟩ := Option.isSome_iff_exists.mp hu
      exact ih s hsr u vu hvu hs
    rcases hcase with hc | ⟨hlook, hedge⟩
    · subst hc
      exact step U0 E0 hU0 hE0
    · split at hlook
      · rename_i vp hvp
        exact step _ _ (by simp [hvp]) hedge
      · contradiction

/-- Keys of one tree are keys of another. -/
def keysIn (t : CodeTree) : CodeTree → Bool
  | .empty => true
  | .node c _ l r => keysIn t l && (lookupC t c).isSome && keysIn t r

theorem keysIn_sound {t : CodeTree} :
    ∀ {s : CodeTree}, keysIn t s = true → s.All (fun c _ => (lookupC t c).isSome = true)
  | .empty, _ => trivial
  | .node c v l r, h => by
      simp only [keysIn, Bool.and_eq_true] at h
      exact ⟨keysIn_sound h.1.1, h.1.2, keysIn_sound h.2⟩

end Sprint.Agent02

#print axioms Sprint.Agent02.reach_from
#print axioms Sprint.Agent02.reach_to
#print axioms Sprint.Agent02.no_rank_of_from
#print axioms Sprint.Agent02.keysIn_sound
#print axioms Sprint.Agent02.allNodes_sound
