import P196.PrefixWidthRealization.Realization

/-!
# Width boundaries and the sharp universal threshold

At full width the whole symmetric word is observed and the high inner
carry is zero. At twice the prefix length only the low scan fixes that
carry. One column below that width also exposes an even center.

The constant prefix of twos supplies a uniform obstruction to carry 1
at every shorter permitted width. Consequently 2*k+1 is the least source
width that realizes every valid length-k prefix with either prescribed
bit in one ordinary integer step.
-/

set_option autoImplicit false

namespace PrefixWidthRealization

open DecimalDigits FoldedDecimal SevenColumnProjection

/-- Full observation imposes the complete symmetry and center equations,
and the high inner carry is the initial zero. -/
theorem fits_full_width (s : List Nat) (b : Nat) :
    Fits s s.length b ↔
      (∀ i, i < s.length →
        s.getD i 0 = s.getD (s.length - 1 - i) 0) ∧
      (∀ i, i < s.length → 2 * i + 1 = s.length →
        s.getD i 0 % 2 = 0) ∧ b = 0 := by
  constructor
  · rintro ⟨hsym, hcenter, hcarry⟩
    refine ⟨?_, hcenter, ?_⟩
    · intro i hi
      exact hsym i hi (by omega)
    · have hc := hcarry (by omega)
      simpa [DecimalDigits.carry] using hc.symm
  · rintro ⟨hsym, hcenter, hbit⟩
    refine ⟨fun i hi _ => hsym i hi, hcenter, ?_⟩
    intro _
    simpa [DecimalDigits.carry] using hbit.symm

/-- Adjacent reflected prefixes impose no overlap or center constraint.
Their common boundary carry is the low scan through the entire prefix. -/
theorem fits_double_width (s : List Nat) (b : Nat) :
    Fits s (2 * s.length) b ↔
      carry (fun i => s.getD i 0) s.length = b := by
  have hindex : 2 * s.length - s.length = s.length := by omega
  constructor
  · intro h
    simpa only [hindex] using h.2.2 (Nat.le_refl _)
  · intro hc
    refine ⟨?_, ?_, ?_⟩
    · intro i hi href
      omega
    · intro i hi hcenter
      omega
    · intro _
      simpa only [hindex] using hc

/-- The first overlapping width exposes exactly the last prefix entry as
the center. Its parity and the preceding low carry are the only tests. -/
theorem fits_odd_boundary (s : List Nat) (b : Nat) (hk : 0 < s.length) :
    Fits s (2 * s.length - 1) b ↔
      s.getD (s.length - 1) 0 % 2 = 0 ∧
      carry (fun i => s.getD i 0) (s.length - 1) = b := by
  have hindex : (2 * s.length - 1) - s.length = s.length - 1 := by omega
  constructor
  · intro h
    refine ⟨h.2.1 (s.length - 1) (by omega) (by omega), ?_⟩
    simpa only [hindex] using h.2.2 (by omega)
  · rintro ⟨hcenter, hc⟩
    refine ⟨?_, ?_, ?_⟩
    · intro i hi href
      have hmirror : (2 * s.length - 1) - 1 - i = i := by omega
      simp only [hmirror]
    · intro i hi hmid
      have he : i = s.length - 1 := by omega
      simpa only [he] using hcenter
    · intro _
      simpa only [hindex] using hc

private theorem carry_replicate_two (k j : Nat) (hj : j ≤ k) :
    carry (fun i => (List.replicate k 2).getD i 0) j = 0 := by
  let q := fun i => (List.replicate k 2).getD i 0
  have hq : ∀ i, i < k → q i = 2 := by
    intro i hi
    simp [q, hi]
  have hsym : ∀ i, i < k → q i = q (k - 1 - i) := by
    intro i hi
    rw [hq i hi, hq (k - 1 - i) (by omega)]
  have hsmall : ∀ i, i < k → q i ≤ 9 := by
    intro i hi
    rw [hq i hi]
    decide
  exact (DecimalCarry.small_digit_sums_give_palindrome k q (carry q) (output q)
    hsym hsmall (fun i _ => column_equation q i) rfl).1 j hj

/-- A single explicit prefix obstructs bit 1 at every source width at most
twice its length. Together with the numeric iff this is an integer control
whenever the source width is at least the positive prefix length. -/
theorem fits_replicate_two (k L b : Nat) (hshort : L ≤ 2 * k) :
    Fits (List.replicate k 2) L b ↔ b = 0 := by
  constructor
  · intro hfit
    have hc := hfit.2.2 (by simpa only [List.length_replicate] using hshort)
    simp only [List.length_replicate] at hc
    rw [carry_replicate_two k (L - k) (by omega)] at hc
    exact hc.symm
  · intro hb
    refine ⟨?_, ?_, ?_⟩
    · intro i hi href
      have hik : i < k := by simpa only [List.length_replicate] using hi
      have hrk : L - 1 - i < k := by
        simpa only [List.length_replicate] using href
      simp [hik, hrk]
    · intro i hi hcenter
      have hik : i < k := by simpa only [List.length_replicate] using hi
      simp [hik]
    · intro _
      simpa only [List.length_replicate] using
        (carry_replicate_two k (L - k) (by omega)).trans hb.symm

private theorem fits_of_long_width (s : List Nat) (L b : Nat)
    (hwidth : 2 * s.length < L) : Fits s L b := by
  refine ⟨?_, ?_, ?_⟩
  · intro i hi href
    omega
  · intro i hi hcenter
    omega
  · intro hshort
    omega

/-- Every valid prefix of a fixed positive length, with either chosen bit,
has an actual canonical one-step realization at width L exactly when L is
strictly greater than twice that prefix length. -/
theorem universal_width_iff (k L : Nat) (hk : 0 < k) (hwidth : k ≤ L) :
    (∀ s : List Nat, s.length = k →
      (∀ a ∈ s, a < 19) → 0 < s.headD 0 →
      ∀ b : Nat, b ≤ 1 →
        ∃ (n : Nat) (d d' : Nat → Nat),
          let q := columnSum d L
          let W := nextWidth q L
          0 < n ∧ Canonical n d L ∧
          wordPrefix q k = s ∧ carry q (L - k) = b ∧
          Canonical (Lychrel196.step n) d' W ∧
          wordPrefix (columnSum d' W) k = forwardPrefix s b) ↔
      2 * k < L := by
  constructor
  · intro hall
    by_cases hlong : 2 * k < L
    · exact hlong
    · have hshort : L ≤ 2 * k := by omega
      let s := List.replicate k 2
      have hlength : s.length = k := by simp [s]
      have hs : ∀ a ∈ s, a < 19 := by
        intro a ha
        have he : a = 2 := List.eq_of_mem_replicate ha
        omega
      have hpos : 0 < s.headD 0 := by
        cases k with
        | zero => omega
        | succ k => simp [s, List.replicate_succ]
      have hr := hall s hlength hs hpos 1 (by decide)
      have hfit : Fits s L 1 := by
        apply (fits_iff_realizable s L 1 (by omega) (by omega) hs hpos
          (by decide)).mpr
        simpa only [hlength] using hr
      have hbad : 1 = 0 := (fits_replicate_two k L 1 hshort).mp hfit
      omega
  · intro hlong s hlength hs hpos b hb
    have hr := (fits_iff_realizable s L b (by omega) (by omega) hs hpos hb).mp
      (fits_of_long_width s L b (by omega))
    simpa only [hlength] using hr

#print axioms fits_full_width
#print axioms fits_double_width
#print axioms fits_odd_boundary
#print axioms fits_replicate_two
#print axioms universal_width_iff

end PrefixWidthRealization
