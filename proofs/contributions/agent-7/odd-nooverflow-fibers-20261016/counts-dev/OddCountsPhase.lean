import OddCountsFixedCenter

/-
Agent #7. The exact six-phase bias for each prescribed odd center digit.
Proof-development extension; excluded from the accepted build until checked.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- The two opposite-coordinate differences rotate through six cases. -/
def CountPhase (k : Nat) (c : Counts) : Prop :=
  match k with
  | 0 => c.a = c.d + 1 ∧ c.b = c.c
  | 1 => c.a = c.d ∧ c.b = c.c + 1
  | 2 => c.d = c.a + 1 ∧ c.b = c.c + 1
  | 3 => c.d = c.a + 1 ∧ c.b = c.c
  | 4 => c.a = c.d ∧ c.c = c.b + 1
  | _ => c.a = c.d + 1 ∧ c.c = c.b + 1

theorem countPhase_advance (k : Nat) (hk : k < 6) (c : Counts)
    (h : CountPhase k c) : CountPhase ((k+1)%6) (advance 9 c) := by
  have he : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 := by omega
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp only [advance_nine_counts, CountPhase] at * <;> omega

theorem nineRun_countPhase (m : Nat) : CountPhase (m%6) (nineRun m) := by
  induction m with
  | zero => simp [CountPhase, nineRun, run, initial]
  | succ m ih =>
    rw [nineRun_succ]
    have h := countPhase_advance (m%6) (Nat.mod_lt _ (by decide)) (nineRun m) ih
    have he : (m+1)%6 = (m%6+1)%6 := by omega
    rw [he]
    exact h

theorem nineRun_even_endpoint (m : Nat) :
    (nineRun m).a + (nineRun m).b =
      if m%6 < 3 then oddMax m else fib (m+1)/2 := by
  have hp := nineRun_countPhase m
  have ht := nineRun_total m
  have hk : m%6 < 6 := Nat.mod_lt _ (by decide)
  have he : m%6 = 0 ∨ m%6 = 1 ∨ m%6 = 2 ∨ m%6 = 3 ∨ m%6 = 4 ∨ m%6 = 5 := by omega
  rcases he with h | h | h | h | h | h <;>
    simp [h, CountPhase, oddMax] at hp ⊢ <;> omega

theorem nineRun_odd_endpoint (m : Nat) :
    (nineRun m).c + (nineRun m).d =
      if m%6 < 3 then fib (m+1)/2 else oddMax m := by
  have hp := nineRun_countPhase m
  have ht := nineRun_total m
  have hk : m%6 < 6 := Nat.mod_lt _ (by decide)
  have he : m%6 = 0 ∨ m%6 = 1 ∨ m%6 = 2 ∨ m%6 = 3 ∨ m%6 = 4 ∨ m%6 = 5 := by omega
  rcases he with h | h | h | h | h | h <;>
    simp [h, CountPhase, oddMax] at hp ⊢ <;> omega

/-- Exact fixed-center maximum. The ceiling belongs to even center digits
in residues 0,1,2 and odd center digits in residues 3,4,5; when Fibonacci
is even, floor and ceiling agree. -/
def oddCenterMax (m : Nat) (v : Fin 10) : Nat :=
  if v.val%2 = 0 then
    if m%6 < 3 then oddMax m else fib (m+1)/2
  else
    if m%6 < 3 then fib (m+1)/2 else oddMax m

theorem nines_fixed_center_formula (m : Nat) (v : Fin 10) :
    oddInverseCount (List.replicate m 9) v = oddCenterMax m v := by
  by_cases h : v.val%2 = 0
  · simpa [oddInverseCount, oddEndpoint, oddCenterMax, nineRun, h] using nineRun_even_endpoint m
  · simpa [oddInverseCount, oddEndpoint, oddCenterMax, nineRun, h] using nineRun_odd_endpoint m

theorem odd_preimages_exact_center_bound (ss : List Symbol) (v : Fin 10) :
    (oddPreimages ss v 0).length ≤ oddCenterMax ss.length v := by
  rw [odd_preimages_length, ← nines_fixed_center_formula]
  exact odd_count_fixed_center_bound ss v

theorem leading_eleven_exact_center (n : Nat) (v : Fin 10) :
    (oddPreimages (11 :: List.replicate n 9) v 0).length = oddCenterMax (n+1) v := by
  rw [odd_preimages_length, leading_eleven_odd_count, nines_fixed_center_formula]

/-- A completely explicit maximizing center, always large enough to make
the target's middle coefficient produce a carry on its next normalization. -/
def sharpCenter (m : Nat) : Fin 10 := if m%6 < 3 then 6 else 7

theorem sharpCenter_six_or_seven (m : Nat) : sharpCenter m = 6 ∨ sharpCenter m = 7 := by
  unfold sharpCenter
  split
  · exact Or.inl rfl
  · exact Or.inr rfl

theorem sharpCenter_large (m : Nat) : 5 ≤ (sharpCenter m).val := by
  unfold sharpCenter
  split <;> decide

theorem oddCenterMax_sharp (m : Nat) : oddCenterMax m (sharpCenter m) = oddMax m := by
  by_cases h : m%6 < 3
  · simp [sharpCenter, oddCenterMax, h, show (6 : Fin 10).val = 6 from rfl]
  · simp [sharpCenter, oddCenterMax, h, show (7 : Fin 10).val = 7 from rfl]

theorem explicit_leading_eleven_sharp (n : Nat) :
    (oddPreimages (11 :: List.replicate n 9) (sharpCenter (n+1)) 0).length = oddMax (n+1) := by
  rw [leading_eleven_exact_center, oddCenterMax_sharp]

/-- The empty-half-width member also has a positive source center. -/
theorem explicit_empty_sharp : oddPreimages [] (sharpCenter 0) 0 = [([],6)] := by
  decide

#print axioms countPhase_advance
#print axioms nineRun_countPhase
#print axioms nineRun_even_endpoint
#print axioms nineRun_odd_endpoint
#print axioms nines_fixed_center_formula
#print axioms odd_preimages_exact_center_bound
#print axioms leading_eleven_exact_center
#print axioms sharpCenter_six_or_seven
#print axioms sharpCenter_large
#print axioms oddCenterMax_sharp
#print axioms explicit_leading_eleven_sharp
#print axioms explicit_empty_sharp

end P196.Agent7.OddFibers
