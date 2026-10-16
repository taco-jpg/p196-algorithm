import Agent1PeriodicQuotient

/-!
Finite signed width accounting for the original literal period-four quotient.
Every used transition specifies all three actual successor blocks. Only the
bounded coefficient and length hypotheses needed by the original local width
identity are assumed. Zero transitions are included. No guarded exponent
trajectory, temporal-period divisibility, positive clock sum, or safe orbit
is inferred from formal interface accounting.
-/

namespace Agent1.Periodic
open Agent8

/-- A finite path of the literal maximal quotient. Preconditions are needed
exactly at the N used source states; no extra condition is imposed at N. -/
def QuotientPath (B H w : Nat → Word) (N : Nat) : Prop :=
  ∀ i, i < N →
    Bounded (B i) 18 ∧ Bounded (H i) 18 ∧ Bounded (w i) 18 ∧
    (w i).length = 4 ∧
    B (i+1) = quotientOuter (B i) (H i) (w i) ∧
    H (i+1) = quotientCenter (B i) (H i) (w i) ∧
    w (i+1) = rawPeriod (B i) (H i) (w i)

/-- Sum of the actual raw terminal-carry bits at the used source states. -/
def quotientClockSum (B H w : Nat → Word) : Nat → Nat
  | 0 => 0
  | N+1 => quotientClockSum B H w N + rawGamma (B N) (H N) (w N)

/-- Sum of the signed shifts of the literal maximal quotient.
Without exponent guards this is formal accounting, not a natural trajectory. -/
def quotientDeltaSum (B H w : Nat → Word) : Nat → Int
  | 0 => 0
  | N+1 => quotientDeltaSum B H w N + exponentDelta (B N) (H N) (w N)

/-- The unchanged local width identity telescopes along every finite exact
quotient path, including N=0, with no safety or exponent-guard premise. -/
theorem quotient_path_width_balance (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N) :
    ((2*(B N).length + (H N).length : Nat) : Int) +
      8 * quotientDeltaSum B H w N =
    ((2*(B 0).length + (H 0).length : Nat) : Int) +
      (quotientClockSum B H w N : Int) := by
  induction N with
  | zero => simp [quotientClockSum, quotientDeltaSum]
  | succ N ih =>
    have hprefix : QuotientPath B H w N := fun i hi => hp i (by omega)
    have hprevious := ih hprefix
    obtain ⟨hB, hH, hw, hlen, hnextB, hnextH, _⟩ := hp N (by omega)
    have hlocal := quotient_width_balance (B N) (H N) (w N) hB hH hw hlen
    rw [← hnextB, ← hnextH] at hlocal
    simp only [quotientClockSum, quotientDeltaSum, Int.natCast_add]
    omega

/-- Equal endpoint interface widths force the actual clock sum to be a
multiple of eight, with the precise signed total shift. This says nothing
about divisibility of N or positivity of either sum. -/
theorem quotient_path_equal_width_clock (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hwidth : 2*(B N).length + (H N).length = 2*(B 0).length + (H 0).length) :
    8 * quotientDeltaSum B H w N = (quotientClockSum B H w N : Int) ∧
      8 ∣ quotientClockSum B H w N ∧
      quotientDeltaSum B H w N = ((quotientClockSum B H w N / 8 : Nat) : Int) := by
  have hb := quotient_path_width_balance B H w N hp
  rw [hwidth] at hb
  have heq : 8 * quotientDeltaSum B H w N = (quotientClockSum B H w N : Int) := by
    omega
  have hd : (8 : Int) ∣ (quotientClockSum B H w N : Int) :=
    ⟨quotientDeltaSum B H w N, heq.symm⟩
  have hn : 8 ∣ quotientClockSum B H w N := Int.ofNat_dvd.mp hd
  have hmul := Nat.div_mul_cancel hn
  refine ⟨heq, hn, ?_⟩
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.QuotientPath
#print axioms Agent1.Periodic.quotientClockSum
#print axioms Agent1.Periodic.quotientDeltaSum
#print axioms Agent1.Periodic.quotient_path_width_balance
#print axioms Agent1.Periodic.quotient_path_equal_width_clock
