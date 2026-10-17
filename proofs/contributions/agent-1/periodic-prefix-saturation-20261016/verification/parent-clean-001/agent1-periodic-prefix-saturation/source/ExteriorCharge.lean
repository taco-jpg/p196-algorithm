import Std

/-
Formal scope: the autonomous exterior formula in the companion quotient note.
The ordinary-integer factor bridge remains a written proof. The algebraic
charge theorem permits some additional phases; only SixPhase states are
used for the closed-return theorem. No assertion that any return exists.
-/

namespace Agent2Exterior

/-- Same-length decimal normalization, with a separately returned final carry. -/
def normalize : List Nat → Nat → List Nat × Nat
  | [], e => ([], e)
  | a :: as, e =>
      let rest := normalize as ((a + e) / 10)
      ((a + e) % 10 :: rest.1, rest.2)

@[simp] theorem sum_append (as bs : List Nat) :
    (as ++ bs).sum = as.sum + bs.sum := by
  induction as with
  | nil => simp
  | cons a as ih => simp [ih, Nat.add_assoc]

@[simp] theorem sum_reverse (as : List Nat) : as.reverse.sum = as.sum := by
  induction as with
  | nil => simp
  | cons a as ih => simp [List.reverse_cons, ih, Nat.add_comm]

theorem sum_zipWith_add (as bs : List Nat) (h : as.length = bs.length) :
    (List.zipWith (· + ·) as bs).sum = as.sum + bs.sum := by
  induction as generalizing bs with
  | nil =>
      cases bs with
      | nil => simp
      | cons b bs => simp at h
  | cons a as ih =>
      cases bs with
      | nil => simp at h
      | cons b bs =>
          have hh : as.length = bs.length := by simpa using h
          simp only [List.zipWith_cons_cons, List.sum_cons]
          rw [ih bs hh]
          omega

@[simp] theorem normalize_length (as : List Nat) (e : Nat) :
    (normalize as e).1.length = as.length := by
  induction as generalizing e with
  | nil => rfl
  | cons a as ih => simp [normalize, ih]

theorem normalize_carry_bit (as : List Nat) (e : Nat)
    (hd : ∀ a ∈ as, a ≤ 18) (he : e ≤ 1) :
    (normalize as e).2 ≤ 1 := by
  induction as generalizing e with
  | nil => exact he
  | cons a as ih =>
      have ha : a ≤ 18 := hd a (by simp)
      have ht : ∀ x ∈ as, x ≤ 18 := by
        intro x hx
        exact hd x (by simp [hx])
      have hn : (a + e) / 10 ≤ 1 := by omega
      exact ih ((a + e) / 10) ht hn

theorem normalize_sum_mod9 (as : List Nat) (e : Nat) :
    ((normalize as e).1.sum + (normalize as e).2) % 9 =
      (as.sum + e) % 9 := by
  induction as generalizing e with
  | nil => simp [normalize]
  | cons a as ih =>
      have h := ih ((a + e) / 10)
      have div := Nat.mod_add_div (a + e) 10
      simp only [normalize, List.sum_cons]
      omega


def phase (c : Nat) : Nat := 2 * (c - 9 * (c / 10))

def overflow (c : Nat) (B : List Nat) : Nat :=
  (normalize B.reverse (c / 10)).2

/-- The untrimmed autonomous exterior, exactly as in the all-gap formula. -/
def rawExterior (c : Nat) (B : List Nat) : List Nat :=
  let D := normalize B 0
  let R := normalize B.reverse (c / 10)
  let u := c + D.2 - 10 * (c / 10)
  let t := c - 9 * (c / 10)
  if R.2 = 0 then
    List.zipWith (· + ·) (D.1 ++ [u]) (R.1.reverse ++ [t])
  else
    List.zipWith (· + ·) (D.1 ++ [u]) (1 :: R.1.reverse)

@[simp] theorem rawExterior_length (c : Nat) (B : List Nat) :
    (rawExterior c B).length = B.length + 1 := by
  simp only [rawExterior]
  split <;> simp [List.length_zipWith]

theorem phase_mod9 (c : Nat) : (phase c) % 9 = (2*c) % 9 := by
  have h := Nat.mod_add_div c 10
  simp only [phase]
  omega

theorem raw_sum_nooverflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 0) :
    (rawExterior c B).sum % 9 = (2*B.sum + 2*c) % 9 := by
  have hD := normalize_sum_mod9 B 0
  have hR := normalize_sum_mod9 B.reverse (c / 10)
  have hc := Nat.mod_add_div c 10
  simp only [List.length_reverse, sum_reverse] at hR
  unfold overflow at hg
  simp only [rawExterior, hg, if_true]
  rw [sum_zipWith_add]
  · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil, Nat.add_zero]
    omega
  · simp

theorem raw_sum_overflow (c : Nat) (B : List Nat)
    (hg : overflow c B = 1) :
    (rawExterior c B).sum % 9 = (2*B.sum + c) % 9 := by
  have hD := normalize_sum_mod9 B 0
  have hR := normalize_sum_mod9 B.reverse (c / 10)
  have hc := Nat.mod_add_div c 10
  simp only [List.length_reverse, sum_reverse] at hR
  unfold overflow at hg
  simp only [rawExterior, hg, Nat.one_ne_zero, if_false]
  rw [sum_zipWith_add]
  · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil, Nat.add_zero]
    omega
  · simp

def charge (c : Nat) (B : List Nat) : Int :=
  (B.sum : Int) - (B.length : Int) * (c : Int)

@[simp] theorem charge_nil (c : Nat) : charge c [] = 0 := by
  simp [charge]

theorem charge_cons (c a : Nat) (B : List Nat) :
    charge c (a :: B) = (a : Int) - (c : Int) + charge c B := by
  simp only [charge, List.sum_cons, List.length_cons, Int.ofNat_add,
    Int.ofNat_succ, Int.add_mul, Int.one_mul]
  omega

/-- Remove a maximal suffix of copies of c. -/
def trimSuffix (c : Nat) : List Nat → List Nat
  | [] => []
  | a :: as =>
      let tail := trimSuffix c as
      if tail = [] ∧ a = c then [] else a :: tail

theorem charge_trimSuffix (c : Nat) (B : List Nat) :
    charge c (trimSuffix c B) = charge c B := by
  induction B with
  | nil => rfl
  | cons a as ih =>
      simp only [trimSuffix]
      split
      · rename_i h
        have ht : charge c as = 0 := by rw [← ih, h.1]; simp
        rw [charge_nil, charge_cons, h.2, ht]
        omega
      · rw [charge_cons, ih, charge_cons]

def exterior (c : Nat) (B : List Nat) : List Nat :=
  trimSuffix (phase c) (rawExterior c B)


theorem raw_charge_mod9 (c : Nat) (B : List Nat)
    (hg : overflow c B ≤ 1) :
    (charge (phase c) (rawExterior c B)) % 9 =
      (2 * charge c B - (overflow c B : Int) * (c : Int)) % 9 := by
  have hp : (phase c : Int) % 9 = (2 * (c : Int)) % 9 := by
    have h := phase_mod9 c
    omega
  have hm : ((B.length : Int) * (phase c : Int)) % 9 =
      (2 * ((B.length : Int) * (c : Int))) % 9 := by
    calc
      _ = ((B.length : Int) % 9 * ((phase c : Int) % 9)) % 9 :=
        Int.mul_emod _ _ _
      _ = ((B.length : Int) % 9 * ((2 * (c : Int)) % 9)) % 9 := by rw [hp]
      _ = ((B.length : Int) * (2 * (c : Int))) % 9 :=
        (Int.mul_emod _ _ _).symm
      _ = _ := by rw [Int.mul_left_comm]
  have cases : overflow c B = 0 ∨ overflow c B = 1 := by omega
  rcases cases with h0 | h1
  · have hs := raw_sum_nooverflow c B h0
    simp only [charge, rawExterior_length, Int.ofNat_add, Int.ofNat_one,
      Int.add_mul, Int.one_mul, Int.mul_sub, h0, Int.ofNat_zero, Int.zero_mul,
      Int.sub_zero]
    omega
  · have hs := raw_sum_overflow c B h1
    simp only [charge, rawExterior_length, Int.ofNat_add, Int.ofNat_one,
      Int.add_mul, Int.one_mul, Int.mul_sub, h1, Int.one_mul]
    omega

/-- All-width charge law for the explicitly defined actual exterior formula. -/
theorem exterior_charge_mod9 (c : Nat) (B : List Nat)
    (hc : c ≤ 18) (hB : ∀ a ∈ B, a ≤ 18) :
    (charge (phase c) (exterior c B)) % 9 =
      (2 * charge c B - (overflow c B : Int) * (c : Int)) % 9 := by
  have hrev : ∀ a ∈ B.reverse, a ≤ 18 := by
    intro a ha
    exact hB a (by simpa using ha)
  have hbit : overflow c B ≤ 1 := by
    exact normalize_carry_bit B.reverse (c / 10) hrev (by omega)
  unfold exterior
  rw [charge_trimSuffix]
  exact raw_charge_mod9 c B hbit

/-- Precisely the six-cycle phases that are invertible modulo nine. -/
def SixPhase (c : Nat) : Prop :=
  c = 2 ∨ c = 4 ∨ c = 8 ∨ c = 16 ∨ c = 14 ∨ c = 10

/-- Representatives of the modular inverses, defined only where used. -/
def inv9 (c : Nat) : Int :=
  if c = 2 then 5 else if c = 4 then 7 else if c = 8 then 8 else
  if c = 16 then 4 else if c = 14 then 2 else if c = 10 then 1 else 0

def J (c : Nat) (E : Int) : Int := (2 * inv9 c * E) % 9

theorem sixPhase_next (c : Nat) (hc : SixPhase c) : SixPhase (phase c) := by
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [phase, SixPhase]

theorem J_step (c : Nat) (E E' g : Int) (hc : SixPhase c)
    (he : E' % 9 = (2*E - g*(c : Int)) % 9) :
    J (phase c) E' = (J c E - g) % 9 := by
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [phase, J, inv9] at * <;> omega

/-- The modular decrement is proved for arbitrary finite exterior lists. -/
theorem exterior_J_step (c : Nat) (B : List Nat)
    (hc : SixPhase c) (hB : ∀ a ∈ B, a ≤ 18) :
    J (phase c) (charge (phase c) (exterior c B)) =
      (J c (charge c B) - (overflow c B : Int)) % 9 := by
  have hbound : c ≤ 18 := by unfold SixPhase at hc; omega
  exact J_step c (charge c B) (charge (phase c) (exterior c B))
    (overflow c B : Int) hc (exterior_charge_mod9 c B hbound hB)


/-- Finite overflow counts; no infinite-survival hypothesis is involved. -/
def prefixCount (g : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => prefixCount g n + g n

theorem J_telescope (j : Nat → Int) (g : Nat → Nat) (n : Nat)
    (hs : ∀ i, i < n → j (i+1) = (j i - (g i : Int)) % 9) :
    (j n + (prefixCount g n : Int)) % 9 = (j 0) % 9 := by
  induction n with
  | zero => simp [prefixCount]
  | succ n ih =>
      have hp := ih (by intro i hi; exact hs i (by omega))
      have hn := hs n (by omega)
      simp only [prefixCount, Int.ofNat_add]
      omega

theorem closed_J_count_mod9 (j : Nat → Int) (g : Nat → Nat) (n : Nat)
    (hs : ∀ i, i < n → j (i+1) = (j i - (g i : Int)) % 9)
    (hc : j n = j 0) : prefixCount g n % 9 = 0 := by
  have h := J_telescope j g n hs
  omega

structure ExteriorState where
  c : Nat
  B : List Nat
  deriving DecidableEq

def nextState (s : ExteriorState) : ExteriorState :=
  ⟨phase s.c, exterior s.c s.B⟩

def validState (s : ExteriorState) : Prop :=
  SixPhase s.c ∧ (∀ a ∈ s.B, a ≤ 18)

def stateJ (s : ExteriorState) : Int := J s.c (charge s.c s.B)


theorem normalize_digit_bound (B : List Nat) (e : Nat) :
    ∀ a ∈ (normalize B e).1, a ≤ 9 := by
  induction B generalizing e with
  | nil => simp [normalize]
  | cons b bs ih =>
      intro a ha
      simp only [normalize, List.mem_cons] at ha
      rcases ha with rfl | ht
      · omega
      · exact ih ((b+e)/10) a ht

theorem zip_digit_bound (A B : List Nat)
    (ha : ∀ a ∈ A, a ≤ 9) (hb : ∀ b ∈ B, b ≤ 9) :
    ∀ x ∈ List.zipWith (· + ·) A B, x ≤ 18 := by
  induction A generalizing B with
  | nil => simp
  | cons a as ih =>
      cases B with
      | nil => simp
      | cons b bs =>
          intro x hx
          simp only [List.zipWith_cons_cons, List.mem_cons] at hx
          rcases hx with rfl | ht
          · have h1 := ha a (by simp)
            have h2 := hb b (by simp)
            omega
          · apply ih bs _ _ x ht
            · intro z hz; exact ha z (by simp [hz])
            · intro z hz; exact hb z (by simp [hz])

theorem trimSuffix_mem (c : Nat) (B : List Nat) (a : Nat)
    (ha : a ∈ trimSuffix c B) : a ∈ B := by
  induction B with
  | nil => exact ha
  | cons b bs ih =>
      simp only [trimSuffix] at ha
      split at ha
      · simp at ha
      · simp only [List.mem_cons] at ha ⊢
        rcases ha with h | h
        · exact Or.inl h
        · exact Or.inr (ih h)

theorem exterior_digit_bound (c : Nat) (B : List Nat)
    (hc : SixPhase c) (hB : ∀ a ∈ B, a ≤ 18) :
    ∀ a ∈ exterior c B, a ≤ 18 := by
  have he := normalize_carry_bit B 0 hB (by omega)
  have hu : c + (normalize B 0).2 - 10*(c/10) ≤ 9 := by
    unfold SixPhase at hc
    omega
  have ht : c - 9*(c/10) ≤ 9 := by
    unfold SixPhase at hc
    omega
  have hD := normalize_digit_bound B 0
  have hR : ∀ a ∈ (normalize B.reverse (c/10)).1.reverse, a ≤ 9 := by
    intro a ha
    exact normalize_digit_bound B.reverse (c/10) a (by simpa using ha)
  have hleft : ∀ a ∈ (normalize B 0).1 ++ [c + (normalize B 0).2 - 10*(c/10)],
      a ≤ 9 := by
    intro a ha
    simp only [List.mem_append, List.mem_singleton] at ha
    rcases ha with ha | rfl
    · exact hD a ha
    · exact hu
  intro a ha
  have hm := trimSuffix_mem (phase c) (rawExterior c B) a ha
  unfold rawExterior at hm
  dsimp only at hm
  split at hm
  · apply zip_digit_bound _ _ hleft _ a hm
    intro x hx
    simp only [List.mem_append, List.mem_singleton] at hx
    rcases hx with hx | rfl
    · exact hR x hx
    · exact ht
  · apply zip_digit_bound _ _ hleft _ a hm
    intro x hx
    simp only [List.mem_cons] at hx
    rcases hx with rfl | hx
    · omega
    · exact hR x hx

theorem valid_nextState (s : ExteriorState) (hv : validState s) :
    validState (nextState s) := by
  exact ⟨sixPhase_next s.c hv.1, exterior_digit_bound s.c s.B hv.1 hv.2⟩

theorem valid_along_walk (s : Nat → ExteriorState) (n : Nat)
    (h0 : validState (s 0))
    (hs : ∀ i, i < n → s (i+1) = nextState (s i)) :
    ∀ i, i ≤ n → validState (s i) := by
  intro i
  induction i with
  | zero => intro _; exact h0
  | succ i ih =>
      intro hi
      rw [hs i (by omega)]
      exact valid_nextState (s i) (ih (by omega))

/-- A genuinely finite closed walk in the defined exterior map has count 0 mod 9.
The ordinary-integer factor bridge is the written argument in the companion note.
-/
theorem closed_exterior_count_mod9 (s : Nat → ExteriorState) (n : Nat)
    (hv : ∀ i, i < n → validState (s i))
    (hs : ∀ i, i < n → s (i+1) = nextState (s i))
    (hc : s n = s 0) :
    prefixCount (fun i => overflow (s i).c (s i).B) n % 9 = 0 := by
  apply closed_J_count_mod9 (fun i => stateJ (s i))
  · intro i hi
    have h := hv i hi
    rw [hs i hi]
    exact exterior_J_step (s i).c (s i).B h.1 h.2
  · rw [hc]


/-- The repeated coefficient and phase bounds follow from the initial state. -/
theorem closed_exterior_count_from_initial (s : Nat → ExteriorState) (n : Nat)
    (h0 : validState (s 0))
    (hs : ∀ i, i < n → s (i+1) = nextState (s i))
    (hc : s n = s 0) :
    prefixCount (fun i => overflow (s i).c (s i).B) n % 9 = 0 := by
  exact closed_exterior_count_mod9 s n
    (by intro i hi; exact valid_along_walk s n h0 hs i (by omega)) hs hc

def trajectory (s : ExteriorState) : Nat → ExteriorState
  | 0 => s
  | n + 1 => nextState (trajectory s n)

/-- A return of the explicitly iterated exterior map has overflow count divisible by nine. -/
theorem closed_trajectory_count_mod9 (s : ExteriorState) (n : Nat)
    (hv : validState s) (hr : trajectory s n = s) :
    prefixCount (fun i => overflow (trajectory s i).c (trajectory s i).B) n % 9 = 0 := by
  exact closed_exterior_count_from_initial (trajectory s) n hv
    (by intro i _; rfl) hr

/-- Arithmetic consequences of the separately stated full-interface bridge. -/
theorem full_return_arithmetic (H p dg dh : Int)
    (hcharge : H % 9 = 0) (hwidth : 2*(dg+dh) = H)
    (hpositive : 0 < H) (hrate : 2*H ≤ p)
    (hdifference : (dg-dh) % 9 = 0) :
    H % 18 = 0 ∧ 18 ≤ H ∧ 36 ≤ p ∧ dg % 9 = 0 ∧ dh % 9 = 0 := by
  omega

theorem minimum_gain_cases (dg dh : Int)
    (hg : 0 ≤ dg) (hh : 0 ≤ dh) (hwidth : dg + dh = 9)
    (hgm : dg % 9 = 0) (hhm : dh % 9 = 0) :
    (dg = 9 ∧ dh = 0) ∨ (dg = 0 ∧ dh = 9) := by omega


#print axioms sum_append
#print axioms sum_reverse
#print axioms sum_zipWith_add
#print axioms normalize_length
#print axioms normalize_carry_bit
#print axioms normalize_sum_mod9
#print axioms rawExterior_length
#print axioms phase_mod9
#print axioms raw_sum_nooverflow
#print axioms raw_sum_overflow
#print axioms charge_nil
#print axioms charge_cons
#print axioms charge_trimSuffix
#print axioms raw_charge_mod9
#print axioms exterior_charge_mod9
#print axioms sixPhase_next
#print axioms J_step
#print axioms exterior_J_step
#print axioms J_telescope
#print axioms closed_J_count_mod9
#print axioms normalize_digit_bound
#print axioms zip_digit_bound
#print axioms trimSuffix_mem
#print axioms exterior_digit_bound
#print axioms valid_nextState
#print axioms valid_along_walk
#print axioms closed_exterior_count_mod9
#print axioms closed_exterior_count_from_initial
#print axioms closed_trajectory_count_mod9
#print axioms full_return_arithmetic
#print axioms minimum_gain_cases

end Agent2Exterior
