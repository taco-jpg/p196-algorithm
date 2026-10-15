import FourColumnProjection
import TwoDigitNumeric

/-!
# Agent #113: number-level four-column projection and a generic depth bound

`quad n` is the four outermost pair sums of the canonical numeral of `n`.
`quad_step` lifts `quad_no_overflow` / `quad_overflow` to ordinary numbers of
width at least four. `Cert4.depth_bound` turns a finite backward-layer
certificate over outer quadruples into a bound on how late any positive
orbit can reach a state whose quadruple lies in layer 0.

Digit and width functions are reused from `Agent113.TwoDigit`
(`TwoDigitNumeric`). No claim about 196 or decimal Lychrel existence.
-/

namespace Agent113.FourColumn

open DecimalDigits FoldedDecimal Lychrel196 DecimalQuantitativeMass
open Agent113.TwoDigit (digitAt width pairAt canonical_width canonical_pairAt
  canonical_digitAt value_digit)

/-! ## Widths -/

theorem value_ge_of_lead (d : Nat → Nat) (L : Nat) (hL : 0 < L) (hlead : 0 < d (L - 1)) :
    10 ^ (L - 1) ≤ value d L := by
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 1 := ⟨L - 1, by omega⟩
  simp only [value, Nat.add_sub_cancel] at hlead ⊢
  have : 10 ^ k ≤ d k * 10 ^ k := Nat.le_mul_of_pos_left _ hlead
  omega

theorem value_lt' (d : Nat → Nat) (L : Nat) (hd : ∀ i, i < L → d i ≤ 9) :
    value d L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have h1 := ih (fun i hi => hd i (by omega))
    have h2 := hd L (by omega)
    simp only [value, Nat.pow_succ]
    have h3 : d L * 10 ^ L ≤ 9 * 10 ^ L := Nat.mul_le_mul_right _ h2
    omega

/-- The canonical width of a positive number brackets it between powers of ten. -/
theorem width_bounds (m : Nat) (hm : 0 < m) :
    0 < width m ∧ 10 ^ (width m - 1) ≤ m ∧ m < 10 ^ width m := by
  obtain ⟨d, L, hcan⟩ := canonical_exists m hm
  rw [canonical_width hcan]
  refine ⟨hcan.1, ?_, ?_⟩
  · rw [← hcan.2.2.2]; exact value_ge_of_lead d L hcan.1 hcan.2.2.1
  · rw [← hcan.2.2.2]; exact value_lt' d L hcan.2.1

theorem pow_ten_mono {a b : Nat} (h : a ≤ b) : 10 ^ a ≤ 10 ^ b :=
  Nat.pow_le_pow_right (by decide) h

theorem width_ge_of_ge (m n : Nat) (hm : 10 ^ n ≤ m) : n + 1 ≤ width m := by
  have hpos : 0 < m := Nat.lt_of_lt_of_le (Nat.pow_pos (by decide)) hm
  obtain ⟨_, _, hlt⟩ := width_bounds m hpos
  rcases Nat.lt_or_ge (width m) (n + 1) with h | h
  · have := pow_ten_mono (show width m ≤ n by omega)
    omega
  · exact h

theorem width_le_of_lt (m n : Nat) (hm0 : 0 < m) (hm : m < 10 ^ n) : width m ≤ n := by
  obtain ⟨hw, hge, _⟩ := width_bounds m hm0
  rcases Nat.lt_or_ge n (width m) with h | h
  · have := pow_ten_mono (show n ≤ width m - 1 by omega)
    omega
  · exact h

theorem width_eq_of_bounds (m n : Nat) (h1 : 10 ^ n ≤ m) (h2 : m < 10 ^ (n + 1)) :
    width m = n + 1 := by
  have a := width_ge_of_ge m n h1
  have b := width_le_of_lt m (n + 1) (Nat.lt_of_lt_of_le (Nat.pow_pos (by decide)) h1) h2
  omega

/-! ## The outer quadruple -/

def quad (n : Nat) : Quad := (pairAt n 0, pairAt n 1, pairAt n 2, pairAt n 3)

def nextQ (w : Quad) (e : Nat) : Quad := nextQuad w.1 w.2.1 w.2.2.1 w.2.2.2 e

def topQ (w : Quad) (e : Nat) : Nat := top4 w.1 w.2.1 w.2.2.1 w.2.2.2 e

theorem canonical_quad {n : Nat} {d : Nat → Nat} {L : Nat}
    (h : Canonical n d L) (hL : 4 ≤ L) :
    quad n = (columnSum d L 0, columnSum d L 1, columnSum d L 2, columnSum d L 3) := by
  simp only [quad, canonical_pairAt h 0 (by omega), canonical_pairAt h 1 (by omega),
    canonical_pairAt h 2 (by omega), canonical_pairAt h 3 (by omega)]

theorem quad_box (n : Nat) (hn : 0 < n) (hw : 4 ≤ width n) :
    1 ≤ (quad n).1 ∧ (quad n).1 ≤ 18 ∧ (quad n).2.1 ≤ 18 ∧
      (quad n).2.2.1 ≤ 18 ∧ (quad n).2.2.2 ≤ 18 := by
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  rw [canonical_width hcan] at hw
  rw [canonical_quad hcan hw]
  have hb := columnSum_bounded d L hcan.2.1
  have hlead := hcan.2.2.1
  have h0 : columnSum d L 0 = d 0 + d (L - 1) := by simp [columnSum, reflected]
  refine ⟨?_, hb 0 (by omega), hb 1 (by omega), hb 2 (by omega), hb 3 (by omega)⟩
  show 1 ≤ columnSum d L 0
  omega

theorem quad_step (n : Nat) (hn : 0 < n) (hw : 4 ≤ width n) :
    ∃ e, e ≤ 1 ∧ quad (step n) = nextQ (quad n) e ∧
      width n ≤ width (step n) := by
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hwL := canonical_width hcan
  rw [hwL] at hw ⊢
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 4 := ⟨L - 4, by omega⟩
  have hq := canonical_quad hcan hw
  have hb := carry_bounded (columnSum d (k + 4)) (k + 4)
    (columnSum_bounded d (k + 4) hcan.2.1)
  refine ⟨carry (columnSum d (k + 4)) k, hb k (by omega), ?_⟩
  rw [hq]
  simp only [nextQ]
  rcases actual_overflow_cases d (k + 4) hcan.2.1 with hc | hc
  · have hnext := canonical_next_no_overflow n d (k + 4) hcan hc
    rw [canonical_quad hnext (by omega), canonical_width hnext]
    exact ⟨quad_no_overflow d k hc, Nat.le_refl _⟩
  · have hnext := canonical_next_overflow n d (k + 4) hcan hc
    rw [canonical_quad hnext (by omega), canonical_width hnext]
    exact ⟨quad_overflow d k hc, by omega⟩

/-- Explicit outer quadruple of a four-digit number. -/
def quad4 (m : Nat) : Quad :=
  (m % 10 + m / 1000 % 10, m / 10 % 10 + m / 100 % 10,
   m / 100 % 10 + m / 10 % 10, m / 1000 % 10 + m % 10)

theorem quad_eq_quad4 (m : Nat) (h1 : 1000 ≤ m) (h2 : m < 10000) : quad m = quad4 m := by
  have hw : width m = 4 := width_eq_of_bounds m 3 (by simpa using h1) (by simpa using h2)
  simp only [quad, quad4, pairAt, hw, digitAt]
  simp

/-! ## Certificates over outer quadruples -/

def memQ (w : Quad) : List Quad → Bool
  | [] => false
  | x :: xs => (x.1 == w.1 && x.2.1 == w.2.1 && x.2.2.1 == w.2.2.1 &&
      x.2.2.2 == w.2.2.2) || memQ w xs

def layerAtQ : List (List Quad) → Nat → List Quad
  | [], _ => []
  | l :: _, 0 => l
  | _ :: ls, r + 1 => layerAtQ ls r

theorem layerAtQ_beyond : ∀ (ls : List (List Quad)) (r : Nat),
    ls.length ≤ r → layerAtQ ls r = []
  | [], _, _ => rfl
  | _ :: _, 0, h => by simp at h
  | _ :: ls, r + 1, h => by
      simp only [List.length_cons] at h
      exact layerAtQ_beyond ls r (by omega)

/-- `rangeAll n p` checks `p i` for every `i < n`. -/
def rangeAll : Nat → (Nat → Bool) → Bool
  | 0, _ => true
  | n + 1, p => p n && rangeAll n p

theorem rangeAll_sound {n : Nat} {p : Nat → Bool} (h : rangeAll n p = true) :
    ∀ i, i < n → p i = true := by
  induction n with
  | zero => intro i hi; omega
  | succ n ih =>
    intro i hi
    simp only [rangeAll, Bool.and_eq_true] at h
    by_cases hin : i = n
    · subst hin; exact h.1
    · exact ih h.2 i (by omega)

structure Cert4 where
  layers : List (List Quad)

def Cert4.h (C : Cert4) : Nat := C.layers.length

def Cert4.inLayer (C : Cert4) (r : Nat) (w : Quad) : Bool :=
  memQ w (layerAtQ C.layers r)

theorem Cert4.inLayer_beyond (C : Cert4) {r : Nat} (hr : C.h ≤ r) (w : Quad) :
    C.inLayer r w = false := by
  simp only [Cert4.inLayer, layerAtQ_beyond C.layers r hr, memQ]

/-- Row `(a, b)` of the closure of layer `r` into layer `r + 1`. -/
def Cert4.stepRow (C : Cert4) (r a b : Nat) : Bool :=
  rangeAll 19 fun c => rangeAll 19 fun d => rangeAll 2 fun e =>
    !(C.inLayer r (nextQ (a, b, c, d) e)) || C.inLayer (r + 1) (a, b, c, d)

/-- No number below 1000 steps to a four-digit number in any layer. -/
def Cert4.shortCheck (C : Cert4) : Bool :=
  rangeAll 1000 fun m => m == 0 || step m < 1000 ||
    (step m < 10000 && rangeAll C.h fun r => !C.inLayer r (quad4 (step m)))

structure Cert4.Checked (C : Cert4) : Prop where
  rest : ∀ r, r < C.h → ∀ a, 1 ≤ a → a ≤ 18 → ∀ b, b ≤ 18 → C.stepRow r a b = true
  short : C.shortCheck = true

theorem Cert4.step_sound {C : Cert4} (hC : C.Checked) (r : Nat) (w : Quad)
    (h0 : 1 ≤ w.1) (h0' : w.1 ≤ 18) (h1 : w.2.1 ≤ 18) (h2 : w.2.2.1 ≤ 18)
    (h3 : w.2.2.2 ≤ 18) (e : Nat) (he : e ≤ 1)
    (hin : C.inLayer r (nextQ w e) = true) : C.inLayer (r + 1) w = true := by
  have hrh : r < C.h := by
    rcases Nat.lt_or_ge r C.h with hlt | hge
    · exact hlt
    · rw [C.inLayer_beyond hge] at hin; cases hin
  obtain ⟨a, b, c, d⟩ := w
  have hrow := hC.rest r hrh a h0 h0' b h1
  have hc := rangeAll_sound hrow c (by simp only at h2; omega)
  have hd := rangeAll_sound hc d (by simp only at h3; omega)
  have he' := rangeAll_sound hd e (by omega)
  simp only [hin, Bool.not_true, Bool.false_or] at he'
  exact he'

theorem Cert4.short_sound {C : Cert4} (hC : C.Checked) (m : Nat)
    (hm : 0 < m) (hw : width m < 4) (hws : 4 ≤ width (step m)) (r : Nat) :
    C.inLayer r (quad (step m)) = false := by
  have hm1000 : m < 1000 := by
    rcases Nat.lt_or_ge m 1000 with hlt | hge
    · exact hlt
    · have := width_ge_of_ge m 3 (by simpa using hge); omega
  have hspos : 0 < step m := by unfold step; omega
  have hs1000 : 1000 ≤ step m := by
    rcases Nat.lt_or_ge (step m) 1000 with hlt | hge
    · have := width_le_of_lt (step m) 3 hspos (by simpa using hlt); omega
    · exact hge
  have hs := rangeAll_sound hC.short m hm1000
  have hm0 : (m == 0) = false := by simp only [beq_eq_false_iff_ne, ne_eq]; omega
  have hsm : decide (step m < 1000) = false := by simp only [decide_eq_false_iff_not]; omega
  simp only [hm0, hsm, Bool.false_or, Bool.and_eq_true, decide_eq_true_eq] at hs
  obtain ⟨hs10000, hall⟩ := hs
  rw [quad_eq_quad4 (step m) hs1000 hs10000]
  rcases Nat.lt_or_ge r C.h with hrh | hrh
  · have hr := rangeAll_sound hall r hrh
    simp only [Bool.not_eq_true'] at hr
    exact hr
  · exact C.inLayer_beyond hrh _

/-- Generic depth bound: no positive orbit reaches, at time `t ≥ h`, a state of
width at least four whose outer quadruple lies in layer 0. -/
theorem Cert4.depth_bound (C : Cert4) (hC : C.Checked) :
    ∀ A t X, 0 < A → orbit A t = X → 4 ≤ width X →
      C.inLayer 0 (quad X) = true → t < C.h := by
  intro A t X hA hrun hwX hX
  have hpos : ∀ j, 0 < orbit A j := DecimalDigits.orbit_positive A hA
  have key : ∀ i, i ≤ t →
      4 ≤ width (orbit A (t - i)) ∧ C.inLayer i (quad (orbit A (t - i))) = true := by
    intro i
    induction i with
    | zero => intro _; rw [Nat.sub_zero, hrun]; exact ⟨hwX, hX⟩
    | succ i ih =>
      intro hi
      obtain ⟨hw, hin⟩ := ih (by omega)
      have hm : step (orbit A (t - (i + 1))) = orbit A (t - i) := by
        rw [show t - i = t - (i + 1) + 1 by omega]; rfl
      have hmpos := hpos (t - (i + 1))
      rcases Nat.lt_or_ge (width (orbit A (t - (i + 1)))) 4 with hsh | hwm
      · exfalso
        have hs := C.short_sound hC _ hmpos hsh (by rw [hm]; exact hw) i
        rw [hm, hin] at hs
        cases hs
      · obtain ⟨e, he, hq, _⟩ := quad_step _ hmpos hwm
        rw [hm] at hq
        refine ⟨hwm, ?_⟩
        obtain ⟨b0, b0', b1, b2, b3⟩ := quad_box _ hmpos hwm
        apply C.step_sound hC i _ b0 b0' b1 b2 b3 e he
        rw [← hq]; exact hin
  obtain ⟨_, hfin⟩ := key t (Nat.le_refl t)
  rcases Nat.lt_or_ge t C.h with hlt | hge
  · exact hlt
  · rw [C.inLayer_beyond hge] at hfin; cases hfin

/-- Nineteen separately checked values cover `b ≤ 18`. -/
theorem cover19 {P : Nat → Prop} (h0 : P 0) (h1 : P 1) (h2 : P 2) (h3 : P 3)
    (h4 : P 4) (h5 : P 5) (h6 : P 6) (h7 : P 7) (h8 : P 8) (h9 : P 9)
    (h10 : P 10) (h11 : P 11) (h12 : P 12) (h13 : P 13) (h14 : P 14)
    (h15 : P 15) (h16 : P 16) (h17 : P 17) (h18 : P 18) :
    ∀ b, b ≤ 18 → P b := by
  intro b hb
  have : b = 0 ∨ b = 1 ∨ b = 2 ∨ b = 3 ∨ b = 4 ∨ b = 5 ∨ b = 6 ∨ b = 7 ∨
      b = 8 ∨ b = 9 ∨ b = 10 ∨ b = 11 ∨ b = 12 ∨ b = 13 ∨ b = 14 ∨ b = 15 ∨
      b = 16 ∨ b = 17 ∨ b = 18 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> assumption

/-- Eighteen separately checked values cover `1 ≤ a ≤ 18`. -/
theorem cover18 {P : Nat → Prop} (h1 : P 1) (h2 : P 2) (h3 : P 3) (h4 : P 4)
    (h5 : P 5) (h6 : P 6) (h7 : P 7) (h8 : P 8) (h9 : P 9) (h10 : P 10)
    (h11 : P 11) (h12 : P 12) (h13 : P 13) (h14 : P 14) (h15 : P 15)
    (h16 : P 16) (h17 : P 17) (h18 : P 18) :
    ∀ a, 1 ≤ a → a ≤ 18 → P a := by
  intro a ha hb
  have : a = 1 ∨ a = 2 ∨ a = 3 ∨ a = 4 ∨ a = 5 ∨ a = 6 ∨ a = 7 ∨ a = 8 ∨
      a = 9 ∨ a = 10 ∨ a = 11 ∨ a = 12 ∨ a = 13 ∨ a = 14 ∨ a = 15 ∨
      a = 16 ∨ a = 17 ∨ a = 18 := by omega
  rcases this with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> assumption

#print axioms quad_step
#print axioms Cert4.depth_bound

end Agent113.FourColumn
