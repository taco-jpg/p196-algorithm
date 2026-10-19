import P196.OddPredecessorTargetCensus.PrefixPairs

/-!
# Finite coefficient tables for the sharp cutoff bound

Agent #6: reuse the existing outer coefficient lists to count all blocks
that can contribute within each two-digit cutoff interval. The finite
certificates cover every integer from ten through ninety-nine, and the
envelope inequalities retain the exact constants needed after squaring.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open OddPredecessorTargetCensus

/-- Number of eligible low outer-prefix blocks in the two-digit range. -/
def lowBlockCount (a : Nat) : Nat := (a - 8) / 2

/-- Upper-prefix block count, including the five special outer-nine choices. -/
def highBlockCount (a : Nat) : Nat := 5 + 10 * min 5 (lowBlockCount a)

/-- Scaled cumulative count envelope at an even decimal width. -/
def evenEnvelope (a : Nat) : Nat :=
  605 + 9 * (lowBlockCount a + highBlockCount a)

/-- Scaled cumulative count envelope at an odd decimal width. -/
def oddEnvelope (a : Nat) : Nat :=
  1505 + 9 * (10 * lowBlockCount a + highBlockCount a)

private theorem prefix_counts_checked :
    ∀ a : Fin 90,
      noOverflowPrefixes.countP (fun p => decide (10 * p.1 + p.2 ≤ a.val + 10)) =
          lowBlockCount (a.val + 10) ∧
      overflowPrefixes.countP (fun p => decide (p.1 ≤ a.val + 10)) =
          highBlockCount (a.val + 10) := by
  decide +kernel

private theorem envelope_squares_checked :
    ∀ a : Fin 90,
      (evenEnvelope (a.val + 10)) ^ 2 ≤ 72900 * (a.val + 10) ∧
      (oddEnvelope (a.val + 10)) ^ 2 ≤ 729000 * (a.val + 10) := by
  decide +kernel

/-- The low coefficient prefixes have every even value from ten through
ninety-eight exactly once, giving the exact cutoff block count. -/
theorem count_noOverflowPrefixes (a : Nat) (ha : 10 ≤ a) (ha' : a ≤ 99) :
    noOverflowPrefixes.countP (fun p => decide (10 * p.1 + p.2 ≤ a)) =
      lowBlockCount a := by
  have h := (prefix_counts_checked ⟨a - 10, by omega⟩).1
  simpa only [Nat.sub_add_cancel ha] using h

/-- Each eligible high even outer coefficient contributes ten choices;
the special outer-nine class contributes its five choices throughout. -/
theorem count_overflowPrefixes (a : Nat) (ha : 10 ≤ a) (ha' : a ≤ 99) :
    overflowPrefixes.countP (fun p => decide (p.1 ≤ a)) =
      highBlockCount a := by
  have h := (prefix_counts_checked ⟨a - 10, by omega⟩).2
  simpa only [Nat.sub_add_cancel ha] using h

/-- The even-width count envelope satisfies the required square bound
at every two-digit cutoff interval. -/
theorem evenEnvelope_square (a : Nat) (ha : 10 ≤ a) (ha' : a ≤ 99) :
    (evenEnvelope a) ^ 2 ≤ 72900 * a := by
  have h := (envelope_squares_checked ⟨a - 10, by omega⟩).1
  simpa only [Nat.sub_add_cancel ha] using h

/-- The odd-width count envelope satisfies its corresponding square bound
at every two-digit cutoff interval. -/
theorem oddEnvelope_square (a : Nat) (ha : 10 ≤ a) (ha' : a ≤ 99) :
    (oddEnvelope a) ^ 2 ≤ 729000 * a := by
  have h := (envelope_squares_checked ⟨a - 10, by omega⟩).2
  simpa only [Nat.sub_add_cancel ha] using h

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.lowBlockCount
#print axioms SharpOddTargetSparsity.highBlockCount
#print axioms SharpOddTargetSparsity.evenEnvelope
#print axioms SharpOddTargetSparsity.oddEnvelope
#print axioms SharpOddTargetSparsity.count_noOverflowPrefixes
#print axioms SharpOddTargetSparsity.count_overflowPrefixes
#print axioms SharpOddTargetSparsity.evenEnvelope_square
#print axioms SharpOddTargetSparsity.oddEnvelope_square
