import AlternatingScalarBoundary

/-!
Agent #14: finite, nonperiodic window version of the Agent #9 obstruction.

STATUS: WIP / UNEXECUTED. These proof scripts have not been compiled in the
current session. They are not accepted results until the exact file passes
Lean 4.19.0 and its transitive axiom audit.

Only the imported exact Slot/Tile model and its local fiber lemmas are used.
The time window has no cyclic seam and requires no infinite extension.
The bound 2*n+1 is deliberately conservative; no optimality is claimed.
-/
namespace Agent14.FiniteWindowBoundary

open Agent9.AlternatingScalarBoundary

set_option autoImplicit false
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

/-- Only j < H is constrained. The shared q(j+1) preserves the actual
successive-time equation; no final-to-first identification is imposed. -/
def StepWindow (H : Nat) (outer inner : Trace) : Prop :=
  ∃ q r e : Nat → Int, ∀ j, j < H →
    Tile (outer j) (inner j) (q j) (r j) (e j) (q (j+1))

def ConstantWindow (H : Nat) (x : Trace) (s : Slot) : Prop :=
  ∀ j, j < H → x j = s

/-- Two available tiles suffice for predecessor classification at j. -/
theorem predecessor_six_window (H : Nat) (x y : Trace)
    (h : StepWindow H x y) (hy : ConstantWindow H y six)
    (j : Nat) (hj : j+1 < H) : x j = six ∨ x j = sixBad := by
  obtain ⟨q,r,e,ht⟩ := h
  have h0 : Tile (x j) six (q j) (r j) (e j) (q (j+1)) := by
    simpa only [hy j (by omega)] using ht j (by omega)
  have h1 : Tile (x (j+1)) six (q (j+1)) (r (j+1)) (e (j+1))
      (q (j+1+1)) := by
    simpa only [hy (j+1) hj] using ht (j+1) hj
  have f0 := six_fiber _ _ _ _ _ h0
  have f1 := six_fiber _ _ _ _ _ h1
  have hv := h0.outer_valid
  have he := h0.o_emission
  unfold Valid at hv
  by_cases hb : (x j).b = 1
  · left
    apply slot_ext <;> simp only [six] <;> omega
  · right
    apply slot_ext <;> simp only [sixBad] <;> omega

theorem predecessor_twelve_window (H : Nat) (x y : Trace)
    (h : StepWindow H x y) (hy : ConstantWindow H y twelve)
    (j : Nat) (hj : j+1 < H) : x j = twelve ∨ x j = twelveBad := by
  obtain ⟨q,r,e,ht⟩ := h
  have h0 : Tile (x j) twelve (q j) (r j) (e j) (q (j+1)) := by
    simpa only [hy j (by omega)] using ht j (by omega)
  have h1 : Tile (x (j+1)) twelve (q (j+1)) (r (j+1)) (e (j+1))
      (q (j+1+1)) := by
    simpa only [hy (j+1) hj] using ht (j+1) hj
  have f0 := twelve_fiber _ _ _ _ _ h0
  have f1 := twelve_fiber _ _ _ _ _ h1
  have hv := h0.outer_valid
  have he := h0.o_emission
  unfold Valid at hv
  by_cases hb : (x j).b = 0
  · left
    apply slot_ext <;> simp only [twelve] <;> omega
  · right
    apply slot_ext <;> simp only [twelveBad] <;> omega

/-- Three available inner-column tiles and two outer-column tiles remove
the exceptional predecessor at time j+1. -/
theorem viable_predecessor_six_window (H : Nat) (p x y : Trace)
    (hp : StepWindow H p x) (hx : StepWindow H x y)
    (hy : ConstantWindow H y six) (j : Nat) (hj : j+2 < H) :
    x (j+1) = six := by
  have hx0 := predecessor_six_window H x y hx hy j (by omega)
  have hx1 := predecessor_six_window H x y hx hy (j+1) (by omega)
  rcases hx1 with hgood | hbad
  · exact hgood
  · obtain ⟨q,r,e,ht⟩ := hp
    have h0 := ht j (by omega)
    have h1 : Tile (p (j+1)) sixBad (q (j+1)) (r (j+1)) (e (j+1))
        (q (j+1+1)) := by
      simpa only [hbad] using ht (j+1) (by omega)
    have f1 := sixBad_fiber _ _ _ _ _ h1
    have hb := h0.outer_valid
    have he := h0.o_emission
    have hd := h0.pending_digit
    unfold Valid at hb
    rcases hx0 with hgood0 | hbad0
    · have f0 := six_fiber _ _ _ _ _ (by simpa only [hgood0] using h0)
      omega
    · have f0 := sixBad_fiber _ _ _ _ _ (by simpa only [hbad0] using h0)
      omega

theorem viable_predecessor_twelve_window (H : Nat) (p x y : Trace)
    (hp : StepWindow H p x) (hx : StepWindow H x y)
    (hy : ConstantWindow H y twelve) (j : Nat) (hj : j+2 < H) :
    x (j+1) = twelve := by
  have hx0 := predecessor_twelve_window H x y hx hy j (by omega)
  have hx1 := predecessor_twelve_window H x y hx hy (j+1) (by omega)
  rcases hx1 with hgood | hbad
  · exact hgood
  · obtain ⟨q,r,e,ht⟩ := hp
    have h0 := ht j (by omega)
    have h1 : Tile (p (j+1)) twelveBad (q (j+1)) (r (j+1)) (e (j+1))
        (q (j+1+1)) := by
      simpa only [hbad] using ht (j+1) (by omega)
    have f1 := twelveBad_fiber _ _ _ _ _ h1
    have hb := h0.outer_valid
    have he := h0.o_emission
    have hd := h0.pending_digit
    unfold Valid at hb
    rcases hx0 with hgood0 | hbad0
    · have f0 := twelve_fiber _ _ _ _ _ (by simpa only [hgood0] using h0)
      omega
    · have f0 := twelveBad_fiber _ _ _ _ _ (by simpa only [hbad0] using h0)
      omega

/-- Shift once while retaining only a genuinely available finite window. -/
theorem stepWindow_shift (H K : Nat) (x y : Trace)
    (h : StepWindow H x y) (hk : K+1 ≤ H) :
    StepWindow K (shift x) (shift y) := by
  obtain ⟨q,r,e,ht⟩ := h
  refine ⟨(fun j => q (j+1)), (fun j => r (j+1)),
    (fun j => e (j+1)), ?_⟩
  intro j hj
  exact ht (j+1) (by omega)

/-- A generic finite-window spatial exclusion. All hypotheses concern only
j < 2*n+1. In the induction, one spatial layer is removed, time shifts once,
and two slots of usable temporal horizon are discarded. -/
theorem no_finite_window_path (s bad outside : Slot)
    (hr : outside ≠ s ∧ outside ≠ bad)
    (hpre : ∀ (H : Nat) (x y : Trace),
      StepWindow H x y → ConstantWindow H y s →
      ∀ j, j+1 < H → x j = s ∨ x j = bad)
    (herase : ∀ (H : Nat) (p x y : Trace),
      StepWindow H p x → StepWindow H x y → ConstantWindow H y s →
      ∀ j, j+2 < H → x (j+1) = s)
    (n : Nat) (cols : Nat → Trace)
    (hroot : ConstantWindow (2*n+1) (cols 0) outside)
    (htail : ConstantWindow (2*n+1) (cols n) s)
    (hpath : ∀ i, i < n → StepWindow (2*n+1) (cols i) (cols (i+1))) : False := by
  induction n generalizing cols with
  | zero =>
      have hs : outside = s :=
        (hroot 0 (by omega)).symm.trans (htail 0 (by omega))
      exact hr.1 hs
  | succ n ih =>
      by_cases hz : n = 0
      · subst n
        have hh := hpre 3 (cols 0) (cols 1) (hpath 0 (by omega)) htail 0 (by omega)
        rcases hh with h | h
        · exact hr.1 ((hroot 0 (by omega)).symm.trans h)
        · exact hr.2 ((hroot 0 (by omega)).symm.trans h)
      · have hlast : StepWindow (2*(n+1)+1) (cols n) (cols (n+1)) :=
          hpath n (by omega)
        have hprior : StepWindow (2*(n+1)+1) (cols (n-1)) (cols n) := by
          have hh := hpath (n-1) (by omega)
          simpa only [show n-1+1 = n by omega] using hh
        apply ih (fun i => shift (cols i))
        · intro j hj
          exact hroot (j+1) (by omega)
        · intro j hj
          exact herase (2*(n+1)+1) (cols (n-1)) (cols n) (cols (n+1))
            hprior hlast htail j (by omega)
        · intro i hi
          exact stepWindow_shift (2*(n+1)+1) (2*n+1) (cols i) (cols (i+1))
            (hpath i (by omega)) (by omega)

theorem no_six_window_path (outside : Slot)
    (hr : outside ≠ six ∧ outside ≠ sixBad)
    (n : Nat) (cols : Nat → Trace)
    (hroot : ConstantWindow (2*n+1) (cols 0) outside)
    (htail : ConstantWindow (2*n+1) (cols n) six)
    (hpath : ∀ i, i < n → StepWindow (2*n+1) (cols i) (cols (i+1))) : False :=
  no_finite_window_path six sixBad outside hr
    predecessor_six_window viable_predecessor_six_window n cols hroot htail hpath

theorem no_twelve_window_path (outside : Slot)
    (hr : outside ≠ twelve ∧ outside ≠ twelveBad)
    (n : Nat) (cols : Nat → Trace)
    (hroot : ConstantWindow (2*n+1) (cols 0) outside)
    (htail : ConstantWindow (2*n+1) (cols n) twelve)
    (hpath : ∀ i, i < n → StepWindow (2*n+1) (cols i) (cols (i+1))) : False :=
  no_finite_window_path twelve twelveBad outside hr
    predecessor_twelve_window viable_predecessor_twelve_window n cols hroot htail hpath

/-- A one-slot control: a physical-outside-to-six tile really is possible.
It must not be rejected by pretending its next coefficient returns to six. -/
theorem one_slot_control : Tile (⟨0,0,0,0⟩ : Slot) six 6 12 1 3 := by
  constructor <;> decide

theorem one_slot_boundary_possible :
    StepWindow 1 (constant (⟨0,0,0,0⟩ : Slot)) (constant six) := by
  refine ⟨(fun j => if j = 0 then 6 else 3), (fun _ => 12), (fun _ => 1), ?_⟩
  intro j hj
  have hj0 : j = 0 := by omega
  subst j
  change Tile (⟨0,0,0,0⟩ : Slot) six 6 12 1 3
  exact one_slot_control

#print axioms predecessor_six_window
#print axioms predecessor_twelve_window
#print axioms viable_predecessor_six_window
#print axioms viable_predecessor_twelve_window
#print axioms stepWindow_shift
#print axioms no_finite_window_path
#print axioms no_six_window_path
#print axioms no_twelve_window_path
#print axioms one_slot_control
#print axioms one_slot_boundary_possible

end Agent14.FiniteWindowBoundary
