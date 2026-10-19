import P196.UniformCarryWindows.LinearEnvelope
import P196.Agent9DigitSumWindows.DecimalEmbedding
import P196.Agent9DigitSumWindows.ProfileIsolation

set_option autoImplicit false

/-!
# A width-independent carry budget for actual decimal orbits

The actual pair-sum word is compared with the unnormalized linear update.
The finite error word counts each outgoing carry twice, with coefficient ten.
Its support and reflection use the actual successor width, including overflow.
The virtual linear estimate therefore applies to ordinary integer dynamics.
-/

namespace UniformCarryWindows

open Lychrel196 DecimalDigits DecimalMass FoldedDecimal
  OverflowCarryNormalization CarryHistory CarryCountGrowth
  DecimalProfile.NumericBridge LinearEnvelope

private def outgoingProfile (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < L then carry q (i + 1) else 0

private def carryError (q : Nat → Nat) (L i : Nat) : Nat :=
  if i < nextWidth q L then
    10 * (outgoingProfile q L i +
      outgoingProfile q L (nextWidth q L - 1 - i))
  else 0

private theorem carryError_tail (q : Nat → Nat) (L i : Nat)
    (hi : nextWidth q L ≤ i) : carryError q L i = 0 := by
  simp [carryError, Nat.not_lt.mpr hi]

private theorem carryError_sum (q : Nat → Nat) (L : Nat) :
    wordSum (carryError q L) (nextWidth q L) = 20 * carryCount q L := by
  have hw : L ≤ nextWidth q L := by
    unfold nextWidth
    split <;> omega
  have hu : wordSum (outgoingProfile q L) (nextWidth q L) = carryCount q L := by
    calc
      wordSum (outgoingProfile q L) (nextWidth q L) =
          wordSum (outgoingProfile q L) L :=
        DecimalProfile.wordSum_padding _ L _
          (fun i hi => by simp [outgoingProfile, Nat.not_lt.mpr hi]) hw
      _ = carryCount q L := by
        apply wordSum_congr
        intro i hi
        simp [outgoingProfile, hi]
  calc
    wordSum (carryError q L) (nextWidth q L) =
        wordSum (fun i => 10 * (outgoingProfile q L i +
          reflected (outgoingProfile q L) (nextWidth q L) i))
          (nextWidth q L) := by
      apply wordSum_congr
      intro i hi
      simp [carryError, reflected, hi]
    _ = 10 * (wordSum (outgoingProfile q L) (nextWidth q L) +
          wordSum (reflected (outgoingProfile q L) (nextWidth q L))
            (nextWidth q L)) := by
      rw [wordSum_mul, wordSum_add]
    _ = 20 * carryCount q L := by
      rw [wordSum_reflected, hu]
      omega

private theorem pad_bounded (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (i : Nat) : pad q L i ≤ 18 := by
  by_cases hi : i < L
  · simpa only [pad, if_pos hi] using ha.2.2.1 i hi
  · simp [pad, hi]

private theorem actual_transport_bound (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (i : Nat) :
    transport (decide (carry q L ≠ 0)) (pad q L) i ≤
      pad (nextColumns q L) (nextWidth q L) i + carryError q L i := by
  by_cases ho : carry q L = 0
  · by_cases hi : i < L
    · have hm : L - 1 - i < L := by omega
      have he : L - 1 - i + 1 = L - i := by omega
      have hcol := next_column_no_overflow q L i hi ha.2.2.2.1 ho
      have hb : 2 * q i ≤ nextColumns q L i +
          10 * (carry q (i + 1) + carry q (L - i)) := by omega
      simpa [transport, ho, pad, carryError, nextWidth, outgoingProfile,
        hi, hm, he] using hb
    · simp [transport, ho, pad, carryError, nextWidth, hi]
  · have hc : carry q L = 1 := by
      have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
      omega
    have hw : nextWidth q L = L + 1 := by simp [nextWidth, ho]
    by_cases hiW : i < L + 1
    · by_cases hz : i = 0
      · subst i
        have hcol := next_column_overflow_outer q L ha.1 hc
        have hb : q 0 ≤ nextColumns q L 0 + 10 * carry q 1 := by omega
        simpa [transport, ho, pad, rightShift, carryError, nextWidth,
          outgoingProfile, ha.1] using hb
      · by_cases hi : i < L
        · have hm : L - i < L := by omega
          have hp : i - 1 < L := by omega
          have hcol := next_column_overflow_interior q L i (by omega) hi
            ha.2.2.2.1 hc
          have hb : q i + q (i - 1) ≤ nextColumns q L i +
              10 * (carry q (i + 1) + carry q (L - i + 1)) := by omega
          simpa [transport, ho, pad, rightShift, carryError, nextWidth,
            outgoingProfile, hiW, hi, hm, hp, hz] using hb
        · have he : i = L := by omega
          subst i
          have hL := ha.1
          have hp : L - 1 < L := by omega
          have hs : q (L - 1) = q 0 := by
            simpa only [Nat.sub_zero] using (ha.2.2.2.1 0 hL).symm
          have hn := NormalizationBridge.admissible_next q L ha
          rw [hw] at hn
          have hns : nextColumns q L L = nextColumns q L 0 := by
            simpa only [Nat.add_sub_cancel, Nat.sub_self] using
              hn.2.2.2.1 L (by omega)
          have hcol := next_column_overflow_outer q L hL hc
          have hb : q (L - 1) ≤ nextColumns q L L + 10 * carry q 1 := by
            rw [hs, hns]
            omega
          simpa [transport, ho, pad, rightShift, carryError, nextWidth,
            outgoingProfile, hL, hp, Nat.ne_of_gt hL] using hb
    · have hi : ¬ i < L := by omega
      have hp : ¬ i - 1 < L := by omega
      have hz : i ≠ 0 := by omega
      simp [transport, ho, pad, rightShift, carryError, nextWidth,
        hiW, hi, hp, hz]

private theorem iter_width_le (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q) : (iterPairs q L t).1 ≤ L + t := by
  have h := DecimalProfile.iter_width_upper (embed (L, q)) t
  rw [iter_embed q L t ha] at h
  simpa only [embed] using h

private theorem iter_carryCount (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L)
    (hr : ∀ i, i < L → columnSum d L i = q i) :
    outgoingCarryCount (orbit n t) =
      carryCount (iterPairs q L t).2 (iterPairs q L t).1 := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L t hc hr
  rw [outgoingCarryCount_of_canonical _ _ _ he]
  unfold carryCount
  apply wordSum_congr
  intro i hi
  exact carry_congr_upto _ _ _ hrep (i + 1) (by omega)

private theorem weighted_mass_bound_of_canonical
    (n : Nat) (d : Nat → Nat) (L N : Nat) (hc : Canonical n d L) :
    2 ^ N * (2 * digitSum n) ≤
      18 * (N + 1) * (2 * digitSum n) +
        20 * CarryCountDecoding.weightedCount
          (fun t => outgoingCarryCount (orbit n t)) N := by
  let q := columnSum d L
  let s := iterPairs q L
  let a := fun t => pad (s t).2 (s t).1
  let b := fun t => decide (carry (s t).2 (s t).1 ≠ 0)
  let e := fun t => carryError (s t).2 (s t).1
  let c := fun t => outgoingCarryCount (orbit n t)
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have has : ∀ t, Admissible (s t).1 (s t).2 :=
    fun t => iterPairs_admissible q L t ha
  have hwidth : ∀ t, (s t).1 ≤ L + t := fun t => iter_width_le q L t ha
  have hstart : ∀ i, L ≤ i → a 0 i = 0 := by
    intro i hi
    simp [a, s, iterPairs, pad, Nat.not_lt.mpr hi]
  have hbounded : ∀ t i, a t i ≤ 18 :=
    fun t i => pad_bounded (s t).2 (s t).1 (has t) i
  have hstep : ∀ t i, transport (b t) (a t) i ≤ a (t + 1) i + e t i := by
    intro t i
    exact actual_transport_bound (s t).2 (s t).1 (has t) i
  have htail : ∀ t i, L + t + 1 ≤ i → e t i = 0 := by
    intro t i hi
    apply carryError_tail
    have hw := hwidth (t + 1)
    change nextWidth (s t).2 (s t).1 ≤ L + (t + 1) at hw
    omega
  have hmass : ∀ t, wordSum (e t) (L + t + 1) ≤ 20 * c t := by
    intro t
    have hw := hwidth (t + 1)
    change nextWidth (s t).2 (s t).1 ≤ L + (t + 1) at hw
    have hcarries := iter_carryCount n d q L t hc (fun _ _ => rfl)
    calc
      wordSum (e t) (L + t + 1) =
          wordSum (e t) (nextWidth (s t).2 (s t).1) :=
        DecimalProfile.wordSum_padding _ _ _
          (fun i hi => carryError_tail (s t).2 (s t).1 i hi) (by omega)
      _ = 20 * carryCount (s t).2 (s t).1 := carryError_sum (s t).2 (s t).1
      _ = 20 * c t := by rw [← hcarries]
      _ ≤ 20 * c t := Nat.le_refl _
  have hinit : wordSum (a 0) L = 2 * digitSum n := by
    calc
      wordSum (a 0) L = wordSum q L := by
        apply wordSum_congr
        intro i hi
        simp [a, s, iterPairs, pad, hi]
      _ = 2 * digitSum n := by
        simpa only [iterPairs, orbit] using
          DecimalUnboundedMass.iterPairs_wordSum n d q L 0 hc (fun _ _ => rfl)
  have h := LinearEnvelope.mass_bound a e b c L N hstart hbounded hstep htail hmass
  rw [hinit] at h
  exact h

/-- The weighted total of actual outgoing carry positions controls the
initial digit sum, independently of decimal width. The zero seed and an
empty observation history are included. -/
theorem weighted_mass_bound (n N : Nat) :
    2 ^ N * (2 * digitSum n) ≤
      18 * (N + 1) * (2 * digitSum n) +
        20 * CarryCountDecoding.weightedCount
          (fun t => outgoingCarryCount (orbit n t)) N := by
  by_cases hz : n = 0
  · subst n
    simp only [digitSum_zero, Nat.mul_zero, Nat.zero_add]
    exact Nat.zero_le _
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    exact weighted_mass_bound_of_canonical n d L N hc

#print axioms weighted_mass_bound

end UniformCarryWindows
