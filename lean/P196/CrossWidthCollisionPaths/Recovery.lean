import P196.CrossWidthCollisionPaths.Profiles

/-!
# Actual carry recovery from closed collision paths

The low column relation propagates the encoded difference of the two
actual carries. The closed endpoint determines both terminal carries,
and the existing positional value identity then gives a common value.
Reflection recovers the second carry coordinate of the supplied path.
No center condition is needed for these statements.
-/

set_option autoImplicit false

namespace CrossWidthCollisionPaths

open DecimalDigits CrossWidthCollisionStates

private theorem carry_step
    (q r : Nat → Nat) (i u v : Nat)
    (hin : u + carry r i = carry q i + 1)
    (hcol : q i + u + 9 = r i + 10 * v) :
    output q i = output r i ∧
      v + carry r (i + 1) = carry q (i + 1) + 1 := by
  have hq := column_equation q i
  have hr := column_equation r i
  have hqb := output_bounded q i
  have hrb := output_bounded r i
  omega

private theorem closed_carry_outputs
    {L : Nat} {f : Nat → State} (h : Closed L f) :
    (∀ i, 1 ≤ i → i ≤ L →
      (f i).u + carry (longWord L f) i = carry (shortWord f) i + 1) ∧
      ∀ i, i < L → output (shortWord f) i = output (longWord L f) i := by
  have hp := closed_word_properties h
  have hq0 : shortWord f 0 = 11 := hp.1
  have hr0 : longWord L f 0 = 1 := hp.2.1
  have hq1 : carry (shortWord f) 1 = 1 := by simp [carry, hq0]
  have hr1 : carry (longWord L f) 1 = 0 := by simp [carry, hr0]
  have hc : ∀ i, 1 ≤ i → i ≤ L →
      (f i).u + carry (longWord L f) i = carry (shortWord f) i + 1 := by
    intro i
    induction i with
    | zero =>
        intro hi _
        omega
    | succ i ih =>
        intro _ hiL
        by_cases hi0 : i = 0
        · subst i
          simp [h.first, initial, hq1, hr1]
        · have hi : 1 ≤ i := by omega
          have hiL' : i < L := by omega
          have hin := ih hi (by omega)
          have hlow := (closed_columns h hi hiL').2
          exact (carry_step (shortWord f) (longWord L f) i
            (f i).u (f (i + 1)).u hin hlow).2
  refine ⟨hc, ?_⟩
  intro i hiL
  by_cases hi0 : i = 0
  · subst i
    simp [output, carry, hq0, hr0]
  · have hi : 1 ≤ i := by omega
    have hin := hc i hi (by omega)
    have hlow := (closed_columns h hi hiL).2
    exact (carry_step (shortWord f) (longWord L f) i
      (f i).u (f (i + 1)).u hin hlow).1

/-- A closed path forces the short word to overflow and the incoming
carry at the longer word's last coefficient to vanish. -/
theorem closed_terminal_carries
    {L : Nat} {f : Nat → State} (h : Closed L f) :
    carry (shortWord f) L = 1 ∧ carry (longWord L f) L = 0 := by
  obtain ⟨_, _, _, hqb, hrb, _, _⟩ := closed_word_properties h
  have hlength := h.length
  have hc := (closed_carry_outputs h).1 L (by omega) (Nat.le_refl L)
  have hlast : (f L).u = 2 := by rw [h.last]; rfl
  have hq := carry_bounded (shortWord f) L hqb L (Nat.le_refl L)
  have hr := carry_bounded (longWord L f) (L + 1) hrb L (by omega)
  omega

/-- The two reconstructed coefficient words have the same ordinary
positional value, even before the center conditions are imposed. -/
theorem closed_values_equal
    {L : Nat} {f : Nat → State} (h : Closed L f) :
    value (shortWord f) L = value (longWord L f) (L + 1) := by
  obtain ⟨hcq, hcr⟩ := closed_terminal_carries h
  have hrL : longWord L f L = 1 := (closed_word_properties h).2.2.1
  have hout := (closed_carry_outputs h).2
  have ho := value_congr (output (shortWord f)) (output (longWord L f)) L hout
  have hq := value_output (shortWord f) L
  have hr := value_output (longWord L f) L
  simp only [hcq, hcr, Nat.one_mul, Nat.zero_mul, Nat.add_zero] at hq hr
  simp only [value, hrL, Nat.one_mul]
  omega

/-- The actual carry differences of the reconstructed words recover
every supplied state on the full finite interval. -/
theorem closed_trace_recovered
    {L : Nat} {f : Nat → State} (h : Closed L f) :
    ∀ i, 1 ≤ i → i ≤ L →
      stateAt (shortWord f) (longWord L f) L i = f i := by
  have hc := (closed_carry_outputs h).1
  intro i hi hiL
  have hx : shortWord f (i - 1) = (f i).x := by
    simp only [shortWord, show i - 1 + 1 = i by omega]
  have hlu := hc i hi hiL
  have hu : carry (shortWord f) i + 1 - carry (longWord L f) i = (f i).u := by
    omega
  have hmirror : L + 1 - i = L - i + 1 := by omega
  have hflip : (f (L - i + 1)).u = (f i).v := by
    have hh := congrArg State.u (h.reflection i hi hiL)
    simpa only [hmirror, flip] using hh
  have hlv := hc (L - i + 1) (by omega) (by omega)
  have hv : carry (shortWord f) (L - i + 1) + 1 -
      carry (longWord L f) (L - i + 1) = (f i).v := by
    omega
  unfold stateAt
  rw [hx, hu, hv]

#print axioms closed_terminal_carries
#print axioms closed_values_equal
#print axioms closed_trace_recovered

end CrossWidthCollisionPaths
