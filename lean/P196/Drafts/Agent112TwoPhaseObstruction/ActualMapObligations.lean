import P196.Drafts.Agent104ReviewAgent4TemporalStrip.NoAlternatingReturn
import P196.Foundations.LychrelDigitSums

/-! Specification of MISSING bridges, not proofs or accepted new results.
The two final declarations merely define propositions. There is no axiom,
admitted theorem, or proof asserting either proposition.
These contracts expose precisely the carry, width, closure and interior-cut
conditions needed to apply Agent #4's abstract strip theorem to actual words.
Compilation would check the contracts' syntax and types, not their truth. -/
namespace Agent104.TemporalStripObligations
open P196.Agent4.TemporalStrip
open DecimalDigits FoldedDecimal OverflowCarryNormalization

def qAt (q : Nat → Nat) (L t : Nat) : Nat → Nat :=
  (iterPairs q L t).2

def widthAt (q : Nat → Nat) (L t : Nat) : Nat :=
  (iterPairs q L t).1

def cycleNext (N : Nat) (hN : 0 < N) (j : Fin N) : Fin N :=
  ⟨(j.val + 1) % N, Nat.mod_lt _ hN⟩

-- Even and odd refer to ordinary step numbers 2*j and 2*j+1.
-- Every high index uses THAT STEP'S actual width, not the initial width.
def actualCut (q : Nat → Nat) (L N i : Nat) : Cut (Fin N) where
  lowEven := fun j => carry (qAt q L (2*j.val)) i
  lowOdd := fun j => carry (qAt q L (2*j.val+1)) i
  highEven := fun j => carry (qAt q L (2*j.val))
    (widthAt q L (2*j.val) - i)
  highOdd := fun j => carry (qAt q L (2*j.val+1))
    (widthAt q L (2*j.val+1) - i)
  delayed := fun j => extended (qAt q L (2*j.val+1))
    (widthAt q L (2*j.val+1)) (widthAt q L (2*j.val+1) - i)

def actualEven (q : Nat → Nat) (L N i : Nat) (j : Fin N) : Nat :=
  qAt q L (2*j.val) i

def actualOdd (q : Nat → Nat) (L N i : Nat) (j : Fin N) : Nat :=
  qAt q L (2*j.val+1) i

/-- UNSUPPLIED bridge: exact ordinary pair evolution must instantiate ALL
strip equations, including the wrap from j=N-1 to j=0. The prefix equality
at time 2*N supplies that wrap; overflow alternation alone does not.
This proposition is intentionally not proved in this review. -/
def ActualPrefixTransportObligation : Prop :=
  ∀ (q : Nat → Nat) (L N width : Nat) (hN : 0 < N),
    Admissible L q →
    (∀ j : Fin N,
      width ≤ widthAt q L (2*j.val) ∧
      width ≤ widthAt q L (2*j.val+1)) →
    (∀ j : Fin N,
      carry (qAt q L (2*j.val)) (widthAt q L (2*j.val)) = 0 ∧
      carry (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1)) = 1) →
    (∀ i, i < width → qAt q L (2*N) i = q i) →
    (∀ i, i ≤ width → Valid (actualCut q L N i)) ∧
    (∀ i, i < width → Column (cycleNext N hN)
      (actualCut q L N i) (actualCut q L N (i+1))
      (actualEven q L N i) (actualOdd q L N i)) ∧
    Outside (actualCut q L N 0)

/-- UNSUPPLIED tail bridge: one common cut is strictly inside the relevant
constant band at EVERY temporal pair, with a common alignment. Two adjacent
constant columns reset the incoming carries on both sides of that cut.
Inferring this common cut from a returned quotient/template requires a
further argument about interface lengths and permissible gap choices.
This proposition is intentionally not proved in this review. -/
def UniformBandTailObligation : Prop :=
  ∀ (q : Nat → Nat) (L N width : Nat),
    Admissible L q → 0 < width →
    (∀ j : Fin N,
      width < widthAt q L (2*j.val) ∧
      width < widthAt q L (2*j.val+1)) →
    ((∀ j : Fin N,
      qAt q L (2*j.val) (width-1) = 6 ∧
      qAt q L (2*j.val) width = 6 ∧
      qAt q L (2*j.val+1) (width-1) = 12 ∧
      qAt q L (2*j.val+1) width = 12) ∨
     (∀ j : Fin N,
      qAt q L (2*j.val) (width-1) = 12 ∧
      qAt q L (2*j.val) width = 12 ∧
      qAt q L (2*j.val+1) (width-1) = 6 ∧
      qAt q L (2*j.val+1) width = 6)) →
    LeftAligned (actualCut q L N width) ∨
      RightAligned (actualCut q L N width)

/- The existing numeric bridge is
OverflowCarryNormalization.iterPairs_representation, supplied with
DecimalDigits.Canonical n d L and q = DecimalDigits.columnSum d L.
NormalizationBridge.canonical_admissible supplies admissibility.

Neither existing theorem proves the two propositions above, supplies a
returned prefix, or locates a common interior cut. Nor does the reviewed
file characterize which Agent109.Cert.Valid template certificates satisfy
those premises. No certificate exclusion or P196 result is asserted here.

Finite scope control: 15 -> 66 -> 132 has carries 0 then 1, and pair words
[6,6], [12,12], [3,6,3] (least significant first). The cut at width=1 is
inside the 6/12 columns, but the required prefix return 3=6 is false.
-/
end Agent104.TemporalStripObligations
