import Agent1PeriodicCycleNumeric

namespace Agent1.Periodic
open Agent8

/-- A positive nine band makes every original canonical realization
nonpalindromic at the represented input, including time zero. -/
theorem periodic_nines_input_nonpalindrome (B H : Word) (k n : Nat)
    (d : Nat → Nat) (hk : 0 < k)
    (hc : DecimalDigits.Canonical n d (periodicWord B H [9,9,9,9] k).length)
    (hrep : ∀ i, i < (periodicWord B H [9,9,9,9] k).length →
      DecimalDigits.columnSum d (periodicWord B H [9,9,9,9] k).length i =
        ((periodicWord B H [9,9,9,9] k)[i]?).getD 0) :
    ¬ Lychrel196.Palindrome n := by
  have hm : 9 ∈ periodicWord B H [9,9,9,9] k :=
    (mem_periodicWord_iff B H [9,9,9,9] k 9 hk).mpr (by simp)
  obtain ⟨i, hi, he⟩ := List.getElem_of_mem hm
  have hcol := hrep i hi
  rw [List.getElem?_eq_getElem hi, Option.getD_some, he] at hcol
  intro hp
  rw [← hc.2.2.2] at hp
  have hs := (DecimalDigits.palindrome_value_iff d _ hc.2.1
    (Or.inr hc.2.2.1)).mp hp i hi
  simp only [DecimalDigits.columnSum, DecimalDigits.reflected] at hcol
  omega

end Agent1.Periodic
#print axioms Agent1.Periodic.periodic_nines_input_nonpalindrome
