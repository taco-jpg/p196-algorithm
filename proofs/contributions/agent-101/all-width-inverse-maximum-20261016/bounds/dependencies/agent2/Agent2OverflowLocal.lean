import Std

/-!
Local arithmetic for the actual overflow inverse scan.

These lemmas do not assert whole-word realizability.  The caller supplies
the actual carry equations, and terminal matching can only remove choices.
The only mathematical inputs are decimal coefficient and binary-carry bounds.
-/

namespace P196.Agent2.OverflowFibers

/-- An actual outgoing overflow past an outer coefficient forces it to be
at least nine, including the neutral-coefficient case. -/
theorem overflow_outer_lower (q c : Nat) (hc : c ≤ 1)
    (hover : (q + c) / 10 = 1) : 9 ≤ q := by
  omega

/-- The overflow target's outer coefficient includes the new leading one. -/
theorem overflow_outer_value (q : Nat) (hlo : 9 ≤ q) (hhi : q ≤ 18) :
    q % 10 + 1 = if q = 9 then 10 else q - 9 := by
  split <;> omega

theorem overflow_outer_target_bounds (q : Nat) :
    1 ≤ q % 10 + 1 ∧ q % 10 + 1 ≤ 10 := by
  omega

/-- The first source coefficient is uniquely determined by the target. -/
theorem overflow_outer_injective (q r : Nat)
    (hqlo : 9 ≤ q) (hqhi : q ≤ 18)
    (hrlo : 9 ≤ r) (hrhi : r ≤ 18)
    (htarget : q % 10 + 1 = r % 10 + 1) : q = r := by
  omega

/-- Version deriving the lower bounds from the actual final carry. -/
theorem actual_overflow_outer_injective (q r c d : Nat)
    (hq : q ≤ 18) (hr : r ≤ 18) (hc : c ≤ 1) (hd : d ≤ 1)
    (hqc : (q + c) / 10 = 1) (hrd : (r + d) / 10 = 1)
    (htarget : q % 10 + 1 = r % 10 + 1) : q = r := by
  exact overflow_outer_injective q r
    (overflow_outer_lower q c hc hqc) hq
    (overflow_outer_lower r d hd hrd) hr htarget

/-- Each fixed reflected outgoing carry confines the coefficient to a
ten-integer interval. The intervals overlap only at the neutral nine. -/
theorem reflected_carry_bounds (x c br : Nat)
    (hx : x ≤ 18) (hc : c ≤ 1) (hcarry : (x + c) / 10 = br) :
    br ≤ 1 ∧ (br = 0 → x ≤ 9) ∧ (br = 1 → 9 ≤ x) := by
  omega

/-- Inside the carry-compatible interval, one residue determines the source
coefficient. No assumption on the auxiliary offset is needed. -/
theorem carry_residue_injective (a br x y cx cy : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18)
    (hcx : cx ≤ 1) (hcy : cy ≤ 1)
    (hcarryx : (x + cx) / 10 = br)
    (hcarryy : (y + cy) / 10 = br)
    (hresidue : (x + a) % 10 = (y + a) % 10) : x = y := by
  have hb := reflected_carry_bounds x cx br hx hcx hcarryx
  by_cases hbr : br = 0
  · have hx9 : x ≤ 9 := by omega
    have hy9 : y ≤ 9 := by omega
    omega
  · have hbr1 : br = 1 := by omega
    have hx9 : 9 ≤ x := by omega
    have hy9 : 9 ≤ y := by omega
    omega

/-- At an inward position, fixing the reflected carry bit leaves at most one
source coefficient satisfying the exact target digit-sum equation. -/
theorem inward_fixed_high_injective (p a br x y cx cy : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18)
    (hcx : cx ≤ 1) (hcy : cy ≤ 1)
    (hcarryx : (x + cx) / 10 = br)
    (hcarryy : (y + cy) / 10 = br)
    (htarget : (x + a) % 10 + (p + br) % 10 =
      (y + a) % 10 + (p + br) % 10) : x = y := by
  apply carry_residue_injective a br x y cx cy hx hy hcx hcy hcarryx hcarryy
  omega

/-- Two even center candidates sharing the already fixed high carry must
also share the proposed next high carry. This is a parity argument, before
any center matching constraint is imposed. -/
theorem even_center_high_carry_unique (p a br bs x y : Nat)
    (hbr : br ≤ 1) (hbs : bs ≤ 1)
    (hevenx : x % 2 = 0) (heveny : y % 2 = 0)
    (hprevious : (p + br) / 10 = (p + bs) / 10)
    (htarget : (x + a) % 10 + (p + br) % 10 =
      (y + a) % 10 + (p + bs) % 10) : br = bs := by
  omega

/-- An odd-width center adds no binary branch: the even coefficient is
unique across both reflected-carry choices. -/
theorem odd_center_injective (p a br bs x y cx cy : Nat)
    (hx : x ≤ 18) (hy : y ≤ 18)
    (hcx : cx ≤ 1) (hcy : cy ≤ 1)
    (hcarryx : (x + cx) / 10 = br)
    (hcarryy : (y + cy) / 10 = bs)
    (hevenx : x % 2 = 0) (heveny : y % 2 = 0)
    (hprevious : (p + br) / 10 = (p + bs) / 10)
    (htarget : (x + a) % 10 + (p + br) % 10 =
      (y + a) % 10 + (p + bs) % 10) : x = y := by
  have hbr := (reflected_carry_bounds x cx br hx hcx hcarryx).1
  have hbs := (reflected_carry_bounds y cy bs hy hcy hcarryy).1
  have heq := even_center_high_carry_unique p a br bs x y
    hbr hbs hevenx heveny hprevious htarget
  rw [← heq] at hcarryy htarget
  exact inward_fixed_high_injective p a br x y cx cy
    hx hy hcx hcy hcarryx hcarryy htarget

/-- Both choices in the sharp family avoid the neutral coefficient nine. -/
theorem binary_family_bounds (y b : Nat) (hylo : 1 ≤ y) (hyhi : y ≤ 8)
    (hb : b ≤ 1) :
    1 ≤ y + 9 * b ∧ y + 9 * b ≤ 18 ∧ y + 9 * b ≠ 9 := by
  omega

/-- Each sharp-family coefficient resets its carry, independently of the
incoming bit. -/
theorem binary_family_carry (y b c : Nat) (hylo : 1 ≤ y) (hyhi : y ≤ 8)
    (hb : b ≤ 1) (hc : c ≤ 1) :
    (y + 9 * b + c) / 10 = b := by
  omega

/-- Every adjacent low/high choice in the sharp family has the same actual
overflow target coefficient. -/
theorem binary_family_pair_output (y b c : Nat)
    (hylo : 1 ≤ y) (hyhi : y ≤ 8) (hb : b ≤ 1) (hc : c ≤ 1) :
    (y + 9 * b + c) % 10 + (y + 9 * c + b) % 10 = 2 * y := by
  have hbc := binary_family_carry y b c hylo hyhi hb hc
  have hcb := binary_family_carry y c b hylo hyhi hc hb
  omega

theorem binary_family_outer_output (y : Nat) (hylo : 1 ≤ y) (hyhi : y ≤ 8) :
    (y + 9) % 10 + 1 = y := by
  omega

/-- The two coefficient choices have opposite parity, so the odd center
has exactly one allowed choice. This records uniqueness; existence is the
explicit parity choice in the following theorem. -/
theorem binary_family_even_unique (y b c : Nat) (hb : b ≤ 1) (hc : c ≤ 1)
    (hbeven : (y + 9 * b) % 2 = 0) (hceven : (y + 9 * c) % 2 = 0) :
    b = c := by
  omega

theorem binary_family_even_choice (y : Nat) :
    y % 2 ≤ 1 ∧ (y + 9 * (y % 2)) % 2 = 0 := by
  omega

#print axioms overflow_outer_lower
#print axioms overflow_outer_value
#print axioms overflow_outer_target_bounds
#print axioms overflow_outer_injective
#print axioms actual_overflow_outer_injective
#print axioms reflected_carry_bounds
#print axioms carry_residue_injective
#print axioms inward_fixed_high_injective
#print axioms even_center_high_carry_unique
#print axioms odd_center_injective
#print axioms binary_family_bounds
#print axioms binary_family_carry
#print axioms binary_family_pair_output
#print axioms binary_family_outer_output
#print axioms binary_family_even_unique
#print axioms binary_family_even_choice

end P196.Agent2.OverflowFibers
