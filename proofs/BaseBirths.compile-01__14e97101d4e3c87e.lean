import Std

/-!
Base-independent local extreme-pair births.  The local expression is a
same-width mirrored pair after one ordinary normalization.  No statement
here asserts persistence, ancestry, or an infinite reverse-and-add orbit.
-/
namespace BaseBirths

/-- A pair coefficient and the two incoming carries determine its next
same-width pair value.  An overflow changes mirror positions, so this is
not by itself an overflow transition formula. -/
def localPair (b x a c : Int) : Int := (x+a)%b + (x+c)%b

private theorem mod_two_ranges (b z : Int) (hb : 0 < b)
    (hz : 0 ≤ z ∧ z < 2*b) : z%b = if z < b then z else z-b := by
  split
  · exact Int.emod_eq_of_lt hz.1 ‹z < b›
  · have he : z = (z-b)+b := by omega
    calc
      z%b = ((z-b)+b)%b := congrArg (· % b) he
      _ = (z-b)%b := Int.add_emod_self
      _ = z-b := Int.emod_eq_of_lt (by omega) (by omega)

/-- Complete zero-output classification; the statement already holds at
base two.  Its three alternatives are disjoint. -/
theorem localPair_eq_zero_iff (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) :
    localPair b x a c = 0 ↔
      (x=0 ∧ a=0 ∧ c=0) ∨
      (x=b ∧ a=0 ∧ c=0) ∨
      (x=b-1 ∧ a=1 ∧ c=1) := by
  unfold localPair
  rw [mod_two_ranges b (x+a) (by omega) (by omega),
      mod_two_ranges b (x+c) (by omega) (by omega)]
  split <;> split <;> omega

/-- Complete maximal-output classification; the statement already holds
at base two.  Its three alternatives are disjoint. -/
theorem localPair_eq_max_iff (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) :
    localPair b x a c = 2*b-2 ↔
      (x=b-1 ∧ a=0 ∧ c=0) ∨
      (x=b-2 ∧ a=1 ∧ c=1) ∨
      (x=2*b-2 ∧ a=1 ∧ c=1) := by
  unfold localPair
  rw [mod_two_ranges b (x+a) (by omega) (by omega),
      mod_two_ranges b (x+c) (by omega) (by omega)]
  split <;> split <;> omega

/-- A zero pair which was not already zero has exactly these two local
sources.  This is a one-step birth predicate, not an ancestry theorem. -/
theorem new_zero_iff (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) :
    (localPair b x a c = 0 ∧ x ≠ 0) ↔
      (x=b ∧ a=0 ∧ c=0) ∨ (x=b-1 ∧ a=1 ∧ c=1) := by
  rw [localPair_eq_zero_iff b x a c hb hx ha hc]
  omega

/-- A maximal pair which was not already maximal has exactly these two
local sources. -/
theorem new_max_iff (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) :
    (localPair b x a c = 2*b-2 ∧ x ≠ 2*b-2) ↔
      (x=b-1 ∧ a=0 ∧ c=0) ∨ (x=b-2 ∧ a=1 ∧ c=1) := by
  rw [localPair_eq_max_iff b x a c hb hx ha hc]
  omega

/-- Mixed incoming carries cannot create either extreme, in any b≥2. -/
theorem mixed_carries_not_extreme (b x a c : Int) (hb : 2 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) (hac : a ≠ c) :
    localPair b x a c ≠ 0 ∧ localPair b x a c ≠ 2*b-2 := by
  have hz := localPair_eq_zero_iff b x a c hb hx ha hc
  have hm := localPair_eq_max_iff b x a c hb hx ha hc
  omega

/-- For b≥3 every newly created extreme comes from a nonextreme source. -/
theorem births_have_interior_sources (b x a c : Int) (hb : 3 ≤ b)
    (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1)
    (hnew : (localPair b x a c = 0 ∧ x ≠ 0) ∨
      (localPair b x a c = 2*b-2 ∧ x ≠ 2*b-2)) :
    0 < x ∧ x < 2*b-2 := by
  have hz := new_zero_iff b x a c (by omega) hx ha hc
  have hm := new_max_iff b x a c (by omega) hx ha hc
  omega

/-- Binary does not alter the complete classification, but does allow
one extreme to turn directly into the other. -/
theorem binary_extremes_swap :
    localPair 2 0 1 1 = 2 ∧ localPair 2 2 0 0 = 0 := by decide

#print axioms localPair_eq_zero_iff
#print axioms localPair_eq_max_iff
#print axioms new_zero_iff
#print axioms new_max_iff
#print axioms mixed_carries_not_extreme
#print axioms births_have_interior_sources
#print axioms binary_extremes_swap

end BaseBirths
