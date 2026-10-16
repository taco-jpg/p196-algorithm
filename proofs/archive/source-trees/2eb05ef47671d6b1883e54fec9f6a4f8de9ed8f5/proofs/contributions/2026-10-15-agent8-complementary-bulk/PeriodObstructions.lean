import Std

/-!
Agent #8: exact leading-pair potentials, digit-mass congruence, and arithmetic
obstructions for the complementary two-gap quotient. Core Lean 4.19.0 only.
The final quotient interpretation is stated separately in the accompanying
written proof; every premise of the formal arithmetic wrappers is explicit.
-/

namespace Agent8

abbrev Word := List Nat

def mass : Word → Int
  | [] => 0
  | x :: xs => (x : Int) + mass xs

def zipAdd : Word → Word → Word
  | x :: xs, y :: ys => (x + y) :: zipAdd xs ys
  | _, _ => []

def pair (w : Word) : Word := zipAdd w w.reverse

def normalize : Word → Nat → Word
  | [], e => if e = 0 then [] else [e]
  | x :: xs, e => ((x + e) % 10) :: normalize xs ((x + e) / 10)

def stepWord (w : Word) : Word := pair (normalize w 0)

def orbit (w : Word) : Nat → Word
  | 0 => w
  | n + 1 => stepWord (orbit w n)

theorem mass_append (a b : Word) : mass (a ++ b) = mass a + mass b := by
  induction a with
  | nil => simp [mass]
  | cons x xs ih => simp [mass, ih, Int.add_assoc]

theorem mass_reverse (a : Word) : mass a.reverse = mass a := by
  induction a with
  | nil => rfl
  | cons x xs ih =>
    simp [List.reverse_cons, mass_append, mass, ih, Int.add_comm]

theorem mass_zipAdd (a b : Word) (hlen : a.length = b.length) :
    mass (zipAdd a b) = mass a + mass b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons y ys => simp at hlen
  | cons x xs ih =>
    cases b with
    | nil => simp at hlen
    | cons y ys =>
      have hlen' : xs.length = ys.length := by simpa using hlen
      have h := ih ys hlen'
      simp only [zipAdd, mass, Int.natCast_add]
      omega

theorem mass_pair (a : Word) : mass (pair a) = 2 * mass a := by
  have h := mass_zipAdd a a.reverse (by simp)
  simp only [pair, mass_reverse] at *
  omega

theorem normalize_mass_mod (a : Word) (e : Nat) :
    mass (normalize a e) % 9 = (mass a + (e : Int)) % 9 := by
  induction a generalizing e with
  | nil =>
    simp only [normalize, mass]
    split <;> simp_all [mass]
  | cons x xs ih =>
    have h := ih ((x + e) / 10)
    have hdiv := Nat.mod_add_div (x + e) 10
    simp only [normalize, mass]
    omega

theorem step_mass_mod (a : Word) :
    mass (stepWord a) % 9 = (2 * mass a) % 9 := by
  have h := normalize_mass_mod a 0
  simp only [stepWord, mass_pair]
  omega

theorem six_steps_mass_mod (a : Word) :
    mass (orbit a 6) % 9 = mass a % 9 := by
  have h0 := step_mass_mod (orbit a 0)
  have h1 := step_mass_mod (orbit a 1)
  have h2 := step_mass_mod (orbit a 2)
  have h3 := step_mass_mod (orbit a 3)
  have h4 := step_mass_mod (orbit a 4)
  have h5 := step_mass_mod (orbit a 5)
  change mass (orbit a 1) % 9 = (2 * mass a) % 9 at h0
  change mass (orbit a 2) % 9 = (2 * mass (orbit a 1)) % 9 at h1
  change mass (orbit a 3) % 9 = (2 * mass (orbit a 2)) % 9 at h2
  change mass (orbit a 4) % 9 = (2 * mass (orbit a 3)) % 9 at h3
  change mass (orbit a 5) % 9 = (2 * mass (orbit a 4)) % 9 at h4
  change mass (orbit a 6) % 9 = (2 * mass (orbit a 5)) % 9 at h5
  omega

theorem orbit_add (a : Word) (m n : Nat) :
    orbit a (m + n) = orbit (orbit a m) n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change stepWord (orbit a (m + n)) = stepWord (orbit (orbit a m) n)
    exact congrArg stepWord ih

theorem six_multiple_mass_mod (a : Word) (k : Nat) :
    mass (orbit a (6 * k)) % 9 = mass a % 9 := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Nat.mul_succ, orbit_add]
    exact (six_steps_mass_mod (orbit a (6 * k))).trans ih

def template (c : Nat) (B A C : Word) (g h : Nat) : Word :=
  B ++ List.replicate g c ++ A ++ List.replicate h (18 - c) ++ C ++
    List.replicate h (18 - c) ++ A.reverse ++ List.replicate g c ++ B.reverse

def SixPhase (c : Nat) : Prop :=
  c = 2 ∨ c = 4 ∨ c = 8 ∨ c = 16 ∨ c = 14 ∨ c = 10

theorem mass_replicate (g c : Nat) :
    mass (List.replicate g c) = (g : Int) * (c : Int) := by
  induction g with
  | zero => simp [mass]
  | succ g ih =>
    simp [List.replicate_succ, mass, ih, Int.add_mul, Int.add_comm]

theorem template_mass (c : Nat) (B A C : Word) (g h : Nat) :
    mass (template c B A C g h) =
      2 * mass B + 2 * mass A + mass C +
      2 * ((g : Int) * (c : Int)) +
      2 * ((h : Int) * ((18 - c : Nat) : Int)) := by
  simp only [template, mass_append, mass_reverse, mass_replicate]
  omega

theorem returned_template_mass_congruence (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 k : Nat) (hc : SixPhase c)
    (hreturn : orbit (template c B A C g0 h0) (6 * k) =
      template c B A C g1 h1) :
    (((g1 : Int) - (g0 : Int)) - ((h1 : Int) - (h0 : Int))) % 9 = 0 := by
  have hm := six_multiple_mass_mod (template c B A C g0 h0) k
  rw [hreturn, template_mass, template_mass] at hm
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl <;> omega

-- p is the positive first/last mirrored coefficient; e is the carry entering
-- the final column. This is exactly the actual exterior formula, not a freely
-- chosen new exterior. The whole-word interpretation is in the written bridge.
def overflow (p e : Nat) : Nat := if p + e < 10 then 0 else 1

def nextExterior (p e : Nat) : Nat :=
  if p + e < 10 then 2 * p + e else p % 10 + 1

def upperPotential : Nat → Int
  | 4 | 6 | 7 | 8 | 10 | 11 | 12 | 14 => 1
  | 9 | 13 | 15 | 16 | 17 => 2
  | 18 => 3
  | _ => 0

def lowerPotential : Nat → Int
  | 1 => 4
  | 2 => 3
  | 3 | 4 | 5 => 2
  | 6 | 7 | 8 | 9 | 10 => 1
  | _ => 0

theorem finite_exterior_certificate :
    ∀ p : Fin 19, ∀ e : Fin 2, 0 < p.val →
      0 < nextExterior p.val e.val ∧ nextExterior p.val e.val ≤ 18 ∧
      2 * (overflow p.val e.val : Int) ≤
        1 + upperPotential p.val - upperPotential (nextExterior p.val e.val) ∧
      1 ≤ 4 * (overflow p.val e.val : Int) +
        lowerPotential p.val - lowerPotential (nextExterior p.val e.val) := by
  decide

theorem exterior_bounds (p e : Nat) (hp : 0 < p) (hp18 : p ≤ 18)
    (he : e ≤ 1) :
    2 * (overflow p e : Int) ≤
      1 + upperPotential p - upperPotential (nextExterior p e) ∧
    1 ≤ 4 * (overflow p e : Int) +
      lowerPotential p - lowerPotential (nextExterior p e) := by
  have h := finite_exterior_certificate ⟨p, by omega⟩ ⟨e, by omega⟩ hp
  exact h.2.2

def total (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => total f n + f n

theorem path_potential_bounds (p e : Nat → Nat) (n : Nat)
    (valid : ∀ i, i < n → 0 < p i ∧ p i ≤ 18 ∧ e i ≤ 1)
    (evolves : ∀ i, i < n → p (i + 1) = nextExterior (p i) (e i)) :
    2 * total (fun i => (overflow (p i) (e i) : Int)) n ≤
      (n : Int) + upperPotential (p 0) - upperPotential (p n) ∧
    (n : Int) ≤ 4 * total (fun i => (overflow (p i) (e i) : Int)) n +
      lowerPotential (p 0) - lowerPotential (p n) := by
  induction n with
  | zero => simp [total]
  | succ n ih =>
    have hprev := ih (by intro i hi; exact valid i (by omega))
      (by intro i hi; exact evolves i (by omega))
    have hv := valid n (by omega)
    have heq := evolves n (by omega)
    have hb := exterior_bounds (p n) (e n) hv.1 hv.2.1 hv.2.2
    rw [← heq] at hb
    simp only [total]
    omega

theorem closed_path_bounds (p e : Nat → Nat) (n : Nat)
    (valid : ∀ i, i < n → 0 < p i ∧ p i ≤ 18 ∧ e i ≤ 1)
    (evolves : ∀ i, i < n → p (i + 1) = nextExterior (p i) (e i))
    (closed : p n = p 0) :
    (n : Int) ≤ 4 * total (fun i => (overflow (p i) (e i) : Int)) n ∧
    2 * total (fun i => (overflow (p i) (e i) : Int)) n ≤ (n : Int) := by
  have h := path_potential_bounds p e n valid evolves
  rw [closed] at h
  omega

-- The following results explicitly assume the returned-interface width law.
-- They do not assume that a cycle exists.
theorem returned_period_at_least_four (P H dg dh : Int)
    (hP : 0 < P) (hLower : P ≤ 4 * H) (hUpper : 2 * H ≤ P)
    (hWidth : H = 2 * (dg + dh)) : 4 ≤ P := by
  omega

theorem no_two_step_return (H dg dh : Int)
    (hLower : 2 ≤ 4 * H) (hUpper : 2 * H ≤ 2)
    (hWidth : H = 2 * (dg + dh)) : False := by
  omega

theorem six_step_forced_loss (H dg dh : Int)
    (hLower : 6 ≤ 4 * H) (hUpper : 2 * H ≤ 6)
    (hWidth : H = 2 * (dg + dh)) (hMass : (dg - dh) % 9 = 0) :
    H = 2 ∧ dg + dh = 1 ∧ (dg ≤ -4 ∨ dh ≤ -4) := by
  omega

theorem no_repeatable_six_step_return (H dg dh : Int)
    (hLower : 6 ≤ 4 * H) (hUpper : 2 * H ≤ 6)
    (hWidth : H = 2 * (dg + dh)) (hMass : (dg - dh) % 9 = 0)
    (hg : 0 ≤ dg) (hh : 0 ≤ dh) : False := by
  have h := six_step_forced_loss H dg dh hLower hUpper hWidth hMass
  omega

theorem short_return_equal_gains (P H dg dh : Int)
    (hP : P < 36) (hUpper : 2 * H ≤ P)
    (hWidth : H = 2 * (dg + dh)) (hMass : (dg - dh) % 9 = 0)
    (hg : 0 ≤ dg) (hh : 0 ≤ dh) : dg = dh ∧ H = 4 * dg := by
  omega

theorem twelve_step_gains (H dg dh : Int)
    (hLower : 12 ≤ 4 * H) (hUpper : 2 * H ≤ 12)
    (hWidth : H = 2 * (dg + dh)) (hMass : (dg - dh) % 9 = 0)
    (hg : 0 ≤ dg) (hh : 0 ≤ dh) : H = 4 ∧ dg = 1 ∧ dh = 1 := by
  have h := short_return_equal_gains 12 H dg dh (by decide) hUpper hWidth hMass hg hh
  omega

theorem eighteen_step_gains (H dg dh : Int)
    (hLower : 18 ≤ 4 * H) (hUpper : 2 * H ≤ 18)
    (hWidth : H = 2 * (dg + dh)) (hMass : (dg - dh) % 9 = 0)
    (hg : 0 ≤ dg) (hh : 0 ≤ dh) : H = 8 ∧ dg = 2 ∧ dh = 2 := by
  have h := short_return_equal_gains 18 H dg dh (by decide) hUpper hWidth hMass hg hh
  omega

theorem no_repeatable_six_step_template_return (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hc : SixPhase c)
    (p e : Nat → Nat)
    (valid : ∀ i, i < 6 → 0 < p i ∧ p i ≤ 18 ∧ e i ≤ 1)
    (evolves : ∀ i, i < 6 → p (i + 1) = nextExterior (p i) (e i))
    (closed : p 6 = p 0)
    (hreturn : orbit (template c B A C g0 h0) 6 = template c B A C g1 h1)
    (hWidth : total (fun i => (overflow (p i) (e i) : Int)) 6 =
      2 * (((g1 : Int) - (g0 : Int)) + ((h1 : Int) - (h0 : Int))))
    (hg : g0 ≤ g1) (hh : h0 ≤ h1) : False := by
  have hb := closed_path_bounds p e 6 valid evolves closed
  have hm := returned_template_mass_congruence c B A C g0 h0 g1 h1 1 hc hreturn
  exact no_repeatable_six_step_return _ _ _ hb.1 hb.2 hWidth hm (by omega) (by omega)

#print axioms mass_append
#print axioms mass_reverse
#print axioms mass_zipAdd
#print axioms mass_pair
#print axioms normalize_mass_mod
#print axioms step_mass_mod
#print axioms six_steps_mass_mod
#print axioms orbit_add
#print axioms six_multiple_mass_mod
#print axioms mass_replicate
#print axioms template_mass
#print axioms returned_template_mass_congruence
#print axioms finite_exterior_certificate
#print axioms exterior_bounds
#print axioms path_potential_bounds
#print axioms closed_path_bounds
#print axioms returned_period_at_least_four
#print axioms no_two_step_return
#print axioms six_step_forced_loss
#print axioms no_repeatable_six_step_return
#print axioms short_return_equal_gains
#print axioms twelve_step_gains
#print axioms eighteen_step_gains
#print axioms no_repeatable_six_step_template_return

end Agent8
