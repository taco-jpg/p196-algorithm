import P196.Agent117P2641.Agent124CodeCert

/-!
# Structural coverage for bounded kernel-check slices

These lemmas use the unchanged Agent124 enumerations. They prove complete
coverage through list membership and the outer two digit choices, so no
whole ten-thousand-word equality or native evaluation is needed.
-/

namespace Agent104.Prefix620

open Agent124.PrefixK

def initialShortWords : List (List Nat) :=
  ((List.range 4).flatMap fun j =>
    (digitLists j).map ([6, 2, 0] ++ ·)).filter (initialOK 7)

def initialSlice (a b : Nat) : List (List Nat) :=
  (digitLists 2).map ([6, 2, 0, a, b] ++ ·)

/-- The original complete initial enumeration is covered by its short
part and every choice of the first two free decimal digits. -/
theorem initial_all_of_slices (p : List Nat → Bool)
    (hshort : initialShortWords.all p = true)
    (hslices : ∀ a, a < 10 → ∀ b, b < 10 → (initialSlice a b).all p = true) :
    (initialWordsK 7 6 2 0).all p = true := by
  apply List.all_eq_true.mpr
  intro w hw
  have hh := List.mem_filter.mp hw
  obtain ⟨j, hj, u, hu, he⟩ :=
    (by simpa only [initialWordsK, List.mem_flatMap, List.mem_range, List.mem_map]
      using hh.1 : ∃ j, j < 7 - 2 ∧ ∃ u, u ∈ digitLists j ∧ [6, 2, 0] ++ u = w)
  subst w
  by_cases hshortj : j < 4
  · apply List.all_eq_true.mp hshort
    apply List.mem_filter.mpr
    refine ⟨?_, hh.2⟩
    exact List.mem_flatMap.mpr ⟨j, List.mem_range.mpr hshortj,
      List.mem_map.mpr ⟨u, hu, rfl⟩⟩
  · have hj4 : j = 4 := by omega
    subst j
    change u ∈ (List.range 10).flatMap (fun a => (digitLists 3).map (a :: ·)) at hu
    simp only [List.mem_flatMap, List.mem_range, List.mem_map] at hu
    obtain ⟨a, ha, v, hv, he⟩ := hu
    subst u
    change v ∈ (List.range 10).flatMap (fun b => (digitLists 2).map (b :: ·)) at hv
    simp only [List.mem_flatMap, List.mem_range, List.mem_map] at hv
    obtain ⟨b, hb, z, hz, he⟩ := hv
    subst v
    apply List.all_eq_true.mp (hslices a ha b hb)
    exact List.mem_map.mpr ⟨z, hz, rfl⟩

def shortSlice (n m a : Nat) : List (List Nat) :=
  ((lists19 m).map (fun tail => mirror n (a :: tail))).filter (symOK n)

/-- Splitting the half-word's first coefficient covers every admissible
short word, retaining the original positivity and center filter. -/
theorem short_all_of_slices (p : List Nat → Bool) (n m : Nat)
    (hm : (n + 1) / 2 = m + 1)
    (hslices : ∀ a, a < 19 → (shortSlice n m a).all p = true) :
    (symWords n).all p = true := by
  apply List.all_eq_true.mpr
  intro w hw
  obtain ⟨hmap, hfilter⟩ := List.mem_filter.mp hw
  obtain ⟨h, hh, he⟩ := List.mem_map.mp hmap
  subst w
  rw [hm] at hh
  change h ∈ (List.range 19).flatMap (fun a => (lists19 m).map (a :: ·)) at hh
  simp only [List.mem_flatMap, List.mem_range, List.mem_map] at hh
  obtain ⟨a, ha, tail, ht, he⟩ := hh
  subst h
  apply List.all_eq_true.mp (hslices a ha)
  exact List.mem_filter.mpr ⟨List.mem_map.mpr ⟨tail, ht, rfl⟩, hfilter⟩

#print axioms initial_all_of_slices
#print axioms short_all_of_slices

end Agent104.Prefix620
