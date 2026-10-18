import P196.Drafts.D20261014CollisionMassCarryResponseMass.CarryResponseMass

/-!
Exact digit-mass response for every finite consecutive partition.
Boundary positions may repeat, so empty blocks are included. Each block
retains its outgoing carry; no terminal carry is discarded. The correction
uses the incoming carry of the actual whole word and the computable initial
nine-run length. This is a one-step identity, not a persistence statement.
-/

namespace Agent107.PartitionMass

open IncomingCarry CarryResponseMass DecimalDigits DecimalMass
  DecimalUnboundedMass Lychrel196 FoldedDecimal OverflowCarryNormalization

def blockLength (boundary : Nat → Nat) (j : Nat) : Nat :=
  boundary (j + 1) - boundary j

def blockWord (q boundary : Nat → Nat) (j i : Nat) : Nat :=
  q (boundary j + i)

/-- The number of neutral columns affected by this block's actual input carry. -/
def blockDeficit (q boundary : Nat → Nat) (j : Nat) : Nat :=
  carryIn q 0 (boundary j) *
    initialNinesLength (blockWord q boundary j) (blockLength boundary j)

def seamMass (q boundary : Nat → Nat) (k : Nat) : Nat :=
  wordSum (blockDeficit q boundary) k

/-- Sum of independent zero-input-carry block masses, including terminal carries. -/
def isolatedMass (q boundary : Nat → Nat) (k : Nat) : Nat :=
  wordSum (fun j => massIn (blockWord q boundary j) 0 (blockLength boundary j)) k

/-- Arbitrarily many blocks, including empty and all-nine blocks. The first
block's incoming carry is zero; all other incoming carries are actual. -/
theorem partition_collision_mass (q boundary : Nat → Nat) (k : Nat)
    (hzero : boundary 0 = 0)
    (hmono : ∀ j, j < k → boundary j ≤ boundary (j + 1))
    (hq : ∀ i, i < boundary k → q i ≤ 18) :
    massIn q 0 (boundary k) + 9 * seamMass q boundary k =
      isolatedMass q boundary k := by
  revert hmono hq
  induction k with
  | zero =>
      intro _ _
      simp [hzero, massIn, seamMass, isolatedMass, wordSum, carryIn]
  | succ k ih =>
      intro hmono hq
      have hstep := hmono k (by omega)
      have hp := ih (fun j hj => hmono j (by omega))
        (fun i hi => hq i (by omega))
      have hlen : boundary k + blockLength boundary k = boundary (k + 1) := by
        unfold blockLength
        omega
      have hadd := massIn_add q 0 (boundary k) (blockLength boundary k)
      rw [hlen] at hadd
      have hc : carryIn q 0 (boundary k) ≤ 1 :=
        carryIn_bounded q 0 (boundary k) (by omega)
          (fun i hi => hq i (by omega))
      have hresponse := massIn_response_computable (blockWord q boundary k)
        (blockLength boundary k) (carryIn q 0 (boundary k))
        (by
          intro i hi
          exact hq (boundary k + i) (by omega)) hc
      change massIn q 0 (boundary (k + 1)) +
        9 * (seamMass q boundary k + blockDeficit q boundary k) =
        isolatedMass q boundary k +
          massIn (blockWord q boundary k) 0 (blockLength boundary k)
      change massIn q 0 (boundary (k + 1)) + carryIn q 0 (boundary k) =
        massIn q 0 (boundary k) +
          massIn (blockWord q boundary k) (carryIn q 0 (boundary k))
            (blockLength boundary k) at hadd
      simp only [Nat.mul_assoc] at hresponse
      unfold blockDeficit
      omega

/-- The whole-word mass in the identity is the digit sum of the actual step. -/
theorem actual_step_partition_collision_mass
    (n : Nat) (d boundary : Nat → Nat) (k : Nat)
    (hc : Canonical n d (boundary k))
    (hzero : boundary 0 = 0)
    (hmono : ∀ j, j < k → boundary j ≤ boundary (j + 1)) :
    digitSum (step n) + 9 * seamMass (columnSum d (boundary k)) boundary k =
      isolatedMass (columnSum d (boundary k)) boundary k := by
  have h := partition_collision_mass (columnSum d (boundary k)) boundary k
    hzero hmono (columnSum_bounded d (boundary k) hc.2.1)
  rw [massIn_actual_step n d (boundary k) hc] at h
  exact h

/-- Pair-coefficient mass is twice digit mass, so its exact deficit is 18
per affected neutral column. The width is the actual overflow-selected width. -/
theorem actual_step_partition_pair_mass
    (n : Nat) (d boundary : Nat → Nat) (k : Nat)
    (hc : Canonical n d (boundary k))
    (hzero : boundary 0 = 0)
    (hmono : ∀ j, j < k → boundary j ≤ boundary (j + 1)) :
    wordSum (nextColumns (columnSum d (boundary k)) (boundary k))
        (nextWidth (columnSum d (boundary k)) (boundary k)) +
      18 * seamMass (columnSum d (boundary k)) boundary k =
      2 * isolatedMass (columnSum d (boundary k)) boundary k := by
  have hm := congrArg (fun x : Nat => 2 * x)
    (actual_step_partition_collision_mass n d boundary k hc hzero hmono)
  have hp := iterPairs_wordSum n d (columnSum d (boundary k)) (boundary k) 1
    hc (fun _ _ => rfl)
  change wordSum (nextColumns (columnSum d (boundary k)) (boundary k))
      (nextWidth (columnSum d (boundary k)) (boundary k)) =
      2 * digitSum (step n) at hp
  rw [hp]
  simpa only [Nat.mul_add, ← Nat.mul_assoc] using hm

private theorem wordSum_eq_zero_iff (f : Nat → Nat) (k : Nat) :
    wordSum f k = 0 ↔ ∀ j, j < k → f j = 0 := by
  induction k with
  | zero => simp [wordSum]
  | succ k ih =>
      constructor
      · intro h j hj
        have hprefix : wordSum f k = 0 := by
          rw [wordSum] at h
          omega
        have hlast : f k = 0 := by
          rw [wordSum] at h
          omega
        by_cases hjk : j < k
        · exact ih.mp hprefix j hjk
        · have he : j = k := by omega
          simpa only [he] using hlast
      · intro h
        rw [wordSum, ih.mpr (fun j hj => h j (by omega)), h k (by omega)]

/-- Zero loss is equivalent to every actual incoming-carry/run product
vanishing, not merely to a condition on a selected pair of seams. -/
theorem partition_collision_mass_eq_iff (q boundary : Nat → Nat) (k : Nat)
    (hzero : boundary 0 = 0)
    (hmono : ∀ j, j < k → boundary j ≤ boundary (j + 1))
    (hq : ∀ i, i < boundary k → q i ≤ 18) :
    massIn q 0 (boundary k) = isolatedMass q boundary k ↔
      ∀ j, j < k → carryIn q 0 (boundary j) *
        initialNinesLength (blockWord q boundary j) (blockLength boundary j) = 0 := by
  have hm := partition_collision_mass q boundary k hzero hmono hq
  constructor
  · intro he
    have hz : seamMass q boundary k = 0 := by omega
    exact (wordSum_eq_zero_iff (blockDeficit q boundary) k).mp hz
  · intro h
    have hz : seamMass q boundary k = 0 :=
      (wordSum_eq_zero_iff (blockDeficit q boundary) k).mpr h
    omega

theorem actual_step_partition_collision_mass_eq_iff
    (n : Nat) (d boundary : Nat → Nat) (k : Nat)
    (hc : Canonical n d (boundary k))
    (hzero : boundary 0 = 0)
    (hmono : ∀ j, j < k → boundary j ≤ boundary (j + 1)) :
    digitSum (step n) = isolatedMass (columnSum d (boundary k)) boundary k ↔
      ∀ j, j < k → carryIn (columnSum d (boundary k)) 0 (boundary j) *
        initialNinesLength (blockWord (columnSum d (boundary k)) boundary j)
          (blockLength boundary j) = 0 := by
  have h := partition_collision_mass_eq_iff (columnSum d (boundary k)) boundary k
    hzero hmono (columnSum_bounded d (boundary k) hc.2.1)
  rw [massIn_actual_step n d (boundary k) hc] at h
  exact h

#print axioms partition_collision_mass
#print axioms actual_step_partition_collision_mass
#print axioms actual_step_partition_pair_mass
#print axioms partition_collision_mass_eq_iff
#print axioms actual_step_partition_collision_mass_eq_iff

end Agent107.PartitionMass
