import Lean

/-!
Exact overflow-tail erasure for the complementary-bulk exterior.
Words `xs` below are INSIDE-OUT (the reverse of the quotient's exterior B).
`rawRev` is the reversal of the raw overflow exterior in equation (7).
Checked with Lean 4.19.0. See verify.py and the source-pinned build record.
-/
namespace Agent9.ExteriorErasure

set_option maxRecDepth 10000
set_option maxHeartbeats 2000000

def carry (x e : Nat) : Nat := (x + e) / 10
def digit (x e : Nat) : Nat := (x + e) % 10

def Bounded (xs : List Nat) : Prop := ∀ x ∈ xs, x ≤ 18

theorem carry_bit (x e : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    carry x e ≤ 1 := by
  unfold carry
  omega

theorem carry_reduced (t z e : Nat) (ht : 1 ≤ t) (ht' : t ≤ 8)
    (hz : z ≤ 1) (he : e ≤ 1) : carry (t + 9*z) e = z := by
  unfold carry
  omega

theorem reduced_pair_sum (t k z : Nat) (ht : 1 ≤ t) (ht' : t ≤ 8)
    (hk : k ≤ 1) (hz : z ≤ 1) :
    digit (t+9*k) z + digit (t+9*z) k = 2*t := by
  have h1 := carry_reduced t k z ht ht' hk hz
  have h2 := carry_reduced t z k ht ht' hz hk
  unfold carry at h1 h2
  unfold digit
  omega

/-- The local matching criterion used at every overflow-tail column. -/
theorem overflow_link_iff (t k x a : Nat) (ht : 1 ≤ t) (ht' : t ≤ 8)
    (hk : k ≤ 1) (hx : x ≤ 18) (ha : a ≤ 1) :
    (digit (t+9*k) (carry x a) + digit x k = 2*t) ↔
      (x = t ∨ x = t+9) := by
  have hca := carry_bit x a hx ha
  have hfirst := carry_reduced t k (carry x a) ht ht' hk hca
  by_cases hlo : x ≤ 8
  · have h1 : carry x a = 0 := by unfold carry; omega
    have h2 : carry x k = 0 := by unfold carry; omega
    unfold carry digit at *
    omega
  · by_cases hn : x = 9
    · subst x
      have h1 : carry 9 a = a := by unfold carry; omega
      have h2 : carry 9 k = k := by unfold carry; omega
      unfold carry digit at *
      omega
    · have h1 : carry x a = 1 := by unfold carry; omega
      have h2 : carry x k = 1 := by unfold carry; omega
      unfold carry digit at *
      omega

/-- With the final forward carry fixed to k, a no-overflow paired column
can match the bulk only when the source coefficient and incoming carry do. -/
theorem no_overflow_column_iff (t k x a : Nat) (_ht : 1 ≤ t) (_ht' : t ≤ 8)
    (hk : k ≤ 1) (hx : x ≤ 18) (ha : a ≤ 1) (hout : carry x a = k) :
    (digit x a + digit x k = 2*t) ↔ (x = t+9*k ∧ a = k) := by
  have hsecond : carry x k = k := by
    by_cases hlo : x ≤ 8
    · unfold carry at *; omega
    · by_cases hn : x = 9
      · subst x; unfold carry at *; omega
      · unfold carry at *; omega
  unfold carry digit at *
  omega

theorem no_overflow_last_iff (t k a : Nat) (ht : 1 ≤ t) (ht' : t ≤ 8)
    (hk : k ≤ 1) (ha : a ≤ 1) :
    (digit (t+9*k) a + t = 2*t) ↔ a = k := by
  unfold digit
  omega

/-- Carry travelling from the finite exterior toward the bulk. -/
def inward : List Nat → Nat → Nat
  | [], e => e
  | x::xs, e => carry x (inward xs e)

/-- Digits of that normalization, read inside-out. -/
def lowDigits : List Nat → Nat → List Nat
  | [], _ => []
  | x::xs, e => digit x (inward xs e) :: lowDigits xs e

/-- The reflected high-side normalization, read inside-out. -/
def highDigits : List Nat → Nat → List Nat
  | [], _ => []
  | x::xs, k => digit x k :: highDigits xs (carry x k)

def outward : List Nat → Nat → Nat
  | [], k => k
  | x::xs, k => outward xs (carry x k)

/-- Reversal of the raw overflow exterior. c=t+9*k; c'=2*t. -/
def rawRev (t k : Nat) (xs : List Nat) : List Nat :=
  List.zipWith (· + ·)
    (digit (t+9*k) (inward xs 0) :: lowDigits xs 0)
    (highDigits xs k ++ [1])

def runEq (v : Nat) : List Nat → Nat
  | [] => 0
  | x::xs => if x = v then 1 + runEq v xs else 0

def runReduced (t : Nat) : List Nat → Nat
  | [] => 0
  | x::xs => if x = t ∨ x = t+9 then 1 + runReduced t xs else 0

theorem bounded_tail {x : Nat} {xs : List Nat} (h : Bounded (x::xs)) :
    Bounded xs := by
  intro y hy
  exact h y (List.mem_cons_of_mem x hy)

theorem bounded_head {x : Nat} {xs : List Nat} (h : Bounded (x::xs)) :
    x ≤ 18 := by
  exact h x (by simp)

theorem inward_bit (xs : List Nat) (e : Nat) (h : Bounded xs) (he : e ≤ 1) :
    inward xs e ≤ 1 := by
  induction xs with
  | nil => exact he
  | cons x xs ih =>
      exact carry_bit x (inward xs e) (bounded_head h)
        (ih (bounded_tail h))

theorem rawRev_cons (t k x : Nat) (xs : List Nat) :
    rawRev t k (x::xs) =
      (digit (t+9*k) (carry x (inward xs 0)) + digit x k) ::
      List.zipWith (· + ·)
        (digit x (inward xs 0) :: lowDigits xs 0)
        (highDigits xs (carry x k) ++ [1]) := by
  rfl

/-- An erasable coefficient contributes exactly one matching output column
and resets the remaining inside-out normalization to its own carry bit. -/
theorem rawRev_cons_reduced (t k z : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hk : k ≤ 1) (hz : z ≤ 1)
    (hxs : Bounded xs) :
    rawRev t k ((t+9*z)::xs) = 2*t :: rawRev t z xs := by
  rw [rawRev_cons]
  have ha := inward_bit xs 0 hxs (by omega)
  rw [carry_reduced t z (inward xs 0) ht ht' hz ha,
      carry_reduced t z k ht ht' hz hk,
      reduced_pair_sum t k z ht ht' hk hz]
  rfl

/-- Exact all-length overflow erasure: maximal matching raw suffix equals
maximal source suffix over {t,t+9}. `xs` is reverse B. -/
theorem overflow_erasure (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (k : Nat) (hk : k ≤ 1) (hover : outward xs k = 1) :
    runEq (2*t) (rawRev t k xs) = runReduced t xs := by
  induction xs generalizing k with
  | nil =>
      have hk1 : k = 1 := hover
      subst k
      have hstop : digit (t+9*1) 0 + 1 ≠ 2*t := by
        unfold digit
        omega
      simp [rawRev, inward, lowDigits, highDigits, runEq, runReduced, hstop]
  | cons x xs ih =>
      have hx := bounded_head hxs
      have htail := bounded_tail hxs
      by_cases hred : x = t ∨ x = t+9
      · rcases hred with h | h
        · subst x
          have hcarry : carry t k = 0 := by
            simpa using carry_reduced t 0 k ht ht' (by omega) hk
          have hover' : outward xs 0 = 1 := by
            simpa [outward, hcarry] using hover
          have hraw : rawRev t k (t::xs) = 2*t :: rawRev t 0 xs := by
            simpa using rawRev_cons_reduced t k 0 xs ht ht' hk (by omega) htail
          rw [hraw]
          simp only [runEq, runReduced, if_pos rfl, true_or, if_true]
          rw [ih htail 0 (by omega) hover']
        · subst x
          have hcarry : carry (t+9) k = 1 := by
            simpa using carry_reduced t 1 k ht ht' (by omega) hk
          have hover' : outward xs 1 = 1 := by
            simpa [outward, hcarry] using hover
          have hraw : rawRev t k ((t+9)::xs) = 2*t :: rawRev t 1 xs := by
            simpa using rawRev_cons_reduced t k 1 xs ht ht' hk (by omega) htail
          rw [hraw]
          simp only [runEq, runReduced, if_pos rfl, or_true, if_true]
          rw [ih htail 1 (by omega) hover']
      · have ha := inward_bit xs 0 htail (by omega)
        have hn : digit (t+9*k) (carry x (inward xs 0)) + digit x k ≠ 2*t := by
          intro h
          exact hred ((overflow_link_iff t k x (inward xs 0) ht ht' hk hx ha).mp h)
        rw [rawRev_cons]
        simp [runEq, runReduced, hn, hred]

theorem runReduced_le_length (t : Nat) (xs : List Nat) :
    runReduced t xs ≤ xs.length := by
  induction xs with
  | nil => simp [runReduced]
  | cons x xs ih =>
      simp only [runReduced, List.length_cons]
      split <;> omega

theorem overflow_never_erases_sentinel (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (k : Nat) (hk : k ≤ 1) (hover : outward xs k = 1) :
    runEq (2*t) (rawRev t k xs) ≤ xs.length := by
  rw [overflow_erasure t xs ht ht' hxs k hk hover]
  exact runReduced_le_length t xs


/-- Reversed raw exterior for equation (6), the no-overflow case. -/
def rawNoRev (t k : Nat) (xs : List Nat) : List Nat :=
  (digit (t+9*k) (inward xs 0) + t) ::
    List.zipWith (· + ·) (lowDigits xs 0) (highDigits xs k)

/-- The original exterior has no suffix equal to its current phase. -/
def Trimmed (c : Nat) : List Nat → Prop
  | [] => True
  | x::_ => x ≠ c

/-- Exact no-overflow rule on trimmed exteriors. The algebraic formula
itself needs no final-overflow assumption; actual use selects equation (6). -/
theorem no_overflow_erasure (t k : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hk : k ≤ 1)
    (hxs : Bounded xs) (htrim : Trimmed (t+9*k) xs) :
    runEq (2*t) (rawNoRev t k xs) = if inward xs 0 = k then 1 else 0 := by
  have hi := inward_bit xs 0 hxs (by omega)
  by_cases hm : inward xs 0 = k
  · have hfirst : digit (t+9*k) (inward xs 0) + t = 2*t :=
      (no_overflow_last_iff t k (inward xs 0) ht ht' hk hi).mpr hm
    rw [if_pos hm]
    cases xs with
    | nil => simp [rawNoRev, lowDigits, highDigits, runEq, hfirst]
    | cons x xs =>
        have hx := bounded_head hxs
        have htail := bounded_tail hxs
        have ha := inward_bit xs 0 htail (by omega)
        have hsecond : digit x (inward xs 0) + digit x k ≠ 2*t := by
          intro heq
          have h := (no_overflow_column_iff t k x (inward xs 0)
            ht ht' hk hx ha hm).mp heq
          exact htrim h.1
        simp [rawNoRev, lowDigits, highDigits, runEq, hfirst, hsecond]
  · have hfirst : digit (t+9*k) (inward xs 0) + t ≠ 2*t := by
      intro h
      exact hm ((no_overflow_last_iff t k (inward xs 0) ht ht' hk hi).mp h)
    simp [rawNoRev, runEq, hfirst, hm]

theorem no_overflow_erasure_le_one (t k : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hk : k ≤ 1)
    (hxs : Bounded xs) (htrim : Trimmed (t+9*k) xs) :
    runEq (2*t) (rawNoRev t k xs) ≤ 1 := by
  rw [no_overflow_erasure t k xs ht ht' hk hxs htrim]
  split <;> omega

def AllReduced (t : Nat) (xs : List Nat) : Prop :=
  ∀ x ∈ xs, x = t ∨ x = t+9

theorem allReduced_tail (t x : Nat) (xs : List Nat)
    (h : AllReduced t (x::xs)) : AllReduced t xs := by
  intro y hy
  exact h y (List.mem_cons_of_mem x hy)

/-- An overflowing exterior consisting wholly of the erasure alphabet
collapses to one coefficient t. This is an exact word identity. -/
theorem full_binary_collapse (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (hred : AllReduced t xs) (k : Nat) (hk : k ≤ 1)
    (hover : outward xs k = 1) :
    rawRev t k xs = List.replicate xs.length (2*t) ++ [t] := by
  induction xs generalizing k with
  | nil =>
      have hk1 : k = 1 := hover
      subst k
      have hlast : digit (t+9*1) 0 + 1 = t := by unfold digit; omega
      simpa [rawRev, inward, lowDigits, highDigits] using hlast
  | cons x xs ih =>
      have htail := bounded_tail hxs
      have hrt := allReduced_tail t x xs hred
      have hr : x = t ∨ x = t+9 := hred x (by simp)
      rcases hr with h | h
      · subst x
        have hc : carry t k = 0 := by
          simpa using carry_reduced t 0 k ht ht' (by omega) hk
        have ho : outward xs 0 = 1 := by simpa [outward, hc] using hover
        have hraw : rawRev t k (t::xs) = 2*t :: rawRev t 0 xs := by
          simpa using rawRev_cons_reduced t k 0 xs ht ht' hk (by omega) htail
        rw [hraw, ih htail hrt 0 (by omega) ho]
        simp [List.replicate_succ]
      · subst x
        have hc : carry (t+9) k = 1 := by
          simpa using carry_reduced t 1 k ht ht' (by omega) hk
        have ho : outward xs 1 = 1 := by simpa [outward, hc] using hover
        have hraw : rawRev t k ((t+9)::xs) = 2*t :: rawRev t 1 xs := by
          simpa using rawRev_cons_reduced t k 1 xs ht ht' hk (by omega) htail
        rw [hraw, ih htail hrt 1 (by omega) ho]
        simp [List.replicate_succ]

theorem lowDigits_length (xs : List Nat) (e : Nat) :
    (lowDigits xs e).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [lowDigits, ih]

theorem highDigits_length (xs : List Nat) (e : Nat) :
    (highDigits xs e).length = xs.length := by
  induction xs generalizing e with
  | nil => rfl
  | cons x xs ih => simp [highDigits, ih]

theorem rawRev_length (t k : Nat) (xs : List Nat) :
    (rawRev t k xs).length = xs.length + 1 := by
  simp [rawRev, lowDigits_length, highDigits_length]

theorem rawNoRev_length (t k : Nat) (xs : List Nat) :
    (rawNoRev t k xs).length = xs.length + 1 := by
  simp [rawNoRev, lowDigits_length, highDigits_length]

/-- Drop exactly the initial equal run (reverse of exterior suffix trimming). -/
def strip (v : Nat) (xs : List Nat) : List Nat := xs.drop (runEq v xs)

theorem overflow_exterior_length (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (k : Nat) (hk : k ≤ 1) (hover : outward xs k = 1) :
    (strip (2*t) (rawRev t k xs)).length = xs.length + 1 - runReduced t xs := by
  simp [strip, rawRev_length, overflow_erasure t xs ht ht' hxs k hk hover]

theorem overflow_exterior_nonempty (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (k : Nat) (hk : k ≤ 1) (hover : outward xs k = 1) :
    1 ≤ (strip (2*t) (rawRev t k xs)).length := by
  rw [overflow_exterior_length t xs ht ht' hxs k hk hover]
  have := runReduced_le_length t xs
  omega

theorem no_overflow_exterior_length (t k : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hk : k ≤ 1)
    (hxs : Bounded xs) (htrim : Trimmed (t+9*k) xs) :
    (strip (2*t) (rawNoRev t k xs)).length =
      xs.length + if inward xs 0 = k then 0 else 1 := by
  simp only [strip, List.length_drop, rawNoRev_length,
    no_overflow_erasure t k xs ht ht' hk hxs htrim]
  split <;> omega

theorem no_overflow_exterior_nondecreasing (t k : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hk : k ≤ 1)
    (hxs : Bounded xs) (htrim : Trimmed (t+9*k) xs) :
    xs.length ≤ (strip (2*t) (rawNoRev t k xs)).length := by
  rw [no_overflow_exterior_length t k xs ht ht' hk hxs htrim]
  omega



theorem runReduced_eq_length (t : Nat) (xs : List Nat)
    (hred : AllReduced t xs) : runReduced t xs = xs.length := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      have hr : x = t ∨ x = t+9 := hred x (by simp)
      have htail := allReduced_tail t x xs hred
      simp [runReduced, hr, ih htail, Nat.add_comm]

theorem strip_full_binary_collapse (t : Nat) (xs : List Nat)
    (ht : 1 ≤ t) (ht' : t ≤ 8) (hxs : Bounded xs)
    (hred : AllReduced t xs) (k : Nat) (hk : k ≤ 1)
    (hover : outward xs k = 1) :
    strip (2*t) (rawRev t k xs) = [t] := by
  unfold strip
  rw [overflow_erasure t xs ht ht' hxs k hk hover,
    runReduced_eq_length t xs hred,
    full_binary_collapse t xs ht ht' hxs hred k hk hover]
  simp

#print axioms carry_bit
#print axioms carry_reduced
#print axioms reduced_pair_sum
#print axioms overflow_link_iff
#print axioms no_overflow_column_iff
#print axioms no_overflow_last_iff
#print axioms bounded_tail
#print axioms bounded_head
#print axioms inward_bit
#print axioms rawRev_cons
#print axioms rawRev_cons_reduced
#print axioms overflow_erasure
#print axioms runReduced_le_length
#print axioms overflow_never_erases_sentinel

#print axioms no_overflow_erasure
#print axioms no_overflow_erasure_le_one
#print axioms allReduced_tail
#print axioms full_binary_collapse
#print axioms lowDigits_length
#print axioms highDigits_length
#print axioms rawRev_length
#print axioms rawNoRev_length
#print axioms overflow_exterior_length
#print axioms overflow_exterior_nonempty
#print axioms no_overflow_exterior_length
#print axioms no_overflow_exterior_nondecreasing
#print axioms runReduced_eq_length
#print axioms strip_full_binary_collapse

end Agent9.ExteriorErasure
