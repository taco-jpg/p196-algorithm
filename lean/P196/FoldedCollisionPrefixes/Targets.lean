import P196.FoldedCollisionPrefixes.Even
import P196.FoldedCollisionPrefixes.Odd
import P196.CrossWidthCollisionPaths.Realization

/-!
# Finite collision prefixes and ordinary common targets

For each specified pair of adjacent source widths, the accepted finite
prefix tuples parametrize exactly the ordinary common reverse-and-add
outputs. The value map is injective on accepted tuples. The construction
reuses the full-path realization and value-injectivity theorems; it does
not assert uniqueness of the original source digit splits.
-/

set_option autoImplicit false

namespace FoldedCollisionPrefixes

open DecimalDigits Lychrel196 CrossWidthCollisionStates CrossWidthCollisionPaths

/-- An ordinary output attained by canonical sources at both adjacent widths. -/
def CommonTarget (L Y : Nat) : Prop :=
  ∃ (n m : Nat) (d e : Nat → Nat),
    Canonical n d L ∧ Canonical m e (L + 1) ∧
    step n = Y ∧ step m = Y

/-- The ordinary value attached to an even-shorter-width prefix. -/
def evenValue (k : Nat) (p : Prefix k) : Nat :=
  pathValue (2 * k + 2) (evenTrace k p)

/-- The ordinary value attached to an odd-shorter-width prefix. -/
def oddValue (k : Nat) (p : Prefix (k + 1)) : Nat :=
  pathValue (2 * k + 3) (oddTrace k p)

private theorem commonTarget_of_valid
    {L Y : Nat} {f : Nat → State}
    (h : Valid L f) (hy : pathValue L f = Y) : CommonTarget L Y := by
  obtain ⟨n, m, d, e, hn, hm, hstep, htrace⟩ :=
    (valid_iff_realized L f).mp h
  have hvalue := pathValue_eq_step hn hm hstep htrace
  have hnY : step n = Y := hvalue.symm.trans hy
  exact ⟨n, m, d, e, hn, hm, hnY, hstep.symm.trans hnY⟩

/-- Accepted even prefixes give exactly all common ordinary targets at
shorter width 2*k+2. -/
theorem even_targets_iff (k Y : Nat) :
    CommonTarget (2 * k + 2) Y ↔
      ∃ p : Prefix k, EvenAccepted k p ∧ evenValue k p = Y := by
  constructor
  · rintro ⟨n, m, d, e, hn, hm, hnY, hmY⟩
    have hstep : step n = step m := hnY.trans hmY.symm
    let f := stateAt (columnSum d (2 * k + 2))
      (columnSum e (2 * k + 2 + 1)) (2 * k + 2)
    have hv : Valid (2 * k + 2) f :=
      actual_trace_valid hn hm hstep (fun _ _ _ => rfl)
    refine ⟨takePrefix k f, evenAccepted_take hv, ?_⟩
    have htrace : ∀ i, 1 ≤ i → i ≤ 2 * k + 2 →
        stateAt (columnSum d (2 * k + 2))
          (columnSum e (2 * k + 2 + 1)) (2 * k + 2) i =
            evenTrace k (takePrefix k f) i := by
      intro i hi hiL
      exact (evenTrace_take hv.toClosed i hi hiL).symm
    exact (pathValue_eq_step hn hm hstep htrace).trans hnY
  · rintro ⟨p, hp, hy⟩
    exact commonTarget_of_valid ((even_valid_iff k p).mp hp) hy

/-- Accepted odd prefixes give exactly all common ordinary targets at
shorter width 2*k+3. -/
theorem odd_targets_iff (k Y : Nat) :
    CommonTarget (2 * k + 3) Y ↔
      ∃ p : Prefix (k + 1), OddAccepted k p ∧ oddValue k p = Y := by
  constructor
  · rintro ⟨n, m, d, e, hn, hm, hnY, hmY⟩
    have hstep : step n = step m := hnY.trans hmY.symm
    let f := stateAt (columnSum d (2 * k + 3))
      (columnSum e (2 * k + 3 + 1)) (2 * k + 3)
    have hv : Valid (2 * k + 3) f :=
      actual_trace_valid hn hm hstep (fun _ _ _ => rfl)
    refine ⟨takePrefix (k + 1) f, oddAccepted_take hv, ?_⟩
    have htrace : ∀ i, 1 ≤ i → i ≤ 2 * k + 3 →
        stateAt (columnSum d (2 * k + 3))
          (columnSum e (2 * k + 3 + 1)) (2 * k + 3) i =
            oddTrace k (takePrefix (k + 1) f) i := by
      intro i hi hiL
      exact (oddTrace_take hv.toClosed i hi hiL).symm
    exact (pathValue_eq_step hn hm hstep htrace).trans hnY
  · rintro ⟨p, hp, hy⟩
    exact commonTarget_of_valid ((odd_valid_iff k p).mp hp) hy

/-- At a fixed even shorter width, the ordinary output determines the
entire accepted finite tuple. -/
theorem even_value_eq_iff {k : Nat} {p q : Prefix k}
    (hp : EvenAccepted k p) (hq : EvenAccepted k q) :
    evenValue k p = evenValue k q ↔ p = q := by
  constructor
  · intro hvalue
    have he := (pathValue_eq_iff ((even_valid_iff k p).mp hp)
      ((even_valid_iff k q).mp hq)).mp hvalue
    calc
      p = takePrefix k (evenTrace k p) := (takePrefix_evenTrace k p).symm
      _ = takePrefix k (evenTrace k q) := by
        funext i
        exact he (i.val + 1) (by omega) (by have := i.isLt; omega)
      _ = q := takePrefix_evenTrace k q
  · rintro rfl
    rfl

/-- At a fixed odd shorter width, the ordinary output determines the
entire accepted finite tuple. -/
theorem odd_value_eq_iff {k : Nat} {p q : Prefix (k + 1)}
    (hp : OddAccepted k p) (hq : OddAccepted k q) :
    oddValue k p = oddValue k q ↔ p = q := by
  constructor
  · intro hvalue
    have he := (pathValue_eq_iff ((odd_valid_iff k p).mp hp)
      ((odd_valid_iff k q).mp hq)).mp hvalue
    calc
      p = takePrefix (k + 1) (oddTrace k p) := (takePrefix_oddTrace k p).symm
      _ = takePrefix (k + 1) (oddTrace k q) := by
        funext i
        exact he (i.val + 1) (by omega) (by have := i.isLt; omega)
      _ = q := takePrefix_oddTrace k q
  · rintro rfl
    rfl

end FoldedCollisionPrefixes

#print axioms FoldedCollisionPrefixes.CommonTarget
#print axioms FoldedCollisionPrefixes.evenValue
#print axioms FoldedCollisionPrefixes.oddValue
#print axioms FoldedCollisionPrefixes.even_targets_iff
#print axioms FoldedCollisionPrefixes.odd_targets_iff
#print axioms FoldedCollisionPrefixes.even_value_eq_iff
#print axioms FoldedCollisionPrefixes.odd_value_eq_iff
