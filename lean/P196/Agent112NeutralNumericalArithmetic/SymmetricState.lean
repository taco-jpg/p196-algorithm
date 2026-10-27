import P196.Agent112NeutralNumericalArithmetic.BidirectionalValues
import P196.Agent112NeutralNumericalArithmetic.Normalization

/-!
# Recovery of bounded centers from numerical data

Symmetric injectivity follows from the shared all-base bidirectional-value
theorem. The zero-state characterization needs only coefficient bounds,
without symmetry, 和 follows by successive least-position residues.
The fixed-width decimal symmetric result is prior work in
`ReverseAddInverse.symmetric_value_injective`; the decimal exterior
injectivity 和 numerical decoders are prior work of Agents 115 和 5.
Agent 112's PR349 already states the symmetric integer-state observation
as a paper proof. This file connects it to the actual A120 `val` 和 the
existing `signedValue`, including width zero.

No decoder, sharp coefficient bound, padding theorem, cycle realization,
or Lychrel conclusion is asserted.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

/-- At fixed width, bounded symmetric coefficient words are determined by
their signed numerical value. Symmetry makes the reverse-value equality
follow from the forward-value equality. -/
theorem symmetric_eq_of_signedValue (b : Nat) (hb : 2 ≤ b) (A B : List Nat)
    (hlen : A.length = B.length)
    (ha : ∀ d ∈ A, d ≤ 2 * (b - 1)) (hboundB : ∀ d ∈ B, d ≤ 2 * (b - 1))
    (hsA : A.reverse = A) (hsB : B.reverse = B)
    (hsigned : signedValue b A = signedValue b B) : A = B := by
  have hval : val b A = val b B := by
    unfold signedValue at hsigned
    rw [hlen] at hsigned
    omega
  apply eq_of_bidirectional_values b hb A B hlen ha hboundB hval
  simpa only [hsA, hsB] using hval

private theorem val_replicate_neutral_add_one (b : Nat) (hb : 0 < b) (m : Nat) :
    val b (List.replicate m (b - 1)) + 1 = b ^ m := by
  induction m with
  | zero => simp
  | succ m ih =>
      simp only [List.replicate_succ, val_cons, Nat.pow_succ]
      have hm := congrArg (fun n : Nat => b * n) ih
      simp only [Nat.mul_add, Nat.mul_one] at hm
      rw [Nat.mul_comm (b ^ m) b]
      omega

private theorem signedValue_replicate_neutral (b : Nat) (hb : 0 < b) (m : Nat) :
    signedValue b (List.replicate m (b - 1)) = 0 := by
  have hval := val_replicate_neutral_add_one b hb m
  simp only [signedValue, List.length_replicate]
  omega

private theorem eq_neutral_of_succ_mod_zero (b : Nat) (hb : 2 ≤ b) (d : Nat)
    (hd : d ≤ 2 * (b - 1)) (hmod : (d + 1) % b = 0) : d = b - 1 := by
  by_cases hsmall : d + 1 < b
  · rw [Nat.mod_eq_of_lt hsmall] at hmod
    omega
  · have hsub : d + 1 - b < b := by omega
    rw [Nat.mod_eq_sub_mod (by omega), Nat.mod_eq_of_lt hsub] at hmod
    omega

private theorem eq_replicate_neutral_of_value (b : Nat) (hb : 2 ≤ b) :
    ∀ (C : List Nat), (∀ d ∈ C, d ≤ 2 * (b - 1)) →
      val b C + 1 = b ^ C.length → C = List.replicate C.length (b - 1)
  | [], _, _ => rfl
  | d :: C, hC, hval => by
      have htail : ∀ x ∈ C, x ≤ 2 * (b - 1) :=
        fun x hx => hC x (List.mem_cons_of_mem d hx)
      have hv : (d + 1) + b * val b C = b * b ^ C.length := by
        simpa only [val_cons, List.length_cons, Nat.pow_succ,
          Nat.mul_comm, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hval
      have hmod : (d + 1) % b = 0 := by
        have hm := congrArg (fun n : Nat => n % b) hv
        simpa only [Nat.add_mul_mod_self_left, Nat.mul_mod_right] using hm
      have hd := eq_neutral_of_succ_mod_zero b hb d (hC d List.mem_cons_self) hmod
      have htailval : val b C + 1 = b ^ C.length := by
        have hmul : b * (val b C + 1) = b * b ^ C.length := by
          simp only [Nat.mul_add, Nat.mul_one]
          omega
        exact Nat.eq_of_mul_eq_mul_left (by omega : 0 < b) hmul
      simpa only [List.length_cons, List.replicate_succ, hd] using
        congrArg (fun W : List Nat => (b - 1) :: W)
          (eq_replicate_neutral_of_value b hb C htail htailval)

/-- Every bounded zero state is its neutral word, without any symmetry
assumption. This includes the empty word at width zero. -/
theorem signedValue_eq_zero_iff (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hC : ∀ d ∈ C, d ≤ 2 * (b - 1)) :
    signedValue b C = 0 ↔ C = List.replicate C.length (b - 1) := by
  have hz := signedValue_replicate_neutral b (by omega) C.length
  constructor
  · intro hzero
    apply eq_replicate_neutral_of_value b hb C hC
    unfold signedValue at hzero
    omega
  · intro hword
    exact (congrArg (signedValue b) hword).trans hz

end Agent112.NeutralNumericalArithmetic
