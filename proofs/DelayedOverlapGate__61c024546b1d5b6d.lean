import PairDelayBridge

/-! Exact finite two-step overlap repair. This is not a recurrent certificate
and proves no decimal Lychrel existence assertion. -/

namespace DelayedOverlapGate

set_option maxHeartbeats 2000000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

def Domain (r p u v : Nat) : Prop :=
  1 ≤ r ∧ 1 ≤ p ∧ p ≤ 4 ∧ 1 ≤ u ∧ 5 ≤ v ∧ u + v ≤ 8

def component (r p u v i : Nat) : Nat :=
  if i = 0 ∨ i = 2 * r + 5 then p
  else if i = r + 1 ∨ i = r + 4 then u
  else if i = r + 2 ∨ i = r + 3 then v
  else 0

/-- Symmetric odd-width shape with four exterior coefficients, two flank
coefficients, two inner coefficients, and one central coefficient. -/
def fiveWord (r p a b c i : Nat) : Nat :=
  if i = 0 ∨ i = 1 ∨ i = 2 * r + 5 ∨ i = 2 * r + 6 then p
  else if i = r + 1 ∨ i = r + 5 then a
  else if i = r + 2 ∨ i = r + 4 then b
  else if i = r + 3 then c
  else 0

def initial (r p u v : Nat) : Nat → Nat := fiveWord r p u (u + v) (2 * v)
def middle (r p u v : Nat) : Nat → Nat :=
  fiveWord r (2 * p) (2 * u) (2 * (u + v) + 1) (4 * v - 20)
def returned (r p u v : Nat) : Nat → Nat :=
  fiveWord r (4 * p) (4 * u + 1) (4 * (u + v) - 18) (8 * v - 38)

def shiftOne (q : Nat → Nat) (i : Nat) : Nat :=
  q i + if i = 0 then 0 else q (i - 1)

theorem carry_certificate (q c : Nat → Nat) (L : Nat) (h0 : c 0 = 0)
    (hstep : ∀ i, i < L → c (i + 1) = (q i + c i) / 10) :
    ∀ i, i ≤ L → carry q i = c i := by
  intro i
  induction i with
  | zero => intro _; exact h0.symm
  | succ i ih =>
    intro hi
    rw [carry, ih (by omega)]
    exact (hstep i (by omega)).symm

theorem component_low (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, component r p u v i ≤ 9 := by
  unfold Domain at h
  intro i
  unfold component
  repeat (first | omega | split)

theorem component_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r p u v) i = 0 := by
  apply carry_certificate _ (fun _ => 0) _ rfl
  intro i hi
  have hb := component_low r p u v h i
  omega

theorem initial_is_overlap (r p u v : Nat) (hr : 1 ≤ r) :
    ∀ i, initial r p u v i = shiftOne (component r p u v) i := by
  intro i
  simp only [initial, fiveWord, shiftOne, component]
  repeat (first | omega | split)

def initialCarry (r i : Nat) : Nat := if i = r + 4 then 1 else 0
def middleCarry (r i : Nat) : Nat := if i = r + 3 ∨ i = r + 5 then 1 else 0
def componentDoubleCarry (r i : Nat) : Nat :=
  if i = r + 3 ∨ i = r + 4 then 1 else 0

theorem initial_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (initial r p u v) i = initialCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold initialCarry; split <;> omega)
  intro i hi
  simp only [initial, fiveWord, initialCarry]
  repeat (first | omega | split)

theorem middle_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (middle r p u v) i = middleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold middleCarry; split <;> omega)
  intro i hi
  simp only [middle, fiveWord, middleCarry]
  repeat (first | omega | split)

theorem component_double_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 6 → carry (component r (2 * p) (2 * u) (2 * v)) i =
      componentDoubleCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold componentDoubleCarry; split <;> omega)
  intro i hi
  simp only [component, componentDoubleCarry]
  repeat (first | omega | split)

theorem initial_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (initial r p u v) (2 * r + 7) = 0 := by
  rw [initial_carry r p u v h _ (Nat.le_refl _)]
  unfold initialCarry
  split <;> omega

theorem middle_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (middle r p u v) (2 * r + 7) = 0 := by
  rw [middle_carry r p u v h _ (Nat.le_refl _)]
  unfold middleCarry
  split <;> omega

theorem component_double_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) = 0 := by
  rw [component_double_carry r p u v h _ (Nat.le_refl _)]
  unfold componentDoubleCarry
  split <;> omega

theorem component_symmetric (r p u v : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2 * r + 6 →
      component r p u v i = component r p u v (2 * r + 6 - 1 - i) := by
  intro i hi
  simp only [component]
  repeat (first | omega | split)

theorem fiveWord_symmetric (r p a b c : Nat) (hr : 1 ≤ r) :
    ∀ i, i < 2 * r + 7 →
      fiveWord r p a b c i = fiveWord r p a b c (2 * r + 7 - 1 - i) := by
  intro i hi
  simp only [fiveWord]
  repeat (first | omega | split)

theorem component_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 6) (component r p u v) := by
  refine ⟨by omega, ?_, ?_, component_symmetric r p u v h.1, ?_⟩
  · simpa only [component, true_or, if_true] using h.2.1
  · intro i hi
    have := component_low r p u v h i
    omega
  · intro i hi he
    omega

theorem fiveWord_admissible (r p a b c : Nat) (hr : 1 ≤ r)
    (hp0 : 0 < p) (hp : p ≤ 18) (ha : a ≤ 18) (hb : b ≤ 18)
    (hc : c ≤ 18) (heven : c % 2 = 0) :
    Admissible (2 * r + 7) (fiveWord r p a b c) := by
  refine ⟨by omega, ?_, ?_, fiveWord_symmetric r p a b c hr, ?_⟩
  · simpa only [fiveWord, true_or, if_true] using hp0
  · intro i hi
    simp only [fiveWord]
    repeat (first | omega | split)
  · intro i hi he
    simp only [fiveWord]
    repeat (first | omega | split)

theorem initial_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 7) (initial r p u v) := by
  unfold Domain at h
  exact fiveWord_admissible r p u (u + v) (2 * v)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem middle_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 7) (middle r p u v) := by
  unfold Domain at h
  exact fiveWord_admissible r (2 * p) (2 * u) (2 * (u + v) + 1) (4 * v - 20)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem returned_admissible (r p u v : Nat) (h : Domain r p u v) :
    Admissible (2 * r + 7) (returned r p u v) := by
  unfold Domain at h
  exact fiveWord_admissible r (4 * p) (4 * u + 1) (4 * (u + v) - 18) (8 * v - 38)
    (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)

theorem component_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 6 → nextColumns (component r p u v) (2 * r + 6) i =
      component r (2 * p) (2 * u) (2 * v) i := by
  intro i hi
  simp only [nextColumns, component_carry r p u v h _ (Nat.le_refl _),
    if_true, columnSum, reflected, output]
  rw [component_carry r p u v h i (by omega),
    component_carry r p u v h (2 * r + 6 - 1 - i) (by omega)]
  have hd := h
  unfold Domain at hd
  simp only [component]
  repeat (first | omega | split)

theorem component_double_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 6 →
      nextColumns (component r (2 * p) (2 * u) (2 * v)) (2 * r + 6) i =
        component r (4 * p) (4 * u + 1) (4 * v - 19) i := by
  intro i hi
  simp only [nextColumns, component_double_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [component_double_carry r p u v h i (by omega),
    component_double_carry r p u v h (2 * r + 6 - 1 - i) (by omega)]
  have hd := h
  unfold Domain at hd
  simp only [component, componentDoubleCarry]
  repeat (first | omega | split)

theorem initial_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 → nextColumns (initial r p u v) (2 * r + 7) i =
      middle r p u v i := by
  intro i hi
  simp only [nextColumns, initial_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [initial_carry r p u v h i (by omega),
    initial_carry r p u v h (2 * r + 7 - 1 - i) (by omega)]
  have hd := h
  unfold Domain at hd
  simp only [initial, middle, fiveWord, initialCarry]
  repeat (first | omega | split)

theorem middle_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 → nextColumns (middle r p u v) (2 * r + 7) i =
      returned r p u v i := by
  intro i hi
  simp only [nextColumns, middle_no_overflow r p u v h,
    if_true, columnSum, reflected, output]
  rw [middle_carry r p u v h i (by omega),
    middle_carry r p u v h (2 * r + 7 - 1 - i) (by omega)]
  have hd := h
  unfold Domain at hd
  simp only [middle, returned, fiveWord, middleCarry]
  repeat (first | omega | split)

theorem returned_is_overlap (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, returned r p u v i =
      shiftOne (component r (4 * p) (4 * u + 1) (4 * v - 19)) i := by
  intro i
  have he := initial_is_overlap r (4 * p) (4 * u + 1) (4 * v - 19) h.1 i
  have hd := h
  unfold Domain at hd
  rw [← he]
  simp only [returned, initial, fiveWord]
  repeat (first | omega | split)

/-- This word is deliberately redundant: its center exceeds 18. -/
def redundant (r p u v i : Nat) : Nat := 2 * initial r p u v i

def redundantCarry (r i : Nat) : Nat :=
  if i = r + 4 then 2 else if i = r + 3 ∨ i = r + 5 then 1 else 0

def coefficientDefect (r i : Nat) : Int :=
  if i = r + 2 ∨ i = r + 4 then 1 else if i = r + 3 then -20 else 0

def digitDefect (r i : Nat) : Int :=
  if i = r + 2 then 1 else if i = r + 4 then -1 else 0

theorem redundant_is_component_overlap (r p u v : Nat) (hr : 1 ≤ r) :
    ∀ i, redundant r p u v i = shiftOne (component r (2 * p) (2 * u) (2 * v)) i := by
  intro i
  rw [← initial_is_overlap r (2 * p) (2 * u) (2 * v) hr i]
  simp only [redundant, initial, fiveWord]
  repeat (first | omega | split)

/-- Exact nonzero seam error (1,-20,1), including all surrounding columns. -/
theorem coefficient_defect_exact (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, (middle r p u v i : Int) - (redundant r p u v i : Int) =
      coefficientDefect r i := by
  intro i
  unfold Domain at h
  simp only [middle, redundant, initial, fiveWord, coefficientDefect]
  repeat (first | omega | split)

theorem redundant_carry (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i ≤ 2 * r + 7 → carry (redundant r p u v) i = redundantCarry r i := by
  unfold Domain at h
  apply carry_certificate _ _ _ (by unfold redundantCarry; repeat (first | omega | split))
  intro i hi
  simp only [redundant, initial, fiveWord, redundantCarry]
  repeat (first | omega | split)

theorem redundant_no_overflow (r p u v : Nat) (h : Domain r p u v) :
    carry (redundant r p u v) (2 * r + 7) = 0 := by
  rw [redundant_carry r p u v h _ (Nat.le_refl _)]
  unfold redundantCarry
  repeat (first | omega | split)

/-- The carry interaction converts the seam error into the antisymmetric
normalized digit difference (1,0,-1), at the same central positions. -/
theorem normalized_digit_defect_exact (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 →
      (output (middle r p u v) i : Int) - (output (redundant r p u v) i : Int) =
        digitDefect r i := by
  intro i hi
  simp only [output]
  rw [middle_carry r p u v h i (by omega), redundant_carry r p u v h i (by omega)]
  unfold Domain at h
  simp only [middle, redundant, initial, fiveWord, middleCarry, redundantCarry, digitDefect]
  repeat (first | omega | split)

theorem digitDefect_antisymmetric (r : Nat) :
    ∀ i, i < 2 * r + 7 →
      digitDefect r i = -digitDefect r (2 * r + 7 - 1 - i) := by
  intro i hi
  simp only [digitDefect]
  repeat (first | omega | split)

/-- General exact cancellation principle for paired normalized digits. -/
theorem columnSum_eq_of_antisymmetric_difference (a b : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → (a i : Int) - (b i : Int) =
      -((a (L - 1 - i) : Int) - (b (L - 1 - i) : Int))) :
    ∀ i, i < L → columnSum a L i = columnSum b L i := by
  intro i hi
  have hd := h i hi
  unfold columnSum reflected
  omega

/-- The concrete nonzero digit error disappears when reflected pairs are
formed. The redundant word is not asserted to be an admissible input. -/
theorem seam_cancels_next (r p u v : Nat) (h : Domain r p u v) :
    ∀ i, i < 2 * r + 7 →
      nextColumns (middle r p u v) (2 * r + 7) i =
        nextColumns (redundant r p u v) (2 * r + 7) i := by
  intro i hi
  simp only [nextColumns, middle_no_overflow r p u v h,
    redundant_no_overflow r p u v h, if_true]
  apply columnSum_eq_of_antisymmetric_difference _ _ _ _ i hi
  intro j hj
  rw [normalized_digit_defect_exact r p u v h j hj,
    normalized_digit_defect_exact r p u v h (2 * r + 7 - 1 - j) (by omega)]
  exact digitDefect_antisymmetric r j hj

theorem fiveWord_zero (r p a b c : Nat) : fiveWord r p a b c 0 = p := by
  simp only [fiveWord, true_or, if_true]

theorem fiveWord_center (r p a b c : Nat) (hr : 1 ≤ r) :
    fiveWord r p a b c (r + 3) = c := by
  simp only [fiveWord, true_or, or_true, if_true]
  repeat (first | omega | split)

theorem fiveWord_inner (r p a b c : Nat) (hr : 1 ≤ r) :
    fiveWord r p a b c (r + 2) = b := by
  simp only [fiveWord, true_or, or_true, if_true]
  repeat (first | omega | split)

theorem redundant_not_admissible (r p u v : Nat) (h : Domain r p u v) :
    ¬ Admissible (2 * r + 7) (redundant r p u v) := by
  intro ha
  have hb := ha.2.2.1 (r + 3) (by omega)
  simp only [redundant, initial, fiveWord_center r p u (u + v) (2 * v) h.1] at hb
  unfold Domain at h
  omega

theorem intermediate_overlap_fails (r p u v : Nat) (h : Domain r p u v) :
    ¬ ∀ i, i < 2 * r + 7 →
      nextColumns (initial r p u v) (2 * r + 7) i =
        shiftOne (component r (2 * p) (2 * u) (2 * v)) i := by
  intro he
  have hcenter := he (r + 3) (by omega)
  rw [initial_next r p u v h (r + 3) (by omega),
    ← redundant_is_component_overlap r p u v h.1 (r + 3)] at hcenter
  have hd := coefficient_defect_exact r p u v h (r + 3)
  rw [hcenter] at hd
  simp only [coefficientDefect, if_true] at hd
  split at hd <;> omega

theorem no_overflow_next_congr (q s : Nat → Nat) (L : Nat) (_hL : 0 < L)
    (hs : carry s L = 0) (he : ∀ i, i < L → q i = s i) :
    nextWidth q L = L ∧ ∀ i, i < L → nextColumns q L i = nextColumns s L i := by
  have hq : carry q L = 0 := (carry_congr_upto q s L he L (Nat.le_refl _)).trans hs
  refine ⟨by simp only [nextWidth, hq, if_true], ?_⟩
  intro i hi
  simp only [nextColumns, hq, hs, if_true, columnSum, reflected]
  rw [output_congr_upto q s L he i hi,
    output_congr_upto q s L he (L - 1 - i) (by omega)]

theorem two_steps_of_explicit_columns (q s t : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : carry q L = 0) (hs : carry s L = 0)
    (hqs : ∀ i, i < L → nextColumns q L i = s i)
    (hst : ∀ i, i < L → nextColumns s L i = t i) :
    (iterPairs q L 2).1 = L ∧ ∀ i, i < L → (iterPairs q L 2).2 i = t i := by
  have hw : nextWidth q L = L := by simp only [nextWidth, hq, if_true]
  have hc := no_overflow_next_congr (nextColumns q L) s L hL hs hqs
  change nextWidth (nextColumns q L) (nextWidth q L) = L ∧
    ∀ i, i < L → nextColumns (nextColumns q L) (nextWidth q L) i = t i
  rw [hw]
  exact ⟨hc.1, fun i hi => (hc.2 i hi).trans (hst i hi)⟩

/-- Full component return with unchanged width, valid for every spacer r. -/
theorem component_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (component r p u v) (2 * r + 6) 2).1 = 2 * r + 6 ∧
      ∀ i, i < 2 * r + 6 → (iterPairs (component r p u v) (2 * r + 6) 2).2 i =
        component r (4 * p) (4 * u + 1) (4 * v - 19) i :=
  two_steps_of_explicit_columns _ _ _ _ (by omega)
    (component_carry r p u v h _ (Nat.le_refl _))
    (component_double_no_overflow r p u v h)
    (component_next r p u v h) (component_double_next r p u v h)

/-- Full delayed overlap repair: G²(Phi₁ A)=Phi₁ A′. The first transition
does not independently preserve overlap, as proved above. -/
theorem whole_two_step_return (r p u v : Nat) (h : Domain r p u v) :
    (iterPairs (initial r p u v) (2 * r + 7) 2).1 = 2 * r + 7 ∧
      ∀ i, i < 2 * r + 7 → (iterPairs (initial r p u v) (2 * r + 7) 2).2 i =
        shiftOne (component r (4 * p) (4 * u + 1) (4 * v - 19)) i := by
  have hg := two_steps_of_explicit_columns _ _ _ _ (by omega : 0 < 2 * r + 7)
    (initial_no_overflow r p u v h) (middle_no_overflow r p u v h)
    (initial_next r p u v h) (middle_next r p u v h)
  exact ⟨hg.1, fun i hi => (hg.2 i hi).trans (returned_is_overlap r p u v h i)⟩

theorem initial_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2 * r + 7) (initial r p u v) := by
  have hc : initial r p u v (r + 3) = 2 * v :=
    fiveWord_center r p u (u + v) (2 * v) h.1
  have ho : initial r p u v 0 = p := fiveWord_zero _ _ _ _ _
  unfold Domain at h
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r + 3) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

theorem middle_not_bad (r p u v : Nat) (h : Domain r p u v) :
    ¬ BadWord (2 * r + 7) (middle r p u v) := by
  have hc : middle r p u v (r + 2) = 2 * (u + v) + 1 :=
    fiveWord_inner r (2 * p) (2 * u) (2 * (u + v) + 1) (4 * v - 20) h.1
  have ho : middle r p u v 0 = 2 * p := fiveWord_zero _ _ _ _ _
  unfold Domain at h
  rintro (hlo | ⟨houter, _⟩)
  · have hb := hlo (r + 2) (by omega)
    rw [hc] at hb
    omega
  · rw [ho] at houter
    omega

/-- The direct third-step criterion for the extended p=1,...,4 gate. -/
theorem returned_bad_iff (r p u v : Nat) (h : Domain r p u v) :
    BadWord (2 * r + 7) (returned r p u v) ↔ p ≤ 2 ∧ u = 1 ∧ v = 5 := by
  have ho : returned r p u v 0 = 4 * p := fiveWord_zero _ _ _ _ _
  have hi : returned r p u v (r + 2) = 4 * (u + v) - 18 :=
    fiveWord_inner r (4 * p) (4 * u + 1) (4 * (u + v) - 18) (8 * v - 38) h.1
  have hd := h
  unfold Domain at hd
  constructor
  · rintro (hlo | ⟨houter, _⟩)
    · have h0 := hlo 0 (by omega)
      have h1 := hlo (r + 2) (by omega)
      rw [ho] at h0
      rw [hi] at h1
      omega
    · rw [ho] at houter
      omega
  · rintro ⟨hp, hu, hv⟩
    left
    intro i hi
    simp only [returned, fiveWord, hu, hv]
    repeat (first | omega | split)

/-- Any canonical ordinary realization reaches the stated middle word
after one actual decimal reverse-and-add, at the same finite width. -/
theorem numeric_middle (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 1) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = middle r p u v i := by
  have hw : nextWidth (initial r p u v) (2 * r + 7) = 2 * r + 7 := by
    simp only [nextWidth, initial_no_overflow r p u v h, if_true]
  obtain ⟨e, he, hrep⟩ := representation_next n d (initial r p u v) (2 * r + 7) hc hr
  rw [hw] at he hrep
  exact ⟨e, he, fun i hi => (hrep i hi).trans (initial_next r p u v h i hi)⟩

/-- The two-step repair holds for every actual ordinary realization. -/
theorem numeric_return (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i) :
    ∃ e, Canonical (orbit n 2) e (2 * r + 7) ∧
      ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = returned r p u v i := by
  obtain ⟨e, he, hrep⟩ := numeric_middle n d r p u v h hc hr
  have hw : nextWidth (middle r p u v) (2 * r + 7) = 2 * r + 7 := by
    simp only [nextWidth, middle_no_overflow r p u v h, if_true]
  obtain ⟨f, hf, hfrep⟩ := representation_next (orbit n 1) e (middle r p u v)
    (2 * r + 7) he hrep
  rw [hw] at hf hfrep
  exact ⟨f, hf, fun i hi => (hfrep i hi).trans (middle_next r p u v h i hi)⟩

/-- Safety concerns both positive ordinary iterates, independently of
which canonical digit realization of the initial pair word was chosen. -/
theorem numeric_two_step_safety (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i) :
    ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) := by
  constructor
  · intro hp
    exact initial_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad n d (initial r p u v) (2 * r + 7) hc hr).mp hp)
  · obtain ⟨e, he, hrep⟩ := numeric_middle n d r p u v h hc hr
    intro hp
    exact middle_not_bad r p u v h
      ((PairDelayBridge.palindrome_iff_bad (orbit n 1) e (middle r p u v)
        (2 * r + 7) he hrep).mp hp)

theorem numeric_third_palindrome_iff (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 7))
    (hr : ∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i) :
    Palindrome (orbit n 3) ↔ p ≤ 2 ∧ u = 1 ∧ v = 5 := by
  obtain ⟨e, he, hrep⟩ := numeric_return n d r p u v h hc hr
  exact (PairDelayBridge.palindrome_iff_bad (orbit n 2) e (returned r p u v)
    (2 * r + 7) he hrep).trans (returned_bad_iff r p u v h)

theorem component_first_palindrome (n : Nat) (d : Nat → Nat) (r p u v : Nat)
    (h : Domain r p u v) (hc : Canonical n d (2 * r + 6))
    (hr : ∀ i, i < 2 * r + 6 → columnSum d (2 * r + 6) i = component r p u v i) :
    Palindrome (orbit n 1) := by
  apply (PairDelayBridge.palindrome_iff_bad n d (component r p u v) (2 * r + 6) hc hr).mpr
  exact Or.inl (fun i hi => component_low r p u v h i)

/-- Full existence of a finite decimal realization of the safe two-step
gate, with the entire realization obligation discharged. -/
theorem realized_safe_gate (r p u v : Nat) (h : Domain r p u v) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 → columnSum d (2 * r + 7) i = initial r p u v i) ∧
      ¬ Palindrome (orbit n 1) ∧ ¬ Palindrome (orbit n 2) ∧
      (∃ e, Canonical (orbit n 2) e (2 * r + 7) ∧
        ∀ i, i < 2 * r + 7 → columnSum e (2 * r + 7) i = returned r p u v i) ∧
      (Palindrome (orbit n 3) ↔ p ≤ 2 ∧ u = 1 ∧ v = 5) := by
  have ha := initial_admissible r p u v h
  obtain ⟨n, d, hn, hc, hr⟩ := valid_word_realizable (initial r p u v) (2 * r + 7)
    ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  have hs := numeric_two_step_safety n d r p u v h hc hr
  exact ⟨n, d, hn, hc, hr, hs.1, hs.2, numeric_return n d r p u v h hc hr,
    numeric_third_palindrome_iff n d r p u v h hc hr⟩

/-- The returned core cannot immediately satisfy this gate's domain.
This records the missing renewal condition, rather than postulating it. -/
theorem return_not_in_domain (r p u v : Nat) (h : Domain r p u v) :
    ¬ Domain r (4 * p) (4 * u + 1) (4 * v - 19) := by
  unfold Domain at h ⊢
  omega

end DelayedOverlapGate
