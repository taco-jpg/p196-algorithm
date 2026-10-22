import Std

namespace Agent213

/-- The selected finite center carry equations uniquely determine the base
    and all six integer parameters. -/
theorem center_rigidity
    (b a c d h k : Int)
    (h_center : h = 2*d + 2*(a+c) - 2*b + 1)
    (k_center : k = 4*(a+c) + 5 - 3*b)
    (d_base : 4*d = b+2)
    (d_center : d = 2*h+1)
    (a_center : a = 2*h)
    (c_center : c = 2*k) :
    b = 26 ∧ a = 6 ∧ c = 14 ∧ d = 7 ∧ h = 3 ∧ k = 7 := by
  omega

/-- In particular, this exact center carry itinerary cannot occur in base 10. -/
theorem center_base10_impossible
    (a c d h k : Int)
    (h_center : h = 2*d + 2*(a+c) - 2*10 + 1)
    (k_center : k = 4*(a+c) + 5 - 3*10)
    (d_base : 4*d = 10+2)
    (d_center : d = 2*h+1)
    (a_center : a = 2*h)
    (c_center : c = 2*k) : False := by
  have hb := (center_rigidity 10 a c d h k h_center k_center d_base
    d_center a_center c_center).1
  omega

#print axioms center_rigidity
#print axioms center_base10_impossible

end Agent213
