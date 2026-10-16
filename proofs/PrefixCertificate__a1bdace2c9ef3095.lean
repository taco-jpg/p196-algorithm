import Std

/-!
Kernel-checkable finite certificates for complete backward relations.

The data generator and tree ordering are untrusted.  A successful lookup is
proved to refer to a node in the tree, and every node's row is checked against
the entire executable predecessor enumeration.  Checking a stored edge list
alone would not establish the required closure and is deliberately insufficient.
-/
namespace SevenColumn.Certificate

abbrev Word := List Nat

/-- The pivot is only a search hint; lookup verifies the whole stored word.
No injectivity theorem for the code, or sortedness claim, is trusted. -/
inductive RankTree where
  | empty
  | node (pivot : Nat) (word : Word) (rank : Nat) (left right : RankTree)
  deriving Inhabited

def wordCode (w : Word) : Nat := w.foldl (fun a d => 19 * a + d) 1

def lookupKey : RankTree → Nat → Word → Option Nat
  | .empty, _, _ => none
  | .node k p r left right, key, w =>
    if key < k then lookupKey left key w
    else if k < key then lookupKey right key w
    else if w = p then some r else none

def lookup (tree : RankTree) (w : Word) : Option Nat :=
  lookupKey tree (wordCode w) w

def RankTree.All (P : Word → Nat → Prop) : RankTree → Prop
  | .empty => True
  | .node _ p r left right => left.All P ∧ P p r ∧ right.All P

instance RankTree.decAll (P : Word → Nat → Prop)
    [d : ∀ p r, Decidable (P p r)] (tree : RankTree) : Decidable (tree.All P) :=
  match tree with
  | .empty => isTrue True.intro
  | .node _ p r left right =>
    have : Decidable (left.All P) := RankTree.decAll P left
    have : Decidable (right.All P) := RankTree.decAll P right
    inferInstanceAs (Decidable (left.All P ∧ P p r ∧ right.All P))

theorem lookupKey_all {P : Word → Nat → Prop} {tree : RankTree}
    (h : tree.All P) {key : Nat} {w : Word} {r : Nat}
    (hr : lookupKey tree key w = some r) : P w r := by
  induction tree with
  | empty => simp [lookupKey] at hr
  | node k p t left right ihl ihr =>
    simp only [RankTree.All] at h
    simp only [lookupKey] at hr
    split at hr
    · exact ihl h.1 hr
    · split at hr
      · exact ihr h.2.2 hr
      · split at hr
        · rename_i hw
          subst w
          cases Option.some.inj hr
          exact h.2.1
        · contradiction

theorem lookup_all {P : Word → Nat → Prop} {tree : RankTree}
    (h : tree.All P) {w : Word} {r : Nat}
    (hr : lookup tree w = some r) : P w r :=
  lookupKey_all h hr

def checkBelow (tree : RankTree) (r : Nat) (q : Word) : Bool :=
  match lookup tree q with
  | none => false
  | some s => decide (s < r)

/-- This quantifies over the complete executable inverse, not a supplied list
of edges.  Duplicate predecessors are harmless. -/
def checkRow (tree : RankTree) (pred : Word → List Word)
    (p : Word) (r : Nat) : Bool :=
  (pred p).all (checkBelow tree r)

def CheckedRows (tree : RankTree) (pred : Word → List Word) : Prop :=
  tree.All (fun p r => checkRow tree pred p r = true)

theorem checkBelow_sound {tree : RankTree} {q : Word} {r : Nat}
    (h : checkBelow tree r q = true) :
    ∃ s, lookup tree q = some s ∧ s < r := by
  unfold checkBelow at h
  split at h
  · contradiction
  · rename_i s hs
    exact ⟨s, hs, of_decide_eq_true h⟩

theorem checkRow_sound {tree : RankTree} {pred : Word → List Word}
    {p q : Word} {r : Nat} (h : checkRow tree pred p r = true)
    (hq : q ∈ pred p) : ∃ s, lookup tree q = some s ∧ s < r := by
  exact checkBelow_sound ((List.all_eq_true.mp h) q hq)

theorem checkedRows_closed {tree : RankTree} {pred : Word → List Word}
    (checked : CheckedRows tree pred) {p q : Word} {r : Nat}
    (hp : lookup tree p = some r) (hq : q ∈ pred p) :
    ∃ s, lookup tree q = some s ∧ s < r :=
  checkRow_sound (lookup_all checked hp) hq

/-- `R p q` means that q is a genuine predecessor of p. -/
inductive BackPath (R : Word → Word → Prop) : Nat → Word → Word → Prop
  | refl (p : Word) : BackPath R 0 p p
  | step {p q z : Word} {n : Nat} :
      R p q → BackPath R n q z → BackPath R (n + 1) p z

/-- Generic soundness: every actual path is bounded if the executable inverse
contains every actual predecessor and all certificate rows pass. -/
theorem backPath_rank {tree : RankTree} {pred : Word → List Word}
    {R : Word → Word → Prop} (checked : CheckedRows tree pred)
    (complete : ∀ p q, R p q → q ∈ pred p)
    {n : Nat} {p z : Word} (path : BackPath R n p z)
    {r : Nat} (hp : lookup tree p = some r) :
    ∃ s, lookup tree z = some s ∧ n + s ≤ r := by
  induction path generalizing r with
  | refl p => exact ⟨r, hp, by omega⟩
  | @step p q z n edge tail ih =>
    obtain ⟨t, ht, hlt⟩ := checkedRows_closed checked hp (complete p q edge)
    obtain ⟨s, hs, hle⟩ := ih ht
    exact ⟨s, hs, by omega⟩

theorem backPath_length_le {tree : RankTree} {pred : Word → List Word}
    {R : Word → Word → Prop} (checked : CheckedRows tree pred)
    (complete : ∀ p q, R p q → q ∈ pred p)
    {n r bound : Nat} {p z : Word} (path : BackPath R n p z)
    (hp : lookup tree p = some r) (hr : r ≤ bound) : n ≤ bound := by
  obtain ⟨s, _, hs⟩ := backPath_rank checked complete path hp
  omega

def checkInitial (tree : RankTree) (bound : Nat) (p : Word) : Bool :=
  match lookup tree p with
  | none => false
  | some r => decide (r ≤ bound)

theorem checkInitial_sound {tree : RankTree} {p : Word} {bound : Nat}
    (h : checkInitial tree bound p = true) :
    ∃ r, lookup tree p = some r ∧ r ≤ bound := by
  unfold checkInitial at h
  split at h
  · contradiction
  · rename_i r hr
    exact ⟨r, hr, of_decide_eq_true h⟩

theorem initial_backPath_length_le {tree : RankTree} {pred : Word → List Word}
    {R : Word → Word → Prop} (checked : CheckedRows tree pred)
    (complete : ∀ p q, R p q → q ∈ pred p)
    {n bound : Nat} {p z : Word} (path : BackPath R n p z)
    (initial : checkInitial tree bound p = true) : n ≤ bound := by
  obtain ⟨r, hp, hr⟩ := checkInitial_sound initial
  exact backPath_length_le checked complete path hp hr

/-- Range combinators allow many small `decide` proofs to be assembled without
asking the kernel to normalize one enormous proposition. -/
theorem checked_range (P : Nat → Prop) (start count : Nat)
    (h : ∀ i : Fin count, P (start + i.val)) :
    ∀ u, start ≤ u → u < start + count → P u := by
  intro u hlo hhi
  have hi : u - start < count := by omega
  have he : start + (u - start) = u := by omega
  simpa only [he] using h ⟨u - start, hi⟩

theorem join_ranges (P : Nat → Prop) (lo middle hi : Nat)
    (left : ∀ u, lo ≤ u → u < middle → P u)
    (right : ∀ u, middle ≤ u → u < hi → P u) :
    ∀ u, lo ≤ u → u < hi → P u := by
  intro u hlo hhi
  by_cases hm : u < middle
  · exact left u hlo hm
  · exact right u (by omega) hhi

#print axioms backPath_rank
#print axioms initial_backPath_length_le

end SevenColumn.Certificate
