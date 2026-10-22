import P196.Agent117P2641.Agent124PrefixL

/-!
# Red team (sprint agent 20): fidelity of `Agent124.PrefixL.PalStartsL`

`PalStartsL pre P` is stated with a digit *function* `e` and a width `W`.
Here it is compared with the textbook arithmetic meaning of
"the decimal expansion of `P` begins with the digit string `pre`":

    DecStarts pre P  :=  ∃ r, num pre * 10^r ≤ P < (num pre + 1) * 10^r

where `num pre` is the number written by `pre` (most significant digit first).

* `startsL_of_decStarts`: for every well-formed prefix (nonzero leading digit,
  all digits ≤ 9) the textbook meaning implies `StartsL`.  This is the direction
  needed for the prose: a Lean theorem `¬ PalStartsL pre (orbit 196 t)` really
  excludes every palindrome whose decimal expansion begins with `pre`.
* `decStarts_of_startsL`: the converse, so the two notions agree exactly.
* `palStartsL_lead_zero` / `palStartsL_big_digit`: for a malformed prefix
  `PalStartsL` is identically false, so an "exclusion" of such a prefix would be
  vacuous.  (All 2,494 prefixes in the repository's entry lists are well-formed;
  see `sprint/agent-20/scripts/extract_entries.py`.)
* `no_196_2641_textbook`: the 2641 endpoint restated with plain inequalities.

Nothing here concerns any prefix not already excluded; nothing here says 196 is Lychrel.
-/

namespace Sprint.Agent20

open DecimalDigits Lychrel196 Agent124.PrefixL

/-- The number written by a most-significant-first digit list. -/
def num : List Nat → Nat
  | [] => 0
  | a :: l => a * 10 ^ l.length + num l

/-- Textbook meaning: the decimal expansion of `P` begins with `pre`. -/
def DecStarts (pre : List Nat) (P : Nat) : Prop :=
  ∃ r, num pre * 10 ^ r ≤ P ∧ P < (num pre + 1) * 10 ^ r

/-- A well-formed digit prefix: nonempty, nonzero leading digit, digits ≤ 9. -/
def WellFormed (pre : List Nat) : Prop :=
  0 < pre.headD 0 ∧ ∀ d ∈ pre, d ≤ 9

instance (pre : List Nat) : Decidable (WellFormed pre) := by
  unfold WellFormed; exact inferInstance

theorem num_lt (l : List Nat) (hd : ∀ d ∈ l, d ≤ 9) : num l < 10 ^ l.length := by
  induction l with
  | nil => simp [num]
  | cons a l ih =>
    have ha : a ≤ 9 := hd a (by simp)
    have hl := ih (fun d h => hd d (by simp [h]))
    have h1 : a * 10 ^ l.length + num l < (a + 1) * 10 ^ l.length := by
      rw [Nat.succ_mul]; omega
    have h2 : (a + 1) * 10 ^ l.length ≤ 10 * 10 ^ l.length :=
      Nat.mul_le_mul_right _ (by omega)
    simp only [num, List.length_cons, Nat.pow_succ]
    rw [Nat.mul_comm (10 ^ l.length) 10]
    omega

theorem num_ge (a : Nat) (l : List Nat) (ha : 0 < a) :
    10 ^ l.length ≤ num (a :: l) := by
  simp only [num]
  have : 10 ^ l.length ≤ a * 10 ^ l.length := Nat.le_mul_of_pos_left _ ha
  omega

/-- Digit extraction from `num`. -/
theorem num_digit (l : List Nat) (hd : ∀ d ∈ l, d ≤ 9) (i : Nat) (hi : i < l.length) :
    num l / 10 ^ (l.length - 1 - i) % 10 = l.getD i 0 := by
  induction l generalizing i with
  | nil => simp at hi
  | cons a l ih =>
    have ha : a ≤ 9 := hd a (by simp)
    have hdl : ∀ d ∈ l, d ≤ 9 := fun d h => hd d (by simp [h])
    have hlt := num_lt l hdl
    have hp : 0 < 10 ^ l.length := Nat.pow_pos (by decide : 0 < 10)
    cases i with
    | zero =>
      simp only [num, List.length_cons, Nat.add_sub_cancel, Nat.sub_zero, List.getD_cons_zero]
      rw [Nat.mul_comm, Nat.mul_add_div hp, Nat.div_eq_of_lt hlt, Nat.add_zero]
      exact Nat.mod_eq_of_lt (by omega)
    | succ j =>
      simp only [List.length_cons] at hi
      have hj : j < l.length := by omega
      simp only [num, List.length_cons, List.getD_cons_succ]
      have he : l.length + 1 - 1 - (j + 1) = l.length - 1 - j := by omega
      rw [he]
      let e := l.length - 1 - j
      have hsplit : 10 ^ l.length = 10 ^ e * (10 * 10 ^ j) := by
        rw [← Nat.pow_succ', ← Nat.pow_add]; (congr 1; try omega)
      have hpe : 0 < 10 ^ e := Nat.pow_pos (by decide : 0 < 10)
      have : a * 10 ^ l.length + num l = 10 ^ e * (a * (10 * 10 ^ j)) + num l := by
        rw [hsplit]; rw [Nat.mul_left_comm]
      rw [this, Nat.mul_add_div hpe]
      have hmod : (a * (10 * 10 ^ j) + num l / 10 ^ e) % 10 = num l / 10 ^ e % 10 := by
        rw [Nat.add_comm, show a * (10 * 10 ^ j) = 10 * (a * 10 ^ j) by
          rw [Nat.mul_left_comm]]
        exact Nat.add_mul_mod_self_left _ _ _
      rw [hmod]
      exact ih hdl j hj

/-- The value of the digit function `i ↦ P / 10^i % 10` over `W` places. -/
theorem value_digits (P W : Nat) :
    value (fun i => P / 10 ^ i % 10) W = P % 10 ^ W := by
  induction W with
  | zero => simp [value, Nat.mod_one]
  | succ W ih =>
    simp only [value, ih, Nat.mod_pow_succ]
    rw [Nat.mul_comm]

/-- **Fidelity (needed direction).** Every number whose decimal expansion
begins with the well-formed prefix `pre` satisfies `StartsL pre`. -/
theorem startsL_of_decStarts (pre : List Nat) (hw : WellFormed pre) (P : Nat)
    (h : DecStarts pre P) : StartsL pre P := by
  obtain ⟨hlead, hd⟩ := hw
  obtain ⟨r, hlo, hhi⟩ := h
  cases pre with
  | nil => simp at hlead
  | cons a l =>
    let n := l.length + 1
    have hn : (a :: l).length = n := rfl
    let W := r + n
    let e : Nat → Nat := fun i => P / 10 ^ i % 10
    have hlt := num_lt (a :: l) hd
    have hge := num_ge a l (by simpa using hlead)
    have hpr : 0 < 10 ^ r := Nat.pow_pos (by decide : 0 < 10)
    -- P < 10^W
    have hPW : P < 10 ^ W := by
      have h1 : (num (a :: l) + 1) * 10 ^ r ≤ 10 ^ n * 10 ^ r :=
        Nat.mul_le_mul_right _ (by simpa [hn] using hlt)
      have h2 : 10 ^ n * 10 ^ r = 10 ^ W := by
        rw [← Nat.pow_add, Nat.add_comm]
      omega
    -- 10^(W-1) ≤ P
    have hPW1 : 10 ^ (W - 1) ≤ P := by
      have h1 : 10 ^ l.length * 10 ^ r ≤ num (a :: l) * 10 ^ r := Nat.mul_le_mul_right _ hge
      have h2 : 10 ^ l.length * 10 ^ r = 10 ^ (W - 1) := by
        rw [← Nat.pow_add]; (congr 1; try omega)
      omega
    -- the quotient by 10^r is the prefix number
    have hq : P / 10 ^ r = num (a :: l) := by
      apply Nat.div_eq_of_lt_le
      · exact hlo
      · exact hhi
    refine ⟨e, W, ⟨by omega, fun i _ => by show P / 10 ^ i % 10 ≤ 9; have := Nat.mod_lt (P / 10 ^ i) (show 10 > 0 by decide); omega, ?_, ?_⟩, by omega, ?_⟩
    · -- nonzero leading digit
      have hW1 : 10 ^ W = 10 * 10 ^ (W - 1) := by
        rw [← Nat.pow_succ']; (congr 1; try omega)
      have hp1 : 0 < 10 ^ (W - 1) := Nat.pow_pos (by decide : 0 < 10)
      have hq1 : 1 ≤ P / 10 ^ (W - 1) := (Nat.le_div_iff_mul_le hp1).mpr (by omega)
      have hq2 : P / 10 ^ (W - 1) < 10 := (Nat.div_lt_iff_lt_mul hp1).mpr (by rw [← hW1]; exact hPW)
      show 0 < P / 10 ^ (W - 1) % 10
      rw [Nat.mod_eq_of_lt hq2]; omega
    · -- exact value
      rw [value_digits, Nat.mod_eq_of_lt hPW]
    · -- prefix digits
      intro i hi
      have hi' : i < n := hi
      show P / 10 ^ (W - 1 - i) % 10 = (a :: l).getD i 0
      have hexp : W - 1 - i = r + (n - 1 - i) := by omega
      rw [hexp, Nat.pow_add, ← Nat.div_div_eq_div_mul, hq]
      have := num_digit (a :: l) hd i (by simpa [hn] using hi')
      simpa [hn] using this

theorem value_lt (e : Nat → Nat) (L : Nat) (hd : ∀ j, j < L → e j ≤ 9) :
    value e L < 10 ^ L := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have h1 := ih (fun j hj => hd j (by omega))
    have h2 : e L * 10 ^ L ≤ 9 * 10 ^ L := Nat.mul_le_mul_right _ (hd L (by omega))
    simp only [value, Nat.pow_succ]
    omega

theorem value_digit (e : Nat → Nat) (L : Nat) (hd : ∀ j, j < L → e j ≤ 9) :
    ∀ i, i < L → value e L / 10 ^ i % 10 = e i := by
  induction L with
  | zero => intro i hi; omega
  | succ L ih =>
    intro i hi
    have hbL : ∀ j, j < L → e j ≤ 9 := fun j hj => hd j (by omega)
    have hvl := value_lt e L hbL
    have hp : 0 < 10 ^ i := Nat.pow_pos (by decide : 0 < 10)
    by_cases hiL : i < L
    · have hsplit : 10 ^ L = 10 ^ i * (10 * 10 ^ (L - 1 - i)) := by
        rw [← Nat.pow_succ', ← Nat.pow_add]; (congr 1; try omega)
      have heq : value e (L + 1) = 10 ^ i * (e L * (10 * 10 ^ (L - 1 - i))) + value e L := by
        simp only [value]; rw [hsplit, Nat.mul_left_comm, Nat.add_comm]
      rw [heq, Nat.mul_add_div hp,
        show e L * (10 * 10 ^ (L - 1 - i)) = 10 * (e L * 10 ^ (L - 1 - i)) by
          rw [Nat.mul_left_comm],
        Nat.add_comm, Nat.add_mul_mod_self_left]
      exact ih hbL i hiL
    · have hi' : i = L := by omega
      subst hi'
      have heq : value e (i + 1) = 10 ^ i * e i + value e i := by
        simp only [value]; rw [Nat.mul_comm, Nat.add_comm]
      rw [heq, Nat.mul_add_div hp, Nat.div_eq_of_lt hvl, Nat.add_zero]
      exact Nat.mod_eq_of_lt (by have := hd i (by omega); omega)

theorem num_snoc (u : List Nat) (y : Nat) : num (u ++ [y]) = 10 * num u + y := by
  induction u with
  | nil => simp [num]
  | cons b u ihu =>
    simp only [List.cons_append, num, List.length_append, List.length_singleton, ihu]
    rw [Nat.pow_succ, Nat.mul_add]
    have : b * (10 ^ u.length * 10) = 10 * (b * 10 ^ u.length) := by
      rw [← Nat.mul_assoc, Nat.mul_comm (b * 10 ^ u.length) 10]
    omega

/-- The top `m` digits of a canonical numeral, read as a number. -/
theorem num_top (P W : Nat) (hPW : P < 10 ^ W) :
    ∀ (m : Nat) (l : List Nat), l.length = m → m ≤ W →
      (∀ i, i < m → l.getD i 0 = P / 10 ^ (W - 1 - i) % 10) →
      num l = P / 10 ^ (W - m) := by
  intro m
  induction m with
  | zero =>
    intro l hl _ _
    have : l = [] := List.eq_nil_of_length_eq_zero hl
    subst this
    simp only [num, Nat.sub_zero]
    exact (Nat.div_eq_of_lt hPW).symm
  | succ m ih =>
    intro l hl hm hdig'
    obtain ⟨l', x, rfl⟩ : ∃ l' x, l = l' ++ [x] := by
      have hne : l ≠ [] := by intro h; subst h; simp at hl
      exact ⟨l.dropLast, l.getLast hne, (List.dropLast_concat_getLast hne).symm⟩
    simp only [List.length_append, List.length_singleton] at hl
    have hl' : l'.length = m := by omega
    have h1 := ih l' hl' (by omega) (fun i hi => by
      have := hdig' i (by omega)
      rwa [List.getD_eq_getElem?_getD, List.getElem?_append_left (by omega),
        ← List.getD_eq_getElem?_getD] at this)
    have hx : x = P / 10 ^ (W - 1 - m) % 10 := by
      have := hdig' m (by omega)
      rw [List.getD_eq_getElem?_getD, List.getElem?_append_right (by omega), hl',
        Nat.sub_self] at this
      simpa using this
    rw [num_snoc, h1, hx]
    have he1 : W - m = (W - (m + 1)) + 1 := by omega
    have he2 : W - 1 - m = W - (m + 1) := by omega
    rw [he1, he2, Nat.pow_succ, ← Nat.div_div_eq_div_mul]
    exact Nat.div_add_mod _ 10

/-- The converse: `StartsL` implies the textbook meaning. -/
theorem decStarts_of_startsL (pre : List Nat) (P : Nat) (h : StartsL pre P) :
    DecStarts pre P := by
  obtain ⟨e, W, ⟨hW, hd, hlead, hv⟩, hlen, hpre⟩ := h
  have hPW : P < 10 ^ W := by rw [← hv]; exact value_lt e W hd
  have hdig : ∀ i, i < W → P / 10 ^ i % 10 = e i := by
    intro i hi; rw [← hv]; exact value_digit e W hd i hi
  have hpre' : ∀ i, i < pre.length → pre.getD i 0 = P / 10 ^ (W - 1 - i) % 10 := by
    intro i hi; rw [← hpre i hi, hdig _ (by omega)]
  have hnum : num pre = P / 10 ^ (W - pre.length) :=
    num_top P W hPW pre.length pre rfl hlen hpre'
  have hp : 0 < 10 ^ (W - pre.length) := Nat.pow_pos (by decide : 0 < 10)
  refine ⟨W - pre.length, ?_, ?_⟩
  · rw [hnum]; exact Nat.div_mul_le_self P _
  · rw [hnum, Nat.add_mul, Nat.one_mul]
    have h1 := Nat.div_add_mod P (10 ^ (W - pre.length))
    have h2 := Nat.mod_lt P hp
    rw [Nat.mul_comm] at h1
    omega

theorem startsL_iff_decStarts (pre : List Nat) (hw : WellFormed pre) (P : Nat) :
    StartsL pre P ↔ DecStarts pre P :=
  ⟨decStarts_of_startsL pre P, startsL_of_decStarts pre hw P⟩

/-- A prefix with leading zero is never matched: such an "exclusion" is vacuous. -/
theorem palStartsL_lead_zero (pre : List Nat) (P : Nat) : ¬ PalStartsL (0 :: pre) P := by
  rintro ⟨_, e, W, ⟨hW, _, hlead, _⟩, _, h⟩
  have := h 0 (by simp)
  simp at this
  omega

/-- A prefix containing an entry ≥ 10 is never matched: such an "exclusion" is vacuous. -/
theorem palStartsL_big_digit (pre : List Nat) (P : Nat) (i : Nat) (hi : i < pre.length)
    (hbig : 10 ≤ pre.getD i 0) : ¬ PalStartsL pre P := by
  rintro ⟨_, e, W, ⟨hW, hd, _, _⟩, hlen, h⟩
  have := h i hi
  have := hd (W - 1 - i) (by omega)
  omega

/-- Generic transfer: an `entries`-style exclusion of a well-formed prefix excludes
every palindrome whose decimal expansion begins with that prefix. -/
theorem no_196_textbook (pre : List Nat) (hw : WellFormed pre)
    (h : ∀ t, ¬ PalStartsL pre (orbit 196 t)) :
    ∀ t r, ¬ (Palindrome (orbit 196 t) ∧
      num pre * 10 ^ r ≤ orbit 196 t ∧ orbit 196 t < (num pre + 1) * 10 ^ r) := by
  rintro t r ⟨hp, hlo, hhi⟩
  exact h t ⟨hp, startsL_of_decStarts pre hw _ ⟨r, hlo, hhi⟩⟩

end Sprint.Agent20

#print axioms Sprint.Agent20.startsL_of_decStarts
#print axioms Sprint.Agent20.decStarts_of_startsL
#print axioms Sprint.Agent20.startsL_iff_decStarts
#print axioms Sprint.Agent20.palStartsL_lead_zero
#print axioms Sprint.Agent20.palStartsL_big_digit
#print axioms Sprint.Agent20.no_196_textbook
