import P196.CarryCountDecoding.CarryCountDecoding
import P196.Agent9DigitSumWindows.ProfileIsolation

/-!
A finite-mass estimate for nonnegative profiles transported by the two
overflow-dependent linear maps. The actual profile has coefficients at most
18, while an explicit nonnegative error is charged to weighted carry totals.
All profiles are functions on the natural-number half-line. A common finite
sum width and explicit zero-tail conditions justify the mass transport.
-/

set_option autoImplicit false

namespace UniformCarryWindows.LinearEnvelope

open DecimalMass CarryCountDecoding

/-- Right translation on the half-line, with an explicit zero boundary. -/
def rightShift (f : Nat → Nat) (i : Nat) : Nat :=
  if i = 0 then 0 else f (i - 1)

/-- The linear part selected by the actual overflow branch. -/
def transport (overflow : Bool) (f : Nat → Nat) (i : Nat) : Nat :=
  if overflow then f i + rightShift f i else 2 * f i

private def TailZero (f : Nat → Nat) (L : Nat) : Prop :=
  ∀ i, L ≤ i → f i = 0

private theorem rightShift_zero (f : Nat → Nat) : rightShift f 0 = 0 := by
  simp [rightShift]

private theorem rightShift_succ (f : Nat → Nat) (i : Nat) :
    rightShift f (i + 1) = f i := by
  simp [rightShift]

private theorem rightShift_mono (f g : Nat → Nat)
    (h : ∀ i, f i ≤ g i) (i : Nat) : rightShift f i ≤ rightShift g i := by
  by_cases hi : i = 0
  · simp [rightShift, hi]
  · simpa only [rightShift, hi, if_false] using h (i - 1)

private theorem rightShift_tail (f : Nat → Nat) (L : Nat)
    (h : TailZero f L) : TailZero (rightShift f) (L + 1) := by
  intro i hi
  have hi0 : i ≠ 0 := by omega
  simp only [rightShift, hi0, if_false]
  exact h (i - 1) (by omega)

private theorem sum_mono (f g : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → f i ≤ g i) : wordSum f L ≤ wordSum g L := by
  induction L with
  | zero => exact Nat.le_refl 0
  | succ L ih =>
    exact Nat.add_le_add (ih (fun i hi => h i (by omega))) (h L (by omega))

private theorem sum_rightShift (f : Nat → Nat) (L : Nat) :
    wordSum (rightShift f) (L + 1) = wordSum f L := by
  rw [wordSum_shift]
  simp only [rightShift_zero, rightShift_succ, Nat.zero_add]

private theorem transport_tail (b : Bool) (f : Nat → Nat) (L : Nat)
    (h : TailZero f L) : TailZero (transport b f) (L + 1) := by
  intro i hi
  have hf := h i (by omega)
  have hs := rightShift_tail f L h i hi
  cases b <;> simp [transport, hf, hs]

private theorem transport_mass (b : Bool) (f : Nat → Nat) (L : Nat)
    (h : TailZero f L) :
    wordSum (transport b f) (L + 1) = 2 * wordSum f L := by
  cases b with
  | false =>
    change wordSum (fun i => 2 * f i) (L + 1) = 2 * wordSum f L
    rw [wordSum_mul, wordSum, h L (Nat.le_refl L), Nat.add_zero]
  | true =>
    change wordSum (fun i => f i + rightShift f i) (L + 1) =
      2 * wordSum f L
    rw [wordSum_add, sum_rightShift, wordSum, h L (Nat.le_refl L)]
    omega

private theorem transport_mono (b : Bool) (f g : Nat → Nat)
    (h : ∀ i, f i ≤ g i) (i : Nat) : transport b f i ≤ transport b g i := by
  cases b with
  | false => exact Nat.mul_le_mul_left 2 (h i)
  | true => exact Nat.add_le_add (h i) (rightShift_mono f g h i)

private theorem transport_add (b : Bool) (f g : Nat → Nat) (i : Nat) :
    transport b (fun j => f j + g j) i =
      transport b f i + transport b g i := by
  by_cases hi : i = 0 <;> cases b <;>
    simp [transport, rightShift, hi, Nat.mul_add,
      Nat.add_assoc, Nat.add_left_comm, Nat.add_comm]

private theorem transport_mul (b : Bool) (f : Nat → Nat) (a i : Nat) :
    transport b (fun j => a * f j) i = a * transport b f i := by
  by_cases hi : i = 0 <;> cases b <;>
    simp [transport, rightShift, hi, Nat.mul_add,
      Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

private def virtual (f : Nat → Nat) (b : Nat → Bool) : Nat → Nat → Nat
  | 0 => f
  | t + 1 => transport (b t) (virtual f b t)

private def error (b : Nat → Bool) (d : Nat → Nat → Nat) : Nat → Nat → Nat
  | 0 => fun _ => 0
  | t + 1 => fun i => transport (b t) (error b d t) i + d t i

private def envelope (f : Nat → Nat) : Nat → Nat → Nat
  | 0 => f
  | t + 1 => fun i => f i + rightShift (envelope f t) i

private theorem virtual_tail (f : Nat → Nat) (b : Nat → Bool) (L : Nat)
    (h : TailZero f L) (t : Nat) : TailZero (virtual f b t) (L + t) := by
  induction t with
  | zero => simpa only [virtual, Nat.add_zero] using h
  | succ t ih =>
    simpa only [virtual, Nat.add_assoc] using
      transport_tail (b t) (virtual f b t) (L + t) ih

private theorem error_tail (b : Nat → Bool) (d : Nat → Nat → Nat) (L : Nat)
    (h : ∀ t i, L + t + 1 ≤ i → d t i = 0) (t : Nat) :
    TailZero (error b d t) (L + t) := by
  induction t with
  | zero => intro i _; rfl
  | succ t ih =>
    intro i hi
    have ht := transport_tail (b t) (error b d t) (L + t) ih i (by omega)
    change transport (b t) (error b d t) i + d t i = 0
    rw [ht, h t i (by omega)]

private theorem virtual_mass (f : Nat → Nat) (b : Nat → Bool) (L : Nat)
    (h : TailZero f L) (t : Nat) :
    wordSum (virtual f b t) (L + t) = 2 ^ t * wordSum f L := by
  induction t with
  | zero => simp [virtual]
  | succ t ih =>
    have ht := transport_mass (b t) (virtual f b t) (L + t)
      (virtual_tail f b L h t)
    have he : wordSum (virtual f b (t + 1)) (L + (t + 1)) =
        2 * wordSum (virtual f b t) (L + t) := by
      simpa only [virtual, Nat.add_assoc] using ht
    rw [he, ih]
    simp only [Nat.pow_succ, Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

private theorem error_mass (b : Nat → Bool) (d : Nat → Nat → Nat)
    (c : Nat → Nat) (L : Nat)
    (htail : ∀ t i, L + t + 1 ≤ i → d t i = 0)
    (hmass : ∀ t, wordSum (d t) (L + t + 1) ≤ 20 * c t) (t : Nat) :
    wordSum (error b d t) (L + t) ≤ 20 * weightedCount c t := by
  induction t with
  | zero => simp [error, wordSum_zero, weightedCount]
  | succ t ih =>
    have ht := transport_mass (b t) (error b d t) (L + t)
      (error_tail b d L htail t)
    have he : wordSum (transport (b t) (error b d t)) (L + (t + 1)) =
        2 * wordSum (error b d t) (L + t) := by
      simpa only [Nat.add_assoc] using ht
    have hd : wordSum (d t) (L + (t + 1)) ≤ 20 * c t := by
      simpa only [Nat.add_assoc] using hmass t
    change wordSum (fun i => transport (b t) (error b d t) i + d t i)
      (L + (t + 1)) ≤ 20 * (2 * weightedCount c t + c t)
    rw [wordSum_add, he]
    omega

private theorem envelope_mass (f : Nat → Nat) (L : Nat)
    (h : TailZero f L) (t : Nat) :
    wordSum (envelope f t) (L + t) = (t + 1) * wordSum f L := by
  induction t with
  | zero => simp [envelope]
  | succ t ih =>
    have hf := DecimalProfile.wordSum_padding f L (L + (t + 1)) h (by omega)
    have hs : wordSum (rightShift (envelope f t)) (L + (t + 1)) =
        wordSum (envelope f t) (L + t) := by
      simpa only [Nat.add_assoc] using sum_rightShift (envelope f t) (L + t)
    change wordSum (fun i => f i + rightShift (envelope f t) i)
      (L + (t + 1)) = (t + 1 + 1) * wordSum f L
    rw [wordSum_add, hf, hs, ih]
    simp only [Nat.add_mul, Nat.one_mul]
    omega

private theorem envelope_mono (f : Nat → Nat) (t : Nat) :
    ∀ i, envelope f t i ≤ envelope f (t + 1) i := by
  induction t with
  | zero =>
    intro i
    change f i ≤ f i + rightShift f i
    omega
  | succ t ih =>
    intro i
    change f i + rightShift (envelope f t) i ≤
      f i + rightShift (envelope f (t + 1)) i
    exact Nat.add_le_add (Nat.le_refl _) (rightShift_mono _ _ ih i)

private theorem transport_envelope (b : Bool) (f : Nat → Nat) (t i : Nat) :
    transport b (envelope f t) i ≤ 2 * envelope f (t + 1) i := by
  have hm := envelope_mono f t i
  have hs : rightShift (envelope f t) i ≤ envelope f (t + 1) i := by
    change rightShift (envelope f t) i ≤ f i + rightShift (envelope f t) i
    omega
  cases b with
  | false => exact Nat.mul_le_mul_left 2 hm
  | true =>
    change envelope f t i + rightShift (envelope f t) i ≤
      2 * envelope f (t + 1) i
    omega

private theorem virtual_le_envelope (f : Nat → Nat) (b : Nat → Bool) (t : Nat) :
    ∀ i, virtual f b t i ≤ 2 ^ t * envelope f t i := by
  induction t with
  | zero => intro i; simp [virtual, envelope]
  | succ t ih =>
    intro i
    have ht := transport_mono (b t) (virtual f b t)
      (fun j => 2 ^ t * envelope f t j) ih i
    rw [transport_mul] at ht
    calc
      virtual f b (t + 1) i = transport (b t) (virtual f b t) i := rfl
      _ ≤ 2 ^ t * transport (b t) (envelope f t) i := ht
      _ ≤ 2 ^ t * (2 * envelope f (t + 1) i) :=
        Nat.mul_le_mul_left (2 ^ t) (transport_envelope (b t) f t i)
      _ = 2 ^ (t + 1) * envelope f (t + 1) i := by
        rw [Nat.pow_succ, Nat.mul_assoc]

private theorem virtual_le_actual_error (q d : Nat → Nat → Nat)
    (b : Nat → Bool)
    (h : ∀ t i, transport (b t) (q t) i ≤ q (t + 1) i + d t i)
    (t : Nat) : ∀ i, virtual (q 0) b t i ≤ q t i + error b d t i := by
  induction t with
  | zero => intro i; simp [virtual, error]
  | succ t ih =>
    intro i
    have ht := transport_mono (b t) (virtual (q 0) b t)
      (fun j => q t j + error b d t j) ih i
    rw [transport_add] at ht
    have hs := h t i
    change transport (b t) (virtual (q 0) b t) i ≤
      q (t + 1) i + (transport (b t) (error b d t) i + d t i)
    omega

/-- Bounded actual coefficients and finitely supported per-step error give a
width-independent weighted mass inequality. The input width only locates the
finite sums and disappears from the conclusion's multiplicative constants. -/
theorem mass_bound (q d : Nat → Nat → Nat) (b : Nat → Bool)
    (c : Nat → Nat) (L N : Nat)
    (hstart : ∀ i, L ≤ i → q 0 i = 0)
    (hbounded : ∀ t i, q t i ≤ 18)
    (hstep : ∀ t i, transport (b t) (q t) i ≤ q (t + 1) i + d t i)
    (hdtail : ∀ t i, L + t + 1 ≤ i → d t i = 0)
    (hdmass : ∀ t, wordSum (d t) (L + t + 1) ≤ 20 * c t) :
    2 ^ N * wordSum (q 0) L ≤
      18 * (N + 1) * wordSum (q 0) L + 20 * weightedCount c N := by
  have hpoint : ∀ i, virtual (q 0) b N i ≤
      18 * envelope (q 0) N i + error b d N i := by
    intro i
    have hv := virtual_le_actual_error q d b hstep N i
    have hf := virtual_le_envelope (q 0) b N i
    by_cases hz : envelope (q 0) N i = 0
    · rw [hz, Nat.mul_zero] at hf ⊢
      omega
    · have hq := hbounded N i
      have hpos : 1 ≤ envelope (q 0) N i := by omega
      omega
  have hs := sum_mono (virtual (q 0) b N)
    (fun i => 18 * envelope (q 0) N i + error b d N i) (L + N)
    (fun i _ => hpoint i)
  rw [wordSum_add, wordSum_mul,
    virtual_mass (q 0) b L hstart N, envelope_mass (q 0) L hstart N] at hs
  have he := error_mass b d c L hdtail hdmass N
  calc
    2 ^ N * wordSum (q 0) L ≤
        18 * ((N + 1) * wordSum (q 0) L) + wordSum (error b d N) (L + N) := hs
    _ ≤ 18 * ((N + 1) * wordSum (q 0) L) + 20 * weightedCount c N :=
      Nat.add_le_add (Nat.le_refl _) he
    _ = 18 * (N + 1) * wordSum (q 0) L + 20 * weightedCount c N := by
      rw [Nat.mul_assoc]

#print axioms mass_bound

end UniformCarryWindows.LinearEnvelope
