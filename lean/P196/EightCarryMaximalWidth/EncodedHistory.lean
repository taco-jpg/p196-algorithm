import P196.EightCarryMaximalWidth.PrefixHistory

/-!
Agent #10: compact normalization between finite prefix observations.
Every recursive transition encodes its entire successor in base nineteen
before the next observation decodes it. The new worker uses exactly the
accepted prefix transition and the complete signatures of PrefixHistory.
-/

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

namespace EightCarryMaximalWidth.PrefixHistory

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open SevenColumnProjection

/-- Fixed-length base-nineteen coding, with the exterior coefficient first. -/
def encode : List Nat → Nat
  | [] => 0
  | a :: s => a + 19 * encode s

/-- The length is retained separately, so zero terminal coefficients are kept. -/
def decode : Nat → Nat → List Nat
  | 0, _ => []
  | k + 1, n => n % 19 :: decode k (n / 19)

theorem decode_encode (s : List Nat) (hs : ∀ x, x ∈ s → x ≤ 18) :
    decode s.length (encode s) = s := by
  induction s with
  | nil => rfl
  | cons a s ih =>
      have ha : a < 19 := by have h := hs a (by simp); omega
      have ht : ∀ x, x ∈ s → x ≤ 18 := by
        intro x hx
        exact hs x (by simp [hx])
      simp only [List.length_cons, encode, decode, Nat.add_mul_mod_self_left,
        Nat.mod_eq_of_lt ha, Nat.add_mul_div_left _ _ (by decide : 0 < 19),
        Nat.div_eq_of_lt ha, Nat.zero_add, ih ht]

theorem valid_bounded (s : List Nat) (hs : valid s = true) :
    ∀ x, x ∈ s → x ≤ 18 := by
  cases s with
  | nil => simp [valid] at hs
  | cons a s =>
      have hh : (1 ≤ a ∧ a ≤ 18) ∧
          s.all (fun x => decide (x ≤ 18)) = true := by
        simpa only [valid, Bool.and_eq_true, decide_eq_true_eq] using hs
      intro x hx
      rcases List.mem_cons.mp hx with hx | hx
      · subst x
        exact hh.1.2
      · have ht := List.all_eq_true.mp hh.2 x hx
        exact of_decide_eq_true ht

theorem decode_encode_valid (s : List Nat) (hs : valid s = true) :
    decode s.length (encode s) = s :=
  decode_encode s (valid_bounded s hs)

theorem lowDigits_length (s : List Nat) (e : Nat) :
    (lowDigits s e).length = s.length := by
  induction s generalizing e with
  | nil => rfl
  | cons a s ih => simp only [lowDigits, List.length_cons, ih]

theorem highDigits_length (s : List Nat) (e : Nat) :
    (highDigits s e).2.length = s.length := by
  induction s with
  | nil => rfl
  | cons a s ih => simp only [highDigits, List.length_cons, ih]

theorem forwardPrefix_length (s : List Nat) (e : Nat) :
    (forwardPrefix s e).length = s.length := by
  unfold forwardPrefix
  dsimp only
  split
  · simp only [List.length_zipWith, lowDigits_length, highDigits_length, Nat.min_self]
  · simp only [List.length_zipWith, lowDigits_length, List.length_cons,
      highDigits_length, Nat.min_eq_left (Nat.le_succ s.length)]

/-- Every recursive state is a fully encoded natural number. -/
def survivesCode (k : Nat) : Nat → Nat → Nat → Bool
  | 0, _, _ => true
  | n + 1, a, b =>
      let s := decode k a
      let r := decode k b
      let branch := fun e =>
        let ns := forwardPrefix s e
        let nr := forwardPrefix r e
        compatible s r e && valid ns && valid nr &&
          survivesCode k n (encode ns) (encode nr)
      branch 0 || branch 1

def survivesEncoded (K : Nat) (s r : List Nat) : Bool :=
  survivesCode s.length K (encode s) (encode r)

theorem survivesCode_step_of (k n : Nat) (s r : List Nat) (e : Nat)
    (hsk : s.length = k) (hrk : r.length = k)
    (hsv : valid s = true) (hrv : valid r = true) (he : e ≤ 1)
    (hc : compatible s r e = true)
    (hs : valid (forwardPrefix s e) = true)
    (hr : valid (forwardPrefix r e) = true)
    (hn : survivesCode k n (encode (forwardPrefix s e))
      (encode (forwardPrefix r e)) = true) :
    survivesCode k (n + 1) (encode s) (encode r) = true := by
  have hdq : decode k (encode s) = s := by
    rw [← hsk]
    exact decode_encode_valid s hsv
  have hdr : decode k (encode r) = r := by
    rw [← hrk]
    exact decode_encode_valid r hrv
  have hb : e = 0 ∨ e = 1 := by omega
  rcases hb with hb | hb
  · subst e
    simp [survivesCode, hdq, hdr, hc, hs, hr, hn]
  · subst e
    simp [survivesCode, hdq, hdr, hc, hs, hr, hn]

/-- The compact worker accepts every valid equal-length history accepted by
the direct checker. No finite enumeration is trusted by this implication. -/
theorem survives_implies_encoded (K : Nat) (s r : List Nat)
    (hlen : s.length = r.length) (hsv : valid s = true) (hrv : valid r = true)
    (hsurvives : survives K s r = true) :
    survivesEncoded K s r = true := by
  induction K generalizing s r with
  | zero => rfl
  | succ K ih =>
      have hex : ∃ e : Nat, e ≤ 1 ∧ compatible s r e = true ∧
          valid (forwardPrefix s e) = true ∧ valid (forwardPrefix r e) = true ∧
          survives K (forwardPrefix s e) (forwardPrefix r e) = true := by
        simp only [survives, Bool.or_eq_true] at hsurvives
        rcases hsurvives with h | h
        · refine ⟨0, by decide, ?_⟩
          simpa only [Bool.and_eq_true, and_assoc] using h
        · refine ⟨1, by decide, ?_⟩
          simpa only [Bool.and_eq_true, and_assoc] using h
      rcases hex with ⟨e, he, hc, hs, hr, hn⟩
      have hlen' : (forwardPrefix s e).length = (forwardPrefix r e).length := by
        rw [forwardPrefix_length, forwardPrefix_length, hlen]
      have hrec := ih (forwardPrefix s e) (forwardPrefix r e) hlen' hs hr hn
      unfold survivesEncoded at hrec ⊢
      rw [forwardPrefix_length] at hrec
      exact survivesCode_step_of s.length K s r e rfl hlen.symm hsv hrv he hc hs hr hrec

/-- Actual complete equal carry histories survive the encoded checker, with
the same observation count and width hypotheses as the direct checker. -/
theorem actual_history_survives_encoded (q r : Nat → Nat) (L k K : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (hk0 : 0 < k) (hk : k ≤ L)
    (hc : ∀ t, t < K → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i) :
    survivesEncoded K (wordPrefix q k) (wordPrefix r k) = true := by
  apply survives_implies_encoded K (wordPrefix q k) (wordPrefix r k)
  · simp only [prefix_length]
  · exact valid_prefix q L k hq hk0 hk
  · exact valid_prefix r L k hr hk0 hk
  · exact actual_history_survives q r L k K hq hr hk0 hk hc

#print axioms decode_encode
#print axioms survives_implies_encoded
#print axioms actual_history_survives_encoded

end EightCarryMaximalWidth.PrefixHistory
