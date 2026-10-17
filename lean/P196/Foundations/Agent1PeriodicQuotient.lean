import P196.Foundations.Agent1PeriodicGuardFacts
import P196.Foundations.Agent1PeriodicOuterStrip
import P196.Foundations.Agent1PeriodicCenterStrip

/-!
Exact whole-period absorption for the spatial quotient. The period word,
normalizer and actual pair map are the original definitions. This module
asserts neither safety preservation nor a return cycle.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

/-- Absorb complete exterior periods and mirrored center periods into the
two repeated bands. All exponents are natural numbers, including zero. -/
theorem periodicWord_absorb (B H w : Word) (u v k : Nat) :
    periodicWord (B ++ pow w u)
      (pow w v ++ H ++ pow w.reverse v) w k =
    periodicWord B H w (k + u + v) := by
  have hl : pow w u ++ pow w k ++ pow w v = pow w (k+u+v) := by
    rw [← pow_append, ← pow_append, Nat.add_comm u k]
  have hr : pow w.reverse v ++ pow w.reverse k ++ pow w.reverse u =
      pow w.reverse (k+u+v) := by
    rw [← pow_append, ← pow_append]
    congr 1
    omega
  simp only [periodicWord, List.reverse_append, pow_reverse]
  simp only [List.append_assoc] at hl hr ⊢
  rw [← hl, ← hr]
  simp only [List.append_assoc]

/-- Exact length, including zero exponents and noncanonical coefficient lists. -/
theorem periodicWord_length (B H w : Word) (k : Nat) :
    (periodicWord B H w k).length = 2*B.length + H.length + 2*(k*w.length) := by
  simp only [periodicWord, List.length_append, List.length_reverse, pow_length]
  omega

/-- Compose any exact whole-block decompositions with the checked raw guard.
The executable maximal algorithms below will supply these equalities. -/
theorem raw_guard_of_stripped (B H w B' H' : Word) (u v k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hk : 3 ≤ k)
    (ho : rawOuter B H w = B' ++ pow (rawPeriod B H w) u)
    (hc : rawCenter B H w =
      pow (rawPeriod B H w) v ++ H' ++ pow (rawPeriod B H w).reverse v) :
    stepWord (periodicWord B H w k) =
      periodicWord B' H' (rawPeriod B H w) ((k-2)+u+v) := by
  rw [raw_guard_bounded B H w k hB hH hw hlen hk, ho, hc]
  exact periodicWord_absorb B' H' (rawPeriod B H w) u v (k-2)

/-- The signed exponent increment agrees exactly with finite word widths.
All length casts are explicit, so a negative increment is never truncated. -/
theorem stripped_width_balance (B H w B' H' : Word) (u v : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4)
    (ho : rawOuter B H w = B' ++ pow (rawPeriod B H w) u)
    (hc : rawCenter B H w =
      pow (rawPeriod B H w) v ++ H' ++ pow (rawPeriod B H w).reverse v) :
    2*(B'.length : Int) + (H'.length : Int) + 8*((u : Int)+(v : Int)-2) =
      2*(B.length : Int) + (H.length : Int) + (rawGamma B H w : Int) := by
  obtain ⟨hbo, hwp, hhc⟩ := raw_block_lengths B H w hB hH hw hlen
  have hb := congrArg List.length ho
  have hh := congrArg List.length hc
  simp only [List.length_append, pow_length, List.length_reverse, hwp] at hb hh
  rw [hbo] at hb
  rw [hhc] at hh
  omega

def quotientOuter (B H w : Word) : Word :=
  (stripPeriodSuffix (rawPeriod B H w) (rawOuter B H w)).1

def quotientCenter (B H w : Word) : Word :=
  (stripPeriodCenter (rawPeriod B H w) (rawCenter B H w)).1

def outerPeriods (B H w : Word) : Nat :=
  (stripPeriodSuffix (rawPeriod B H w) (rawOuter B H w)).2

def centerPeriods (B H w : Word) : Nat :=
  (stripPeriodCenter (rawPeriod B H w) (rawCenter B H w)).2

def exponentDelta (B H w : Word) : Int :=
  (outerPeriods B H w : Int) + (centerPeriods B H w : Int) - 2

/-- The executable, maximally stripped quotient computes the exact actual
one-step image for every admissible exponent. No stripping premise remains. -/
theorem quotient_step_bounded (B H w : Word) (k : Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hk : 3 ≤ k) :
    stepWord (periodicWord B H w k) =
      periodicWord (quotientOuter B H w) (quotientCenter B H w)
        (rawPeriod B H w) ((k-2)+outerPeriods B H w+centerPeriods B H w) := by
  have hp : rawPeriod B H w ≠ [] := by
    have := (raw_block_lengths B H w hB hH hw hlen).2.1
    intro he
    simp only [he, List.length_nil] at this
    omega
  exact raw_guard_of_stripped B H w _ _ _ _ k hB hH hw hlen hk
    (stripPeriodSuffix_spec _ _ hp) (stripPeriodCenter_decomposition _ _)

/-- Maximality is about complete words, including nonprimitive periods. -/
theorem quotient_irreducible (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    (¬ ∃ D, quotientOuter B H w = D ++ rawPeriod B H w) ∧
      (¬ ∃ K, quotientCenter B H w =
        rawPeriod B H w ++ K ++ (rawPeriod B H w).reverse) := by
  have hp : rawPeriod B H w ≠ [] := by
    have := (raw_block_lengths B H w hB hH hw hlen).2.1
    intro he
    simp only [he, List.length_nil] at this
    omega
  exact ⟨stripPeriodSuffix_maximal _ _ hp, stripPeriodCenter_maximal _ _ hp⟩

/-- Exact width balance for the executable quotient and signed shift. -/
theorem quotient_width_balance (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) :
    2*((quotientOuter B H w).length : Int) +
      ((quotientCenter B H w).length : Int) + 8*exponentDelta B H w =
      2*(B.length : Int) + (H.length : Int) + (rawGamma B H w : Int) := by
  have hp : rawPeriod B H w ≠ [] := by
    have := (raw_block_lengths B H w hB hH hw hlen).2.1
    intro he
    simp only [he, List.length_nil] at this
    omega
  exact stripped_width_balance B H w _ _ _ _ hB hH hw hlen
    (stripPeriodSuffix_spec _ _ hp) (stripPeriodCenter_decomposition _ _)

/-- Natural exponents and the signed shift agree on every permitted input. -/
theorem quotient_exponent_accounting (B H w : Word) (k : Nat) (hk : 3 ≤ k) :
    1 ≤ (k-2)+outerPeriods B H w+centerPeriods B H w ∧
      (((k-2)+outerPeriods B H w+centerPeriods B H w : Nat) : Int) =
        (k : Int) + exponentDelta B H w := by
  unfold exponentDelta
  omega

end Agent1.Periodic

#print axioms Agent1.Periodic.periodicWord_absorb
#print axioms Agent1.Periodic.periodicWord_length
#print axioms Agent1.Periodic.raw_guard_of_stripped
#print axioms Agent1.Periodic.stripped_width_balance
#print axioms Agent1.Periodic.quotient_step_bounded
#print axioms Agent1.Periodic.quotient_irreducible
#print axioms Agent1.Periodic.quotient_width_balance
#print axioms Agent1.Periodic.quotient_exponent_accounting
