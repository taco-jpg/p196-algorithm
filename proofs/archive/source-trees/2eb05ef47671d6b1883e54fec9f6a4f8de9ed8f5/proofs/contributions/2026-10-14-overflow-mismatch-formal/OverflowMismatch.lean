import LychrelDigitSums

/-! Unequal isolated interval carries certify one nonpalindromic output.
The intervals need not be symmetric, disjoint, or members of a partition.
Their lengths and terminal coefficients must be positive. -/

namespace OverflowMismatch

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196

/-- Independent normalization of an interval, starting with carry zero. -/
def isolatedCarry (q : Nat → Nat) (start length : Nat) : Nat :=
  carry (fun i => q (start + i)) length

def PositiveTerminalInterval (q : Nat → Nat) (L start length : Nat) : Prop :=
  0 < length ∧ start + length ≤ L ∧ 0 < q (start + (length - 1))

instance (q : Nat → Nat) (L start length : Nat) :
    Decidable (PositiveTerminalInterval q L start length) :=
  inferInstanceAs (Decidable
    (0 < length ∧ start + length ≤ L ∧ 0 < q (start + (length - 1))))

theorem carry_zero_of_small (q : Nat → Nat) (length : Nat)
    (hsmall : ∀ i, i < length → q i ≤ 9) : carry q length = 0 := by
  induction length with
  | zero => rfl
  | succ length ih =>
    have hprev := ih (fun i hi => hsmall i (by omega))
    have hlast := hsmall length (by omega)
    simp only [carry, hprev, Nat.add_zero]
    omega

theorem isolatedCarry_zero_of_small (q : Nat → Nat) (L start length : Nat)
    (hsmall : ∀ i, i < L → q i ≤ 9) (hinside : start + length ≤ L) :
    isolatedCarry q start length = 0 :=
  carry_zero_of_small (fun i => q (start + i)) length
    (fun i hi => hsmall (start + i) (by omega))

/-- A terminal coefficient 11 forces outgoing carry one, irrespective
of the carry produced by earlier coefficients in the isolated interval. -/
theorem isolatedCarry_one_of_terminal_eleven (q : Nat → Nat) (L start length : Nat)
    (hbound : ∀ i, i < L → q i ≤ 18) (hlen : 0 < length)
    (hinside : start + length ≤ L) (hlast : q (start + (length - 1)) = 11) :
    isolatedCarry q start length = 1 := by
  have hb := carry_bounded (fun i => q (start + i)) length
    (fun i hi => hbound (start + i) (by omega)) (length - 1) (by omega)
  have hindex : length = (length - 1) + 1 := by omega
  unfold isolatedCarry
  calc
    carry (fun i => q (start + i)) length =
        carry (fun i => q (start + i)) ((length - 1) + 1) :=
      congrArg (carry (fun i => q (start + i))) hindex
    _ = 1 := by rw [carry, hlast]; omega

/-- Exact palindrome predecessor classes synchronize all isolated
positive-terminal interval carry bits. No interval symmetry is assumed. -/
theorem badWord_interval_carries_equal (q : Nat → Nat) (L a m b k : Nat)
    (hbad : BadWord L q)
    (ha : PositiveTerminalInterval q L a m)
    (hb : PositiveTerminalInterval q L b k) :
    isolatedCarry q a m = isolatedCarry q b k := by
  rcases hbad with hsmall | ⟨_, hspecial⟩
  · rw [isolatedCarry_zero_of_small q L a m hsmall ha.2.1,
      isolatedCarry_zero_of_small q L b k hsmall hb.2.1]
  · have hbound : ∀ i, i < L → q i ≤ 18 := by
      intro i hi
      rcases hspecial i hi with hzero | heleven <;> omega
    have hlastA : q (a + (m - 1)) = 11 := by
      have hp := ha.2.2
      rcases hspecial (a + (m - 1)) (by have := ha.1; have := ha.2.1; omega)
        with hzero | heleven <;> omega
    have hlastB : q (b + (k - 1)) = 11 := by
      have hp := hb.2.2
      rcases hspecial (b + (k - 1)) (by have := hb.1; have := hb.2.1; omega)
        with hzero | heleven <;> omega
    rw [isolatedCarry_one_of_terminal_eleven q L a m hbound ha.1 ha.2.1 hlastA,
      isolatedCarry_one_of_terminal_eleven q L b k hbound hb.1 hb.2.1 hlastB]

theorem mismatch_not_badWord (q : Nat → Nat) (L a m b k : Nat)
    (ha : PositiveTerminalInterval q L a m)
    (hb : PositiveTerminalInterval q L b k)
    (hmismatch : isolatedCarry q a m ≠ isolatedCarry q b k) : ¬ BadWord L q := by
  intro hbad
  exact hmismatch (badWord_interval_carries_equal q L a m b k hbad ha hb)

theorem canonical_badWord_of_palindrome (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hp : Palindrome (step n)) : BadWord L q := by
  have hp' : Palindrome (step (value d L)) := by simpa only [hc.2.2.2] using hp
  rcases (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp'
    with hsmall | ⟨houter, hspecial⟩
  · exact Or.inl (fun i hi => by simpa only [hrep i hi] using hsmall i hi)
  · refine Or.inr ⟨?_, ?_⟩
    · simpa only [hrep 0 hc.1] using houter
    · intro i hi
      simpa only [hrep i hi] using hspecial i hi

theorem numeric_palindrome_interval_carries_equal (n : Nat) (d q : Nat → Nat)
    (L a m b k : Nat) (hc : Canonical n d L)
    (hrep : ∀ i, i < L → columnSum d L i = q i)
    (ha : PositiveTerminalInterval q L a m)
    (hb : PositiveTerminalInterval q L b k) (hp : Palindrome (step n)) :
    isolatedCarry q a m = isolatedCarry q b k :=
  badWord_interval_carries_equal q L a m b k
    (canonical_badWord_of_palindrome n d q L hc hrep hp) ha hb

/-- Unequal isolated interval carry bits certify an actual ordinary
reverse-and-add output as nonpalindromic. -/
theorem numeric_mismatch_safe (n : Nat) (d q : Nat → Nat) (L a m b k : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (ha : PositiveTerminalInterval q L a m)
    (hb : PositiveTerminalInterval q L b k)
    (hmismatch : isolatedCarry q a m ≠ isolatedCarry q b k) :
    ¬ Palindrome (step n) := by
  intro hp
  exact hmismatch (numeric_palindrome_interval_carries_equal n d q L a m b k
    hc hrep ha hb hp)

/-- The same certificate applies at any actual orbit time, with the
iterated word's real changing width. No persistence premise is asserted. -/
theorem numeric_orbit_mismatch_safe (n : Nat) (d q : Nat → Nat) (L t a m b k : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (ha : PositiveTerminalInterval (iterPairs q L t).2 (iterPairs q L t).1 a m)
    (hb : PositiveTerminalInterval (iterPairs q L t).2 (iterPairs q L t).1 b k)
    (hmismatch : isolatedCarry (iterPairs q L t).2 a m ≠
      isolatedCarry (iterPairs q L t).2 b k) :
    ¬ Palindrome (orbit n (t + 1)) := by
  obtain ⟨e, he, her⟩ := iterPairs_representation n d q L t hc hrep
  exact numeric_mismatch_safe (orbit n t) e (iterPairs q L t).2
    (iterPairs q L t).1 a m b k he her ha hb hmismatch

def mismatchDigits : Nat → Nat
  | 0 => 0 | 1 => 0 | 2 => 9 | 3 => 2 | 4 => 2 | _ => 0

theorem mismatchDigits_canonical : Canonical 22900 mismatchDigits 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;> decide

/-- External overflow-mismatch example, with safety derived from the new
criterion rather than merely evaluating the palindrome predicate. -/
theorem mismatch_example :
    isolatedCarry (columnSum mismatchDigits 5) 0 2 = 0 ∧
    isolatedCarry (columnSum mismatchDigits 5) 2 1 = 1 ∧
    step 22900 = 23822 ∧ ¬ Palindrome (step 22900) := by
  refine ⟨by decide, by decide, by decide, ?_⟩
  exact numeric_mismatch_safe 22900 mismatchDigits (columnSum mismatchDigits 5)
    5 0 2 2 1 mismatchDigits_canonical (fun _ _ => rfl)
    (by decide) (by decide) (by decide)

def nonsymmetricDigits : Nat → Nat
  | 0 => 6 | 1 => 6 | 2 => 9 | 3 => 2 | 4 => 1 | _ => 0

theorem nonsymmetricDigits_canonical : Canonical 12966 nonsymmetricDigits 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;> decide

/-- The interval `(7,8)` is not symmetric, yet its carry differs from
the singleton interval `(18)`, certifying the actual output's safety. -/
theorem nonsymmetric_interval_example :
    columnSum nonsymmetricDigits 5 0 = 7 ∧ columnSum nonsymmetricDigits 5 1 = 8 ∧
    isolatedCarry (columnSum nonsymmetricDigits 5) 0 2 = 0 ∧
    isolatedCarry (columnSum nonsymmetricDigits 5) 2 1 = 1 ∧
    step 12966 = 79887 ∧ ¬ Palindrome (step 12966) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, ?_⟩
  exact numeric_mismatch_safe 12966 nonsymmetricDigits (columnSum nonsymmetricDigits 5)
    5 0 2 2 1 nonsymmetricDigits_canonical (fun _ _ => rfl)
    (by decide) (by decide) (by decide)

def zeroTerminalDigits : Nat → Nat
  | 0 => 2 | 1 => 2 | 2 => 0 | 3 => 9 | 4 => 9 | _ => 0

theorem zeroTerminalDigits_canonical : Canonical 99022 zeroTerminalDigits 5 := by
  refine ⟨by decide, ?_, by decide, by decide⟩
  intro i hi
  have h : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 := by omega
  rcases h with rfl | rfl | rfl | rfl | rfl <;> decide

/-- Dropping terminal positivity makes the implication false: the central
zero interval has carry zero while `(11,11)` has carry one. -/
theorem zero_terminal_counterexample :
    step 99022 = 121121 ∧ Palindrome (step 99022) ∧
    isolatedCarry (columnSum zeroTerminalDigits 5) 0 2 = 1 ∧
    isolatedCarry (columnSum zeroTerminalDigits 5) 2 1 = 0 ∧
    columnSum zeroTerminalDigits 5 2 = 0 ∧
    ¬ PositiveTerminalInterval (columnSum zeroTerminalDigits 5) 5 2 1 := by
  decide

end OverflowMismatch
