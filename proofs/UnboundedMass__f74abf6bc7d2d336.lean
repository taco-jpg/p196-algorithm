import ZeroGap

/-!
# Unbounded digit sums in every positive decimal reverse-and-add orbit

The combinatorial estimate says that bounded mass and a uniform bound on
zero runs force a finite word to have bounded length. Combined with exact
zero-run propagation and the existing quantitative width growth theorem,
this rules out bounded digit sums along any positive orbit.
-/

namespace DecimalUnboundedMass

open DecimalDigits DecimalMass FoldedDecimal OverflowCarryNormalization
  CarryHistory Lychrel196

/-- Splitting an unweighted finite word sum at any position. -/
theorem wordSum_split (q : Nat → Nat) (a k : Nat) :
    wordSum q (a + k) =
      wordSum q a + wordSum (fun i => q (a + i)) k := by
  induction k with
  | zero => simp [wordSum]
  | succ k ih =>
    change wordSum q (a + k) + q (a + k) =
      wordSum q a + (wordSum (fun i => q (a + i)) k + q (a + k))
    rw [ih]
    omega

/-- A finite word with no zero run longer than `K` has length at most
`(mass + 1) * (K + 1)`. Endpoint assumptions are unnecessary. -/
theorem length_le_of_zero_runs (q : Nat → Nat) (L K : Nat)
    (hz : ∀ a k, 0 < k → a + k ≤ L →
      (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) :
    L ≤ (wordSum q L + 1) * (K + 1) := by
  induction L using Nat.strongRecOn generalizing q with
  | ind L ih =>
    by_cases hshort : L ≤ K
    · have hm := Nat.mul_le_mul_right (K + 1)
        (show 1 ≤ wordSum q L + 1 by omega)
      simp only [Nat.one_mul] at hm
      omega
    · have hnonzero : ∃ i, i ≤ K ∧ 0 < q i := by
        apply Classical.byContradiction
        intro hn
        have hzprefix : ∀ i, 0 ≤ i → i < 0 + (K + 1) → q i = 0 := by
          intro i _ hi
          have hnot : ¬ 0 < q i := by
            intro hpos
            exact hn ⟨i, by omega, hpos⟩
          omega
        have hbad := hz 0 (K + 1) (by omega) (by omega) hzprefix
        omega
      obtain ⟨i, hi, hqi⟩ := hnonzero
      let a := i + 1
      let R := L - a
      have ha : 0 < a := by dsimp [a]; omega
      have haL : a ≤ L := by dsimp [a]; omega
      have hR : R < L := by dsimp [R]; omega
      have hsplit : a + R = L := by dsimp [R]; omega
      have htail : ∀ b k, 0 < k → b + k ≤ R →
          (∀ j, b ≤ j → j < b + k → (fun x => q (a + x)) j = 0) →
          k ≤ K := by
        intro b k hk hbk hzero
        apply hz (a + b) k hk (by omega)
        intro j hjlo hjhi
        have heq : a + (j - a) = j := by omega
        have hh := hzero (j - a) (by omega) (by omega)
        simpa only [heq] using hh
      have hbound := ih R hR (fun j => q (a + j)) htail
      have hmass : wordSum (fun j => q (a + j)) R + 1 ≤ wordSum q L := by
        have hs := wordSum_split q a R
        rw [hsplit] at hs
        have hp : wordSum q a = wordSum q i + q i := by rfl
        omega
      have hmul := Nat.mul_le_mul_right (K + 1) hmass
      have halim : a ≤ K + 1 := by dsimp [a]; omega
      rw [Nat.add_mul, Nat.one_mul]
      omega

/-- The mass of each exact pair-sum state is twice the ordinary decimal
digit sum of the actual numeric iterate. -/
theorem iterPairs_wordSum (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L)
    (hr : ∀ i, i < L → columnSum d L i = q i) :
    wordSum (iterPairs q L t).2 (iterPairs q L t).1 =
      2 * digitSum (orbit n t) := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L t hc hr
  calc
    wordSum (iterPairs q L t).2 (iterPairs q L t).1 =
        wordSum (columnSum e (iterPairs q L t).1) (iterPairs q L t).1 :=
      (wordSum_congr _ _ _ hrep).symm
    _ = 2 * wordSum e (iterPairs q L t).1 := wordSum_columns _ _
    _ = 2 * digitSum (orbit n t) := by
      rw [← digitSum_value e _ he.2.1, he.2.2.2]

/-- A bounded mass sharpens the purely combinatorial length estimate. -/
theorem length_le_of_mass_zero_runs (q : Nat → Nat) (L M K : Nat)
    (hm : wordSum q L ≤ M)
    (hz : ∀ a k, 0 < k → a + k ≤ L →
      (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) :
    L ≤ (M + 1) * (K + 1) := by
  apply Nat.le_trans (length_le_of_zero_runs q L K hz)
  exact Nat.mul_le_mul_right (K + 1) (by omega)

/-- The already established growth theorem excludes a uniform width
bound on an exact admissible pair-sum orbit. -/
theorem iterPairs_width_unbounded (q : Nat → Nat) (L H : Nat)
    (ha : Admissible L q) : ∃ t, H < (iterPairs q L t).1 := by
  refine ⟨4 * H + 5, ?_⟩
  have hg := DecimalWidthGrowth.width_lower_bound q L (4 * H + 5) ha
  omega

/-- The last argument is the local zero-run propagation theorem. This
auxiliary statement isolates the numeric connection and iteration. -/
theorem digitSum_unbounded_of_zero_run_propagation
    (hnext : ∀ (q : Nat → Nat) (L M K : Nat),
      Admissible L q → wordSum q L ≤ M →
      (∀ a k, 0 < k → a + k ≤ L →
        (∀ i, a ≤ i → i < a + k → q i = 0) → k ≤ K) →
      M + 2 ≤ K →
      (∀ a k, 0 < k → a + k ≤ nextWidth q L →
        (∀ i, a ≤ i → i < a + k → nextColumns q L i = 0) → k ≤ K))
    (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, B < digitSum (orbit n t) := by
  apply Classical.byContradiction
  intro hnone
  have hs : ∀ t, digitSum (orbit n t) ≤ B := by
    intro t
    have hnot : ¬ B < digitSum (orbit n t) := by
      intro hgt
      exact hnone ⟨t, hgt⟩
    omega
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  let q := columnSum d L
  let K := max L (2 * B + 2)
  let H := (2 * B + 1) * (K + 1)
  have ha : Admissible L q := NormalizationBridge.canonical_admissible n d L hc
  have hK : 2 * B + 2 ≤ K := Nat.le_max_right _ _
  have hLK : L ≤ K := Nat.le_max_left _ _
  have hm : ∀ t, wordSum (iterPairs q L t).2 (iterPairs q L t).1 ≤ 2 * B := by
    intro t
    rw [iterPairs_wordSum n d q L t hc (fun _ _ => rfl)]
    exact Nat.mul_le_mul_left 2 (hs t)
  have hz : ∀ t a k, 0 < k → a + k ≤ (iterPairs q L t).1 →
      (∀ i, a ≤ i → i < a + k → (iterPairs q L t).2 i = 0) → k ≤ K := by
    intro t
    induction t with
    | zero =>
      intro a k _ hlen _
      change a + k ≤ L at hlen
      omega
    | succ t ih =>
      exact hnext (iterPairs q L t).2 (iterPairs q L t).1 (2 * B) K
        (iterPairs_admissible q L t ha) (hm t) ih hK
  have hw : ∀ t, (iterPairs q L t).1 ≤ H := by
    intro t
    exact length_le_of_mass_zero_runs (iterPairs q L t).2
      (iterPairs q L t).1 (2 * B) K (hm t) (hz t)
  obtain ⟨t, ht⟩ := iterPairs_width_unbounded q L H ha
  have hb := hw t
  omega

/-- Every positive decimal reverse-and-add orbit has unbounded ordinary
digit sums. This is unconditional and concerns the actual numeric orbit. -/
theorem digitSum_unbounded (n : Nat) (hn : 0 < n) (B : Nat) :
    ∃ t, B < digitSum (orbit n t) :=
  digitSum_unbounded_of_zero_run_propagation DecimalZeroGap.zeroBound_next n hn B

/-- In particular, a positive reverse-and-add orbit cannot have constant
digit sum at every time. -/
theorem not_constant_digitSum (n : Nat) (hn : 0 < n) :
    ¬ (∀ t, digitSum (orbit n t) = digitSum n) := by
  intro hconstant
  obtain ⟨t, ht⟩ := digitSum_unbounded n hn (digitSum n)
  rw [hconstant t] at ht
  omega

#print axioms length_le_of_zero_runs
#print axioms iterPairs_wordSum
#print axioms digitSum_unbounded
#print axioms not_constant_digitSum

end DecimalUnboundedMass
