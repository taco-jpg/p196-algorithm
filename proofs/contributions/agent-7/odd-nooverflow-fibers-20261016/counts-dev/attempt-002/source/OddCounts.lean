import OddCenter

/-
Agent #7. Sharp counting for odd no-overflow inverse fibers.
The decimal transition table is imported from the pinned Agent #9 proof.
Finite discovery data is retained separately in counts-dev and is not a proof.
-/
namespace P196.Agent7.OddFibers

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

def countLe (v w : Counts) : Prop :=
  v.a ≤ w.a ∧ v.b ≤ w.b ∧ v.c ≤ w.c ∧ v.d ≤ w.d

instance (v w : Counts) : Decidable (countLe v w) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

def classAdvance (k : Fin 5) (v : Counts) : Counts :=
  match k.val with
  | 0 => ⟨v.c, v.a + v.b, v.c + v.d, v.b⟩
  | 1 => ⟨v.c, v.a, v.d, v.b⟩
  | 2 => ⟨v.a, 0, v.b, v.d⟩
  | 3 => ⟨v.a, v.c, 0, v.d⟩
  | _ => ⟨v.a, v.c, v.b, v.d⟩

def symbolClass (s : Symbol) : Fin 5 :=
  if s.val = 9 then 0
  else if s.val % 2 = 1 then 1
  else if s.val = 0 then 2
  else if s.val = 18 then 3
  else 4

theorem advance_eq_class (s : Symbol) (v : Counts) :
    advance s v = classAdvance (symbolClass s) v := by
  rw [advance_formula]
  by_cases h9 : s.val = 9
  · simp [symbolClass, classAdvance, h9]
  · by_cases ho : s.val % 2 = 1
    · simp [symbolClass, classAdvance, h9, ho]
    · by_cases h0 : s.val = 0
      · simp [symbolClass, classAdvance, h9, ho, h0]
      · by_cases h18 : s.val = 18
        · simp [symbolClass, classAdvance, h9, ho, h0, h18]
        · simp [symbolClass, classAdvance, h9, ho, h0, h18]

def nineRun (n : Nat) : Counts := run (List.replicate n 9) initial

theorem nineRun_succ (n : Nat) :
    nineRun (n+1) = advance 9 (nineRun n) := by
  rw [nineRun, replicate_snoc, run_append]
  rfl

def GrowthGood (v : Counts) : Prop :=
  v.a ≤ v.c ∧ v.d ≤ v.b ∧ v.c ≤ v.a + v.b ∧ v.b ≤ v.c + v.d

instance (v : Counts) : Decidable (GrowthGood v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))

theorem advance_nine_counts (v : Counts) :
    advance 9 v = ⟨v.c, v.a + v.b, v.c + v.d, v.b⟩ := by
  rw [advance_formula]
  rfl

theorem nine_growth_good (v : Counts) (h : GrowthGood v) :
    GrowthGood (advance 9 v) := by
  rw [advance_nine_counts]
  dsimp only [GrowthGood] at *
  omega

theorem nineRun_growth_good (n : Nat) : GrowthGood (nineRun (n+2)) := by
  induction n with
  | zero => decide
  | succ n ih =>
    rw [show n+1+2 = (n+2)+1 by omega, nineRun_succ]
    exact nine_growth_good _ ih

/-- Each of the five exact symbol classes is bounded by a nine step once
the reference vector has the growth inequalities. -/
theorem advance_le_nine (s : Symbol) (v w : Counts)
    (h : countLe v w) (hg : GrowthGood w) :
    countLe (advance s v) (advance 9 w) := by
  rw [advance_formula, advance_nine_counts]
  simp only [countLe, GrowthGood] at *
  split
  · dsimp only; omega
  · split
    · dsimp only; omega
    · split
      · dsimp only; omega
      · split <;> dsimp only <;> omega

/-- The small certificate has only 5^4 cases and uses kernel reduction. -/
theorem four_class_bound : ∀ i j k l : Fin 5,
    countLe (classAdvance l (classAdvance k (classAdvance j
      (classAdvance i initial)))) ⟨1,1,2,1⟩ := by
  decide

theorem four_symbol_bound (s t u v : Symbol) :
    countLe (run [s,t,u,v] initial) (nineRun 4) := by
  have h := four_class_bound (symbolClass s) (symbolClass t)
    (symbolClass u) (symbolClass v)
  have h4 : nineRun 4 = ⟨1,1,2,1⟩ := by decide
  simpa only [run, advance_eq_class, h4] using h

theorem run_le_nines (ss : List Symbol) (n : Nat) (v : Counts)
    (h : countLe v (nineRun (n+2))) :
    countLe (run ss v) (nineRun (n + ss.length + 2)) := by
  induction ss generalizing n v with
  | nil => simpa [run] using h
  | cons s ss ih =>
    have hs := advance_le_nine s v (nineRun (n+2)) h (nineRun_growth_good n)
    rw [← nineRun_succ] at hs
    have ht : countLe (advance s v) (nineRun (n+1+2)) := by
      simpa only [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hs
    have hr := ih (n+1) (advance s v) ht
    simpa only [run, List.length_cons, Nat.add_assoc, Nat.add_comm,
      Nat.add_left_comm] using hr

/-- Four columns suffice for coordinatewise domination by the all-nine run. -/
theorem long_run_dominated (s t u v : Symbol) (ss : List Symbol) :
    countLe (run (s :: t :: u :: v :: ss) initial) (nineRun (ss.length+4)) := by
  have h := run_le_nines ss 2 (run [s,t,u,v] initial) (four_symbol_bound s t u v)
  rw [show 2 + ss.length + 2 = ss.length + 4 by omega] at h
  simpa only [run] using h

def NearBalanced (v : Counts) : Prop :=
  v.a + v.b ≤ v.c + v.d + 1 ∧ v.c + v.d ≤ v.a + v.b + 1 ∧
  v.a ≤ v.d + 1 ∧ v.d ≤ v.a + 1 ∧ v.b ≤ v.c + 1 ∧ v.c ≤ v.b + 1

instance (v : Counts) : Decidable (NearBalanced v) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

theorem nine_near_balanced (v : Counts) (h : NearBalanced v) :
    NearBalanced (advance 9 v) := by
  rw [advance_nine_counts]
  dsimp only [NearBalanced] at *
  omega

theorem nineRun_near_balanced (n : Nat) : NearBalanced (nineRun n) := by
  induction n with
  | zero => decide
  | succ n ih => rw [nineRun_succ]; exact nine_near_balanced _ ih

theorem nineRun_total (n : Nat) :
    (nineRun n).a + (nineRun n).b + (nineRun n).c + (nineRun n).d = fib (n+1) := by
  cases n with
  | zero => decide
  | succ n =>
    have h := nines_exact n
    change (nineRun (n+1)).U = fib n ∧ (nineRun (n+1)).V = fib (n+1) at h
    change _ = fib (n+2)
    rw [fib_succ_succ]
    simp only [Counts.U, Counts.V] at h
    omega

def adjacentMaximum (v : Counts) : Nat := max (v.a + v.b) (v.c + v.d)

/-- The sharp odd-width fiber bound; `m` is the number of exterior pairs. -/
def oddMax (m : Nat) : Nat := (fib (m+1) + 1) / 2

theorem nineRun_adjacent_exact (n : Nat) :
    adjacentMaximum (nineRun n) = oddMax n := by
  have hb := nineRun_near_balanced n
  have ht := nineRun_total n
  simp only [NearBalanced] at hb
  unfold adjacentMaximum oddMax
  by_cases h : (nineRun n).a + (nineRun n).b ≤ (nineRun n).c + (nineRun n).d
  · rw [Nat.max_eq_right h]
    omega
  · have h' : (nineRun n).c + (nineRun n).d ≤ (nineRun n).a + (nineRun n).b := by omega
    rw [Nat.max_eq_left h']
    omega

theorem adjacent_monotone (v w : Counts) (h : countLe v w) :
    adjacentMaximum v ≤ adjacentMaximum w := by
  simp only [countLe] at h
  apply Nat.max_le.mpr
  constructor
  · exact Nat.le_trans (by omega : v.a+v.b ≤ w.a+w.b) (Nat.le_max_left _ _)
  · exact Nat.le_trans (by omega : v.c+v.d ≤ w.c+w.d) (Nat.le_max_right _ _)

theorem one_class_adjacent_bound : ∀ i : Fin 5,
    adjacentMaximum (classAdvance i initial) ≤ 1 := by decide

theorem two_class_adjacent_bound : ∀ i j : Fin 5,
    adjacentMaximum (classAdvance j (classAdvance i initial)) ≤ 1 := by decide

theorem three_class_adjacent_bound : ∀ i j k : Fin 5,
    adjacentMaximum (classAdvance k (classAdvance j (classAdvance i initial))) ≤ 2 := by
  decide

theorem adjacent_run_bound (ss : List Symbol) :
    adjacentMaximum (run ss initial) ≤ oddMax ss.length := by
  cases ss with
  | nil => decide
  | cons s ss =>
    cases ss with
    | nil => simpa [run, advance_eq_class, oddMax, fib] using one_class_adjacent_bound (symbolClass s)
    | cons t ss =>
      cases ss with
      | nil => simpa [run, advance_eq_class, oddMax, fib] using two_class_adjacent_bound (symbolClass s) (symbolClass t)
      | cons u ss =>
        cases ss with
        | nil => simpa [run, advance_eq_class, oddMax, fib] using three_class_adjacent_bound (symbolClass s) (symbolClass t) (symbolClass u)
        | cons v ss =>
          have h := adjacent_monotone _ _ (long_run_dominated s t u v ss)
          rw [nineRun_adjacent_exact] at h
          simpa only [List.length_cons, Nat.add_assoc] using h

def oddEndpoint (v : Fin 10) (c : Counts) : Nat :=
  if v.val % 2 = 0 then c.a + c.b else c.c + c.d

def oddInverseCount (ss : List Symbol) (v : Fin 10) : Nat :=
  oddEndpoint v (run ss initial)

theorem odd_count_bound (ss : List Symbol) (v : Fin 10) :
    oddInverseCount ss v ≤ oddMax ss.length := by
  have h := adjacent_run_bound ss
  unfold oddInverseCount oddEndpoint
  split
  · exact Nat.le_trans (Nat.le_max_left _ _) h
  · exact Nat.le_trans (Nat.le_max_right _ _) h

theorem nines_odd_count_sharp (m : Nat) :
    ∃ v : Fin 10, oddInverseCount (List.replicate m 9) v = oddMax m := by
  have he := nineRun_adjacent_exact m
  unfold adjacentMaximum at he
  by_cases h : (nineRun m).a + (nineRun m).b ≤ (nineRun m).c + (nineRun m).d
  · refine ⟨1, ?_⟩
    rw [Nat.max_eq_right h] at he
    simpa [oddInverseCount, oddEndpoint, nineRun] using he
  · have h' : (nineRun m).c + (nineRun m).d ≤ (nineRun m).a + (nineRun m).b := by omega
    refine ⟨0, ?_⟩
    rw [Nat.max_eq_left h'] at he
    simpa [oddInverseCount, oddEndpoint, nineRun] using he

def oddSuffixCounts (ss : List Symbol) (v : Fin 10) : Counts :=
  ⟨(oddPreimages ss v 0).length, (oddPreimages ss v 1).length,
   (oddPreimages ss v 2).length, (oddPreimages ss v 3).length⟩

theorem odd_dot_suffix (s : Symbol) (ss : List Symbol) (v : Fin 10) (c : Counts) :
    dot c (oddSuffixCounts (s :: ss) v) =
      dot (advance s c) (oddSuffixCounts ss v) := by
  simp only [dot, oddSuffixCounts, oddPreimages, states,
    List.flatMap_cons, List.flatMap_nil, List.append_nil,
    List.length_append, length_oddExtend, advance]
  change _ = _
  simp only [weight, labels, Nat.mul_add, Nat.add_mul, Nat.mul_assoc]
  ac_rfl

theorem odd_dot_run (ss : List Symbol) (v : Fin 10) (c : Counts) :
    dot c (oddSuffixCounts ss v) = oddEndpoint v (run ss c) := by
  induction ss generalizing c with
  | nil =>
    have hv : v.val % 2 < 2 := Nat.mod_lt _ (by decide)
    by_cases h : v.val % 2 = 0
    · simp [dot, oddSuffixCounts, oddPreimages, low, oddEndpoint, run, h,
        show (3 : State).val = 3 from rfl]
    · have h1 : v.val % 2 = 1 := by omega
      simp [dot, oddSuffixCounts, oddPreimages, low, oddEndpoint, run, h, h1,
        show (3 : State).val = 3 from rfl]
  | cons s ss ih => rw [odd_dot_suffix, ih]; rfl

/-- The DP counts the complete duplicate-free exact input enumerator. -/
theorem odd_preimages_length (ss : List Symbol) (v : Fin 10) :
    (oddPreimages ss v 0).length = oddInverseCount ss v := by
  have h := odd_dot_run ss v initial
  simpa [dot, oddSuffixCounts, initial, oddInverseCount] using h

theorem odd_preimages_bound (ss : List Symbol) (v : Fin 10) :
    (oddPreimages ss v 0).length ≤ oddMax ss.length := by
  rw [odd_preimages_length]
  exact odd_count_bound ss v

theorem leading_eleven_odd_count (n : Nat) (v : Fin 10) :
    oddInverseCount (11 :: List.replicate n 9) v =
      oddInverseCount (List.replicate (n+1) 9) v := by
  simp only [oddInverseCount, List.replicate_succ, run, first_eleven_eq_nine]

theorem leading_eleven_odd_sharp (n : Nat) :
    ∃ v : Fin 10, (oddPreimages (11 :: List.replicate n 9) v 0).length = oddMax (n+1) := by
  obtain ⟨v, h⟩ := nines_odd_count_sharp (n+1)
  refine ⟨v, ?_⟩
  rw [odd_preimages_length, leading_eleven_odd_count]
  exact h

/-- Every exact preimage in the attaining family has exterior coefficient
five, so canonical positivity removes none of its members. -/
theorem leading_eleven_odd_positive (ss : List Symbol) (v : Fin 10)
    (xs : List Nat) (z : Nat) (h : (xs,z) ∈ oddPreimages (11 :: ss) v 0) :
    0 < xs.headD z := by
  rw [mem_oddPreimages] at h
  cases xs with
  | nil => exact False.elim h
  | cons x xs =>
    obtain ⟨q, hx, _⟩ := h
    have hp := (leading_eleven_labels q ⟨x, hx.1⟩).mp hx
    have he : x = 5 := hp.2
    simp [he]

theorem odd_count_center_parity (ss : List Symbol) (v w : Fin 10)
    (h : v.val % 2 = w.val % 2) : oddInverseCount ss v = oddInverseCount ss w := by
  simp only [oddInverseCount, oddEndpoint, h]

theorem odd_preimages_center_parity (ss : List Symbol) (v w : Fin 10)
    (h : v.val % 2 = w.val % 2) :
    (oddPreimages ss v 0).length = (oddPreimages ss w 0).length := by
  rw [odd_preimages_length, odd_preimages_length]
  exact odd_count_center_parity ss v w h

#print axioms four_class_bound
#print axioms long_run_dominated
#print axioms nineRun_near_balanced
#print axioms nineRun_adjacent_exact
#print axioms odd_count_bound
#print axioms nines_odd_count_sharp
#print axioms odd_preimages_length
#print axioms odd_preimages_bound
#print axioms leading_eleven_odd_count
#print axioms leading_eleven_odd_sharp
#print axioms leading_eleven_odd_positive
#print axioms odd_count_center_parity
#print axioms odd_preimages_center_parity

end P196.Agent7.OddFibers
