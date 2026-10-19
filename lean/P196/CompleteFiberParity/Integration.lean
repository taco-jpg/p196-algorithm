import P196.CompleteFiberParity.ProfileParity
import P196.CompleteFiberParity.CrossWidth
import P196.Agent105AllPredecessors.Agent105Predecessors9df76b
import P196.Agent2OverflowFibers.Agent2OverflowBound

/-!
# Parity of the complete positive predecessor set

Agent #6: the existing numerical decoder supplies an explicit coefficient
test at each of the only two possible source widths. Cross-width divisibility
prevents two odd contributions, so their union has odd cardinality exactly
when either test accepts. The final theorem transports the result to any
duplicate-free list containing exactly the positive ordinary predecessors.
-/

set_option autoImplicit false

namespace CompleteFiberParity

open DecimalDigits Lychrel196 Agent101
open Agent105WordFiber9df76b Agent105NumericDecoder9df76b
open Agent105DecodedFiber9df76b Agent105Predecessors9df76b

/-- Decode a target at a specified source width and apply the exact
coefficient parity test. A rejected width contributes zero predecessors. -/
def oddDecoded (e : Nat → Nat) (W L : Nat) : Bool :=
  match decodeNumerical e W L with
  | none => false
  | some qs => oddProfile (half qs) (center qs)

/-- Exact parity of the existing complete numerical fiber at any width. -/
theorem decodedFiber_mod_two (e : Nat → Nat) (W L : Nat) :
    (decodedFiber e W L).length % 2 = if oddDecoded e W L then 1 else 0 := by
  unfold decodedFiber oddDecoded
  cases decodeNumerical e W L with
  | none => rfl
  | some qs => exact numericFiber_mod_two (half qs) (center qs)

/-- The complete positive predecessor count of any canonical decimal target
is odd exactly when either of its two source-width profile tests accepts. -/
theorem complete_predecessor_parity (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical Y e W) :
    (predecessors e W).length % 2 =
      if oddDecoded e W W || oddDecoded e W (W - 1) then 1 else 0 := by
  have hlong := decodedFiber_mod_two e W W
  have hshort := decodedFiber_mod_two e W (W - 1)
  have hnot := not_both_width_fibers_odd Y e W (W - 1) W htarget
    (by have hW := htarget.1; omega)
  change (decodedFiber e W W ++ decodedFiber e W (W - 1)).length % 2 = _
  rw [List.length_append, Nat.add_mod]
  cases hl : oddDecoded e W W <;>
    cases hs : oddDecoded e W (W - 1) <;>
    simp [hl, hs] at hlong hshort ⊢ <;> omega

/-- Boolean acceptance characterizes odd cardinality for the complete
ordinary positive predecessor list, without a source-width restriction. -/
theorem complete_predecessor_odd_iff (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical Y e W) :
    (predecessors e W).length % 2 = 1 ↔
      oddDecoded e W W = true ∨ oddDecoded e W (W - 1) = true := by
  rw [complete_predecessor_parity Y e W htarget]
  cases hl : oddDecoded e W W <;>
    cases hs : oddDecoded e W (W - 1) <;> simp [hl, hs]

/-- The same parity holds for any duplicate-free list enumerating exactly
the positive integers whose ordinary reverse-and-add step equals Y. -/
theorem ordinary_complete_predecessor_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical Y e W) (ns : List Nat) (hnd : ns.Nodup)
    (hcomplete : ∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) :
    ns.length % 2 =
      if oddDecoded e W W || oddDecoded e W (W - 1) then 1 else 0 := by
  have hleft : ns.length ≤ (predecessors e W).length := by
    apply P196.Agent2.OverflowFibers.nodup_subset_length_le ns (predecessors e W) hnd
    intro n hn
    exact (mem_predecessors Y e W n htarget).mpr ((hcomplete n).mp hn)
  have hright : (predecessors e W).length ≤ ns.length := by
    apply P196.Agent2.OverflowFibers.nodup_subset_length_le
      (predecessors e W) ns (predecessors_nodup Y e W htarget)
    intro n hn
    exact (hcomplete n).mpr ((mem_predecessors Y e W n htarget).mp hn)
  rw [Nat.le_antisymm hleft hright]
  exact complete_predecessor_parity Y e W htarget

#print axioms oddDecoded
#print axioms decodedFiber_mod_two
#print axioms complete_predecessor_parity
#print axioms complete_predecessor_odd_iff
#print axioms ordinary_complete_predecessor_parity

end CompleteFiberParity
