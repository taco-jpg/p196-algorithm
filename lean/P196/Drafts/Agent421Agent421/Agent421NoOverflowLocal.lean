import P196.Core.HighBaseNormalization

namespace Agent421NoOverflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase

/-- Source normalization for a mirrored pair of outgoing carry bits. -/
def norm (b s u v : Int) : Int :=
  if u = v then if u = 0 then 2 else b+s-1 else b-1

theorem low_divmod (b x : Int) (hx : 0 ≤ x) (hxb : x < b) :
    x / b = 0 ∧ x % b = x := by
  exact ⟨Int.ediv_eq_zero_of_lt hx hxb, Int.emod_eq_of_lt hx hxb⟩

theorem norm_symmetric (b s u v : Int) : norm b s u v = norm b s v u := by
  unfold norm
  by_cases h : u = v
  · subst v; rfl
  · simp [h, Ne.symm h]

theorem quotient_zero_iff (b x : Int) (hb : 0 < b) (hx : 0 ≤ x) :
    x / b = 0 ↔ x < b := by
  constructor
  · intro h
    have hm := Int.emod_lt_of_pos x hb
    have he := Int.emod_add_ediv x b
    rw [h, Int.mul_zero, Int.add_zero] at he
    omega
  · exact Int.ediv_eq_zero_of_lt hx

/-- Different outgoing carry bits force the neutral column and different inputs. -/
theorem unequal_carries (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2) (ha : 0 ≤ a ∧ a ≤ 1)
    (hc : 0 ≤ c ∧ c ≤ 1) (hne : (x+a)/b ≠ (x+c)/b) :
    x = b-1 ∧ a+c = 1 := by
  have ua := carry_bit b x a hb hx ha
  have uc := carry_bit b x c hb hx hc
  have za := quotient_zero_iff b (x+a) (by omega) (by omega)
  have zc := quotient_zero_iff b (x+c) (by omega) (by omega)
  have hac : a = 0 ∨ a = 1 := by omega
  have hcc : c = 0 ∨ c = 1 := by omega
  rcases hac with rfl | rfl <;> rcases hcc with rfl | rfl <;>
    rcases ua with ua | ua <;> rcases uc with uc | uc <;> omega

/-- Exact local preservation and next-pair bound; no width bound or enumeration. -/
theorem norm_local (b s x a c : Int) (hb : 7 ≤ b)
    (hs : 1 ≤ s ∧ 2*s ≤ b-1)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2) (ha : 0 ≤ a ∧ a ≤ 1)
    (hc : 0 ≤ c ∧ c ≤ 1) :
    let u := (x+a)/b
    let v := (x+c)/b
    (norm b s u v+a)/b = u ∧
    (norm b s u v+c)/b = v ∧
    (norm b s u v+a)%b + (norm b s u v+c)%b ≤ b-1 := by
  dsimp
  have hu := carry_bit b x a (by omega) hx ha
  have hv := carry_bit b x c (by omega) hx hc
  by_cases he : (x+a)/b = (x+c)/b
  · rcases hu with hu | hu
    · have hv0 : (x+c)/b = 0 := by omega
      have da := low_divmod b (2+a) (by omega) (by omega)
      have dc := low_divmod b (2+c) (by omega) (by omega)
      simp only [norm, hu, hv0, ↓reduceIte, da.1, dc.1, da.2, dc.2]
      simp only [true_and]
      omega
    · have hv1 : (x+c)/b = 1 := by omega
      have da := high_divmod b (b+s-1+a) (by omega) (by omega)
      have dc := high_divmod b (b+s-1+c) (by omega) (by omega)
      simp only [norm, hu, hv1, Int.reduceEq, ↓reduceIte, da.1, dc.1, da.2, dc.2]
      simp only [true_and]
      omega
  · have hn := unequal_carries b x a c (by omega) hx ha hc he
    have hnorm : norm b s ((x+a)/b) ((x+c)/b) = x := by
      simp only [norm, he, ↓reduceIte]; omega
    rw [hnorm]
    have da := Int.emod_add_ediv (x+a) b
    have dc := Int.emod_add_ediv (x+c) b
    rcases hu with hu | hu <;> rcases hv with hv | hv
    all_goals simp only [hu, hv, Int.mul_zero, Int.mul_one] at da dc ⊢
    all_goals simp only [true_and]
    all_goals omega

theorem norm_range (b s u v : Int) (hb : 7 ≤ b)
    (hs : 1 ≤ s ∧ 2*s ≤ b-1) :
    0 < norm b s u v ∧ norm b s u v ≤ 2*b-2 := by
  unfold norm
  split
  · split <;> omega
  · omega

theorem norm_center_even (b s u : Int) (he : (b+s-1)%2 = 0) :
    norm b s u u % 2 = 0 := by
  simp only [norm, ↓reduceIte]
  split <;> simp_all

#print axioms norm_local
#print axioms unequal_carries
#print axioms norm_center_even
end Agent421NoOverflow
