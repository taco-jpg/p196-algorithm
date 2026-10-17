import P196.Agent117P2641.Agent124CodeCert

/-!
# Splitting row checks of one subtree by key range (Agent #124)

A row check of a subtree can be divided into several kernel-reduced Boolean
checks, each restricted to stored keys in a half-open range.  This keeps the
kernel's per-declaration work and memory bounded for subtrees whose nodes
have many predecessors, without changing the certificate data.
-/

namespace Agent124.CodeRange

open Agent124.CodeCert

def belowB (hi : Option Nat) (c : Nat) : Bool :=
  match hi with
  | none => true
  | some h => Nat.blt c h

def InRange (lo : Nat) (hi : Option Nat) (c : Nat) : Prop :=
  lo ≤ c ∧ belowB hi c = true

/-- Check the rows of the nodes of `sub` whose keys lie in `[lo, hi)`. -/
def allRowsRange (t : CodeTree) (k lo : Nat) (hi : Option Nat) : CodeTree → Bool
  | .empty => true
  | .node c r l rt =>
      allRowsRange t k lo hi l &&
        (!(Nat.ble lo c && belowB hi c) || rowOK t k c r) &&
        allRowsRange t k lo hi rt

theorem allRowsRange_sound {t : CodeTree} {k lo : Nat} {hi : Option Nat} :
    ∀ {sub : CodeTree}, allRowsRange t k lo hi sub = true →
      sub.All (fun c r => InRange lo hi c → rowOK t k c r = true)
  | .empty, _ => trivial
  | .node c r l rt, h => by
      simp only [allRowsRange, Bool.and_eq_true] at h
      refine ⟨allRowsRange_sound h.1.1, ?_, allRowsRange_sound h.2⟩
      intro hin
      have hc : (Nat.ble lo c && belowB hi c) = true := by
        simp only [Bool.and_eq_true, Nat.ble_eq]
        exact ⟨hin.1, hin.2⟩
      have := h.1.2
      rw [hc] at this
      simpa using this

theorem all_join {P : Nat → Nat → Prop} {lo mid : Nat} {hi : Option Nat} :
    ∀ {sub : CodeTree},
      sub.All (fun c r => InRange lo (some mid) c → P c r) →
      sub.All (fun c r => InRange mid hi c → P c r) →
      sub.All (fun c r => InRange lo hi c → P c r)
  | .empty, _, _ => trivial
  | .node c r l rt, h1, h2 => by
      refine ⟨all_join h1.1 h2.1, ?_, all_join h1.2.2 h2.2.2⟩
      intro hin
      by_cases hc : c < mid
      · exact h1.2.1 ⟨hin.1, by simp [belowB, Nat.blt_eq, hc]⟩
      · exact h2.2.1 ⟨by omega, hin.2⟩

theorem all_full {P : Nat → Nat → Prop} :
    ∀ {sub : CodeTree}, sub.All (fun c r => InRange 0 none c → P c r) → sub.All P
  | .empty, _ => trivial
  | .node c r l rt, h =>
      ⟨all_full h.1, h.2.1 ⟨Nat.zero_le c, rfl⟩, all_full h.2.2⟩

end Agent124.CodeRange

#print axioms Agent124.CodeRange.allRowsRange_sound
#print axioms Agent124.CodeRange.all_join
#print axioms Agent124.CodeRange.all_full
