import P196.Agent112NeutralNumericalArithmetic.CenterStep
import P196.Agent119NeutralCenterPadding.Main

/-!
# Signed numerical accounting for an accepted center trim

Agent112's paper numerical model (#349/#368) and verified raw update (#398)
use the signed value relative to a neutral word of the same width. Agent7's
neutral-padding covariance identifies the accepted trimmed center with that
raw word. This module connects the two existing APIs: each paired neutral
layer multiplies the signed value by the base, so the actual trim gives an
exact scaled update. No symmetry or maximal-trim premise is needed.
-/

namespace Agent119.NeutralCenterNumericChain

open Agent120.Neutral
open Agent112.NeutralNumericalArithmetic
open Agent119.NeutralCenterPadding

/-- A natural base power viewed as an integer, without truncated subtraction. -/
def scale (b k : Nat) : Int := ((b ^ k : Nat) : Int)

theorem scale_zero (b : Nat) : scale b 0 = 1 := by
  simp only [scale, Nat.pow_zero, Int.ofNat_one]

theorem scale_add (b k l : Nat) : scale b (k + l) = scale b k * scale b l := by
  simp only [scale, Nat.pow_add, Int.ofNat_mul]

/-- The exact additive term in the existing raw signed-center update. -/
def increment (b : Nat) (B C : List Nat) : Int :=
  scale b (gam b B C) *
    ((reverseAtWidth b C.length (val b C + e1 b B) : Int) +
      (e1 b B : Int) * (scale b C.length + 1) - scale b C.length)

private theorem signedValue_padC_one {b : Nat} (hb : 1 ≤ b) (C : List Nat) :
    signedValue b (padC b 1 C) = (b : Int) * signedValue b C := by
  have hs : ((b - 1 : Nat) : Int) = (b : Int) - 1 := Int.ofNat_sub hb
  have hm : (b : Int) * ((b ^ C.length : Nat) : Int) =
      ((b ^ C.length : Nat) : Int) * (b : Int) := Int.mul_comm _ _
  simp only [signedValue, padC, List.replicate_one, List.cons_append,
    List.nil_append, val_cons, val_append, val_nil, List.length_cons,
    List.length_append, List.length_nil, Nat.add_zero, Nat.mul_zero,
    Nat.pow_succ, Int.ofNat_add, Int.ofNat_mul, Int.ofNat_one, hs,
    Int.mul_add, Int.mul_sub, Int.sub_mul, Int.mul_one, Int.one_mul,
    ← Int.mul_assoc, hm]
  omega

/-- Paired neutral padding scales the signed value for every coefficient word. -/
theorem signedValue_padC {b : Nat} (hb : 1 ≤ b) (v : Nat) (C : List Nat) :
    signedValue b (padC b v C) = scale b v * signedValue b C := by
  induction v with
  | zero => simp only [padC_zero, scale_zero, Int.one_mul]
  | succ v ih =>
      have hp : padC b (v + 1) C = padC b 1 (padC b v C) := by
        rw [padC_add, Nat.add_comm 1 v]
      rw [hp, signedValue_padC_one hb, ih]
      simp only [scale, Nat.pow_succ, Int.ofNat_mul]
      ac_rfl

/-- The accepted trim equation converts the raw numerical update into its scaled form. -/
theorem trimmed_signed_update {b : Nat} {B C C2 : List Nat} {v : Nat}
    (h : Hyp b B C) (ht : nextC b B C = padC b v C2) :
    scale b v * signedValue b C2 = signedValue b C + increment b B C := by
  have hs := signedValue_nextC h
  rw [ht, signedValue_padC (by have := h.base; omega)] at hs
  exact hs

/-- Every edge accepted by the unchanged checker obeys the exact signed trim law. -/
theorem edge_signed_update {b : Nat} {E : Edge} (he : edgeOK b E = true) :
    scale b E.v * signedValue b E.C2 =
      signedValue b E.C + increment b E.B E.C := by
  obtain ⟨h, _, ht⟩ := edgeOK_sound he
  exact trimmed_signed_update h ht

end Agent119.NeutralCenterNumericChain

#print axioms Agent119.NeutralCenterNumericChain.scale_zero
#print axioms Agent119.NeutralCenterNumericChain.scale_add
#print axioms Agent119.NeutralCenterNumericChain.signedValue_padC
#print axioms Agent119.NeutralCenterNumericChain.trimmed_signed_update
#print axioms Agent119.NeutralCenterNumericChain.edge_signed_update
