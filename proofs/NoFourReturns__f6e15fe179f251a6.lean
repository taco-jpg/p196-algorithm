import ClockPaths
import ActualRank
import RankCertificate

/-! An actual orbit cannot maintain the seven-phase boundary clock
indefinitely. Failure of this clock does not imply a palindrome. -/

namespace NoFourReturns

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary SevenStepOrbit ClockPaths

theorem phasePrefix_lookup (i : Nat) (hi : i < 7) :
    ([⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
       ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] : List Prefix)[i]? =
      some (RankCertificate.phasePrefix i) := by
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

theorem phaseOverflow_lookup (i : Nat) (hi : i < 7) :
    ([0, 0, 1, 0, 1, 0, 1] : List Nat)[i]? = some (RankCertificate.phaseOverflow i) := by
  have hc : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 ∨ i = 5 ∨ i = 6 := by omega
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

def ClockThrough (q : Nat → Nat) (L N : Nat) : Prop :=
  (∀ t, t ≤ N → boundaryAt q L t = RankCertificate.phasePrefix (t % 7)) ∧
  (∀ t, t < N → overflowAt q L t = RankCertificate.phaseOverflow (t % 7))

/-- Consecutive actual return endpoints force every intervening phase and
every overflow. No choice of interior carries is introduced. -/
theorem returns_force_clock (q : Nat → Nat) (L K : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hreturns : ∀ j, j ≤ K → boundaryAt q L (7*j) = initial) :
    ClockThrough q L (7*K) := by
  have hblocks : ∀ j, j < K →
      actualTrace q L (7*j) 7 =
        [⟨4, 4, 0⟩, ⟨8, 8, 0⟩, ⟨16, 16, 0⟩, ⟨7, 14, 7⟩,
         ⟨15, 8, 15⟩, ⟨6, 14, 14⟩, ⟨13, 9, 9⟩, ⟨4, 4, 0⟩] ∧
      actualOverflows q L (7*j) 7 = [0, 0, 1, 0, 1, 0, 1] := by
    intro j hj
    have hs := hreturns j (by omega)
    have he : boundaryAt q L (7*j+7) = initial := by
      have hh := hreturns (j+1) (by omega)
      simpa only [Nat.mul_add, Nat.mul_one] using hh
    exact ⟨segment_trace_of_endpoints q L (7*j) hL ha hs he,
      segment_overflows_of_endpoints q L (7*j) hL ha hs he⟩
  constructor
  · intro t ht
    by_cases he : t = 7*K
    · subst t
      have hm : (7*K) % 7 = 0 := by omega
      rw [hm, hreturns K (Nat.le_refl K)]
      decide
    · have hj : t / 7 < K := by omega
      have hm : t % 7 < 7 := Nat.mod_lt _ (by decide)
      have heq : 7*(t/7) + t%7 = t := by omega
      have hg := actualTrace_get q L (7*(t/7)) 7 (t%7) (by omega)
      rw [(hblocks (t/7) hj).1, phasePrefix_lookup _ hm, heq] at hg
      exact (Option.some.inj hg).symm
  · intro t ht
    have hj : t / 7 < K := by omega
    have hm : t % 7 < 7 := Nat.mod_lt _ (by decide)
    have heq : 7*(t/7) + t%7 = t := by omega
    have hg := actualOverflows_get q L (7*(t/7)) 7 (t%7) hm
    rw [(hblocks (t/7) hj).2, phaseOverflow_lookup _ hm, heq] at hg
    exact (Option.some.inj hg).symm

/-- Rank descent applies to the actual six-column boundary at each
clock-preserving step, using its actual whole-word carry. -/
theorem actual_rank_decreases (q : Nat → Nat) (L t : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hbefore : boundaryAt q L t = RankCertificate.phasePrefix (t % 7))
    (hafter : boundaryAt q L (t + 1) = RankCertificate.phasePrefix ((t + 1) % 7))
    (hover : overflowAt q L t = RankCertificate.phaseOverflow (t % 7)) :
    ActualRank.rankAt q L (t + 1) < ActualRank.rankAt q L t := by
  obtain ⟨h3, h4, h5, hf, he, hr⟩ :=
    ActualRank.actual_clock_edge q L t hL ha hbefore hafter hover
  rw [hr]
  exact RankCertificate.rank_decreases (t % 7)
    ((iterPairs q L t).2 3) ((iterPairs q L t).2 4) ((iterPairs q L t).2 5)
    (SixPrefix.actualControl (iterPairs q L t).2 (iterPairs q L t).1)
    (Nat.mod_lt _ (by decide)) h3 h4 h5 hf he

/-- A phase-zero actual orbit follows this exact boundary and overflow
clock for at most 26 transitions. -/
theorem clock_length_bound (q : Nat → Nat) (L N : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hclock : ClockThrough q L N) : N ≤ 26 := by
  have hp := rank_path_bound (ActualRank.rankAt q L) N (by
    intro t ht
    exact actual_rank_decreases q L t hL ha
      (hclock.1 t (by omega)) (hclock.1 (t+1) (by omega)) (hclock.2 t ht))
  obtain ⟨h3, h4, h5⟩ := ActualRank.tail_bounds q L 0 hL ha
  have hb := RankCertificate.phase0_bound (q 3) (q 4) (q 5) h3 h4 h5
  change N ≤ RankCertificate.rank 0 (q 3) (q 4) (q 5) at hp
  omega

theorem no_twenty_seven_clock_steps (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) : ¬ ClockThrough q L 27 := by
  intro hc
  have hb := clock_length_bound q L 27 hL ha hc
  omega

/-- Four consecutive returns of the initial 440 boundary at times
7,14,21,28 are impossible. -/
theorem at_most_three_returns (q : Nat → Nat) (L K : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hreturns : ∀ j, j ≤ K → boundaryAt q L (7*j) = initial) : K ≤ 3 := by
  have hb := clock_length_bound q L (7*K) hL ha
    (returns_force_clock q L K hL ha hreturns)
  omega

theorem no_four_returns (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    ¬ (∀ j, j ≤ 4 → boundaryAt q L (7*j) = initial) := by
  intro hr
  have hb := at_most_three_returns q L 4 hL ha hr
  omega

theorem one_of_four_returns_fails (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) (hinit : boundary q = initial) :
    boundaryAt q L 7 ≠ initial ∨ boundaryAt q L 14 ≠ initial ∨
      boundaryAt q L 21 ≠ initial ∨ boundaryAt q L 28 ≠ initial := by
  by_cases h1 : boundaryAt q L 7 = initial
  · by_cases h2 : boundaryAt q L 14 = initial
    · by_cases h3 : boundaryAt q L 21 = initial
      · by_cases h4 : boundaryAt q L 28 = initial
        · exfalso
          apply no_four_returns q L hL ha
          intro j hj
          have hc : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 := by omega
          rcases hc with rfl | rfl | rfl | rfl | rfl
          · exact hinit
          · exact h1
          · exact h2
          · exact h3
          · exact h4
        · exact Or.inr (Or.inr (Or.inr h4))
      · exact Or.inr (Or.inr (Or.inl h3))
    · exact Or.inr (Or.inl h2)
  · exact Or.inl h1

theorem no_perpetual_returns (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    ¬ (∀ j, boundaryAt q L (7*j) = initial) := by
  intro hr
  exact no_four_returns q L hL ha (fun j _ => hr j)

/-- Canonical decimal digits supply admissibility automatically. This
corollary still concerns boundary recurrence, not palindrome occurrence. -/
theorem no_four_returns_of_canonical (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hL : 6 ≤ L) : ¬ (∀ j, j ≤ 4 → boundaryAt q L (7*j) = initial) := by
  have ha : Admissible L q := NormalizationBridge.admissible_congr _ _ _
    (NormalizationBridge.canonical_admissible n d L hc) hrep
  exact no_four_returns q L hL ha

end NoFourReturns
