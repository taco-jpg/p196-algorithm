import P196.OddPredecessorTargetCensus.EvenWords

/-!
# The forty-five and fifty-five outer coefficient choices

Agent #6: odd multiplicity allows a low odd outer coefficient or a high
even outer coefficient. The next independent coefficient is even. These
two coefficients partition into forty-five choices without a terminal
carry and fifty-five choices with one; the arithmetic characterizations
below are used by the separate actual-carry proof.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

/-- The outer two independent coefficients in the no-overflow class. -/
def noOverflowPrefixes : List (Nat × Nat) :=
  ([1, 3, 5, 7].flatMap fun s => evenCoefficients.map fun t => (s, t)) ++
    ([0, 2, 4, 6, 8].map fun t => (9, t))

/-- The outer two independent coefficients in the overflow class. -/
def overflowPrefixes : List (Nat × Nat) :=
  ([10, 12, 14, 16, 18].flatMap fun s => evenCoefficients.map fun t => (s, t)) ++
    ([10, 12, 14, 16, 18].map fun t => (9, t))

theorem mem_noOverflowPrefixes (s t : Nat) :
    (s, t) ∈ noOverflowPrefixes ↔
      s ≤ 9 ∧ s % 2 = 1 ∧ t ≤ 18 ∧ t % 2 = 0 ∧ (s ≤ 7 ∨ t ≤ 8) := by
  simp [noOverflowPrefixes, List.mem_flatMap, mem_evenCoefficients,
    Prod.mk.injEq] <;> omega

theorem mem_overflowPrefixes (s t : Nat) :
    (s, t) ∈ overflowPrefixes ↔
      t ≤ 18 ∧ t % 2 = 0 ∧
        ((10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) ∨ (s = 9 ∧ 10 ≤ t)) := by
  simp [overflowPrefixes, List.mem_flatMap, mem_evenCoefficients,
    Prod.mk.injEq] <;> omega

theorem noOverflowPrefixes_nodup : noOverflowPrefixes.Nodup := by decide

theorem overflowPrefixes_nodup : overflowPrefixes.Nodup := by decide

theorem length_noOverflowPrefixes : noOverflowPrefixes.length = 45 := by decide

theorem length_overflowPrefixes : overflowPrefixes.length = 55 := by decide

#print axioms noOverflowPrefixes
#print axioms overflowPrefixes
#print axioms mem_noOverflowPrefixes
#print axioms mem_overflowPrefixes
#print axioms noOverflowPrefixes_nodup
#print axioms overflowPrefixes_nodup
#print axioms length_noOverflowPrefixes
#print axioms length_overflowPrefixes

end OddPredecessorTargetCensus
