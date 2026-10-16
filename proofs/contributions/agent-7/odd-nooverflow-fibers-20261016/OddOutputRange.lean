import OddActual

/-!
The actual no-overflow output of every odd-length coefficient word admits the
finite target encoding used by the odd inverse-fiber enumerator.  No symmetry
or center-parity premise on the input is needed for this output-range bridge.
The original Agent8 normalizer and stepWord are imported unchanged.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

/-- Every digit emitted by the original scan is a decimal remainder. -/
theorem scan_digits_lt_ten (q : List Nat) (e : Nat) :
    ∀ d ∈ (scan q e).1, d < 10 := by
  induction q generalizing e with
  | nil => simp [scan]
  | cons x xs ih =>
    intro d hd
    change d ∈ (x + e) % 10 :: (scan xs ((x + e) / 10)).1 at hd
    rcases List.mem_cons.mp hd with rfl | hd
    · exact Nat.mod_lt _ (by decide)
    · exact ih _ _ hd

/-- Split an arbitrary odd list into equal outside halves and one center. -/
theorem odd_list_halves {α : Type} (q : List α) (m : Nat)
    (hlen : q.length = 2 * m + 1) :
    ∃ ds es : List α, ∃ v : α,
      ds.length = m ∧ es.length = m ∧ q = ds ++ [v] ++ es.reverse := by
  have hm : m < q.length := by omega
  refine ⟨q.take m, (q.drop (m + 1)).reverse, q[m], ?_, ?_, ?_⟩
  · simp only [List.length_take]
    exact Nat.min_eq_left (by omega)
  · simp only [List.length_reverse, List.length_drop]
    omega
  · simp only [List.reverse_reverse]
    calc
      q = q.take (m + 1) ++ q.drop (m + 1) :=
        (List.take_append_drop _ _).symm
      _ = (q.take m ++ [q[m]]) ++ q.drop (m + 1) := by
        rw [List.take_succ_eq_append_getElem hm]

/-- Opposite decimal digits sum to a coefficient in the original Fin 19 alphabet. -/
theorem zipAdd_digits_lt_nineteen (xs ys : List Nat)
    (hx : ∀ x ∈ xs, x < 10) (hy : ∀ y ∈ ys, y < 10) :
    ∀ s ∈ zipAdd xs ys, s < 19 := by
  induction xs generalizing ys with
  | nil => simp [zipAdd]
  | cons x xs ih =>
    cases ys with
    | nil => simp [zipAdd]
    | cons y ys =>
      intro s hs
      change s ∈ (x + y) :: zipAdd xs ys at hs
      rcases List.mem_cons.mp hs with rfl | hs
      · have hxb := hx x (by simp)
        have hyb := hy y (by simp)
        omega
      · exact ih ys (fun a ha => hx a (by simp [ha]))
          (fun b hb => hy b (by simp [hb])) s hs

/-- Every bounded coefficient list is the value list of a finite-symbol list. -/
theorem exists_symbol_list (xs : List Nat) (hb : ∀ x ∈ xs, x < 19) :
    ∃ ss : List Symbol, ss.map Fin.val = xs := by
  induction xs with
  | nil => exact ⟨[], rfl⟩
  | cons x xs ih =>
    have hx : x < 19 := hb x (by simp)
    obtain ⟨ss, hs⟩ := ih (fun y hy => hb y (by simp [hy]))
    exact ⟨⟨x, hx⟩ :: ss, by simp [hs]⟩

/-- Every actual odd-width output without overflow has the encoded target shape.
The conclusion needs no coefficient bound, symmetry, or parity assumption on q. -/
theorem odd_nooverflow_output_range (q : List Nat) (m : Nat)
    (hlen : q.length = 2 * m + 1) (hc : (scan q 0).2 = 0) :
    ∃ ss : List Symbol, ∃ v : Fin 10,
      ss.length = m ∧
        Agent8.stepWord q = oddMirror (ss.map Fin.val) (2 * v.val) := by
  have hdlen : (scan q 0).1.length = 2 * m + 1 :=
    (scan_length q 0).trans hlen
  obtain ⟨ds, es, c, hd, he, hsplit⟩ := odd_list_halves (scan q 0).1 m hdlen
  have hdigits := scan_digits_lt_ten q 0
  have hds : ∀ d ∈ ds, d < 10 := by
    intro d hmem
    apply hdigits d
    rw [hsplit]
    simp [hmem]
  have hes : ∀ e ∈ es, e < 10 := by
    intro e hmem
    apply hdigits e
    rw [hsplit]
    simp [hmem]
  have hcenter : c < 10 := by
    apply hdigits c
    rw [hsplit]
    simp
  obtain ⟨ss, hs⟩ := exists_symbol_list (zipAdd ds es)
    (zipAdd_digits_lt_nineteen ds es hds hes)
  refine ⟨ss, ⟨c, hcenter⟩, ?_, ?_⟩
  · have hh := congrArg List.length hs
    simp only [List.length_map] at hh
    exact hh.trans ((zipAdd_length ds es (hd.trans he.symm)).trans hd)
  · unfold Agent8.stepWord
    rw [normalize_scan, hc]
    simp only [↓reduceIte, List.append_nil]
    rw [hsplit, pair_odd_halves ds es c (hd.trans he.symm), hs]

/-- The bounded coefficient-word form of the actual output-range theorem. -/
theorem odd_output_range (q : List Nat) (m : Nat)
    (hlen : q.length = 2 * m + 1) (_hb : ∀ x ∈ q, x < 19)
    (hc : (scan q 0).2 = 0) :
    ∃ ss : List Symbol, ∃ v : Fin 10,
      ss.length = m ∧
        Agent8.stepWord q = oddMirror (ss.map Fin.val) (2 * v.val) :=
  odd_nooverflow_output_range q m hlen hc

#print axioms scan_digits_lt_ten
#print axioms odd_list_halves
#print axioms zipAdd_digits_lt_nineteen
#print axioms exists_symbol_list
#print axioms odd_nooverflow_output_range
#print axioms odd_output_range

end P196.Agent7.OddFibers
