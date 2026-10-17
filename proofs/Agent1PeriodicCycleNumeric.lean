import Agent1PeriodicCyclePath
import Agent1PeriodicCycleGuard
import Agent1PeriodicSafetyNumeric

/-!
Conditional ordinary-orbit interpretation of one supplied safe full quotient
cycle. Original METHOD_AND_PROOF section 4, lines 168--176 already states
this criterion. The repeated path and guarded copy schedule discharge its
local repetition obligation; existing arithmetic representation and safety
theorems provide the numeric interpretation unchanged.

One finite positive integer is chosen once before all time indices. Safety
classifies each next output, so the all-time witness is that integer's
successor. No qualifying cycle, particular seed, or result for 196 is supplied.
-/

namespace Agent1.Periodic
open Agent8

/-- One fixed positive ordinary seed follows every traversal of the supplied
full quotient cycle, with a globally guarded natural copy schedule. -/
theorem quotient_cycle_actual_orbit (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ k : Nat → Nat, k 0 = 2*N+3 ∧ (∀ t, 3 ≤ k t) ∧
      ∃ n, 0 < n ∧ ∀ t,
        ∃ d, DecimalDigits.Canonical (Lychrel196.orbit n t) d
            (periodicWord (B (t%N)) (H (t%N)) (w (t%N)) (k t)).length ∧
          ∀ j, j < (periodicWord (B (t%N)) (H (t%N)) (w (t%N)) (k t)).length →
            DecimalDigits.columnSum d
              (periodicWord (B (t%N)) (H (t%N)) (w (t%N)) (k t)).length j =
              ((periodicWord (B (t%N)) (H (t%N)) (w (t%N)) (k t))[j]?).getD 0 := by
  obtain ⟨k, hk0, hguard, hkstep⟩ :=
    quotient_return_guarded_schedule B H w N hp hv hN hreturn
  obtain ⟨n, d, hn, hc, hr⟩ := periodicWord_realizable
    (B 0) (H 0) (w 0) (k 0) hv (by have := hguard 0; omega)
  refine ⟨k, hk0, hguard, n, hn, ?_⟩
  intro t
  have hp' := quotient_path_repeat B H w N hp hN hreturn t
  have hreal := quotient_path_actual_prefix
    (repeatWordState B N) (repeatWordState H N) (repeatWordState w N)
    k t hp' (fun i _ => hguard i) (fun i _ => hkstep i) n d
    (by simpa only [quotientPathWord, repeatWordState_zero] using hc)
    (by simpa only [quotientPathWord, repeatWordState_zero] using hr)
  exact (hreal t (Nat.le_refl t)).2

/-- Explicit safety at every state of one exact positive full quotient cycle
gives a positive ordinary all-time palindrome-avoiding successor seed.
The complete cycle and its safety remain hypotheses, not constructed data. -/
theorem quotient_cycle_safe_positive_seed (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0)) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
    (hsafe : ∀ i, i < N → safePeriodic (B i) (H i) (w i) = true) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  obtain ⟨k, _, hguard, n, hn, hreal⟩ :=
    quotient_cycle_actual_orbit B H w N hp hv hN hreturn
  refine ⟨Lychrel196.step n, ?_, ?_⟩
  · exact DecimalDigits.orbit_positive n hn 1
  · intro t
    obtain ⟨d, hc, hr⟩ := hreal t
    have hi := Nat.mod_lt t hN
    have hlen := (hp (t%N) hi).2.2.2.1
    have hw : w (t%N) ≠ [] := by
      intro heq
      simp only [heq, List.length_nil] at hlen
      contradiction
    have hs := (safePeriodic_iff_next_not_palindrome
      (B (t%N)) (H (t%N)) (w (t%N)) (k t) (Lychrel196.orbit n t) d
      (by have := hguard t; omega) hw hc hr).mp (hsafe (t%N) hi)
    rw [Lychrel196.orbit_from_step]
    exact hs

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_cycle_actual_orbit
#print axioms Agent1.Periodic.quotient_cycle_safe_positive_seed
