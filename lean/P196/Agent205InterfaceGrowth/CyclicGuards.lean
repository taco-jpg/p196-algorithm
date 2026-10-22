import Std

/-!
Agent #205: exact elimination of cyclic run-length lower bounds.

The input is a finite cycle of signed increments, with a specified lower
threshold at each phase.  Cyclic lower bounds exist exactly when the total
increment is nonnegative.  A computable maximum of prefix deficits is the
least initial reserve for a concrete traversal, and suffices for every later
traversal when the total increment is nonnegative.

This is a generic integer-arithmetic result.  It supplies neither a decimal
interface cycle nor a return-certificate instance or palindrome-free seed.
-/

namespace Agent205.CyclicGuards

/-- Sum of the first `n` signed increments. -/
def partialSum (a : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => partialSum a n + a n

/-- A two-argument integer maximum, with its definition kept transparent. -/
def maxInt (a b : Int) : Int := if a ≤ b then b else a

theorem maxInt_le_iff (a b x : Int) :
    maxInt a b ≤ x ↔ a ≤ x ∧ b ≤ x := by
  unfold maxInt
  split <;> omega

/-- The maximum guard deficit over phases `0,...,n`. -/
def reserve (a h : Nat → Int) : Nat → Int
  | 0 => h 0
  | n + 1 => maxInt (reserve a h n) (h (n + 1) - partialSum a (n + 1))

/-- Exact minimality of the prefix-deficit reserve. -/
theorem reserve_le_iff (a h : Nat → Int) (n : Nat) (x : Int) :
    reserve a h n ≤ x ↔ ∀ i, i ≤ n → h i ≤ x + partialSum a i := by
  induction n with
  | zero =>
      constructor
      · intro hx i hi
        have hi0 : i = 0 := by omega
        subst i
        simpa [reserve, partialSum] using hx
      · intro hx
        simpa [reserve, partialSum] using hx 0 (by omega)
  | succ n ih =>
      rw [reserve, maxInt_le_iff, ih]
      constructor
      · rintro ⟨hx, hn⟩ i hi
        by_cases hin : i ≤ n
        · exact hx i hin
        · have hie : i = n + 1 := by omega
          subst i
          omega
      · intro hx
        constructor
        · intro i hi
          exact hx i (by omega)
        · have hn := hx (n + 1) (by omega)
          omega

/-- The least initial value meeting all phase guards in one positive cycle. -/
theorem initial_reserve_iff (a h : Nat → Int) (P : Nat) (hP : 0 < P)
    (x : Int) :
    reserve a h (P - 1) ≤ x ↔ ∀ i, i < P → h i ≤ x + partialSum a i := by
  rw [reserve_le_iff]
  constructor
  · intro hx i hi
    exact hx i (by omega)
  · intro hx i hi
    exact hx i (by omega)

/-- Summing upper bounds on successive increments bounds the endpoint. -/
theorem path_bound (a x : Nat → Int) (n : Nat)
    (hx : ∀ i, i < n → x (i + 1) ≤ x i + a i) :
    x n ≤ x 0 + partialSum a n := by
  induction n with
  | zero => simp [partialSum]
  | succ n ih =>
      have hn := ih (fun i hi => hx i (by omega))
      have hs := hx n (by omega)
      simp only [partialSum]
      omega

/-- A cyclic system of lower-bound transition inequalities. -/
def CyclicBounds (a h : Nat → Int) (P : Nat) (lo : Nat → Int) : Prop :=
  (∀ i, i < P → h i ≤ lo i) ∧
  (∀ i, i < P → lo ((i + 1) % P) ≤ lo i + a i)

/-- Exact feasibility: the thresholds impose no additional cycle obstruction. -/
theorem cyclic_bounds_iff_nonnegative (a h : Nat → Int) (P : Nat)
    (hP : 0 < P) :
    (∃ lo, CyclicBounds a h P lo) ↔ 0 ≤ partialSum a P := by
  constructor
  · rintro ⟨lo, hlo⟩
    have hp := path_bound a (fun i => lo (i % P)) P (by
      intro i hi
      have hs := hlo.2 i hi
      simpa only [Nat.mod_eq_of_lt hi] using hs)
    have hp' : lo 0 ≤ lo 0 + partialSum a P := by
      simpa only [Nat.mod_self, Nat.zero_mod] using hp
    omega
  · intro htotal
    let M := reserve a h (P - 1)
    refine ⟨fun i => M + partialSum a i, ?_, ?_⟩
    · intro i hi
      exact (initial_reserve_iff a h P hP M).mp (Int.le_refl M) i hi
    · intro i hi
      by_cases hit : i + 1 < P
      · rw [Nat.mod_eq_of_lt hit]
        simp only [partialSum]
        omega
      · have hie : i + 1 = P := by omega
        rw [hie, Nat.mod_self]
        have hpref : partialSum a i + a i = partialSum a P := by
          rw [← hie]
          rfl
        simp only [partialSum]
        omega

/-- Constant lower thresholds are included without a sign restriction. -/
theorem constant_threshold_iff (a : Nat → Int) (P : Nat) (hP : 0 < P)
    (H : Int) :
    (∃ lo : Nat → Int,
      (∀ i, i < P → H ≤ lo i) ∧
      (∀ i, i < P → lo ((i + 1) % P) ≤ lo i + a i)) ↔
      0 ≤ partialSum a P := by
  exact cyclic_bounds_iff_nonnegative a (fun _ => H) P hP

/-- The least initial reserve protects every phase on every later traversal. -/
theorem every_traversal_guard (a h : Nat → Int) (P : Nat) (hP : 0 < P)
    (x : Int) (htotal : 0 ≤ partialSum a P)
    (hstart : reserve a h (P - 1) ≤ x) (k i : Nat) (hi : i < P) :
    h i ≤ x + (k : Int) * partialSum a P + partialSum a i := by
  have hphase := (initial_reserve_iff a h P hP x).mp hstart i hi
  have hk : 0 ≤ (k : Int) * partialSum a P :=
    Int.mul_nonneg (by omega) htotal
  omega

/-- The two-band guard variables can be eliminated independently. -/
theorem two_coordinates_iff (a b h k : Nat → Int) (P : Nat) (hP : 0 < P) :
    (∃ lo lo', CyclicBounds a h P lo ∧ CyclicBounds b k P lo') ↔
      0 ≤ partialSum a P ∧ 0 ≤ partialSum b P := by
  constructor
  · rintro ⟨lo, lo', ha, hb⟩
    exact ⟨(cyclic_bounds_iff_nonnegative a h P hP).mp ⟨lo, ha⟩,
      (cyclic_bounds_iff_nonnegative b k P hP).mp ⟨lo', hb⟩⟩
  · rintro ⟨ha, hb⟩
    obtain ⟨lo, hlo⟩ := (cyclic_bounds_iff_nonnegative a h P hP).mpr ha
    obtain ⟨lo', hlo'⟩ := (cyclic_bounds_iff_nonnegative b k P hP).mpr hb
    exact ⟨lo, lo', hlo, hlo'⟩

/-- Natural-number lower bounds have exactly the same feasibility criterion. -/
theorem natural_bounds_iff (a : Nat → Int) (h : Nat → Nat) (P : Nat)
    (hP : 0 < P) :
    (∃ lo : Nat → Nat,
      (∀ i, i < P → h i ≤ lo i) ∧
      (∀ i, i < P → (lo ((i + 1) % P) : Int) ≤ (lo i : Int) + a i)) ↔
      0 ≤ partialSum a P := by
  constructor
  · rintro ⟨lo, hlower, hstep⟩
    apply (cyclic_bounds_iff_nonnegative a (fun i => (h i : Int)) P hP).mp
    refine ⟨fun i => (lo i : Int), ?_, hstep⟩
    intro i hi
    have hl := hlower i hi
    dsimp only
    omega
  · intro htotal
    obtain ⟨lo, hlo⟩ :=
      (cyclic_bounds_iff_nonnegative a (fun i => (h i : Int)) P hP).mpr htotal
    have hnonneg : ∀ i, i < P → 0 ≤ lo i := by
      intro i hi
      have hl := hlo.1 i hi
      dsimp only at hl
      omega
    refine ⟨fun i => (lo i).toNat, ?_, ?_⟩
    · intro i hi
      have hl := hlo.1 i hi
      have he := Int.toNat_of_nonneg (hnonneg i hi)
      dsimp only at hl ⊢
      omega
    · intro i hi
      rw [Int.toNat_of_nonneg (hnonneg i hi),
        Int.toNat_of_nonneg (hnonneg ((i + 1) % P) (Nat.mod_lt _ hP))]
      exact hlo.2 i hi

end Agent205.CyclicGuards
