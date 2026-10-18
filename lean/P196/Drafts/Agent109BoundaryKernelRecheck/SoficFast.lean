import P196.Drafts.ResearchMainExistenceAttempt.SoficProof

/-!
Agent #109: a kernel-efficient projection checker with a proved soundness
theorem into the unchanged `Sofic.Projection` predicate of `SoficProof.lean`.

The original `Sofic.checkProjection` compares all pairs of raw nodes and looks
ranks up with `findIdx`; that is quadratic-to-cubic and exhausts memory under
`decide +kernel` for the larger graphs. Here ranks/projections and destination
edges are looked up in binary search trees, and only node pairs in a
source-vertex bucket are visited; a separate conjunct checks that every raw node
lies in its own bucket and every tree edge lies in the destination graph.
Soundness does not assume the trees are sorted, balanced or complete: a wrong
tree can only make the Boolean check fail.
-/

namespace Sofic.Fast

open Sofic

inductive BT (α : Type) where
  | leaf : BT α
  | node : BT α → Nat → α → BT α → BT α

def BT.find {α : Type} : BT α → Nat → Option α
  | .leaf, _ => none
  | .node l k v r, x => if x < k then l.find x else if k < x then r.find x else some v

def BT.toList {α : Type} : BT α → List (Nat × α)
  | .leaf => []
  | .node l k v r => l.toList ++ [(k, v)] ++ r.toList

theorem BT.find_mem {α : Type} (t : BT α) (x : Nat) (v : α) (h : t.find x = some v) :
    (x, v) ∈ t.toList := by
  induction t with
  | leaf => simp [BT.find] at h
  | node l k w r ihl ihr =>
    simp only [BT.find] at h
    simp only [BT.toList, List.mem_append, List.mem_singleton]
    by_cases h1 : x < k
    · rw [if_pos h1] at h; exact Or.inl (Or.inl (ihl h))
    · rw [if_neg h1] at h
      by_cases h2 : k < x
      · rw [if_pos h2] at h; exact Or.inr (ihr h)
      · rw [if_neg h2] at h
        have hx : x = k := by omega
        cases h; subst hx; exact Or.inl (Or.inr rfl)

/-- Node and edge keys (the edge key is the original `decodeEdge` encoding). -/
def code (a : Node) : Nat := ((a.1.src * 4096 + a.1.dst) * 4096 + a.1.lab) * 65536 + a.2
def ecode (e : LEdge) : Nat := (e.src * 4096 + e.dst) * 4096 + e.lab

def rankT (t : BT (Nat × Nat)) (a : Node) : Nat := ((t.find (code a)).getD (0, 0)).1
def projT (t : BT (Nat × Nat)) (a : Node) : Nat := ((t.find (code a)).getD (0, 0)).2
def bucket (bt : BT (List Node)) (v : Nat) : List Node := (bt.find v).getD []

/-- Destination-edge membership: the tree stores, under the edge key, an index
into the destination graph, which is rechecked with `h[i]?`. -/
def edgeOK (h : Graph) (ht : BT (Nat × LEdge)) (e : LEdge) : Bool :=
  match ht.find (ecode e) with
  | some (i, e') => e' == e && h[i]? == some e
  | none => false

/-- Local condition for one candidate pair. -/
def pairOK (output : Nat → Nat → Option Nat) (h : Graph) (t : BT (Nat × Nat))
    (ht : BT (Nat × LEdge)) (a b : Node) : Bool :=
  if a.1.dst == b.1.src then
    match output a.2 b.2 with
    | none => true
    | some l => decide (rankT t a ≤ rankT t b) &&
        (rankT t a != rankT t b || edgeOK h ht { src := projT t a, dst := projT t b, lab := l })
  else true

/-- Every node of `ns` lies in the bucket of its source vertex. -/
def bucketsOK (bt : BT (List Node)) (ns : List Node) : Bool :=
  ns.all fun b => (bucket bt b.1.src).contains b

/-- The pair condition for every node of `ns` against its destination bucket. -/
def pairsOK (output : Nat → Nat → Option Nat) (h : Graph) (t : BT (Nat × Nat))
    (bt : BT (List Node)) (ht : BT (Nat × LEdge)) (ns : List Node) : Bool :=
  ns.all fun a => (bucket bt a.1.dst).all fun b => pairOK output h t ht a b

theorem edgeOK_mem {h : Graph} {ht : BT (Nat × LEdge)} {e : LEdge}
    (he : edgeOK h ht e = true) : e ∈ h := by
  unfold edgeOK at he
  split at he
  · rename_i i e' _
    simp only [Bool.and_eq_true, beq_iff_eq] at he
    exact List.mem_of_getElem? he.2
  · simp at he

/-- **Soundness.** The three Boolean checks over the complete raw node list give
the original `Sofic.Projection` property for the tree-defined rank and projection. -/
theorem fast_sound {fiber : Nat → List Nat} {output : Nat → Nat → Option Nat}
    {g h : Graph} {t : BT (Nat × Nat)} {bt : BT (List Node)} {ht : BT (Nat × LEdge)}
    (hb : bucketsOK bt (rawNodes fiber g) = true)
    (hp : pairsOK output h t bt ht (rawNodes fiber g) = true) :
    Projection fiber output g h (rankT t) (projT t) := by
  intro a ha b hbmem l hcomp
  obtain ⟨hsrc, hout⟩ := hcomp
  have hbk : b ∈ bucket bt a.1.dst := by
    have := List.all_eq_true.mp hb b hbmem
    simp only [List.contains_iff_mem] at this
    rw [hsrc]; exact this
  have hpair := List.all_eq_true.mp (List.all_eq_true.mp hp a ha) b hbk
  unfold pairOK at hpair
  simp only [hsrc, beq_self_eq_true, if_true, hout, Bool.and_eq_true, decide_eq_true_eq,
    Bool.or_eq_true, bne_iff_ne, ne_eq] at hpair
  refine ⟨hpair.1, fun heq => ?_⟩
  rcases hpair.2 with hne | hok
  · exact absurd heq hne
  · exact edgeOK_mem hok

/-- Chunked form: the node list may be split into consecutive pieces. -/
theorem pairsOK_append (output : Nat → Nat → Option Nat) (h : Graph) (t : BT (Nat × Nat))
    (bt : BT (List Node)) (ht : BT (Nat × LEdge)) (xs ys : List Node) :
    pairsOK output h t bt ht (xs ++ ys) =
      (pairsOK output h t bt ht xs && pairsOK output h t bt ht ys) := by
  simp [pairsOK, List.all_append]

theorem bucketsOK_append (bt : BT (List Node)) (xs ys : List Node) :
    bucketsOK bt (xs ++ ys) = (bucketsOK bt xs && bucketsOK bt ys) := by
  simp [bucketsOK, List.all_append]

/-- Chunked evaluation of `List.all`: consecutive slices of width `m`. -/
theorem all_of_chunks {α : Type} (P : α → Bool) (m : Nat) :
    ∀ (K : Nat) (l : List α), (∀ i, i < K → ((l.drop (i * m)).take m).all P = true) →
      l.drop (K * m) = [] → l.all P = true := by
  intro K
  induction K with
  | zero => intro l _ hd; simp at hd; subst hd; rfl
  | succ K ih =>
    intro l hc hd
    have h0 := hc 0 (by omega)
    simp only [Nat.zero_mul, List.drop_zero] at h0
    have hrest : (l.drop m).all P = true := by
      apply ih
      · intro i hi
        have := hc (i + 1) (by omega)
        rw [List.drop_drop, show m + i * m = (i + 1) * m by rw [Nat.succ_mul]; omega]
        exact this
      · rw [List.drop_drop, show m + K * m = (K + 1) * m by rw [Nat.succ_mul]; omega]
        exact hd
    rw [← List.take_append_drop m l, List.all_append, h0, hrest]; rfl

theorem pairsOK_chunks (output : Nat → Nat → Option Nat) (h : Graph) (t : BT (Nat × Nat))
    (bt : BT (List Node)) (ht : BT (Nat × LEdge)) (m K : Nat) (l : List Node)
    (hc : ∀ i, i < K → pairsOK output h t bt ht ((l.drop (i * m)).take m) = true)
    (hd : l.drop (K * m) = []) : pairsOK output h t bt ht l = true :=
  all_of_chunks _ m K l hc hd

theorem bucketsOK_chunks (bt : BT (List Node)) (m K : Nat) (l : List Node)
    (hc : ∀ i, i < K → bucketsOK bt ((l.drop (i * m)).take m) = true)
    (hd : l.drop (K * m) = []) : bucketsOK bt l = true :=
  all_of_chunks _ m K l hc hd

theorem rawNodes_append (fiber : Nat → List Nat) (a b : Graph) :
    rawNodes fiber (a ++ b) = rawNodes fiber a ++ rawNodes fiber b := by
  simp [rawNodes, List.flatMap_append]

theorem pairsOK_graph_append (output : Nat → Nat → Option Nat) (h : Graph) (t : BT (Nat × Nat))
    (bt : BT (List Node)) (ht : BT (Nat × LEdge)) (fiber : Nat → List Nat) (a b : Graph)
    (ha : pairsOK output h t bt ht (rawNodes fiber a) = true)
    (hb : pairsOK output h t bt ht (rawNodes fiber b) = true) :
    pairsOK output h t bt ht (rawNodes fiber (a ++ b)) = true := by
  rw [rawNodes_append, pairsOK_append, ha, hb]; rfl

theorem bucketsOK_graph_append (bt : BT (List Node)) (fiber : Nat → List Nat) (a b : Graph)
    (ha : bucketsOK bt (rawNodes fiber a) = true) (hb : bucketsOK bt (rawNodes fiber b) = true) :
    bucketsOK bt (rawNodes fiber (a ++ b)) = true := by
  rw [rawNodes_append, bucketsOK_append, ha, hb]; rfl

end Sofic.Fast

#print axioms Sofic.Fast.BT.find_mem
#print axioms Sofic.Fast.fast_sound
#print axioms Sofic.Fast.all_of_chunks
