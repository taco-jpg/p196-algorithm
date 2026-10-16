import FiniteWords

namespace Agent13ProductWeights
open DecimalDigits FoldedDecimal Agent13FoldedFamily

def extendBits {r : Nat} (e : Fin r → Bool) (i : Nat) : Bool := if hi : i < r then e ⟨i,hi⟩ else false

def familyState (r k : Nat) (e : Fin r → Bool) : FiniteWord :=
  encodeWord (inputWord (extendBits e) r k) (2*halfWidth r k)
    (input_admissible (extendBits e) r k).2.2.1

def targetState (r k : Nat) : FiniteWord :=
  encodeWord (targetWord r k) (2*halfWidth r k) (target_admissible r k).2.2.1

theorem encoded_safe (q : Nat → Nat) (L : Nat) (hq : ∀ i, i < L → q i ≤ 18)
    (hs : WordSafe L q) : SafeState (encodeWord q L hq) := by
  have hd := digits_encodeWord q L hq
  refine ⟨⟨hs.1.1,?_,?_,?_,?_⟩, ?_⟩
  · change 0 < digits (encodeWord q L hq) 0
    rw [hd 0 hs.1.1]
    exact hs.1.2.1
  · exact fun i _ => digits_bounded _ i
  · intro i hi
    change digits (encodeWord q L hq) i = digits (encodeWord q L hq) (L-1-i)
    rw [hd i hi, hd (L-1-i) (by have := hs.1.1; omega)]
    exact hs.1.2.2.2.1 i hi
  · intro i hi heq
    change digits (encodeWord q L hq) i % 2 = 0
    rw [hd i hi]
    exact hs.1.2.2.2.2 i hi heq
  · change ¬ Lychrel196.Palindrome (value (digits (encodeWord q L hq)) L)
    rw [value_congr _ _ _ hd]
    exact hs.2

/-- Replacing a bounded coefficient function by its finite encoding preserves
an entire no-overflow edge, not merely selected coordinates. -/
theorem encoded_transition (q p : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hp : ∀ i, i < L → p i ≤ 18)
    (hc : carry q L=0) (ht : ∀ i, i < L → nextColumns q L i = p i) :
    MapsTo (encodeWord q L hq) (encodeWord p L hp) := by
  have he := digits_encodeWord q L hq
  have hcarry : carry (digits (encodeWord q L hq)) L = 0 := by
    rw [carry_congr_upto _ _ L he L (by omega),hc]
  refine ⟨?_,?_⟩
  · change nextWidth (digits (encodeWord q L hq)) L = L
    simp [nextWidth,hcarry]
  · intro i hi
    change nextColumns (digits (encodeWord q L hq)) L i = digits (encodeWord p L hp) i
    have hr : L-1-i < L := by change i < L at hi; omega
    rw [digits_encodeWord p L hp i hi, ← ht i hi]
    simp only [nextColumns,hcarry,hc,if_true,columnSum,reflected]
    rw [output_congr_upto _ _ L he i hi, output_congr_upto _ _ L he (L-1-i) hr]

theorem targetState_safe (r k : Nat) (hk : 0 < k) : SafeState (targetState r k) := by
  exact encoded_safe _ _ _ (binary_family_safe (fun _ => false) r k hk).2

theorem familyState_spec (r k : Nat) (e : Fin r → Bool) (hk : 0 < k) :
    SafeState (familyState r k e) ∧ MapsTo (familyState r k e) (targetState r k) := by
  refine ⟨encoded_safe _ _ _ (binary_family_safe (extendBits e) r k hk).1, ?_⟩
  exact encoded_transition _ _ _ _ _ (binary_family_no_overflow (extendBits e) r k hk)
    (binary_family_transition (extendBits e) r k hk).2

theorem familyState_injective (r k : Nat) : Function.Injective (familyState r k) := by
  intro e f hf
  have he : ∀ i, i < 2*halfWidth r k → inputWord (extendBits e) r k i = inputWord (extendBits f) r k i := by
    intro i hi
    have h := congrArg (fun s => digits s i) hf
    simpa only [familyState,digits_encodeWord _ _ _ i hi] using h
  have hb := input_word_bits_injective (extendBits e) (extendBits f) r k he
  funext i
  have h := hb i.val i.isLt
  simpa [extendBits,i.isLt] using h

/-- Canonical finite safe states are realizable by positive ordinary seeds. -/
theorem safe_state_realizable (s : FiniteWord) (hs : SafeState s) :
    ∃ n d, 0 < n ∧ Canonical n d s.1 ∧
      (∀ i, i < s.1 → columnSum d s.1 i = digits s i) ∧
      ¬ Lychrel196.Palindrome (Lychrel196.step n) := by
  have ha := hs.1
  obtain ⟨n,d,hn,hc,hr⟩ := valid_word_realizable _ _ ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  refine ⟨n,d,hn,hc,hr,?_⟩
  rw [step_eq_word_value _ _ _ _ hc hr]
  exact hs.2

end Agent13ProductWeights
