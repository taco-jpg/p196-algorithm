import P196.Core.TwoDigitNumeric

/-!
# Agent #113: backward-layer certificates for two-digit palindrome prefixes

A certificate `C` names a two-digit prefix `a, b` and a list of layer
bitmasks over outer triples. `C.Checked` collects Boolean obligations, each
evaluated by the Lean kernel (one evaluation per row `s0 = a` of the box).
They verify

* `base`: every triple `(a, b, c)`, `c ≤ 9`, is in layer 0;
* `first`: every triple of the finite box `1 ≤ s0 ≤ 18`, `s1, s2 ≤ 18` that
  reaches layer 0 by a *non-overflowing* update lies in layer 1;
* `rest`: for each `1 ≤ r < h`, every box triple reaching layer `r` by any
  update lies in layer `r + 1` (layer `h` is empty by definition);
* `short`: no number `1 ≤ m < 100` steps to a three-digit number whose outer
  triple lies in a layer `r ≥ 1`.

`Cert.ancestry_bound` proves that a passing certificate with `b < a` bounds the ancestry depth of every palindrome beginning with `a, b`
by `h`, for every positive starting value and every width. The proof uses
the all-width projection `tri_step`, Lemma 1
(`width_step_eq_of_small_descending`) for the second-to-last step, and the
reviewed last-step bridge. No claim about 196 is made in this module.
-/

namespace Agent113.TwoDigit

open Lychrel196

abbrev Triple := Nat × Nat × Nat

/-- Bit position of a triple in a layer bitmask. Injectivity is never used:
soundness only needs `inLayer` to be some Boolean predicate. -/
def code (w : Triple) : Nat := w.1 * 361 + w.2.1 * 19 + w.2.2

/-- Bit `k` of `m`. -/
def bitAt (m k : Nat) : Bool := m / 2 ^ k % 2 == 1

theorem bitAt_zero (k : Nat) : bitAt 0 k = false := by
  simp [bitAt]

/-- The `r`-th layer bitmask, zero beyond the end of the list. -/
def layerAt : List Nat → Nat → Nat
  | [], _ => 0
  | l :: _, 0 => l
  | _ :: ls, r + 1 => layerAt ls r

theorem layerAt_beyond : ∀ (ls : List Nat) (r : Nat),
    ls.length ≤ r → layerAt ls r = 0
  | [], _, _ => rfl
  | _ :: _, 0, h => by simp at h
  | _ :: ls, r + 1, h => by
      simp only [List.length_cons] at h
      exact layerAt_beyond ls r (by omega)

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

/-- One row `s0 = a` of the box `s1, s2 ≤ 18`. -/
def rowAll (a : Nat) (p : Triple → Bool) : Bool :=
  rangeAll 19 fun b => rangeAll 19 fun c => p (a, b, c)

theorem rowAll_sound {a : Nat} {p : Triple → Bool} (h : rowAll a p = true)
    (b c : Nat) (hb : b ≤ 18) (hc : c ≤ 18) : p (a, b, c) = true :=
  rangeAll_sound (rangeAll_sound h b (by omega)) c (by omega)

/-- Eighteen separately checked rows cover `1 ≤ a ≤ 18`. -/
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

/-- A two-digit prefix certificate: layer `r` is a bitmask over `code`. -/
structure Cert where
  a : Nat
  b : Nat
  layers : List Nat

/-- The certified depth bound: the number of listed layers. Non-emptiness of
the layers is not checked; exactness of a bound is a separate theorem. -/
def Cert.h (C : Cert) : Nat := C.layers.length

def Cert.inLayer (C : Cert) (r : Nat) (w : Triple) : Bool :=
  bitAt (layerAt C.layers r) (code w)

theorem Cert.inLayer_beyond (C : Cert) {r : Nat} (hr : C.h ≤ r) (w : Triple) :
    C.inLayer r w = false := by
  simp only [Cert.inLayer, layerAt_beyond C.layers r hr, bitAt_zero]

def Cert.baseCheck (C : Cert) : Bool :=
  rangeAll 10 fun c => C.inLayer 0 (C.a, C.b, c)

/-- Row `a` of the non-overflow closure into layer 1. -/
def Cert.firstRow (C : Cert) (a : Nat) : Bool :=
  rowAll a fun w => rangeAll 2 fun e =>
    !(topT w e == 0 && C.inLayer 0 (nextT w e)) || C.inLayer 1 w

/-- Row `a` of the closure from layer `r` into layer `r + 1`. -/
def Cert.stepRow (C : Cert) (r a : Nat) : Bool :=
  rowAll a fun w => rangeAll 2 fun e =>
    !(C.inLayer r (nextT w e)) || C.inLayer (r + 1) w

def Cert.shortCheck (C : Cert) : Bool :=
  rangeAll 100 fun m => m == 0 || step m < 100 ||
    (step m < 1000 && rangeAll C.h fun r => r == 0 || !C.inLayer r (tri3 (step m)))

/-- All finite obligations of a certificate. Each row is a separate
kernel evaluation in the concrete instances. -/
structure Cert.Checked (C : Cert) : Prop where
  base : C.baseCheck = true
  first : ∀ a, 1 ≤ a → a ≤ 18 → C.firstRow a = true
  rest : ∀ r, 1 ≤ r → r < C.h → ∀ a, 1 ≤ a → a ≤ 18 → C.stepRow r a = true
  short : C.shortCheck = true

/-! ## Soundness of the individual checks -/

theorem Cert.base_sound {C : Cert} (h : C.baseCheck = true) (c : Nat) (hc : c ≤ 9) :
    C.inLayer 0 (C.a, C.b, c) = true :=
  rangeAll_sound h c (by omega)

theorem Cert.first_sound {C : Cert}
    (h : ∀ a, 1 ≤ a → a ≤ 18 → C.firstRow a = true) (w : Triple)
    (h0 : 1 ≤ w.1) (h0' : w.1 ≤ 18) (h1 : w.2.1 ≤ 18) (h2 : w.2.2 ≤ 18)
    (e : Nat) (he : e ≤ 1) (htop : topT w e = 0)
    (hin : C.inLayer 0 (nextT w e) = true) : C.inLayer 1 w = true := by
  obtain ⟨a, b, c⟩ := w
  have hw := rowAll_sound (h a h0 h0') b c h1 h2
  have he' := rangeAll_sound hw e (by omega)
  simp only [htop, hin, beq_self_eq_true, Bool.and_self, Bool.not_true,
    Bool.false_or] at he'
  exact he'

theorem Cert.step_sound {C : Cert}
    (h : ∀ r, 1 ≤ r → r < C.h → ∀ a, 1 ≤ a → a ≤ 18 → C.stepRow r a = true)
    (r : Nat) (hr0 : 1 ≤ r) (w : Triple)
    (h0 : 1 ≤ w.1) (h0' : w.1 ≤ 18) (h1 : w.2.1 ≤ 18) (h2 : w.2.2 ≤ 18)
    (e : Nat) (he : e ≤ 1)
    (hin : C.inLayer r (nextT w e) = true) : C.inLayer (r + 1) w = true := by
  have hrh : r < C.h := by
    rcases Nat.lt_or_ge r C.h with hlt | hge
    · exact hlt
    · rw [C.inLayer_beyond hge] at hin
      cases hin
  obtain ⟨a, b, c⟩ := w
  have hw := rowAll_sound (h r hr0 hrh a h0 h0') b c h1 h2
  have he' := rangeAll_sound hw e (by omega)
  simp only [hin, Bool.not_true, Bool.false_or] at he'
  exact he'

theorem width_le_two (m : Nat) (h : m < 100) : width m ≤ 2 := by
  simp only [width]
  by_cases h0 : m = 0
  · subst h0; rw [DecimalQuantitativeMass.decimalLength_zero]; omega
  rw [DecimalQuantitativeMass.decimalLength]
  simp only [h0, ↓reduceDIte]
  by_cases h1 : m / 10 = 0
  · rw [h1, DecimalQuantitativeMass.decimalLength_zero]; omega
  rw [DecimalQuantitativeMass.decimalLength]
  simp only [h1, ↓reduceDIte]
  rw [show m / 10 / 10 = 0 by omega, DecimalQuantitativeMass.decimalLength_zero]
  omega

theorem Cert.short_sound {C : Cert} (h : C.shortCheck = true) (m : Nat)
    (hm : 0 < m) (hw : width m < 3) (hws : 3 ≤ width (step m))
    (r : Nat) (hr0 : 1 ≤ r) : C.inLayer r (tri (step m)) = false := by
  have hm100 : m < 100 := by
    rcases Nat.lt_or_ge m 100 with hlt | hge
    · exact hlt
    · have := width_ge_three m hge
      omega
  have hs100 : 100 ≤ step m := by
    rcases Nat.lt_or_ge (step m) 100 with hlt | hge
    · have := width_le_two (step m) hlt
      omega
    · exact hge
  have hs := rangeAll_sound h m hm100
  have hm0 : (m == 0) = false := by simp only [beq_eq_false_iff_ne, ne_eq]; omega
  have hs1 : decide (step m < 100) = false := by simp only [decide_eq_false_iff_not]; omega
  simp only [hm0, hs1, Bool.false_or, Bool.and_eq_true, decide_eq_true_eq] at hs
  obtain ⟨hs1000, hall⟩ := hs
  rw [tri_eq_tri3 (step m) hs100 hs1000]
  by_cases hrh : r < C.h
  · have hr := rangeAll_sound hall r hrh
    have hr' : (r == 0) = false := by simp only [beq_eq_false_iff_ne, ne_eq]; omega
    simp only [hr', Bool.false_or, Bool.not_eq_true'] at hr
    exact hr
  · exact C.inLayer_beyond (by omega) _

/-! ## The ancestry bound -/

/-- Every passing certificate with a strictly descending prefix `b < a`
bounds the ancestry depth of every palindrome beginning with `a, b`. -/
theorem Cert.ancestry_bound (C : Cert) (hab : C.b < C.a)
    (hcheck : C.Checked) :
    ∀ A P t, 0 < A → PalindromeStartsTwo C.a C.b P → orbit A t = P → t ≤ C.h := by
  obtain ⟨hbase, hfirst, hrest, hshort⟩ := hcheck
  intro A P t hA hP hrun
  cases t with
  | zero => omega
  | succ s =>
  have hpos : ∀ j, 0 < orbit A j := DecimalDigits.orbit_positive A hA
  have hlast : step (orbit A s) = P := hrun
  obtain ⟨hwM, hsmallM, hM0, hM1, hM2⟩ :=
    last_step_triple C.a C.b hab (hpos s) hlast hP
  have key : ∀ i, i ≤ s →
      3 ≤ width (orbit A (s - i)) ∧ C.inLayer i (tri (orbit A (s - i))) = true := by
    intro i
    induction i with
    | zero =>
      intro _
      rw [Nat.sub_zero]
      refine ⟨hwM, ?_⟩
      have htri : tri (orbit A s) = (C.a, C.b, pairAt (orbit A s) 2) := by
        simp only [tri, hM0, hM1]
      rw [htri]
      exact C.base_sound hbase _ hM2
    | succ i ih =>
      intro hi
      obtain ⟨hw, hin⟩ := ih (by omega)
      have hm : step (orbit A (s - (i + 1))) = orbit A (s - i) := by
        rw [show s - i = s - (i + 1) + 1 by omega]
        rfl
      have hmpos := hpos (s - (i + 1))
      by_cases hi0 : i = 0
      · subst hi0
        rw [Nat.sub_zero] at hm
        have hwe := width_step_eq_of_small_descending (orbit A (s - (0 + 1))) hmpos
          (by rw [hm]; exact hsmallM) (by rw [hm, hM0, hM1]; exact hab)
        have hwm : 3 ≤ width (orbit A (s - (0 + 1))) := by
          rw [← hwe, hm]; exact hwM
        obtain ⟨e, he, htri, hwidth⟩ := tri_step _ hmpos hwm
        rw [hm] at htri hwidth
        have htop : topT (tri (orbit A (s - (0 + 1)))) e = 0 := by
          rw [hm] at hwe; omega
        refine ⟨hwm, ?_⟩
        obtain ⟨b0, b0', b1, b2⟩ := tri_box _ hmpos hwm
        apply C.first_sound hfirst _ b0 b0' b1 b2 e he htop
        rw [← htri]
        rw [Nat.sub_zero] at hin
        exact hin
      · by_cases hwm : 3 ≤ width (orbit A (s - (i + 1)))
        · obtain ⟨e, he, htri, _⟩ := tri_step _ hmpos hwm
          rw [hm] at htri
          refine ⟨hwm, ?_⟩
          obtain ⟨b0, b0', b1, b2⟩ := tri_box _ hmpos hwm
          apply C.step_sound hrest i (by omega) _ b0 b0' b1 b2 e he
          rw [← htri]
          exact hin
        · exfalso
          have hshort' := C.short_sound hshort (orbit A (s - (i + 1))) hmpos
            (by omega) (by rw [hm]; exact hw) i (by omega)
          rw [hm, hin] at hshort'
          cases hshort'
  obtain ⟨_, hfin⟩ := key s (Nat.le_refl s)
  have hsh : s < C.h := by
    rcases Nat.lt_or_ge s C.h with hlt | hge
    · exact hlt
    · rw [C.inLayer_beyond hge] at hfin
      cases hfin
  omega

#print axioms Cert.ancestry_bound

end Agent113.TwoDigit
