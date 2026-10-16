import BulkTargets
import Agent414CyclicWordPeriod

/-! Agent #414. Discharge the six-divisibility premise from the exact original
bulk-word semantics. Legacy proofs in imported modules are not used below;
all exported dependency audits are retained. -/
namespace Agent414BulkPeriod
open Sofic BoundaryCertificate Agent414CyclicWordPeriod

/-- All and only multiples of six are periods of either original bulk word,
for every original phase. This includes the zero period on both sides. -/
theorem bulk_periodic_iff_dvd (n : Nat) (family : Fin 2) (phase : Fin 6) :
    Periodic n (bulkWord family phase) ↔ 6 ∣ n := by
  have hinj : ∀ a b : Fin 6,
      (bulkLetters family)[a.val]! = (bulkLetters family)[b.val]! → a = b := by
    simpa only [bulkLetters] using bulk_letter_injective_checked family
  simpa only [cyclicWord, bulkWord] using
    periodic_iff_dvd (n := n) (by decide : 0 < 6)
      (fun i : Fin 6 => (bulkLetters family)[i.val]!) phase hinj

/-- The divisibility premise follows from the path itself, not from an
extra assumption about the chosen clock. -/
theorem six_dvd_of_bulk_path {n : Nat} (family : Fin 2) (phase : Fin 6)
    (hp : ReverseClosure.Path (ArithmeticColumn n) (fun _ => 41) (bulkWord family phase)) :
    6 ∣ n := by
  apply (bulk_periodic_iff_dvd n family phase).mp
  exact periodic_of_path (fun _ => rfl) (fun _ _ h => h.2.1) hp

/-- Non-multiple-of-six clocks are excluded by exact periodicity alone,
without importing the large finite-exterior certificate as a proof dependency. -/
theorem no_bulk_exterior_of_not_dvd {n : Nat} (hn : ¬ 6 ∣ n)
    (family : Fin 2) (phase : Fin 6) :
    ¬ ReverseClosure.Path (ArithmeticColumn n) (fun _ => 41) (bulkWord family phase) := by
  intro hp
  exact hn (six_dvd_of_bulk_path family phase hp)

/-- Boundary-case audit: the original zero-clock arithmetic column has no
nonempty range of digit constraints, and therefore relates any two words. -/
theorem zero_clock_column (u v : Word) : ArithmeticColumn 0 u v := by
  refine ⟨?_, ?_, (fun _ => ⟨0, 0, 0, 0, 0, 0⟩), ?_, ?_⟩
  · intro i; rfl
  · intro i; rfl
  · intro i; rfl
  · intro i hi; omega

/-- Positivity cannot be silently deleted from an all-clock exclusion. -/
theorem zero_clock_path (u v : Word) : ReverseClosure.Path (ArithmeticColumn 0) u v :=
  .snoc (.refl u) (zero_clock_column u v)

#print axioms bulk_periodic_iff_dvd
#print axioms six_dvd_of_bulk_path
#print axioms no_bulk_exterior_of_not_dvd
#print axioms zero_clock_column
#print axioms zero_clock_path
end Agent414BulkPeriod
