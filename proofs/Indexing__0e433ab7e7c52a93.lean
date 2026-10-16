import Safety

namespace Agent13FoldedFamily
open DecimalDigits FoldedDecimal Lychrel196

/-- Equality of the actual finite words recovers each selected binary block. -/
theorem input_word_bits_injective (e f : Nat → Bool) (r k : Nat)
    (h : ∀ i, i < 2*halfWidth r k → inputWord e r k i = inputWord f r k i) :
    ∀ j, j < r → e j = f j := by
  intro j hj
  have hi : 4*j+1 < halfWidth r k := by unfold halfWidth; omega
  have he := h (4*j+1) (by omega)
  have ha : 4*j+1 < 4*r+1 := by omega
  simp only [inputWord, reflectHalf, hi, if_true, inputHalf,
    show 4*j+1 ≠ 0 by omega, if_false, ha, Nat.add_sub_cancel,
    Nat.mul_div_right, Nat.mul_mod_right, blockDigit] at he
  cases h1 : e j <;> cases h2 : f j <;> simp_all

theorem input_word_congr (e f : Nat → Bool) (r k : Nat)
    (h : ∀ j, j < r → e j = f j) :
    ∀ i, i < 2*halfWidth r k → inputWord e r k i = inputWord f r k i := by
  have hp : ∀ j, inputHalf e r j = inputHalf f r j := by
    intro j
    unfold inputHalf
    split
    · rfl
    · split
      · rename_i hz hb
        rw [h ((j-1)/4) (by omega)]
      · rfl
  intro i _
  exact hp _

def bit : Nat → Nat → Bool
  | n, 0 => n%2 == 1
  | n, i+1 => bit (n/2) i

def encode (e : Nat → Bool) : Nat → Nat
  | 0 => 0
  | r+1 => (if e 0 then 1 else 0) + 2*encode (fun i => e (i+1)) r

theorem encode_bound (e : Nat → Bool) (r : Nat) : encode e r < 2^r := by
  induction r generalizing e with
  | zero => simp [encode]
  | succ r ih =>
    have h := ih (fun i => e (i+1))
    rw [encode, Nat.pow_succ]
    split <;> omega

theorem encode_bit (n r : Nat) (hn : n < 2^r) : encode (bit n) r = n := by
  induction r generalizing n with
  | zero => simp only [Nat.pow_zero] at hn; simp [encode,show n=0 by omega]
  | succ r ih =>
    have hs : n/2 < 2^r := by rw [Nat.pow_succ] at hn; omega
    simp only [encode, bit]
    rw [ih (n/2) hs]
    split <;> simp_all <;> omega

theorem bit_encode (e : Nat → Bool) (r i : Nat) (hi : i < r) : bit (encode e r) i = e i := by
  induction r generalizing e i with
  | zero => omega
  | succ r ih =>
    cases i with
    | zero =>
      simp only [encode,bit]
      cases he : e 0 <;> simp [he]
    | succ i =>
      simp only [encode,bit]
      have hdiv : ((if e 0 then 1 else 0)+2*encode (fun i => e (i+1)) r)/2 =
          encode (fun i => e (i+1)) r := by split <;> omega
      rw [hdiv]
      exact ih (fun j => e (j+1)) i (by omega)

theorem encode_congr (e f : Nat → Bool) (r : Nat)
    (h : ∀ i, i < r → e i = f i) : encode e r = encode f r := by
  induction r generalizing e f with
  | zero => rfl
  | succ r ih =>
    rw [encode, encode, h 0 (by omega), ih _ _ (fun i hi => h (i+1) (by omega))]

def indexedWord (r k : Nat) (j : Fin (2^r)) : Nat → Nat := inputWord (bit j.val) r k

/-- Exactly 2^r different finite pair words are indexed, with no duplicate bits. -/
theorem indexed_word_injective (r k : Nat) (i j : Fin (2^r))
    (h : ∀ t, t < 2*halfWidth r k → indexedWord r k i t = indexedWord r k j t) : i = j := by
  have he := input_word_bits_injective (bit i.val) (bit j.val) r k h
  have hv := encode_congr _ _ r he
  rw [encode_bit _ _ i.isLt, encode_bit _ _ j.isLt] at hv
  exact Fin.ext hv

/-- Conversely, every source binary word appears in that exact finite indexing. -/
theorem indexed_word_complete (e : Nat → Bool) (r k : Nat) :
    ∃ j : Fin (2^r), ∀ t, t < 2*halfWidth r k → indexedWord r k j t = inputWord e r k t := by
  refine ⟨⟨encode e r, encode_bound e r⟩, ?_⟩
  exact input_word_congr _ _ r k (fun i hi => bit_encode e r i hi)

/-- Exact all-parameter source theorem; cardinality is the constructed family,
not necessarily the complete incoming fiber. -/
theorem exact_binary_family (r k : Nat) (hk : 0 < k) :
    ∃ f : Fin (2^r) → (Nat → Nat),
      (∀ i j, (∀ t, t < 2*halfWidth r k → f i t = f j t) → i=j) ∧
      WordSafe (2*halfWidth r k) (targetWord r k) ∧
      ∀ j, WordSafe (2*halfWidth r k) (f j) ∧
        carry (f j) (2*halfWidth r k) = 0 ∧
        (∀ t, t < 2*halfWidth r k → nextColumns (f j) (2*halfWidth r k) t = targetWord r k t) ∧
        ∃ n d d', 0 < n ∧ Canonical n d (2*halfWidth r k) ∧
          (∀ t, t < 2*halfWidth r k → columnSum d (2*halfWidth r k) t = f j t) ∧
          Canonical (step n) d' (2*halfWidth r k) ∧
          (∀ t, t < 2*halfWidth r k → columnSum d' (2*halfWidth r k) t = targetWord r k t) ∧
          ¬ Palindrome n ∧ ¬ Palindrome (step n) ∧ ¬ Palindrome (step (step n)) := by
  refine ⟨indexedWord r k, indexed_word_injective r k, (binary_family_safe (fun _ => false) r k hk).2, ?_⟩
  intro j
  exact ⟨(binary_family_safe (bit j.val) r k hk).1,
    binary_family_no_overflow (bit j.val) r k hk,
    (binary_family_transition (bit j.val) r k hk).2,
    binary_family_safe_realization (bit j.val) r k hk⟩

end Agent13FoldedFamily
