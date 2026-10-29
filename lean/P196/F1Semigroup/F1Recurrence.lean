import P196.F1Semigroup.F1MinDFA
/-!
# Audit formalization, part 4: the order-10 recurrence for the number of rooted accepted words

`a n` = number of length-`n` words `w` with `LangB w` (i.e. a closed walk of the F1 automaton labelled `w`).
We prove, for all `m`:

  a (m+10) = a (m+8) + a (m+7) + a (m+6) + a (m+5) + a (m+3) + 2 * a (m+1)

and the initial values `a 0 .. a 9 = 1, 0, 2, 3, 6, 10, 11, 28, 30, 75`
(this is `a(n) = a(n-2)+a(n-3)+a(n-4)+a(n-5)+a(n-7)+2a(n-9)`, `n ≥ 10`, of `Agent9F1AllPeriodRecurrence`).
The proof is a finite check of the identity on all 434 reachable relation states plus induction.
-/
namespace F1

def allWords : Nat → List (List Bool)
  | 0 => [[]]
  | n + 1 => (allWords n).map (fun w => false :: w) ++ (allWords n).map (fun w => true :: w)

theorem mem_allWords : ∀ (w : List Bool), w ∈ allWords w.length := by
  intro w
  induction w with
  | nil => simp [allWords]
  | cons a w ih =>
    cases a <;> simp [allWords, ih]

theorem length_allWords (n : Nat) : (allWords n).length = 2 ^ n := by
  induction n with
  | zero => simp [allWords]
  | succ n ih => simp [allWords, ih, Nat.pow_succ]; omega

theorem mem_allWords_length : ∀ (n : Nat) (w : List Bool), w ∈ allWords n → w.length = n := by
  intro n
  induction n with
  | zero => intro w hw; simp [allWords] at hw; simp [hw]
  | succ n ih =>
    intro w hw
    simp only [allWords, List.mem_append, List.mem_map] at hw
    rcases hw with ⟨v, hv, rfl⟩ | ⟨v, hv, rfl⟩ <;> simp [ih v hv]

theorem nodup_allWords : ∀ n, (allWords n).Nodup := by
  intro n
  induction n with
  | zero => simp [allWords]
  | succ n ih =>
    simp only [allWords]
    unfold List.Nodup
    rw [List.pairwise_append]
    refine ⟨?_, ?_, ?_⟩
    · exact List.Pairwise.map (fun w : List Bool => false :: w) (fun a b h h2 => h (List.cons.inj h2).2) ih
    · exact List.Pairwise.map (fun w : List Bool => true :: w) (fun a b h h2 => h (List.cons.inj h2).2) ih
    · intro x hx y hy hxy
      simp only [List.mem_map] at hx hy
      obtain ⟨v, _, rfl⟩ := hx
      obtain ⟨u, _, rfl⟩ := hy
      simp at hxy

/-- number of length-`n` words accepted from the relation state `r` -/
def cntFrom (n : Nat) (r : Rel) : Nat := ((allWords n).filter (fun w => accept (run r w))).length

/-- `a n`: number of length-`n` words in the language (= number of rooted F1-legal overflow words) -/
def a (n : Nat) : Nat := cntFrom n initRel

theorem a_eq_count (n : Nat) : a n = ((allWords n).filter LangB).length := rfl

theorem cntFrom_succ (n : Nat) (r : Rel) :
    cntFrom (n + 1) r = cntFrom n (delta false r) + cntFrom n (delta true r) := by
  unfold cntFrom
  simp only [allWords, List.filter_append, List.length_append, List.filter_map, List.length_map]
  have e1 : ((fun w => accept (run r w)) ∘ fun w => false :: w) = (fun w => accept (run (delta false r) w)) := by
    funext w; rfl
  have e2 : ((fun w => accept (run r w)) ∘ fun w => true :: w) = (fun w => accept (run (delta true r) w)) := by
    funext w; rfl
  rw [e1, e2]

theorem cntFrom_zero (r : Rel) : cntFrom 0 r = if accept r then 1 else 0 := by
  unfold cntFrom
  cases h : accept r <;> simp [allWords, run, h]

/-! ## Level tables, packed 12 bits per state -/

def vget (V i : Nat) : Nat := (V >>> (12 * i)) % 4096

def v0 : Nat := (List.range nS).foldl (fun acc i => acc + ((if accQ i then 1 else 0) <<< (12 * i))) 0

def vnext (V : Nat) : Nat :=
  (List.range nS).foldl (fun acc i => acc + ((vget V (Nget false i) + vget V (Nget true i)) <<< (12 * i))) 0

def vk : Nat → Nat
  | 0 => v0
  | k + 1 => vnext (vk k)

def W (k i : Nat) : Nat := vget (vk k) i

def stepOK (k i : Nat) : Bool := decide (W (k + 1) i = W k (Nget false i) + W k (Nget true i))

theorem W0_ok : ∀ i, i < nS → W 0 i = if accQ i then 1 else 0 := by decide +kernel

theorem stepOK_all : ∀ k, k < 10 → ∀ i, i < nS → stepOK k i = true := by decide +kernel

theorem W_succ (k i : Nat) (hk : k < 10) (hi : i < nS) :
    W (k + 1) i = W k (Nget false i) + W k (Nget true i) := by
  have := stepOK_all k hk i hi
  simpa [stepOK] using this

theorem W_eq_cnt : ∀ k, k ≤ 10 → ∀ i, i < nS → W k i = cntFrom k (Sget i) := by
  intro k
  induction k with
  | zero =>
    intro _ i hi
    rw [W0_ok i hi, cntFrom_zero, accQ_eq i hi]
    rfl
  | succ k ih =>
    intro hk i hi
    rw [W_succ k i (by omega) hi, cntFrom_succ]
    obtain ⟨h1, h2⟩ := tab_step false i hi
    obtain ⟨h3, h4⟩ := tab_step true i hi
    rw [← h2, ← h4, ih (by omega) _ h1, ih (by omega) _ h3]

/-- the base identity on all 434 states -/
theorem base_ok : ∀ i, i < nS →
    W 10 i = W 8 i + W 7 i + W 6 i + W 5 i + W 3 i + 2 * W 1 i := by decide +kernel

theorem base_cnt (i : Nat) (hi : i < nS) :
    cntFrom 10 (Sget i) = cntFrom 8 (Sget i) + cntFrom 7 (Sget i) + cntFrom 6 (Sget i) +
      cntFrom 5 (Sget i) + cntFrom 3 (Sget i) + 2 * cntFrom 1 (Sget i) := by
  have h := base_ok i hi
  rw [W_eq_cnt 10 (by omega) i hi, W_eq_cnt 8 (by omega) i hi, W_eq_cnt 7 (by omega) i hi,
    W_eq_cnt 6 (by omega) i hi, W_eq_cnt 5 (by omega) i hi, W_eq_cnt 3 (by omega) i hi,
    W_eq_cnt 1 (by omega) i hi] at h
  exact h

/-- the recurrence holds from every reachable relation state, for all lengths `m + 10` -/
theorem rec_all (m : Nat) : ∀ i, i < nS →
    cntFrom (m + 10) (Sget i) = cntFrom (m + 8) (Sget i) + cntFrom (m + 7) (Sget i) +
      cntFrom (m + 6) (Sget i) + cntFrom (m + 5) (Sget i) + cntFrom (m + 3) (Sget i) +
      2 * cntFrom (m + 1) (Sget i) := by
  induction m with
  | zero => intro i hi; exact base_cnt i hi
  | succ m ih =>
    intro i hi
    obtain ⟨h1, h2⟩ := tab_step false i hi
    obtain ⟨h3, h4⟩ := tab_step true i hi
    have i0 := ih _ h1
    have i1 := ih _ h3
    rw [h2] at i0
    rw [h4] at i1
    have s : ∀ e, cntFrom (m + 1 + e) (Sget i) = cntFrom (m + e) (delta false (Sget i)) + cntFrom (m + e) (delta true (Sget i)) := by
      intro e
      have : m + 1 + e = (m + e) + 1 := by omega
      rw [this]; exact cntFrom_succ _ _
    rw [s 10, s 8, s 7, s 6, s 5, s 3]
    have s1 : cntFrom (m + 1 + 1) (Sget i) = cntFrom (m + 1) (delta false (Sget i)) + cntFrom (m + 1) (delta true (Sget i)) := cntFrom_succ _ _
    rw [s1]
    omega

theorem recurrence (m : Nat) :
    a (m + 10) = a (m + 8) + a (m + 7) + a (m + 6) + a (m + 5) + a (m + 3) + 2 * a (m + 1) := by
  have h0 : 0 < nS := by decide
  have := rec_all m 0 h0
  rw [S_zero] at this
  exact this

theorem initial_values : [a 0, a 1, a 2, a 3, a 4, a 5, a 6, a 7, a 8, a 9] = [1, 0, 2, 3, 6, 10, 11, 28, 30, 75] := by
  have h0 : 0 < nS := by decide
  have e : ∀ k, k ≤ 10 → a k = W k 0 := by
    intro k hk
    rw [W_eq_cnt k hk 0 h0, S_zero]; rfl
  rw [e 0 (by omega), e 1 (by omega), e 2 (by omega), e 3 (by omega), e 4 (by omega), e 5 (by omega),
    e 6 (by omega), e 7 (by omega), e 8 (by omega), e 9 (by omega)]
  decide +kernel

/-- the final statement, in the indexing of the result note (`n ≥ 10`) -/
theorem recurrence_n (n : Nat) (hn : 10 ≤ n) :
    a n = a (n - 2) + a (n - 3) + a (n - 4) + a (n - 5) + a (n - 7) + 2 * a (n - 9) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 10 := ⟨n - 10, by omega⟩
  have := recurrence m
  have e1 : m + 10 - 2 = m + 8 := by omega
  have e2 : m + 10 - 3 = m + 7 := by omega
  have e3 : m + 10 - 4 = m + 6 := by omega
  have e4 : m + 10 - 5 = m + 5 := by omega
  have e5 : m + 10 - 7 = m + 3 := by omega
  have e6 : m + 10 - 9 = m + 1 := by omega
  rw [e1, e2, e3, e4, e5, e6]; exact this

end F1
