import P196.InverseFiberGrowth.RationalEnvelopes
import P196.Drafts.Agent7OddNooverflowFibers.SharpMaximum

/-!
# Rational growth bounds for exact folded coefficient fibers

Agent #9. These results import the existing duplicate-free enumerators and
their exact Fibonacci cardinalities. The objects counted are even mirrored
coefficient words for the repository's zero-overflow word transition.
They are not counts of ordinary integer predecessors, and the statements
make no assertion about infinite orbits or a palindrome in the orbit of 196.
-/

namespace P196.InverseFiberGrowth

open P196.Agent9.InverseFibers

/-- A uniform upper rate for every canonical half-word fiber of half-width
at least two. The exponent is the half-width minus two. -/
theorem canonical_upper (p q : Nat) (h : p * q + q ^ 2 ≤ p ^ 2)
    (s t : Symbol) (ss : List Symbol) :
    q ^ ss.length * (canonicalPreimages (s :: t :: ss)).length ≤ p ^ ss.length := by
  exact Nat.le_trans
    (Nat.mul_le_mul_left (q ^ ss.length) (canonical_bound s t ss))
    (fib_upper p q ss.length h)

/-- The explicit sharp family supplies the corresponding lower rate. -/
theorem canonical_lower (p q n : Nat) (h : p ^ 2 ≤ p * q + q ^ 2) :
    p ^ n ≤ q ^ n *
      (canonicalPreimages (11 :: List.replicate (n + 2) 9)).length := by
  rw [canonical_sharp]
  exact fib_lower p q n h

/-- The same upper bound counts complete coefficient words, using the
existing injective mirror map rather than introducing another enumerator. -/
theorem full_upper (p q : Nat) (h : p * q + q ^ 2 ≤ p ^ 2)
    (s t : Symbol) (ss : List Symbol) :
    q ^ ss.length * (fullPreimages (s :: t :: ss)).length ≤ p ^ ss.length := by
  simpa only [fullPreimages, List.length_map] using canonical_upper p q h s t ss

/-- A lower rate for the existing complete coefficient-word sharp family. -/
theorem full_lower (p q n : Nat) (h : p ^ 2 ≤ p * q + q ^ 2) :
    p ^ n ≤ q ^ n *
      (fullPreimages (11 :: List.replicate (n + 2) 9)).length := by
  simpa only [fullPreimages, List.length_map] using canonical_lower p q n h

/-- Exact rational rate certificates on either side of the Fibonacci rate.
This is an integer inequality at every finite width, not a real-valued limit. -/
theorem sharp_family_rate_sandwich (n : Nat) :
    144 ^ n ≤ 89 ^ n *
      (fullPreimages (11 :: List.replicate (n + 2) 9)).length ∧
    144 ^ (n + 1) *
      (fullPreimages (11 :: List.replicate (n + 2) 9)).length ≤ 233 ^ (n + 1) := by
  constructor
  · exact full_lower 144 89 n (by decide)
  · simp only [fullPreimages, List.length_map, canonical_sharp]
    exact fib_upper 233 144 (n + 1) (by decide)

end P196.InverseFiberGrowth
