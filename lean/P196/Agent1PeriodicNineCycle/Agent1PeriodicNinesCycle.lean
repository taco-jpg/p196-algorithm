import P196.Agent1PeriodicCycleAdapter.Agent1PeriodicCycleNumeric
import P196.Agent1PeriodicNineExcursion.Agent1PeriodicNinesPath

/-!
Automatic safety for one supplied positive full period-four quotient cycle
whose initial period is four nines. The finite path cannot exit to the
absorbing zero or eighteen phases and return to nine. Every canonical
realization of a positive nine band is nonpalindromic at the input.

The existing same-seed cycle realization and numeric safety equivalence
then discharge the explicit safety hypothesis of the original conditional
safe-cycle criterion (METHOD_AND_PROOF, section 4, lines 168--176).
No qualifying return is constructed, and no center obstruction, cycle
search, unconditional decimal existence, or claim about 196 is supplied.
-/

namespace Agent1.Periodic
open Agent8

/-- A positive nine band makes every original canonical realization
nonpalindromic at the represented input, including time zero. -/
theorem periodic_nines_input_nonpalindrome (B H : Word) (k n : Nat)
    (d : Nat → Nat) (hk : 0 < k)
    (hc : DecimalDigits.Canonical n d (periodicWord B H [9,9,9,9] k).length)
    (hrep : ∀ i, i < (periodicWord B H [9,9,9,9] k).length →
      DecimalDigits.columnSum d (periodicWord B H [9,9,9,9] k).length i =
        ((periodicWord B H [9,9,9,9] k)[i]?).getD 0) :
    ¬ Lychrel196.Palindrome n := by
  have hm : 9 ∈ periodicWord B H [9,9,9,9] k :=
    (mem_periodicWord_iff B H [9,9,9,9] k 9 hk).mpr (by simp)
  obtain ⟨i, hi, he⟩ := List.getElem_of_mem hm
  have hcol := hrep i hi
  rw [List.getElem?_eq_getElem hi, Option.getD_some, he] at hcol
  intro hp
  rw [← hc.2.2.2] at hp
  have hs := (DecimalDigits.palindrome_value_iff d _ hc.2.1
    (Or.inr hc.2.2.1)).mp hp i hi
  simp only [DecimalDigits.columnSum, DecimalDigits.reflected] at hcol
  omega

private theorem nines_cycle_safe_of_phase (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
    (hphase : ∀ i, i ≤ N → w i = [9,9,9,9]) :
    ∀ i, i < N → safePeriodic (B i) (H i) (w i) = true := by
  obtain ⟨k, _, hguard, n, _, hreal⟩ :=
    quotient_cycle_actual_orbit B H w N hp hv hN hreturn
  intro i hi
  obtain ⟨d, hc, hr⟩ := hreal i
  have hmod : i % N = i := Nat.mod_eq_of_lt hi
  simp only [hmod] at hc hr
  obtain ⟨d', hc', hr'⟩ := hreal (i+1)
  have hj := Nat.mod_lt (i+1) hN
  have hnext := hphase ((i+1)%N) (Nat.le_of_lt hj)
  rw [hnext] at hc' hr'
  have hn := periodic_nines_input_nonpalindrome
    (B ((i+1)%N)) (H ((i+1)%N)) (k (i+1))
    (Lychrel196.orbit n (i+1)) d'
    (by have := hguard (i+1); omega) hc' hr'
  have hw : w i ≠ [] := by
    rw [hphase i (Nat.le_of_lt hi)]
    decide
  exact (safePeriodic_iff_next_not_palindrome
    (B i) (H i) (w i) (k i) (Lychrel196.orbit n i) d
    (by have := hguard i; omega) hw hc hr).mpr hn

/-- Every finite state of the supplied full nine cycle passes the original
next-output safety test. Safety is derived, not assumed. -/
theorem quotient_cycle_nines_safe (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∀ i, i < N → safePeriodic (B i) (H i) (w i) = true := by
  exact nines_cycle_safe_of_phase B H w N hp hv hN hreturn
    (quotient_path_nines_phase B H w N hp hw0 (hreturn.2.2.trans hw0))

/-- A supplied original-valid positive full nine cycle yields one positive
ordinary all-time palindrome-avoiding seed, with no separate safety premise.
The full cycle remains a hypothesis; this theorem supplies no instance. -/
theorem quotient_cycle_nines_positive_seed (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw0 : w 0 = [9,9,9,9]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ n, 0 < n ∧ Lychrel196.IsLychrel n := by
  exact quotient_cycle_safe_positive_seed B H w N hp hv hN hreturn
    (quotient_cycle_nines_safe B H w N hp hv hw0 hN hreturn)

end Agent1.Periodic
#print axioms Agent1.Periodic.periodic_nines_input_nonpalindrome
#print axioms Agent1.Periodic.quotient_cycle_nines_safe
#print axioms Agent1.Periodic.quotient_cycle_nines_positive_seed
