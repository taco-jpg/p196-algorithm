import DifferenceObservability
import Agent10EightCarryCounterexample

/-!
Agent #10: the exact uniform complete-carry observation threshold is nine.

The upper bound is the unchanged repository theorem in DifferenceObservability.
The lower bound is the new direct canonical width-seventeen certificate in
Agent10EightCarryCounterexample. Restriction of an observed history gives the
lower bound for every smaller observation count, including zero.

Both predicates quantify over a common initial width and observe every carry,
including terminal overflow. The numeric conclusion concerns the next integer,
not injectivity of the initial integer. Iteration is unrestricted: these
predicates do not require palindrome avoidance or terminate at a palindrome.
-/

namespace Agent10NineCarrySharp
open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

/-- Uniform reconstruction of all active initial pair coefficients. -/
def UniformPairReconstruction (K : Nat) : Prop :=
  ∀ (q r : Nat → Nat) (L : Nat), Admissible L q → Admissible L r →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) →
    ∀ i, i < L → q i = r i

/-- Uniform next-integer reconstruction for ordinary canonical decimal inputs. -/
def UniformNextIntegerReconstruction (K : Nat) : Prop :=
  ∀ (n m : Nat) (d e : Nat → Nat) (L : Nat),
    Canonical n d L → Canonical m e L →
    (∀ t, t < K → ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
      carry (iterPairs (columnSum d L) L t).2 i =
        carry (iterPairs (columnSum e L) L t).2 i) →
    Lychrel196.step n = Lychrel196.step m

theorem pair_reconstruction_of_nine_le (K : Nat) (hK : 9 ≤ K) :
    UniformPairReconstruction K := by
  intro q r L hq hr hc
  exact DifferenceObservability.nine_carry_words_determine_pair_sums q r L hq hr
    (fun t ht i hi => hc t (by omega) i hi)

theorem next_integer_reconstruction_of_nine_le (K : Nat) (hK : 9 ≤ K) :
    UniformNextIntegerReconstruction K := by
  intro n m d e L hn hm hc
  exact DifferenceObservability.nine_carry_words_determine_next_integer n m d e L hn hm
    (fun t ht i hi => hc t (by omega) i hi)

theorem not_pair_reconstruction_of_lt_nine (K : Nat) (hK : K < 9) :
    ¬ UniformPairReconstruction K := by
  intro h
  have hl := NormalizationBridge.canonical_admissible
    90000000560706169 Agent10EightCarryCounterexample.leftDigits 17
    Agent10EightCarryCounterexample.left_canonical
  have hr := NormalizationBridge.canonical_admissible
    90000000806235169 Agent10EightCarryCounterexample.rightDigits 17
    Agent10EightCarryCounterexample.right_canonical
  have he := h Agent10EightCarryCounterexample.leftColumns
    Agent10EightCarryCounterexample.rightColumns 17 hl hr
    (fun t ht i hi => Agent10EightCarryCounterexample.eight_complete_carries
      t (by omega) i hi)
  exact Agent10EightCarryCounterexample.initial_pair_difference_active.2 (he 3 (by decide))

theorem not_next_integer_reconstruction_of_lt_nine (K : Nat) (hK : K < 9) :
    ¬ UniformNextIntegerReconstruction K := by
  intro h
  apply Agent10EightCarryCounterexample.next_integers_differ
  exact h 90000000560706169 90000000806235169
    Agent10EightCarryCounterexample.leftDigits Agent10EightCarryCounterexample.rightDigits 17
    Agent10EightCarryCounterexample.left_canonical Agent10EightCarryCounterexample.right_canonical
    (fun t ht i hi => Agent10EightCarryCounterexample.eight_complete_carries
      t (by omega) i hi)

theorem uniform_pair_reconstruction_iff (K : Nat) :
    UniformPairReconstruction K ↔ 9 ≤ K := by
  constructor
  · intro h
    by_cases hK : 9 ≤ K
    · exact hK
    · exact False.elim (not_pair_reconstruction_of_lt_nine K (by omega) h)
  · exact pair_reconstruction_of_nine_le K

theorem uniform_next_integer_reconstruction_iff (K : Nat) :
    UniformNextIntegerReconstruction K ↔ 9 ≤ K := by
  constructor
  · intro h
    by_cases hK : 9 ≤ K
    · exact hK
    · exact False.elim (not_next_integer_reconstruction_of_lt_nine K (by omega) h)
  · exact next_integer_reconstruction_of_nine_le K

theorem eight_insufficient :
    ¬ UniformPairReconstruction 8 ∧ ¬ UniformNextIntegerReconstruction 8 :=
  ⟨not_pair_reconstruction_of_lt_nine 8 (by decide),
    not_next_integer_reconstruction_of_lt_nine 8 (by decide)⟩

theorem nine_sufficient :
    UniformPairReconstruction 9 ∧ UniformNextIntegerReconstruction 9 :=
  ⟨pair_reconstruction_of_nine_le 9 (by decide),
    next_integer_reconstruction_of_nine_le 9 (by decide)⟩

/-- Both uniform reconstruction tasks have exactly the same sharp threshold. -/
theorem nine_is_exact_uniform_threshold :
    (∀ K, UniformPairReconstruction K ↔ 9 ≤ K) ∧
    (∀ K, UniformNextIntegerReconstruction K ↔ 9 ≤ K) :=
  ⟨uniform_pair_reconstruction_iff, uniform_next_integer_reconstruction_iff⟩

#print axioms pair_reconstruction_of_nine_le
#print axioms next_integer_reconstruction_of_nine_le
#print axioms not_pair_reconstruction_of_lt_nine
#print axioms not_next_integer_reconstruction_of_lt_nine
#print axioms uniform_pair_reconstruction_iff
#print axioms uniform_next_integer_reconstruction_iff
#print axioms eight_insufficient
#print axioms nine_sufficient
#print axioms nine_is_exact_uniform_threshold

end Agent10NineCarrySharp
