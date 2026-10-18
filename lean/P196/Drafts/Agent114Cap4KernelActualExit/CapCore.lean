import P196.Agent6CertificateCoordinateAudit.OuterBounds

/-!
Agent #114. A kernel-reduced finite escape checker for the existing exterior
map. The indices count transitions; time zero is included in the checked
interval. The soundness theorem uses the unchanged upstream outerIterate.
-/
namespace Agent114.Exterior
open P196.Agent7.Finite

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- True exactly when an exterior exceeds the cap at some time up to steps. -/
def escapes (cap : Nat) : Nat → Outer → Bool
  | 0, s => decide (cap < s.B.length)
  | steps + 1, s => decide (cap < s.B.length) || escapes cap steps (outerNext s)

/-- A successful finite check gives a witness in the original exterior orbit. -/
theorem escapes_sound (cap steps : Nat) (s : Outer)
    (h : escapes cap steps s = true) :
    ∃ i, i ≤ steps ∧ cap < (outerIterate i s).B.length := by
  induction steps generalizing s with
  | zero =>
    exact ⟨0, Nat.le_refl _, of_decide_eq_true h⟩
  | succ steps ih =>
    by_cases hlen : cap < s.B.length
    · exact ⟨0, Nat.zero_le _, hlen⟩
    · have hnext : escapes cap steps (outerNext s) = true := by
        simpa only [escapes, hlen, decide_false, Bool.false_or] using h
      obtain ⟨i, hi, he⟩ := ih (outerNext s) hnext
      exact ⟨i + 1, by omega, he⟩

/-- All checks in a half-open natural interval, without proof-valued finite enumeration. -/
def checkRange (f : Nat → Bool) (start : Nat) : Nat → Bool
  | 0 => true
  | n + 1 => f start && checkRange f (start + 1) n

theorem checkRange_sound (f : Nat → Bool) (start n : Nat)
    (h : checkRange f start n = true) :
    ∀ i, start ≤ i → i < start + n → f i = true := by
  induction n generalizing start with
  | zero => intro i hi hi'; omega
  | succ n ih =>
    have hp : f start = true ∧ checkRange f (start + 1) n = true := by
      simpa only [checkRange, Bool.and_eq_true] using h
    intro i hi hi'
    by_cases he : i = start
    · simpa [he] using hp.1
    · exact ih (start + 1) hp.2 i (by omega) (by omega)

/-- One-step proof constructor. Candidate successors are checked by definitional equality. -/
theorem escapes_step (cap steps : Nat) (s t : Outer)
    (he : outerNext s = t) (ht : escapes cap steps t = true) :
    escapes cap (steps + 1) s = true := by
  simp only [escapes, he, ht, Bool.or_true]

/-- Composing checked cells avoids expanding a long finite check in one reduction. -/
theorem checkRange_step (f : Nat → Bool) (start n : Nat)
    (h0 : f start = true) (ht : checkRange f (start + 1) n = true) :
    checkRange f start (n + 1) = true := by
  simp only [checkRange, h0, ht, Bool.true_and]

/-- A literal exterior checked in the four-column enumeration. -/
def fourState (p a b c d : Nat) : Outer :=
  ⟨2 * (p + 1), [a + 1, b, c, d]⟩

def cell (p a b c d : Nat) : Bool :=
  !validOuter (fourState p a b c d) || escapes 4 15 (fourState p a b c d)

def line (p a b c : Nat) : Bool := checkRange (cell p a b c) 0 19

def plane (p a b : Nat) : Bool := checkRange (line p a b) 0 19

/-- One four-column batch: fixed phase and positive first coefficient. -/
def fourBatch (p a : Nat) : Bool := checkRange (plane p a) 0 19

theorem guarded_escape (s : Outer) (h : escapes 4 15 s = true) :
    (!validOuter s || escapes 4 15 s) = true := by simp only [h, Bool.or_true]

/-- Proof certificate for a bounded exit. The kernel checks every transition;
using a proposition prevents conversion from repeatedly unfolding a whole orbit. -/
inductive ExitBound (cap : Nat) : Nat → Outer → Prop
  | now (steps : Nat) (s : Outer) (h : cap < s.B.length) : ExitBound cap steps s
  | next (steps : Nat) (s t : Outer) (he : outerNext s = t)
      (tail : ExitBound cap steps t) : ExitBound cap (steps + 1) s

theorem ExitBound.checked {cap steps : Nat} {s : Outer} (h : ExitBound cap steps s) :
    escapes cap steps s = true := by
  induction h with
  | now steps s h => cases steps <;> simp only [escapes, h, decide_true, Bool.true_or]
  | next steps s t he _ ih => exact escapes_step cap steps s t he ih

theorem ExitBound.sound {cap steps : Nat} {s : Outer} (h : ExitBound cap steps s) :
    ∃ i, i ≤ steps ∧ cap < (outerIterate i s).B.length :=
  escapes_sound cap steps s h.checked

/-- Half-open interval coverage for proof-valued predicates. -/
def AllRange (P : Nat → Prop) (start count : Nat) : Prop :=
  ∀ i, start ≤ i → i < start + count → P i

theorem allRange_zero (P : Nat → Prop) (start : Nat) : AllRange P start 0 := by
  intro i h0 h1; omega

theorem allRange_step (P : Nat → Prop) (start count : Nat)
    (h0 : P start) (ht : AllRange P (start + 1) count) : AllRange P start (count + 1) := by
  intro i hi hi'
  by_cases h : i = start
  · simpa only [h] using h0
  · exact ht i (by omega) (by omega)

def CellProp (p a b c d : Nat) : Prop :=
  validOuter (fourState p a b c d) = true → ExitBound 4 15 (fourState p a b c d)
def LineProp (p a b c : Nat) : Prop := AllRange (CellProp p a b c) 0 19
def PlaneProp (p a b : Nat) : Prop := AllRange (LineProp p a b) 0 19
def FourBatch (p a : Nat) : Prop := AllRange (PlaneProp p a) 0 19

theorem valid_cell (s : Outer) (h : ExitBound 4 15 s) :
    validOuter s = true → ExitBound 4 15 s := fun _ => h

theorem invalid_cell (s : Outer) (h : validOuter s = false) :
    validOuter s = true → ExitBound 4 15 s := by simp only [h, Bool.false_eq_true, false_implies]

#print axioms escapes_sound
#print axioms checkRange_sound
#print axioms escapes_step
#print axioms checkRange_step
#print axioms guarded_escape
#print axioms ExitBound.checked
#print axioms ExitBound.sound
#print axioms allRange_zero
#print axioms allRange_step
#print axioms valid_cell
#print axioms invalid_cell
end Agent114.Exterior
