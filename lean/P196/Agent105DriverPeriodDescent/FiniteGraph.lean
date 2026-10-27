import Std

/-!
The finite base-six, two-phase exterior graph for overflow word `01`.
The twelve-state separator is closed under every predecessor, even when
the first coefficient column is allowed to contain zeroes.  Its exclusion
therefore applies to every finite column path from the physical root.
-/

namespace Agent105.DriverPeriod

structure Cut where
  l0 : Fin 2
  l1 : Fin 2
  h0 : Fin 2
  h1 : Fin 2
  y : Fin 6
  deriving DecidableEq

theorem Cut.ext {s t : Cut}
    (hl0 : s.l0 = t.l0) (hl1 : s.l1 = t.l1)
    (hh0 : s.h0 = t.h0) (hh1 : s.h1 = t.h1) (hy : s.y = t.y) : s = t := by
  cases s
  cases t
  simp_all

def root : Cut := ⟨0, 0, 0, 1, 1⟩
def terminal : Cut := ⟨0, 1, 1, 0, 5⟩

/-- Literal normalization and temporal equations at one coefficient column. -/
structure Column (s t : Cut) (x0 x1 : Nat) : Prop where
  low0 : t.l0.val = (x0 + s.l0.val) / 6
  low1 : t.l1.val = (x1 + s.l1.val) / 6
  high0 : s.h0.val = (x0 + t.h0.val) / 6
  high1 : s.h1.val = (x1 + t.h1.val) / 6
  reverse1 : t.y.val = (x1 + t.h1.val) % 6
  time0 : x1 = (x0 + s.l0.val) % 6 + (x0 + t.h0.val) % 6
  time1 : x0 = (x1 + s.l1.val) % 6 + s.y.val

/-- Enumerate a column by its phase-zero coefficient and two inward carries. -/
def next? (s : Cut) (x0 : Fin 11) (a0 a1 : Fin 2) : Option Cut :=
  let x1 := (x0.val + s.l0.val) % 6 + (x0.val + a0.val) % 6
  if s.h0.val = (x0.val + a0.val) / 6 ∧
      s.h1.val = (x1 + a1.val) / 6 ∧
      x0.val = (x1 + s.l1.val) % 6 + s.y.val then
    some {
      l0 := ⟨(x0.val + s.l0.val) / 6, by
        have := x0.isLt
        have := s.l0.isLt
        omega⟩
      l1 := ⟨(x1 + s.l1.val) / 6, by
        have := s.l1.isLt
        have := Nat.mod_lt (x0.val + s.l0.val) (by decide : 0 < 6)
        have := Nat.mod_lt (x0.val + a0.val) (by decide : 0 < 6)
        dsimp [x1]
        omega⟩
      h0 := a0
      h1 := a1
      y := ⟨(x1 + a1.val) % 6, Nat.mod_lt _ (by decide)⟩ }
  else none

def Step (s t : Cut) : Prop :=
  ∃ (x0 : Fin 11) (a0 a1 : Fin 2), next? s x0 a0 a1 = some t

/-- Every bounded literal column is included in the finite graph. -/
theorem step_of_column (s t : Cut) (x0 x1 : Nat)
    (hx0 : x0 ≤ 10) (_hx1 : x1 ≤ 10) (h : Column s t x0 x1) : Step s t := by
  refine ⟨⟨x0, by omega⟩, t.h0, t.h1, ?_⟩
  have hx1 := h.time0.symm
  have hg : s.h0.val = (x0 + t.h0.val) / 6 ∧
      s.h1.val = (x1 + t.h1.val) / 6 ∧
      x0 = (x1 + s.l1.val) % 6 + s.y.val := ⟨h.high0, h.high1, h.time1⟩
  simp only [next?, hx1, Fin.val_mk, if_pos hg]
  congr 1
  apply Cut.ext
  · apply Fin.ext
    exact h.low0.symm
  · apply Fin.ext
    exact h.low1.symm
  · rfl
  · rfl
  · apply Fin.ext
    exact h.reverse1.symm

/-- The complete twelve-state predecessor separator, including both carry sums. -/
def separator : List Cut := [
  ⟨0, 0, 0, 1, 2⟩,
  ⟨0, 0, 0, 1, 3⟩,
  ⟨0, 0, 1, 0, 3⟩,
  ⟨0, 1, 0, 0, 2⟩,
  ⟨0, 1, 0, 1, 1⟩,
  ⟨0, 1, 0, 1, 2⟩,
  ⟨0, 1, 1, 0, 5⟩,
  ⟨1, 0, 0, 1, 2⟩,
  ⟨1, 0, 1, 0, 5⟩,
  ⟨1, 1, 0, 1, 1⟩,
  ⟨1, 1, 1, 0, 4⟩,
  ⟨1, 1, 1, 1, 5⟩]

def InSeparator (s : Cut) : Prop := s ∈ separator

instance (s : Cut) : Decidable (InSeparator s) :=
  inferInstanceAs (Decidable (s ∈ separator))

private def closedCheck (s : Cut) (x0 : Fin 11) (a0 a1 : Fin 2) : Bool :=
  match next? s x0 a0 a1 with
  | none => true
  | some t => decide (InSeparator t → InSeparator s)

private theorem finite_closure :
    ∀ (l0 l1 h0 h1 : Fin 2) (y : Fin 6) (x0 : Fin 11) (a0 a1 : Fin 2),
    closedCheck ⟨l0, l1, h0, h1, y⟩ x0 a0 a1 = true := by
  decide

theorem separator_of_step {s t : Cut} (h : Step s t)
    (ht : InSeparator t) : InSeparator s := by
  rcases s with ⟨l0, l1, h0, h1, y⟩
  rcases h with ⟨x0, a0, a1, hn⟩
  have hc := finite_closure l0 l1 h0 h1 y x0 a0 a1
  simp only [closedCheck, hn] at hc
  exact (of_decide_eq_true hc) ht

theorem root_not_in_separator : ¬ InSeparator root := by decide

theorem terminal_in_separator : InSeparator terminal := by decide

inductive Walk : Cut → Cut → Prop where
  | nil (s : Cut) : Walk s s
  | cons {s t u : Cut} : Step s t → Walk t u → Walk s u

theorem Walk.separator_source {s t : Cut} (h : Walk s t)
    (ht : InSeparator t) : InSeparator s := by
  induction h with
  | nil => exact ht
  | cons hs _ ih => exact separator_of_step hs (ih ht)

/-- No finite sequence of generic coefficient columns connects these endpoints. -/
theorem no_root_terminal : ¬ Walk root terminal := by
  intro h
  exact root_not_in_separator (h.separator_source terminal_in_separator)

end Agent105.DriverPeriod
