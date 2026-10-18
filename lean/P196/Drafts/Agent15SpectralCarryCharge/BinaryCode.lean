import P196.Drafts.Agent15SpectralCarryCharge.SpectralWeights

/-!
Binary coefficient words and their exact highest-weight-first integer codes.
This supporting result is scoped to carry bits, not the T/R coefficient code.
-/

namespace P196.Agent15.SpectralCarry

def Binary (cs : List Nat) : Prop :=
  ∀ a ∈ cs, a = 0 ∨ a = 1

def weighted (w : Nat → Int) : List Nat → Int
  | [] => 0
  | a :: xs => (a : Int) * w xs.length + weighted w xs

theorem binary_nil : Binary [] := by
  simp [Binary]

theorem binary_tail {a : Nat} {xs : List Nat} (h : Binary (a :: xs)) :
    Binary xs := by
  intro b hb
  exact h b (List.mem_cons_of_mem a hb)

theorem weighted_bounds (w : Nat → Int) (hpos : ∀ n, 0 ≤ w n)
    {xs : List Nat} (hxs : Binary xs) :
    0 ≤ weighted w xs ∧ weighted w xs ≤ weightSum w xs.length := by
  induction xs with
  | nil => simp [weighted, weightSum]
  | cons a xs ih =>
    have ht := ih (binary_tail hxs)
    have hw := hpos xs.length
    have ha := hxs a (by simp)
    rcases ha with rfl | rfl <;> simp [weighted, weightSum] <;> omega

theorem weighted_lt_next (w : Nat → Int) (hpos : ∀ n, 0 ≤ w n)
    (hdom : ∀ n, weightSum w n < w n) {xs : List Nat} (hxs : Binary xs) :
    weighted w xs < w xs.length := by
  have hb := weighted_bounds w hpos hxs
  exact Int.lt_of_le_of_lt hb.2 (hdom xs.length)

theorem weighted_injective_binary (w : Nat → Int) (hpos : ∀ n, 0 ≤ w n)
    (hdom : ∀ n, weightSum w n < w n)
    {xs ys : List Nat} (hx : Binary xs) (hy : Binary ys)
    (hlen : xs.length = ys.length) (hvalue : weighted w xs = weighted w ys) :
    xs = ys := by
  induction xs generalizing ys with
  | nil =>
    cases ys with
    | nil => rfl
    | cons b ys => simp at hlen
  | cons a xs ih =>
    cases ys with
    | nil => simp at hlen
    | cons b ys =>
      have hx' := binary_tail hx
      have hy' := binary_tail hy
      have hlen' : xs.length = ys.length := by simpa using hlen
      have bx := weighted_bounds w hpos hx'
      have by' := weighted_bounds w hpos hy'
      have dx := hdom xs.length
      have dy := hdom ys.length
      rw [← hlen'] at by' dy
      have ha := hx a (by simp)
      have hb := hy b (by simp)
      have hab : a = b := by
        rcases ha with rfl | rfl <;> rcases hb with rfl | rfl
        · rfl
        · simp [weighted, ← hlen'] at hvalue
          omega
        · simp [weighted, ← hlen'] at hvalue
          omega
        · rfl
      subst b
      have htail : weighted w xs = weighted w ys := by
        simp only [weighted] at hvalue
        rw [← hlen'] at hvalue
        omega
      exact congrArg (List.cons a) (ih hx' hy' hlen' htail)

end P196.Agent15.SpectralCarry
