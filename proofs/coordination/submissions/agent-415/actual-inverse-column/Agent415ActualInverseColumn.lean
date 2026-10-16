import Agent415InverseColumn
import ActualStrip

/-!
Agent #415: the arithmetic inverse-column relation is instantiated by the
repository's actual pair-word dynamics. Explicit carry alternation, a common
prefix width, and prefix return remain hypotheses, not global assertions.
Agent112's exact actual-prefix transport theorem is reused unchanged.
-/
namespace Agent415.InverseColumn
open P196.Agent4.TemporalStrip BoundaryCertificate
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open Agent104.TemporalStripObligations

/-- Extend a finite temporal word without introducing any time-seam assumption. -/
def repeatFin {α : Type} (n : Nat) (hn : 0 < n) (w : Fin n → α) : Nat → α :=
  fun i => w ⟨i % n, Nat.mod_lt i hn⟩

theorem repeatFin_periodic {α : Type} (n : Nat) (hn : 0 < n) (w : Fin n → α) :
    Sofic.Periodic n (repeatFin n hn w) := by
  intro i
  simp [repeatFin, Nat.add_mod]

theorem repeatFin_next {α : Type} (n : Nat) (hn : 0 < n) (w : Fin n → α) (i : Nat) :
    repeatFin n hn w (i+1) = w (cycleNext n hn ⟨i % n, Nat.mod_lt i hn⟩) := by
  apply congrArg w
  apply Fin.ext
  simp [cycleNext, Nat.add_mod]

/-- The scalar proof extends through the last-to-first temporal seam. -/
theorem column_to_arithmetic (n : Nat) (hn : 0 < n) (s t : Cut (Fin n))
    (x y : Fin n → Nat) (hs : Valid s) (ht : Valid t)
    (hc : Column (cycleNext n hn) s t x y) :
    ArithmeticColumn n (repeatFin n hn (encode s)) (repeatFin n hn (encode t)) := by
  refine ⟨repeatFin_periodic n hn _, repeatFin_periodic n hn _,
    repeatFin n hn (inverseOption s x y), repeatFin_periodic n hn _, ?_⟩
  intro i _hi
  refine ⟨column_permitted (cycleNext n hn) s t x y hs ht hc _, ?_⟩
  simpa only [repeatFin, cycleNext, Nat.add_mod, Nat.mod_mod] using
    column_output (cycleNext n hn) s t x y hs hc ⟨i % n, Nat.mod_lt i hn⟩

/-- A temporal boundary word computed directly from the actual pair orbit. -/
def actualWord (q : Nat → Nat) (L n : Nat) (hn : 0 < n) (i : Nat) : Sofic.Word :=
  repeatFin n hn (encode (actualCut q L n i))

/-- No postulated inverse-column correspondence remains in this statement. -/
theorem actual_inverse_columns (q : Nat → Nat) (L n width : Nat)
    (hn : 0 < n) (ha : Admissible L q)
    (hw : ∀ j : Fin n, width ≤ widthAt q L (2*j.val) ∧
      width ≤ widthAt q L (2*j.val+1))
    (hg : ∀ j : Fin n,
      carry (qAt q L (2*j.val)) (widthAt q L (2*j.val)) = 0 ∧
      carry (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1)) = 1)
    (hp : ∀ i, i < width → qAt q L (2*n) i = q i) :
    ∀ i, i < width → ArithmeticColumn n (actualWord q L n hn i)
      (actualWord q L n hn (i+1)) := by
  obtain ⟨hv, hc, _ho⟩ := Agent112.TwoPhase.actual_prefix_transport q L n width hn ha hw hg hp
  intro i hi
  exact column_to_arithmetic n hn _ _ _ _ (hv i (by omega))
    (hv (i+1) (by omega)) (hc i hi)

end Agent415.InverseColumn
#print axioms Agent415.InverseColumn.repeatFin_periodic
#print axioms Agent415.InverseColumn.repeatFin_next
#print axioms Agent415.InverseColumn.column_to_arithmetic
#print axioms Agent415.InverseColumn.actual_inverse_columns
