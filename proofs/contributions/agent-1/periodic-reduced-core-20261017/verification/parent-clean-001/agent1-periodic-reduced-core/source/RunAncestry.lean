import LychrelDigitSums

/-!
# Maximal 0/18-run ancestry under actual decimal reverse-and-add

Agent #102 contribution (task `agent102-ancestry-lean`).

All statements concern the exact full symmetric column-sum word `q` of width `L`
(`FoldedDecimal.Admissible L q`) and its actual successor
`FoldedDecimal.nextColumns q L` of width `FoldedDecimal.nextWidth q L`, i.e. the
canonical pair-sum words of consecutive ordinary integers of an orbit
(`OverflowCarryNormalization.iterPairs_representation`).

This formalizes Section 2 of
`proofs/research/main_existence_attempt/continuation_pass/seam_persistence/followup_absorbing_core/ABSORBING_CORE.md`
(exact descendant interval, no expansion, no merging) and the extinction-time corollary of
`proofs/contributions/2026-10-15-ancestry-potential-bound/ANCESTRY_BOUND.md`.

It follows ONE ancestry. It does not show that 0/18 coefficients disappear from an orbit,
that a palindrome is reached, or anything about 196.
-/

namespace RunAncestry

open DecimalDigits FoldedDecimal

/-- The carry that a constant column of `0` (resp. `18`) forces. -/
def reset (c : Nat) : Nat := if c = 18 then 1 else 0

/-- Maximal run `[a,b)` of the symbol `c` inside a width-`L` word. -/
def MaximalRun (q : Nat → Nat) (L c a b : Nat) : Prop :=
  a < b ∧ b ≤ L ∧ (∀ i, a ≤ i → i < b → q i = c) ∧
  (a = 0 ∨ q (a - 1) ≠ c) ∧ (b = L ∨ q b ≠ c)

/-- The natural descendant interval of the run `[a,b)` after one actual step.
Without overflow an endpoint survives exactly when its exterior incoming carry equals the
reset carry; with overflow the low endpoint is always lost.  An interval with
`fst ≥ snd` is empty. -/
def descendant (q : Nat → Nat) (L c a b : Nat) : Nat × Nat :=
  if carry q L = 0 then
    (if carry q a = reset c then a else a + 1,
     if carry q (L - b) = reset c then b else b - 1)
  else (a + 1, b)

/-! ## Local carry and emission facts -/

theorem carry_le_one (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    ∀ i, i ≤ L → carry q i ≤ 1 :=
  carry_bounded q L ha.2.2.1

/-- Inside a run of `0` or `18`, every incoming carry is the reset carry. -/
theorem carry_after_constant (q : Nat → Nat) (L c i : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hi : i < L) (hq : q i = c) :
    carry q (i + 1) = reset c := by
  have hb := carry_le_one q L ha i (by omega)
  show (q i + carry q i) / 10 = reset c
  rw [hq]
  rcases hc with rfl | rfl <;> simp [reset] <;> omega

theorem next_no_overflow (q : Nat → Nat) (L i : Nat) (ha : Admissible L q)
    (hov : carry q L = 0) (hi : i < L) :
    nextColumns q L i = (q i + carry q i) % 10 + (q i + carry q (L - 1 - i)) % 10 :=
  folded_emission_no_overflow q L i hi ha.2.2.2.1 hov

theorem next_overflow_pos (q : Nat → Nat) (L i : Nat) (ha : Admissible L q)
    (hov : carry q L = 1) (h0 : 0 < i) (hi : i < L) :
    nextColumns q L i =
      (q i + carry q i) % 10 + (q (i - 1) + carry q (L - i)) % 10 := by
  rw [folded_emission_overflow q L i hi hov]
  have hm : L - i < L := by omega
  have hs := ha.2.2.2.1 (L - i) hm
  have hind : L - 1 - (L - i) = i - 1 := by omega
  rw [hind] at hs
  simp only [extended, hm, if_pos, output, hs]

theorem next_overflow_zero (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hov : carry q L = 1) :
    nextColumns q L 0 = q 0 % 10 + 1 := by
  rw [folded_emission_overflow q L 0 ha.1 hov]
  simp [extended, hov, output, carry]

theorem next_overflow_top (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hov : carry q L = 1) :
    nextColumns q L L = 1 + q 0 % 10 := by
  have hL := ha.1
  simp only [nextColumns, hov, Nat.one_ne_zero, if_false, columnSum, reflected]
  have h1 : L + 1 - 1 - L = 0 := by omega
  rw [h1]
  simp [extended, hL, hov, output, carry]

theorem carry_pred (q : Nat → Nat) (i : Nat) (hi : 0 < i) :
    carry q i = (q (i - 1) + carry q (i - 1)) / 10 := by
  obtain ⟨k, rfl⟩ : ∃ k, i = k + 1 := ⟨i - 1, by omega⟩
  rfl

theorem carry_top (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    carry q L = (q 0 + carry q (L - 1)) / 10 := by
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 1 := ⟨L - 1, by have := ha.1; omega⟩
  have hs := ha.2.2.2.1 0 (by omega)
  have h0 : q 0 = q k := by simpa using hs
  simp only [carry, Nat.add_sub_cancel]
  rw [h0]

/-! ## The one-step ancestry theorem -/

/-- Common facts about a maximal run and its mirror image. -/
theorem run_facts (q : Nat → Nat) (L c a b : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b) :
    (∀ i, a < i → i ≤ b → carry q i = reset c) ∧
    (∀ i, L - b ≤ i → i < L - a → q i = c) ∧
    (∀ i, L - b < i → i ≤ L - a → carry q i = reset c) := by
  obtain ⟨hab, hbL, hrun, -, -⟩ := hr
  have hmir : ∀ i, L - b ≤ i → i < L - a → q i = c := by
    intro i h1 h2
    rw [ha.2.2.2.1 i (by omega)]
    exact hrun _ (by omega) (by omega)
  refine ⟨?_, hmir, ?_⟩
  · intro i h1 h2
    have he : i = (i - 1) + 1 := by omega
    rw [he]
    exact carry_after_constant q L c (i - 1) ha hc (by omega) (hrun _ (by omega) (by omega))
  · intro i h1 h2
    have he : i = (i - 1) + 1 := by omega
    rw [he]
    exact carry_after_constant q L c (i - 1) ha hc (by omega) (hmir _ (by omega) (by omega))

/-! ### Finite arithmetic kernels (all digits/carries are bounded) -/

theorem reset_zero : reset 0 = 0 := rfl
theorem reset_eighteen : reset 18 = 1 := rfl

theorem pair_eq_iff (c u v : Nat) (hc : c = 0 ∨ c = 18) (hu : u ≤ 1) (hv : v ≤ 1) :
    (c + u) % 10 + (c + v) % 10 = c ↔ u = reset c ∧ v = reset c := by
  have k0 : ∀ u, u < 2 → ∀ v, v < 2 →
      ((0 + u) % 10 + (0 + v) % 10 = 0 ↔ u = 0 ∧ v = 0) := by decide
  have k1 : ∀ u, u < 2 → ∀ v, v < 2 →
      ((18 + u) % 10 + (18 + v) % 10 = 18 ↔ u = 1 ∧ v = 1) := by decide
  rcases hc with rfl | rfl
  · exact k0 u (by omega) v (by omega)
  · exact k1 u (by omega) v (by omega)

/-- A non-`c` exterior column whose outgoing carry is the reset carry emits a non-`c`
symbol when there is no overflow. -/
theorem neighbor_no_overflow (c z x : Nat) (hc : c = 0 ∨ c = 18) (hz : z ≤ 18) (hzc : z ≠ c)
    (hx : x ≤ 1) (hout : (z + x) / 10 = reset c) :
    (z + x) % 10 + (z + reset c) % 10 ≠ c := by
  have k0 : ∀ z, z < 19 → ∀ x, x < 2 → z ≠ 0 → (z + x) / 10 = 0 →
      (z + x) % 10 + (z + 0) % 10 ≠ 0 := by decide
  have k1 : ∀ z, z < 19 → ∀ x, x < 2 → z ≠ 18 → (z + x) / 10 = 1 →
      (z + x) % 10 + (z + 1) % 10 ≠ 18 := by decide
  rcases hc with rfl | rfl
  · exact k0 z (by omega) x (by omega) hzc hout
  · exact k1 z (by omega) x (by omega) hzc hout

/-- The overflow-shifted boundary column between a run and a non-`c` neighbour. -/
theorem neighbor_overflow (c z x : Nat) (hc : c = 0 ∨ c = 18) (hz : z ≤ 18) (hzc : z ≠ c)
    (hx : x ≤ 1) :
    (c + (z + x) / 10) % 10 + (z + reset c) % 10 ≠ c := by
  have k0 : ∀ z, z < 19 → ∀ x, x < 2 → z ≠ 0 →
      (0 + (z + x) / 10) % 10 + (z + 0) % 10 ≠ 0 := by decide
  have k1 : ∀ z, z < 19 → ∀ x, x < 2 → z ≠ 18 →
      (18 + (z + x) / 10) % 10 + (z + 1) % 10 ≠ 18 := by decide
  rcases hc with rfl | rfl
  · exact k0 z (by omega) x (by omega) hzc
  · exact k1 z (by omega) x (by omega) hzc

theorem run_value (c : Nat) (hc : c = 0 ∨ c = 18) :
    (c + reset c) % 10 + (c + reset c) % 10 = c := by
  rcases hc with rfl | rfl <;> decide

/-- Exact one-step law for a maximal run of `0` or `18`.

* `exact`: on the old run, the new symbol is `c` exactly on the descendant interval;
* `maximal`: a nonempty descendant is a maximal run of `c` in the new word
  (no expansion and no merging with newly born runs);
* `bounds`: the descendant lies inside the old run, and its length drops by at least
  the actual overflow bit. -/
theorem descendant_step (q : Nat → Nat) (L c a b : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b) :
    (∀ i, a ≤ i → i < b →
        (nextColumns q L i = c ↔
          (descendant q L c a b).1 ≤ i ∧ i < (descendant q L c a b).2)) ∧
    ((descendant q L c a b).1 < (descendant q L c a b).2 →
        MaximalRun (nextColumns q L) (nextWidth q L) c
          (descendant q L c a b).1 (descendant q L c a b).2) ∧
    (a ≤ (descendant q L c a b).1 ∧ (descendant q L c a b).2 ≤ b ∧
      (descendant q L c a b).2 - (descendant q L c a b).1 + carry q L ≤ b - a) := by
  obtain ⟨hcr, hmir, hcm⟩ := run_facts q L c a b ha hc hr
  obtain ⟨hab, hbL, hrun, hleft, hright⟩ := hr
  have hL := ha.1
  have hq18 := ha.2.2.1
  have hs := ha.2.2.2.1
  have hcb := carry_le_one q L ha
  have hpos := ha.2.1
  have hov := hcb L (Nat.le_refl L)
  have htop := carry_top q L ha
  have hcl := hcb (L - 1) (by omega)
  have hres : reset c ≤ 1 := by rcases hc with rfl | rfl <;> decide
  by_cases h0 : carry q L = 0
  · -- no overflow: the run is strictly interior
    have ha0 : 0 < a := by
      rcases Nat.eq_zero_or_pos a with hz | hz
      · exfalso
        have hq := hrun 0 (by omega) (by omega)
        rcases hc with rfl | rfl <;> omega
      · exact hz
    have hbL' : b < L := by
      rcases Nat.lt_or_ge b L with hz | hz
      · exact hz
      · exfalso
        have hq : q (L - 1) = c := hrun (L - 1) (by omega) (by omega)
        have h00 := hs 0 hL
        simp only [Nat.sub_zero] at h00
        rcases hc with rfl | rfl <;> omega
    have hd : descendant q L c a b =
        (if carry q a = reset c then a else a + 1,
         if carry q (L - b) = reset c then b else b - 1) := by
      simp [descendant, h0]
    rw [hd]
    dsimp only
    have hnw : nextWidth q L = L := by simp [nextWidth, h0]
    have em := fun i (hi : i < L) => next_no_overflow q L i ha h0 hi
    have hα := hcb a (by omega)
    have hβ := hcb (L - b) (by omega)
    -- position-wise characterization on the old run
    have key : ∀ i, a ≤ i → i < b →
        (nextColumns q L i = c ↔ carry q i = reset c ∧ carry q (L - 1 - i) = reset c) := by
      intro i h1 h2
      rw [em i (by omega), hrun i h1 h2]
      exact pair_eq_iff c _ _ hc (hcb i (by omega)) (hcb _ (by omega))
    have cond : ∀ i, a ≤ i → i < b →
        (carry q i = reset c ∧ carry q (L - 1 - i) = reset c ↔
          (if carry q a = reset c then a else a + 1) ≤ i ∧
            i < (if carry q (L - b) = reset c then b else b - 1)) := by
      intro i h1 h2
      have hA : carry q i = reset c ↔ (i = a → carry q a = reset c) := by
        by_cases hia : i = a
        · subst hia; simp
        · have := hcr i (by omega) (by omega)
          simp [this, hia]
      have hB : carry q (L - 1 - i) = reset c ↔ (i = b - 1 → carry q (L - b) = reset c) := by
        by_cases hib : i = b - 1
        · have hm : L - 1 - i = L - b := by omega
          rw [hm]; simp [hib]
        · have := hcm (L - 1 - i) (by omega) (by omega)
          simp [this, hib]
      rw [hA, hB]
      by_cases hx : carry q a = reset c <;> by_cases hy : carry q (L - b) = reset c
      · rw [if_pos hx, if_pos hy]
        exact ⟨fun _ => ⟨h1, h2⟩, fun _ => ⟨fun _ => hx, fun _ => hy⟩⟩
      · rw [if_pos hx, if_neg hy]
        constructor
        · rintro ⟨-, h⟩
          have : i ≠ b - 1 := fun e => hy (h e)
          omega
        · rintro ⟨-, h3⟩
          exact ⟨fun _ => hx, fun e => by omega⟩
      · rw [if_neg hx, if_pos hy]
        constructor
        · rintro ⟨h, -⟩
          have : i ≠ a := fun e => hx (h e)
          omega
        · rintro ⟨h3, -⟩
          exact ⟨fun e => by omega, fun _ => hy⟩
      · rw [if_neg hx, if_neg hy]
        constructor
        · rintro ⟨h, h'⟩
          have : i ≠ a := fun e => hx (h e)
          have : i ≠ b - 1 := fun e => hy (h' e)
          omega
        · rintro ⟨h3, h4⟩
          exact ⟨fun e => by omega, fun e => by omega⟩
    have exact : ∀ i, a ≤ i → i < b →
        (nextColumns q L i = c ↔
          (if carry q a = reset c then a else a + 1) ≤ i ∧
            i < (if carry q (L - b) = reset c then b else b - 1)) :=
      fun i h1 h2 => (key i h1 h2).trans (cond i h1 h2)
    refine ⟨exact, ?_, ?_⟩
    · intro hne
      refine ⟨hne, ?_, ?_, ?_, ?_⟩
      · rw [hnw]; split <;> omega
      · intro i h1 h2
        exact (exact i (by split at h1 <;> omega) (by split at h2 <;> omega)).2 ⟨h1, h2⟩
      · right
        by_cases hx : carry q a = reset c
        · -- the old low neighbour a-1 is a non-c column
          simp only [hx, if_true]
          have hz : q (a - 1) ≠ c := by rcases hleft with h | h <;> omega
          rw [em (a - 1) (by omega)]
          have hm : L - 1 - (a - 1) = L - a := by omega
          rw [hm, hcm (L - a) (by omega) (by omega)]
          apply neighbor_no_overflow c _ _ hc (hq18 _ (by omega)) hz (hcb _ (by omega))
          have : carry q a = (q (a - 1) + carry q (a - 1)) / 10 := carry_pred q a (by omega)
          rw [← this]; exact hx
        · simp only [hx, if_false]
          simp only [hx, if_false] at hne
          have := (exact (a + 1 - 1) (by omega) (by omega))
          intro hcon
          have hm : a + 1 - 1 = a := by omega
          rw [hm] at this hcon
          have h5 := (this.1 hcon).1
          rw [if_neg hx] at h5
          omega
      · right
        by_cases hy : carry q (L - b) = reset c
        · simp only [hy, if_true]
          have hz : q b ≠ c := by rcases hright with h | h <;> omega
          rw [em b hbL', hcr b (by omega) (by omega)]
          have hsb : q (L - 1 - b) = q b := by
            have := hs (L - 1 - b) (by omega)
            have hm : L - 1 - (L - 1 - b) = b := by omega
            rw [hm] at this; exact this
          have hout : (q b + carry q (L - 1 - b)) / 10 = reset c := by
            have : carry q (L - b) = (q (L - 1 - b) + carry q (L - 1 - b)) / 10 := by
              have hm : L - b - 1 = L - 1 - b := by omega
              rw [carry_pred q (L - b) (by omega), hm]
            rw [← hsb, ← this]; exact hy
          have := neighbor_no_overflow c _ _ hc (hq18 b hbL') hz (hcb (L - 1 - b) (by omega)) hout
          omega
        · simp only [hy, if_false]
          simp only [hy, if_false] at hne
          intro hcon
          have := (exact (b - 1) (by split at hne <;> omega) (by omega)).1 hcon
          simp [hy] at this
    · refine ⟨by split <;> omega, by split <;> omega, ?_⟩
      rw [h0]; split <;> split <;> omega
  · -- overflow
    have h1 : carry q L = 1 := by omega
    have hd : descendant q L c a b = (a + 1, b) := by simp [descendant, h0]
    rw [hd]
    dsimp only
    have hnw : nextWidth q L = L + 1 := by simp [nextWidth, h0]
    -- the low endpoint is lost
    have lowlost : nextColumns q L a ≠ c := by
      rcases Nat.eq_zero_or_pos a with hz | hz
      · subst hz
        rw [next_overflow_zero q L ha h1, hrun 0 (Nat.le_refl 0) hab]
        rcases hc with rfl | rfl <;> decide
      · have hz' : q (a - 1) ≠ c := by rcases hleft with h | h <;> omega
        rw [next_overflow_pos q L a ha h1 hz (by omega), hrun a (Nat.le_refl a) hab]
        have hsym : q (L - a) = q (a - 1) := by
          have := hs (L - a) (by omega)
          have hm : L - 1 - (L - a) = a - 1 := by omega
          rw [hm] at this; exact this
        have hca : carry q a = (q (a - 1) + carry q (a - 1)) / 10 := carry_pred q a (by omega)
        rw [hca, hcm (L - a) (by omega) (by omega)]
        exact neighbor_overflow c _ _ hc (hq18 _ (by omega)) hz' (hcb _ (by omega))
    have inner : ∀ i, a < i → i < b → nextColumns q L i = c := by
      intro i h1' h2
      rw [next_overflow_pos q L i ha h1 (by omega) (by omega), hrun i (by omega) h2,
        hrun (i - 1) (by omega) (by omega), hcr i h1' (by omega),
        hcm (L - i) (by omega) (by omega)]
      exact run_value c hc
    have exact : ∀ i, a ≤ i → i < b → (nextColumns q L i = c ↔ a + 1 ≤ i ∧ i < b) := by
      intro i h1' h2
      by_cases hia : i = a
      · subst hia; constructor
        · intro h; exact absurd h lowlost
        · intro h; omega
      · constructor
        · intro _; omega
        · intro _; exact inner i (by omega) h2
    refine ⟨exact, ?_, ?_⟩
    · intro hne
      refine ⟨hne, by rw [hnw]; omega, fun i h1' h2 => inner i (by omega) h2, ?_, ?_⟩
      · right
        have hm : a + 1 - 1 = a := by omega
        rw [hm]; exact lowlost
      · right
        rcases Nat.lt_or_ge b L with hbl | hbl
        · have hz : q b ≠ c := by rcases hright with h | h <;> omega
          rw [next_overflow_pos q L b ha h1 (by omega) hbl, hrun (b - 1) (by omega) (by omega),
            hcr b (by omega) (Nat.le_refl b)]
          have hsb : q (L - b - 1) = q b := by
            have := hs (L - b - 1) (by omega)
            have hm : L - 1 - (L - b - 1) = b := by omega
            rw [hm] at this; exact this
          have hcb' : carry q (L - b) = (q (L - b - 1) + carry q (L - b - 1)) / 10 :=
            carry_pred q (L - b) (by omega)
          rw [hcb', hsb]
          have := neighbor_overflow c _ _ hc (hq18 b hbl) hz (hcb (L - b - 1) (by omega))
          omega
        · have hbE : b = L := by omega
          rw [hbE, next_overflow_top q L ha h1]
          have hq : q (L - 1) = c := hrun (L - 1) (by omega) (by omega)
          have h00 := hs 0 hL
          simp only [Nat.sub_zero] at h00
          rw [h00, hq]
          rcases hc with rfl | rfl <;> decide
    · refine ⟨by omega, Nat.le_refl b, ?_⟩
      rw [h1]; omega

end RunAncestry

#print axioms RunAncestry.descendant_step
