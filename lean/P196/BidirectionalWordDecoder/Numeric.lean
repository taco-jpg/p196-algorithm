import P196.Agent6CoordinateDynamics.ExteriorObservationInjective

/-!
# Constructive reconstruction from both positional values

For a word of known length, its little-endian value determines the units
residue of the first coefficient. Its big-endian value places that
coefficient in an interval of ten consecutive integers whenever the tail
value is below ten times its positional scale. These two observations
recover the coefficient, and subtraction exposes the two tail values.

The resulting recursive decoder is correct for all words with coefficients
at most 90. A parameterized positional bound supplies the tail estimate.
The decoder is total on arbitrary natural inputs and takes one recursive
step per requested coefficient.
-/

namespace Agent5.BidirectionalWordDecoder

open Agent115.ExteriorFactorization

/-- A uniform positional estimate for coefficients bounded by nine times
an arbitrary natural parameter. -/
theorem highValue_bound (k : Nat) (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 9 * k) :
    highValue B + k ≤ k * 10 ^ B.length := by
  induction B with
  | nil => simp [highValue]
  | cons x xs ih =>
      have hx := hB x List.mem_cons_self
      have ht := ih (fun y hy => hB y (List.mem_cons_of_mem x hy))
      have hm : x * 10 ^ xs.length ≤ 9 * (k * 10 ^ xs.length) := by
        simpa only [Nat.mul_assoc] using Nat.mul_le_mul_right (10 ^ xs.length) hx
      rw [highValue_cons, List.length_cons, Nat.pow_succ]
      have hp : k * (10 ^ xs.length * 10) = 10 * (k * 10 ^ xs.length) := by
        ac_rfl
      rw [hp]
      omega

/-- Reconstruct a word from its width and two positional values by
recovering one coefficient and then its two tail values at each step. -/
def decodeValues : Nat → Nat → Nat → List Nat
  | 0, _, _ => []
  | n + 1, V, H =>
      let P := 10 ^ n
      let r := V % 10
      let q := H / P
      let x := r + 10 * ((q - r) / 10)
      x :: decodeValues n ((V - x) / 10) (H - x * P)

/-- Every input produces exactly the requested number of coefficients. -/
theorem decodeValues_length (n V H : Nat) :
    (decodeValues n V H).length = n := by
  induction n generalizing V H with
  | zero => rfl
  | succ n ih => simp only [decodeValues, List.length_cons, ih]

private theorem recover_head (x V H P : Nat)
    (hP : 0 < P) (hH : H < 10 * P) :
    let r := (x + 10 * V) % 10
    let q := (x * P + H) / P
    r + 10 * ((q - r) / 10) = x := by
  dsimp only
  have hmod : (x + 10 * V) % 10 = x % 10 := by omega
  rw [hmod]
  have hdiv : (x * P + H) / P = x + H / P := by
    rw [Nat.mul_comm x P, Nat.mul_add_div hP]
  rw [hdiv]
  have hsmall : H / P < 10 := (Nat.div_lt_iff_lt_mul hP).mpr hH
  have hdecomp := Nat.mod_add_div x 10
  have hsub : x + H / P - x % 10 = 10 * (x / 10) + H / P := by
    calc
      _ = (x % 10 + 10 * (x / 10)) + H / P - x % 10 :=
        congrArg (fun z => z + H / P - x % 10) hdecomp.symm
      _ = _ := by rw [Nat.add_assoc, Nat.add_sub_cancel_left]
  rw [hsub, Nat.mul_add_div (by decide : 0 < 10),
    Nat.div_eq_of_lt hsmall, Nat.add_zero]
  exact hdecomp

/-- The explicit decoder recovers every word whose coefficients are at
most 90 from its length and original little- and big-endian values. -/
theorem decodeValues_correct (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 90) :
    decodeValues B.length (lowValue B) (highValue B) = B := by
  induction B with
  | nil => rfl
  | cons x xs ih =>
      have hxs : ∀ y ∈ xs, y ≤ 90 :=
        fun y hy => hB y (List.mem_cons_of_mem x hy)
      have hb := highValue_bound 10 xs (by simpa using hxs)
      have ht : highValue xs < 10 * 10 ^ xs.length := by omega
      have hp : 0 < 10 ^ xs.length := Nat.pow_pos (by decide)
      have hh := recover_head x (lowValue xs) (highValue xs)
        (10 ^ xs.length) hp ht
      simp only [List.length_cons, lowValue, highValue_cons, decodeValues]
      rw [hh]
      have hlo : (x + 10 * lowValue xs - x) / 10 = lowValue xs := by omega
      have hhi : x * 10 ^ xs.length + highValue xs - x * 10 ^ xs.length =
          highValue xs := by omega
      rw [hlo, hhi, ih hxs]

#print axioms highValue_bound
#print axioms decodeValues_length
#print axioms decodeValues_correct

end Agent5.BidirectionalWordDecoder
