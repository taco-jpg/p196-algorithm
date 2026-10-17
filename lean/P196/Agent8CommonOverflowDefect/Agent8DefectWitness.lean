import P196.Agent8CommonOverflowDefect.Agent8DefectNumeric

/-! A kernel-checked actual-integer witness for nonzero common-overflow
transport. The second seed ends in zero; both initial widths are canonical.
Finite witnesses certify nonvacuity, not the universal transport theorem. -/

namespace P196.Agent8.CommonOverflowDefect.Witness

open DecimalDigits FoldedDecimal

def leftDigits (i : Nat) : Nat :=
  if i = 0 ∨ i = 2 then 5 else if i = 3 ∨ i = 4 then 9 else 0

def rightDigits (i : Nat) : Nat :=
  if i = 1 then 1 else if i = 3 ∨ i = 4 then 9 else 0

def leftWord : Nat → Nat := columnSum leftDigits 5
def rightWord : Nat → Nat := columnSum rightDigits 5

theorem left_canonical : Canonical 99505 leftDigits 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold leftDigits
  split <;> (first | omega | split <;> omega)

theorem right_canonical : Canonical 99010 rightDigits 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  unfold rightDigits
  split <;> (first | omega | split <;> omega)

theorem left_admissible : Admissible 5 leftWord :=
  NormalizationBridge.canonical_admissible 99505 leftDigits 5 left_canonical

theorem right_admissible : Admissible 5 rightWord :=
  NormalizationBridge.canonical_admissible 99010 rightDigits 5 right_canonical

theorem terminal_carries : carry leftWord 5 = 1 ∧ carry rightWord 5 = 1 := by
  decide

theorem old_digit_defect : ∀ i, i < 5 → oldDigitDefect leftWord rightWord 5 i =
    if i = 0 then -5 else if i = 4 then 5 else 0 := by
  intro i hi
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl <;> decide

theorem antisymmetric : AntisymmetricDefect leftWord rightWord 5 := by
  intro i hi
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl <;> decide

theorem nonzero_old_digit : ∃ i, i < 5 ∧ output leftWord i ≠ output rightWord i := by
  exact ⟨0, by decide, by decide⟩

theorem exact_paired_difference : ∀ i, i < 6 →
    (nextColumns leftWord 5 i : Int) - (nextColumns rightWord 5 i : Int) =
      if i = 0 ∨ i = 5 then -5 else if i = 1 ∨ i = 4 then 5 else 0 := by
  intro i hi
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;> decide

theorem actual_first_values :
    Lychrel196.step 99505 = 150104 ∧ Lychrel196.step 99010 = 100109 := by
  decide

theorem actual_second_values :
    Lychrel196.step (Lychrel196.step 99505) = 551155 ∧
    Lychrel196.step (Lychrel196.step 99010) = 1001110 := by
  decide

/-- The general theorem applies to two concrete positive decimal seeds. -/
theorem actual_second_values_differ :
    Lychrel196.step (Lychrel196.step 99505) ≠
      Lychrel196.step (Lychrel196.step 99010) :=
  numeric_overflow_noncancellation 99505 99010 leftDigits rightDigits leftWord rightWord
    5 left_canonical right_canonical (fun _ _ => rfl) (fun _ _ => rfl)
    terminal_carries.1 terminal_carries.2 antisymmetric nonzero_old_digit

end P196.Agent8.CommonOverflowDefect.Witness
