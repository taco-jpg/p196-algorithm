import P196.Core.BaseReflection

namespace ResetNormalization
open BaseReflection SignedDigitUniqueness

/-- True marks a block start, where the incoming carry resets to zero. -/
def columns (b incoming : Int) : List (Int × Bool) → List (Int × Int)
  | [] => []
  | (q,reset) :: xs =>
    let active := if reset then 0 else incoming
    let outgoing := (q+active)/b
    (q,outgoing) :: columns b outgoing xs

/-- Raw placement of independent normalized blocks. At a reset, the
previous block's terminal carry is placed on top of the new block's
first digit. The final terminal carry is always included. -/
def placed (b incoming : Int) : List (Int × Bool) → List Int
  | [] => [incoming]
  | (q,reset) :: xs =>
    let active := if reset then 0 else incoming
    let outgoing := (q+active)/b
    ((q+active)%b + if reset then incoming else 0) :: placed b outgoing xs

def Bounded (b : Int) (xs : List (Int × Bool)) : Prop :=
  ∀ p ∈ xs, 0 ≤ p.1 ∧ p.1 ≤ 2*b-2

theorem carry_bit (b q i : Int) (hb : 2 ≤ b)
    (hq : 0 ≤ q ∧ q ≤ 2*b-2) (hi : 0 ≤ i ∧ i ≤ 1) :
    (q+i)/b = 0 ∨ (q+i)/b = 1 := by
  have hlo := Int.ediv_nonneg (show 0 ≤ q+i by omega) (show 0 ≤ b by omega)
  have hhi : (q+i)/b < 2 := Int.ediv_lt_of_lt_mul (by omega) (by omega)
  omega

theorem columns_qs (b i : Int) (xs : List (Int × Bool)) :
    qs (columns b i xs) = xs.map Prod.fst := by
  induction xs generalizing i with
  | nil => rfl
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    change q :: qs (columns b ((q + if r then 0 else i)/b) xs) = q :: xs.map Prod.fst
    rw [ih]

theorem columns_conditions (b i : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hbound : Bounded b xs) :
    ColumnConditions b (columns b i xs) := by
  induction xs generalizing i with
  | nil => simp [columns, ColumnConditions]
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    have hq := hbound (q,r) (by simp)
    have ht : Bounded b xs := by
      intro p hp
      exact hbound p (by simp [hp])
    let active : Int := if r then 0 else i
    have ha : 0 ≤ active ∧ active ≤ 1 := by
      dsimp [active]
      split <;> omega
    have hc := carry_bit b q active hb hq ha
    have hci : 0 ≤ (q+active)/b ∧ (q+active)/b ≤ 1 := by omega
    have htail := ih ((q+active)/b) hci ht
    intro p hp
    simp only [columns, List.mem_cons] at hp
    rcases hp with hp | hp
    · subst p
      refine ⟨hc, active, (q+active)%b, hq, ha, ?_, ?_⟩
      · exact ⟨Int.emod_nonneg _ (by omega), by
          have := Int.emod_lt_of_pos (q+active) (show 0 < b by omega)
          omega⟩
      · exact (Int.emod_add_ediv (q+active) b).symm
    · exact htail p hp

theorem placed_eq_raw (b i : Int) (xs : List (Int × Bool)) :
    placed b i xs = raw b i (columns b i xs) := by
  induction xs generalizing i with
  | nil => rfl
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    simp only [placed, columns, raw, List.cons.injEq]
    constructor
    · cases r <;> simp only [Bool.false_eq_true, ↓reduceIte, Int.add_zero]
      · have := Int.emod_add_ediv (q+i) b
        omega
      · have := Int.emod_add_ediv q b
        omega
    · exact ih _

/-- The raw sum of independently normalized blocks preserves the value
of the original coefficient list (and the optional initial carry). -/
theorem placed_eval (b i : Int) (xs : List (Int × Bool)) :
    eval b (placed b i xs) = eval b (xs.map Prod.fst) + i := by
  rw [placed_eq_raw, raw_eval, columns_qs]

theorem placed_overflow_classification (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (he : (placed b 0 xs).reverse = placed b 0 xs) :
    ∀ p ∈ columns b 0 xs, p.1 = (b+1)*p.2 ∧ (p.1 = 0 ∨ p.1 = b+1) := by
  apply overflow_classification b (columns b 0 xs) hb
  · simpa only [columns_qs] using hq
  · simpa only [placed_eq_raw] using he
  · exact columns_conditions b 0 xs (by omega) (by omega) hbound

theorem placed_nooverflow_classification (b : Int) (xs : List (Int × Bool))
    (e : List Int) (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hraw : placed b 0 xs = e ++ [0]) (he : e.reverse = e) :
    e = xs.map Prod.fst ∧
      ∀ p ∈ columns b 0 xs, p.2 = 0 ∧ p.1 ≤ b-1 := by
  have hc := columns_conditions b 0 xs (by omega) (by omega) hbound
  have hqs : (qs (columns b 0 xs)).reverse = qs (columns b 0 xs) := by
    simpa only [columns_qs] using hq
  rw [placed_eq_raw] at hraw
  constructor
  · simpa only [columns_qs] using
      nooverflow_raw_equals_input b (columns b 0 xs) e hb hqs hraw he hc
  · exact nooverflow_classification b (columns b 0 xs) e hb hqs hraw he hc

def ordinaryTags (xs : List (Int × Bool)) : List (Int × Bool) :=
  xs.map (fun p => (p.1, false))

/-- Ordinary normalization: one continuous carry chain, no resets.
Its terminal carry slot is retained even when zero. -/
def ordinary (b : Int) (xs : List (Int × Bool)) : List Int :=
  placed b 0 (ordinaryTags xs)

theorem low_columns_zero (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hlow : ∀ p ∈ xs, 0 ≤ p.1 ∧ p.1 < b) :
    ∀ p ∈ columns b 0 xs, p.2 = 0 := by
  induction xs with
  | nil => simp [columns]
  | cons a xs ih =>
    rcases a with ⟨q,r⟩
    have hq := hlow (q,r) (by simp)
    have ht : ∀ p ∈ xs, 0 ≤ p.1 ∧ p.1 < b := by
      intro p hp
      exact hlow p (by simp [hp])
    have hz : q/b=0 := Int.ediv_eq_zero_of_lt hq.1 hq.2
    have active : (if r then (0:Int) else 0) = 0 := by split <;> rfl
    simp only [columns, active, Int.add_zero, hz, List.mem_cons]
    intro p hp
    rcases hp with rfl | hp
    · rfl
    · exact ih ht p hp

theorem low_placed (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hlow : ∀ p ∈ xs, 0 ≤ p.1 ∧ p.1 < b) :
    placed b 0 xs = xs.map Prod.fst ++ [0] := by
  rw [placed_eq_raw, raw_of_zero_carries b _ (low_columns_zero b xs hb hlow),
    columns_qs]

theorem high_carry (b q i : Int) (hb : 3 ≤ b)
    (hq : q=0 ∨ q=b+1) (hi : 0 ≤ i ∧ i ≤ 1) :
    (q+i)/b = if q=0 then 0 else 1 := by
  rcases hq with rfl | rfl
  · simp only [Int.zero_add, ↓reduceIte]
    exact Int.ediv_eq_zero_of_lt hi.1 (by omega)
  · have hbit := carry_bit b (b+1) i (by omega) (by omega) hi
    have hnot : ¬ (b+1+i)/b ≤ 0 := by
      rw [Int.ediv_le_iff_le_mul (show 0 < b by omega)]
      simp only [Int.zero_mul, Int.zero_add]
      omega
    have hz : b+1 ≠ 0 := by omega
    simp only [hz, ↓reduceIte]
    omega

theorem high_columns_ignore_resets (b i j : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hj : 0 ≤ j ∧ j ≤ 1)
    (hhigh : ∀ p ∈ xs, p.1=0 ∨ p.1=b+1) :
    columns b i xs = columns b j (ordinaryTags xs) := by
  induction xs generalizing i j with
  | nil => rfl
  | cons a xs ih =>
    rcases a with ⟨q,r⟩
    have hq := hhigh (q,r) (by simp)
    have ht : ∀ p ∈ xs, p.1=0 ∨ p.1=b+1 := by
      intro p hp
      exact hhigh p (by simp [hp])
    let active : Int := if r then 0 else i
    have ha : 0 ≤ active ∧ active ≤ 1 := by
      dsimp [active]; split <;> omega
    have hleft := high_carry b q active hb hq ha
    have hright := high_carry b q j hb hq hj
    have heq : (q+active)/b = (q+j)/b := hleft.trans hright.symm
    have hc := carry_bit b q j (by omega) (by rcases hq with rfl | rfl <;> omega) hj
    have hci : 0 ≤ (q+j)/b ∧ (q+j)/b ≤ 1 := by omega
    simp only [ordinaryTags, List.map_cons, columns, Bool.false_eq_true, ↓reduceIte]
    change (q,(q+active)/b) :: columns b ((q+active)/b) xs =
      (q,(q+j)/b) :: columns b ((q+j)/b) (ordinaryTags xs)
    rw [heq, ih _ _ hci hci ht]

theorem high_placed_equals_ordinary (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hhigh : ∀ p ∈ xs, p.1=0 ∨ p.1=b+1) :
    placed b 0 xs = ordinary b xs := by
  unfold ordinary
  rw [placed_eq_raw, placed_eq_raw,
    high_columns_ignore_resets b 0 0 xs hb (by omega) (by omega) hhigh]

theorem low_placed_equals_ordinary (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hlow : ∀ p ∈ xs, 0 ≤ p.1 ∧ p.1 < b) :
    placed b 0 xs = ordinary b xs := by
  have ho : ∀ p ∈ ordinaryTags xs, 0 ≤ p.1 ∧ p.1 < b := by
    intro p hp
    obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hp
    exact hlow a ha
  rw [low_placed b xs hb hlow, ordinary, low_placed b _ hb ho]
  simp [ordinaryTags, List.map_map, Function.comp_def]

/-- Membership transport uses the proved coefficient projection, not a
hypothesis identifying arbitrary chosen carry lists. -/
theorem coefficient_mem_columns (b i : Int) (xs : List (Int × Bool))
    (p : Int × Bool) (hp : p ∈ xs) :
    ∃ a ∈ columns b i xs, a.1=p.1 := by
  have hm : p.1 ∈ qs (columns b i xs) := by
    rw [columns_qs]
    exact List.mem_map.mpr ⟨p,hp,rfl⟩
  exact List.mem_map.mp hm

theorem overflow_symmetry_forces_ordinary (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (he : (placed b 0 xs).reverse = placed b 0 xs) :
    placed b 0 xs = ordinary b xs := by
  have hclass := placed_overflow_classification b xs hb hbound hq he
  apply high_placed_equals_ordinary b xs hb
  intro p hp
  obtain ⟨a, ha, heq⟩ := coefficient_mem_columns b 0 xs p hp
  have h := (hclass a ha).2
  rwa [heq] at h

theorem nooverflow_symmetry_forces_ordinary (b : Int) (xs : List (Int × Bool))
    (e : List Int) (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hraw : placed b 0 xs = e ++ [0]) (he : e.reverse = e) :
    placed b 0 xs = ordinary b xs := by
  have hclass := placed_nooverflow_classification b xs e hb hbound hq hraw he
  apply low_placed_equals_ordinary b xs (by omega)
  intro p hp
  obtain ⟨a, ha, heq⟩ := coefficient_mem_columns b 0 xs p hp
  have h := (hclass.2 a ha).2
  rw [heq] at h
  exact ⟨(hbound p hp).1, by omega⟩

end ResetNormalization
