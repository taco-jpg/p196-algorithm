import Std

namespace P196.Agent5

abbrev Word := List Int

def normalize : Word → Int → Word × Int
  | [], carry => ([], carry)
  | x :: xs, carry =>
    let tail := normalize xs ((x + carry) / 10)
    ((x + carry) % 10 :: tail.1, tail.2)

theorem normalize_length (w : Word) (e : Int) :
    (normalize w e).1.length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [normalize, ih]

theorem normalize_mod9 (w : Word) (e : Int) :
    ((normalize w e).1.sum + (normalize w e).2) % 9 =
      (w.sum + e) % 9 := by
  induction w generalizing e with
  | nil => simp [normalize]
  | cons x xs ih =>
    have h := ih ((x + e) / 10)
    have div := Int.emod_add_ediv (x + e) 10
    simp only [normalize, List.sum_cons]
    omega

theorem sum_append (a b : Word) : (a ++ b).sum = a.sum + b.sum := by
  induction a with
  | nil => simp
  | cons x xs ih =>
    simp only [List.cons_append, List.sum_cons, ih]
    omega

theorem sum_reverse (w : Word) : w.reverse.sum = w.sum := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    simp [List.reverse_cons, sum_append, ih]
    omega

theorem sum_zip_add (a b : Word) (h : a.length = b.length) :
    (List.zipWith (· + ·) a b).sum = a.sum + b.sum := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons y ys => simp at h
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      have hlen : xs.length = ys.length := by simpa using h
      have hind := ih ys hlen
      simp only [List.zipWith_cons_cons, List.sum_cons]
      omega

def mass (c : Int) (w : Word) : Int := w.sum - c * (w.length : Int)

def stripPrefix (c : Int) : Word → Word × Nat
  | [] => ([], 0)
  | x :: xs =>
    if x = c then
      let tail := stripPrefix c xs
      (tail.1, tail.2 + 1)
    else (x :: xs, 0)

def stripSuffix (c : Int) (w : Word) : Word × Nat :=
  let t := stripPrefix c w.reverse
  (t.1.reverse, t.2)

theorem mass_stripPrefix (c : Int) (w : Word) :
    mass c (stripPrefix c w).1 = mass c w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    simp only [stripPrefix]
    split
    next h =>
      subst x
      simp only [mass, List.sum_cons, List.length_cons, Int.natCast_add,
        Int.natCast_one, Int.mul_add, Int.mul_one] at *
      omega
    next h => rfl

theorem mass_reverse (c : Int) (w : Word) : mass c w.reverse = mass c w := by
  simp [mass, sum_reverse]

theorem mass_stripSuffix (c : Int) (w : Word) :
    mass c (stripSuffix c w).1 = mass c w := by
  simp only [stripSuffix, mass_reverse, mass_stripPrefix]

def bulkCarry (c : Int) : Int := if 10 ≤ c then 1 else 0

def nextPhase (c : Int) : Int := 2 * (c - 9 * bulkCarry c)

def exteriorOverflow (c : Int) (B : Word) : Int :=
  (normalize B.reverse (bulkCarry c)).2

def rawExterior (c : Int) (B : Word) : Word :=
  let low := normalize B 0
  let high := normalize B.reverse (bulkCarry c)
  let u := c + low.2 - 10 * bulkCarry c
  if high.2 = 0 then
    List.zipWith (· + ·) (low.1 ++ [u])
      (high.1.reverse ++ [c - 9 * bulkCarry c])
  else
    List.zipWith (· + ·) (low.1 ++ [u]) (1 :: high.1.reverse)

def nextExterior (c : Int) (B : Word) : Word :=
  (stripSuffix (nextPhase c) (rawExterior c B)).1

theorem normalize_carry_bit (w : Word) (e : Int)
    (hw : ∀ x ∈ w, 0 ≤ x ∧ x ≤ 18) (he : 0 ≤ e ∧ e ≤ 1) :
    0 ≤ (normalize w e).2 ∧ (normalize w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => simpa [normalize] using he
  | cons x xs ih =>
    have hx := hw x (by simp)
    have he' : 0 ≤ (x + e) / 10 ∧ (x + e) / 10 ≤ 1 := by omega
    have hxs : ∀ y ∈ xs, 0 ≤ y ∧ y ≤ 18 := by
      intro y hy
      exact hw y (by simp [hy])
    exact ih ((x + e) / 10) hxs he'

theorem rawExterior_length (c : Int) (B : Word) :
    (rawExterior c B).length = B.length + 1 := by
  simp only [rawExterior]
  split <;> simp [normalize_length, List.length_zipWith]

theorem rawExterior_sum_mod9 (c : Int) (B : Word)
    (hg : exteriorOverflow c B = 0 ∨ exteriorOverflow c B = 1) :
    (rawExterior c B).sum % 9 =
      (2 * B.sum + (2 - exteriorOverflow c B) * c) % 9 := by
  have hl := normalize_mod9 B 0
  have hh := normalize_mod9 B.reverse (bulkCarry c)
  rw [sum_reverse] at hh
  have hn1 := normalize_length B 0
  have hn2 := normalize_length B.reverse (bulkCarry c)
  simp only [List.length_reverse] at hn2
  cases hg with
  | inl hg =>
    simp only [exteriorOverflow] at hg
    simp only [rawExterior, hg, if_true]
    rw [sum_zip_add]
    · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil,
        Int.add_zero]
      simp only [exteriorOverflow, hg]
      omega
    · simp [hn1, hn2]
  | inr hg =>
    simp only [exteriorOverflow] at hg
    simp only [rawExterior, hg]
    simp only [show (1 : Int) ≠ 0 by decide, if_false]
    rw [sum_zip_add]
    · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil,
        Int.add_zero]
      simp only [exteriorOverflow, hg]
      omega
    · simp [hn1, hn2]

theorem scalar_mass_congruence (c k S R b g : Int)
    (h : R % 9 = (2 * S + (2 - g) * c) % 9) :
    (R - (2 * (c - 9 * k)) * (b + 1)) % 9 =
      (2 * (S - c * b) - g * c) % 9 := by
  simp only [Int.sub_mul, Int.mul_add, Int.mul_sub, Int.mul_one,
    Int.mul_assoc] at *
  omega

theorem exterior_mass_step (c : Int) (B : Word)
    (hg : exteriorOverflow c B = 0 ∨ exteriorOverflow c B = 1) :
    mass (nextPhase c) (nextExterior c B) % 9 =
      (2 * mass c B - exteriorOverflow c B * c) % 9 := by
  have hs := rawExterior_sum_mod9 c B hg
  have hm := scalar_mass_congruence c (bulkCarry c) B.sum
    (rawExterior c B).sum (B.length : Int) (exteriorOverflow c B) hs
  unfold nextExterior
  rw [mass_stripSuffix]
  simpa [mass, rawExterior_length, nextPhase, Int.natCast_add] using hm

theorem exterior_overflow_bit (c : Int) (B : Word)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 18) :
    exteriorOverflow c B = 0 ∨ exteriorOverflow c B = 1 := by
  have hb : 0 ≤ bulkCarry c ∧ bulkCarry c ≤ 1 := by
    unfold bulkCarry
    split <;> omega
  have hr : ∀ x ∈ B.reverse, 0 ≤ x ∧ x ≤ 18 := by
    intro x hx
    exact hB x (by simpa using hx)
  have h := normalize_carry_bit B.reverse (bulkCarry c) hr hb
  simp only [exteriorOverflow]
  omega

theorem exterior_mass_step_bounded (c : Int) (B : Word)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 18) :
    mass (nextPhase c) (nextExterior c B) % 9 =
      (2 * mass c B - exteriorOverflow c B * c) % 9 :=
  exterior_mass_step c B (exterior_overflow_bit c B hB)

def UnitPhase (c : Int) : Prop :=
  c = 2 ∨ c = 4 ∨ c = 8 ∨ c = 16 ∨ c = 14 ∨ c = 10

def clockMultiplier (c : Int) : Int :=
  if c = 2 then 1 else if c = 4 then 5 else if c = 8 then 7
  else if c = 16 then 8 else if c = 14 then 4 else if c = 10 then 2 else 0

def residueClock (c : Int) (B : Word) : Int :=
  (clockMultiplier c * mass c B) % 9

theorem unitPhase_next (c : Int) (hc : UnitPhase c) : UnitPhase (nextPhase c) := by
  rcases hc with h | h | h | h | h | h <;> subst c <;>
    simp [UnitPhase, nextPhase, bulkCarry]

theorem scalar_clock_step (c m m' g : Int) (hc : UnitPhase c)
    (hm : m' % 9 = (2 * m - g * c) % 9) :
    (clockMultiplier (nextPhase c) * m' + g) % 9 =
      (clockMultiplier c * m) % 9 := by
  rcases hc with h | h | h | h | h | h <;> subst c <;>
    simp [nextPhase, bulkCarry, clockMultiplier] at * <;> omega

theorem exterior_clock_step (c : Int) (B : Word) (hc : UnitPhase c)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 18) :
    (residueClock (nextPhase c) (nextExterior c B) + exteriorOverflow c B) % 9 =
      residueClock c B := by
  have h := scalar_clock_step c (mass c B)
    (mass (nextPhase c) (nextExterior c B)) (exteriorOverflow c B) hc
    (exterior_mass_step_bounded c B hB)
  simp only [residueClock]
  omega

def prefixSum (g : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => prefixSum g n + g n

theorem clock_telescopes (r g : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → (r (i + 1) + g i) % 9 = r i % 9) :
    (r n + prefixSum g n) % 9 = r 0 % 9 := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [prefixSum]
    omega

theorem closed_clock_mod9 (r g : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → (r (i + 1) + g i) % 9 = r i % 9)
    (hc : r n = r 0) : prefixSum g n % 9 = 0 := by
  have ht := clock_telescopes r g n h
  omega

theorem unitPhase_along (c : Nat → Int) (n : Nat) (hc : UnitPhase (c 0))
    (hstep : ∀ i, i < n → c (i + 1) = nextPhase (c i)) : UnitPhase (c n) := by
  induction n with
  | zero => exact hc
  | succ n ih =>
    have hp := ih (fun i hi => hstep i (by omega))
    rw [hstep n (by omega)]
    exact unitPhase_next (c n) hp

theorem exterior_path_mod9 (c : Nat → Int) (B : Nat → Word) (n : Nat)
    (hc : UnitPhase (c 0))
    (hB : ∀ i, i < n → ∀ x ∈ B i, 0 ≤ x ∧ x ≤ 18)
    (hstep : ∀ i, i < n → c (i + 1) = nextPhase (c i) ∧
      B (i + 1) = nextExterior (c i) (B i))
    (closeC : c n = c 0) (closeB : B n = B 0) :
    prefixSum (fun i => exteriorOverflow (c i) (B i)) n % 9 = 0 := by
  apply closed_clock_mod9 (fun i => residueClock (c i) (B i))
  · intro i hi
    have hphase := unitPhase_along c i hc (fun j hj => (hstep j (by omega)).1)
    rw [(hstep i hi).1, (hstep i hi).2]
    simpa [residueClock] using exterior_clock_step (c i) (B i) hphase (hB i hi)
  · simp [closeC, closeB]

def outerOverflow (p e : Nat) : Nat := (p + e) / 10

def outerNext (p e : Nat) : Nat :=
  if p + e < 10 then 2 * p + e else p % 10 + 1

def upperPotential (p : Nat) : Nat :=
  if p = 1 then 0 else if p ≤ 3 then 1 else if p = 10 then 1
  else if p ≤ 9 then 2 else 3

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem outer_budget_table : ∀ p : Fin 19, ∀ e : Fin 2, 0 < p.val →
    2 * outerOverflow p.val e.val + upperPotential (outerNext p.val e.val) ≤
      1 + upperPotential p.val := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem outer_progress_table : ∀ p : Fin 19, ∀ e : Fin 2, 0 < p.val →
    p.val + 1 ≤ outerNext p.val e.val + 10 * outerOverflow p.val e.val := by decide

theorem outer_budget (p e : Nat) (hp : 0 < p ∧ p ≤ 18) (he : e ≤ 1) :
    2 * outerOverflow p e + upperPotential (outerNext p e) ≤ 1 + upperPotential p := by
  exact outer_budget_table ⟨p, by omega⟩ ⟨e, by omega⟩ hp.1

theorem outer_progress (p e : Nat) (hp : 0 < p ∧ p ≤ 18) (he : e ≤ 1) :
    p + 1 ≤ outerNext p e + 10 * outerOverflow p e := by
  exact outer_progress_table ⟨p, by omega⟩ ⟨e, by omega⟩ hp.1

theorem budget_telescopes (psi g : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → 2 * g i + psi (i + 1) ≤ 1 + psi i) :
    2 * prefixSum g n + psi n ≤ (n : Int) + psi 0 := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [prefixSum, Int.natCast_succ]
    omega

theorem progress_telescopes (p g : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → p i + 1 ≤ p (i + 1) + 10 * g i) :
    p 0 + (n : Int) ≤ p n + 10 * prefixSum g n := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    simp only [prefixSum, Int.natCast_succ]
    omega

theorem full_cycle_numeric_bound (period overflows : Int)
    (hpos : 0 < overflows) (h9 : overflows % 9 = 0)
    (h2 : overflows % 2 = 0) (hbudget : 2 * overflows ≤ period) :
    18 ≤ overflows ∧ 36 ≤ period := by omega

theorem closed_path_obstruction (r p psi g : Nat → Int) (n : Nat)
    (hn : 0 < n)
    (hr : ∀ i, i < n → (r (i + 1) + g i) % 9 = r i % 9)
    (hb : ∀ i, i < n → 2 * g i + psi (i + 1) ≤ 1 + psi i)
    (hp : ∀ i, i < n → p i + 1 ≤ p (i + 1) + 10 * g i)
    (cr : r n = r 0) (cb : psi n = psi 0) (cp : p n = p 0)
    (heven : prefixSum g n % 2 = 0) :
    18 ≤ prefixSum g n ∧ 36 ≤ n := by
  have h9 := closed_clock_mod9 r g n hr cr
  have hbudget := budget_telescopes psi g n hb
  have hprogress := progress_telescopes p g n hp
  have hpos : 0 < prefixSum g n := by omega
  have hbound : 2 * prefixSum g n ≤ (n : Int) := by omega
  have h := full_cycle_numeric_bound (n : Int) (prefixSum g n) hpos h9 heven hbound
  omega

#print axioms normalize_length
#print axioms normalize_mod9
#print axioms sum_append
#print axioms sum_reverse
#print axioms sum_zip_add
#print axioms mass_stripPrefix
#print axioms mass_reverse
#print axioms mass_stripSuffix
#print axioms normalize_carry_bit
#print axioms rawExterior_length
#print axioms rawExterior_sum_mod9
#print axioms scalar_mass_congruence
#print axioms exterior_mass_step
#print axioms exterior_overflow_bit
#print axioms exterior_mass_step_bounded
#print axioms unitPhase_next
#print axioms scalar_clock_step
#print axioms exterior_clock_step
#print axioms clock_telescopes
#print axioms closed_clock_mod9
#print axioms unitPhase_along
#print axioms exterior_path_mod9
#print axioms outer_budget_table
#print axioms outer_progress_table
#print axioms outer_budget
#print axioms outer_progress
#print axioms budget_telescopes
#print axioms progress_telescopes
#print axioms full_cycle_numeric_bound
#print axioms closed_path_obstruction

end P196.Agent5
