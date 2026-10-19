import P196.OddTargetPredecessorParity.ProfileShift
import P196.OddTargetPredecessorParity.SourceWidth
import P196.OddTargetPredecessorParity.CandidateBounds

/-!
# The shifted half-target at a prescribed source width

Agent #6: increasing both outer coefficient positions of an odd profile
produces an even profile with a palindromic realization. Its value is the
target plus one in each outer position. Conversely, a palindrome in the
specified numerical range yields an odd profile after lowering those two
positions, and the original complete decoder recovers that profile.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105WordFiber9df76b Agent105NumericDecoder9df76b
open Agent105DecodedFiber9df76b CompleteFiberParity

private theorem odd_profile_candidate
    (Y L s : Nat) (h : List Nat) (c : Option Nat)
    (hL : 2 ≤ L)
    (hlen : (coefficientWord (s :: h) c).length = L)
    (hvalue : natValue (coefficientWord (s :: h) c) = Y)
    (hodd : s % 2 = 1) (ho : oddProfile (s :: h) c = true) :
    candidateAccepts Y L := by
  obtain ⟨⟨p, hpmem, hpal⟩, hs9⟩ :=
    (oddProfile_iff_shifted_palindrome s h c hodd).mp ho
  obtain ⟨ds, hds, hprofile, hpvalue⟩ :=
    (mem_numericFiber_digits ((s + 1) :: h) c p).mp hpmem
  have hdslen : ds.length = L := by
    have hl := congrArg List.length hprofile
    simp only [length_digitPairSums, length_coefficientWord,
      List.length_cons] at hl hlen
    omega
  have hpcan : Canonical p (digitFn ds) L := by
    simpa only [hpvalue, hdslen] using (canonicalDigits_iff ds).mp hds
  have hreverse : ds.reverse = ds :=
    (palindrome_natValue_iff_reverse ds hds).mp
      (by simpa only [hpvalue] using hpal)
  have hsym := digitFn_symmetric_of_reverse ds hreverse 0 (by omega)
  have houter : columnSum (digitFn ds) ds.length 0 = s + 1 := by
    rw [← digitFn_digitPairSums ds 0 (by omega), hprofile,
      digitFn_coefficientWord_cons_zero]
  have hlead : digitFn ds (L - 1) ≤ 5 := by
    simp only [columnSum, reflected, Nat.sub_zero] at houter
    simp only [Nat.sub_zero] at hsym
    rw [hdslen] at houter hsym
    omega
  have hpstep : step p = natValue (coefficientWord ((s + 1) :: h) c) := by
    rw [← hpvalue, step_natValue ds hds, hprofile]
  have hfixed : reverse10 p = p := hpal
  have hdouble : p + p = Y + 10 ^ (L - 1) + 1 := by
    rw [coefficientWord_outer_shift s h c, hvalue, hlen] at hpstep
    simpa only [step, hfixed] using hpstep
  have hpeq : p = shiftedHalf Y L := by
    unfold shiftedHalf
    omega
  have hwidth := canonical_decimalWidth p (digitFn ds) L hpcan
  have hupper := (canonical_leading_le_five_iff p L (digitFn ds) hpcan).mp hlead
  change 2 ≤ L ∧ 10 ^ (L - 1) ≤ shiftedHalf Y L ∧
    shiftedHalf Y L < 6 * 10 ^ (L - 1) ∧ Palindrome (shiftedHalf Y L)
  rw [← hpeq]
  exact ⟨hL, hwidth.2.1, hupper, hpal⟩

private theorem shiftedHalf_double
    (Y L : Nat) (hodd : Y % 2 = 1) (hL : 2 ≤ L) :
    shiftedHalf Y L + shiftedHalf Y L = Y + 10 ^ (L - 1) + 1 := by
  obtain ⟨k, hk⟩ := Nat.exists_eq_succ_of_ne_zero (show L - 1 ≠ 0 by omega)
  have hpow : 10 ^ (L - 1) % 2 = 0 := by
    rw [hk, Nat.pow_succ, Nat.mul_mod]
    simp
  unfold shiftedHalf
  omega

private theorem candidate_odd_profile
    (Y L : Nat) (hodd : Y % 2 = 1) (haccept : candidateAccepts Y L) :
    ∃ s h c, oddProfile (s :: h) c = true ∧
      (coefficientWord (s :: h) c).length = L ∧
      natValue (coefficientWord (s :: h) c) = Y := by
  rcases haccept with ⟨hL, hlow, hupp, hpal⟩
  obtain ⟨d, hpcan, hlead⟩ :=
    (candidate_canonical_iff (shiftedHalf Y L) L (by omega)).mp ⟨hlow, hupp⟩
  obtain ⟨ds, hdslen, hds, hpvalue, hdigit⟩ :=
    canonical_to_list (shiftedHalf Y L) d L hpcan
  have hreverse : ds.reverse = ds :=
    (palindrome_natValue_iff_reverse ds hds).mp
      (by simpa only [hpvalue] using hpal)
  obtain ⟨t, h, c, hprofile, _, hplen, ht⟩ :=
    digitPairSums_profile_cons ds (by omega)
  have hsym := digitFn_symmetric_of_reverse ds hreverse 0 (by omega)
  have hleadpos : 0 < digitFn ds (ds.length - 1) :=
    ((canonicalDigits_iff ds).mp hds).2.2.1
  have hleadle : digitFn ds (ds.length - 1) ≤ 5 := by
    rw [hdslen, hdigit (L - 1) (by omega)]
    exact hlead
  have htouter : t = digitFn ds (ds.length - 1) + digitFn ds (ds.length - 1) := by
    simp only [columnSum, reflected, Nat.sub_zero] at ht
    simp only [Nat.sub_zero] at hsym
    omega
  have htpos : 2 ≤ t := by omega
  have htbound : t ≤ 10 := by omega
  have hteven : t % 2 = 0 := by omega
  have htshift : t - 1 + 1 = t := by omega
  have hsodd : (t - 1) % 2 = 1 := by omega
  have hpmem : shiftedHalf Y L ∈ numericFiber ((t - 1 + 1) :: h) c := by
    apply (mem_numericFiber_digits ((t - 1 + 1) :: h) c (shiftedHalf Y L)).mpr
    exact ⟨ds, hds, by simpa only [htshift] using hprofile, hpvalue⟩
  have ho : oddProfile ((t - 1) :: h) c = true :=
    (oddProfile_iff_shifted_palindrome (t - 1) h c hsodd).mpr
      ⟨⟨shiftedHalf Y L, hpmem, hpal⟩, by omega⟩
  have hlen : (coefficientWord ((t - 1) :: h) c).length = L := by
    simp only [length_coefficientWord, List.length_cons] at hplen ⊢
    omega
  have hpstep : step (shiftedHalf Y L) = natValue (coefficientWord (t :: h) c) := by
    rw [← hpvalue, step_natValue ds hds, hprofile]
  have hfixed : reverse10 (shiftedHalf Y L) = shiftedHalf Y L := hpal
  have hdouble := shiftedHalf_double Y L hodd hL
  have hshift := coefficientWord_outer_shift (t - 1) h c
  rw [htshift, hlen] at hshift
  have hvalue : natValue (coefficientWord ((t - 1) :: h) c) = Y := by
    simp only [step, hfixed] at hpstep
    omega
  exact ⟨t - 1, h, c, ho, hlen, hvalue⟩

private theorem odd_profile_decode
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : Canonical Y e W) (s : Nat) (h : List Nat) (c : Option Nat)
    (ho : oddProfile (s :: h) c = true)
    (hlen : (coefficientWord (s :: h) c).length = L)
    (hvalue : natValue (coefficientWord (s :: h) c) = Y) :
    oddDecoded e W L = true := by
  have hcount : (numericFiber (s :: h) c).length % 2 = 1 :=
    (numericFiber_odd_iff (s :: h) c).mpr ho
  have hmember : ∃ n, n ∈ numericFiber (s :: h) c := by
    cases hf : numericFiber (s :: h) c with
    | nil => simp only [hf, List.length_nil] at hcount; omega
    | cons n ns => exact ⟨n, by simp only [hf, List.mem_cons, true_or]⟩
  obtain ⟨n, hn⟩ := hmember
  obtain ⟨ds, hds, hprofile, hnvalue⟩ :=
    (mem_numericFiber_digits (s :: h) c n).mp hn
  have hdslen : ds.length = L := by
    have hh := congrArg List.length hprofile
    simpa only [length_digitPairSums, hlen] using hh
  have hncan : Canonical n (digitFn ds) L := by
    simpa only [hnvalue, hdslen] using (canonicalDigits_iff ds).mp hds
  have hnpos : 0 < n := by
    simpa only [hnvalue] using natValue_positive ds hds
  have hnstep : step n = Y := by
    rw [← hnvalue, step_natValue ds hds, hprofile, hvalue]
  have hdec : decodeNumerical e W L = some (coefficientWord (s :: h) c) := by
    apply (decodeNumerical_eq_some_iff Y e W L (coefficientWord (s :: h) c) hY).mpr
    refine ⟨hlen, n, digitFn ds, hnpos, hncan, ?_, hnstep⟩
    intro i hi
    rw [← hdslen, ← digitFn_digitPairSums ds i (by omega), hprofile]
  simpa only [oddDecoded, hdec, half_coefficientWord, center_coefficientWord] using ho

/-- At any prescribed width, the complete predecessor multiplicity of an
odd canonical target is odd exactly when the source width is at least two
and its shifted half is a palindrome of that width whose leading digit
is at most five. -/
theorem odd_target_odd_decoded_iff
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1) :
    oddDecoded e W L = true ↔ candidateAccepts Y L := by
  constructor
  · intro ho
    cases hdec : decodeNumerical e W L with
    | none => simp only [oddDecoded, hdec] at ho; cases ho
    | some qs =>
      obtain ⟨hlen, n, d, _, hn, hprofile, hstep⟩ :=
        (decodeNumerical_eq_some_iff Y e W L qs hY).mp hdec
      have hL := odd_predecessor_width_ge_two n Y L d hn hstep hodd
      have hqodd : digitFn qs 0 % 2 = 1 := by
        rw [← hprofile 0 hn.1]
        exact odd_predecessor_outer n Y L d hn hstep hodd
      obtain ⟨_, hrev, _, hvalue⟩ :=
        decodeNumerical_word_spec Y e W L qs hY hdec
      obtain ⟨halfProfile, c, hq⟩ := exists_coefficientWord_of_reverse qs hrev
      cases halfProfile with
      | nil =>
        have hh := congrArg List.length hq
        rw [hlen, length_coefficientWord] at hh
        cases c <;> simp only [List.length_nil, Nat.mul_zero,
          Option.toList_none, Option.toList_some, List.length_cons] at hh <;> omega
      | cons s h =>
        rw [hq, digitFn_coefficientWord_cons_zero] at hqodd
        have hlen' : (coefficientWord (s :: h) c).length = L := by
          simpa only [hq] using hlen
        have hvalue' : natValue (coefficientWord (s :: h) c) = Y := by
          simpa only [hq] using hvalue
        have ho' : oddProfile (s :: h) c = true := by
          simpa only [oddDecoded, hdec, hq, half_coefficientWord,
            center_coefficientWord] using ho
        exact odd_profile_candidate Y L s h c hL hlen' hvalue' hqodd ho'
  · intro haccept
    obtain ⟨s, h, c, ho, hlen, hvalue⟩ := candidate_odd_profile Y L hodd haccept
    exact odd_profile_decode Y e W L hY s h c ho hlen hvalue

#print axioms odd_target_odd_decoded_iff

end OddTargetPredecessorParity
