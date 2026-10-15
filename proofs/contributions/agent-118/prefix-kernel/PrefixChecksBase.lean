import PrefixAncestry
import RowBoolean

/-!
# Chunked finite-check interfaces for prefix instances (Agent #118)

Concrete instances discharge the three premises of
`Agent118.PrefixKernel.ancestry_bound_of_finite_checks` by many small kernel
reductions. This module only proves that the chunks recombine into those
premises. It contains no certificate data.
-/

namespace Agent118.PrefixKernel

open SevenColumn.Certificate SevenColumn.ShortBoundary

/-- All short source widths two through six with one fixed outer pair sum. -/
def ShortDescentAt (tree : RankTree) (a : Nat) : Prop :=
  shortDescentOK tree [a+1, a+1] = true ∧
  (∀ c : Fin 10, shortDescentOK tree [a+1, 2*c.val, a+1] = true) ∧
  (∀ b : Fin 19, shortDescentOK tree [a+1, b.val, b.val, a+1] = true) ∧
  (∀ b : Fin 19, ∀ c : Fin 10,
    shortDescentOK tree [a+1, b.val, 2*c.val, b.val, a+1] = true) ∧
  (∀ b : Fin 19, ∀ c : Fin 19,
    shortDescentOK tree [a+1, b.val, c.val, c.val, b.val, a+1] = true)

instance (tree : RankTree) (a : Nat) : Decidable (ShortDescentAt tree a) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

/-- The chunked short checks cover every exact short word of widths 1..6. -/
theorem shortDescent_of_cases (tree : RankTree)
    (one : ∀ a : Fin 9, shortDescentOK tree [2*(a.val+1)] = true)
    (rest : ∀ a, a < 18 → ShortDescentAt tree a) :
    ShortDescent tree := by
  intro s hs
  simp only [shortWords, List.mem_append, or_assoc] at hs
  rcases hs with hs | hs | hs | hs | hs | hs
  · simp only [rawWords, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, rfl⟩
    exact one ⟨a, ha⟩
  · simp only [rawWords, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, rfl⟩
    exact (rest a ha).1
  · simp only [rawWords, List.mem_flatMap, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, c, hc, rfl⟩
    exact (rest a ha).2.1 ⟨c, hc⟩
  · simp only [rawWords, List.mem_flatMap, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, b, hb, rfl⟩
    exact (rest a ha).2.2.1 ⟨b, hb⟩
  · simp only [rawWords, List.mem_flatMap, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, b, hb, c, hc, rfl⟩
    exact (rest a ha).2.2.2.1 ⟨b, hb⟩ ⟨c, hc⟩
  · simp only [rawWords, List.mem_flatMap, List.mem_map, List.mem_range] at hs
    rcases hs with ⟨a, ha, b, hb, c, hc, rfl⟩
    exact (rest a ha).2.2.2.2 ⟨b, hb⟩ ⟨c, hc⟩

/-- Short targets and the 10,000 indexed long targets cover the initial family. -/
theorem initialCovered_of_checks (a b c bound : Nat) (tree : RankTree)
    (hshort : ∀ p ∈ shortTargets a b c, checkInitial tree bound p = true)
    (hlong : ∀ i, i < 10000 → checkInitial tree bound (targetInitialWord a b c i) = true) :
    ∀ p ∈ targetInitialWords a b c, checkInitial tree bound p = true := by
  intro p hp
  simp only [targetInitialWords, List.mem_append, List.mem_map, List.mem_range] at hp
  rcases hp with hp | ⟨i, hi, rfl⟩
  · exact hshort p hp
  · exact hlong i hi

/-- A stored subtree checked by one boolean traversal satisfies the row predicate. -/
theorem leaf_rows_of_block {tree leaf : RankTree} {pred : Word → List Word}
    (h : checkRowsBlock tree pred leaf = true) :
    leaf.All (fun p r => checkRow tree pred p r = true) :=
  checkRowsBlock_sound h

#print axioms shortDescent_of_cases
#print axioms initialCovered_of_checks
#print axioms leaf_rows_of_block

end Agent118.PrefixKernel
