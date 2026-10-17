import P196.Agent104P620Witness.FastRowsBase

/-!
# A kernel-friendly complete prefix inverse (Agent #124)

`pred2` enumerates the same candidate predecessors as Agent #104's
`SevenColumn.fastPrefixPredecessors`, but with the four carry guesses of each
column written out explicitly and every guard evaluated as a `Bool` built
from `Nat.blt`/`Nat.beq`.  This avoids `List.range`/`List.flatMap` closures
and `Decidable` instance unfolding during kernel reduction.

Only completeness is needed for certificate soundness: every genuine
`LongCompatible` predecessor occurs in `pred2` (`longCompatible_mem_pred2`).
Consequently a certificate whose rows are checked against `longPred2 k`
also satisfies `CheckedRows tree (longPred k)` (`checkedRows_pred2_to_long`).
Spurious extra candidates would only make the row check harder to pass.
-/

namespace Agent124.FastPred

open SevenColumn SevenColumn.Certificate

/-- Bool guard for the no-overflow equation with guessed carries `b, z`. -/
def noOK (v x y a b z : Nat) : Bool :=
  Nat.blt a 19 && Nat.beq ((a + x) / 10) b && Nat.beq ((a + z) / 10) y &&
    Nat.beq v ((a + x) % 10 + (a + z) % 10)

/-- Bool guard for the shifted overflow equation with guessed carries `b, z`. -/
def ovOK (v prev x y a b z : Nat) : Bool :=
  Nat.blt a 19 && Nat.beq ((a + x) / 10) b && Nat.beq ((prev + z) / 10) y &&
    Nat.beq v ((a + x) % 10 + (prev + z) % 10)

def noPred2 : List Nat → Nat → Nat → List (List Nat)
  | [], _, _ => [[]]
  | v :: p, x, y =>
      (cond (noOK v x y (noCandidate v x y 0 0) 0 0)
        ((noPred2 p 0 0).map (noCandidate v x y 0 0 :: ·)) []) ++
      (cond (noOK v x y (noCandidate v x y 0 1) 0 1)
        ((noPred2 p 0 1).map (noCandidate v x y 0 1 :: ·)) []) ++
      (cond (noOK v x y (noCandidate v x y 1 0) 1 0)
        ((noPred2 p 1 0).map (noCandidate v x y 1 0 :: ·)) []) ++
      (cond (noOK v x y (noCandidate v x y 1 1) 1 1)
        ((noPred2 p 1 1).map (noCandidate v x y 1 1 :: ·)) [])

def ovTailPred2 : List Nat → Nat → Nat → Nat → List (List Nat)
  | [], a, _, y =>
      cond (Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y) [[]] []
  | v :: p, prev, x, y =>
      (cond (ovOK v prev x y (overflowCandidate v prev x y 0 0) 0 0)
        ((ovTailPred2 p (overflowCandidate v prev x y 0 0) 0 0).map
          (overflowCandidate v prev x y 0 0 :: ·)) []) ++
      (cond (ovOK v prev x y (overflowCandidate v prev x y 0 1) 0 1)
        ((ovTailPred2 p (overflowCandidate v prev x y 0 1) 0 1).map
          (overflowCandidate v prev x y 0 1 :: ·)) []) ++
      (cond (ovOK v prev x y (overflowCandidate v prev x y 1 0) 1 0)
        ((ovTailPred2 p (overflowCandidate v prev x y 1 0) 1 0).map
          (overflowCandidate v prev x y 1 0 :: ·)) []) ++
      (cond (ovOK v prev x y (overflowCandidate v prev x y 1 1) 1 1)
        ((ovTailPred2 p (overflowCandidate v prev x y 1 1) 1 1).map
          (overflowCandidate v prev x y 1 1 :: ·)) [])

def ovPred2 : List Nat → List (List Nat)
  | [] => []
  | v :: p =>
      cond (Nat.blt 0 v && Nat.ble v 10)
        ((ovTailPred2 p (overflowFirst v) ((overflowFirst v + 0) / 10) 1).map
          (overflowFirst v :: ·)) []

def headPos (s : List Nat) : Bool := Nat.blt 0 (s.headD 0)

def pred2 (p : List Nat) : List (List Nat) :=
  (noPred2 p 0 0).filter headPos ++ ovPred2 p

def longPred2 (width : Nat) (p : List Nat) : List (List Nat) :=
  cond (Nat.beq p.length width) (pred2 p) []

theorem noOK_of {v x y a z : Nat} (ha : a < 19) (hy : carry a z = y)
    (hv : v = lowDigit a x + lowDigit a z) :
    noOK v x y a (carry a x) z = true := by
  unfold carry at hy
  unfold lowDigit at hv
  unfold noOK carry
  simp only [Bool.and_eq_true, Nat.blt_eq, Nat.beq_eq]
  exact ⟨⟨⟨ha, trivial⟩, hy⟩, hv⟩

theorem ovOK_of {v prev x y a z : Nat} (ha : a < 19) (hy : carry prev z = y)
    (hv : v = lowDigit a x + lowDigit prev z) :
    ovOK v prev x y a (carry a x) z = true := by
  unfold carry at hy
  unfold lowDigit at hv
  unfold ovOK carry
  simp only [Bool.and_eq_true, Nat.blt_eq, Nat.beq_eq]
  exact ⟨⟨⟨ha, trivial⟩, hy⟩, hv⟩

theorem mem_four {α : Type} {l0 l1 l2 l3 : List α} {s : α} {b z : Nat}
    (hb : b < 2) (hz : z < 2)
    (h00 : b = 0 → z = 0 → s ∈ l0) (h01 : b = 0 → z = 1 → s ∈ l1)
    (h10 : b = 1 → z = 0 → s ∈ l2) (h11 : b = 1 → z = 1 → s ∈ l3) :
    s ∈ l0 ++ l1 ++ l2 ++ l3 := by
  simp only [List.mem_append]
  have : (b = 0 ∨ b = 1) ∧ (z = 0 ∨ z = 1) := by omega
  rcases this with ⟨rfl | rfl, rfl | rfl⟩
  · exact Or.inl (Or.inl (Or.inl (h00 rfl rfl)))
  · exact Or.inl (Or.inl (Or.inr (h01 rfl rfl)))
  · exact Or.inl (Or.inr (h10 rfl rfl))
  · exact Or.inr (h11 rfl rfl)

theorem mem_cond_map {c : Bool} {l : List (List Nat)} {a : Nat} {s : List Nat}
    (hc : c = true) (hs : s ∈ l) : a :: s ∈ cond c (l.map (a :: ·)) [] := by
  subst hc
  simp only [cond_true, List.mem_map]
  exact ⟨s, hs, rfl⟩

theorem NoOverflow.mem_noPred2 {p s : List Nat} {x y : Nat}
    (h : NoOverflow p s x y) (hx : x < 2) : s ∈ noPred2 p x y := by
  induction h with
  | nil => simp [noPred2]
  | @cons p s v a x y z ha hz hy hv tail ih =>
      have hb := carry_lt_two ha hx
      have he := noCandidate_eq hy hv
      have hok := noOK_of (x := x) ha hy hv
      have hrec := ih hb
      simp only [noPred2]
      apply mem_four hb hz <;> intro hb' hz' <;> rw [hb', hz'] at he hok hrec <;>
        rw [he] <;> exact mem_cond_map hok hrec

theorem OverflowTail.mem_ovTailPred2 {p s : List Nat} {a x y : Nat}
    (h : OverflowTail p s a x y) (hx : x < 2) : s ∈ ovTailPred2 p a x y := by
  induction h with
  | @nil a x y terminal =>
      rcases terminal with ⟨z, hz, hy⟩
      have hc : (Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y) = true := by
        unfold carry at hy
        simp only [Bool.or_eq_true, Nat.beq_eq]
        have : z = 0 ∨ z = 1 := by omega
        rcases this with rfl | rfl
        · exact Or.inl (by simpa using hy)
        · exact Or.inr hy
      show [] ∈ cond (Nat.beq (a / 10) y || Nat.beq ((a + 1) / 10) y) [[]] []
      rw [hc]
      simp
  | @cons p s v a prev x y z ha hz hy hv tail ih =>
      have hb := carry_lt_two ha hx
      have he := overflowCandidate_eq hy hv
      have hok := ovOK_of (x := x) ha hy hv
      have hrec := ih hb
      simp only [ovTailPred2]
      apply mem_four hb hz <;> intro hb' hz' <;> rw [hb', hz'] at he hok hrec <;>
        rw [he] <;> exact mem_cond_map hok hrec

theorem longCompatible_mem_pred2 {p s : List Nat}
    (h : LongCompatible p s) : s ∈ pred2 p := by
  cases h with
  | @noOverflow p s a positive equations =>
      apply List.mem_append_left
      rw [List.mem_filter]
      refine ⟨NoOverflow.mem_noPred2 equations (by decide), ?_⟩
      simp [headPos, positive]
  | @overflow p s v a positive ha outer equations =>
      rcases equations.outer_carry with ⟨z, hz, hy⟩
      rcases overflowFirst_eq ha hz hy outer with ⟨hv, heq⟩
      have hx := carry_lt_two ha (show 0 < 2 by decide)
      have hvpos : 0 < v := by omega
      apply List.mem_append_right
      have hc : (Nat.blt 0 v && Nat.ble v 10) = true := by
        simp only [Bool.and_eq_true, Nat.blt_eq, Nat.ble_eq]
        omega
      simp only [ovPred2, hc, cond_true, List.mem_map]
      refine ⟨s, ?_, by rw [heq]⟩
      rw [heq]
      exact OverflowTail.mem_ovTailPred2 equations hx

theorem longPred_mem_longPred2 {width : Nat} {p q : Word}
    (h : q ∈ longPred width p) : q ∈ longPred2 width p := by
  unfold longPred at h
  unfold longPred2
  split at h
  · rename_i hp
    have hb : Nat.beq p.length width = true := by simp only [Nat.beq_eq]; exact hp
    rw [hb, cond_true]
    exact longCompatible_mem_pred2 (mem_prefixPredecessors_iff.mp h)
  · contradiction

theorem checkedRows_pred2_to_long {tree : RankTree} {width : Nat}
    (checked : CheckedRows tree (longPred2 width)) :
    CheckedRows tree (longPred width) :=
  checkedRows_of_complete_enumeration checked (fun _ _ h => longPred_mem_longPred2 h)

end Agent124.FastPred

#print axioms Agent124.FastPred.longCompatible_mem_pred2
#print axioms Agent124.FastPred.checkedRows_pred2_to_long
