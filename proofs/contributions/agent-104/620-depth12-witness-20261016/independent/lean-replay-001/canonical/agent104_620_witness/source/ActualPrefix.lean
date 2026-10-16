import LychrelDigitSums
import PrefixInverse

/-!
Actual full-word projection to a deterministic finite-prefix normalization.
Only one high inner carry is supplied, and the actual word supplies it as
`DecimalDigits.carry q (L - k)`. No disjointness of the two boundaries is used.
-/

namespace SevenColumnProjection

open DecimalDigits FoldedDecimal OverflowCarryNormalization

/-- A finite segment in increasing low-to-high column order. -/
def segment (q : Nat → Nat) (start : Nat) : Nat → List Nat
  | 0 => []
  | n + 1 => q start :: segment q (start + 1) n

def wordPrefix (q : Nat → Nat) (k : Nat) : List Nat := segment q 0 k

theorem segment_eq_range_map (q : Nat → Nat) (start n : Nat) :
    segment q start n = (List.range' start n).map q := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih => simp only [segment, List.range'_succ, List.map_cons, ih]

theorem wordPrefix_eq_range_map (q : Nat → Nat) (k : Nat) :
    wordPrefix q k = (List.range k).map q := by
  rw [wordPrefix, segment_eq_range_map, List.range_eq_range']

/-- The deterministic low scan, with the incoming carry as its argument. -/
def lowDigits : List Nat → Nat → List Nat
  | [], _ => []
  | a :: s, x => (a + x) % 10 :: lowDigits s ((a + x) / 10)

/-- The deterministic high scan. The carry is passed from the end of the
list toward its head; the result is the outer carry and the high digits. -/
def highDigits : List Nat → Nat → Nat × List Nat
  | [], e => (e, [])
  | a :: s, e =>
      let tail := highDigits s e
      ((a + tail.1) / 10, (a + tail.1) % 10 :: tail.2)

/-- Literal list counterpart of `verify_certificates.py:forward_prefixes`
for one selected high inner carry. A nonzero outer carry shifts the high
list by the appended leading digit 1. -/
def forwardPrefix (s : List Nat) (e : Nat) : List Nat :=
  let lo := lowDigits s 0
  let hi := highDigits s e
  if hi.1 = 0 then List.zipWith (· + ·) lo hi.2
  else List.zipWith (· + ·) lo (1 :: hi.2)

/-- The two possible boundary carries used by the finite prefix abstraction. -/
def ForwardAdmitted (s p : List Nat) : Prop :=
  ∃ e, e ≤ 1 ∧ forwardPrefix s e = p

@[simp] theorem segment_length (q : Nat → Nat) (start n : Nat) :
    (segment q start n).length = n := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih => simp only [segment, List.length_cons, ih]

@[simp] theorem prefix_length (q : Nat → Nat) (k : Nat) :
    (wordPrefix q k).length = k := segment_length q 0 k

theorem lowDigits_segment (q : Nat → Nat) (start n : Nat) :
    lowDigits (segment q start n) (DecimalDigits.carry q start) =
      segment (output q) start n := by
  induction n generalizing start with
  | zero => rfl
  | succ n ih =>
      simp only [segment, lowDigits]
      have hc : (q start + DecimalDigits.carry q start) / 10 =
          DecimalDigits.carry q (start + 1) := rfl
      rw [hc, ih]
      rfl

/-- Backward scan computed from the actual innermost carry. This remains
valid past the midpoint and at k = L, where the input carry is zero. -/
theorem highDigits_segment (q : Nat → Nat) (L start n : Nat)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) (hw : start + n ≤ L) :
    highDigits (segment q start n) (DecimalDigits.carry q (L - (start + n))) =
      (DecimalDigits.carry q (L - start),
        segment (fun i => output q (L - 1 - i)) start n) := by
  induction n generalizing start with
  | zero => simp only [segment, highDigits, Nat.add_zero]
  | succ n ih =>
      have ht : start + (n + 1) = (start + 1) + n := by omega
      simp only [segment, highDigits, ht]
      rw [ih (start + 1) (by omega)]
      have hc := (folded_carry_transition q L start (by omega) hs).2
      have hi : L - (start + 1) = L - 1 - start := by omega
      simp only [hi]
      rw [← hc]
      have hd : (q start + DecimalDigits.carry q (L - 1 - start)) % 10 =
          output q (L - 1 - start) := by
        simp only [output, ← hs start (by omega)]
      rw [hd]

/-- Zip a short segment against a segment at least as long. -/
theorem zip_segments (f : Nat → Nat → Nat) (a b c : Nat → Nat)
    (sa sb sc n m : Nat) (hn : n ≤ m)
    (h : ∀ j, j < n → f (a (sa + j)) (b (sb + j)) = c (sc + j)) :
    List.zipWith f (segment a sa n) (segment b sb m) = segment c sc n := by
  induction n generalizing sa sb sc m with
  | zero => rfl
  | succ n ih =>
      cases m with
      | zero => omega
      | succ m =>
          simp only [segment, List.zipWith_cons_cons]
          congr 1
          · simpa only [Nat.add_zero] using h 0 (by omega)
          · apply ih (sa + 1) (sb + 1) (sc + 1) m (by omega)
            intro j hj
            have hh := h (j + 1) (by omega)
            simpa only [Nat.add_assoc, Nat.add_comm 1 j] using hh

/-- Every positive long source projects exactly through the deterministic
forward prefix computation, with its one ACTUAL high inner carry. The
hypothesis is only k ≤ L, so this includes overlapping reflected prefixes. -/
theorem actual_forwardPrefix (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : k ≤ L) :
    forwardPrefix (wordPrefix q k) (DecimalDigits.carry q (L - k)) =
      wordPrefix (nextColumns q L) k := by
  have hh := highDigits_segment q L 0 k ha.2.2.2.1 (by omega)
  simp only [Nat.zero_add, Nat.sub_zero] at hh
  have hl := lowDigits_segment q 0 k
  simp only [DecimalDigits.carry] at hl
  unfold forwardPrefix wordPrefix
  rw [hl, hh]
  simp only
  by_cases ho : DecimalDigits.carry q L = 0
  · simp only [ho, if_true]
    apply zip_segments (· + ·) (output q) (fun i => output q (L - 1 - i))
      (nextColumns q L) 0 0 0 k k (Nat.le_refl k)
    intro i hi
    simp only [Nat.zero_add, nextColumns, ho, if_true, columnSum, reflected]
  · simp only [ho, if_false]
    have hb := DecimalDigits.carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
    have ho1 : DecimalDigits.carry q L = 1 := by omega
    cases k with
    | zero => rfl
    | succ k =>
        simp only [segment, List.zipWith_cons_cons]
        congr 1
        · have he := folded_emission_overflow q L 0 ha.1 ho1
          simpa only [Nat.sub_zero, extended, Nat.lt_irrefl, if_false, ho1, output]
            using he.symm
        · apply zip_segments (· + ·) (output q)
            (fun i => output q (L - 1 - i)) (nextColumns q L)
            1 0 1 k (k + 1) (by omega)
          intro i hi
          have he := folded_emission_overflow q L (1 + i) (by omega) ho1
          have hidx : L - (1 + i) = L - 1 - i := by omega
          have hbound : L - 1 - i < L := by omega
          simpa only [Nat.zero_add, extended, hbound, if_true, hidx, output]
            using he.symm

/-- Actual transitions are admitted, with the exact input boundary value
retained rather than an unrelated existential carry trace. -/
theorem actual_forward_admitted (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : k ≤ L) :
    ForwardAdmitted (wordPrefix q k) (wordPrefix (nextColumns q L) k) := by
  exact ⟨DecimalDigits.carry q (L - k),
    DecimalDigits.carry_bounded q L ha.2.2.1 _ (by omega),
    actual_forwardPrefix q L k ha hk⟩

/-- At full width the unique actual high inner carry is the initial zero. -/
theorem actual_full_width_inner_carry (q : Nat → Nat) (L : Nat) :
    DecimalDigits.carry q (L - L) = 0 := by simp [DecimalDigits.carry]

/-- The actual low and reflected high carries satisfy every no-overflow
local inverse equation, without requiring disjoint boundary segments. -/
theorem actual_noOverflow (q : Nat → Nat) (L start n : Nat)
    (ha : Admissible L q) (hw : start + n ≤ L)
    (ho : DecimalDigits.carry q L = 0) :
    SevenColumn.NoOverflow (segment (nextColumns q L) start n)
      (segment q start n) (DecimalDigits.carry q start)
      (DecimalDigits.carry q (L - start)) := by
  induction n generalizing start with
  | zero => exact SevenColumn.NoOverflow.nil _ _
  | succ n ih =>
      have hc := (folded_carry_transition q L start (by omega) ha.2.2.2.1).2
      have hz := DecimalDigits.carry_bounded q L ha.2.2.1 (L - 1 - start) (by omega)
      have he := folded_emission_no_overflow q L start (by omega) ha.2.2.2.1 ho
      apply SevenColumn.NoOverflow.cons (z := DecimalDigits.carry q (L - 1 - start))
      · have := ha.2.2.1 start (by omega); omega
      · omega
      · exact hc.symm
      · exact he
      · have hi : L - (start + 1) = L - 1 - start := by omega
        simpa only [hi, DecimalDigits.carry, SevenColumn.carry]
          using ih (start + 1) (by omega)

/-- The actual overflow suffix obeys the delayed high-digit equations.
Its terminal test uses the actual carry at the last inner boundary. -/
theorem actual_overflowTail (q : Nat → Nat) (L start n : Nat)
    (ha : Admissible L q) (hs : 0 < start) (hw : start + n ≤ L)
    (ho : DecimalDigits.carry q L = 1) :
    SevenColumn.OverflowTail (segment (nextColumns q L) start n)
      (segment q start n) (q (start - 1)) (DecimalDigits.carry q start)
      (DecimalDigits.carry q (L - start + 1)) := by
  induction n generalizing start with
  | zero =>
      apply SevenColumn.OverflowTail.nil
      refine ⟨DecimalDigits.carry q (L - start), ?_, ?_⟩
      · have := DecimalDigits.carry_bounded q L ha.2.2.1 (L - start) (by omega)
        omega
      · have hc := (folded_carry_transition q L (start - 1) (by omega) ha.2.2.2.1).2
        have hidx : L - (start - 1) = L - start + 1 := by omega
        have hidx' : L - 1 - (start - 1) = L - start := by omega
        simpa only [SevenColumn.carry, hidx, hidx'] using hc.symm
  | succ n ih =>
      have hc := (folded_carry_transition q L (start - 1) (by omega) ha.2.2.2.1).2
      have hidx : L - (start - 1) = L - start + 1 := by omega
      have hidx' : L - 1 - (start - 1) = L - start := by omega
      have hz := DecimalDigits.carry_bounded q L ha.2.2.1 (L - start) (by omega)
      apply SevenColumn.OverflowTail.cons (z := DecimalDigits.carry q (L - start))
      · have := ha.2.2.1 start (by omega); omega
      · omega
      · simpa only [SevenColumn.carry, hidx, hidx'] using hc.symm
      · have he := folded_emission_overflow q L start (by omega) ho
        have hbound : L - start < L := by omega
        have hsym : q (L - start) = q (start - 1) := by
          have hh := ha.2.2.2.1 (start - 1) (by omega)
          simpa only [hidx'] using hh.symm
        simpa only [extended, hbound, if_true, output, hsym, SevenColumn.lowDigit]
          using he
      · have hi : L - (start + 1) + 1 = L - start := by omega
        have hh := ih (start + 1) (by omega) (by omega)
        rw [Nat.add_sub_cancel, hi] at hh
        exact hh

/-- Actual long projections satisfy the exact local relation consumed by
`prefixPredecessors`; the first source sum is positive by admissibility. -/
theorem actual_longCompatible (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk0 : 0 < k) (hk : k ≤ L) :
    SevenColumn.LongCompatible (wordPrefix (nextColumns q L) k) (wordPrefix q k) := by
  cases k with
  | zero => omega
  | succ k =>
      by_cases ho : DecimalDigits.carry q L = 0
      · apply SevenColumn.LongCompatible.noOverflow ha.2.1
        have hh := actual_noOverflow q L 0 (k + 1) ha (by omega) ho
        simpa only [Nat.sub_zero, DecimalDigits.carry, ho] using hh
      · have hb := DecimalDigits.carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
        have ho1 : DecimalDigits.carry q L = 1 := by omega
        apply SevenColumn.LongCompatible.overflow ha.2.1
        · have := ha.2.2.1 0 ha.1; omega
        · have he := folded_emission_overflow q L 0 ha.1 ho1
          simpa only [Nat.sub_zero, extended, Nat.lt_irrefl, if_false, ho1,
            DecimalDigits.carry, SevenColumn.lowDigit, Nat.add_comm] using he
        · have hh := actual_overflowTail q L 1 k ha (by omega) (by omega) ho1
          have hi : L - 1 + 1 = L := by omega
          rw [Nat.sub_self, hi, ho1] at hh
          exact hh

/-- Explicit semantic completeness of the executable inverse enumeration
for every actual source whose width is at least the retained prefix width. -/
theorem actual_mem_prefixPredecessors (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk0 : 0 < k) (hk : k ≤ L) :
    wordPrefix q k ∈ SevenColumn.prefixPredecessors (wordPrefix (nextColumns q L) k) :=
  SevenColumn.longCompatible_mem_prefixPredecessors (actual_longCompatible q L k ha hk0 hk)

#print axioms actual_noOverflow
#print axioms actual_overflowTail
#print axioms actual_longCompatible
#print axioms actual_mem_prefixPredecessors

#print axioms highDigits_segment
#print axioms actual_forwardPrefix
#print axioms actual_forward_admitted

end SevenColumnProjection
