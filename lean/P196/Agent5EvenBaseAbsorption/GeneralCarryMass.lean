import P196.Agent5EvenBaseAbsorption.ExteriorClock

namespace P196.Agent5.General

/-- The base is m+1; m is the neutral coefficient. -/
def normalize (m : Int) : Word → Int → Word × Int
  | [], carry => ([], carry)
  | x :: xs, carry =>
    let tail := normalize m xs ((x + carry) / (m + 1))
    ((x + carry) % (m + 1) :: tail.1, tail.2)

/-- Sum of every outgoing carry, including the final one. -/
def carrySum (m : Int) : Word → Int → Int
  | [], _ => 0
  | x :: xs, carry =>
    let q := (x + carry) / (m + 1)
    q + carrySum m xs q

theorem normalize_length (m : Int) (w : Word) (e : Int) :
    (normalize m w e).1.length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [normalize, ih]

theorem normalize_mass_exact (m : Int) (w : Word) (e : Int) :
    (normalize m w e).1.sum + (normalize m w e).2 =
      w.sum + e - m * carrySum m w e := by
  induction w generalizing e with
  | nil => simp [normalize, carrySum]
  | cons x xs ih =>
    have ht := ih ((x + e) / (m + 1))
    have hd := Int.emod_add_ediv (x + e) (m + 1)
    simp only [Int.add_mul, Int.one_mul] at hd
    simp only [normalize, carrySum, List.sum_cons, Int.mul_add]
    omega

def bulkCarry (m c : Int) : Int := if m + 1 ≤ c then 1 else 0

def nextPhase (m c : Int) : Int := 2 * (c - m * bulkCarry m c)

def exteriorOverflow (m c : Int) (B : Word) : Int :=
  (normalize m B.reverse (bulkCarry m c)).2

def rawExterior (m c : Int) (B : Word) : Word :=
  let low := normalize m B 0
  let high := normalize m B.reverse (bulkCarry m c)
  let u := c + low.2 - (m + 1) * bulkCarry m c
  if high.2 = 0 then
    List.zipWith (· + ·) (low.1 ++ [u])
      (high.1.reverse ++ [c - m * bulkCarry m c])
  else
    List.zipWith (· + ·) (low.1 ++ [u]) (1 :: high.1.reverse)

def nextExterior (m c : Int) (B : Word) : Word :=
  (stripSuffix (nextPhase m c) (rawExterior m c B)).1

def carryCorrection (m c : Int) (B : Word) : Int :=
  2 * bulkCarry m c * (B.length : Int) + exteriorOverflow m c B * bulkCarry m c
    - carrySum m B 0 - carrySum m B.reverse (bulkCarry m c)

theorem rawExterior_length (m c : Int) (B : Word) :
    (rawExterior m c B).length = B.length + 1 := by
  simp only [rawExterior]
  split <;> simp [normalize_length, List.length_zipWith]

theorem rawExterior_sum_exact (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 0 ∨ exteriorOverflow m c B = 1) :
    (rawExterior m c B).sum =
      2 * B.sum + (2 - exteriorOverflow m c B) * c -
        m * (carrySum m B 0 + carrySum m B.reverse (bulkCarry m c) +
          (2 - exteriorOverflow m c B) * bulkCarry m c) := by
  have hl := normalize_mass_exact m B 0
  have hh := normalize_mass_exact m B.reverse (bulkCarry m c)
  rw [sum_reverse] at hh
  have hn1 := normalize_length m B 0
  have hn2 := normalize_length m B.reverse (bulkCarry m c)
  simp only [List.length_reverse] at hn2
  cases hg with
  | inl hg =>
    simp only [exteriorOverflow] at hg
    simp only [rawExterior, hg, if_true]
    rw [sum_zip_add]
    · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil, Int.add_zero]
      simp only [exteriorOverflow, hg, Int.sub_zero, Int.add_mul, Int.mul_add,
        Int.one_mul, Int.mul_assoc, Int.mul_left_comm m 2] at *
      omega
    · simp [hn1, hn2]
  | inr hg =>
    simp only [exteriorOverflow] at hg
    simp only [rawExterior, hg]
    simp only [show (1 : Int) ≠ 0 by decide, if_false]
    rw [sum_zip_add]
    · simp only [sum_append, sum_reverse, List.sum_cons, List.sum_nil, Int.add_zero]
      simp only [exteriorOverflow, hg, show (2 : Int) - 1 = 1 by decide,
        Int.add_mul, Int.mul_add, Int.one_mul, Int.mul_assoc, Int.mul_left_comm m 2] at *
      omega
    · simp [hn1, hn2]

theorem exterior_mass_exact (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 0 ∨ exteriorOverflow m c B = 1) :
    mass (nextPhase m c) (nextExterior m c B) =
      2 * mass c B - exteriorOverflow m c B * c + m * carryCorrection m c B := by
  have hs := rawExterior_sum_exact m c B hg
  unfold nextExterior
  rw [mass_stripSuffix]
  simp only [mass, rawExterior_length, nextPhase, carryCorrection,
    Int.natCast_add, Int.natCast_one, Int.mul_add, Int.mul_sub, Int.add_mul,
    Int.sub_mul, Int.mul_one, Int.mul_assoc, Int.mul_left_comm m 2] at *
  omega

theorem exterior_mass_congruence (m c : Int) (B : Word)
    (hg : exteriorOverflow m c B = 0 ∨ exteriorOverflow m c B = 1) :
    mass (nextPhase m c) (nextExterior m c B) % m =
      (2 * mass c B - exteriorOverflow m c B * c) % m := by
  rw [exterior_mass_exact m c B hg]
  exact Int.add_mul_emod_self_left _ _ _

theorem next_carry_bit (m x e : Int) (hm : 1 ≤ m)
    (hx : 0 ≤ x ∧ x ≤ 2 * m) (he : 0 ≤ e ∧ e ≤ 1) :
    0 ≤ (x + e) / (m + 1) ∧ (x + e) / (m + 1) ≤ 1 := by
  have h0 := Int.ediv_nonneg (a := x + e) (b := m + 1) (by omega) (by omega)
  have h2 := Int.ediv_lt_of_lt_mul (a := x + e) (b := 2) (c := m + 1)
    (by omega) (by omega)
  omega

theorem normalize_carry_bit (m : Int) (w : Word) (e : Int) (hm : 1 ≤ m)
    (hw : ∀ x ∈ w, 0 ≤ x ∧ x ≤ 2 * m) (he : 0 ≤ e ∧ e ≤ 1) :
    0 ≤ (normalize m w e).2 ∧ (normalize m w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => simpa [normalize] using he
  | cons x xs ih =>
    have hx := hw x (by simp)
    have he' := next_carry_bit m x e hm hx he
    have hxs : ∀ y ∈ xs, 0 ≤ y ∧ y ≤ 2 * m := by
      intro y hy
      exact hw y (by simp [hy])
    exact ih ((x + e) / (m + 1)) hxs he'

theorem carrySum_bounds (m : Int) (w : Word) (e : Int) (hm : 1 ≤ m)
    (hw : ∀ x ∈ w, 0 ≤ x ∧ x ≤ 2 * m) (he : 0 ≤ e ∧ e ≤ 1) :
    0 ≤ carrySum m w e ∧ carrySum m w e ≤ (w.length : Int) := by
  induction w generalizing e with
  | nil => simp [carrySum]
  | cons x xs ih =>
    have hx := hw x (by simp)
    have he' := next_carry_bit m x e hm hx he
    have hxs : ∀ y ∈ xs, 0 ≤ y ∧ y ≤ 2 * m := by
      intro y hy
      exact hw y (by simp [hy])
    have ht := ih ((x + e) / (m + 1)) hxs he'
    simp only [carrySum, List.length_cons, Int.natCast_succ]
    omega

theorem exterior_overflow_bit (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m) :
    exteriorOverflow m c B = 0 ∨ exteriorOverflow m c B = 1 := by
  have hb : 0 ≤ bulkCarry m c ∧ bulkCarry m c ≤ 1 := by
    unfold bulkCarry
    split <;> omega
  have hr : ∀ x ∈ B.reverse, 0 ≤ x ∧ x ≤ 2 * m := by
    intro x hx
    exact hB x (by simpa using hx)
  have h := normalize_carry_bit m B.reverse (bulkCarry m c) hm hr hb
  simp only [exteriorOverflow]
  omega

theorem exterior_mass_exact_bounded (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m) :
    mass (nextPhase m c) (nextExterior m c B) =
      2 * mass c B - exteriorOverflow m c B * c + m * carryCorrection m c B :=
  exterior_mass_exact m c B (exterior_overflow_bit m c B hm hB)


theorem carryCorrection_low (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m) (hk : bulkCarry m c = 0) :
    -2 * (B.length : Int) ≤ carryCorrection m c B ∧ carryCorrection m c B ≤ 0 := by
  have hl := carrySum_bounds m B 0 hm hB (by omega)
  have hrange : ∀ x ∈ B.reverse, 0 ≤ x ∧ x ≤ 2 * m := by
    intro x hx
    exact hB x (by simpa using hx)
  have hh := carrySum_bounds m B.reverse 0 hm hrange (by omega)
  simp only [List.length_reverse] at hh
  simp only [carryCorrection, hk, Int.mul_zero, Int.zero_mul,
    Int.zero_add, Int.zero_sub]
  omega

theorem carryCorrection_high (m c : Int) (B : Word) (hm : 1 ≤ m)
    (hB : ∀ x ∈ B, 0 ≤ x ∧ x ≤ 2 * m) (hk : bulkCarry m c = 1) :
    exteriorOverflow m c B ≤ carryCorrection m c B ∧
      carryCorrection m c B ≤ 2 * (B.length : Int) + exteriorOverflow m c B := by
  have hl := carrySum_bounds m B 0 hm hB (by omega)
  have hrange : ∀ x ∈ B.reverse, 0 ≤ x ∧ x ≤ 2 * m := by
    intro x hx
    exact hB x (by simpa using hx)
  have hh := carrySum_bounds m B.reverse 1 hm hrange (by omega)
  simp only [List.length_reverse] at hh
  simp only [carryCorrection, hk, Int.mul_one]
  omega

def Cong (m a b : Int) : Prop := a % m = b % m

theorem Cong.refl (m a : Int) : Cong m a a := rfl

theorem Cong.symm {m a b : Int} (h : Cong m a b) : Cong m b a := Eq.symm h

theorem Cong.trans {m a b c : Int} (h : Cong m a b) (h' : Cong m b c) :
    Cong m a c := Eq.trans h h'

theorem Cong.add {m a b c d : Int} (h : Cong m a b) (h' : Cong m c d) :
    Cong m (a + c) (b + d) := by
  unfold Cong at *
  rw [Int.add_emod, Int.add_emod b, h, h']

theorem Cong.sub {m a b c d : Int} (h : Cong m a b) (h' : Cong m c d) :
    Cong m (a - c) (b - d) := by
  unfold Cong at *
  rw [Int.sub_emod, Int.sub_emod b, h, h']

theorem Cong.mul {m a b c d : Int} (h : Cong m a b) (h' : Cong m c d) :
    Cong m (a * c) (b * d) := by
  unfold Cong at *
  rw [Int.mul_emod, Int.mul_emod b, h, h']

theorem Cong.mul_left (m a b z : Int) (h : Cong m a b) :
    Cong m (z * a) (z * b) := (Cong.refl m z).mul h

theorem Cong.cancel_unit_left (m a b z zinv : Int) (h : Cong m (z * a) (z * b))
    (hu : Cong m (zinv * z) 1) : Cong m a b := by
  have hs := h.mul_left m _ _ zinv
  have ha := hu.mul (Cong.refl m a)
  have hb := hu.mul (Cong.refl m b)
  simp only [Int.mul_assoc, Int.one_mul] at ha hb
  exact ha.symm.trans (hs.trans hb)

def powTwo : Nat → Int
  | 0 => 1
  | n + 1 => 2 * powTwo n

theorem phase_path_congruence (m : Int) (c : Nat → Int) (n : Nat)
    (h : ∀ i, i < n → Cong m (c (i+1)) (2 * c i)) :
    Cong m (c n) (powTwo n * c 0) := by
  induction n with
  | zero => simp [powTwo, Cong]
  | succ n ih =>
    have hp := ih (fun i hi => h i (by omega))
    have hs := h n (by omega)
    have hm := hp.mul_left m _ _ 2
    simpa [powTwo, Int.mul_assoc] using hs.trans hm

theorem scaled_mass_path_congruence (m : Int) (c M g : Nat → Int) (n : Nat)
    (hc : ∀ i, i < n → Cong m (c (i+1)) (2 * c i))
    (hM : ∀ i, i < n → Cong m (M (i+1)) (2 * M i - g i * c i)) :
    Cong m (2 * M n + c n * prefixSum g n) (2 * powTwo n * M 0) := by
  induction n with
  | zero => simp [powTwo, prefixSum, Cong]
  | succ n ih =>
    have hp := ih (fun i hi => hc i (by omega)) (fun i hi => hM i (by omega))
    have hc' := hc n (by omega)
    have hM' := hM n (by omega)
    have hleft := (hM'.mul_left m _ _ 2).add
      (hc'.mul (Cong.refl m (prefixSum g (n+1))))
    have heq : 2 * (2 * M n - g n * c n) + (2 * c n) * prefixSum g (n+1) =
        2 * (2 * M n + c n * prefixSum g n) := by
      simp only [prefixSum, Int.mul_sub, Int.mul_add, Int.mul_assoc]
      rw [Int.mul_comm (g n) (c n)]
      omega
    rw [heq] at hleft
    have hright := hp.mul_left m _ _ 2
    simpa [powTwo, Int.mul_assoc] using hleft.trans hright


theorem general_closed_mass_congruence (m : Int) (c M g : Nat → Int) (n : Nat)
    (hc : ∀ i, i < n → Cong m (c (i+1)) (2 * c i))
    (hM : ∀ i, i < n → Cong m (M (i+1)) (2 * M i - g i * c i))
    (closeC : c n = c 0) (closeM : M n = M 0) :
    Cong m (c 0 * prefixSum g n) (2 * (powTwo n - 1) * M 0) := by
  have h := scaled_mass_path_congruence m c M g n hc hM
  rw [closeC, closeM] at h
  have hs := h.sub (Cong.refl m (2 * M 0))
  have hl : 2 * M 0 + c 0 * prefixSum g n - 2 * M 0 = c 0 * prefixSum g n := by omega
  have hr : 2 * powTwo n * M 0 - 2 * M 0 = 2 * (powTwo n - 1) * M 0 := by
    simp only [Int.mul_sub, Int.sub_mul, Int.mul_one, Int.one_mul]
  rwa [hl, hr] at hs

theorem general_unit_closed_overflow (m : Int) (c M g : Nat → Int) (n : Nat)
    (hc : ∀ i, i < n → Cong m (c (i+1)) (2 * c i))
    (hM : ∀ i, i < n → Cong m (M (i+1)) (2 * M i - g i * c i))
    (closeC : c n = c 0) (closeM : M n = M 0)
    (hu : ∃ inv : Int, Cong m (inv * c 0) 1) :
    prefixSum g n % m = 0 := by
  obtain ⟨inv, hinv⟩ := hu
  have hp := phase_path_congruence m c n hc
  rw [closeC] at hp
  have hp' : Cong m (c 0 * 1) (c 0 * powTwo n) := by
    simpa [Int.mul_comm] using hp
  have hpow := Cong.cancel_unit_left m 1 (powTwo n) (c 0) inv hp' hinv
  have hm := scaled_mass_path_congruence m c M g n hc hM
  rw [closeC, closeM] at hm
  have hpowmul := ((Cong.refl m 2).mul hpow.symm).mul (Cong.refl m (M 0))
  simp only [Int.mul_one] at hpowmul
  have hm' := hm.trans hpowmul
  have cancel := hm'.sub (Cong.refl m (2 * M 0))
  have heq1 : 2 * M 0 + c 0 * prefixSum g n - 2 * M 0 = c 0 * prefixSum g n := by omega
  rw [heq1, Int.sub_self] at cancel
  have hz : Cong m (c 0 * prefixSum g n) (c 0 * 0) := by simpa using cancel
  have done := Cong.cancel_unit_left m (prefixSum g n) 0 (c 0) inv hz hinv
  simpa [Cong] using done

theorem phase_step_congruence (m c : Int) : Cong m (nextPhase m c) (2 * c) := by
  unfold Cong nextPhase
  rw [Int.mul_sub]
  have heq : 2 * (m * bulkCarry m c) = m * (2 * bulkCarry m c) := by
    rw [Int.mul_left_comm]
  rw [heq, Int.sub_emod]
  simp

theorem general_exterior_closed_overflow (m : Int) (c : Nat → Int)
    (B : Nat → Word) (n : Nat) (hm : 1 ≤ m)
    (hB : ∀ i, i < n → ∀ x ∈ B i, 0 ≤ x ∧ x ≤ 2 * m)
    (hstep : ∀ i, i < n → c (i+1) = nextPhase m (c i) ∧
      B (i+1) = nextExterior m (c i) (B i))
    (closeC : c n = c 0) (closeB : B n = B 0)
    (hu : ∃ inv : Int, Cong m (inv * c 0) 1) :
    prefixSum (fun i => exteriorOverflow m (c i) (B i)) n % m = 0 := by
  apply general_unit_closed_overflow m c (fun i => mass (c i) (B i))
  · intro i hi
    rw [(hstep i hi).1]
    exact phase_step_congruence m (c i)
  · intro i hi
    rw [(hstep i hi).1, (hstep i hi).2]
    exact exterior_mass_congruence m (c i) (B i)
      (exterior_overflow_bit m (c i) (B i) hm (hB i hi))
  · exact closeC
  · simp [closeC, closeB]
  · exact hu

#print axioms normalize_length
#print axioms normalize_mass_exact
#print axioms rawExterior_length
#print axioms rawExterior_sum_exact
#print axioms exterior_mass_exact
#print axioms exterior_mass_congruence
#print axioms next_carry_bit
#print axioms normalize_carry_bit
#print axioms carrySum_bounds
#print axioms exterior_overflow_bit
#print axioms exterior_mass_exact_bounded
#print axioms carryCorrection_low
#print axioms carryCorrection_high
#print axioms Cong.refl
#print axioms Cong.symm
#print axioms Cong.trans
#print axioms Cong.add
#print axioms Cong.sub
#print axioms Cong.mul
#print axioms Cong.mul_left
#print axioms Cong.cancel_unit_left
#print axioms phase_path_congruence
#print axioms scaled_mass_path_congruence
#print axioms general_closed_mass_congruence
#print axioms general_unit_closed_overflow
#print axioms phase_step_congruence
#print axioms general_exterior_closed_overflow

end P196.Agent5.General
