import NormTail
import ZipTail
import BoundaryArithmetic

/-! Isolated Agent19 candidate. All formulas below are projections of the
original Agent6.advance; no width bound or monotonicity is assumed. -/
namespace Agent19.TwoStep
open P196.Agent6
open Agent110.TwoStepNorm Agent110.TwoStepZip Agent110.TwoStepBoundary

def Bounded (w : Word) : Prop := ∀ x ∈ w, x ≤ 18

def rawWord (c : Nat) (w : Word) : Word :=
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let left := norm w 0
  let right := norm w.reverse k
  let u := c + left.2 - 10 * k
  let rhs := if right.2 == 0 then right.1.reverse ++ [t]
             else 1 :: right.1.reverse
  List.zipWith Nat.add (left.1 ++ [u]) rhs

theorem advance_six (w : Word) :
    advance ⟨6,w⟩ = ⟨12, trim 12 (rawWord 6 w)⟩ := rfl

theorem advance_twelve (w : Word) :
    advance ⟨12,w⟩ = ⟨6, trim 6 (rawWord 12 w)⟩ := rfl

theorem norm_carry_bound (w : Word) (e : Nat) (hw : Bounded w)
    (he : e ≤ 1) : (norm w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => exact he
  | cons x xs ih =>
      have hx : x ≤ 18 := hw x (by simp)
      have ht : Bounded xs := by
        intro y hy
        exact hw y (by simp [hy])
      exact ih ((x+e)/10) ht (by omega)

theorem norm_digit_bound (w : Word) (e : Nat) :
    ∀ x ∈ (norm w e).1, x ≤ 9 := by
  induction w generalizing e with
  | nil => simp [norm]
  | cons x xs ih =>
      intro y hy
      simp only [norm, List.mem_cons] at hy
      rcases hy with rfl | hy
      · omega
      · exact ih _ _ hy

theorem exists_snoc (w : Word) (h : w ≠ []) :
    ∃ p x, w = p ++ [x] := by
  induction w with
  | nil => contradiction
  | cons x xs ih =>
      by_cases ht : xs = []
      · subst xs; exact ⟨[], x, rfl⟩
      · obtain ⟨p,y,hp⟩ := ih ht
        exact ⟨x::p,y,by simp [hp]⟩

theorem raw_length (c : Nat) (w : Word) :
    (rawWord c w).length = w.length + 1 := by
  unfold rawWord
  split <;> simp [norm_digits_length]

theorem zip_bounded (a b : Word)
    (ha : ∀ x ∈ a, x ≤ 9) (hb : ∀ x ∈ b, x ≤ 9) :
    Bounded (List.zipWith Nat.add a b) := by
  induction a generalizing b with
  | nil => simp [Bounded]
  | cons x xs ih =>
      cases b with
      | nil => simp [Bounded]
      | cons y ys =>
          have hx := ha x (by simp)
          have hy := hb y (by simp)
          intro z hz
          simp only [List.zipWith, List.mem_cons] at hz
          rcases hz with rfl | hz
          · omega
          · exact ih ys (by intro z hz; exact ha z (by simp [hz]))
              (by intro z hz; exact hb z (by simp [hz])) z hz

theorem raw_bounded (c : Nat) (w : Word) (hc : c = 6 ∨ c = 12)
    (hw : Bounded w) : Bounded (rawWord c w) := by
  have he := norm_carry_bound w 0 hw (by omega)
  have hd := norm_digit_bound w 0
  have hr := norm_digit_bound w.reverse (if 10 ≤ c then 1 else 0)
  unfold rawWord
  apply zip_bounded
  · intro x hx
    simp only [List.mem_append, List.mem_singleton] at hx
    rcases hx with hx | rfl
    · exact hd x hx
    · rcases hc with rfl | rfl <;> simp <;> omega
  · intro x hx
    split at hx
    · simp only [List.mem_append, List.mem_reverse, List.mem_singleton] at hx
      rcases hx with hx | rfl
      · exact hr x hx
      · rcases hc with rfl | rfl <;> decide
    · simp only [List.mem_cons, List.mem_reverse] at hx
      rcases hx with rfl | hx
      · omega
      · exact hr x hx

/-- Two terminal columns of the exact raw successor for every nonempty word.
The reflected penultimate digit may be arbitrary, but remains a decimal digit. -/
theorem raw_tail (c k t : Nat) (xs : Word) (x : Nat)
    (hk : (if 10 ≤ c then 1 else 0) = k) (ht : c - 9*k = t)
    (hw : Bounded (xs ++ [x])) :
    ∃ a mu p P,
      a ≤ 1 ∧ mu ≤ 1 ∧
      rawWord c (xs ++ [x]) = p ++
        [P, c + (x+a)/10 - 10*k + (if mu = 0 then t else (x+k)%10)] ∧
      (if mu = 0 then P = (x+a)%10 + (x+k)%10
       else (x+a)%10 ≤ P ∧ P ≤ (x+a)%10 + 9) := by
  let a := (norm xs 0).2
  let mu := (norm (xs ++ [x]).reverse k).2
  have hxs : Bounded xs := by
    intro y hy; exact hw y (by simp [hy])
  have ha : a ≤ 1 := norm_carry_bound xs 0 hxs (by omega)
  have hkbit : k ≤ 1 := by rw [← hk]; split <;> omega
  have hmu : mu ≤ 1 := norm_carry_bound _ k
    (by intro y hy; exact hw y (List.mem_reverse.mp hy)) hkbit
  have hrev : (xs ++ [x]).reverse = x :: xs.reverse := by simp
  have hnorm : norm (xs ++ [x]).reverse k =
      ((x+k)%10 :: (norm xs.reverse ((x+k)/10)).1,
       (norm xs.reverse ((x+k)/10)).2) := by rw [hrev]; rfl
  have hlen : (norm xs 0).1.length =
      (norm xs.reverse ((x+k)/10)).1.reverse.length := by
    simp [norm_digits_length]
  by_cases hm : mu = 0
  · refine ⟨a,mu,
      List.zipWith Nat.add (norm xs 0).1
        (norm xs.reverse ((x+k)/10)).1.reverse,
      (x+a)%10+(x+k)%10,ha,hmu,?_,by simp [hm]⟩
    have hz : (norm xs.reverse ((x+k)/10)).2 = 0 := by
      simpa [mu, hnorm] using hm
    simp only [rawWord, hk, ht, norm_snoc, hnorm, hz, beq_self_eq_true,
      List.reverse_cons, a, ite_true]
    rw [zipWith_add_snoc _ _ _ _ (by simp [hlen])]
    rw [zipWith_add_snoc _ _ _ _ hlen]
    simp [a, hm, List.append_assoc]
  · have hrne : 1 :: (norm xs.reverse ((x+k)/10)).1.reverse ≠ [] := by simp
    obtain ⟨ys,y,hy⟩ := exists_snoc _ hrne
    have hybound : y ≤ 9 := by
      have hymem : y ∈ 1 :: (norm xs.reverse ((x+k)/10)).1.reverse := by
        rw [hy]; simp
      simp only [List.mem_cons, List.mem_reverse] at hymem
      rcases hymem with rfl | hymem
      · omega
      · exact norm_digit_bound _ _ _ hymem
    have hyslen : (norm xs 0).1.length = ys.length := by
      have hh := congrArg List.length hy
      simp only [List.length_cons, List.length_append, List.length_singleton] at hh
      omega
    refine ⟨a,mu,List.zipWith Nat.add (norm xs 0).1 ys,
      (x+a)%10+y,ha,hmu,?_,by simp [hm]; omega⟩
    have hz : (norm xs.reverse ((x+k)/10)).2 ≠ 0 := by
      simpa [mu, hnorm] using hm
    simp only [rawWord, hk, ht, norm_snoc, hnorm, List.reverse_cons,
      show ((norm xs.reverse ((x+k)/10)).2 == 0) = false by simpa using hz,
      a, ite_false]
    rw [← List.cons_append, hy]
    rw [zipWith_add_snoc _ _ _ _ (by simp [hyslen])]
    rw [zipWith_add_snoc _ _ _ _ hyslen]
    simp [a, hm, List.append_assoc]

end Agent19.TwoStep
