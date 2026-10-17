import P196.Agent117P2641.Agent124CodeCert

/-!
# Splitting short-descent checks by the leading half entry (Agent #124)

`symWords n` is generated from all half words in `lists19 ((n+1)/2)`.
Grouping those halves by their first entry divides the Boolean short-descent
check of one width into nineteen kernel-reduced checks, which keeps the
kernel's per-declaration memory bounded for the longer short widths.
-/

namespace Agent124.ShortSplit

open Agent124.PrefixK Agent124.CodeCert

/-- The words of `symWords n` whose half begins with `a`. -/
def symChunk (n a : Nat) : List (List Nat) :=
  (((lists19 ((n + 1) / 2 - 1)).map (a :: ·)).map (mirror n)).filter (symOK n)

theorem all_symWords_of_chunks {n : Nat} (hn : 1 ≤ (n + 1) / 2) {f : List Nat → Bool}
    (h : ∀ a, a < 19 → (symChunk n a).all f = true) : (symWords n).all f = true := by
  apply List.all_eq_true.mpr
  intro w hw
  unfold symWords at hw
  rw [List.mem_filter, List.mem_map] at hw
  obtain ⟨⟨half, hhalf, rfl⟩, hok⟩ := hw
  have hm : (n + 1) / 2 = ((n + 1) / 2 - 1) + 1 := by omega
  rw [hm] at hhalf
  simp only [lists19, List.mem_flatMap, List.mem_range, List.mem_map] at hhalf
  obtain ⟨a, ha, t, ht, rfl⟩ := hhalf
  apply List.all_eq_true.mp (h a ha)
  unfold symChunk
  rw [List.mem_filter, List.mem_map]
  refine ⟨⟨a :: t, ?_, rfl⟩, hok⟩
  rw [List.mem_map]
  exact ⟨t, ht, rfl⟩

end Agent124.ShortSplit

#print axioms Agent124.ShortSplit.all_symWords_of_chunks
