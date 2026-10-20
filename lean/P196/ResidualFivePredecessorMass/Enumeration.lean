import P196.Agent105AllPredecessors.Agent105Predecessors9df76b
import P196.ResidualFivePredecessorCount.Basic

set_option autoImplicit false

/-!
# Ordinary predecessors of the residual-five fiber

The existing complete numerical predecessor list is applied to every
surviving canonical target word. This enumerates actual positive integers,
including every possible source width. A source cannot occur under two
different target words because its reverse-and-add image is unique and
canonical decimal words have distinct numerical values.

Membership refers to the existing residual-five fiber. It makes no claim
about occurrence in the orbit of 196 or about unbounded inverse depth.
-/

namespace P196.ResidualFivePredecessorMass

open Lychrel196

/-- Every positive ordinary source whose next iterate belongs to the
existing residual-five fiber, using the original two-width decoder. -/
def predecessors (r : Nat) : List Nat :=
  (P196.ResidualFivePredecessorCount.survivorWords r).flatMap
    (fun ds => Agent105Predecessors9df76b.predecessors
      (Agent101.digitFn ds) ds.length)

/-- Exact membership among ordinary positive integers, without a
restriction on the width of the enumerated source. -/
theorem mem_predecessors (r m : Nat) :
    m ∈ predecessors r ↔
      0 < m ∧ step m ∈ Agent103.ResidualFiveFibers.fiber r := by
  unfold predecessors
  rw [List.mem_flatMap]
  constructor
  · rintro ⟨ds, hds, hm⟩
    have hcanonical := (Agent101.canonicalDigits_iff ds).mp
      (P196.ResidualFivePredecessorCount.survivorWords_canonical r ds hds)
    obtain ⟨hp, hs⟩ := (Agent105Predecessors9df76b.mem_predecessors
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length m hcanonical).mp hm
    have htarget : Agent101.natValue ds ∈
        P196.ResidualFivePredecessorCount.survivors r :=
      List.mem_map.mpr ⟨ds, hds, rfl⟩
    have hfiber := ((P196.ResidualFivePredecessorCount.mem_survivors
      r (Agent101.natValue ds)).mp htarget).1
    exact ⟨hp, by simpa only [hs] using hfiber⟩
  · rintro ⟨hp, hfiber⟩
    have htarget : step m ∈ P196.ResidualFivePredecessorCount.survivors r :=
      (P196.ResidualFivePredecessorCount.mem_survivors r (step m)).mpr
        ⟨hfiber, m, hp, rfl⟩
    obtain ⟨ds, hds, hvalue⟩ := List.mem_map.mp htarget
    have hcanonical := (Agent101.canonicalDigits_iff ds).mp
      (P196.ResidualFivePredecessorCount.survivorWords_canonical r ds hds)
    refine ⟨ds, hds, ?_⟩
    exact (Agent105Predecessors9df76b.mem_predecessors
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length m hcanonical).mpr
        ⟨hp, hvalue.symm⟩

/-- Each actual source is listed once: each target's complete predecessor
list is duplicate free, and distinct canonical targets have disjoint lists. -/
theorem predecessors_nodup (r : Nat) : (predecessors r).Nodup := by
  unfold predecessors
  apply List.pairwise_flatMap.mpr
  constructor
  · intro ds hds
    exact Agent105Predecessors9df76b.predecessors_nodup
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length
        ((Agent101.canonicalDigits_iff ds).mp
          (P196.ResidualFivePredecessorCount.survivorWords_canonical r ds hds))
  · apply List.Pairwise.imp_of_mem
      (p := P196.ResidualFivePredecessorCount.survivorWords_nodup r)
    intro ds es hds hes hne a ha b hb hab
    subst b
    have hd := P196.ResidualFivePredecessorCount.survivorWords_canonical r ds hds
    have he := P196.ResidualFivePredecessorCount.survivorWords_canonical r es hes
    have hleft := (Agent105Predecessors9df76b.mem_predecessors
      (Agent101.natValue ds) (Agent101.digitFn ds) ds.length a
        ((Agent101.canonicalDigits_iff ds).mp hd)).mp ha
    have hright := (Agent105Predecessors9df76b.mem_predecessors
      (Agent101.natValue es) (Agent101.digitFn es) es.length a
        ((Agent101.canonicalDigits_iff es).mp he)).mp hb
    exact hne (Agent101.natValue_injective_canonical ds es hd he
      (hleft.2.symm.trans hright.2))

end P196.ResidualFivePredecessorMass

#print axioms P196.ResidualFivePredecessorMass.mem_predecessors
#print axioms P196.ResidualFivePredecessorMass.predecessors_nodup
