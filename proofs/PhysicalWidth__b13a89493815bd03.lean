import ResetNormalization

namespace PhysicalWidth
open BaseReflection ResetNormalization SignedDigitUniqueness

def terminal (b i : Int) : List (Int × Bool) → Int
  | [] => i
  | (q,r)::xs => terminal b ((q + if r then 0 else i)/b) xs

def body (b i : Int) : List (Int × Bool) → List Int
  | [] => []
  | (q,r)::xs =>
    let active := if r then 0 else i
    ((q+active)%b + if r then i else 0) :: body b ((q+active)/b) xs

theorem placed_body_terminal (b i : Int) (xs : List (Int × Bool)) :
    placed b i xs = body b i xs ++ [terminal b i xs] := by
  induction xs generalizing i with
  | nil => rfl
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    simp [placed, body, terminal, ih]

theorem body_length (b i : Int) (xs : List (Int × Bool)) :
    (body b i xs).length = xs.length := by
  induction xs generalizing i with
  | nil => rfl
  | cons p xs ih => simp [body, ih]

theorem terminal_bit (b i : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hbound : Bounded b xs) :
    terminal b i xs = 0 ∨ terminal b i xs = 1 := by
  induction xs generalizing i with
  | nil => simp only [terminal]; omega
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    have hq := hbound (q,r) (by simp)
    have ht : Bounded b xs := by
      intro p hp; exact hbound p (by simp [hp])
    have ha : 0 ≤ (if r then (0:Int) else i) ∧ (if r then (0:Int) else i) ≤ 1 := by
      split <;> omega
    have hc := carry_bit b q _ hb hq ha
    exact ih _ (by omega) ht

theorem terminal_le_ordinary (b i j : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hj : 0 ≤ j ∧ j ≤ 1)
    (hij : i ≤ j) (hbound : Bounded b xs) :
    terminal b i xs ≤ terminal b j (ordinaryTags xs) := by
  induction xs generalizing i j with
  | nil => exact hij
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    have hq := hbound (q,r) (by simp)
    have ht : Bounded b xs := by
      intro p hp; exact hbound p (by simp [hp])
    let active : Int := if r then 0 else i
    have ha : 0 ≤ active ∧ active ≤ 1 := by dsimp [active]; split <;> omega
    have haj : active ≤ j := by dsimp [active]; split <;> omega
    have hc := carry_bit b q active hb hq ha
    have hd := carry_bit b q j hb hq hj
    have hcd := Int.ediv_le_ediv (show 0 < b by omega) (show q+active ≤ q+j by omega)
    change terminal b ((q+active)/b) xs ≤ terminal b ((q+j)/b) (ordinaryTags xs)
    exact ih _ _ (by omega) (by omega) hcd ht

theorem ordinary_bound (b : Int) (xs : List (Int × Bool)) (h : Bounded b xs) :
    Bounded b (ordinaryTags xs) := by
  intro p hp
  obtain ⟨a, ha, rfl⟩ := List.mem_map.mp hp
  exact h a ha

theorem ordinary_qs (xs : List (Int × Bool)) :
    (ordinaryTags xs).map Prod.fst = xs.map Prod.fst := by
  simp [ordinaryTags, List.map_map, Function.comp_def]

theorem ordinary_overflow_symmetry_forces_placed (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hd : (ordinary b xs).reverse = ordinary b xs) :
    placed b 0 xs = ordinary b xs := by
  have hclass := placed_overflow_classification b (ordinaryTags xs) hb
    (ordinary_bound b xs hbound) (by simpa only [ordinary_qs] using hq) hd
  apply high_placed_equals_ordinary b xs hb
  intro p hp
  have hm : (p.1,false) ∈ ordinaryTags xs := List.mem_map.mpr ⟨p,hp,rfl⟩
  obtain ⟨a, ha, heq⟩ := coefficient_mem_columns b 0 (ordinaryTags xs) _ hm
  have hh := (hclass a ha).2
  rwa [heq] at hh

theorem ordinary_nooverflow_symmetry_forces_placed (b : Int) (xs : List (Int × Bool))
    (d : List Int) (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hraw : ordinary b xs = d ++ [0]) (hd : d.reverse = d) :
    placed b 0 xs = ordinary b xs := by
  have hclass := placed_nooverflow_classification b (ordinaryTags xs) d hb
    (ordinary_bound b xs hbound) (by simpa only [ordinary_qs] using hq) hraw hd
  apply low_placed_equals_ordinary b xs (by omega)
  intro p hp
  have hm : (p.1,false) ∈ ordinaryTags xs := List.mem_map.mpr ⟨p,hp,rfl⟩
  obtain ⟨a, ha, heq⟩ := coefficient_mem_columns b 0 (ordinaryTags xs) _ hm
  have hh := (hclass.2 a ha).2
  rw [heq] at hh
  exact ⟨(hbound p hp).1, by omega⟩

theorem overflow_symmetry_iff (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (placed b 0 xs).reverse = placed b 0 xs ↔
    (ordinary b xs).reverse = ordinary b xs := by
  constructor
  · intro he
    have eq := overflow_symmetry_forces_ordinary b xs hb hbound hq he
    rwa [eq] at he
  · intro hd
    have eq := ordinary_overflow_symmetry_forces_placed b xs hb hbound hq hd
    rwa [eq]

/-- If actual normalization does not overflow, no independent block
partition can have a nonzero terminal carry slot. -/
theorem nooverflow_terminal_zero (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ht : terminal b 0 (ordinaryTags xs) = 0) : terminal b 0 xs = 0 := by
  have hl := terminal_le_ordinary b 0 0 xs hb (by omega) (by omega) (by omega) hbound
  have hc := terminal_bit b 0 xs hb (by omega) hbound
  omega

theorem nooverflow_symmetry_iff (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (ht : terminal b 0 (ordinaryTags xs) = 0) :
    (body b 0 xs).reverse = body b 0 xs ↔
    (body b 0 (ordinaryTags xs)).reverse = body b 0 (ordinaryTags xs) := by
  have heq : placed b 0 xs = body b 0 xs ++ [0] := by
    rw [placed_body_terminal, nooverflow_terminal_zero b xs (by omega) hbound ht]
  have hdq : ordinary b xs = body b 0 (ordinaryTags xs) ++ [0] := by
    rw [ordinary, placed_body_terminal, ht]
  constructor
  · intro he
    have eq := nooverflow_symmetry_forces_ordinary b xs _ hb hbound hq heq he
    rw [heq, hdq] at eq
    have hbody := List.append_cancel_right eq
    rwa [hbody] at he
  · intro hd
    have eq := ordinary_nooverflow_symmetry_forces_placed b xs _ hb hbound hq hdq hd
    rw [heq, hdq] at eq
    have hbody := List.append_cancel_right eq
    rwa [hbody]

/-- Select the actual normalization width from its computed final carry. -/
def atActualWidth (b : Int) (xs : List (Int × Bool)) : List Int :=
  if terminal b 0 (ordinaryTags xs) = 0 then body b 0 xs else placed b 0 xs

def actualDigits (b : Int) (xs : List (Int × Bool)) : List Int :=
  atActualWidth b (ordinaryTags xs)

theorem ordinaryTags_idempotent (xs : List (Int × Bool)) :
    ordinaryTags (ordinaryTags xs) = ordinaryTags xs := by
  simp [ordinaryTags, List.map_map, Function.comp_def]

/-- Raw symmetry at the computed actual width is equivalent to the
palindromicity of continuous-carry normalized digits, for every reset set. -/
theorem actual_width_symmetry_iff (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (atActualWidth b xs).reverse = atActualWidth b xs ↔
    (actualDigits b xs).reverse = actualDigits b xs := by
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  split
  · exact nooverflow_symmetry_iff b xs hb hbound hq (by assumption)
  · exact overflow_symmetry_iff b xs hb hbound hq

def PositiveTerminal : List (Int × Bool) → Prop
  | [] => False
  | [p] => 0 < p.1
  | _ :: p :: xs => PositiveTerminal (p :: xs)

def PositiveLast (ds : List Int) : Prop :=
  ∃ front digit, ds = front ++ [digit] ∧ 0 < digit

theorem ordinary_body_digits (b i : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hbound : Bounded b xs) :
    ∀ d ∈ body b i (ordinaryTags xs), 0 ≤ d ∧ d < b := by
  induction xs generalizing i with
  | nil => simp [ordinaryTags, body]
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    have hq := hbound (q,r) (by simp)
    have ht : Bounded b xs := by
      intro p hp; exact hbound p (by simp [hp])
    have hc := carry_bit b q i hb hq hi
    have hci : 0 ≤ (q+i)/b ∧ (q+i)/b ≤ 1 := by omega
    intro d hd
    simp only [ordinaryTags, List.map_cons, body, Bool.false_eq_true, ↓reduceIte, Int.add_zero] at hd
    rcases List.mem_cons.mp hd with rfl | hd
    · exact ⟨Int.emod_nonneg _ (by omega), Int.emod_lt_of_pos _ (by omega)⟩
    · exact ih _ hci ht d hd

theorem ordinary_body_positive_last (b i : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hi : 0 ≤ i ∧ i ≤ 1) (hbound : Bounded b xs)
    (hp : PositiveTerminal xs) (ht : terminal b i (ordinaryTags xs)=0) :
    PositiveLast (body b i (ordinaryTags xs)) := by
  induction xs generalizing i with
  | nil => contradiction
  | cons p xs ih =>
    rcases p with ⟨q,r⟩
    have hq := hbound (q,r) (by simp)
    have htail : Bounded b xs := by
      intro p hp; exact hbound p (by simp [hp])
    have hc := carry_bit b q i hb hq hi
    have hci : 0 ≤ (q+i)/b ∧ (q+i)/b ≤ 1 := by omega
    cases xs with
    | nil =>
      change 0 < q at hp
      change (q+i)/b=0 at ht
      have hval := Int.emod_add_ediv (q+i) b
      rw [ht] at hval
      simp only [Int.mul_zero, Int.add_zero] at hval
      refine ⟨[], (q+i)%b, ?_, ?_⟩
      · simp [ordinaryTags, body]
      · omega
    | cons a tail =>
      have hpt : PositiveTerminal (a::tail) := hp
      have htt : terminal b ((q+i)/b) (ordinaryTags (a::tail))=0 := ht
      obtain ⟨front,digit,he,hpos⟩ := ih _ hci htail hpt htt
      refine ⟨((q+i)%b)::front, digit, ?_, hpos⟩
      have hh : body b i (ordinaryTags ((q,r)::a::tail)) =
          ((q+i)%b)::body b ((q+i)/b) (ordinaryTags (a::tail)) := by
        simp only [ordinaryTags, List.map_cons, body, Bool.false_eq_true, ↓reduceIte, Int.add_zero]
      rw [hh, he]
      rfl

theorem actual_digits_length (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs) :
    (actualDigits b xs).length = xs.length +
      (terminal b 0 (ordinaryTags xs)).toNat := by
  have hc := terminal_bit b 0 (ordinaryTags xs) hb (by omega)
    (ordinary_bound b xs hbound)
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  rcases hc with hc | hc
  · rw [if_pos hc, body_length, hc]
    simp [ordinaryTags]
  · rw [if_neg (by omega), placed_body_terminal, hc]
    simp [body_length, ordinaryTags]

theorem actual_digits_bounded (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs) :
    ∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b := by
  have hd := ordinary_body_digits b 0 xs hb (by omega) hbound
  have hc := terminal_bit b 0 (ordinaryTags xs) hb (by omega)
    (ordinary_bound b xs hbound)
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  rcases hc with hc | hc
  · simpa [hc] using hd
  · rw [if_neg (by omega), placed_body_terminal, hc]
    intro d hmem
    rcases List.mem_append.mp hmem with hm | hm
    · exact hd d hm
    · simp only [List.mem_singleton] at hm
      subst d
      omega

theorem actual_digits_positive_last (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs) (hp : PositiveTerminal xs) :
    PositiveLast (actualDigits b xs) := by
  have hc := terminal_bit b 0 (ordinaryTags xs) hb (by omega)
    (ordinary_bound b xs hbound)
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  rcases hc with hc | hc
  · rw [if_pos hc]
    exact ordinary_body_positive_last b 0 xs hb (by omega) hbound hp hc
  · rw [if_neg (by omega), placed_body_terminal, hc]
    exact ⟨_,1,rfl,by decide⟩

/-- Canonical finite normalization, including its value and actual width.
The positive-terminal hypothesis excludes the empty and leading-zero
coefficient words. Symmetry is not needed for these normalization facts. -/
theorem canonical_normalization (b : Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hbound : Bounded b xs) (hp : PositiveTerminal xs) :
    (∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b) ∧
    PositiveLast (actualDigits b xs) ∧
    (actualDigits b xs).length = xs.length +
      (terminal b 0 (ordinaryTags xs)).toNat ∧
    eval b (actualDigits b xs) = eval b (xs.map Prod.fst) := by
  refine ⟨actual_digits_bounded b xs hb hbound,
    actual_digits_positive_last b xs hb hbound hp,
    actual_digits_length b xs hb hbound, ?_⟩
  have hv := placed_eval b 0 (ordinaryTags xs)
  rw [ordinary_qs] at hv
  simp only [Int.add_zero] at hv
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  split
  · rename_i hc
    rw [placed_body_terminal, hc, eval_append] at hv
    simpa [eval] using hv
  · exact hv

theorem actual_width_symmetry_forces_equality (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (he : (atActualWidth b xs).reverse = atActualWidth b xs) :
    atActualWidth b xs = actualDigits b xs := by
  unfold atActualWidth at he
  unfold actualDigits atActualWidth
  rw [ordinaryTags_idempotent]
  split at he
  · rename_i ht
    have heraw : placed b 0 xs = body b 0 xs ++ [0] := by
      rw [placed_body_terminal, nooverflow_terminal_zero b xs (by omega) hbound ht]
    have hdraw : ordinary b xs = body b 0 (ordinaryTags xs) ++ [0] := by
      rw [ordinary, placed_body_terminal, ht]
    have heq := nooverflow_symmetry_forces_ordinary b xs _ hb hbound hq heraw he
    rw [heraw, hdraw] at heq
    simpa only [if_pos ht] using List.append_cancel_right heq
  · rename_i ht
    simpa only [if_neg ht, ordinary] using
      overflow_symmetry_forces_ordinary b xs hb hbound hq he

/-- The main canonical theorem: actual digit bounds, positive leading
output digit, computed physical width and value, plus raw symmetry
 equivalence and equality in either symmetric case. -/
theorem canonical_raw_symmetry (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs) (hp : PositiveTerminal xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b) ∧
    PositiveLast (actualDigits b xs) ∧
    (actualDigits b xs).length = xs.length +
      (terminal b 0 (ordinaryTags xs)).toNat ∧
    eval b (actualDigits b xs) = eval b (xs.map Prod.fst) ∧
    ((atActualWidth b xs).reverse = atActualWidth b xs ↔
      (actualDigits b xs).reverse = actualDigits b xs) ∧
    ((atActualWidth b xs).reverse = atActualWidth b xs →
      atActualWidth b xs = actualDigits b xs) := by
  obtain ⟨hd,hl,hw,hv⟩ := canonical_normalization b xs (by omega) hbound hp
  exact ⟨hd,hl,hw,hv,actual_width_symmetry_iff b xs hb hbound hq,
    actual_width_symmetry_forces_equality b xs hb hbound hq⟩

end PhysicalWidth
