import ActualWords

namespace P196.Agent9.InverseFibers

set_option maxRecDepth 1000
set_option maxHeartbeats 4000000

theorem fib_succ_positive (n : Nat) : 1 ≤ fib (n+1) := by
  induction n with
  | zero => decide
  | succ n ih => change 1 ≤ fib (n+2); rw [fib_succ_succ]; omega

theorem canonical_bound_all (ss : List Symbol) (h : 0 < ss.length) :
    (canonicalPreimages ss).length ≤ max 1 (fib (ss.length-1)) := by
  cases ss with
  | nil => simp at h
  | cons s ss =>
    cases ss with
    | nil =>
      have hf := List.length_filter_le (fun xs => decide (0 < xs.headD 0)) (preimages [s] 0)
      have hh := one_symbol_bound s
      rw [← preimages_length] at hh
      simpa [canonicalPreimages] using Nat.le_trans hf hh
    | cons t ts =>
      have hh := canonical_bound s t ts
      have hf := fib_succ_positive ts.length
      simpa [List.length_cons, Nat.add_sub_cancel, Nat.max_eq_right hf] using hh

theorem width_two_witness : canonicalPreimages [2] = [[1]] := by decide

/-- The exact maximum for every positive even half-width, with a real witness. -/
theorem sharp_maximum (m : Nat) (hm : 0 < m) :
    (∀ ss : List Symbol, ss.length = m →
      (canonicalPreimages ss).length ≤ max 1 (fib (m-1))) ∧
    ∃ ss : List Symbol, ss.length = m ∧
      (canonicalPreimages ss).length = max 1 (fib (m-1)) := by
  constructor
  · intro ss hs; simpa [hs] using canonical_bound_all ss (by omega)
  · cases m with
    | zero => omega
    | succ n =>
      cases n with
      | zero => exact ⟨[2], rfl, by rw [width_two_witness]; decide⟩
      | succ k =>
        refine ⟨11 :: List.replicate (k+1) 9, by simp, ?_⟩
        rw [canonical_sharp]
        have hp := fib_succ_positive k
        simpa using (Nat.max_eq_right hp).symm

theorem replicate_add (n m : Nat) (a : Nat) :
    List.replicate (n+m) a = List.replicate n a ++ List.replicate m a := by
  induction n with
  | zero => simp only [Nat.zero_add, List.replicate_zero, List.nil_append]
  | succ n ih =>
    calc
      List.replicate (Nat.succ n + m) a = a :: List.replicate (n+m) a := by
        rw [Nat.succ_add, List.replicate_succ]
      _ = a :: (List.replicate n a ++ List.replicate m a) := congrArg (List.cons a) ih
      _ = List.replicate (n+1) a ++ List.replicate m a := by
        rw [List.replicate_succ]; rfl

/-- A run of coefficient nines with incoming carry one emits zeros and
preserves that carry, in the existing repository arithmetic. -/
theorem normalize_nines (n : Nat) (xs : List Nat) :
    Agent8.normalize (List.replicate n 9 ++ xs) 1 =
      List.replicate n 0 ++ Agent8.normalize xs 1 := by
  induction n with
  | zero => rfl
  | succ n ih => simp [List.replicate_succ, Agent8.normalize, ih]

/-- Exact digit output of the sharp family's target. -/
theorem sharp_target_digits (n : Nat) :
    Agent8.normalize (mirror (11 :: List.replicate n 9)) 0 =
      1 :: (List.replicate (2*n) 0 ++ [2,1]) := by
  have hm : mirror (11 :: List.replicate n 9) =
      11 :: (List.replicate (2*n) 9 ++ [11]) := by
    simp only [mirror, List.reverse_cons, List.reverse_replicate, List.cons_append,
      List.append_assoc, show 2*n = n+n by omega, replicate_add]
  rw [hm]
  simp [Agent8.normalize, normalize_nines]

/-- At every half-width at least two, the maximizing target is not
palindrome-producing at its next normalization step. -/
theorem sharp_target_not_palindrome (n : Nat) (hn : 0 < n) :
    Agent8.normalize (mirror (11 :: List.replicate n 9)) 0 ≠
      (Agent8.normalize (mirror (11 :: List.replicate n 9)) 0).reverse := by
  rw [sharp_target_digits]
  cases n with
  | zero => omega
  | succ k =>
    intro h
    have hh := congrArg (fun xs : List Nat => xs[1]?) h
    simp [Nat.mul_add, List.replicate_succ, List.reverse_cons,
      List.reverse_append, List.append_assoc] at hh

theorem sharp_target_symbol_values (n : Nat) :
    (11 :: List.replicate n (9 : Symbol)).map Fin.val = 11 :: List.replicate n 9 := by
  simp [show (11 : Symbol).val = 11 from rfl, show (9 : Symbol).val = 9 from rfl]

/-- Sharpness survives the next-step palindrome-avoidance restriction.
This is still a one-step fiber theorem, not an infinite-orbit assertion. -/
theorem sharp_avoiding_family (n : Nat) (hn : 0 < n) :
    (canonicalPreimages (11 :: List.replicate n 9)).Nodup ∧
    (canonicalPreimages (11 :: List.replicate n 9)).length = fib n ∧
    Agent8.normalize (mirror ((11 :: List.replicate n (9 : Symbol)).map Fin.val)) 0 ≠
      (Agent8.normalize (mirror ((11 :: List.replicate n (9 : Symbol)).map Fin.val)) 0).reverse := by
  refine ⟨canonical_nodup _, canonical_sharp n, ?_⟩
  rw [sharp_target_symbol_values]
  exact sharp_target_not_palindrome n hn

theorem mirror_injective (xs ys : List Nat) (h : mirror xs = mirror ys) : xs = ys := by
  have hl := congrArg List.length h
  simp only [mirror, List.length_append, List.length_reverse] at hl
  have hlen : xs.length = ys.length := by omega
  have ht := congrArg (List.take xs.length) h
  simpa [mirror, List.take_append, hlen] using ht

/-- The full coefficient words, not just their half-word encodings. -/
def fullPreimages (ss : List Symbol) : List (List Nat) :=
  (canonicalPreimages ss).map mirror

theorem fullPreimages_nodup (ss : List Symbol) : (fullPreimages ss).Nodup :=
  List.Pairwise.map mirror (fun xs ys hxy he => hxy (mirror_injective xs ys he))
    (canonical_nodup ss)

theorem fullPreimages_membership (ss : List Symbol) (q : List Nat) :
    q ∈ fullPreimages ss ↔ ∃ xs : List Nat,
      ActualFiber ss xs ∧ 0 < xs.headD 0 ∧ mirror xs = q := by
  simp [fullPreimages, canonical_membership, and_assoc]

/-- Literal complete coefficient-word fiber maximum, with no duplicate words. -/
theorem full_sharp_maximum (m : Nat) (hm : 0 < m) :
    (∀ ss : List Symbol, ss.length = m →
      (fullPreimages ss).Nodup ∧ (fullPreimages ss).length ≤ max 1 (fib (m-1))) ∧
    ∃ ss : List Symbol, ss.length = m ∧
      (fullPreimages ss).length = max 1 (fib (m-1)) := by
  obtain ⟨hu, ss, hs, he⟩ := sharp_maximum m hm
  constructor
  · intro ts ht
    exact ⟨fullPreimages_nodup ts, by simpa [fullPreimages] using hu ts ht⟩
  · exact ⟨ss, hs, by simpa [fullPreimages] using he⟩

#print axioms fullPreimages_membership
#print axioms full_sharp_maximum

#print axioms sharp_maximum
#print axioms sharp_target_digits
#print axioms sharp_target_not_palindrome
#print axioms sharp_avoiding_family

end P196.Agent9.InverseFibers
