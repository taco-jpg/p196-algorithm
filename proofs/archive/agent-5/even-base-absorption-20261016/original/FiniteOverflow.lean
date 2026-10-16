import InitialValidity

/-!
Agent #5. SOURCE_PRESENT / BUILD_NOT_RUN.
The exact exterior update has a genuine overflow among transitions 0,...,4
from every initially valid decimal state with positive exterior head.
The moment is consequently zero modulo 22 at every state of time >= 5.
No arithmetic correspondence or palindrome-avoidance conclusion is asserted.
-/

namespace P196.Agent5.General.InitialValidity

def head (s : State) : Int := s.B.headD s.c

theorem normalize_append (m : Int) (a b : Word) (e : Int) :
    normalize m (a ++ b) e =
      ((normalize m a e).1 ++ (normalize m b (normalize m a e).2).1,
        (normalize m b (normalize m a e).2).2) := by
  induction a generalizing e with
  | nil => simp [normalize]
  | cons x xs ih => simp [normalize, ih]

theorem normalize_reverse_cons (m x : Int) (xs : Word) (e : Int) :
    normalize m (x :: xs).reverse e =
      ((normalize m xs.reverse e).1 ++
        [(x + (normalize m xs.reverse e).2) % (m + 1)],
        (x + (normalize m xs.reverse e).2) / (m + 1)) := by
  rw [List.reverse_cons, normalize_append]
  simp [normalize]

theorem headD_append_replicate (c : Int) (B : Word) (n : Nat) :
    (B ++ List.replicate n c).headD c = B.headD c := by
  cases B with
  | nil => cases n <;> simp [List.replicate_succ]
  | cons x xs => simp

theorem headD_stripSuffix (c : Int) (B : Word) :
    (stripSuffix c B).1.headD c = B.headD c := by
  conv => rhs; rw [Moment.stripSuffix_decomposition c B]
  exact (headD_append_replicate c (stripSuffix c B).1 (stripSuffix c B).2).symm

theorem head_step_raw (m : Int) (s : State) :
    head (step m s) = (rawExterior m s.c s.B).headD (nextPhase m s.c) := by
  exact headD_stripSuffix (nextPhase m s.c) (rawExterior m s.c s.B)

theorem raw_head_nil (m c : Int) :
    (rawExterior m c []).headD (nextPhase m c) =
      if bulkCarry m c = 0 then 2 * c else c - m := by
  by_cases hk : m + 1 ≤ c <;>
    simp [rawExterior, normalize, bulkCarry, hk] <;> omega

theorem raw_head_cons_no_overflow (m c x : Int) (xs : Word)
    (hg : exteriorOverflow m c (x :: xs) = 0) :
    (rawExterior m c (x :: xs)).headD (nextPhase m c) =
      x % (m + 1) +
        (x + (normalize m xs.reverse (bulkCarry m c)).2) % (m + 1) := by
  have hg' : (normalize m (x :: xs).reverse (bulkCarry m c)).2 = 0 := hg
  simp only [normalize_reverse_cons] at hg'
  simp [rawExterior, normalize_reverse_cons, normalize, hg', List.reverse_append]

theorem raw_head_cons_overflow (m c x : Int) (xs : Word)
    (hg : exteriorOverflow m c (x :: xs) ≠ 0) :
    (rawExterior m c (x :: xs)).headD (nextPhase m c) = x % (m + 1) + 1 := by
  have hg' : (normalize m (x :: xs).reverse (bulkCarry m c)).2 ≠ 0 := hg
  simp [rawExterior, hg', normalize]

/-- A non-overflow doubles the true exterior head, up to a nonnegative carry. -/
theorem head_no_overflow (m : Int) (s : State) (hm : 1 ≤ m)
    (hs : Valid m s) (hg : exteriorOverflow m s.c s.B = 0) :
    head s ≤ m ∧ 2 * head s ≤ head (step m s) := by
  rcases s with ⟨c, B⟩
  cases B with
  | nil =>
    have hk : bulkCarry m c = 0 := hg
    have hc := hs.1
    have hcb : c ≤ m := by
      unfold bulkCarry at hk
      split at hk <;> simp_all <;> omega
    rw [head_step_raw, raw_head_nil, if_pos hk]
    change c ≤ m ∧ 2 * c ≤ 2 * c
    omega
  | cons x xs =>
    have hx := hs.2 x (by simp)
    have hxs : ∀ y ∈ xs.reverse, 0 ≤ y ∧ y ≤ 2 * m := by
      intro y hy
      have hy' : y ∈ xs := by simpa using hy
      exact hs.2 y (by simp [hy'])
    have hk : 0 ≤ bulkCarry m c ∧ bulkCarry m c ≤ 1 := by
      unfold bulkCarry
      split <;> omega
    have he := normalize_carry_bit m xs.reverse (bulkCarry m c) hm hxs hk
    have hg' : (x + (normalize m xs.reverse (bulkCarry m c)).2) / (m + 1) = 0 := by
      simpa only [exteriorOverflow, normalize_reverse_cons] using hg
    have hrem := Int.emod_add_ediv
      (x + (normalize m xs.reverse (bulkCarry m c)).2) (m + 1)
    have hlt := Int.emod_lt_of_pos
      (x + (normalize m xs.reverse (bulkCarry m c)).2) (show 0 < m + 1 by omega)
    have hsum : x + (normalize m xs.reverse (bulkCarry m c)).2 ≤ m := by
      rw [hg'] at hrem
      simp only [Int.mul_zero, Int.add_zero] at hrem
      omega
    have hxmod : x % (m + 1) = x := Int.emod_eq_of_lt hx.1 (by omega)
    have hsum_mod :
        (x + (normalize m xs.reverse (bulkCarry m c)).2) % (m + 1) =
          x + (normalize m xs.reverse (bulkCarry m c)).2 :=
      Int.emod_eq_of_lt (by omega) (by omega)
    rw [head_step_raw, raw_head_cons_no_overflow m c x xs hg, hxmod, hsum_mod]
    change x ≤ m ∧ 2 * x ≤ x + (x + (normalize m xs.reverse (bulkCarry m c)).2)
    omega

theorem head_positive_step (m : Int) (s : State) (hm : 1 ≤ m)
    (hs : Valid m s) (hp : 0 < head s) : 0 < head (step m s) := by
  by_cases hg : exteriorOverflow m s.c s.B = 0
  · have h := (head_no_overflow m s hm hs hg).2
    omega
  · rcases s with ⟨c, B⟩
    cases B with
    | nil =>
      have hk : bulkCarry m c ≠ 0 := hg
      have ht := band_digit_bounds m c hs.1
      have hk1 : bulkCarry m c = 1 := by
        unfold bulkCarry at *
        split at hk <;> simp_all
      rw [head_step_raw, raw_head_nil, if_neg hk]
      simp only [hk1, Int.mul_one] at ht
      omega
    | cons x xs =>
      rw [head_step_raw, raw_head_cons_overflow m c x xs hg]
      have h0 := Int.emod_nonneg x (show m + 1 ≠ 0 by omega)
      omega

theorem head_positive_orbit (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hp : 0 < head s) (n : Nat) : 0 < head (orbit m s n) := by
  induction n with
  | zero => exact hp
  | succ n ih =>
    exact head_positive_step m (orbit m s n) hm (valid_orbit m s hm hodd hs n) ih

/-- The first n non-overflow steps force exponential growth of the head. -/
theorem head_powTwo_lower_bound (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hp : 0 < head s) (n : Nat)
    (hg : ∀ j : Nat, j < n →
      exteriorOverflow m (orbit m s j).c (orbit m s j).B = 0) :
    powTwo n ≤ head (orbit m s n) := by
  induction n with
  | zero => simpa only [powTwo, orbit] using (show (1 : Int) ≤ head s by omega)
  | succ n ih =>
    have hprev := ih (fun j hj => hg j (by omega))
    have hstep := (head_no_overflow m (orbit m s n) hm
      (valid_orbit m s hm hodd hs n) (hg n (by omega))).2
    change powTwo (n + 1) ≤ head (step m (orbit m s n))
    simp only [powTwo]
    omega

/-- All even bases: 2^H > m forces overflow by transition index H. -/
theorem overflow_by_power_bound (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hp : 0 < head s) (H : Nat) (hH : m < powTwo H) :
    ∃ j : Nat, j ≤ H ∧
      exteriorOverflow m (orbit m s j).c (orbit m s j).B = 1 := by
  classical
  by_cases hex : ∃ j : Nat, j ≤ H ∧
      exteriorOverflow m (orbit m s j).c (orbit m s j).B = 1
  · exact hex
  · have hg (j : Nat) (hj : j ≤ H) :
        exteriorOverflow m (orbit m s j).c (orbit m s j).B = 0 := by
      rcases overflow_bit_orbit m s hm hodd hs j with h | h
      · exact h
      · exact False.elim (hex ⟨j, hj, h⟩)
    have hlo := head_powTwo_lower_bound m s hm hodd hs hp H
      (fun j hj => hg j (by omega))
    have hhi := (head_no_overflow m (orbit m s H) hm
      (valid_orbit m s hm hodd hs H) (hg H (by omega))).1
    omega

/-- The reset state occurs no later than time five. -/
theorem decimal_overflow_before_five (s : State) (hs : Valid 9 s)
    (hp : 0 < head s) :
    ∃ j : Nat, j < 5 ∧ exteriorOverflow 9 (orbit 9 s j).c (orbit 9 s j).B = 1 := by
  obtain ⟨j, hj, hg⟩ := overflow_by_power_bound 9 s (by decide)
    ⟨4, by decide⟩ hs hp 4 (by decide)
  exact ⟨j, by omega, hg⟩

/-- The overflow guarantee restarts at every actual exterior state. -/
theorem overflow_in_every_window (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hp : 0 < head s) (H start : Nat) (hH : m < powTwo H) :
    ∃ j : Nat, start ≤ j ∧ j ≤ start + H ∧
      exteriorOverflow m (orbit m s j).c (orbit m s j).B = 1 := by
  obtain ⟨j, hj, hg⟩ := overflow_by_power_bound m (orbit m s start) hm hodd
    (valid_orbit m s hm hodd hs start)
    (head_positive_orbit m s hm hodd hs hp start) H hH
  refine ⟨start + j, by omega, by omega, ?_⟩
  simpa only [orbit_add] using hg

/-- Every five consecutive decimal exterior transitions include an overflow. -/
theorem decimal_overflow_every_five (s : State) (hs : Valid 9 s)
    (hp : 0 < head s) (start : Nat) :
    ∃ j : Nat, start ≤ j ∧ j < start + 5 ∧
      exteriorOverflow 9 (orbit 9 s j).c (orbit 9 s j).B = 1 := by
  obtain ⟨j, hj0, hj1, hg⟩ := overflow_in_every_window 9 s (by decide)
    ⟨4, by decide⟩ hs hp 4 start (by decide)
  exact ⟨j, hj0, by omega, hg⟩

/-- Cofinal computed overflows; no all-time arithmetic realization is inferred. -/
theorem decimal_overflows_arbitrarily_late (s : State) (hs : Valid 9 s)
    (hp : 0 < head s) (N : Nat) :
    ∃ j : Nat, N ≤ j ∧
      exteriorOverflow 9 (orbit 9 s j).c (orbit 9 s j).B = 1 := by
  obtain ⟨j, hj, _, hg⟩ := decimal_overflow_every_five s hs hp N
  exact ⟨j, hj, hg⟩

/-- General-base absorption with initial validity only. -/
theorem residue_zero_from_power_bound (m : Int) (s : State) (hm : 1 ≤ m)
    (hodd : ∃ r : Int, m = 2 * r + 1) (hs : Valid m s)
    (hp : 0 < head s) (H : Nat) (hH : m < powTwo H) (n : Nat) :
    residue m (orbit m s (H + 1 + n)) = 0 := by
  obtain ⟨j, hj, hg⟩ := overflow_by_power_bound m s hm hodd hs hp H hH
  have htime : j + 1 + (H - j) = H + 1 := by omega
  have hz : residue m (orbit m s (H + 1)) = 0 := by
    have h := residue_zero_after_overflow m s hm hodd hs j (H - j) hg
    rwa [htime] at h
  rw [orbit_add]
  exact residue_zero_orbit m (orbit m s (H + 1)) hm hodd
    (valid_orbit m s hm hodd hs (H + 1)) hz n

/-- Neither later digit bounds nor an overflow occurrence is assumed. -/
theorem decimal_residue_zero_from_five (s : State) (hs : Valid 9 s)
    (hp : 0 < head s) (n : Nat) :
    Moment.moment (orbit 9 s (5 + n)).c (orbit 9 s (5 + n)).B % 22 = 0 := by
  obtain ⟨j, hj, hg⟩ := decimal_overflow_before_five s hs hp
  have htime : j + 1 + (4 - j) = 5 := by omega
  have hz5 : residue 9 (orbit 9 s 5) = 0 := by
    have h := residue_zero_after_overflow 9 s (by decide) ⟨4, by decide⟩ hs j (4 - j) hg
    rwa [htime] at h
  change residue 9 (orbit 9 s (5 + n)) = 0
  rw [orbit_add]
  exact residue_zero_orbit 9 (orbit 9 s 5) (by decide) ⟨4, by decide⟩
    (decimal_valid_orbit s hs 5) hz5 n

/-- A canonical even-phase witness: no overflow at 0,1,2,3; overflow at 4. -/
def sharpStart : State := ⟨2, [1]⟩

theorem sharpStart_valid : Valid 9 sharpStart ∧ 0 < head sharpStart := by decide

theorem sharp_no_earlier_overflow :
    ∀ j : Fin 4, exteriorOverflow 9 (orbit 9 sharpStart j.val).c
      (orbit 9 sharpStart j.val).B = 0 := by decide

theorem sharp_fifth_transition :
    exteriorOverflow 9 (orbit 9 sharpStart 4).c (orbit 9 sharpStart 4).B = 1 := by decide

/-- The five-state absorption time is also sharp within the eight even phases. -/
def sharpAbsorptionStart : State := ⟨2, [1, 0]⟩

theorem sharpAbsorptionStart_valid :
    Valid 9 sharpAbsorptionStart ∧ 0 < head sharpAbsorptionStart := by decide

theorem sharpAbsorption_not_at_four :
    residue 9 (orbit 9 sharpAbsorptionStart 4) = 20 := by decide

theorem sharpAbsorption_at_five :
    residue 9 (orbit 9 sharpAbsorptionStart 5) = 0 := by decide

/-- Dropping positive head invalidates the claimed uniform reset time. -/
def zeroHeadStart : State := ⟨2, [0]⟩

theorem zeroHeadStart_valid : Valid 9 zeroHeadStart := by decide

theorem zeroHead_not_absorbed_at_five :
    residue 9 (orbit 9 zeroHeadStart 5) = 2 := by decide

end P196.Agent5.General.InitialValidity
