import ActualHistories

/-!
Agent #3: exact finite enumeration for the two-history extension.
The arithmetic transitions and canonicality are imported from
ActualHistories. Counting reuses the previously checked allBits
enumeration and inputWord injectivity from OverflowHorizon.
-/

namespace P196.Agent3.TwoHistory

open Agent8
open P196.Agent3.OverflowHorizon

/-- A fixed-length correction never obscures the original free word. -/
theorem completedBits_injective (xs ys : List Bool)
    (h : completedBits xs = completedBits ys) : xs = ys := by
  unfold completedBits at h
  have hlen := congrArg List.length h
  simp only [List.length_append, correction_length] at hlen
  exact (List.append_inj h (by omega)).1

theorem historyWord2_injective (k : Nat) (xs ys : List Bool)
    (h : historyWord2 xs k = historyWord2 ys k) : xs = ys := by
  apply completedBits_injective xs ys
  exact inputWord_injective k (completedBits xs) (completedBits ys) h

/-- Equal initial histories have equal two-step images; distinctness of
the protected image family therefore forces distinct initial histories. -/
theorem historyWord0_injective (k : Nat) (xs ys : List Bool)
    (h : historyWord0 xs k = historyWord0 ys k) : xs = ys := by
  apply historyWord2_injective k xs ys
  have ht := congrArg (fun w => stepWord (stepWord w)) h
  simpa only [historyWord0_step, historyWord1_step] using ht

/-- Initial coefficient words of the enumerated two-history family. -/
def historyFamily0 (m k : Nat) : List Word :=
  (allBits m).map (fun xs => historyWord0 xs k)

/-- Protected coefficient words reached after the two incoming steps. -/
def historyFamily2 (m k : Nat) : List Word :=
  (allBits m).map (fun xs => historyWord2 xs k)

theorem historyFamily0_length (m k : Nat) :
    (historyFamily0 m k).length = 2 ^ m := by
  simp [historyFamily0, allBits_length]

theorem historyFamily2_length (m k : Nat) :
    (historyFamily2 m k).length = 2 ^ m := by
  simp [historyFamily2, allBits_length]

theorem historyFamily0_nodup (m k : Nat) :
    (historyFamily0 m k).Nodup := by
  exact List.Pairwise.map (fun xs => historyWord0 xs k)
    (fun xs ys hne heq => hne (historyWord0_injective k xs ys heq))
    (allBits_nodup m)

theorem historyFamily2_nodup (m k : Nat) :
    (historyFamily2 m k).Nodup := by
  exact List.Pairwise.map (fun xs => historyWord2 xs k)
    (fun xs ys hne heq => hne (historyWord2_injective k xs ys heq))
    (allBits_nodup m)

theorem mem_historyFamily0_iff (w : Word) (m k : Nat) :
    w ∈ historyFamily0 m k ↔
      ∃ xs : List Bool, xs.length = m ∧ historyWord0 xs k = w := by
  simp [historyFamily0, List.mem_map, mem_allBits_iff]

theorem mem_historyFamily2_iff (w : Word) (m k : Nat) :
    w ∈ historyFamily2 m k ↔
      ∃ xs : List Bool, xs.length = m ∧ historyWord2 xs k = w := by
  simp [historyFamily2, List.mem_map, mem_allBits_iff]

theorem historyFamily0_member_properties (m k : Nat) (w : Word)
    (hw : w ∈ historyFamily0 m k) :
    CanonicalPair w ∧ w.length = 2 * (m + k + 7) ∧ w.length % 2 = 0 := by
  rcases (mem_historyFamily0_iff w m k).mp hw with ⟨xs, hlen, rfl⟩
  exact ⟨historyWord0_canonical xs k,
    by rw [historyWord0_length, hlen], historyWord0_even xs k⟩

theorem historyFamily2_member_properties (m k : Nat) (w : Word)
    (hw : w ∈ historyFamily2 m k) :
    CanonicalPair w ∧ w.length = 2 * (m + k + 7) ∧ w.length % 2 = 0 := by
  rcases (mem_historyFamily2_iff w m k).mp hw with ⟨xs, hlen, rfl⟩
  exact ⟨historyWord2_canonical xs k,
    by rw [historyWord2_length, hlen], historyWord2_even xs k⟩

/-- Exact size and admissibility of the distinct initial histories. -/
theorem historyFamily0_exact (m k : Nat) :
    (historyFamily0 m k).length = 2 ^ m ∧
    (historyFamily0 m k).Nodup ∧
    ∀ w ∈ historyFamily0 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 7) ∧ w.length % 2 = 0 := by
  exact ⟨historyFamily0_length m k, historyFamily0_nodup m k,
    historyFamily0_member_properties m k⟩

/-- Exact size and admissibility of the distinct protected words. -/
theorem historyFamily2_exact (m k : Nat) :
    (historyFamily2 m k).length = 2 ^ m ∧
    (historyFamily2 m k).Nodup ∧
    ∀ w ∈ historyFamily2 m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 7) ∧ w.length % 2 = 0 := by
  exact ⟨historyFamily2_length m k, historyFamily2_nodup m k,
    historyFamily2_member_properties m k⟩

/-- Applying the actual two-step map to the complete initial enumeration
gives the protected enumeration in the same order. -/
theorem historyFamilies_two_step (m k : Nat) :
    (historyFamily0 m k).map (fun w => stepWord (stepWord w)) =
      historyFamily2 m k := by
  simp only [historyFamily0, historyFamily2, List.map_map, Function.comp_def,
    historyWord0_step, historyWord1_step]

#print axioms completedBits_injective
#print axioms historyWord2_injective
#print axioms historyWord0_injective
#print axioms historyFamily0
#print axioms historyFamily2
#print axioms historyFamily0_length
#print axioms historyFamily2_length
#print axioms historyFamily0_nodup
#print axioms historyFamily2_nodup
#print axioms mem_historyFamily0_iff
#print axioms mem_historyFamily2_iff
#print axioms historyFamily0_member_properties
#print axioms historyFamily2_member_properties
#print axioms historyFamily0_exact
#print axioms historyFamily2_exact
#print axioms historyFamilies_two_step

end P196.Agent3.TwoHistory
