import P196.Agent119EightFamilies.TemporalResidues

/-!
Finite arithmetic for perfect-power compatibility with the existing six
modulo-99 phases of the ordinary orbit of 196.  The phase function and the
general periodic reduction lemma are imported unchanged.

A root of one of these phases is a multiple of eleven and is not divisible
by three.  Its residue therefore lies in six classes whose positive
exponents have period six.  Exponents reduce to 1 through 6; the final finite table
counts roots, rather than asserting any visit of the integer orbit.
-/

set_option autoImplicit false

namespace P196.OrbitPowerResidues.Arithmetic

open Agent423.TemporalResidues

/-- The six possible residues of a root of an eventual 196 phase. -/
def RootClass (a : Nat) : Prop := a % 99 ∈ [11, 22, 44, 55, 77, 88]

/-- Positive representative of the exponent residue modulo six. -/
def positiveExponent (e : Nat) : Nat := (e - 1) % 6 + 1

/-- All distinct residue roots, retained in increasing numerical order. -/
def residueRoots (e t : Nat) : List Nat :=
  (List.range 99).filter (fun a => decide (a ^ e % 99 = phase196 t))

/-- Congruent bases have congruent powers, with no positivity hypotheses. -/
theorem power_congr (a b m e : Nat) (h : a % m = b % m) :
    a ^ e % m = b ^ e % m := by
  induction e with
  | zero => rfl
  | succ e ih =>
    calc
      a ^ (e + 1) % m = (a ^ e % m * (a % m)) % m := by
        rw [Nat.pow_succ]
        exact Nat.mul_mod _ _ _
      _ = (b ^ e % m * (b % m)) % m := by rw [ih, h]
      _ = b ^ (e + 1) % m := by
        rw [Nat.pow_succ]
        exact (Nat.mul_mod _ _ _).symm

theorem power_base_mod (a e m : Nat) :
    (a % m) ^ e % m = a ^ e % m :=
  power_congr (a % m) a m e (Nat.mod_mod a m)

private theorem phase_arithmetic (t : Nat) :
    phase196 t % 11 = 0 ∧ phase196 t % 3 ≠ 0 := by
  have h : ∀ j : Fin 6,
      phase196 j.val % 11 = 0 ∧ phase196 j.val % 3 ≠ 0 := by
    decide +kernel
  simpa only [phase196, Nat.mod_mod] using
    h ⟨t % 6, Nat.mod_lt _ (by decide)⟩

private theorem gcd_eleven_of_nonzero (a : Nat) (ha : a % 11 ≠ 0) :
    Nat.gcd a 11 = 1 := by
  have h : ∀ r : Fin 11, r.val ≠ 0 → Nat.gcd r.val 11 = 1 := by
    decide +kernel
  calc
    Nat.gcd a 11 = Nat.gcd 11 a := Nat.gcd_comm a 11
    _ = Nat.gcd (a % 11) 11 := Nat.gcd_rec 11 a
    _ = 1 := h ⟨a % 11, Nat.mod_lt _ (by decide)⟩ ha

/-- A power matching an eventual phase has its base in the six root classes. -/
theorem root_class_of_power (a e t : Nat) (he : 0 < e)
    (hroot : a ^ e % 99 = phase196 t) : RootClass a := by
  have hp11 : a ^ e % 11 = 0 := by
    calc
      a ^ e % 11 = (a ^ e % 99) % 11 :=
        (Nat.mod_mod_of_dvd _ (by decide : 11 ∣ 99)).symm
      _ = phase196 t % 11 := congrArg (fun x => x % 11) hroot
      _ = 0 := (phase_arithmetic t).1
  have ha11 : a % 11 = 0 := by
    by_cases hz : a % 11 = 0
    · exact hz
    · have hg : Nat.gcd a 11 = 1 := gcd_eleven_of_nonzero a hz
      have hpow : Nat.gcd (a ^ e) 11 = 1 :=
        Nat.gcd_pow_left_of_gcd_eq_one hg
      have hd : 11 ∣ a ^ e := Nat.dvd_of_mod_eq_zero hp11
      have hzero : Nat.gcd (a ^ e) 11 = 11 := Nat.gcd_eq_right hd
      omega
  have ha3 : a % 3 ≠ 0 := by
    intro hz
    have hpow := power_base_mod a e 3
    rw [hz, Nat.zero_pow he, Nat.zero_mod] at hpow
    have hres : a ^ e % 3 = phase196 t % 3 := by
      have h := congrArg (fun x => x % 3) hroot
      simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 99)] using h
    exact (phase_arithmetic t).2 (hres.symm.trans hpow.symm)
  have hclasses : ∀ r : Fin 99,
      r.val % 11 = 0 → r.val % 3 ≠ 0 →
        r.val ∈ [11, 22, 44, 55, 77, 88] := by
    decide +kernel
  apply hclasses ⟨a % 99, Nat.mod_lt _ (by decide)⟩
  · simpa only [Nat.mod_mod_of_dvd _ (by decide : 11 ∣ 99)] using ha11
  · simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 99)] using ha3

theorem positiveExponent_bounds (e : Nat) :
    0 < positiveExponent e ∧ positiveExponent e ≤ 6 := by
  unfold positiveExponent
  omega

theorem positiveExponent_mod (e : Nat) (he : 0 < e) :
    positiveExponent e % 6 = e % 6 := by
  have hs : e - 1 + 1 = e := by omega
  calc
    positiveExponent e % 6 = (e - 1 + 1) % 6 := by
      simp only [positiveExponent, Nat.add_mod, Nat.mod_mod]
    _ = e % 6 := by rw [hs]

private theorem gcd_six_mod (e : Nat) :
    Nat.gcd e 6 = Nat.gcd (e % 6) 6 := by
  calc
    Nat.gcd e 6 = Nat.gcd 6 e := Nat.gcd_comm e 6
    _ = Nat.gcd (e % 6) 6 := Nat.gcd_rec 6 e

theorem positiveExponent_gcd (e : Nat) (he : 0 < e) :
    Nat.gcd (positiveExponent e) 6 = Nat.gcd e 6 := by
  rw [gcd_six_mod (positiveExponent e), gcd_six_mod e,
    positiveExponent_mod e he]

private theorem root_power_seven (a : Nat) (ha : RootClass a) :
    a ^ 7 % 99 = a % 99 := by
  have h : ∀ r : Fin 99, r.val ∈ [11, 22, 44, 55, 77, 88] →
      r.val ^ 7 % 99 = r.val := by
    decide +kernel
  calc
    a ^ 7 % 99 = (a % 99) ^ 7 % 99 := (power_base_mod a 7 99).symm
    _ = a % 99 := h ⟨a % 99, Nat.mod_lt _ (by decide)⟩ ha

/-- On these root classes, positive exponents have period six modulo 99. -/
theorem positive_power_reduce (a e : Nat) (he : 0 < e) (ha : RootClass a) :
    a ^ e % 99 = a ^ positiveExponent e % 99 := by
  have hseven := root_power_seven a ha
  have hperiod : ∀ k, a ^ (1 + (k + 6)) % 99 = a ^ (1 + k) % 99 := by
    intro k
    calc
      a ^ (1 + (k + 6)) % 99 = (a ^ k * a ^ 7) % 99 := by
        rw [show 1 + (k + 6) = k + 7 by omega, Nat.pow_add]
      _ = (a ^ k % 99 * (a ^ 7 % 99)) % 99 := Nat.mul_mod _ _ _
      _ = (a ^ k % 99 * (a % 99)) % 99 := by rw [hseven]
      _ = (a ^ k * a) % 99 := (Nat.mul_mod _ _ _).symm
      _ = a ^ (1 + k) % 99 := by
        rw [show 1 + k = k + 1 by omega, Nat.pow_succ]
  have h := periodic_reduce (fun k => a ^ (1 + k) % 99) 6
    (by decide) hperiod (e - 1)
  have hl : 1 + (e - 1) = e := by omega
  have hr : 1 + (e - 1) % 6 = positiveExponent e := by
    unfold positiveExponent
    omega
  rw [hl, hr] at h
  exact h

/-- The matching predicate reduces even when the base is not a root class. -/
theorem power_target_reduce (a e t : Nat) (he : 0 < e) :
    (a ^ e % 99 = phase196 t) ↔
      (a ^ positiveExponent e % 99 = phase196 t) := by
  constructor
  · intro h
    have ha := root_class_of_power a e t he h
    exact (positive_power_reduce a e he ha).symm.trans h
  · intro h
    have ha := root_class_of_power a (positiveExponent e) t
      (positiveExponent_bounds e).1 h
    exact (positive_power_reduce a e he ha).trans h

theorem residueRoots_reduce (e t : Nat) (he : 0 < e) :
    residueRoots e t = residueRoots (positiveExponent e) t := by
  apply List.filter_congr
  intro a _
  simp only [power_target_reduce a e t he]

theorem residueRoots_time_reduce (e t : Nat) :
    residueRoots e t = residueRoots e (t % 6) := by
  simp only [residueRoots, phase196, Nat.mod_mod]

private theorem phase_dvd_reduce (g t : Nat) (hg : g ∣ 6) :
    (g ∣ t % 6 + 4) ↔ (g ∣ t + 4) := by
  have hm : (t % 6 + 4) % 6 = (t + 4) % 6 := by omega
  calc
    (g ∣ t % 6 + 4) ↔ (g ∣ (t % 6 + 4) % 6) := (Nat.dvd_mod_iff hg).symm
    _ ↔ (g ∣ (t + 4) % 6) := by rw [hm]
    _ ↔ (g ∣ t + 4) := Nat.dvd_mod_iff hg

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
/-- Six positive exponent representatives and six phases, with 99 candidate residues per case. -/
theorem finite_root_count : ∀ e : Fin 7, 0 < e.val → ∀ t : Fin 6,
    (residueRoots e.val t.val).length =
      if Nat.gcd e.val 6 ∣ t.val + 4 then Nat.gcd e.val 6 else 0 := by
  decide +kernel

/-- The finite certificate determines the root count for every positive exponent. -/
theorem root_count (e t : Nat) (he : 0 < e) :
    (residueRoots e t).length =
      if Nat.gcd e 6 ∣ t + 4 then Nat.gcd e 6 else 0 := by
  have hb := positiveExponent_bounds e
  have hfinite := finite_root_count ⟨positiveExponent e, by omega⟩ hb.1
    ⟨t % 6, Nat.mod_lt _ (by decide)⟩
  have hdiv := phase_dvd_reduce (Nat.gcd e 6) t (Nat.gcd_dvd_right e 6)
  calc
    (residueRoots e t).length = (residueRoots (positiveExponent e) t).length :=
      congrArg List.length (residueRoots_reduce e t he)
    _ = (residueRoots (positiveExponent e) (t % 6)).length :=
      congrArg List.length (residueRoots_time_reduce (positiveExponent e) t)
    _ = if Nat.gcd (positiveExponent e) 6 ∣ t % 6 + 4 then
        Nat.gcd (positiveExponent e) 6 else 0 := hfinite
    _ = if Nat.gcd e 6 ∣ t + 4 then Nat.gcd e 6 else 0 := by
      rw [positiveExponent_gcd e he]
      simp only [hdiv]

end P196.OrbitPowerResidues.Arithmetic
