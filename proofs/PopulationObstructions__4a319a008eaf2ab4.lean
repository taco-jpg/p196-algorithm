import LychrelDigitSums

/-!
Exact population obstructions, including an obstruction on the 196 orbit.

All words are in least-significant-column-first order.  Counts range over
the entire physical word; a center column is counted once.  `runCount v`
counts maximal nonempty runs of the single symbol v (via their right ends).

The integer and actual carry-transition certificates are kernel `decide`
proofs.  The Python enumeration is discovery only.  No search exhaustiveness
or minimality claim is used by any theorem below.  In particular these
obstructions do not prove or disprove the 196 conjecture.
-/

namespace RunBirths.PopulationObstructions

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- The actual decimal digit at position i. -/
def digitAt (n i : Nat) : Nat := (n / 10 ^ i) % 10

/-- The actual folded column-sum word of an integer at a specified width. -/
def integerWord (n L : Nat) : List Nat :=
  (List.range L).map (columnSum (digitAt n) L)

def wordAt (q : List Nat) (i : Nat) : Nat := q.getD i 0

/-- Exact q transition, using the repository's overflow-dependent width
and `nextColumns`, rather than a spatial approximation. -/
def actualQStep (q : List Nat) : List Nat :=
  List.ofFn (fun i : Fin (nextWidth (wordAt q) q.length) =>
    nextColumns (wordAt q) q.length i.val)

def coefficientCount (v : Nat) (q : List Nat) : Nat := q.count v

def runCount (v : Nat) : List Nat → Nat
  | [] => 0
  | x :: xs =>
      (if x = v ∧ xs.head? ≠ some v then 1 else 0) + runCount v xs

def overflowSource : List Nat := [10,9,8,9,10]
def overflowTarget : List Nat := [1,0,18,18,0,1]
def noOverflowSource : List Nat := [9,1,10,1,9]
def noOverflowTarget : List Nat := [18,3,0,3,18]
def orbitSource : List Nat := [9,3,10,3,9]
def orbitTarget : List Nat := [18,7,0,7,18]

theorem canonical_of_value (n L : Nat) (hL : 0 < L)
    (hlead : 0 < digitAt n (L - 1))
    (hvalue : value (digitAt n) L = n) : Canonical n (digitAt n) L := by
  refine ⟨hL, ?_, hlead, hvalue⟩
  intro i _
  exact Nat.le_of_lt_succ (Nat.mod_lt _ (by decide))

theorem witness_inputs_canonical :
    Canonical 10499 (digitAt 10499) 5 ∧
    Canonical 10518 (digitAt 10518) 5 ∧
    Canonical 52514 (digitAt 52514) 5 := by
  exact ⟨canonical_of_value _ _ (by decide) (by decide) (by decide),
    canonical_of_value _ _ (by decide) (by decide) (by decide),
    canonical_of_value _ _ (by decide) (by decide) (by decide)⟩

/-- Overflow simultaneously creates both extreme symbols from none. -/
theorem overflow_integer_certificate :
    reverse10 10499 = 99401 ∧ step 10499 = 109900 ∧
    integerWord 10499 5 = overflowSource ∧
    integerWord 109900 6 = overflowTarget ∧
    carry (wordAt overflowSource) 5 = 1 ∧
    nextWidth (wordAt overflowSource) 5 = 6 ∧
    actualQStep overflowSource = overflowTarget ∧
    AstraLanguages.qstep overflowSource = overflowTarget ∧
    ¬ Palindrome 10499 ∧ ¬ Palindrome 109900 := by
  decide

/-- The obstruction also occurs without width growth. -/
theorem noOverflow_integer_certificate :
    reverse10 10518 = 81501 ∧ step 10518 = 92019 ∧
    integerWord 10518 5 = noOverflowSource ∧
    integerWord 92019 5 = noOverflowTarget ∧
    carry (wordAt noOverflowSource) 5 = 0 ∧
    nextWidth (wordAt noOverflowSource) 5 = 5 ∧
    actualQStep noOverflowSource = noOverflowTarget ∧
    AstraLanguages.qstep noOverflowSource = noOverflowTarget ∧
    ¬ Palindrome 10518 ∧ ¬ Palindrome 92019 := by
  decide

/-- This obstruction lies on the actual 196 orbit at time 5 → 6. -/
theorem orbit196_integer_certificate :
    orbit 196 5 = 52514 ∧ orbit 196 6 = 94039 ∧
    reverse10 52514 = 41525 ∧ step 52514 = 94039 ∧
    integerWord (orbit 196 5) 5 = orbitSource ∧
    integerWord (orbit 196 6) 5 = orbitTarget ∧
    carry (wordAt orbitSource) 5 = 0 ∧
    nextWidth (wordAt orbitSource) 5 = 5 ∧
    actualQStep orbitSource = orbitTarget ∧
    AstraLanguages.qstep orbitSource = orbitTarget ∧
    ¬ Palindrome 52514 ∧ ¬ Palindrome 94039 := by
  decide

theorem overflow_population_certificate :
    coefficientCount 0 overflowSource = 0 ∧
    coefficientCount 18 overflowSource = 0 ∧
    runCount 0 overflowSource = 0 ∧ runCount 18 overflowSource = 0 ∧
    coefficientCount 0 overflowTarget = 2 ∧
    coefficientCount 18 overflowTarget = 2 ∧
    runCount 0 overflowTarget = 2 ∧ runCount 18 overflowTarget = 1 := by
  decide

theorem noOverflow_population_certificate :
    coefficientCount 0 noOverflowSource = 0 ∧
    coefficientCount 18 noOverflowSource = 0 ∧
    runCount 0 noOverflowSource = 0 ∧ runCount 18 noOverflowSource = 0 ∧
    coefficientCount 0 noOverflowTarget = 1 ∧
    coefficientCount 18 noOverflowTarget = 2 ∧
    runCount 0 noOverflowTarget = 1 ∧ runCount 18 noOverflowTarget = 2 := by
  decide

/-- Both counts and both run counts increase on the 196 orbit. -/
theorem orbit196_population_certificate :
    coefficientCount 0 orbitSource = 0 ∧
    coefficientCount 18 orbitSource = 0 ∧
    runCount 0 orbitSource = 0 ∧ runCount 18 orbitSource = 0 ∧
    coefficientCount 0 orbitTarget = 1 ∧
    coefficientCount 18 orbitTarget = 2 ∧
    runCount 0 orbitTarget = 1 ∧ runCount 18 orbitTarget = 2 := by
  decide

def populationPotential (w0 w18 : Int) (q : List Nat) : Int :=
  w0 * (coefficientCount 0 q : Int) + w18 * (coefficientCount 18 q : Int)

def runPotential (w0 w18 : Int) (q : List Nat) : Int :=
  w0 * (runCount 0 q : Int) + w18 * (runCount 18 q : Int)

def jointPotential (a b c d : Int) (q : List Nat) : Int :=
  populationPotential a b q + runPotential c d q

/-- All positive integer weights fail at the same actual 196-orbit step. -/
theorem every_positive_population_weight_increases (w0 w18 : Int)
    (h0 : 0 < w0) (h18 : 0 < w18) :
    populationPotential w0 w18 orbitSource <
      populationPotential w0 w18 (actualQStep orbitSource) := by
  change w0 * 0 + w18 * 0 < w0 * 1 + w18 * 2
  omega

theorem every_positive_run_weight_increases (w0 w18 : Int)
    (h0 : 0 < w0) (h18 : 0 < w18) :
    runPotential w0 w18 orbitSource <
      runPotential w0 w18 (actualQStep orbitSource) := by
  change w0 * 0 + w18 * 0 < w0 * 1 + w18 * 2
  omega

/-- Even combining all four statistics with positive weights cannot help. -/
theorem every_positive_joint_weight_increases (a b c d : Int)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) :
    jointPotential a b c d orbitSource <
      jointPotential a b c d (actualQStep orbitSource) := by
  change (a * 0 + b * 0) + (c * 0 + d * 0) <
    (a * 1 + b * 2) + (c * 1 + d * 2)
  omega

/-- Nonincrease is required only on canonical actual integer inputs. -/
def DecimalNonincreasing (P : List Nat → Int) : Prop :=
  ∀ n L, Canonical n (digitAt n) L →
    P (actualQStep (integerWord n L)) ≤ P (integerWord n L)

theorem no_positive_population_potential (w0 w18 : Int)
    (h0 : 0 < w0) (h18 : 0 < w18) :
    ¬ DecimalNonincreasing (populationPotential w0 w18) := by
  intro h
  have hn := h 52514 5 witness_inputs_canonical.2.2
  have hw : integerWord 52514 5 = orbitSource := by decide
  rw [hw] at hn
  have hi := every_positive_population_weight_increases w0 w18 h0 h18
  omega

theorem no_positive_run_potential (w0 w18 : Int)
    (h0 : 0 < w0) (h18 : 0 < w18) :
    ¬ DecimalNonincreasing (runPotential w0 w18) := by
  intro h
  have hn := h 52514 5 witness_inputs_canonical.2.2
  have hw : integerWord 52514 5 = orbitSource := by decide
  rw [hw] at hn
  have hi := every_positive_run_weight_increases w0 w18 h0 h18
  omega

theorem no_positive_joint_potential (a b c d : Int)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) :
    ¬ DecimalNonincreasing (jointPotential a b c d) := by
  intro h
  have hn := h 52514 5 witness_inputs_canonical.2.2
  have hw : integerWord 52514 5 = orbitSource := by decide
  rw [hw] at hn
  have hi := every_positive_joint_weight_increases a b c d ha hb hc hd
  omega

/- The vector certificate above is scalar-independent: over the real or
rational numbers the same population/run change is w0 + 2*w18 > 0, and the
joint change is a + 2*b + c + 2*d > 0.  The imported Std-only foundation
does not define the real numbers; the following abstract score theorem
records exactly the order-independent obstruction without adding axioms. -/

/-- Any score that assigns a larger value to (1,2,1,2) than to (0,0,0,0)
fails nonincrease at this actual step, including nonlinear scores.  The
comparison and its incompatibility with the proposed nonincrease relation
are explicit hypotheses, not axioms or unproved ordered-field instances. -/
theorem any_strict_score_obstruction {α : Type} (score : Nat → Nat → Nat → Nat → α)
    (nonincrease : α → α → Prop)
    (h : ¬ nonincrease (score 1 2 1 2) (score 0 0 0 0)) :
    ¬ nonincrease
      (score (coefficientCount 0 (actualQStep orbitSource))
        (coefficientCount 18 (actualQStep orbitSource))
        (runCount 0 (actualQStep orbitSource))
        (runCount 18 (actualQStep orbitSource)))
      (score (coefficientCount 0 orbitSource) (coefficientCount 18 orbitSource)
        (runCount 0 orbitSource) (runCount 18 orbitSource)) := by
  exact h

#print axioms overflow_integer_certificate
#print axioms noOverflow_integer_certificate
#print axioms orbit196_integer_certificate
#print axioms orbit196_population_certificate
#print axioms no_positive_population_potential
#print axioms no_positive_run_potential
#print axioms no_positive_joint_potential
#print axioms any_strict_score_obstruction

end RunBirths.PopulationObstructions
