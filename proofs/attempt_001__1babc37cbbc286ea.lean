import LychrelDigitSums

/-!
An actual full-width one-step family exhibiting new coefficient-18 births.
For every g >= 2, (1,10,8),18^g,(8,10,1) has the exact no-overflow
successor (3,0,18,17),18^(g-2),(17,18,0,3).  The old core shortens by
two and two new singleton 18 runs are born outside its 17 barriers.
Indices are least-significant first.  This is a one-step statement;
no repeated regeneration or infinite nonpalindromic orbit is asserted.
-/

namespace RunBirths.BirthFamily

open DecimalDigits FoldedDecimal

def width (g : Nat) : Nat := g + 6

/-- The entire source word, with zero irrelevant tail. -/
def source (g i : Nat) : Nat :=
  if i = 0 ∨ i = g + 5 then 1
  else if i = 1 ∨ i = g + 4 then 10
  else if i = 2 ∨ i = g + 3 then 8
  else if 3 ≤ i ∧ i < g + 3 then 18 else 0

/-- Explicit actual incoming carry, to be checked against the recursive carry. -/
def incoming (g i : Nat) : Nat :=
  if i = 2 ∨ (4 ≤ i ∧ i ≤ g + 3) ∨ i = g + 5 then 1 else 0

/-- The decimal result digits after normalizing the source columns. -/
def normalized (g i : Nat) : Nat :=
  if i = 0 then 1
  else if i = 2 ∨ (4 ≤ i ∧ i ≤ g + 3) then 9
  else if i = 3 then 8
  else if i = g + 5 then 2 else 0

/-- Full successor word, including the empty residual core when g=2. -/
def target (g i : Nat) : Nat :=
  if i = 0 ∨ i = g + 5 then 3
  else if i = 2 ∨ i = g + 3 ∨ (4 ≤ i ∧ i < g + 2) then 18
  else if i = 3 ∨ i = g + 2 then 17 else 0

theorem source_bounded (g i : Nat) : source g i ≤ 18 := by
  unfold source
  repeat first | omega | split

theorem normalized_bounded (g i : Nat) : normalized g i ≤ 9 := by
  unfold normalized
  repeat first | omega | split

theorem incoming_zero (g : Nat) : incoming g 0 = 0 := by
  unfold incoming
  split <;> omega

theorem incoming_terminal (g : Nat) : incoming g (width g) = 0 := by
  unfold incoming width
  split <;> omega

set_option maxHeartbeats 1000000 in
theorem exact_column_equation (g i : Nat) (hg : 2 ≤ g) :
    normalized g i + 10 * incoming g (i + 1) = source g i + incoming g i := by
  have hcases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨
      (4 ≤ i ∧ i < g + 3) ∨ i = g + 3 ∨ i = g + 4 ∨ i = g + 5 ∨ g + 6 ≤ i := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [normalized, incoming, source]
  all_goals (repeat first | omega | split)

theorem actual_carry (g i : Nat) (hg : 2 ≤ g) :
    carry (source g) i = incoming g i := by
  induction i with
  | zero => exact (incoming_zero g).symm
  | succ i ih =>
    have he := exact_column_equation g i hg
    have hd := normalized_bounded g i
    simp only [carry, ih]
    omega

theorem actual_output (g i : Nat) (hg : 2 ≤ g) :
    output (source g) i = normalized g i := by
  have he := exact_column_equation g i hg
  have hd := normalized_bounded g i
  simp only [output, actual_carry g i hg]
  omega

theorem no_overflow (g : Nat) (hg : 2 ≤ g) :
    carry (source g) (width g) = 0 := by
  rw [actual_carry g _ hg, incoming_terminal]

theorem actual_width (g : Nat) (hg : 2 ≤ g) :
    nextWidth (source g) (width g) = width g := by
  simp only [nextWidth, no_overflow g hg, if_true]

theorem source_symmetric (g i : Nat) (hi : i < width g) :
    source g i = source g (width g - 1 - i) := by
  let j := width g - 1 - i
  have hj : j = g + 5 - i := by simp [j, width]
  have hib : i < g + 6 := hi
  have h1 : (i = 0 ∨ i = g + 5) ↔ (j = 0 ∨ j = g + 5) := by omega
  have h10 : (i = 1 ∨ i = g + 4) ↔ (j = 1 ∨ j = g + 4) := by omega
  have h8 : (i = 2 ∨ i = g + 3) ↔ (j = 2 ∨ j = g + 3) := by omega
  have h18 : (3 ≤ i ∧ i < g + 3) ↔ (3 ≤ j ∧ j < g + 3) := by omega
  change source g i = source g j
  simp only [source, h1, h10, h8, h18]

theorem source_core (g i : Nat) (hlo : 3 ≤ i) (hhi : i < g + 3) :
    source g i = 18 := by
  simp (disch := omega) [source]

theorem source_admissible (g : Nat) (hg : 2 ≤ g) :
    Admissible (width g) (source g) := by
  refine ⟨by unfold width; omega, by simp [source],
    (fun i _ => source_bounded g i), source_symmetric g, ?_⟩
  intro i hi heq
  have hlo : 3 ≤ i := by unfold width at hi heq; omega
  have hhi : i < g + 3 := by unfold width at hi heq; omega
  rw [source_core g i hlo hhi]

set_option maxHeartbeats 1000000 in
theorem exact_pair_equation (g i : Nat) (hg : 2 ≤ g) (hi : i < width g) :
    columnSum (normalized g) (width g) i = target g i := by
  have hib : i < g + 6 := hi
  have hcases : i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨
      (4 ≤ i ∧ i < g + 2) ∨ i = g + 2 ∨ i = g + 3 ∨ i = g + 4 ∨ i = g + 5 := by omega
  rcases hcases with h | h | h | h | h | h | h | h | h
  all_goals (try subst i)
  all_goals simp (disch := omega) [columnSum, reflected, normalized, target, width]
  all_goals (repeat first | omega | split)

/-- The exact update uses the real recursive carry and its actual final branch. -/
theorem actual_update (g i : Nat) (hg : 2 ≤ g) (hi : i < width g) :
    nextColumns (source g) (width g) i = target g i := by
  simp only [nextColumns, no_overflow g hg, if_true, columnSum, reflected,
    actual_output g _ hg]
  exact exact_pair_equation g i hg hi

theorem target_admissible (g : Nat) (hg : 2 ≤ g) :
    Admissible (width g) (target g) := by
  have ha := NormalizationBridge.admissible_next (source g) (width g) (source_admissible g hg)
  rw [actual_width g hg] at ha
  exact NormalizationBridge.admissible_congr _ _ _ ha (fun i hi => actual_update g i hg hi)

/-- Exact predecessor and successor positions of the two genuinely new 18s. -/
theorem two_new_births (g : Nat) (hg : 2 ≤ g) :
    source g 2 = 8 ∧ source g (g + 3) = 8 ∧
    nextColumns (source g) (width g) 2 = 18 ∧
    nextColumns (source g) (width g) (g + 3) = 18 := by
  rw [actual_update g 2 hg (by unfold width; omega),
    actual_update g (g + 3) hg (by unfold width; omega)]
  simp (disch := omega) [source, target]

/-- The residual old core consists exactly of g-2 consecutive 18 columns. -/
theorem residual_core (g i : Nat) (hg : 2 ≤ g) (hlo : 4 ≤ i) (hhi : i < g + 2) :
    source g i = 18 ∧ nextColumns (source g) (width g) i = 18 := by
  rw [actual_update g i hg (by unfold width; omega)]
  simp (disch := omega) [source, target]

/-- The two old endpoints become 17; the two new births are singleton runs. -/
theorem barriers_and_singletons (g : Nat) (hg : 2 ≤ g) :
    source g 3 = 18 ∧ source g (g + 2) = 18 ∧
    nextColumns (source g) (width g) 1 = 0 ∧
    nextColumns (source g) (width g) 3 = 17 ∧
    nextColumns (source g) (width g) (g + 2) = 17 ∧
    nextColumns (source g) (width g) (g + 4) = 0 := by
  rw [actual_update g 1 hg (by unfold width; omega),
    actual_update g 3 hg (by unfold width; omega),
    actual_update g (g + 2) hg (by unfold width; omega),
    actual_update g (g + 4) hg (by unfold width; omega)]
  simp (disch := omega) [source, target]

theorem core_lengths (g : Nat) (hg : 2 ≤ g) :
    (g + 3) - 3 = g ∧ (g + 2) - 4 = g - 2 ∧ (g - 2) + 2 = g := by omega

/-- Full classification, so there are no unlisted coefficient-18 positions. -/
theorem exact_18_positions (g i : Nat) (hg : 2 ≤ g) (hi : i < width g) :
    (source g i = 18 ↔ 3 ≤ i ∧ i < g + 3) ∧
    (nextColumns (source g) (width g) i = 18 ↔
      i = 2 ∨ i = g + 3 ∨ (4 ≤ i ∧ i < g + 2)) := by
  rw [actual_update g i hg hi]
  constructor
  · unfold source
    repeat first | omega | split
  · unfold target
    repeat first | omega | split


/-- A coefficient 18 and the exterior coefficient 1 exclude both bad patterns. -/
theorem source_not_bad (g : Nat) (hg : 2 ≤ g) :
    ¬ BadWord (width g) (source g) := by
  rintro (hlo | ⟨hout, _⟩)
  · have h := hlo 3 (by unfold width; omega)
    rw [source_core g 3 (by omega) (by omega)] at h
    omega
  · simp [source] at hout

/-- The newly born 18 at position 2 supplies finite safety for the target. -/
theorem target_not_bad (g : Nat) (hg : 2 ≤ g) :
    ¬ BadWord (width g) (target g) := by
  rintro (hlo | ⟨hout, _⟩)
  · have h := hlo 2 (by unfold width; omega)
    simp (disch := omega) [target] at h
  · simp [target] at hout

theorem source_value_normalized (g : Nat) (hg : 2 ≤ g) :
    value (source g) (width g) = value (normalized g) (width g) := by
  have hv := value_output (source g) (width g)
  rw [no_overflow g hg] at hv
  simp only [Nat.zero_mul, Nat.add_zero] at hv
  exact hv.symm.trans (value_congr _ _ _ (fun i _ => actual_output g i hg))

theorem normalized_leading (g : Nat) (hg : 2 ≤ g) :
    normalized g (width g - 1) = 2 := by
  simp (disch := omega) [normalized, width]

/-- Every ordinary decimal realization has these exact canonical next digits. -/
theorem numeric_canonical_next (g n : Nat) (d : Nat → Nat) (hg : 2 ≤ g)
    (hc : Canonical n d (width g))
    (hr : ∀ i, i < width g → columnSum d (width g) i = source g i) :
    Canonical (Lychrel196.step n) (normalized g) (width g) := by
  refine ⟨by unfold width; omega, (fun i _ => normalized_bounded g i), ?_, ?_⟩
  · rw [normalized_leading g hg]
    decide
  · exact ((step_eq_word_value n d (source g) (width g) hc hr).trans
      (source_value_normalized g hg)).symm

private theorem numeric_safe (n L : Nat) (d q : Nat → Nat)
    (hc : Canonical n d L)
    (hr : ∀ i, i < L → columnSum d L i = q i)
    (hb : ¬ BadWord L q) : ¬ Lychrel196.Palindrome (Lychrel196.step n) := by
  intro hp
  rw [← hc.2.2.2] at hp
  have h := (step_palindrome_iff d L hc.1 hc.2.1 hc.2.2.1).mp hp
  apply hb
  rcases h with hlo | ⟨hout, hex⟩
  · exact Or.inl (fun i hi => by simpa only [hr i hi] using hlo i hi)
  · refine Or.inr ⟨?_, ?_⟩
    · simpa only [hr 0 hc.1] using hout
    · intro i hi
      simpa only [hr i hi] using hex i hi

/-- Exactly finite safety: the input and its first two numeric successors. -/
theorem numeric_two_steps_safe (g n : Nat) (d : Nat → Nat) (hg : 2 ≤ g)
    (hc : Canonical n d (width g))
    (hr : ∀ i, i < width g → columnSum d (width g) i = source g i) :
    ¬ Lychrel196.Palindrome n ∧ ¬ Lychrel196.Palindrome (Lychrel196.step n) ∧
    ¬ Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  refine ⟨?_, numeric_safe n (width g) d (source g) hc hr (source_not_bad g hg), ?_⟩
  · intro hp
    rw [← hc.2.2.2] at hp
    have hs := (palindrome_value_iff d (width g) hc.2.1 (Or.inr hc.2.2.1)).mp hp 0 hc.1
    have hq := hr 0 hc.1
    simp only [columnSum, reflected, Nat.sub_zero] at hq hs
    simp only [source, true_or, if_true] at hq
    omega
  · exact numeric_safe (Lychrel196.step n) (width g) (normalized g) (target g)
      (numeric_canonical_next g n d hg hc hr)
      (fun i hi => exact_pair_equation g i hg hi) (target_not_bad g hg)

/-- Every g >= 2 is an actual positive decimal instance of this one-step family. -/
theorem family_realized (g : Nat) (hg : 2 ≤ g) :
    ∃ n d, 0 < n ∧ Canonical n d (width g) ∧
      (∀ i, i < width g → columnSum d (width g) i = source g i) ∧
      Canonical (Lychrel196.step n) (normalized g) (width g) ∧
      ¬ Lychrel196.Palindrome n ∧ ¬ Lychrel196.Palindrome (Lychrel196.step n) ∧
      ¬ Lychrel196.Palindrome (Lychrel196.step (Lychrel196.step n)) := by
  obtain ⟨hL, ho, hb, hs, hm⟩ := source_admissible g hg
  obtain ⟨n, d, hp, hc, hr⟩ := valid_word_realizable (source g) (width g) hL ho hb hs hm
  exact ⟨n, d, hp, hc, hr, numeric_canonical_next g n d hg hc hr,
    numeric_two_steps_safe g n d hg hc hr⟩

#print axioms source_bounded
#print axioms normalized_bounded
#print axioms incoming_zero
#print axioms incoming_terminal
#print axioms exact_column_equation
#print axioms actual_carry
#print axioms actual_output
#print axioms no_overflow
#print axioms actual_width
#print axioms source_symmetric
#print axioms source_core
#print axioms source_admissible
#print axioms exact_pair_equation
#print axioms actual_update
#print axioms target_admissible
#print axioms two_new_births
#print axioms residual_core
#print axioms barriers_and_singletons
#print axioms core_lengths
#print axioms exact_18_positions
#print axioms source_not_bad
#print axioms target_not_bad
#print axioms source_value_normalized
#print axioms normalized_leading
#print axioms numeric_canonical_next
#print axioms numeric_two_steps_safe
#print axioms family_realized

end RunBirths.BirthFamily
