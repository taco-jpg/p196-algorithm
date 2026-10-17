import P196.Core.HighBaseThreshold

namespace Agent11HighBase
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd

/-- The ordinary digit algorithm; this does not stop when a palindrome occurs. -/
def ordinaryStep (b : Int) (digits : List Int) : List Int := normalize b (pairs digits)

theorem ordinary_step_canonical (b : Int) (digits : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits) :
    DigitBounds b (ordinaryStep b digits) ∧ PositiveLast (ordinaryStep b digits) ∧
      eval b (ordinaryStep b digits) = eval b digits + eval b digits.reverse := by
  obtain ⟨h1,h2,_,h4⟩ := reverse_add_normalization b digits (tags (pairs digits))
    hb hd hp (tags_projection _)
  exact ⟨h1,h2,h4⟩

theorem canonical_pairs_nonempty (digits : List Int) (hp : PositiveLast digits) :
    pairs digits ≠ [] := by
  obtain ⟨front,d,he,hpos⟩ := hp
  intro hn
  have hh := congrArg List.length hn
  rw [pairs_length,he] at hh
  simp at hh

/-- The exact first-step and second-step arithmetic correspondences accompany
both canonical outputs. Every numeral is arbitrary and quantified, not a
certificate instance. Palindromicity uses the computed canonical width. -/
theorem numeric_two_step_threshold (b : Int) (digits : List Int) (hb : 3 ≤ b)
    (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hh : ∀ x ∈ pairs digits, b-1 ≤ x ∧ x ≤ 2*b-2)
    (ho : b ≤ (pairs digits).headD 0) :
    let first := ordinaryStep b digits
    let second := ordinaryStep b first
    DigitBounds b first ∧ PositiveLast first ∧
    DigitBounds b second ∧ PositiveLast second ∧
    eval b first = eval b digits + eval b digits.reverse ∧
    eval b second = eval b first + eval b first.reverse ∧
    (second.reverse=second ↔
      ∀ i : Nat, ∀ h : i+1<(pairs digits).length,
        (pairs digits)[i] + (pairs digits)[i+1] ≤ 3*b-3) := by
  obtain ⟨a,q,he⟩ := List.exists_cons_of_ne_nil (canonical_pairs_nonempty digits hp)
  have ha : b ≤ a ∧ a ≤ 2*b-2 := by
    rw [he] at ho hh
    have hh0 := hh a (by simp)
    simp only [List.headD_cons] at ho
    omega
  have ht : ∀ x ∈ q, b-1 ≤ x ∧ x ≤ 2*b-2 := by
    intro x hx
    apply hh x
    rw [he]
    simp [hx]
  have hs : (a::q).reverse=a::q := by
    rw [←he]
    exact pairs_symmetric digits
  obtain ⟨hd1,hp1,hv1⟩ := ordinary_step_canonical b digits (by omega) hd hp
  obtain ⟨hd2,hp2,hv2⟩ := ordinary_step_canonical b (ordinaryStep b digits)
    (by omega) hd1 hp1
  refine ⟨hd1,hp1,hd2,hp2,hv1,hv2,?_⟩
  change (normalize b (pairs (normalize b (pairs digits)))).reverse =
    normalize b (pairs (normalize b (pairs digits))) ↔ _
  rw [← adjacent_bound_iff (pairs digits) (3*b-3), he]
  exact second_palindrome_iff_adjacent b a q hb ha ht hs

/-- Width one has no internal adjacency obligation; decimal 9 -> 18 -> 99. -/
theorem width_one_control :
    ordinaryStep 10 [9] = [8,1] ∧
    ordinaryStep 10 (ordinaryStep 10 [9]) = [9,9] ∧
    adjacent (pairs [9]) = [] := by decide

/-- Odd-base, equality-at-threshold case: 23 -> 46 -> 80 in ordinary values. -/
theorem base_three_threshold_control :
    pairs [2,1,2] = [4,2,4] ∧
    adjacent (pairs [2,1,2]) = [6,6] ∧
    ordinaryStep 3 [2,1,2] = [1,0,2,1] ∧
    ordinaryStep 3 (ordinaryStep 3 [2,1,2]) = [2,2,2,2] ∧
    eval 3 [2,1,2] = 23 ∧ eval 3 [1,0,2,1] = 46 ∧
    eval 3 [2,2,2,2] = 80 := by decide

/-- Base two is genuinely excluded: 7 -> 14 -> 21, whose second output is
palindromic despite adjacent pair sums exceeding 3*b-3. -/
theorem binary_threshold_counterexample :
    DigitBounds 2 [1,1,1] ∧ PositiveLast [1,1,1] ∧
    pairs [1,1,1] = [2,2,2] ∧
    ordinaryStep 2 [1,1,1] = [0,1,1,1] ∧
    ordinaryStep 2 (ordinaryStep 2 [1,1,1]) = [1,0,1,0,1] ∧
    (ordinaryStep 2 (ordinaryStep 2 [1,1,1])).reverse =
      ordinaryStep 2 (ordinaryStep 2 [1,1,1]) ∧
    ¬ (∀ s ∈ adjacent (pairs [1,1,1]), s ≤ 3*(2:Int)-3) := by
  refine ⟨by simp [DigitBounds], ⟨[1,1],1,rfl,by decide⟩,by decide⟩

/-- An earlier palindrome must not silently halt the stipulated two-step map:
base-three 8 -> 16 -> 32 has a palindromic first output, not its second. -/
theorem continuing_after_palindrome_control :
    ordinaryStep 3 [2,2] = [1,2,1] ∧
    (ordinaryStep 3 [2,2]).reverse = ordinaryStep 3 [2,2] ∧
    ordinaryStep 3 (ordinaryStep 3 [2,2]) = [2,1,0,1] ∧
    (ordinaryStep 3 (ordinaryStep 3 [2,2])).reverse ≠
      ordinaryStep 3 (ordinaryStep 3 [2,2]) := by decide

end Agent11HighBase
