import P196.Agent104ExactMass.ProfileDynamics

namespace DecimalProfile

open DecimalDigits DecimalMass DecimalZeroGap DecimalUnboundedMass

/-- A finite nonempty set of positive positions has a first position. -/
private theorem first_positive (q : Nat → Nat) (N : Nat)
    (hex : ∃ i, i < N ∧ 0 < q i) :
    ∃ i, i < N ∧ 0 < q i ∧ ∀ j, j < i → q j = 0 := by
  induction N with
  | zero => obtain ⟨i, hi, _⟩ := hex; omega
  | succ N ih =>
    by_cases hearlier : ∃ i, i < N ∧ 0 < q i
    · obtain ⟨i, hi, hp, hz⟩ := ih hearlier
      exact ⟨i, by omega, hp, hz⟩
    · have hp : 0 < q N := by
        obtain ⟨i, hi, hqi⟩ := hex
        by_cases he : i < N
        · exact False.elim (hearlier ⟨i, he, hqi⟩)
        · have hei : i = N := by omega
          simpa only [hei] using hqi
      refine ⟨N, by omega, hp, ?_⟩
      intro j hj
      by_cases hpj : 0 < q j
      · exact False.elim (hearlier ⟨j, hj, hpj⟩)
      · omega

/-- Positive endpoints remove both exterior zero-gap allowances. -/
theorem length_le_mass_gaps (q : Nat → Nat) (L K : Nat)
    (hL : 0 < L) (hleft : 0 < q 0) (hright : 0 < q (L-1))
    (hz : ZeroBound q L K) :
    L ≤ wordSum q L + (wordSum q L - 1) * K := by
  induction L using Nat.strongRecOn generalizing q with
  | ind L ih =>
    by_cases hsingle : L = 1
    · subst L
      simp only [wordSum, Nat.zero_add]
      omega
    · have hLtwo : 2 ≤ L := by omega
      have hex : ∃ j, j < L-1 ∧ 0 < (fun x => q (1+x)) j := by
        refine ⟨L-2, by omega, ?_⟩
        have he : 1+(L-2) = L-1 := by omega
        simpa only [he] using hright
      obtain ⟨j, hj, hpj, hzj⟩ := first_positive (fun x => q (1+x)) (L-1) hex
      let a := 1+j
      let R := L-a
      let r := fun i => q (a+i)
      have ha : 0 < a := by dsimp [a]; omega
      have haL : a < L := by dsimp [a]; omega
      have hR : 0 < R := by dsimp [R]; omega
      have hRL : R < L := by dsimp [R]; omega
      have hsplit : a+R = L := by dsimp [R]; omega
      have hrleft : 0 < r 0 := by simpa [r, a] using hpj
      have hrright : 0 < r (R-1) := by
        have he : a+(R-1) = L-1 := by omega
        simpa only [r, he] using hright
      have hgap : a ≤ K+1 := by
        by_cases hjzero : j = 0
        · dsimp [a]; omega
        · have hbound : j ≤ K := hz 1 j (by omega) (by omega) (by
            intro i hi hik
            have he : 1+(i-1) = i := by omega
            have h := hzj (i-1) (by omega)
            simpa only [he] using h)
          dsimp [a]
          omega
      have hrtail : ZeroBound r R K := by
        intro b k hk hbk hzero
        apply hz (a+b) k hk (by omega)
        intro i hilo hihi
        have he : a+(i-a) = i := by omega
        have h := hzero (i-a) (by omega) (by omega)
        simpa only [r, he] using h
      have hrec := ih R hRL r hR hrleft hrright hrtail
      have hmasssplit := wordSum_split q a R
      rw [hsplit] at hmasssplit
      have hprefix := wordSum_mono_length q 1 a (by omega)
      simp only [wordSum, Nat.zero_add] at hprefix
      have hm : wordSum r R + 1 ≤ wordSum q L := by
        change wordSum q L = wordSum q a + wordSum r R at hmasssplit
        omega
      have hrmass := wordSum_mono_length r 1 R (by omega)
      simp only [wordSum, Nat.zero_add] at hrmass
      have hmulid : (wordSum r R - 1)*K + K = wordSum r R*K := by
        calc
          (wordSum r R - 1)*K + K = (wordSum r R - 1 + 1)*K := by
            rw [Nat.add_mul, Nat.one_mul]
          _ = wordSum r R*K := by
            rw [Nat.sub_add_cancel (by omega : 1 ≤ wordSum r R)]
      have hmul := Nat.mul_le_mul_right K (by omega : wordSum r R ≤ wordSum q L - 1)
      omega

/-- The sharp support estimate using a mass ceiling. -/
theorem length_le_mass_zero_runs_sharp (q : Nat → Nat) (L M K : Nat)
    (hv : Valid L q) (hm : wordSum q L ≤ M) (hz : ZeroBound q L K) :
    L ≤ M + (M-1)*K := by
  have hh := length_le_mass_gaps q L K hv.1 hv.2.1 hv.2.2.2.2 hz
  have hmul := Nat.mul_le_mul_right K (by omega : wordSum q L - 1 ≤ M-1)
  omega

/-- The short-run exception needs only two; the mass argument needs one extra column. -/
theorem zeroBound_phi_sharp (q : Nat → Nat) (L M K : Nat)
    (ha : Valid L q) (hm : wordSum q L ≤ M)
    (hz : DecimalZeroGap.ZeroBound q L K) (hKsmall : 2 ≤ K)
    (hKmass : M + 1 ≤ K) :
    DecimalZeroGap.ZeroBound (phi q L) (nextLen q L) K := by
  intro a k hk hbound hzero
  by_cases hshort : k ≤ K
  · exact hshort
  have hlong : 3 ≤ k := by omega
  have hlast := phi_zero_index q L (a+k-1) ha (by omega)
    (hzero (a+k-1) (by omega) (by omega))
  have hb : a + k ≤ L := by omega
  by_cases hc : backCarry q L 0 = 0
  · have hboth : ∀ i, a ≤ i → i < a + k →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      exact phi_zero_no_overflow q L i hc (hzero i hia hik)
    rcases simultaneous_zero_interval q L a k ha (by omega) hb hboth with ho | hn
    · exact hz a k hk hb ho
    · have hmass := DecimalZeroGap.interval_length_le_mass q L a k hb
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega
  · have hout : ∀ i, a ≤ i → i < a + k →
        0 < i ∧ i < L ∧ output q i = 0 ∧ backOutput q L (i - 1) = 0 := by
      intro i hia hik
      exact phi_zero_overflow q L i ha hc (by omega) (hzero i hia hik)
    have hfirst := hout a (by omega) (by omega)
    have ha0 : 0 < a := hfirst.1
    have hcore : ∀ i, a ≤ i → i < a + (k - 1) →
        output q i = 0 ∧ backOutput q L i = 0 := by
      intro i hia hik
      have hr := (hout i hia (by omega)).2.2.1
      have hu := (hout (i + 1) (by omega) (by omega)).2.2.2
      exact ⟨hr, by simpa only [Nat.add_sub_cancel] using hu⟩
    rcases simultaneous_zero_interval q L a (k - 1) ha (by omega) (by omega) hcore
      with ho | hn
    · have hright : output q (a + (k - 1)) = 0 :=
        (hout (a + (k - 1)) (by omega) (by omega)).2.2.1
      have hext := zero_core_extends q L a (k - 1) ha ha0 (by omega)
        (by omega) ho hcore hfirst.2.2.2 hright
      have hold : k + 1 ≤ K := hz (a - 1) (k + 1) (by omega) (by omega)
        (fun i hia hik => hext i hia (by omega))
      omega
    · have hmass := DecimalZeroGap.interval_length_le_mass q L a (k - 1) (by omega)
        (fun i hia hik => by rw [hn i hia hik]; decide)
      omega

#print axioms length_le_mass_gaps
#print axioms length_le_mass_zero_runs_sharp
#print axioms zeroBound_phi_sharp

end DecimalProfile
