import P196.Agent112NeutralNumericalArithmetic.Normalization

/-!
# Faithful bounded words from both positional values

At a fixed width, the forward 和 reversed base-`b` values determine every
natural coefficient word bounded by `2 * (b - 1)`, for every `b >= 2`.
Empty words 和 base two are included; symmetry is unnecessary.

This formalizes an all-base version of established positional recovery.
The decimal bound-18 theorem 和 its residue/tail argument are prior work in
`Agent115.ExteriorFactorization.eq_of_values`
(`P196.Agent6CoordinateDynamics.ExteriorObservationInjective`).
The head-recovery arithmetic below generalizes the private `recover_head`
used by Agent5's stronger decimal decoder in
`P196.BidirectionalWordDecoder.Numeric`. Agent112's prior PAPER symmetric
injectivity also implies the present mathematical statement by symmetric
concatenation. No new mathematical injectivity discovery is claimed.

The strict positional bound is imported through the verified normalization
quotient 和 carry bound, without a new coefficient-sum estimate. No decoder,
padding quotient, sharp alphabet threshold, cycle, or Lychrel claim is made.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

private theorem bounded_val_lt_twice_pow (b : Nat) (hb : 0 < b)
    (A : List Nat) (ha : ∀ d ∈ A, d ≤ 2 * (b - 1)) :
    val b A < 2 * b ^ A.length := by
  have hc := norm_carry_le_one b hb A 0 ha (by decide)
  rw [norm_carry_eq_div b hb A 0] at hc
  simp only [Nat.add_zero] at hc
  exact (Nat.div_lt_iff_lt_mul (Nat.pow_pos hb)).mp (by omega)

private theorem val_reverse_cons (b x : Nat) (A : List Nat) :
    val b (x :: A).reverse = x * b ^ A.length + val b A.reverse := by
  rw [List.reverse_cons, val_append]
  simp only [val_cons, val_nil, Nat.mul_zero, Nat.add_zero, List.length_reverse]
  ac_rfl

/-- Low residue 和 high quotient recover the first coefficient when the
reversed tail contributes fewer than `b` quotient units. -/
private theorem recover_head (b : Nat) (hb : 0 < b) (x V H P : Nat)
    (hP : 0 < P) (hH : H < b * P) :
    let r := (x + b * V) % b
    let q := (x * P + H) / P
    r + b * ((q - r) / b) = x := by
  dsimp only
  rw [Nat.add_mul_mod_self_left]
  have hdiv : (x * P + H) / P = x + H / P := by
    rw [Nat.mul_comm x P, Nat.mul_add_div hP]
  rw [hdiv]
  have hsmall : H / P < b := (Nat.div_lt_iff_lt_mul hP).mpr hH
  have hdecomp := Nat.mod_add_div x b
  have hsub : x + H / P - x % b = b * (x / b) + H / P := by
    calc
      _ = (x % b + b * (x / b)) + H / P - x % b :=
        congrArg (fun z : Nat => z + H / P - x % b) hdecomp.symm
      _ = _ := by rw [Nat.add_assoc, Nat.add_sub_cancel_left]
  rw [hsub, Nat.mul_add_div hb, Nat.div_eq_of_lt hsmall, Nat.add_zero]
  exact hdecomp

/-- A bounded coefficient word is determined by its width 和 its two
original positional values in every base at least two. -/
theorem eq_of_bidirectional_values (b : Nat) (hb : 2 ≤ b) (A B : List Nat)
    (hlen : A.length = B.length)
    (ha : ∀ d ∈ A, d ≤ 2 * (b - 1))
    (hboundB : ∀ d ∈ B, d ≤ 2 * (b - 1))
    (hv : val b A = val b B)
    (hr : val b A.reverse = val b B.reverse) : A = B := by
  have hb0 : 0 < b := by omega
  induction A generalizing B with
  | nil =>
      cases B with
      | nil => rfl
      | cons y ys => simp at hlen
  | cons x xs ih =>
      cases B with
      | nil => simp at hlen
      | cons y ys =>
          have hlen' : xs.length = ys.length := by simpa using hlen
          have hxs : ∀ d ∈ xs, d ≤ 2 * (b - 1) :=
            fun d hd => ha d (List.mem_cons_of_mem x hd)
          have hys : ∀ d ∈ ys, d ≤ 2 * (b - 1) :=
            fun d hd => hboundB d (List.mem_cons_of_mem y hd)
          have hP : 0 < b ^ ys.length := Nat.pow_pos hb0
          have hxsHigh : val b xs.reverse < b * b ^ ys.length := by
            have h := bounded_val_lt_twice_pow b hb0 xs.reverse
              (fun d hd => hxs d (List.mem_reverse.mp hd))
            rw [List.length_reverse, hlen'] at h
            exact Nat.lt_of_lt_of_le h (Nat.mul_le_mul_right (b ^ ys.length) hb)
          have hysHigh : val b ys.reverse < b * b ^ ys.length := by
            have h := bounded_val_lt_twice_pow b hb0 ys.reverse
              (fun d hd => hys d (List.mem_reverse.mp hd))
            rw [List.length_reverse] at h
            exact Nat.lt_of_lt_of_le h (Nat.mul_le_mul_right (b ^ ys.length) hb)
          change x + b * val b xs = y + b * val b ys at hv
          rw [val_reverse_cons, val_reverse_cons, hlen'] at hr
          have hx := recover_head b hb0 x (val b xs) (val b xs.reverse)
            (b ^ ys.length) hP hxsHigh
          have hy := recover_head b hb0 y (val b ys) (val b ys.reverse)
            (b ^ ys.length) hP hysHigh
          dsimp only at hx hy
          have hxy : x = y := by
            rw [hv, hr] at hx
            exact hx.symm.trans hy
          subst y
          have htailV : val b xs = val b ys :=
            Nat.eq_of_mul_eq_mul_left hb0 (Nat.add_left_cancel hv)
          have htailR : val b xs.reverse = val b ys.reverse := by omega
          rw [ih ys hlen' hxs hys htailV htailR]

end Agent112.NeutralNumericalArithmetic
