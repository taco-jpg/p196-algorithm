import P196.Agent114NeutralExteriorCycle.CycleTransport

/-!
# Prescribed exterior trim schedules

Natural offsets are the already consumed original exterior trims plus the
remaining requested trims.  Equal total trims make the offsets cyclic.
This uses the credited padding/telescoping argument and does not assert a
new decimal certificate, a width bound, or minimal padding.
-/

namespace Agent114.NeutralExteriorCycle

open Agent120.Neutral Agent114.NeutralExteriorPadding

/-- Retiming with a natural accumulated reserve.  The theorems require equal
list lengths; unmatched lists have no certified interpretation. -/
def retimeEdges (b : Nat) : Nat → List Edge → List Nat → List Edge
  | spent, e :: es, w :: ws =>
      padEdge b (spent + (w + ws.sum)) ((spent + e.u) + ws.sum) w e ::
        retimeEdges b (spent + e.u) es ws
  | _, _, _ => []

/-- The all-natural construction satisfies every local count equation. -/
theorem retimeEdges_plan (b spent : Nat) (es : List Edge) (ws : List Nat)
    (hlen : es.length = ws.length) :
    PadChain b (spent + ws.sum) (spent + (es.map Edge.u).sum)
      es (retimeEdges b spent es ws) := by
  induction es generalizing spent ws with
  | nil =>
      cases ws with
      | nil => simpa [retimeEdges] using (PadChain.nil (b := b) spent)
      | cons w ws => simp at hlen
  | cons e es ih =>
      cases ws with
      | nil => simp at hlen
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hlen
          have hp := ih (spent + e.u) ws ht
          have hc : spent + (w + ws.sum) + e.u = w + ((spent + e.u) + ws.sum) := by
            omega
          simpa only [retimeEdges, List.map_cons, List.sum_cons, Nat.add_assoc] using
            (PadChain.cons w hc hp)

/-- The output exterior trim list is exactly the prescribed schedule. -/
theorem retimeEdges_trims (b spent : Nat) (es : List Edge) (ws : List Nat)
    (hlen : es.length = ws.length) :
    (retimeEdges b spent es ws).map Edge.u = ws := by
  induction es generalizing spent ws with
  | nil =>
      cases ws with
      | nil => rfl
      | cons w ws => simp at hlen
  | cons e es ih =>
      cases ws with
      | nil => simp at hlen
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hlen
          simp only [retimeEdges, List.map_cons, padEdge, ih (spent + e.u) ws ht]

/-- Both center words and their trim count remain fixed at every edge. -/
theorem retimeEdges_centers (b spent : Nat) (es : List Edge) (ws : List Nat)
    (hlen : es.length = ws.length) :
    (retimeEdges b spent es ws).map (fun e => (e.C, e.C2, e.v)) =
      es.map (fun e => (e.C, e.C2, e.v)) := by
  induction es generalizing spent ws with
  | nil =>
      cases ws with
      | nil => rfl
      | cons w ws => simp at hlen
  | cons e es ih =>
      cases ws with
      | nil => simp at hlen
      | cons w ws =>
          have ht : es.length = ws.length := by simpa using hlen
          simp only [retimeEdges, List.map_cons, padEdge, ih (spent + e.u) ws ht]

/-- Equal total exterior trims make the offsets cyclic and preserve the full
unchanged Boolean cycle check in both directions. -/
theorem retimeEdges_cycleOK_iff (b spent : Nat) (es : List Edge) (ws B C : List Nat)
    (hlen : es.length = ws.length) (htotal : (es.map Edge.u).sum = ws.sum) :
    cycleOK b (retimeEdges b spent es ws) (suffixPad b (spent + ws.sum) B) C = true ↔
      cycleOK b es B C = true := by
  have hp := retimeEdges_plan b spent es ws hlen
  rw [htotal] at hp
  exact hp.cycleOK_iff B C

/-- Every nonnegative exterior schedule with the same length and total is
realized by an explicitly constructed accepted cycle after exterior padding. -/
theorem exists_cycle_with_exterior_schedule {b : Nat} {es : List Edge} {B C : List Nat}
    (hcert : cycleOK b es B C = true) (ws : List Nat)
    (hlen : es.length = ws.length) (htotal : (es.map Edge.u).sum = ws.sum) :
    ∃ fs : List Edge, cycleOK b fs (suffixPad b ws.sum B) C = true ∧ fs.map Edge.u = ws := by
  refine ⟨retimeEdges b 0 es ws, ?_, retimeEdges_trims b 0 es ws hlen⟩
  simpa using (retimeEdges_cycleOK_iff b 0 es ws B C hlen htotal).2 hcert

end Agent114.NeutralExteriorCycle

#print axioms Agent114.NeutralExteriorCycle.retimeEdges_plan
#print axioms Agent114.NeutralExteriorCycle.retimeEdges_cycleOK_iff
#print axioms Agent114.NeutralExteriorCycle.exists_cycle_with_exterior_schedule
