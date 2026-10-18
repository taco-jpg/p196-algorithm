import P196.Drafts.Agent108WindowWeightsB31b8818.WholeWord

namespace Agent13FoldedFamily
open DecimalDigits FoldedDecimal Lychrel196

/-- Pair-word safety is the original next-integer nonpalindromicity. -/
def WordSafe (L : Nat) (q : Nat → Nat) : Prop := Admissible L q ∧ ¬ Palindrome (value q L)

theorem central_input (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    inputWord e r k (halfWidth r k-1) = 18 := by
  have hi : halfWidth r k-1 < halfWidth r k := by unfold halfWidth; omega
  have h0 : halfWidth r k-1 ≠ 0 := by unfold halfWidth; omega
  have hg : ¬ halfWidth r k-1 < 4*r+1 := by unfold halfWidth; omega
  have he : halfWidth r k-1 ≠ 4*r+1 := by unfold halfWidth; omega
  rw [show inputWord e r k (halfWidth r k-1) = inputHalf e r (halfWidth r k-1) from reflect_low _ _ _ hi]
  simp [inputHalf,h0,hg,he]

theorem central_target (r k : Nat) (hk : 0 < k) :
    targetWord r k (halfWidth r k-1) = 18 := by
  have hi : halfWidth r k-1 < halfWidth r k := by unfold halfWidth; omega
  have h0 : halfWidth r k-1 ≠ 0 := by unfold halfWidth; omega
  have hg : ¬ halfWidth r k-1 ≤ 4*r+1 := by unfold halfWidth; omega
  rw [show targetWord r k (halfWidth r k-1) = targetHalf r (halfWidth r k-1) from reflect_low _ _ _ hi]
  simp [targetHalf,h0,hg]

theorem eighteen_not_bad (q : Nat → Nat) (L j : Nat) (hj : j < L) (h18 : q j = 18) :
    ¬ BadWord L q := by
  intro h
  rcases h with h | h
  · have hh := h j hj; omega
  · have hh := h.2 j hj; omega

/-- The original predecessor classification transfers to encoded admissible words. -/
theorem admissible_safe (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hs : ¬ BadWord L q) : WordSafe L q := by
  refine ⟨ha, ?_⟩
  obtain ⟨n,d,hn,hcan,hrep⟩ := valid_word_realizable q L ha.1 ha.2.1 ha.2.2.1 ha.2.2.2.1 ha.2.2.2.2
  intro hp
  have hstep : step n = value q L := step_eq_word_value n d q L hcan hrep
  rw [← hstep, ← hcan.2.2.2] at hp
  have hb := (step_palindrome_iff d L hcan.1 hcan.2.1 hcan.2.2.1).mp hp
  apply hs
  rcases hb with hb | hb
  · exact Or.inl (fun i hi => by rw [← hrep i hi]; exact hb i hi)
  · refine Or.inr ⟨?_,fun i hi => ?_⟩
    · rw [← hrep 0 hcan.1]; exact hb.1
    · rw [← hrep i hi]; exact hb.2 i hi

theorem binary_family_safe (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    WordSafe (2*halfWidth r k) (inputWord e r k) ∧
    WordSafe (2*halfWidth r k) (targetWord r k) := by
  have hi : halfWidth r k-1 < 2*halfWidth r k := by unfold halfWidth; omega
  exact ⟨admissible_safe _ _ (input_admissible e r k)
      (eighteen_not_bad _ _ _ hi (central_input e r k hk)),
    admissible_safe _ _ (target_admissible r k)
      (eighteen_not_bad _ _ _ hi (central_target r k hk))⟩

/-- An odd outer pair sum excludes initial palindromicity of every realization. -/
theorem realization_nonpalindrome (q : Nat → Nat) (L n : Nat) (d : Nat → Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hodd : q 0 % 2 = 1) : ¬ Palindrome n := by
  intro hp
  rw [← hc.2.2.2] at hp
  have hs := (palindrome_value_iff d L hc.2.1 (Or.inr hc.2.2.1)).mp hp
  have hz := hs 0 hc.1
  have hq := hrep 0 hc.1
  simp only [columnSum,reflected,Nat.sub_zero] at hq
  simp only [Nat.sub_zero] at hz
  omega

theorem input_outer (e : Nat → Bool) (r k : Nat) : inputWord e r k 0 = 5 := by
  simp [inputWord,reflectHalf,halfWidth,inputHalf]

theorem target_outer (r k : Nat) : targetWord r k 0 = 11 := by
  simp [targetWord,reflectHalf,halfWidth,targetHalf]

theorem binary_family_initial_nonpalindrome (e : Nat → Bool) (r k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (2*halfWidth r k))
    (hrep : ∀ i, i < 2*halfWidth r k → columnSum d (2*halfWidth r k) i = inputWord e r k i) :
    ¬ Palindrome n := by
  apply realization_nonpalindrome _ _ _ _ hc hrep
  rw [input_outer]

theorem target_initial_nonpalindrome (r k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (2*halfWidth r k))
    (hrep : ∀ i, i < 2*halfWidth r k → columnSum d (2*halfWidth r k) i = targetWord r k i) :
    ¬ Palindrome n := by
  apply realization_nonpalindrome _ _ _ _ hc hrep
  rw [target_outer]

/-- A complete actual arithmetic endpoint, including both successive safe words. -/
theorem binary_family_safe_realization (e : Nat → Bool) (r k : Nat) (hk : 0 < k) :
    ∃ n d d', 0 < n ∧ Canonical n d (2*halfWidth r k) ∧
      (∀ i, i < 2*halfWidth r k → columnSum d (2*halfWidth r k) i = inputWord e r k i) ∧
      Canonical (step n) d' (2*halfWidth r k) ∧
      (∀ i, i < 2*halfWidth r k → columnSum d' (2*halfWidth r k) i = targetWord r k i) ∧
      ¬ Palindrome n ∧ ¬ Palindrome (step n) ∧ ¬ Palindrome (step (step n)) := by
  obtain ⟨n,d,hn,hcan,hrep,hstep,d',hc',hr'⟩ := binary_family_realization e r k hk
  have hs := binary_family_safe e r k hk
  refine ⟨n,d,d',hn,hcan,hrep,hc',hr',binary_family_initial_nonpalindrome e r k n d hcan hrep,?_,?_⟩
  · rw [hstep]; exact hs.1.2
  · rw [step_eq_word_value _ _ _ _ hc' hr']; exact hs.2.2

end Agent13FoldedFamily
