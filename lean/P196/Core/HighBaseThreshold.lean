import P196.Core.HighBasePairs

namespace Agent11HighBase
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd

theorem low_terminal (b : Int) (q : List Int) (hq : DigitBounds b q) :
    terminal b 0 (tags q) = 0 := by
  induction q with
  | nil => rfl
  | cons a q ih =>
      have ha := hq a (by simp)
      have ht : DigitBounds b q := by intro x hx; exact hq x (by simp [hx])
      have hd := Int.ediv_eq_zero_of_lt ha.1 ha.2
      simpa only [tags, List.map_cons, terminal, Bool.false_eq_true,
        ↓reduceIte, Int.add_zero, hd] using ih ht

theorem low_body (b : Int) (q : List Int) (hq : DigitBounds b q) :
    body b 0 (tags q) = q := by
  induction q with
  | nil => rfl
  | cons a q ih =>
      have ha := hq a (by simp)
      have ht : DigitBounds b q := by intro x hx; exact hq x (by simp [hx])
      have hd := Int.ediv_eq_zero_of_lt ha.1 ha.2
      have hm := Int.emod_eq_of_lt ha.1 ha.2
      simpa only [tags, List.map_cons, body, Bool.false_eq_true,
        ↓reduceIte, Int.add_zero, hd, hm] using congrArg (List.cons a) (ih ht)

theorem low_normalize (b : Int) (q : List Int) (hq : DigitBounds b q) :
    normalize b q = q := by
  simp only [normalize, actualDigits, atActualWidth, tags_ordinary,
    low_terminal b q hq, ↓reduceIte]
  exact low_body b q hq

/-- A positive outside coefficient below the base rules out the exceptional
palindrome-predecessor overflow class in every base at least three. -/
theorem low_outer_palindrome_iff (b a : Int) (q : List Int) (hb : 3 ≤ b)
    (ha : 0 < a ∧ a < b)
    (hq : ∀ x ∈ a::q, 0 ≤ x ∧ x ≤ 2*b-2)
    (hs : (a::q).reverse=a::q) :
    (normalize b (a::q)).reverse=normalize b (a::q) ↔
      (∀ x ∈ a::q, x ≤ b-1) := by
  have htbound := tags_bound b (a::q) hq
  have htsym : ((tags (a::q)).map Prod.fst).reverse=(tags (a::q)).map Prod.fst := by
    simpa only [tags_projection] using hs
  constructor
  · intro hp
    unfold normalize actualDigits atActualWidth at hp
    simp only [tags_ordinary] at hp
    split at hp
    · rename_i ht
      have hraw : placed b 0 (tags (a::q)) = body b 0 (tags (a::q)) ++ [0] := by
        rw [placed_body_terminal, ht]
      have hc := placed_nooverflow_classification b (tags (a::q))
        (body b 0 (tags (a::q))) hb htbound htsym hraw hp
      intro x hx
      have hmem : (x,false) ∈ tags (a::q) := List.mem_map.mpr ⟨x,hx,rfl⟩
      obtain ⟨p,hm,he⟩ := coefficient_mem_columns b 0 (tags (a::q)) (x,false) hmem
      have hh := (hc.2 p hm).2
      simpa only [he] using hh
    · have hc := placed_overflow_classification b (tags (a::q)) hb htbound htsym hp
      obtain ⟨p,hm,he⟩ := coefficient_mem_columns b 0 (tags (a::q))
        (a,false) (by simp [tags])
      have hh := (hc p hm).2
      simp only [he] at hh
      rcases hh with hh | hh <;> omega
  · intro hl
    have hd : DigitBounds b (a::q) := by
      intro x hx
      exact ⟨(hq x hx).1, by have := hl x hx; omega⟩
    rw [low_normalize b (a::q) hd]
    exact hs

theorem high_first_digit_bounds (b a : Int) (q : List Int) (hb : 2 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2) :
    DigitBounds b (normalize b (a::q)) := by
  rw [high_first_digits b a q hb ha hq]
  intro d hd
  simp only [List.mem_append, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hd
  rcases hd with (rfl | hm) | rfl
  · omega
  · obtain ⟨x,hx,rfl⟩ := List.mem_map.mp hm
    have := hq x hx
    omega
  · omega

/-- The source's all-base threshold (9), without any finite-width cutoff. -/
theorem second_palindrome_iff_adjacent (b a : Int) (q : List Int) (hb : 3 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2)
    (hs : (a::q).reverse=a::q) :
    (normalize b (nextPairs b (a::q))).reverse=normalize b (nextPairs b (a::q)) ↔
      (∀ s ∈ adjacent (a::q), s ≤ 3*b-3) := by
  have hf := next_pairs_formula b a q (by omega) ha hq hs
  have hbnd : ∀ x ∈ nextPairs b (a::q), 0 ≤ x ∧ x ≤ 2*b-2 :=
    pairs_bounds b (normalize b (a::q)) (high_first_digit_bounds b a q (by omega) ha hq)
  have hsym : (nextPairs b (a::q)).reverse=nextPairs b (a::q) := pairs_symmetric _
  rw [hf] at hbnd hsym ⊢
  simp only [List.cons_append] at hbnd hsym ⊢
  rw [low_outer_palindrome_iff b (a-b+1)
    (((adjacent (a::q)).map (fun s => s-2*b+2)) ++ [a-b+1]) hb (by omega)
    (by simpa only [List.cons_append] using hbnd)
    (by simpa only [List.cons_append] using hsym)]
  constructor
  · intro hl s hmem
    have hm : s-2*b+2 ∈ (a-b+1)::
        ((adjacent (a::q)).map (fun t => t-2*b+2)) ++ [a-b+1] := by
      simp only [List.mem_append, List.mem_cons, List.mem_singleton]
      exact Or.inl (Or.inr (List.mem_map.mpr ⟨s,hmem,rfl⟩))
    have := hl _ hm
    omega
  · intro hl x hx
    simp only [List.mem_cons, List.mem_append, List.mem_singleton, List.not_mem_nil, or_false] at hx
    rcases hx with rfl | hm | rfl
    · omega
    · obtain ⟨s,hsMem,rfl⟩ := List.mem_map.mp hm
      have := hl s hsMem
      omega
    · omega

end Agent11HighBase
