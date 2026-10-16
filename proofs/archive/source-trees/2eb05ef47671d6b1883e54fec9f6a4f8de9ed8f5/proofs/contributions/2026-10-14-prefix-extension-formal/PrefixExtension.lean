import LychrelDigitSums

/-!
Exact necessary one-column extension relation for actual finite decimal
pair words. The low outgoing carry advances in space within one addition;
it is not the low incoming carry at the next orbit time. Every witness
used by the actual-word and iterated theorems is a computed actual carry.
-/

namespace PrefixExtension

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory Lychrel196

/-- The emission used by the finite prefix-extension graph. -/
def nextCoefficient (previous a alpha gamma overflow v : Nat) : Nat :=
  (a + alpha) % 10 +
    if overflow = 0 then (a + v) % 10 else (previous + gamma) % 10

/-- One proposed deeper carry and its exact local consistency equations. -/
def ExtensionChoice (previous a alpha gamma overflow next lowOut v : Nat) : Prop :=
  gamma = (a + v) / 10 ∧
  next = nextCoefficient previous a alpha gamma overflow v ∧
  lowOut = (a + alpha) / 10

/-- The graph may existentially forget the deeper actual carry. This is
a necessary local relation; no converse global realizability is asserted. -/
def ExtensionEdge (previous a alpha gamma overflow next lowOut : Nat) : Prop :=
  ∃ v, v ≤ 1 ∧ ExtensionChoice previous a alpha gamma overflow next lowOut v

/-- The formula is valid at every positive old-word index, even before
the stronger disjoint-boundary width assumption is imposed. -/
theorem actual_extension_formula (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk0 : 0 < k) (hk : k < L) :
    carry q (L - k) = (q k + carry q (L - 1 - k)) / 10 ∧
    nextColumns q L k = nextCoefficient (q (k - 1)) (q k)
      (carry q k) (carry q (L - k)) (carry q L) (carry q (L - 1 - k)) ∧
    carry q (k + 1) = (q k + carry q k) / 10 := by
  have hcarry := folded_carry_transition q L k hk ha.2.2.2.1
  refine ⟨hcarry.2, ?_, hcarry.1⟩
  by_cases ho : carry q L = 0
  · simpa only [nextCoefficient, ho, if_true] using
      folded_emission_no_overflow q L k hk ha.2.2.2.1 ho
  · have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
    have hone : carry q L = 1 := by omega
    have hsym : q (L - k) = q (k - 1) := by
      have hs := (ha.2.2.2.1 (k - 1) (by omega)).symm
      have hi : L - 1 - (k - 1) = L - k := by omega
      simpa only [hi] using hs
    have he := folded_emission_overflow q L k hk hone
    simpa only [nextCoefficient, ho, if_false, extended,
      show L - k < L by omega, if_true, output, hsym] using he

/-- Exact extension with the actual deeper carry. Overlapping lower and
upper positions introduce correlations but do not invalidate necessity. -/
theorem actual_extension_choice (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : 1 ≤ k) (hwidth : k < L) :
    ExtensionChoice (q (k - 1)) (q k) (carry q k) (carry q (L - k)) (carry q L)
      (nextColumns q L k) (carry q (k + 1)) (carry q (L - 1 - k)) :=
  actual_extension_formula q L k ha (by omega) (by omega)

theorem actual_extension_edge (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : 1 ≤ k) (hwidth : k < L) :
    ExtensionEdge (q (k - 1)) (q k) (carry q k) (carry q (L - k)) (carry q L)
      (nextColumns q L k) (carry q (k + 1)) := by
  exact ⟨carry q (L - 1 - k), carry_bounded q L ha.2.2.1 _ (by omega),
    actual_extension_choice q L k ha hk hwidth⟩

/-- Exact finite enumeration: there are only the two deeper-carry choices. -/
theorem extensionEdge_iff_zero_or_one (previous a alpha gamma overflow next lowOut : Nat) :
    ExtensionEdge previous a alpha gamma overflow next lowOut ↔
      ExtensionChoice previous a alpha gamma overflow next lowOut 0 ∨
      ExtensionChoice previous a alpha gamma overflow next lowOut 1 := by
  constructor
  · rintro ⟨v, hv, hc⟩
    by_cases hz : v = 0
    · exact Or.inl (by simpa only [hz] using hc)
    · have ho : v = 1 := by omega
      exact Or.inr (by simpa only [ho] using hc)
  · rintro (hc | hc)
    · exact ⟨0, by omega, hc⟩
    · exact ⟨1, by omega, hc⟩

/-- All local quantities lie in the finite ranges used by the graph. -/
theorem actual_extension_bounds (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : 1 ≤ k) (hwidth : k < L) :
    q (k - 1) ≤ 18 ∧ q k ≤ 18 ∧ carry q k ≤ 1 ∧
    carry q (L - 1 - k) ≤ 1 ∧ carry q (L - k) ≤ 1 ∧ carry q L ≤ 1 ∧
    nextColumns q L k ≤ 18 ∧ carry q (k + 1) ≤ 1 := by
  have hnext := NormalizationBridge.admissible_next q L ha
  have hnwidth : k < nextWidth q L := by
    unfold nextWidth
    split <;> omega
  exact ⟨ha.2.2.1 _ (by omega), ha.2.2.1 _ (by omega),
    carry_bounded q L ha.2.2.1 _ (by omega),
    carry_bounded q L ha.2.2.1 _ (by omega),
    carry_bounded q L ha.2.2.1 _ (by omega),
    carry_bounded q L ha.2.2.1 _ (by omega), hnext.2.2.1 k hnwidth,
    carry_bounded q L ha.2.2.1 _ (by omega)⟩

private theorem width_ge_initial (q : Nat → Nat) (L t : Nat) :
    L ≤ (iterPairs q L t).1 := by
  induction t with
  | zero => exact Nat.le_refl _
  | succ t ih =>
    change L ≤ nextWidth (iterPairs q L t).2 (iterPairs q L t).1
    unfold nextWidth
    split <;> omega

/-- Every transition of an actual whole-word orbit supplies a graph edge
using its own actual interior carries and overflow bit. -/
theorem iterated_extension_edge (q : Nat → Nat) (L k t : Nat)
    (ha : Admissible L q) (hk : 1 ≤ k) (hwidth : k < L) :
    ExtensionEdge ((iterPairs q L t).2 (k - 1)) ((iterPairs q L t).2 k)
      (carry (iterPairs q L t).2 k)
      (carry (iterPairs q L t).2 ((iterPairs q L t).1 - k))
      (carry (iterPairs q L t).2 (iterPairs q L t).1)
      ((iterPairs q L (t + 1)).2 k) (carry (iterPairs q L t).2 (k + 1)) := by
  have hw := width_ge_initial q L t
  exact actual_extension_edge (iterPairs q L t).2 (iterPairs q L t).1 k
    (iterPairs_admissible q L t ha) hk (by omega)

/-- Both graph choices cannot be excluded for an actual finite word. -/
theorem actual_extension_not_both_excluded (q : Nat → Nat) (L k : Nat)
    (ha : Admissible L q) (hk : 1 ≤ k) (hwidth : k < L) :
    ¬ (¬ ExtensionChoice (q (k - 1)) (q k) (carry q k) (carry q (L - k)) (carry q L)
        (nextColumns q L k) (carry q (k + 1)) 0 ∧
      ¬ ExtensionChoice (q (k - 1)) (q k) (carry q k) (carry q (L - k)) (carry q L)
        (nextColumns q L k) (carry q (k + 1)) 1) := by
  have he := (extensionEdge_iff_zero_or_one _ _ _ _ _ _ _).mp
    (actual_extension_edge q L k ha hk hwidth)
  rintro ⟨h0, h1⟩
  exact he.elim h0 h1

/-- The next graph coefficient is an actual digit-pair coefficient of
the ordinary integer step, with canonical representation supplied. -/
theorem numeric_extension_realization (n : Nat) (d : Nat → Nat) (L k : Nat)
    (hc : Canonical n d L) (hk : 1 ≤ k) (hwidth : k < L) :
    ∃ e, Canonical (step n) e (nextWidth (columnSum d L) L) ∧
      ExtensionEdge (columnSum d L (k - 1)) (columnSum d L k)
        (carry (columnSum d L) k) (carry (columnSum d L) (L - k))
        (carry (columnSum d L) L)
        (columnSum e (nextWidth (columnSum d L) L) k)
        (carry (columnSum d L) (k + 1)) := by
  obtain ⟨e, he, hr⟩ := representation_next n d (columnSum d L) L hc (fun i hi => rfl)
  refine ⟨e, he, ?_⟩
  have hknew : k < nextWidth (columnSum d L) L := by
    unfold nextWidth
    split <;> omega
  rw [hr k hknew]
  exact actual_extension_edge (columnSum d L) L k
    (NormalizationBridge.canonical_admissible n d L hc) hk hwidth

#print axioms actual_extension_formula
#print axioms actual_extension_edge
#print axioms iterated_extension_edge
#print axioms numeric_extension_realization

end PrefixExtension
