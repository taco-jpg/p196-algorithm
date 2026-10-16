import Agent105CrossWidth9df76b
import Agent101NonpalindromicFibers
import Agent101WidthFiberBounds
import Agent101MaximumWitnesses

/-!
Agent #101: sharp all-width ordinary-integer inverse cardinality.
The original two-width collision constraints refine the exterior counts to
eight and one; fixed-profile multiplicities supply the remaining factors.
-/

namespace Agent101.Maximum

open Lychrel196 DecimalDigits

/-- The existing actual-step width theorem expressed in numeric width form. -/
theorem predecessor_width_cases (Y D n : Nat) (hY : decimalWidth Y D)
    (hn : 0 < n) (hs : step n = Y) :
    decimalWidth n D ∨ decimalWidth n (D - 1) := by
  obtain ⟨d, L, hd⟩ := canonical_exists n hn
  obtain ⟨e, he⟩ := (decimalWidth_iff_canonical Y D).mp hY
  have he' : Canonical (step n) e D := by simpa only [hs] using he
  have hw := canonical_decimalWidth n d L hd
  rcases Agent105WidthSupport9df76b.step_width_cases hd he' with h | h
  · exact Or.inl (by simpa only [h.1] using hw)
  · exact Or.inr (by simpa only [h.1, Nat.add_sub_cancel] using hw)

theorem predecessor_one_digit_width (Y n : Nat) (hY : decimalWidth Y 1)
    (hn : 0 < n) (hs : step n = Y) : decimalWidth n 1 := by
  rcases predecessor_width_cases Y 1 n hY hn hs with h | h
  · exact h
  · have hp := h.1
    omega

theorem width_bound_mono (L K : Nat) (hLK : L ≤ K) :
    9 * 10 ^ (L / 2 - 1) ≤ 9 * 10 ^ (K / 2 - 1) := by
  exact Nat.mul_le_mul_left 9
    (Nat.pow_le_pow_right (by decide : 0 < 10) (by omega))

/-- The refined exterior factors 8 and 1 share a sufficient common bound. -/
theorem two_width_bound_arithmetic (D a b : Nat)
    (ha : a ≤ 8 * 10 ^ ((D - 1) / 2 - 1))
    (hb : b ≤ 10 ^ (D / 2 - 1)) :
    a + b ≤ 9 * 10 ^ (D / 2 - 1) := by
  have hpow : 10 ^ ((D - 1) / 2 - 1) ≤ 10 ^ (D / 2 - 1) :=
    Nat.pow_le_pow_right (by decide : 0 < 10) (by omega)
  have hm := Nat.mul_le_mul_left 8 hpow
  omega

/-- The bound counts all positive predecessors, including both possible
input widths; the list is arbitrary and need only be duplicate-free. -/
theorem all_width_preimages_bound (Y D : Nat) (ns : List Nat)
    (hY : decimalWidth Y D) (hD : 2 ≤ D) (hns : ns.Nodup)
    (hm : ∀ n ∈ ns, 0 < n ∧ step n = Y) :
    ns.length ≤ 9 * 10 ^ (D / 2 - 1) := by
  classical
  let wide := ns.filter (fun n => decide (decimalWidth n D))
  let short := ns.filter (fun n => !decide (decimalWidth n D))
  have hwp : ∀ n ∈ wide, decimalWidth n D ∧ step n = Y := by
    intro n hn
    have hx : n ∈ ns ∧ decimalWidth n D := by simpa [wide] using hn
    exact ⟨hx.2, (hm n hx.1).2⟩
  have hsp : ∀ n ∈ short, decimalWidth n (D - 1) ∧ step n = Y := by
    intro n hn
    have hx : n ∈ ns ∧ ¬ decimalWidth n D := by simpa [short] using hn
    have hp := hm n hx.1
    rcases predecessor_width_cases Y D n hY hp.1 hp.2 with hw | hs
    · exact False.elim (hx.2 hw)
    · exact ⟨hs, hp.2⟩
  have hwn : wide.Nodup := hns.filter _
  have hsn : short.Nodup := hns.filter _
  have hpart : wide.length + short.length = ns.length :=
    length_filter_partition ns (fun n => decide (decimalWidth n D))
  by_cases hw0 : wide = []
  · have hwlen : wide.length = 0 := by simp [hw0]
    by_cases hsmall : D - 1 = 1
    · have hslen : short.length ≤ 1 := one_digit_preimages_bound Y short hsn
        (by simpa only [hsmall] using hsp)
      have hpos : 0 < 10 ^ (D / 2 - 1) := Nat.pow_pos (by decide)
      omega
    · have hslen := fixed_width_preimages_bound Y (D - 1) short
        (by omega) hsn hsp
      have hmono := width_bound_mono (D - 1) D (by omega)
      omega
  · by_cases hs0 : short = []
    · have hslen : short.length = 0 := by simp [hs0]
      have hwlen := fixed_width_preimages_bound Y D wide hD hwn hwp
      omega
    · have hse : ∃ n, n ∈ short := by
        cases he : short with
        | nil => exact False.elim (hs0 he)
        | cons n xs => exact ⟨n, by simp [he]⟩
      have hwe : ∃ n, n ∈ wide := by
        cases he : wide with
        | nil => exact False.elim (hw0 he)
        | cons n xs => exact ⟨n, by simp [he]⟩
      obtain ⟨a, ha⟩ := hse
      obtain ⟨b, hb⟩ := hwe
      obtain ⟨haw, has⟩ := hsp a ha
      obtain ⟨hbw, hbs⟩ := hwp b hb
      obtain ⟨da, hca⟩ := (decimalWidth_iff_canonical a (D - 1)).mp haw
      obtain ⟨db, hcb⟩ := (decimalWidth_iff_canonical b D).mp hbw
      have hlt : D - 1 < D := by omega
      have heq : step a = step b := has.trans hbs.symm
      have houter := Agent105CrossWidth9df76b.cross_width_outer hca hcb hlt heq
      have hshortlen :=
        Agent105CrossWidth9df76b.cross_width_short_length hca hcb hlt heq
      have hsb := fixed_width_preimages_outer_bound Y (D - 1) a 11 da hca
        hshortlen has houter.1 short hsn hsp
      have hwb := fixed_width_preimages_outer_bound Y D b 1 db hcb
        hD hbs houter.2 wide hwn hwp
      have hsb' : short.length ≤ 8 * 10 ^ ((D - 1) / 2 - 1) := by
        simpa [pairCount] using hsb
      have hwb' : wide.length ≤ 10 ^ (D / 2 - 1) := by
        simpa [pairCount] using hwb
      have htotal := two_width_bound_arithmetic D short.length wide.length hsb' hwb'
      omega

/-- The one-digit target case has sharp bound one, not the multi-digit
formula with a truncated exponent. -/
theorem one_digit_target_preimages_bound (Y : Nat) (ns : List Nat)
    (hY : decimalWidth Y 1) (hns : ns.Nodup)
    (hm : ∀ n ∈ ns, 0 < n ∧ step n = Y) : ns.length ≤ 1 := by
  apply one_digit_preimages_bound Y ns hns
  intro n hn
  exact ⟨predecessor_one_digit_width Y n hY (hm n hn).1 (hm n hn).2,
    (hm n hn).2⟩

/-- Uniform upper bound over every D-digit target, together with an
explicit complete fiber attaining it. -/
theorem all_width_inverse_maximum (D : Nat) (hD : 2 ≤ D) :
    (∀ (Y : Nat) (ns : List Nat), decimalWidth Y D → ns.Nodup →
      (∀ n ∈ ns, 0 < n ∧ step n = Y) →
      ns.length ≤ 9 * 10 ^ (D / 2 - 1)) ∧
    (∃ (Y : Nat) (ns : List Nat), decimalWidth Y D ∧ ns.Nodup ∧
      (∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) ∧
      ns.length = 9 * 10 ^ (D / 2 - 1)) := by
  exact ⟨fun Y ns hY hn hm => all_width_preimages_bound Y D ns hY hD hn hm,
    MaximumWitnesses.all_width_maximum_witness D hD⟩

theorem one_digit_inverse_maximum :
    (∀ (Y : Nat) (ns : List Nat), decimalWidth Y 1 → ns.Nodup →
      (∀ n ∈ ns, 0 < n ∧ step n = Y) → ns.length ≤ 1) ∧
    (∃ (Y : Nat) (ns : List Nat), decimalWidth Y 1 ∧ ns.Nodup ∧
      (∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) ∧ ns.length = 1) := by
  exact ⟨fun Y ns hY hn hm => one_digit_target_preimages_bound Y ns hY hn hm,
    MaximumWitnesses.one_digit_maximum_witness⟩

#print axioms predecessor_width_cases
#print axioms predecessor_one_digit_width
#print axioms width_bound_mono
#print axioms two_width_bound_arithmetic
#print axioms all_width_preimages_bound
#print axioms one_digit_target_preimages_bound
#print axioms all_width_inverse_maximum
#print axioms one_digit_inverse_maximum

end Agent101.Maximum
