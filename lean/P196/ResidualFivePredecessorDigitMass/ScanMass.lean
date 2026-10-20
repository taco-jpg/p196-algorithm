import P196.ResidualFivePredecessorCount.ScanSupport
import P196.Drafts.Agent19Session8ff2acAgent19Session8ff2ac.ResidualFivePredecessorFilter
import P196.Agent2SaturatedProfile.ExteriorCharge

set_option autoImplicit false

/-!
The original numerical scanner has an exact scalar invariant on words
whose mirrored target digits sum to nine. The local identity is extracted
from the existing complete transition table, and the global identity
telescopes along the original successful scan, including the empty word.
-/

namespace P196.ResidualFivePredecessorDigitMass

open Agent101
open Agent105DecoderLocal9df76b (Edge ValidEdge decodePair decodePair_sound)
open Agent105DecoderScan9df76b (scan)

/-- Each existing sum-nine transition preserves this coefficient-mass
balance between its incoming and outgoing carry bits. -/
theorem validEdge_sum_nine_mass
    {u v a b : Nat} {E : Edge}
    (huv : u + v = 9) (ha : a ≤ 1) (hb : b ≤ 1)
    (hE : ValidEdge u v a b E) :
    2 * E.coeff + 10 * a + 10 * E.high =
      18 + 10 * E.low + 10 * b := by
  rcases (Agent103.ResidualFivePredecessorFilter.validEdge_sum_nine_iff
    huv ha hb).mp hE with h | h | h | h | h | h <;> omega

/-- The complete decoded coefficient word has an exact sum for every
accepted complementary target word and every pair of boundary carry bits.
No acceptance or existence assertion is made for a rejected scan. -/
theorem scan_raw_nines_sum
    (r a b : Nat) (ds qs : List Nat)
    (ha : a ≤ 1) (hb : b ≤ 1)
    (hds : ds ∈ rawWords (List.replicate r 9) none)
    (hscan : scan ds.length (digitFn ds) a b = some qs) :
    qs.sum + 10 * a = 18 * r + 10 * b := by
  induction r generalizing a b ds qs with
  | zero =>
    have hnil : ds = [] := by
      simpa only [List.replicate_zero, rawWords, centerWords,
        List.mem_singleton] using hds
    subst ds
    simp only [List.length_nil, scan] at hscan
    split at hscan
    · rename_i hab
      have hqs : qs = [] := (Option.some.inj hscan).symm
      subst qs
      simp [hab]
    · cases hscan
  | succ r ih =>
    rw [List.replicate_succ, rawWords] at hds
    obtain ⟨p, hp, hword⟩ := List.mem_flatMap.mp hds
    obtain ⟨inner, hinner, rfl⟩ := List.mem_map.mp hword
    rcases p with ⟨u, v⟩
    have huv : u + v = 9 := (mem_pairChoices false 9 u v).mp hp |>.2.2.1
    rw [length_wrapDigits, P196.ResidualFivePredecessorCount.scan_wrap] at hscan
    cases he : decodePair u v a b with
    | none => simp [he] at hscan
    | some E =>
      rw [he] at hscan
      simp only [Option.some_bind] at hscan
      cases hi : scan inner.length (digitFn inner) E.low E.high with
      | none => simp [hi] at hscan
      | some innerqs =>
        rw [hi] at hscan
        have hqs : wrapDigits E.coeff E.coeff innerqs = qs := Option.some.inj hscan
        have hE := decodePair_sound he
        have hm := ih E.low E.high inner innerqs hE.2.1 hE.2.2.1 hinner hi
        have hl := validEdge_sum_nine_mass huv ha hb hE
        subst qs
        simp only [wrapDigits, List.sum_cons, Agent2Exterior.sum_append,
          List.sum_nil, Nat.add_zero]
        omega

end P196.ResidualFivePredecessorDigitMass

#print axioms P196.ResidualFivePredecessorDigitMass.validEdge_sum_nine_mass
#print axioms P196.ResidualFivePredecessorDigitMass.scan_raw_nines_sum
