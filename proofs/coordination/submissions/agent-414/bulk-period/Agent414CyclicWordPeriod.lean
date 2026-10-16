import SoficProof

/-!
Agent #414: primitive periods of injectively labelled cyclic words.
This supplies the clock-divisibility premise for the exact six-letter bulk targets.
The final specialization uses the original BulkTargets definitions, not a new model.
-/
namespace Agent414CyclicWordPeriod
open Sofic

set_option maxRecDepth 10000
set_option maxHeartbeats 5000000

def cyclicWord {m : Nat} (hm : 0 < m) (letters : Fin m → Nat)
    (phase : Fin m) : Word :=
  fun i => letters ⟨(i + phase.val) % m, Nat.mod_lt _ hm⟩

/-- An injectively labelled cycle has precisely the periods divisible by its size.
Zero is included on both sides; positivity is required later for the exclusion. -/
theorem periodic_iff_dvd {m n : Nat} (hm : 0 < m)
    (letters : Fin m → Nat) (phase : Fin m)
    (hinj : ∀ a b, letters a = letters b → a = b) :
    Periodic n (cyclicWord hm letters phase) ↔ m ∣ n := by
  constructor
  · intro hp
    let i := m - phase.val
    have hi : i + phase.val = m := Nat.sub_add_cancel (Nat.le_of_lt phase.isLt)
    have hin : i + n + phase.val = m + n := by omega
    have hvals : (i + n + phase.val) % m = (i + phase.val) % m :=
      congrArg Fin.val (hinj _ _ (hp i))
    have hzero : n % m = 0 := by
      simpa only [hin, hi, Nat.add_mod, Nat.mod_self, Nat.zero_add, Nat.mod_mod] using hvals
    exact Nat.dvd_of_mod_eq_zero hzero
  · intro hd i
    have hn : n % m = 0 := Nat.mod_eq_zero_of_dvd hd
    apply congrArg letters
    apply Fin.ext
    change (i + n + phase.val) % m = (i + phase.val) % m
    simp [Nat.add_mod, hn]

/-- Kernel check of injectivity for the exact two six-letter tables in BulkTargets.
This closed finite assertion does not assume the injectivity needed above. -/
theorem bulk_letter_injective_checked : ∀ (family : Fin 2) (a b : Fin 6),
    ((if family.val = 0 then #[80, 31, 62, 25, 56, 7] else #[56, 25, 62, 31, 80, 7]) : Array Nat)[a.val]! =
    ((if family.val = 0 then #[80, 31, 62, 25, 56, 7] else #[56, 25, 62, 31, 80, 7]) : Array Nat)[b.val]! →
    a = b := by
  decide +kernel

/-- Destination periodicity propagates through a finite path, including its
reflexive case. The arithmetic-column specialization supplies hstep by definition. -/
theorem periodic_of_path {n : Nat} {E : Word → Word → Prop} {u v : Word}
    (hu : Periodic n u) (hstep : ∀ a b, E a b → Periodic n b)
    (hp : ReverseClosure.Path E u v) : Periodic n v := by
  induction hp with
  | refl => exact hu
  | snoc _ edge _ => exact hstep _ _ edge

#print axioms periodic_iff_dvd
#print axioms bulk_letter_injective_checked
#print axioms periodic_of_path
end Agent414CyclicWordPeriod
