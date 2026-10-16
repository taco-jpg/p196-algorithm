import Std

/-!
Exact local carry-complement identities and a checked obstruction to a
correlated folded-word candidate.  This file does not prove a Lychrel number
exists.  It imports no unproved research hypotheses.
-/

namespace AstraLanguages

def carry (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i + 1 => (q i + carry q i) / 10

def digit (q : Nat → Nat) (i : Nat) : Nat :=
  (q i + carry q i) % 10

theorem complementary_column (q r a b : Nat)
    (hq : q + r = 18) (ha : a + b = 1) :
    (q + a) / 10 + (r + b) / 10 = 1 ∧
    (q + a) % 10 + (r + b) % 10 = 9 := by
  omega

/-- Equal zero incoming carries are repaired at the first non-neutral
complementary pair.  At that pair the output digits sum to eight. -/
theorem mismatched_column_repair (q r : Nat)
    (hq : q + r = 18) (hne : q ≠ 9) :
    q / 10 + r / 10 = 1 ∧ q % 10 + r % 10 = 8 := by
  omega

theorem neutral_column_preserves_mismatch :
    9 / 10 + 9 / 10 = 0 ∧ 9 % 10 + 9 % 10 = 18 := by
  decide

/-- A half-word carry of one makes an anti-complementary q word produce
complementary digit halves, at every finite width. -/
theorem half_complement_carries (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) :
    ∀ i, i ≤ s → carry q i + carry q (s + i) = 1 := by
  intro i
  induction i with
  | zero =>
      intro _
      simpa [carry] using hm
  | succ i ih =>
      intro hi
      have ha := ih (by omega)
      have hx := (complementary_column (q i) (q (s + i))
        (carry q i) (carry q (s + i)) (hp i (by omega)) ha).1
      have hs : s + (i + 1) = (s + i) + 1 := by omega
      simpa only [hs, carry] using hx

theorem half_complement_digits (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) :
    ∀ i, i < s → digit q i + digit q (s + i) = 9 := by
  intro i hi
  exact (complementary_column (q i) (q (s + i))
    (carry q i) (carry q (s + i)) (hp i hi)
    (half_complement_carries q s hp hm i (by omega))).2

theorem half_complement_no_overflow (q : Nat → Nat) (s : Nat)
    (hp : ∀ i, i < s → q i + q (s + i) = 18)
    (hm : carry q s = 1) : carry q (2 * s) = 0 := by
  have hx := half_complement_carries q s hp hm s (by omega)
  have hs : s + s = 2 * s := by omega
  rw [hm, hs] at hx
  omega

def addColumns : List Nat → Nat → List Nat
  | [], 0 => []
  | [], c => [c]
  | q :: qs, c => (q + c) % 10 :: addColumns qs ((q + c) / 10)

def qstep (q : List Nat) : List Nat :=
  let d := addColumns q 0
  List.zipWith (fun a b => a + b) d d.reverse

def lowOnly (q : List Nat) : Prop := ∀ x ∈ q, x ≤ 9

/-- An anti-complementary folded seed with a nonzero marked adjacency
defect loses that defect and reaches the low-only bad language in four
exact q transitions. -/
theorem correlated_seed_counterexample :
    qstep [2,3,15,16,16,15,3,2] = [4,7,11,14,14,11,7,4] ∧
    qstep [4,7,11,14,14,11,7,4] = [8,15,3,10,10,3,15,8] ∧
    qstep [8,15,3,10,10,3,15,8] = [17,10,8,1,1,8,10,17] ∧
    qstep [17,10,8,1,1,8,10,17] = [8,9,9,9,2,9,9,9,8] ∧
    lowOnly [8,9,9,9,2,9,9,9,8] := by
  refine ⟨by decide, by decide, by decide, by decide, ?_⟩
  simp [lowOnly]

/-- Even in the odd-width correlated phase, a marked non-nine symbol
can disappear in a single non-overflow step. -/
theorem odd_marked_defect_counterexample :
    qstep [3,4,9,14,12,14,9,4,3] = [6,9,9,9,6,9,9,9,6] ∧
    lowOnly [6,9,9,9,6,9,9,9,6] := by
  refine ⟨by decide, ?_⟩
  simp [lowOnly]

#print axioms complementary_column
#print axioms mismatched_column_repair
#print axioms half_complement_carries
#print axioms half_complement_digits
#print axioms half_complement_no_overflow
#print axioms correlated_seed_counterexample
#print axioms odd_marked_defect_counterexample

end AstraLanguages
