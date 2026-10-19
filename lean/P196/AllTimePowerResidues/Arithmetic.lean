import P196.AllTimePowerResidues.Orbit

/-!
Exact root counts for the three initial modulo-99 residues of the ordinary
orbit of 196. Their roots are units modulo both three and eleven, so their
powers have period thirty. This adds the initial gcd(e,10) factor to the
existing gcd(e,6) condition.

The finite certificate checks thirty exponent classes and three targets,
with ninety-nine candidate base residues per case. All exponent reduction
and all links to the unbounded exponent are proved inside Lean.
-/

set_option autoImplicit false

namespace P196.AllTimePowerResidues.Arithmetic

open Agent423.TemporalResidues
open P196.OrbitPowerResidues.Arithmetic

/-- Distinct residue roots of one of the three initial target residues. -/
def initialRoots (e k : Nat) : List Nat :=
  (List.range 99).filter (fun a => decide (a ^ e % 99 = initialResidue k))

private theorem initial_residue_arithmetic (k : Nat) (hk : k < 3) :
    initialResidue k % 3 ≠ 0 ∧ initialResidue k % 11 ≠ 0 ∧
      initialResidue k ≠ 1 := by
  have h : ∀ j : Fin 3,
      initialResidue j.val % 3 ≠ 0 ∧ initialResidue j.val % 11 ≠ 0 ∧
        initialResidue j.val ≠ 1 := by
    decide +kernel
  exact h ⟨k, hk⟩

private def UnitBase (a : Nat) : Prop := a % 3 ≠ 0 ∧ a % 11 ≠ 0

private theorem unit_of_initial_power (a e k : Nat) (he : 0 < e) (hk : k < 3)
    (hroot : a ^ e % 99 = initialResidue k) : UnitBase a := by
  have htarget := initial_residue_arithmetic k hk
  constructor
  · intro hz
    have hpow := power_base_mod a e 3
    rw [hz, Nat.zero_pow he, Nat.zero_mod] at hpow
    have hres : a ^ e % 3 = initialResidue k % 3 := by
      have h := congrArg (fun x => x % 3) hroot
      simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 99)] using h
    exact htarget.1 (hres.symm.trans hpow.symm)
  · intro hz
    have hpow := power_base_mod a e 11
    rw [hz, Nat.zero_pow he, Nat.zero_mod] at hpow
    have hres : a ^ e % 11 = initialResidue k % 11 := by
      have h := congrArg (fun x => x % 11) hroot
      simpa only [Nat.mod_mod_of_dvd _ (by decide : 11 ∣ 99)] using h
    exact htarget.2.1 (hres.symm.trans hpow.symm)

private theorem unit_power_thirty (a : Nat) (ha : UnitBase a) :
    a ^ 30 % 99 = 1 := by
  have h : ∀ r : Fin 99, r.val % 3 ≠ 0 → r.val % 11 ≠ 0 →
      r.val ^ 30 % 99 = 1 := by
    decide +kernel
  have hthree : (a % 99) % 3 ≠ 0 := by
    simpa only [Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 99)] using ha.1
  have heleven : (a % 99) % 11 ≠ 0 := by
    simpa only [Nat.mod_mod_of_dvd _ (by decide : 11 ∣ 99)] using ha.2
  calc
    a ^ 30 % 99 = (a % 99) ^ 30 % 99 := (power_base_mod a 30 99).symm
    _ = 1 := h ⟨a % 99, Nat.mod_lt _ (by decide)⟩ hthree heleven

private theorem unit_power_reduce (a e : Nat) (ha : UnitBase a) :
    a ^ e % 99 = a ^ (e % 30) % 99 := by
  have hthirty := unit_power_thirty a ha
  have hperiod : ∀ j, a ^ (j + 30) % 99 = a ^ j % 99 := by
    intro j
    rw [Nat.pow_add, Nat.mul_mod, hthirty, Nat.mul_one, Nat.mod_mod]
  exact periodic_reduce (fun j => a ^ j % 99) 30 (by decide) hperiod e

private theorem initial_power_target_reduce (a e k : Nat)
    (he : 0 < e) (hk : k < 3) :
    (a ^ e % 99 = initialResidue k) ↔
      (a ^ (e % 30) % 99 = initialResidue k) := by
  constructor
  · intro h
    have ha := unit_of_initial_power a e k he hk h
    exact (unit_power_reduce a e ha).symm.trans h
  · intro h
    by_cases hz : e % 30 = 0
    · have ht : initialResidue k = 1 := by simpa [hz] using h.symm
      exact False.elim ((initial_residue_arithmetic k hk).2.2 ht)
    · have ha := unit_of_initial_power a (e % 30) k (by omega) hk h
      exact (unit_power_reduce a e ha).trans h

private theorem initialRoots_reduce (e k : Nat) (he : 0 < e) (hk : k < 3) :
    initialRoots e k = initialRoots (e % 30) k := by
  apply List.filter_congr
  intro a _
  simp only [initial_power_target_reduce a e k he hk]

private theorem gcd_mod_thirty (e d : Nat) (hd : d ∣ 30) :
    Nat.gcd (e % 30) d = Nat.gcd e d := by
  calc
    Nat.gcd (e % 30) d = Nat.gcd d (e % 30) := Nat.gcd_comm _ _
    _ = Nat.gcd ((e % 30) % d) d := Nat.gcd_rec _ _
    _ = Nat.gcd (e % d) d := by rw [Nat.mod_mod_of_dvd _ hd]
    _ = Nat.gcd d e := (Nat.gcd_rec _ _).symm
    _ = Nat.gcd e d := Nat.gcd_comm _ _

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
private theorem finite_initial_root_count : ∀ e : Fin 30, ∀ k : Fin 3,
    (initialRoots e.val k.val).length =
      if Nat.gcd e.val 6 ∣ k.val + 4 ∧ Nat.gcd e.val 10 ∣ k.val + 6 then
        Nat.gcd e.val 6 * Nat.gcd e.val 10 else 0 := by
  decide +kernel

/-- Exact root count at the initial times, for every positive exponent. -/
theorem initial_root_count (e k : Nat) (he : 0 < e) (hk : k < 3) :
    (initialRoots e k).length =
      if Nat.gcd e 6 ∣ k + 4 ∧ Nat.gcd e 10 ∣ k + 6 then
        Nat.gcd e 6 * Nat.gcd e 10 else 0 := by
  have hfinite := finite_initial_root_count
    ⟨e % 30, Nat.mod_lt _ (by decide)⟩ ⟨k, hk⟩
  calc
    (initialRoots e k).length = (initialRoots (e % 30) k).length :=
      congrArg List.length (initialRoots_reduce e k he hk)
    _ = if Nat.gcd (e % 30) 6 ∣ k + 4 ∧ Nat.gcd (e % 30) 10 ∣ k + 6 then
        Nat.gcd (e % 30) 6 * Nat.gcd (e % 30) 10 else 0 := hfinite
    _ = if Nat.gcd e 6 ∣ k + 4 ∧ Nat.gcd e 10 ∣ k + 6 then
        Nat.gcd e 6 * Nat.gcd e 10 else 0 := by
      rw [gcd_mod_thirty e 6 (by decide), gcd_mod_thirty e 10 (by decide)]

end P196.AllTimePowerResidues.Arithmetic
