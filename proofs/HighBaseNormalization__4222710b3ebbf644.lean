import ReverseAdd

namespace Agent11HighBase
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd

/-- False flags give one continuous ordinary carry chain. -/
def tags (q : List Int) : List (Int × Bool) := q.map (fun a => (a, false))
def normalize (b : Int) (q : List Int) : List Int := actualDigits b (tags q)
def nextPairs (b : Int) (q : List Int) : List Int := pairs (normalize b q)
def shifted (b : Int) (q : List Int) : List Int := q.map (fun a => a-b+1)
def adjacent (q : List Int) : List Int := List.zipWith (· + ·) q.dropLast q.tail

@[simp] theorem tags_projection (q : List Int) : (tags q).map Prod.fst = q := by
  simp [tags, List.map_map, Function.comp_def]
@[simp] theorem tags_ordinary (q : List Int) : ordinaryTags (tags q) = tags q := by
  simp [tags, ordinaryTags, List.map_map, Function.comp_def]

theorem tags_bound (b : Int) (q : List Int)
    (h : ∀ a ∈ q, 0 ≤ a ∧ a ≤ 2*b-2) : Bounded b (tags q) := by
  intro p hp
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hp
  exact h a ha

theorem high_divmod (b a : Int) (hb : 2 ≤ b) (ha : b ≤ a ∧ a < 2*b) :
    a/b=1 ∧ a%b=a-b := by
  have hlt : a/b < 2 := Int.ediv_lt_of_lt_mul (by omega) (by omega)
  have hn : ¬ a/b ≤ 0 := by
    rw [Int.ediv_le_iff_le_mul (show 0 < b by omega)]
    simp only [Int.zero_mul, Int.zero_add]
    omega
  have he : a/b=1 := by omega
  have hv := Int.emod_add_ediv a b
  rw [he, Int.mul_one] at hv
  exact ⟨he, by omega⟩

theorem high_tail_terminal (b : Int) (q : List Int) (hb : 2 ≤ b)
    (hq : ∀ a ∈ q, b-1 ≤ a ∧ a ≤ 2*b-2) :
    terminal b 1 (tags q) = 1 := by
  induction q with
  | nil => rfl
  | cons a q ih =>
      have ha := hq a (by simp)
      have ht : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2 := by
        intro x hx; exact hq x (by simp [hx])
      have hd := (high_divmod b (a+1) hb (by omega)).1
      simpa only [tags, List.map_cons, terminal, Bool.false_eq_true,
        ↓reduceIte, hd] using ih ht

theorem high_tail_body (b : Int) (q : List Int) (hb : 2 ≤ b)
    (hq : ∀ a ∈ q, b-1 ≤ a ∧ a ≤ 2*b-2) :
    body b 1 (tags q) = shifted b q := by
  induction q with
  | nil => rfl
  | cons a q ih =>
      have ha := hq a (by simp)
      have ht : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2 := by
        intro x hx; exact hq x (by simp [hx])
      obtain ⟨hd, hm⟩ := high_divmod b (a+1) hb (by omega)
      have hm' : (a+1)%b=a-b+1 := by omega
      simp only [tags, List.map_cons, body, Bool.false_eq_true, ↓reduceIte,
        Int.add_zero, hd, hm', shifted]
      exact congrArg (List.cons (a-b+1)) (ih ht)

theorem high_first_digits (b a : Int) (q : List Int) (hb : 2 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2) :
    normalize b (a::q) = (a-b)::shifted b q ++ [1] := by
  obtain ⟨hd,hm⟩ := high_divmod b a hb (by omega)
  have ht : terminal b 0 (tags (a::q)) = 1 := by
    simp only [tags, List.map_cons, terminal, Bool.false_eq_true, ↓reduceIte,
      Int.add_zero, hd]
    exact high_tail_terminal b q hb hq
  simp only [normalize, actualDigits, atActualWidth, tags_ordinary, ht,
    Int.reduceEq, ↓reduceIte, placed_body_terminal]
  simp only [tags, List.map_cons, body, Bool.false_eq_true, ↓reduceIte,
    Int.add_zero, hd, hm]
  rw [show body b 1 (q.map (fun a => (a,false))) = shifted b q from
    high_tail_body b q hb hq]

/-- The displayed first output uses the true overflow width, including L=1. -/
theorem high_first_width (b a : Int) (q : List Int) (hb : 2 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2) :
    (normalize b (a::q)).length = (a::q).length + 1 := by
  rw [high_first_digits b a q hb ha hq]
  simp [shifted]

end Agent11HighBase
