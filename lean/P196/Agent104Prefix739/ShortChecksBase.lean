import P196.Agent104P620Witness.ShortBoundary
import P196.Agent104P620Witness.PrefixCertificate

namespace SevenColumn.Certificate739
open Certificate ShortBoundary

/-- All widths two through six, with one fixed positive outside pair sum. -/
def ShortAt (tree : RankTree) (a : Nat) : Prop :=
  lookup tree (nextWord [a+1,a+1]) = none ∧
  (∀ c : Fin 10, lookup tree (nextWord [a+1,2*c.val,a+1]) = none) ∧
  (∀ b : Fin 19, lookup tree (nextWord [a+1,b.val,b.val,a+1]) = none) ∧
  (∀ b : Fin 19, ∀ c : Fin 10,
    lookup tree (nextWord [a+1,b.val,2*c.val,b.val,a+1]) = none) ∧
  (∀ b : Fin 19, ∀ c : Fin 19,
    lookup tree (nextWord [a+1,b.val,c.val,c.val,b.val,a+1]) = none)

instance (tree : RankTree) (a : Nat) : Decidable (ShortAt tree a) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

theorem shortChecked_of_cases (tree : RankTree)
    (one : ∀ a : Fin 9, lookup tree (nextWord [2*(a.val+1)]) = none)
    (rest : ∀ a, a < 18 → ShortAt tree a) :
    ∀ s ∈ shortWords, lookup tree (nextWord s) = none := by
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

#print axioms shortChecked_of_cases
end SevenColumn.Certificate739
