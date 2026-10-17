import P196.Agent107FoldedTransducer.Agent107TransducerNumeric
import P196.Agent107FoldedTransducer.Agent107TransducerReachable

/-! Exact finite table paths and their edge/terminal row indices. -/
namespace Agent107.FoldedTransducer
open DecimalDigits FoldedDecimal

def edgeAt (q : Nat → Nat) (p : Nat → State) (i : Nat) : Table.Edge :=
  ⟨p i, q i, emit (p i) (q i) (p (i+1)).high, p (i+1)⟩

def terminalAt (L : Nat) (q : Nat → Nat) (p : Nat → State) : Table.TerminalRow :=
  ⟨p (L/2), inputCenter L q, terminalExtra (p (L/2)) (inputCenter L q),
    terminalCenter (p (L/2)) (inputCenter L q)⟩

def GraphAccepts (L : Nat) (q : Nat → Nat) (p : Nat → State) : Prop :=
  (∃ h, h ≤ 1 ∧ p 0 = initial h) ∧
  (∀ i, i < L/2 → edgeAt q p i ∈ Table.edges) ∧
  terminalAt L q p ∈ Table.terminals

theorem accepting_states_mem (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (hp : Accepts L q p) : ∀ i, i ≤ L/2 → p i ∈ Table.states := by
  intro i hi
  induction i with
  | zero =>
    obtain ⟨h, hh, he⟩ := hp.1
    rw [he]
    exact Table.starts_mem h hh
  | succ i ih =>
    exact Table.states_closed (p i) (p (i+1)) (q i)
      (ih (by omega)) (hp.2.1 i (by omega))

theorem graphAccepts_iff_accepts (L : Nat) (q : Nat → Nat) (p : Nat → State) :
    GraphAccepts L q p ↔ Accepts L q p := by
  constructor
  · intro hg
    refine ⟨hg.1, ?_, ?_⟩
    · intro i hi
      exact (Table.edge_sound _ (hg.2.1 i hi)).2.2.1
    · exact (Table.terminal_sound _ hg.2.2).2.1
  · intro hp
    refine ⟨hp.1, ?_, ?_⟩
    · intro i hi
      exact Table.transition_complete _ _ _
        (accepting_states_mem L q p hp i (by omega)) (hp.2.1 i hi)
    · exact Table.terminal_complete _ _
        (accepting_states_mem L q p hp (L/2) (by omega)) hp.2.2

/-- The unread half need not be admissible for finite-state uniqueness. -/
theorem accepting_state_unique (L : Nat) (q : Nat → Nat) (p r : Nat → State)
    (hp : Accepts L q p) (hr : Accepts L q r) :
    ∀ i, i ≤ L/2 → p i = r i := by
  have ha := reconstructed_admissible L q p hp
  have hp' := (accepts_symmetrize L q p).2 hp
  have hr' := (accepts_symmetrize L q r).2 hr
  intro i hi
  exact (accepting_state_eq_actual L (symmetrize L q) p ha hp' i hi).trans
    (accepting_state_eq_actual L (symmetrize L q) r ha hr' i hi).symm

theorem accepting_finitePath_unique_unrestricted (L : Nat) (q : Nat → Nat)
    (p r : Nat → State) (hp : Accepts L q p) (hr : Accepts L q r) :
    finitePath L p = finitePath L r := by
  unfold finitePath
  congr 1
  funext i
  exact accepting_state_unique L q p r hp hr i.val (by have := i.isLt; omega)

structure History (L : Nat) where
  edgeIndices : Fin (L/2) → Fin Table.edges.length
  terminalIndex : Fin Table.terminals.length

/-- This reads only source/input/target and terminal source/center. Output
values are obtained from the original table, not assumed in this relation. -/
def IndexedAccepts (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) : Prop :=
  (∃ b, b ≤ 1 ∧ p 0 = initial b) ∧
  (∀ i : Fin (L/2),
    (Table.edges.get (h.edgeIndices i)).source = p i.val ∧
    (Table.edges.get (h.edgeIndices i)).input = q i.val ∧
    (Table.edges.get (h.edgeIndices i)).target = p (i.val+1)) ∧
  (Table.terminals.get h.terminalIndex).source = p (L/2) ∧
  (Table.terminals.get h.terminalIndex).center = inputCenter L q

def historyOutput (L : Nat) (h : History L) : Word :=
  ⟨List.ofFn (fun i : Fin (L/2) => (Table.edges.get (h.edgeIndices i)).output) ++
    (Table.terminals.get h.terminalIndex).extra.toList,
    (Table.terminals.get h.terminalIndex).outputCenter⟩

theorem indexed_edge_eq (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) (hh : IndexedAccepts L q p h) (i : Fin (L/2)) :
    Table.edges.get (h.edgeIndices i) = edgeAt q p i.val := by
  have hs := Table.edge_sound _ (List.get_mem Table.edges (h.edgeIndices i))
  have hi := hh.2.1 i
  have hout : (Table.edges.get (h.edgeIndices i)).output =
      emit (p i.val) (q i.val) (p (i.val+1)).high := by
    simpa only [hi.1, hi.2.1, hi.2.2] using hs.2.2.2
  cases he : Table.edges.get (h.edgeIndices i) with
  | mk s a o t =>
    simp only [he] at hi hout
    simp only [edgeAt, hi.1, hi.2.1, hi.2.2, hout]

theorem indexed_terminal_eq (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) (hh : IndexedAccepts L q p h) :
    Table.terminals.get h.terminalIndex = terminalAt L q p := by
  have hs := Table.terminal_sound _ (List.get_mem Table.terminals h.terminalIndex)
  have hx : (Table.terminals.get h.terminalIndex).extra =
      terminalExtra (p (L/2)) (inputCenter L q) := by
    simpa only [hh.2.2.1, hh.2.2.2] using hs.2.2.1
  have hc : (Table.terminals.get h.terminalIndex).outputCenter =
      terminalCenter (p (L/2)) (inputCenter L q) := by
    simpa only [hh.2.2.1, hh.2.2.2] using hs.2.2.2
  cases he : Table.terminals.get h.terminalIndex with
  | mk s c x o =>
    have hsrc := hh.2.2.1
    have hcen := hh.2.2.2
    simp only [he] at hsrc hcen hx hc
    simp only [terminalAt, hsrc, hcen, hx, hc]

theorem indexed_accepts (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) (hh : IndexedAccepts L q p h) : Accepts L q p := by
  apply (graphAccepts_iff_accepts L q p).1
  refine ⟨hh.1, ?_, ?_⟩
  · intro i hi
    rw [← indexed_edge_eq L q p h hh ⟨i, hi⟩]
    exact List.get_mem _ _
  · rw [← indexed_terminal_eq L q p h hh]
    exact List.get_mem _ _

theorem accepting_indexed_exists (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (hp : Accepts L q p) : ∃ h, IndexedAccepts L q p h := by
  have hg := (graphAccepts_iff_accepts L q p).2 hp
  have he : ∀ i : Fin (L/2), ∃ j, Table.edges.get j = edgeAt q p i.val :=
    fun i => List.get_of_mem (hg.2.1 i.val i.isLt)
  let es := fun i : Fin (L/2) => Classical.choose (he i)
  have hes : ∀ i : Fin (L/2), Table.edges.get (es i) = edgeAt q p i.val :=
    fun i => Classical.choose_spec (he i)
  obtain ⟨t, ht⟩ := List.get_of_mem hg.2.2
  refine ⟨⟨es, t⟩, hp.1, ?_, ?_⟩
  · intro i
    change (Table.edges.get (es i)).source = _ ∧ _
    rw [hes i]
    exact ⟨rfl, rfl, rfl⟩
  · change (Table.terminals.get t).source = _ ∧ _
    rw [ht]
    exact ⟨rfl, rfl⟩

theorem indexed_output (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) (hh : IndexedAccepts L q p h) :
    historyOutput L h = pathOutput L q p := by
  have he : List.ofFn (fun i : Fin (L/2) => (Table.edges.get (h.edgeIndices i)).output) =
      List.ofFn (fun i : Fin (L/2) => emit (p i.val) (q i.val) (p (i.val+1)).high) := by
    congr 1
    funext i
    rw [indexed_edge_eq L q p h hh i]
    rfl
  simp only [historyOutput, pathOutput, he, indexed_terminal_eq L q p h hh, terminalAt]

theorem nodup_get_injective {α : Type} (xs : List α) (hx : xs.Nodup)
    (i j : Fin xs.length) (h : xs.get i = xs.get j) : i = j := by
  apply Fin.ext
  apply List.getElem?_inj i.isLt hx
  rw [List.getElem?_eq_getElem i.isLt, List.getElem?_eq_getElem j.isLt]
  exact congrArg some h

theorem indexed_history_unique (L : Nat) (q : Nat → Nat) (p r : Nat → State)
    (h k : History L) (hh : IndexedAccepts L q p h) (hk : IndexedAccepts L q r k) :
    h = k := by
  have hp := indexed_accepts L q p h hh
  have hr := indexed_accepts L q r k hk
  have hs := accepting_state_unique L q p r hp hr
  have he : h.edgeIndices = k.edgeIndices := by
    funext i
    apply nodup_get_injective Table.edges Table.edges_nodup
    rw [indexed_edge_eq L q p h hh i, indexed_edge_eq L q r k hk i]
    simp only [edgeAt, hs i.val (by have := i.isLt; omega),
      hs (i.val+1) (by have := i.isLt; omega)]
  have ht : h.terminalIndex = k.terminalIndex := by
    apply nodup_get_injective Table.terminals Table.terminals_nodup
    rw [indexed_terminal_eq L q p h hh, indexed_terminal_eq L q r k hk]
    simp only [terminalAt, hs (L/2) (by omega)]
  cases h
  cases k
  cases he
  cases ht
  rfl

theorem admissible_unique_history (L : Nat) (q : Nat → Nat) (hAd : Admissible L q) :
    ∃ h : History L, (∃ p, IndexedAccepts L q p h) ∧
      ∀ k : History L, (∃ p, IndexedAccepts L q p k) → k = h := by
  obtain ⟨h, hh⟩ := accepting_indexed_exists L q (actualState L q) (actual_accepts L q hAd)
  refine ⟨h, ⟨actualState L q, hh⟩, ?_⟩
  rintro k ⟨p, hp⟩
  exact indexed_history_unique L q p (actualState L q) k h hp hh

theorem indexed_numeric_realizable (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (h : History L) (hh : IndexedAccepts L q p h) :
    ∃ n d e, 0 < n ∧ Canonical n d L ∧
      Canonical (Lychrel196.step n) e (nextWidth (symmetrize L q) L) ∧
      foldPrefix L (columnSum d L) = foldPrefix L q ∧
      foldPrefix (nextWidth (symmetrize L q) L)
        (columnSum e (nextWidth (symmetrize L q) L)) = historyOutput L h := by
  obtain ⟨n, d, e, hn, hc, he, _, hin, hout⟩ :=
    accepting_numeric_realizable L q p (indexed_accepts L q p h hh)
  exact ⟨n, d, e, hn, hc, he, hin, hout.trans (indexed_output L q p h hh).symm⟩

#print axioms graphAccepts_iff_accepts
#print axioms accepting_state_unique
#print axioms accepting_finitePath_unique_unrestricted
#print axioms indexed_edge_eq
#print axioms indexed_terminal_eq
#print axioms indexed_accepts
#print axioms accepting_indexed_exists
#print axioms indexed_output
#print axioms nodup_get_injective
#print axioms indexed_history_unique
#print axioms admissible_unique_history
#print axioms indexed_numeric_realizable

end Agent107.FoldedTransducer
