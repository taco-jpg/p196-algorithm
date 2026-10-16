import Std

/-!
Exact local decimal obstruction for a proposed alternating 13/14 column bulk.
The overflow adjacency rule collapses this alternating bulk to uniform 9.
The uniform bulk values 0,9,18 are closed under either local phase whenever
both directional carries are spatially constant and internally consistent.
This does not assert that arbitrary finite interfaces satisfy a closed
renewal law, and does not decide the existence of decimal Lychrel numbers.
-/
namespace AlternatingBulkCollapse

def digit (q carry : Nat) : Nat := (q + carry) % 10
def carryOut (q carry : Nat) : Nat := (q + carry) / 10

def stableUniform (q : Nat) : Prop := q = 0 ∨ q = 9 ∨ q = 18

/-- Constant carries on a uniform bulk must reproduce themselves across
one decimal column. The same digit-sum formula applies to the non-overflow
phase and to the interior of a uniform region in the overflow phase. -/
def uniformStep (q next : Nat) : Prop :=
  ∃ low high : Nat, low ≤ 1 ∧ high ≤ 1 ∧
    carryOut q low = low ∧ carryOut q high = high ∧
    next = digit q low + digit q high

theorem high_column_forces_carry (q c : Nat)
    (hq : q = 13 ∨ q = 14) (hc : c ≤ 1) : carryOut q c = 1 := by
  rcases hq with rfl | rfl <;> unfold carryOut <;> omega

theorem alternating_overflow_collapse :
    digit 13 1 + digit 14 1 = 9 ∧
    digit 14 1 + digit 13 1 = 9 := by decide

theorem neutral_carry_transmission (c : Nat) (hc : c ≤ 1) :
    carryOut 9 c = c := by
  unfold carryOut
  omega

theorem uniform_zero_fixed (next : Nat) (h : uniformStep 0 next) : next = 0 := by
  obtain ⟨low, high, hl, hh, hcl, hch, hn⟩ := h
  unfold carryOut at hcl hch
  have : low = 0 ∧ high = 0 := by omega
  rcases this with ⟨rfl, rfl⟩
  simpa [digit] using hn

theorem uniform_eighteen_fixed (next : Nat) (h : uniformStep 18 next) : next = 18 := by
  obtain ⟨low, high, hl, hh, hcl, hch, hn⟩ := h
  unfold carryOut at hcl hch
  have : low = 1 ∧ high = 1 := by omega
  rcases this with ⟨rfl, rfl⟩
  simpa [digit] using hn

theorem uniform_nine_trichotomy (next : Nat) (h : uniformStep 9 next) :
    stableUniform next := by
  obtain ⟨low, high, hl, hh, _, _, hn⟩ := h
  have hlo : low = 0 ∨ low = 1 := by omega
  have hhi : high = 0 ∨ high = 1 := by omega
  rcases hlo with rfl | rfl <;> rcases hhi with rfl | rfl <;>
    rw [hn] <;> unfold stableUniform <;> decide

theorem uniform_trichotomy_invariant (q next : Nat)
    (hq : stableUniform q) (h : uniformStep q next) : stableUniform next := by
  rcases hq with rfl | rfl | rfl
  · exact Or.inl (uniform_zero_fixed next h)
  · exact uniform_nine_trichotomy next h
  · exact Or.inr (Or.inr (uniform_eighteen_fixed next h))

/-- No number of subsequent uniform local phases can recreate either
13 or 14 after the alternating bulk has collapsed to 9. -/
theorem no_alternating_recovery (trace : Nat → Nat) (hstart : trace 0 = 9)
    (hstep : ∀ t, uniformStep (trace t) (trace (t+1))) :
    ∀ t, trace t ≠ 13 ∧ trace t ≠ 14 := by
  have inv : ∀ t, stableUniform (trace t) := by
    intro t
    induction t with
    | zero => exact Or.inr (Or.inl hstart)
    | succ t ih => exact uniform_trichotomy_invariant _ _ ih (hstep t)
  intro t
  rcases inv t with h | h | h <;> omega

#print axioms high_column_forces_carry
#print axioms alternating_overflow_collapse
#print axioms uniform_trichotomy_invariant
#print axioms no_alternating_recovery

end AlternatingBulkCollapse
