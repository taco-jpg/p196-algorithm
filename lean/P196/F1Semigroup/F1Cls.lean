import P196.F1Semigroup.F1MinDefs
/-! Congruence of the 241-class map and accepting-state counts (kernel checks). -/
namespace F1

/-- the stored accepting-set bitmask agrees with `accept` on every state -/
theorem accQ_eq : ∀ i, i < nS → accQ i = accB i := by decide +kernel


theorem clsOK_all : ∀ i, i < nS → clsOK i = true := by decide +kernel

theorem acc104 : ((List.range nC).filter fun c => accQ (Rget c)).length = 104 := by decide +kernel

theorem acc176 : ((List.range nS).filter fun i => accQ i).length = 176 := by decide +kernel


end F1
