import P196.CertificateInterface208.InterfaceRanks

namespace Agent208.Interface
open Agent109 Agent109.Cert

theorem short_word_code (A : Word) (hA : Bounded A) (hlen : A.length ≤ 2) :
    wordCode A < 381 ∧ decodeWord (wordCode A) = A := by
  cases A with
  | nil => simp [wordCode, decodeWord]
  | cons a xs =>
    have ha : a ≤ 18 := hA a (by simp)
    cases xs with
    | nil =>
      constructor
      · simp only [wordCode]; omega
      · simp [wordCode, decodeWord, show a + 1 ≠ 0 by omega,
          show a + 1 < 20 by omega]
    | cons b ys =>
      have hb : b ≤ 18 := hA b (by simp)
      have hy : ys = [] := by
        have := hlen
        simp only [List.length_cons] at this
        have : ys.length = 0 := by omega
        exact List.length_eq_zero_iff.mp this
      subst ys
      constructor
      · simp only [wordCode]; omega
      · simp only [wordCode, decodeWord,
          show 20 + 19 * a + b ≠ 0 by omega,
          show ¬ 20 + 19 * a + b < 20 by omega, if_false]
        have hdiv : (20 + 19 * a + b - 20) / 19 = a := by omega
        have hmod : (20 + 19 * a + b - 20) % 19 = b := by omega
        rw [hdiv, hmod]

theorem even_phase_code (c : Nat) (hc : Phase c) (he : c % 2 = 0) :
    phaseCode c < 8 ∧ 2 * (phaseCode c + 1) = c := by
  unfold Phase at hc
  unfold phaseCode
  omega

theorem middle_of_trim (W A : Word) (c d j k : Nat)
    (h : W = List.replicate j c ++ A ++ List.replicate k d) :
    middle W j k = A := by
  have hlen : W.length - j - k = A.length := by
    rw [h]
    simp only [List.length_append, List.length_replicate]
    omega
  unfold middle
  rw [hlen, h]
  simp [List.drop_append, List.take_append]

/-- All bounded short-interface edges strictly decrease the checked rank. -/
theorem rank_decreases (c : Nat) (A A' : Word) (g j k : Nat)
    (hc : Phase c) (he : c % 2 = 0) (hA : Bounded A) (hlen : A.length ≤ 2)
    (hg : g ≤ 1) (hnextlen : A'.length ≤ 2)
    (htrim : raw c A g = List.replicate j (tOf c + tOf c) ++ A' ++
      List.replicate k (18 - (tOf c + tOf c))) :
    rank (tOf c + tOf c) A' < rank c A := by
  obtain ⟨hp, hpEq⟩ := even_phase_code c hc he
  obtain ⟨ha, haEq⟩ := short_word_code A hA hlen
  have hlenRaw := raw_length_le c A g
  have htrimlen := congrArg List.length htrim
  simp only [List.length_append, List.length_replicate] at htrimlen
  have hj : j < 5 := by omega
  have hk : k < 5 := by omega
  have h := List.all_eq_true.mp (phaseCheck_true (phaseCode c) hp)
    (wordCode A) (List.mem_range.mpr ha)
  change rowCheck (2 * (phaseCode c + 1)) (decodeWord (wordCode A)) = true at h
  rw [hpEq, haEq] at h
  have h1 := List.all_eq_true.mp h g (List.mem_range.mpr (by omega : g < 2))
  have h2 := List.all_eq_true.mp h1 j (List.mem_range.mpr hj)
  have h3 := List.all_eq_true.mp h2 k (List.mem_range.mpr hk)
  have hm := middle_of_trim _ A' _ _ j k htrim
  change edgeCheck c A g j k = true at h3
  simp only [edgeCheck] at h3
  rw [hm, if_pos ⟨htrim, hnextlen⟩] at h3
  exact of_decide_eq_true h3

end Agent208.Interface
#print axioms Agent208.Interface.rank_decreases
