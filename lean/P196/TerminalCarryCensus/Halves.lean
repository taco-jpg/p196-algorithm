import P196.SymmetricCarryCensus.Enumeration

/-!
Finite half words for the terminal-carry census. Every independent pair
coefficient has nineteen choices; an odd center has ten even choices.
Outer zero coefficients are retained, and width zero has one empty half.
The construction uses the existing finite word and append products.
-/

set_option autoImplicit false

namespace TerminalCarryCensus

open P196.Agent9.Ensemble SymmetricCarryCensus

/-- Independent bounded coefficients, followed by an even center at odd width. -/
def halves (L : Nat) : List (List Nat) :=
  if L % 2 = 0 then wordChoices (List.range 19) (L / 2)
  else appendProduct (wordChoices (List.range 19) (L / 2))
    ((List.range 10).map (fun c => [2 * c]))

private theorem mem_odd_halves (m : Nat) (h : List Nat) :
    h ∈ appendProduct (wordChoices (List.range 19) m)
      ((List.range 10).map (fun c => [2 * c])) ↔
      h.length = m + 1 ∧ (∀ x ∈ h, x < 19) ∧ h.getD m 0 % 2 = 0 := by
  constructor
  · intro hh
    obtain ⟨xs, hxs, ys, hys, rfl⟩ := (mem_appendProduct _ _ h).mp hh
    obtain ⟨c, hc, rfl⟩ := List.mem_map.mp hys
    obtain ⟨hlen, hb⟩ := (mem_wordChoices _ _ xs).mp hxs
    have hcBound := List.mem_range.mp hc
    refine ⟨by simp [hlen], ?_, ?_⟩
    · intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · exact List.mem_range.mp (hb x hx)
      · have hx' := List.mem_singleton.mp hx
        omega
    · have hlast : (xs ++ [2 * c]).getD m 0 = 2 * c := by
        rw [← hlen]
        simp [List.getElem?_append]
      rw [hlast]
      omega
  · rintro ⟨hlen, hb, hc⟩
    have hi : m < h.length := by omega
    have hget : h.getD m 0 = h[m]'hi := by
      simp only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi,
        Option.getD_some]
    have hbound := hb (h[m]'hi) (List.getElem_mem hi)
    have heven : (h[m]'hi) % 2 = 0 := by simpa only [hget] using hc
    apply (mem_appendProduct _ _ h).mpr
    refine ⟨h.take m, ?_, [h[m]'hi], ?_, ?_⟩
    · apply (mem_wordChoices _ _ _).mpr
      refine ⟨?_, ?_⟩
      · simp only [List.length_take, Nat.min_eq_left (Nat.le_of_lt hi)]
      · intro x hx
        exact List.mem_range.mpr (hb x (List.mem_of_mem_take hx))
    · apply List.mem_map.mpr
      refine ⟨(h[m]'hi) / 2, List.mem_range.mpr (by omega), ?_⟩
      have hdouble : 2 * ((h[m]'hi) / 2) = h[m]'hi := by omega
      simp only [hdouble]
    · calc
        h.take m ++ [h[m]'hi] = h.take (m + 1) := List.take_append_getElem hi
        _ = h := by rw [← hlen, List.take_length]

/-- Exact half length, coefficient bounds, and optional even center. -/
theorem mem_halves_iff (L : Nat) (h : List Nat) :
    h ∈ halves L ↔ h.length = (L + 1) / 2 ∧
      (∀ x ∈ h, x < 19) ∧
      (L % 2 = 0 ∨ h.getD (L / 2) 0 % 2 = 0) := by
  by_cases he : L % 2 = 0
  · have hhalf : (L + 1) / 2 = L / 2 := by omega
    rw [halves, if_pos he, mem_wordChoices]
    simp only [List.mem_range, he, true_or, and_true, hhalf]
  · have hhalf : (L + 1) / 2 = L / 2 + 1 := by omega
    rw [halves, if_neg he, mem_odd_halves]
    simp only [he, false_or, hhalf]

/-- Each half word occurs once, including the empty half at width zero. -/
theorem halves_nodup (L : Nat) : (halves L).Nodup := by
  by_cases he : L % 2 = 0
  · rw [halves, if_pos he]
    exact wordChoices_nodup _ List.nodup_range _
  · rw [halves, if_neg he]
    apply appendProduct_nodup _ _ (L / 2)
    · exact wordChoices_nodup _ List.nodup_range _
    · apply nodup_map_of_injOn _ _ List.nodup_range
      intro a _ b _ hab
      have hdouble : 2 * a = 2 * b := (List.cons.inj hab).1
      omega
    · intro xs hx
      exact ((mem_wordChoices _ _ xs).mp hx).1

/-- The existing product counts give the exact size at every width. -/
theorem halves_length (L : Nat) :
    (halves L).length =
      if L % 2 = 0 then 19 ^ (L / 2) else 10 * 19 ^ (L / 2) := by
  by_cases he : L % 2 = 0
  · simp only [halves, he, if_true, length_wordChoices, List.length_range]
  · simp only [halves, he, if_false, length_appendProduct, length_wordChoices,
      List.length_map, List.length_range]
    exact Nat.mul_comm _ _

#print axioms mem_halves_iff
#print axioms halves_nodup
#print axioms halves_length

end TerminalCarryCensus
