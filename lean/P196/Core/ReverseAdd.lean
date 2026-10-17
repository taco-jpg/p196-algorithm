import P196.Core.SeamSafety

namespace ReverseAdd
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth SeamSafety

def pairs (digits : List Int) : List Int :=
  List.zipWith (· + ·) digits digits.reverse

def DigitBounds (b : Int) (digits : List Int) : Prop :=
  ∀ d ∈ digits, 0 ≤ d ∧ d < b

/-- Reversal is evaluated as an integer, so zeros at its most significant
end contribute zero and do not change the reversed integer. -/
def reversedValue (b : Int) (digits : List Int) : Int := eval b digits.reverse

theorem pairs_length (digits : List Int) : (pairs digits).length = digits.length := by
  simp [pairs, List.length_zipWith]

theorem pairs_symmetric (digits : List Int) : (pairs digits).reverse = pairs digits := by
  unfold pairs
  rw [List.reverse_zipWith (by simp), List.reverse_reverse, List.zipWith_comm]
  simp only [Int.add_comm]

theorem eval_zip_add (b : Int) (xs ys : List Int) (h : xs.length=ys.length) :
    eval b (List.zipWith (· + ·) xs ys) = eval b xs + eval b ys := by
  induction xs generalizing ys with
  | nil =>
    have hy : ys=[] := List.eq_nil_of_length_eq_zero (by simpa using h.symm)
    subst ys; simp [eval]
  | cons a xs ih =>
    cases ys with
    | nil => simp at h
    | cons c ys =>
      have ht : xs.length=ys.length := by simpa using h
      simp only [List.zipWith_cons_cons, eval, ih ys ht, Int.mul_add]
      omega

theorem pairs_value (b : Int) (digits : List Int) :
    eval b (pairs digits) = eval b digits + reversedValue b digits := by
  exact eval_zip_add b digits digits.reverse (by simp)

theorem zip_add_bounds (b : Int) (xs ys : List Int)
    (hx : DigitBounds b xs) (hy : DigitBounds b ys) :
    ∀ q ∈ List.zipWith (· + ·) xs ys, 0 ≤ q ∧ q ≤ 2*b-2 := by
  induction xs generalizing ys with
  | nil => simp
  | cons a xs ih =>
    cases ys with
    | nil => simp
    | cons c ys =>
      have ha := hx a (by simp)
      have hc := hy c (by simp)
      have hxt : DigitBounds b xs := by intro d hd; exact hx d (by simp [hd])
      have hyt : DigitBounds b ys := by intro d hd; exact hy d (by simp [hd])
      intro q hq
      rcases List.mem_cons.mp hq with rfl | ht
      · change 0 ≤ a+c ∧ a+c ≤ 2*b-2
        omega
      · exact ih ys hxt hyt q ht

theorem pairs_bounds (b : Int) (digits : List Int) (hd : DigitBounds b digits) :
    ∀ q ∈ pairs digits, 0 ≤ q ∧ q ≤ 2*b-2 := by
  apply zip_add_bounds b digits digits.reverse hd
  intro d hm
  exact hd d (by simpa only [List.mem_reverse] using hm)

theorem pairs_positive_last (b : Int) (digits : List Int)
    (hd : DigitBounds b digits) (hp : PositiveLast digits) :
    PositiveLast (pairs digits) := by
  obtain ⟨front,last,he,hpos⟩ := hp
  have hne : digits ≠ [] := by
    intro hn
    have hm : last ∈ digits := by rw [he]; simp
    simp [hn] at hm
  obtain ⟨a,tail,ha⟩ := List.exists_cons_of_ne_nil hne
  have hanonneg := (hd a (by rw [ha]; simp)).1
  have hr : digits.reverse = last :: front.reverse := by simp [he]
  let rest := List.zipWith (· + ·) tail front.reverse
  have hh : pairs digits = (a+last)::rest := by
    unfold pairs
    rw [hr,ha]
    rfl
  refine ⟨rest.reverse,a+last,?_,by omega⟩
  calc
    pairs digits = (pairs digits).reverse := (pairs_symmetric digits).symm
    _ = rest.reverse ++ [a+last] := by rw [hh,List.reverse_cons]

theorem positive_terminal_append (front : List (Int × Bool)) (p : Int × Bool)
    (hp : 0 < p.1) : PositiveTerminal (front ++ [p]) := by
  induction front with
  | nil => exact hp
  | cons a front ih =>
    cases front with
    | nil => exact hp
    | cons c tail => exact ih

theorem positive_terminal_of_projection (xs : List (Int × Bool))
    (hp : PositiveLast (xs.map Prod.fst)) : PositiveTerminal xs := by
  obtain ⟨front,d,he,hpos⟩ := hp
  have hlast : (xs.map Prod.fst).getLast? = some d :=
    List.getLast?_eq_some_iff.mpr ⟨front,he⟩
  rw [List.getLast?_map] at hlast
  cases hxs : xs.getLast? with
  | none => simp [hxs] at hlast
  | some p =>
    have heq : p.1=d := by simpa [hxs] using hlast
    obtain ⟨pre,hpre⟩ := List.getLast?_eq_some_iff.mp hxs
    rw [hpre]
    exact positive_terminal_append pre p (by omega)

theorem tagged_pairs_bound (b : Int) (digits : List Int) (xs : List (Int × Bool))
    (hd : DigitBounds b digits) (hqs : xs.map Prod.fst = pairs digits) : Bounded b xs := by
  intro p hp
  have hm : p.1 ∈ pairs digits := by
    rw [← hqs]
    exact List.mem_map.mpr ⟨p,hp,rfl⟩
  exact pairs_bounds b digits hd _ hm

/-- Canonical digits of the ordinary integer n+reverse_b(n), computed by
continuous carrying. The supplied reset flags affect only raw comparison. -/
theorem reverse_add_normalization (b : Int) (digits : List Int)
    (xs : List (Int × Bool)) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hqs : xs.map Prod.fst = pairs digits) :
    (∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b) ∧
    PositiveLast (actualDigits b xs) ∧
    (actualDigits b xs).length = digits.length +
      (terminal b 0 (ordinaryTags xs)).toNat ∧
    eval b (actualDigits b xs) = eval b digits + reversedValue b digits := by
  have hbound := tagged_pairs_bound b digits xs hd hqs
  have hpositive : PositiveTerminal xs := positive_terminal_of_projection xs
    (by rw [hqs]; exact pairs_positive_last b digits hd hp)
  obtain ⟨hout,hpos,hlen,hval⟩ := canonical_normalization b xs hb hbound hpositive
  have hlength : xs.length=digits.length := by
    have hh := congrArg List.length hqs
    simpa only [List.length_map,pairs_length] using hh
  rw [hlength] at hlen
  rw [hqs,pairs_value] at hval
  exact ⟨hout,hpos,hlen,hval⟩

/-- Any reset/actual outgoing-carry defect certifies that the ordinary
reverse-and-add result has a nonpalindromic canonical digit expansion. -/
theorem reverse_add_defect_safety (b : Int) (digits : List Int)
    (xs : List (Int × Bool)) (index : Nat) (hb : 3 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hqs : xs.map Prod.fst = pairs digits)
    (hdefect : outgoing b xs index ≠ outgoing b (ordinaryTags xs) index) :
    (∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b) ∧
    PositiveLast (actualDigits b xs) ∧
    eval b (actualDigits b xs) = eval b digits + reversedValue b digits ∧
    (actualDigits b xs).reverse ≠ actualDigits b xs := by
  obtain ⟨hout,hpos,_,hvalue⟩ := reverse_add_normalization b digits xs (by omega) hd hp hqs
  have hbound := tagged_pairs_bound b digits xs hd hqs
  have hsym : (xs.map Prod.fst).reverse = xs.map Prod.fst := by
    rw [hqs]; exact pairs_symmetric digits
  exact ⟨hout,hpos,hvalue,outgoing_defect_nonpalindromic b xs index hb hbound hsym hdefect⟩

theorem eval_nonnegative (b : Int) (digits : List Int) (hb : 0 ≤ b)
    (hd : ∀ d ∈ digits, 0 ≤ d) : 0 ≤ eval b digits := by
  induction digits with
  | nil => exact Int.le_refl 0
  | cons a digits ih =>
    have ha := hd a (by simp)
    have ht : ∀ d ∈ digits, 0 ≤ d := by
      intro d hm; exact hd d (by simp [hm])
    have hm := Int.mul_nonneg hb (ih ht)
    change 0 ≤ a + b * eval b digits
    omega

theorem canonical_input_positive (b : Int) (digits : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits) : 0 < eval b digits := by
  obtain ⟨front,d,he,hpos⟩ := hp
  have hfront : ∀ a ∈ front, 0 ≤ a := by
    intro a ha
    exact (hd a (by rw [he]; simp [ha])).1
  have hf := eval_nonnegative b front (by omega) hfront
  have hm := Int.mul_pos (Int.pow_pos (show 0 < b by omega) (m := front.length)) hpos
  rw [he, eval_append]
  simp only [eval, Int.mul_zero, Int.add_zero]
  omega

/-- Odd-base control: a carry defect guarantees a nonpalindromic OUTPUT,
not a nonpalindromic input. Here 212 base three is already palindromic. -/
theorem base_three_palindromic_input_control :
    ([2,1,2] : List Int).reverse = [2,1,2] ∧
    pairs [2,1,2] = [4,2,4] ∧
    outgoing 3 [(4,false),(2,true),(4,false)] 1 = 0 ∧
    outgoing 3 (ordinaryTags [(4,false),(2,true),(4,false)]) 1 = 1 ∧
    actualDigits 3 [(4,false),(2,true),(4,false)] = [1,0,2,1] := by
  decide

end ReverseAdd
