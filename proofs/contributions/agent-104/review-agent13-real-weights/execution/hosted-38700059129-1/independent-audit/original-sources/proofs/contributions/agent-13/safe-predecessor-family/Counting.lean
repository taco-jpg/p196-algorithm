import TargetSafety

namespace Agent13SafeFamily
open DecimalDigits Lychrel196

/-- Fixed-width natural digits, preserving zero positions. -/
def natDigit : Nat → Nat → Nat
  | n, 0 => n % 10
  | n, i+1 => natDigit (n/10) i

theorem natDigit_bounded (n i : Nat) : natDigit n i ≤ 9 := by
  induction i generalizing n with
  | zero => simp only [natDigit]; omega
  | succ i ih => exact ih (n/10)

theorem natDigit_eq_div (n i : Nat) : natDigit n i = n / 10^i % 10 := by
  induction i generalizing n with
  | zero => simp [natDigit]
  | succ i ih =>
    simp only [natDigit, ih, Nat.div_div_eq_div_mul, Nat.pow_succ]
    rw [Nat.mul_comm 10]

theorem natDigit_value (n L : Nat) (hn : n < 10^L) : value (natDigit n) L = n := by
  induction L generalizing n with
  | zero =>
    simp only [Nat.pow_zero] at hn
    have hz : n=0 := by omega
    simp [value,hz]
  | succ L ih =>
    have hsmall : n/10 < 10^L := by
      rw [Nat.pow_succ] at hn
      omega
    rw [value_shift]
    change n%10 + 10*value (natDigit (n/10)) L = n
    rw [ih _ hsmall]
    exact Nat.mod_add_div n 10

theorem indexed_high_bounds (r j : Nat) (hj : j < 9*10^r) :
    10^r ≤ 10^r+j ∧ 10^r+j < 10^(r+1) := by
  rw [Nat.pow_succ]
  omega

theorem indexed_high_leading (r j : Nat) (hj : j < 9*10^r) :
    0 < natDigit (10^r+j) ((r+1)-1) := by
  simp only [Nat.add_sub_cancel, natDigit_eq_div]
  have hpow : 0 < 10^r := Nat.pow_pos (by decide)
  have hp : 0 < (10^r+j)/10^r := Nat.div_pos (by omega) hpow
  have hs : (10^r+j)/10^r < 10 := by
    apply (Nat.div_lt_iff_lt_mul hpow).mpr
    omega
  rw [Nat.mod_eq_of_lt hs]
  exact hp

/-- A finite indexing of every canonical high word, with no leading zero. -/
def predecessor (r : Nat) (j : Fin (9*10^r)) : Nat :=
  family (natDigit (10^r+j.val)) (r+1)

theorem predecessor_spec (r : Nat) (j : Fin (9*10^r)) :
    Safe (predecessor r j) ∧ Safe (target (r+1)) ∧
    step (predecessor r j) = target (r+1) ∧
    predecessor r j < 10^(2*(r+1)+2) ∧ 10^(2*(r+1)+2) < target (r+1) := by
  exact family_safe_predecessor _ _ (by omega)
    (fun i _ => natDigit_bounded _ i) (indexed_high_leading r j.val j.isLt)

theorem predecessor_injective (r : Nat) (i j : Fin (9*10^r))
    (h : predecessor r i = predecessor r j) : i = j := by
  have hd := family_injective _ _ (r+1)
    (fun t _ => natDigit_bounded (10^r+i.val) t)
    (fun t _ => natDigit_bounded (10^r+j.val) t) h
  have hv := value_congr _ _ (r+1) hd
  rw [natDigit_value _ _ (indexed_high_bounds r i.val i.isLt).2,
    natDigit_value _ _ (indexed_high_bounds r j.val j.isLt).2] at hv
  apply Fin.ext
  omega

/-- Only the used high-word positions affect the full constructed number. -/
theorem family_congr (a b : Nat → Nat) (k : Nat)
    (h : ∀ i, i < k → a i = b i) : family a k = family b k := by
  apply value_congr
  intro i hi
  unfold familyDigit
  split
  · rw [h _ (by omega)]
  · split
    · rfl
    · rw [h _ (by omega)]

/-- Completeness: every canonical high word occurs in the finite indexing. -/
theorem predecessor_complete (r : Nat) (a : Nat → Nat)
    (ha : ∀ i, i < r+1 → a i ≤ 9) (hlead : 0 < a r) :
    ∃ j : Fin (9*10^r), predecessor r j = family a (r+1) := by
  let A := value a (r+1)
  have hb : 10^r ≤ A := by
    have hmul := Nat.mul_le_mul_right (10^r) (show 1 ≤ a r by omega)
    simp only [Nat.one_mul] at hmul
    dsimp [A]
    rw [value]
    omega
  have ht : A < 10^(r+1) := value_lt_pow a (r+1) ha
  have hj : A-10^r < 9*10^r := by
    rw [Nat.pow_succ] at ht
    omega
  let j : Fin (9*10^r) := ⟨A-10^r, hj⟩
  refine ⟨j, ?_⟩
  have hjA : 10^r+j.val = A := by dsimp [j]; omega
  have hv : value (natDigit (10^r+j.val)) (r+1) = value a (r+1) := by
    rw [hjA, natDigit_value A (r+1) ht]
  exact family_congr _ _ _ (value_injective _ _ _ (fun i _ => natDigit_bounded _ i) ha hv)

/-- Original parameterization and exact advertised number of distinct safe
predecessors. The size counts this family, not necessarily the whole fiber. -/
theorem safe_predecessor_family (m : Nat) (hm : 2 ≤ m) :
    ∃ f : Fin (9*10^(m-2)) → Nat,
      (∀ i j, f i = f j → i = j) ∧
      Safe (10^(2*m) + 99*10^(m-1) - 1) ∧
      ∀ i, Safe (f i) ∧ step (f i) = 10^(2*m) + 99*10^(m-1) - 1 ∧
        f i < 10^(2*m) ∧ 10^(2*m) < 10^(2*m) + 99*10^(m-1) - 1 := by
  have hw : 2*((m-2)+1)+2 = 2*m := by omega
  have he : (m-2)+1 = m-1 := by omega
  have ht : target ((m-2)+1) = 10^(2*m)+99*10^(m-1)-1 := by
    unfold target
    rw [hw, he]
  refine ⟨predecessor (m-2), predecessor_injective (m-2), ?_, ?_⟩
  · rw [← ht]
    exact target_safe _ (by omega)
  · intro i
    have hs := predecessor_spec (m-2) i
    rw [ht, hw] at hs
    exact ⟨hs.1, hs.2.2⟩

theorem index_capacity (r : Nat) : r < 9*10^r := by
  induction r with
  | zero => decide
  | succ r ih =>
    rw [Nat.pow_succ]
    omega

/-- No uniform finite bound on the number of safe predecessors of safe states. -/
theorem safe_fibers_unbounded (N : Nat) :
    ∃ y, Safe y ∧ ∃ f : Fin N → Nat,
      (∀ i j, f i = f j → i = j) ∧ ∀ i, Safe (f i) ∧ step (f i) = y ∧ f i < y := by
  let embed : Fin N → Fin (9*10^N) := fun i => ⟨i.val, Nat.lt_trans i.isLt (index_capacity N)⟩
  refine ⟨target (N+1), target_safe _ (by omega), (fun i => predecessor N (embed i)), ?_, ?_⟩
  · intro i j hij
    have h := predecessor_injective N (embed i) (embed j) hij
    apply Fin.ext
    have hv : (embed i).val = (embed j).val :=
      congrArg (fun x : Fin (9*10^N) => x.val) h
    exact hv
  · intro i
    have h := predecessor_spec N (embed i)
    exact ⟨h.1, h.2.2.1, Nat.lt_trans h.2.2.2.1 h.2.2.2.2⟩

end Agent13SafeFamily
