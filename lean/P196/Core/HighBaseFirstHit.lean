import P196.Core.HighBaseNumeric

namespace Agent11HighBase
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd

/-- Full high-region first-output classification, stronger than the smaller
interval needed by the original first-positive-time theorem. -/
theorem first_palindrome_iff_constant (b a : Int) (q : List Int) (hb : 3 ≤ b)
    (ha : b ≤ a ∧ a ≤ 2*b-2)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2)
    (hs : (a::q).reverse=a::q) :
    (normalize b (a::q)).reverse=normalize b (a::q) ↔
      ∀ x ∈ a::q, x=b+1 := by
  constructor
  · intro hp
    have ht : terminal b 0 (tags (a::q))=1 := by
      have hd := (high_divmod b a (by omega) (by omega)).1
      simp only [tags, List.map_cons, terminal, Bool.false_eq_true, ↓reduceIte,
        Int.add_zero, hd]
      exact high_tail_terminal b q (by omega) hq
    have hn : normalize b (a::q)=placed b 0 (tags (a::q)) := by
      simp only [normalize, actualDigits, atActualWidth, tags_ordinary, ht,
        Int.reduceEq, ↓reduceIte]
    have hbound : ∀ x ∈ a::q, 0 ≤ x ∧ x ≤ 2*b-2 := by
      intro x hx
      rcases List.mem_cons.mp hx with rfl | hx
      · omega
      · have := hq x hx; omega
    rw [hn] at hp
    have hc := placed_overflow_classification b (tags (a::q)) hb
      (tags_bound b _ hbound) (by simpa using hs) hp
    intro x hx
    obtain ⟨p,hm,he⟩ := coefficient_mem_columns b 0 (tags (a::q)) (x,false)
      (List.mem_map.mpr ⟨x,hx,rfl⟩)
    have hh := (hc p hm).2
    simp only [he] at hh
    have hxpos : 0<x := by
      rcases List.mem_cons.mp hx with rfl | hx
      · omega
      · have := hq x hx; omega
    rcases hh with hh | hh <;> omega
  · intro hc
    have he : a=b+1 := hc a (by simp)
    have ht : shifted b q = List.replicate q.length 2 := by
      apply List.map_eq_replicate_iff.mpr
      intro x hx
      have := hc x (by simp [hx])
      omega
    rw [high_first_digits b a q (by omega) ha hq, ht, he]
    have hone : b+1-b=(1:Int) := by omega
    simp only [hone, List.reverse_append, List.reverse_cons, List.reverse_nil,
      List.nil_append, List.reverse_replicate, List.singleton_append, List.cons_append]

/-- Exact floor arithmetic; no parity restriction on the base. -/
theorem half_base_bounds (b : Int) (hb : 3 ≤ b) :
    1 ≤ (b-1)/2 ∧ (b-1)/2 ≤ b-1 ∧ 2*((b-1)/2) ≤ b-1 := by
  have hr0 := Int.emod_nonneg (b-1) (show (2:Int) ≠ 0 by decide)
  have hr2 := Int.emod_lt_of_pos (b-1) (show (0:Int)<2 by decide)
  have he := Int.emod_add_ediv (b-1) 2
  omega

theorem interval_high_bounds (b : Int) (q : List Int) (hb : 3 ≤ b)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ b+(b-1)/2-1) :
    ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2 := by
  intro x hx
  have hh := half_base_bounds b hb
  have := hq x hx
  omega

theorem interval_adjacent_bound (b : Int) (q : List Int) (hb : 3 ≤ b)
    (hq : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ b+(b-1)/2-1) :
    ∀ s ∈ adjacent q, s ≤ 3*b-3 := by
  apply (adjacent_bound_iff q (3*b-3)).mpr
  intro i hi
  have hx := hq q[i] (List.getElem_mem (by omega))
  have hy := hq q[i+1] (List.getElem_mem hi)
  have hh := half_base_bounds b hb
  omega


/-- Iteration is the ordinary digit algorithm at every time, including after a hit. -/
def digitOrbit (b : Int) (digits : List Int) : Nat → List Int
  | 0 => digits
  | t+1 => ordinaryStep b (digitOrbit b digits t)

/-- The usual first positive hitting time; time zero is deliberately excluded. -/
def FirstPositivePalindrome (b : Int) (digits : List Int) (t : Nat) : Prop :=
  0<t ∧ (digitOrbit b digits t).reverse=digitOrbit b digits t ∧
    ∀ s, 0<s → s<t → (digitOrbit b digits s).reverse≠digitOrbit b digits s

/-- Every iterate remains a genuine canonical numeral. -/
theorem digit_orbit_canonical (b : Int) (digits : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits) (t : Nat) :
    DigitBounds b (digitOrbit b digits t) ∧ PositiveLast (digitOrbit b digits t) := by
  induction t with
  | zero => exact ⟨hd,hp⟩
  | succ t ih =>
      obtain ⟨h1,h2,_⟩ := ordinary_step_canonical b (digitOrbit b digits t) hb ih.1 ih.2
      exact ⟨h1,h2⟩

/-- This is the integer reverse-add recurrence, not only a symbolic orbit. -/
theorem digit_orbit_value (b : Int) (digits : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits) (t : Nat) :
    0 < eval b (digitOrbit b digits t) ∧
    eval b (digitOrbit b digits (t+1)) =
      eval b (digitOrbit b digits t) + eval b (digitOrbit b digits t).reverse := by
  obtain ⟨h1,h2⟩ := digit_orbit_canonical b digits hb hd hp t
  exact ⟨canonical_input_positive b _ hb h1 h2,
    (ordinary_step_canonical b _ hb h1 h2).2.2⟩

theorem first_positive_one_iff (b : Int) (digits : List Int) :
    FirstPositivePalindrome b digits 1 ↔
      (ordinaryStep b digits).reverse=ordinaryStep b digits := by
  constructor
  · intro h
    exact h.2.1
  · intro h
    refine ⟨by decide,h,?_⟩
    intro s hs hlt
    omega

theorem first_positive_two_iff (b : Int) (digits : List Int) :
    FirstPositivePalindrome b digits 2 ↔
      (ordinaryStep b digits).reverse≠ordinaryStep b digits ∧
      (ordinaryStep b (ordinaryStep b digits)).reverse=ordinaryStep b (ordinaryStep b digits) := by
  constructor
  · intro h
    exact ⟨h.2.2 1 (by decide) (by decide),h.2.1⟩
  · intro h
    refine ⟨by decide,h.2,?_⟩
    intro s hs hlt
    have he : s=1 := by omega
    subst s
    exact h.1

/-- Actual canonical numerals have precisely the two source cases for first
positive palindrome time. The original numeral may itself be palindromic. -/
theorem numeric_interval_first_hit (b : Int) (digits : List Int) (hb : 3 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hh : ∀ x ∈ pairs digits, b-1 ≤ x ∧ x ≤ b+(b-1)/2-1)
    (ho : b ≤ (pairs digits).headD 0) :
    (∀ t, DigitBounds b (digitOrbit b digits t) ∧
      PositiveLast (digitOrbit b digits t) ∧
      0 < eval b (digitOrbit b digits t) ∧
      eval b (digitOrbit b digits (t+1)) =
        eval b (digitOrbit b digits t) + eval b (digitOrbit b digits t).reverse) ∧
    (FirstPositivePalindrome b digits 1 ↔ ∀ x ∈ pairs digits, x=b+1) ∧
    (FirstPositivePalindrome b digits 2 ↔ ¬ (∀ x ∈ pairs digits, x=b+1)) ∧
    (FirstPositivePalindrome b digits 1 ∨ FirstPositivePalindrome b digits 2) := by
  refine ⟨?_, ?_⟩
  · intro t
    obtain ⟨hc,hp'⟩ := digit_orbit_canonical b digits (by omega) hd hp t
    obtain ⟨hv,hs⟩ := digit_orbit_value b digits (by omega) hd hp t
    exact ⟨hc,hp',hv,hs⟩
  · obtain ⟨a,q,he⟩ := List.exists_cons_of_ne_nil (canonical_pairs_nonempty digits hp)
    have hfull := interval_high_bounds b (pairs digits) hb hh
    have ha : b ≤ a ∧ a ≤ 2*b-2 := by
      rw [he] at ho hfull
      have h0 := hfull a (by simp)
      simp only [List.headD_cons] at ho
      omega
    have ht : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2 := by
      intro x hx
      apply hfull x
      rw [he]
      simp [hx]
    have hs : (a::q).reverse=a::q := by rw [←he]; exact pairs_symmetric digits
    have hfirst : (ordinaryStep b digits).reverse=ordinaryStep b digits ↔
        ∀ x ∈ pairs digits, x=b+1 := by
      unfold ordinaryStep
      rw [he]
      exact first_palindrome_iff_constant b a q hb ha ht hs
    have hsecond : (ordinaryStep b (ordinaryStep b digits)).reverse=
        ordinaryStep b (ordinaryStep b digits) := by
      change (normalize b (nextPairs b (pairs digits))).reverse=normalize b (nextPairs b (pairs digits))
      rw [he]
      apply (second_palindrome_iff_adjacent b a q hb ha ht hs).mpr
      rw [←he]
      exact interval_adjacent_bound b (pairs digits) hb hh
    have h1 := (first_positive_one_iff b digits).trans hfirst
    have h2 : FirstPositivePalindrome b digits 2 ↔ ¬ (∀ x ∈ pairs digits, x=b+1) := by
      rw [first_positive_two_iff]
      constructor
      · intro h hc
        exact h.1 (hfirst.mpr hc)
      · intro h
        exact ⟨fun hpal => h (hfirst.mp hpal),hsecond⟩
    refine ⟨h1,h2,?_⟩
    by_cases hc : ∀ x ∈ pairs digits, x=b+1
    · exact Or.inl (h1.mpr hc)
    · exact Or.inr (h2.mpr hc)

/-- Equal numerals cannot have two distinct first positive palindrome times. -/
theorem first_positive_unique (b : Int) (digits : List Int) (s t : Nat)
    (hs : FirstPositivePalindrome b digits s) (ht : FirstPositivePalindrome b digits t) : s=t := by
  by_cases he : s=t
  · exact he
  exfalso
  have hlt : s<t ∨ t<s := by omega
  rcases hlt with hlt | hlt
  · exact (ht.2.2 s hs.1 hlt) hs.2.1
  · exact (hs.2.2 t ht.1 hlt) ht.2.1

/-- Base five permits the constant case even in width one: 3 -> 6 is a hit. -/
theorem odd_base_first_hit_one_control :
    FirstPositivePalindrome 5 [3] 1 ∧ pairs [3] = [6] := by
  constructor
  · apply (first_positive_one_iff 5 [3]).mpr
    decide
  · decide

/-- The base-three high interval excludes b+1, so this concrete case hits at two. -/
theorem base_three_first_hit_two_control : FirstPositivePalindrome 3 [1,2] 2 := by
  apply (first_positive_two_iff 3 [1,2]).mpr
  decide

end Agent11HighBase
