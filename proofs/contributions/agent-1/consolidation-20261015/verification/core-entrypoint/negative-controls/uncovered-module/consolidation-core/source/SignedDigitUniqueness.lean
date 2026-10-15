import Std

/-! Finite zero-representation uniqueness for small signed coefficients.
Lists are least-significant coefficient first: evaluation is recursive
Horner evaluation `a + b * eval tail`. This is the finite uniqueness step
in the general-base seam argument, not a polynomial-reflection theorem. -/

namespace SignedDigitUniqueness

def eval (base : Int) : List Int → Int
  | [] => 0
  | a :: coefficients => a + base * eval base coefficients

def AllZero (coefficients : List Int) : Prop :=
  ∀ a, a ∈ coefficients → a = 0

def CoefficientBounds (base : Int) (coefficients : List Int) : Prop :=
  ∀ a, a ∈ coefficients → -2 ≤ a ∧ a ≤ base - 1

/-- An integer multiple of a positive base cannot cancel a coefficient
strictly between minus that base and the base, unless both are zero. -/
theorem head_tail_zero (base a tail : Int) (hb : 0 < base)
    (hlow : -base < a) (hhigh : a < base) (hz : a + base * tail = 0) :
    a = 0 ∧ tail = 0 := by
  have ht : tail = 0 := by
    by_cases hp : 0 < tail
    · have hmul := Int.mul_le_mul_of_nonneg_left (show (1 : Int) ≤ tail by omega)
        (show 0 ≤ base by omega)
      have hm : base ≤ base * tail := by simpa only [Int.mul_one] using hmul
      omega
    · by_cases hn : tail < 0
      · have hmul := Int.mul_le_mul_of_nonneg_left (show tail ≤ (-1 : Int) by omega)
          (show 0 ≤ base by omega)
        have hm : base * tail ≤ -base := by simpa using hmul
        omega
      · omega
  have ha : a = 0 := by simpa only [ht, Int.mul_zero, Int.add_zero] using hz
  exact ⟨ha, ht⟩

/-- The stronger open-interval form of finite signed zero uniqueness. -/
theorem all_zero_of_eval_zero_open (base : Int) (coefficients : List Int)
    (hb : 0 < base)
    (hbound : ∀ a, a ∈ coefficients → -base < a ∧ a < base)
    (hz : eval base coefficients = 0) : AllZero coefficients := by
  induction coefficients with
  | nil => simp [AllZero]
  | cons a rest ih =>
    have ha := hbound a (by simp)
    have hsplit := head_tail_zero base a (eval base rest) hb ha.1 ha.2 hz
    have hrest : AllZero rest := ih (by
      intro x hx
      exact hbound x (by simp [hx])) hsplit.2
    intro x hx
    simp only [List.mem_cons] at hx
    rcases hx with hxa | hxrest
    · exact hxa.trans hsplit.1
    · exact hrest x hxrest

/-- The coefficient interval occurring in the general-base seam proof. -/
theorem all_zero_of_eval_zero (base : Int) (coefficients : List Int)
    (hb : 3 ≤ base) (hbound : CoefficientBounds base coefficients)
    (hz : eval base coefficients = 0) : AllZero coefficients := by
  apply all_zero_of_eval_zero_open base coefficients (by omega) ?_ hz
  intro a ha
  have h := hbound a ha
  omega

theorem eval_zero_of_all_zero (base : Int) (coefficients : List Int)
    (hzero : AllZero coefficients) : eval base coefficients = 0 := by
  induction coefficients with
  | nil => rfl
  | cons a rest ih =>
    have ha := hzero a (by simp)
    have hr : AllZero rest := by
      intro x hx
      exact hzero x (by simp [hx])
    simp only [eval, ha, ih hr, Int.mul_zero, Int.add_zero]

theorem eval_zero_iff_all_zero (base : Int) (coefficients : List Int)
    (hb : 3 ≤ base) (hbound : CoefficientBounds base coefficients) :
    eval base coefficients = 0 ↔ AllZero coefficients :=
  ⟨all_zero_of_eval_zero base coefficients hb hbound,
    eval_zero_of_all_zero base coefficients⟩

/-- Multiplying a reciprocal-base polynomial evaluation by the highest
base power reverses coefficient order. The uniqueness implication is
unchanged by that reversal. -/
theorem all_zero_of_reverse_eval_zero (base : Int) (coefficients : List Int)
    (hb : 3 ≤ base) (hbound : CoefficientBounds base coefficients)
    (hz : eval base coefficients.reverse = 0) : AllZero coefficients := by
  have hreverse : CoefficientBounds base coefficients.reverse := by
    intro a ha
    exact hbound a (by simpa only [List.mem_reverse] using ha)
  have hall := all_zero_of_eval_zero base coefficients.reverse hb hreverse hz
  intro a ha
  exact hall a (by simpa only [List.mem_reverse] using ha)

theorem eval_ne_zero_of_nonzero_member (base : Int) (coefficients : List Int) (a : Int)
    (hb : 3 ≤ base) (hbound : CoefficientBounds base coefficients)
    (hmem : a ∈ coefficients) (hne : a ≠ 0) : eval base coefficients ≠ 0 := by
  intro hz
  exact hne (all_zero_of_eval_zero base coefficients hb hbound hz a hmem)

/-- The local column equation supplies exactly the residual interval used
above. The carry-bit and digit-range premises are explicit. -/
theorem carry_residual_bounds (base coefficient incoming outgoing digit : Int)
    (hq : 0 ≤ coefficient ∧ coefficient ≤ 2 * base - 2)
    (hin : 0 ≤ incoming ∧ incoming ≤ 1)
    (hout : outgoing = 0 ∨ outgoing = 1)
    (hdigit : 0 ≤ digit ∧ digit ≤ base - 1)
    (heq : coefficient + incoming = digit + base * outgoing) :
    -2 ≤ coefficient - (base + 1) * outgoing ∧
      coefficient - (base + 1) * outgoing ≤ base - 1 := by
  rcases hout with rfl | rfl
  · simp only [Int.mul_zero, Int.sub_zero, Int.add_zero] at *
    omega
  · simp only [Int.mul_one] at *
    omega

/-- A base-two counterexample satisfies the same closed coefficient bounds. -/
theorem base_two_failure :
    CoefficientBounds 2 [-2, 1] ∧ eval 2 [-2, 1] = 0 ∧ ¬ AllZero [-2, 1] := by
  constructor
  · intro a ha
    simp only [List.mem_cons, List.not_mem_nil, or_false] at ha
    rcases ha with rfl | rfl <;> decide
  · constructor
    · decide
    · intro h
      have hz := h (-2) (by simp)
      contradiction

end SignedDigitUniqueness
