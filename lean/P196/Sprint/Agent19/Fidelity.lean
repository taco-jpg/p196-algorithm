import P196.Agent117P2641.Agent124PrefixL

/-!
# Agent 19 review: plain-arithmetic reading of the prefix predicates

The prefix exclusions under review are stated with `Canonical`-digit predicates
(`Agent124.PrefixL.StartsL`, `Agent124.PrefixK.Starts3`, `Agent118.PrefixKernel.Starts3`,
`SevenColumnKernel.PalindromeBridge.Starts739`).  This file proves that each of them is
implied by the plain arithmetic statement "some truncation `n / 10 ^ k` equals the
prefix read as a number", for every nonempty digit list with a nonzero leading digit.

Consequently every exclusion `¬ PalStartsL pre (orbit 196 t)` implies the plain form
`Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ fromDigits pre` for all `k`
(see `ArithLight.lean` / `ArithHeavy.lean`).  The converse direction is not needed for
that reading and is not proved here.
-/

namespace Sprint.Agent19.Fidelity

open DecimalDigits Lychrel196 Agent124.PrefixL

/-- Big-endian value of a digit list: `fromDigits [2, 1, 7] = 217`. -/
def fromDigits : List Nat → Nat
  | [] => 0
  | d :: ds => d * 10 ^ ds.length + fromDigits ds

/-- Decimal digit `i` of `n`, counted from the units digit `i = 0`. -/
def dig (n i : Nat) : Nat := n / 10 ^ i % 10

theorem fromDigits_lt : ∀ l : List Nat, (∀ x ∈ l, x ≤ 9) → fromDigits l < 10 ^ l.length
  | [], _ => by simp [fromDigits]
  | d :: ds, h => by
      have hd : d ≤ 9 := h d (List.mem_cons_self ..)
      have ih := fromDigits_lt ds (fun x hx => h x (List.mem_cons_of_mem _ hx))
      simp only [fromDigits, List.length_cons, Nat.pow_succ]
      have hm : d * 10 ^ ds.length ≤ 9 * 10 ^ ds.length := Nat.mul_le_mul_right _ hd
      omega

/-- Digit extraction from the big-endian value. -/
theorem fromDigits_digit : ∀ l : List Nat, (∀ x ∈ l, x ≤ 9) →
    ∀ j, j < l.length → fromDigits l / 10 ^ j % 10 = l.getD (l.length - 1 - j) 0
  | [], _, j, hj => by simp at hj
  | d :: ds, h, j, hj => by
      have hd : d ≤ 9 := h d (List.mem_cons_self ..)
      have hds : ∀ x ∈ ds, x ≤ 9 := fun x hx => h x (List.mem_cons_of_mem _ hx)
      have hlt := fromDigits_lt ds hds
      simp only [List.length_cons] at hj ⊢
      simp only [fromDigits]
      by_cases hjm : j = ds.length
      · subst hjm
        have hpos : 0 < 10 ^ ds.length := Nat.pow_pos (by decide)
        rw [Nat.add_comm, Nat.add_mul_div_right _ _ hpos, Nat.div_eq_of_lt hlt]
        simp only [Nat.zero_add, Nat.add_sub_cancel, Nat.sub_self, List.getD_cons_zero]
        omega
      · have hjl : j < ds.length := by omega
        have hQ : 0 < 10 ^ j := Nat.pow_pos (by decide)
        have hpow : 10 ^ ds.length = 10 ^ (ds.length - 1 - j) * 10 * 10 ^ j := by
          rw [← Nat.pow_succ, ← Nat.pow_add]
          congr 1
          omega
        have hmul : d * (10 ^ (ds.length - 1 - j) * 10 * 10 ^ j) =
            d * 10 ^ (ds.length - 1 - j) * 10 * 10 ^ j := by
          simp only [Nat.mul_assoc]
        rw [hpow, hmul, Nat.add_comm, Nat.add_mul_div_right _ _ hQ,
          show ds.length + 1 - 1 - j = (ds.length - 1 - j) + 1 by omega,
          List.getD_cons_succ, ← fromDigits_digit ds hds j hjl]
        generalize d * 10 ^ (ds.length - 1 - j) = B
        omega

theorem dig_add (n k j : Nat) : dig n (k + j) = n / 10 ^ k / 10 ^ j % 10 := by
  simp only [dig, Nat.pow_add, Nat.div_div_eq_div_mul]

theorem value_dig (n : Nat) : ∀ L, value (dig n) L = n % 10 ^ L
  | 0 => by simp [value, Nat.mod_one]
  | L + 1 => by
      rw [value, value_dig n L, Nat.mod_pow_succ]
      simp only [dig]
      rw [Nat.mul_comm]

/-- **Bridge.** If a truncation of `n` equals the prefix read as a number, then `n`
begins with that prefix in the sense of `StartsL` (canonical digits, exact width). -/
theorem startsL_of_div {pre : List Nat} {n k : Nat} (hne : pre ≠ [])
    (hd : ∀ x ∈ pre, x ≤ 9) (hlead : 1 ≤ pre.headD 0)
    (hk : n / 10 ^ k = fromDigits pre) : StartsL pre n := by
  have hm : 1 ≤ pre.length := by
    cases pre with
    | nil => exact absurd rfl hne
    | cons a s => simp
  have hlt := fromDigits_lt pre hd
  have hpos : 0 < 10 ^ k := Nat.pow_pos (by decide)
  have hn : n < 10 ^ (k + pre.length) := by
    have h1 : n / 10 ^ k < 10 ^ pre.length := by rw [hk]; exact hlt
    rw [Nat.div_lt_iff_lt_mul hpos] at h1
    rw [Nat.pow_add, Nat.mul_comm]
    exact h1
  have hdig : ∀ i, i < pre.length →
      dig n (k + pre.length - 1 - i) = pre.getD i 0 := by
    intro i hi
    rw [show k + pre.length - 1 - i = k + (pre.length - 1 - i) by omega, dig_add, hk,
      fromDigits_digit pre hd _ (by omega)]
    congr 1
    omega
  refine ⟨dig n, k + pre.length, ⟨by omega, ?_, ?_, ?_⟩, by omega, ?_⟩
  · intro i _
    simp only [dig]
    omega
  · have := hdig 0 hm
    rw [Nat.sub_zero] at this
    rw [this]
    cases pre with
    | nil => exact absurd rfl hne
    | cons a s => simpa using hlead
  · rw [value_dig, Nat.mod_eq_of_lt hn]
  · intro i hi
    have := hdig i hi
    rw [show k + pre.length - 1 - i = k + pre.length - 1 - i from rfl] at this
    exact this

/-- Plain reading of an exclusion: no palindrome iterate has a truncation equal to the
prefix. -/
theorem plain_of_palStartsL {pre : List Nat} {N : Nat} (hne : pre ≠ [])
    (hd : ∀ x ∈ pre, x ≤ 9) (hlead : 1 ≤ pre.headD 0)
    (hex : ¬ PalStartsL pre N) : Palindrome N → ∀ k, N / 10 ^ k ≠ fromDigits pre := by
  intro hp k hk
  exact hex ⟨hp, startsL_of_div hne hd hlead hk⟩

/-- Boolean form of the side conditions, for checking explicit lists by evaluation. -/
def validPrefix (pre : List Nat) : Bool :=
  !pre.isEmpty && pre.all (fun x => decide (x ≤ 9)) && decide (1 ≤ pre.headD 0)

theorem validPrefix_sound {pre : List Nat} (h : validPrefix pre = true) :
    pre ≠ [] ∧ (∀ x ∈ pre, x ≤ 9) ∧ 1 ≤ pre.headD 0 := by
  unfold validPrefix at h
  simp only [Bool.and_eq_true, Bool.not_eq_true', List.isEmpty_eq_false_iff,
    List.all_eq_true, decide_eq_true_eq] at h
  exact ⟨h.1.1, h.1.2, h.2⟩

theorem plain_of_valid {pre : List Nat} {N : Nat} (hv : validPrefix pre = true)
    (hex : ¬ PalStartsL pre N) : Palindrome N → ∀ k, N / 10 ^ k ≠ fromDigits pre :=
  let ⟨h1, h2, h3⟩ := validPrefix_sound hv
  plain_of_palStartsL h1 h2 h3 hex

/-- The three-digit predicates of Agent #124 and Agent #118 are `PalStartsL [a, b, c]`. -/
theorem palStarts3_iff (a b c P : Nat) :
    Agent124.PrefixK.PalStarts3 a b c P ↔ PalStartsL [a, b, c] P :=
  (palStartsL_three_iff a b c P).symm

end Sprint.Agent19.Fidelity

#print axioms Sprint.Agent19.Fidelity.fromDigits_digit
#print axioms Sprint.Agent19.Fidelity.startsL_of_div
#print axioms Sprint.Agent19.Fidelity.plain_of_palStartsL
#print axioms Sprint.Agent19.Fidelity.plain_of_valid
