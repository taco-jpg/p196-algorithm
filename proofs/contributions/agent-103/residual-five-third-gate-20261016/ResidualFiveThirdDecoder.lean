import Agent105NumericDecoder9df76b
import ResidualFiveThirdWidth

set_option autoImplicit false

/-!
# The central decoder for the concrete residual-five predecessor fiber

This module specializes the original numerical decoder to the two forced
outer digit pairs (1,1) and (6,6). The unmodified inner `scan` accepts an
empty center and does not impose root positivity on an inner coefficient.
The final equivalence quantifies over every positive ordinary predecessor;
the original width obstruction removes all other possible source widths.
No generic predecessor enumeration is introduced.
-/

namespace Agent103.ResidualFiveThirdDecoder

open Lychrel196 DecimalDigits FoldedDecimal Agent101
open Agent105DecoderLocal9df76b Agent105DecoderScan9df76b
open Agent105NumericDecoder9df76b
open Agent103.ResidualFiveFibers

/-- Strip exactly the two concrete exterior pairs, retaining the original
scanner and its two zero boundary carries on all `2*r` central digits. -/
theorem scan_forced_boundary (r : Nat) (e : Nat → Nat)
    (h0 : e 0 = 1) (hlast : e (2 * r + 3) = 1)
    (h1 : e 1 = 6) (hsecond : e (2 * r + 2) = 6) :
    scan (2 * r + 4) e 0 0 =
      (scan (2 * r) (fun i => e (i + 2)) 0 0).map
        (fun qs => wrapDigits 1 1 (wrapDigits 6 6 qs)) := by
  have h11 : decodePair 1 1 0 0 = some ⟨1, 0, 0⟩ := by decide
  have h66 : decodePair 6 6 0 0 = some ⟨6, 0, 0⟩ := by decide
  simp only [scan, h0, hlast, h1, hsecond, h11, h66,
    Option.map_map, Function.comp_def, Nat.add_assoc]

/-- The forced positive exterior coefficient makes the original root
guard automatic, while the full central scan remains unchanged. -/
theorem decodeNumerical_forced_boundary (r : Nat) (e : Nat → Nat)
    (h0 : e 0 = 1) (hlast : e (2 * r + 3) = 1)
    (h1 : e 1 = 6) (hsecond : e (2 * r + 2) = 6) :
    decodeNumerical e (2 * r + 4) (2 * r + 4) =
      (scan (2 * r) (fun i => e (i + 2)) 0 0).map
        (fun qs => wrapDigits 1 1 (wrapDigits 6 6 qs)) := by
  unfold decodeNumerical
  rw [if_pos rfl]
  unfold decodeAtWidth
  rw [if_pos (show 0 < 2 * r + 4 ∧ 0 ≤ 1 by omega)]
  rw [scan_forced_boundary r e h0 hlast h1 hsecond]
  cases hscan : scan (2 * r) (fun i => e (i + 2)) 0 0 with
  | none => rfl
  | some qs => rfl

/-- At the forced source width, actual positive numerical predecessors are
equivalent to acceptance by the unchanged central scan. -/
theorem fixed_width_predecessor_iff_scan (r n : Nat) (e : Nat → Nat)
    (he : Canonical n e (2 * r + 4))
    (h0 : e 0 = 1) (hlast : e (2 * r + 3) = 1)
    (h1 : e 1 = 6) (hsecond : e (2 * r + 2) = 6) :
    (∃ z d, 0 < z ∧ Canonical z d (2 * r + 4) ∧ step z = n) ↔
      (scan (2 * r) (fun i => e (i + 2)) 0 0).isSome = true := by
  rw [← decodeNumerical_isSome_iff n e (2 * r + 4) (2 * r + 4) he]
  rw [decodeNumerical_forced_boundary r e h0 hlast h1 hsecond]
  cases scan (2 * r) (fun i => e (i + 2)) 0 0 <;> rfl

/-- The complete third-layer gate for the actual residual-five fiber.
There is no source-width premise on the quantified ordinary predecessor. -/
theorem fiber_predecessor_iff (r n : Nat) (e : Nat → Nat)
    (hn : n ∈ fiber r) (he : Canonical n e (2 * r + 4)) :
    (∃ z, 0 < z ∧ step z = n) ↔
      e 0 = 1 ∧ e (2 * r + 3) = 1 ∧
      e 1 = 6 ∧ e (2 * r + 2) = 6 ∧
      (scan (2 * r) (fun i => e (i + 2)) 0 0).isSome = true := by
  constructor
  · rintro ⟨z, hz, hstep⟩
    obtain ⟨d, L, hd⟩ := canonical_exists z hz
    obtain ⟨hwidth, _, _, _, h0, hlast, h1, hsecond⟩ :=
      Agent103.ResidualFiveThirdWidth.predecessor_boundary
        r n z L d e hn hz hstep hd he
    refine ⟨h0, hlast, h1, hsecond, ?_⟩
    apply (fixed_width_predecessor_iff_scan r n e he h0 hlast h1 hsecond).mp
    exact ⟨z, d, hz, by simpa only [hwidth] using hd, hstep⟩
  · rintro ⟨h0, hlast, h1, hsecond, hscan⟩
    obtain ⟨z, d, hz, _, hstep⟩ :=
      (fixed_width_predecessor_iff_scan r n e he h0 hlast h1 hsecond).mpr hscan
    exact ⟨z, hz, hstep⟩

/-- The same complete gate with an explicit caller-supplied target width.
The two upper indices are the actual highest and next-highest digits. -/
theorem fiber_predecessor_iff_of_width (r n W : Nat) (e : Nat → Nat)
    (hw : W = 2 * r + 4) (hn : n ∈ fiber r) (he : Canonical n e W) :
    (∃ z, 0 < z ∧ step z = n) ↔
      e 0 = 1 ∧ e (W - 1) = 1 ∧ e 1 = 6 ∧ e (W - 2) = 6 ∧
      (scan (2 * r) (fun i => e (i + 2)) 0 0).isSome = true := by
  subst W
  simpa only [show 2 * r + 4 - 1 = 2 * r + 3 by omega,
    show 2 * r + 4 - 2 = 2 * r + 2 by omega] using
    fiber_predecessor_iff r n e hn he

#print axioms scan_forced_boundary
#print axioms decodeNumerical_forced_boundary
#print axioms fixed_width_predecessor_iff_scan
#print axioms fiber_predecessor_iff
#print axioms fiber_predecessor_iff_of_width

end Agent103.ResidualFiveThirdDecoder
