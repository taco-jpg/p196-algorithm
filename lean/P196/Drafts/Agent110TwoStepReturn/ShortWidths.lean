import P196.Agent5OrdinaryStreamPrefix.ExteriorCore

/-! Agent #110: exact finite widths 0 and 1 for the original Agent6.advance.
At this checkpoint compilation is pending; no theorem acceptance is inferred. -/
namespace Agent110.TwoStepShort
open P196.Agent6

theorem empty_not_period_two :
    advance (advance (⟨6, []⟩ : Exterior)) ≠ (⟨6, []⟩ : Exterior) := by
  decide

theorem all_singletons_not_period_two :
    (List.range 19).all (fun x =>
      decide (advance (advance (⟨6, [x]⟩ : Exterior)) ≠ (⟨6, [x]⟩ : Exterior))) =
      true := by
  decide

theorem singleton_not_period_two (x : Nat) (hx : x ≤ 18) :
    advance (advance (⟨6, [x]⟩ : Exterior)) ≠ (⟨6, [x]⟩ : Exterior) := by
  have hxmem : x ∈ List.range 19 := List.mem_range.mpr (by omega)
  have h := List.all_eq_true.mp all_singletons_not_period_two x hxmem
  exact of_decide_eq_true h

#print axioms empty_not_period_two
#print axioms all_singletons_not_period_two
#print axioms singleton_not_period_two
end Agent110.TwoStepShort
