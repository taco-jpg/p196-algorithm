import ActualBoundary

/-!
Composition of the finite boundary transducer along the actual whole-word
orbit. Every control below is computed from iterPairs. The return guards
are hypotheses or equivalent conditions, not asserted invariants.
-/

namespace SevenStepOrbit

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196

def widthAt (q : Nat → Nat) (L t : Nat) : Nat := (iterPairs q L t).1
def boundaryAt (q : Nat → Nat) (L t : Nat) : Prefix := boundary (iterPairs q L t).2
def controlAt (q : Nat → Nat) (L t : Nat) : Bool :=
  actualControl (iterPairs q L t).2 (iterPairs q L t).1
def overflowAt (q : Nat → Nat) (L t : Nat) : Nat :=
  carry (iterPairs q L t).2 (iterPairs q L t).1
def innerCarryAt (q : Nat → Nat) (L t : Nat) : Nat :=
  carry (iterPairs q L t).2 ((iterPairs q L t).1 - 3)

def controls (q : Nat → Nat) (L a : Nat) : Nat → List Bool
  | 0 => []
  | n + 1 => controlAt q L a :: controls q L (a + 1) n

def actualTrace (q : Nat → Nat) (L a : Nat) : Nat → List Prefix
  | 0 => [boundaryAt q L a]
  | n + 1 => boundaryAt q L a :: actualTrace q L (a + 1) n

def actualOverflows (q : Nat → Nat) (L a : Nat) : Nat → List Nat
  | 0 => []
  | n + 1 => overflowAt q L a :: actualOverflows q L (a + 1) n

theorem widthAt_lower (q : Nat → Nat) (L t : Nat) : L ≤ widthAt q L t := by
  induction t with
  | zero => exact Nat.le_refl _
  | succ t ih =>
    change L ≤ nextWidth (iterPairs q L t).2 (iterPairs q L t).1
    unfold nextWidth
    change L ≤ (iterPairs q L t).1 at ih
    split <;> omega

/-- Exact boundary and overflow recurrence at every actual orbit index. -/
theorem actual_step_at (q : Nat → Nat) (L t : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    (boundaryAt q L (t + 1), overflowAt q L t) =
      BoundaryTransducer.step (boundaryAt q L t) (controlAt q L t) := by
  have hw := widthAt_lower q L t
  exact actual_boundary_step (iterPairs q L t).2 (iterPairs q L t).1
    (by change L ≤ (iterPairs q L t).1 at hw; omega)
    (iterPairs_admissible q L t ha)

theorem run_actual (q : Nat → Nat) (L a n : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    run (boundaryAt q L a) (controls q L a n) = boundaryAt q L (a + n) := by
  induction n generalizing a with
  | zero => rfl
  | succ n ih =>
    have hs := congrArg Prod.fst (actual_step_at q L a hL ha)
    simp only [Prod.fst] at hs
    simp only [controls, run]
    rw [← hs, ih (a + 1)]
    congr 1
    omega

theorem trace_actual (q : Nat → Nat) (L a n : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    trace (boundaryAt q L a) (controls q L a n) = actualTrace q L a n := by
  induction n generalizing a with
  | zero => rfl
  | succ n ih =>
    have hs := congrArg Prod.fst (actual_step_at q L a hL ha)
    simp only [Prod.fst] at hs
    simp only [controls, trace, actualTrace]
    rw [← hs, ih (a + 1)]

theorem overflows_actual (q : Nat → Nat) (L a n : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    overflows (boundaryAt q L a) (controls q L a n) = actualOverflows q L a n := by
  induction n generalizing a with
  | zero => rfl
  | succ n ih =>
    have hs := congrArg Prod.fst (actual_step_at q L a hL ha)
    have he := congrArg Prod.snd (actual_step_at q L a hL ha)
    simp only [Prod.fst] at hs
    simp only [Prod.snd] at he
    simp only [controls, overflows, actualOverflows]
    rw [← hs, ← he, ih (a + 1)]

def SevenGuards (q : Nat → Nat) (L : Nat) : Prop :=
  controlAt q L 0 = false ∧ controlAt q L 1 = false ∧
  controlAt q L 3 = false ∧ controlAt q L 5 = false ∧ controlAt q L 6 = true

/-- Exact seven-step return criterion for the actual pair-word orbit. -/
theorem seven_return_iff (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial) :
    boundaryAt q L 7 = initial ↔ SevenGuards q L := by
  have hr := run_actual q L 0 7 hL ha
  change run (boundary q)
    [controlAt q L 0, controlAt q L 1, controlAt q L 2, controlAt q L 3,
      controlAt q L 4, controlAt q L 5, controlAt q L 6] = boundaryAt q L 7 at hr
  rw [hinit] at hr
  rw [← hr]
  exact BoundaryTransducer.seven_return_iff _ _ _ _ _ _ _

theorem seven_guards_iff_carries (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    SevenGuards q L ↔ innerCarryAt q L 0 = 0 ∧ innerCarryAt q L 1 = 0 ∧
      innerCarryAt q L 3 = 0 ∧ innerCarryAt q L 5 = 0 ∧ innerCarryAt q L 6 = 1 := by
  simp only [SevenGuards, controlAt, innerCarryAt,
    actualControl_false_iff _ _ (iterPairs_admissible q L 0 ha),
    actualControl_false_iff _ _ (iterPairs_admissible q L 1 ha),
    actualControl_false_iff _ _ (iterPairs_admissible q L 3 ha),
    actualControl_false_iff _ _ (iterPairs_admissible q L 5 ha),
    actualControl_true_iff]

theorem seven_return_iff_actual_carries (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial) :
    boundaryAt q L 7 = initial ↔ innerCarryAt q L 0 = 0 ∧ innerCarryAt q L 1 = 0 ∧
      innerCarryAt q L 3 = 0 ∧ innerCarryAt q L 5 = 0 ∧ innerCarryAt q L 6 = 1 :=
  (seven_return_iff q L hL ha hinit).trans (seven_guards_iff_carries q L ha)

theorem seven_trace_of_guards (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial)
    (hg : SevenGuards q L) :
    actualTrace q L 0 7 =
      [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] := by
  have hr := trace_actual q L 0 7 hL ha
  change trace (boundary q)
    [controlAt q L 0, controlAt q L 1, controlAt q L 2, controlAt q L 3,
      controlAt q L 4, controlAt q L 5, controlAt q L 6] = actualTrace q L 0 7 at hr
  rw [hinit] at hr
  rw [← hr]
  exact seven_trace_of_controls _ _ _ _ _ _ _ hg

theorem seven_overflows_of_guards (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial)
    (hg : SevenGuards q L) : actualOverflows q L 0 7 = [0, 0, 1, 0, 1, 0, 1] := by
  have hr := overflows_actual q L 0 7 hL ha
  change overflows (boundary q)
    [controlAt q L 0, controlAt q L 1, controlAt q L 2, controlAt q L 3,
      controlAt q L 4, controlAt q L 5, controlAt q L 6] = actualOverflows q L 0 7 at hr
  rw [hinit] at hr
  rw [← hr]
  exact seven_overflows_of_controls _ _ _ _ _ _ _ hg

theorem widthAt_succ (q : Nat → Nat) (L t : Nat) (ha : Admissible L q) :
    widthAt q L (t + 1) = widthAt q L t + overflowAt q L t := by
  have had := iterPairs_admissible q L t ha
  have hb := carry_bounded (iterPairs q L t).2 (iterPairs q L t).1 had.2.2.1
    (iterPairs q L t).1 (Nat.le_refl _)
  change nextWidth (iterPairs q L t).2 (iterPairs q L t).1 =
    (iterPairs q L t).1 + carry (iterPairs q L t).2 (iterPairs q L t).1
  unfold nextWidth
  split <;> omega

theorem widthAt_add_overflows (q : Nat → Nat) (L a n : Nat)
    (ha : Admissible L q) :
    widthAt q L (a + n) = widthAt q L a + (actualOverflows q L a n).sum := by
  induction n generalizing a with
  | zero => simp [actualOverflows]
  | succ n ih =>
    have hindex : a + (n + 1) = (a + 1) + n := by omega
    rw [hindex, ih (a + 1), widthAt_succ q L a ha]
    simp only [actualOverflows, List.sum_cons]
    omega

/-- The seven return transitions increase the actual finite width by three. -/
theorem seven_width_of_guards (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial)
    (hg : SevenGuards q L) : widthAt q L 7 = L + 3 := by
  have hw := widthAt_add_overflows q L 0 7 ha
  rw [seven_overflows_of_guards q L hL ha hinit hg] at hw
  simpa only [Nat.zero_add, widthAt, iterPairs, List.sum_cons, List.sum_nil,
    Nat.add_zero] using hw

/-- A return condition supplies an actual canonical representation of the
seventh numeric iterate, with the returned boundary and exact new width. -/
theorem seven_numeric_representation (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hL : 6 ≤ L) (hinit : boundary q = initial)
    (hg : SevenGuards q L) :
    ∃ e, Canonical (orbit n 7) e (L + 3) ∧ boundary (columnSum e (L + 3)) = initial := by
  have ha : Admissible L q := NormalizationBridge.admissible_congr _ _ _
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  obtain ⟨e, he, her⟩ := iterPairs_representation n d q L 7 hc hrep
  have hw := seven_width_of_guards q L hL ha hinit hg
  change (iterPairs q L 7).1 = L + 3 at hw
  rw [hw] at he her
  have hr := (seven_return_iff q L hL ha hinit).mpr hg
  have hb : boundary (columnSum e (L + 3)) = boundaryAt q L 7 := by
    unfold boundaryAt boundary
    rw [her 0 (by omega), her 1 (by omega), her 2 (by omega)]
  exact ⟨e, he, hb.trans hr⟩

theorem seven_numeric_decimalLength (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hL : 6 ≤ L) (hinit : boundary q = initial)
    (hg : SevenGuards q L) : DecimalQuantitativeMass.decimalLength (orbit n 7) = L + 3 := by
  obtain ⟨e, he, _⟩ := seven_numeric_representation n d q L hc hrep hL hinit hg
  exact DecimalQuantitativeMass.decimalLength_of_canonical _ e _ he

#print axioms seven_return_iff_actual_carries
#print axioms seven_overflows_of_guards
#print axioms seven_width_of_guards
#print axioms seven_numeric_representation
#print axioms seven_numeric_decimalLength

end SevenStepOrbit
