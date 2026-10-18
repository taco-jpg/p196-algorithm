import P196.Foundations.LychrelDigitSums

/-! Constructive decimal realization for exact-length palindrome residues. -/
namespace ExactLengthResidues
open DecimalDigits Lychrel196

/-- Ordinary low-to-high decimal digits, with arbitrarily many zero padding digits. -/
def paddedDigits : Nat → Nat → Nat
  | n, 0 => n % 10
  | n, i + 1 => paddedDigits (n / 10) i

theorem paddedDigits_bound (n i : Nat) : paddedDigits n i ≤ 9 := by
  induction i generalizing n with
  | zero => simp [paddedDigits]; omega
  | succ i ih => exact ih (n / 10)

theorem paddedDigits_value (n k : Nat) (hn : n < 10 ^ k) :
    value (paddedDigits n) k = n := by
  induction k generalizing n with
  | zero =>
    simp only [Nat.pow_zero] at hn
    have hz : n = 0 := by omega
    subst n
    rfl
  | succ k ih =>
    rw [value_shift]
    have hquot : n / 10 < 10 ^ k := by
      apply (Nat.div_lt_iff_lt_mul (by decide : 0 < 10)).mpr
      simpa only [Nat.pow_succ] using hn
    change n % 10 + 10 * value (paddedDigits (n / 10)) k = n
    rw [ih (n / 10) hquot]
    exact Nat.mod_add_div n 10

/-- One low-index position and its reflected partner carry a digit 1. -/
def spike (j i : Nat) : Nat := if i = j then 1 else 0

def selectedDigit (ps : List Nat) (i : Nat) : Nat := if i ∈ ps then 1 else 0

def pairDigits (L : Nat) (ps : List Nat) (i : Nat) : Nat :=
  selectedDigit ps i + selectedDigit ps (L - 1 - i)

def pairValue (L i : Nat) : Nat := 10 ^ i + 10 ^ (L - 1 - i)

def pairTotal (L : Nat) : List Nat → Nat
  | [] => 0
  | i :: ps => pairValue L i + pairTotal L ps

def LowerPositions (k L : Nat) (ps : List Nat) : Prop :=
  ∀ i, i ∈ ps → k ≤ i ∧ i < L - 1 - i

theorem value_zero (L : Nat) : value (fun _ => 0) L = 0 := by
  induction L with
  | zero => rfl
  | succ L ih => simp [value, ih]

theorem value_spike (j L : Nat) : value (spike j) L = if j < L then 10 ^ j else 0 := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    rw [value, ih]
    by_cases hj : j < L
    · simp [spike, hj, show L ≠ j by omega, show j < L + 1 by omega]
    · by_cases he : j = L
      · subst j; simp [spike]
      · simp [spike, hj, show L ≠ j by omega, show ¬ j < L + 1 by omega]

theorem value_reflected_spike (j L : Nat) (hj : j < L) :
    value (fun i => spike j (L - 1 - i)) L = 10 ^ (L - 1 - j) := by
  have he : value (fun i => spike j (L - 1 - i)) L = value (spike (L - 1 - j)) L := by
    apply value_congr
    intro i hi
    simp only [spike, show (L - 1 - i = j) ↔ (i = L - 1 - j) by omega]
  rw [he, value_spike]
  simp [show L - 1 - j < L by omega]

theorem selectedDigit_cons (j : Nat) (ps : List Nat) (hj : j ∉ ps) (i : Nat) :
    selectedDigit (j :: ps) i = spike j i + selectedDigit ps i := by
  by_cases he : i = j
  · subst i; simp [selectedDigit, spike, hj]
  · simp [selectedDigit, spike, List.mem_cons, he]

theorem pairDigits_cons (L j : Nat) (ps : List Nat) (hj : j ∉ ps) (i : Nat) :
    pairDigits L (j :: ps) i =
      (spike j i + spike j (L - 1 - i)) + pairDigits L ps i := by
  simp only [pairDigits, selectedDigit_cons j ps hj]
  omega

theorem pairDigits_value (k L : Nat) (ps : List Nat) (hn : ps.Nodup)
    (hp : LowerPositions k L ps) : value (pairDigits L ps) L = pairTotal L ps := by
  induction ps with
  | nil =>
    have hz : value (pairDigits L []) L = value (fun _ => 0) L := by
      apply value_congr; intro i _; simp [pairDigits, selectedDigit]
    rw [hz, value_zero]
    rfl
  | cons j ps ih =>
    have hnd := List.nodup_cons.mp hn
    have hpos := hp j (by simp)
    have htail : LowerPositions k L ps := by
      intro i hi; exact hp i (by simp [hi])
    have he : value (pairDigits L (j :: ps)) L =
        value (fun i => (spike j i + spike j (L - 1 - i)) + pairDigits L ps i) L := by
      apply value_congr; intro i _; exact pairDigits_cons L j ps hnd.1 i
    rw [he, value_add, value_add, value_spike, value_reflected_spike _ _ (by omega),
      ih hnd.2 htail]
    simp [pairTotal, pairValue, show j < L by omega]

theorem pairDigits_bound (k L : Nat) (ps : List Nat)
    (hp : LowerPositions k L ps) (i : Nat) (hi : i < L) : pairDigits L ps i ≤ 1 := by
  have hinv : L - 1 - (L - 1 - i) = i := by omega
  by_cases ha : i ∈ ps
  · have hai := (hp i ha).2
    have hb : L - 1 - i ∉ ps := by
      intro hb; have hbi := (hp (L - 1 - i) hb).2; rw [hinv] at hbi; omega
    simp [pairDigits, selectedDigit, ha, hb]
  · simp only [pairDigits, selectedDigit, if_neg ha, Nat.zero_add]
    split <;> omega

theorem pairDigits_symmetric (L : Nat) (ps : List Nat) (i : Nat) (hi : i < L) :
    pairDigits L ps i = pairDigits L ps (L - 1 - i) := by
  simp only [pairDigits, show L - 1 - (L - 1 - i) = i by omega]
  omega

theorem pairDigits_zero_outer (k L : Nat) (ps : List Nat)
    (hp : LowerPositions k L ps) (i : Nat) (hi : i < L)
    (ho : i < k ∨ L - 1 - i < k) : pairDigits L ps i = 0 := by
  have ha : i ∉ ps := by
    intro ha; have h := hp i ha; omega
  have hb : L - 1 - i ∉ ps := by
    intro hb; have h := hp (L - 1 - i) hb
    have hinv : L - 1 - (L - 1 - i) = i := by omega
    rw [hinv] at h; omega
  simp [pairDigits, selectedDigit, ha, hb]

/-- Fixed low k-block, its high reflected block, and zero interior. -/
def outerDigits (d : Nat → Nat) (k L i : Nat) : Nat :=
  if i < k then d i else if L - 1 - i < k then d (L - 1 - i) else 0

def realizedDigits (d : Nat → Nat) (k L : Nat) (ps : List Nat) (i : Nat) : Nat :=
  outerDigits d k L i + pairDigits L ps i

theorem outerDigits_symmetric (d : Nat → Nat) (k L i : Nat)
    (hL : 2 * k ≤ L) (hi : i < L) :
    outerDigits d k L i = outerDigits d k L (L - 1 - i) := by
  have hinv : L - 1 - (L - 1 - i) = i := by omega
  simp only [outerDigits, hinv]
  by_cases ha : i < k
  · have hb : ¬ L - 1 - i < k := by omega
    simp [ha, hb]
  · by_cases hb : L - 1 - i < k <;> simp [ha, hb]

theorem realizedDigits_canonical (d : Nat → Nat) (k L : Nat) (ps : List Nat)
    (hk : 0 < k) (hL : 2 * k ≤ L) (hd : ∀ i, i < k → d i ≤ 9)
    (hd0 : 0 < d 0) (hp : LowerPositions k L ps) :
    Canonical (value (realizedDigits d k L ps) L) (realizedDigits d k L ps) L := by
  refine ⟨by omega, ?_, ?_, rfl⟩
  · intro i hi
    by_cases ha : i < k
    · have hz := pairDigits_zero_outer k L ps hp i hi (Or.inl ha)
      simpa [realizedDigits, outerDigits, ha, hz] using hd i ha
    · by_cases hb : L - 1 - i < k
      · have hz := pairDigits_zero_outer k L ps hp i hi (Or.inr hb)
        simpa [realizedDigits, outerDigits, ha, hb, hz] using hd (L - 1 - i) hb
      · have hpair := pairDigits_bound k L ps hp i hi
        simpa [realizedDigits, outerDigits, ha, hb] using (show pairDigits L ps i ≤ 9 by omega)
  · have ha : ¬ L - 1 < k := by omega
    have hb : L - 1 - (L - 1) = 0 := by omega
    have hz := pairDigits_zero_outer k L ps hp (L - 1) (by omega) (Or.inr (by omega))
    simpa [realizedDigits, outerDigits, ha, hb, hk, hz] using hd0

theorem realizedDigits_palindrome (d : Nat → Nat) (k L : Nat) (ps : List Nat)
    (hk : 0 < k) (hL : 2 * k ≤ L) (hd : ∀ i, i < k → d i ≤ 9)
    (hd0 : 0 < d 0) (hp : LowerPositions k L ps) :
    Palindrome (value (realizedDigits d k L ps) L) := by
  have hc := realizedDigits_canonical d k L ps hk hL hd hd0 hp
  apply (palindrome_value_iff _ _ hc.2.1 (Or.inr hc.2.2.1)).mpr
  intro i hi
  simp only [realizedDigits, outerDigits_symmetric d k L i hL hi,
    pairDigits_symmetric L ps i hi]

theorem realizedDigits_value (d : Nat → Nat) (k L : Nat) (ps : List Nat)
    (hn : ps.Nodup) (hp : LowerPositions k L ps) :
    value (realizedDigits d k L ps) L = value (outerDigits d k L) L + pairTotal L ps := by
  unfold realizedDigits
  rw [value_add, pairDigits_value k L ps hn hp]

/-- Altering only positions at or above k preserves every divisor of 10^k. -/
theorem value_mod_eq_of_low_eq (d e : Nat → Nat) (k L u : Nat)
    (hu : u ∣ 10 ^ k) (he : ∀ i, i < k → d i = e i) :
    value d L % u = value e L % u := by
  induction L with
  | zero => rfl
  | succ L ih =>
    change (value d L + d L * 10 ^ L) % u = (value e L + e L * 10 ^ L) % u
    rw [Nat.add_mod (value d L) (d L * 10 ^ L),
      Nat.add_mod (value e L) (e L * 10 ^ L)]
    rw [ih]
    by_cases hL : L < k
    · rw [he L hL]
    · have hdvd : u ∣ 10 ^ L := Nat.dvd_trans hu (Nat.pow_dvd_pow 10 (by omega))
      have hz := Nat.mod_eq_zero_of_dvd hdvd
      rw [Nat.mul_mod (d L), Nat.mul_mod (e L), hz]
      simp

/-- Extending a digit block by zero digits does not change its value. -/
def truncateDigits (d : Nat → Nat) (k i : Nat) : Nat := if i < k then d i else 0

theorem truncateDigits_value (d : Nat → Nat) (k L : Nat) (hL : k ≤ L) :
    value (truncateDigits d k) L = value d k := by
  induction L with
  | zero =>
    have hz : k = 0 := by omega
    subst k
    rfl
  | succ L ih =>
    by_cases hk : k ≤ L
    · rw [value, ih hk]; simp [truncateDigits, show ¬ L < k by omega]
    · have he : k = L + 1 := by omega
      subst k
      apply value_congr
      intro i hi; simp [truncateDigits, hi]

theorem realizedDigits_mod_outer (d : Nat → Nat) (k L u : Nat) (ps : List Nat)
    (hL : k ≤ L) (hu : u ∣ 10 ^ k) (hp : LowerPositions k L ps) :
    value (realizedDigits d k L ps) L % u = value d k % u := by
  have he : ∀ i, i < k → realizedDigits d k L ps i = truncateDigits d k i := by
    intro i hi
    have hz := pairDigits_zero_outer k L ps hp i (by omega) (Or.inl hi)
    simp [realizedDigits, outerDigits, truncateDigits, hi, hz]
  rw [value_mod_eq_of_low_eq _ _ k L u hu he, truncateDigits_value d k L hL]

theorem pairTotal_append (L : Nat) (ps ts : List Nat) :
    pairTotal L (ps ++ ts) = pairTotal L ps + pairTotal L ts := by
  induction ps with
  | nil => simp [pairTotal]
  | cons i ps ih => simp [pairTotal, ih, Nat.add_assoc]

theorem add_mod_congr (a b c d q : Nat) (ha : a % q = c % q)
    (hb : b % q = d % q) : (a + b) % q = (c + d) % q := by
  calc
    (a + b) % q = (a % q + b % q) % q := Nat.add_mod a b q
    _ = (c % q + d % q) % q := by rw [ha, hb]
    _ = (c + d) % q := (Nat.add_mod c d q).symm

theorem pairTotal_mod (L q c : Nat) (ps : List Nat)
    (hc : ∀ i, i ∈ ps → pairValue L i % q = c % q) :
    pairTotal L ps % q = (ps.length * c) % q := by
  induction ps with
  | nil => simp [pairTotal]
  | cons i ps ih =>
    have hh := hc i (by simp)
    have ht := ih (fun j hj => hc j (by simp [hj]))
    change (pairValue L i + pairTotal L ps) % q = ((ps.length + 1) * c) % q
    rw [Nat.add_mul, Nat.one_mul, Nat.add_comm (ps.length * c) c]
    exact add_mod_congr _ _ _ _ q hh ht

/-- The starting palindrome containing only the prescribed outer block. -/
def outerValue (A k L : Nat) : Nat := value (outerDigits (paddedDigits A) k L) L

theorem outerValue_palindrome (A k L : Nat) (hk : 0 < k) (hL : 2 * k ≤ L)
    (hA0 : A % 10 ≠ 0) : Palindrome (outerValue A k L) := by
  have hzero : LowerPositions k L [] := by intro i hi; simp at hi
  have hpal := realizedDigits_palindrome (paddedDigits A) k L [] hk hL
    (fun i _ => paddedDigits_bound A i) (by simpa [paddedDigits] using Nat.pos_of_ne_zero hA0)
    hzero
  have he : value (realizedDigits (paddedDigits A) k L []) L = outerValue A k L := by
    apply value_congr
    intro i _
    simp [realizedDigits, pairDigits, selectedDigit]
  rwa [he] at hpal

theorem outerValue_dvd11 (A k L : Nat) (hL : 2 * k ≤ L) (he : L % 2 = 0) :
    11 ∣ outerValue A k L := by
  apply AstraModular.even_symmetric_value_dvd11 _ _ he
  intro i hi
  exact outerDigits_symmetric (paddedDigits A) k L i hL hi

/-- A concrete actual palindrome realizes any two disjoint pools of binary
mirror pairs. The target residues are expressed through the selected counts. -/
theorem two_pool_realization (A k L u q c0 c1 : Nat) (ps0 ps1 : List Nat)
    (hk : 0 < k) (hL : 2 * k ≤ L) (hA : A < 10 ^ k) (hA0 : A % 10 ≠ 0)
    (hu : u ∣ 10 ^ k) (hn : (ps0 ++ ps1).Nodup)
    (hp : LowerPositions k L (ps0 ++ ps1))
    (hc0 : ∀ i, i ∈ ps0 → pairValue L i % q = c0 % q)
    (hc1 : ∀ i, i ∈ ps1 → pairValue L i % q = c1 % q) :
    ∃ P d, Canonical P d L ∧ Palindrome P ∧ P % u = A % u ∧
      P % q = (outerValue A k L + ps0.length * c0 + ps1.length * c1) % q := by
  let ds := realizedDigits (paddedDigits A) k L (ps0 ++ ps1)
  have hd : ∀ i, i < k → paddedDigits A i ≤ 9 := fun i _ => paddedDigits_bound A i
  have hd0 : 0 < paddedDigits A 0 := by
    simpa [paddedDigits] using Nat.pos_of_ne_zero hA0
  refine ⟨value ds L, ds, realizedDigits_canonical _ k L _ hk hL hd hd0 hp,
    realizedDigits_palindrome _ k L _ hk hL hd hd0 hp, ?_, ?_⟩
  · rw [realizedDigits_mod_outer _ k L u _ (by omega) hu hp, paddedDigits_value A k hA]
  · dsimp [ds]
    rw [realizedDigits_value _ k L _ hn hp, pairTotal_append]
    have hsum := add_mod_congr _ _ _ _ q (pairTotal_mod L q c0 ps0 hc0)
      (pairTotal_mod L q c1 ps1 hc1)
    have hall := add_mod_congr (outerValue A k L) _ (outerValue A k L) _ q rfl hsum
    simpa [outerValue, Nat.add_assoc] using hall

end ExactLengthResidues
