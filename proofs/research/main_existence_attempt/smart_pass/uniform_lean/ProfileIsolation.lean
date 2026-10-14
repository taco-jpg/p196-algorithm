import ProfileDynamics

/-! Exact carry isolation across a genuine zero gap. -/

namespace DecimalProfile

open DecimalDigits DecimalMass FoldedDecimal

theorem carry_zero_prefix (q : Nat → Nat) (D : Nat)
    (hz : ∀ i, i < D → q i = 0) :
    ∀ i, i ≤ D → carry q i = 0 := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    simp only [carry, hz i (by omega), ih (by omega)]

theorem output_zero_prefix (q : Nat → Nat) (D i : Nat)
    (hz : ∀ j, j < D → q j = 0) (hi : i < D) : output q i = 0 := by
  simp only [output, hz i hi, carry_zero_prefix q D hz i (by omega)]

theorem carry_zero_tail (q : Nat → Nat) (A : Nat)
    (hq : ∀ i, q i ≤ 18) (hz : ∀ i, A ≤ i → q i = 0) :
    ∀ i, A + 1 ≤ i → carry q i = 0 := by
  intro i
  induction i with
  | zero => intro hi; omega
  | succ i ih =>
    intro hi
    have hqi := hz i (by omega)
    have hci := carry_bounded q i (fun j _ => hq j) i (by omega)
    simp only [carry, hqi]
    omega

theorem output_zero_tail (q : Nat → Nat) (A i : Nat)
    (hq : ∀ j, q j ≤ 18) (hz : ∀ j, A ≤ j → q j = 0)
    (hi : A + 1 ≤ i) : output q i = 0 := by
  simp only [output, hz i (by omega), carry_zero_tail q A hq hz i hi]

/-- With a zero column between the supports, the forward normalization
of the sum is the sum of the two independently computed normalizations. -/
theorem forward_separated (p v : Nat → Nat) (A D : Nat)
    (hp : ∀ i, p i ≤ 18) (hv : ∀ i, v i ≤ 18)
    (hpz : ∀ i, A ≤ i → p i = 0)
    (hvz : ∀ i, i < D → v i = 0) (hgap : A < D) :
    (∀ i, carry (fun j => p j + v j) i = carry p i + carry v i) ∧
    (∀ i, output (fun j => p j + v j) i = output p i + output v i) := by
  have hc : ∀ i, carry (fun j => p j + v j) i = carry p i + carry v i := by
    intro i
    induction i with
    | zero => rfl
    | succ i ih =>
      by_cases hi : i < D
      · have hzv := hvz i hi
        have hcv := carry_zero_prefix v D hvz i (by omega)
        simp only [carry, ih, hzv, hcv, Nat.add_zero, Nat.zero_add]
        omega
      · have hzp := hpz i (by omega)
        have hcp := carry_zero_tail p A hp hpz i (by omega)
        simp only [carry, ih, hzp, hcp, Nat.add_zero, Nat.zero_add]
        omega
  refine ⟨hc, ?_⟩
  intro i
  by_cases hi : i < D
  · have hzv := hvz i hi
    have hcv := carry_zero_prefix v D hvz i (by omega)
    simp only [output, hc, hzv, hcv, Nat.add_zero, Nat.zero_add]
    omega
  · have hzp := hpz i (by omega)
    have hcp := carry_zero_tail p A hp hpz i (by omega)
    simp only [output, hc, hzp, hcp, Nat.add_zero, Nat.zero_add]
    omega

theorem reflect_add (p v : Nat → Nat) (L i : Nat) :
    reflect (fun j => p j + v j) L i = reflect p L i + reflect v L i := by
  unfold reflect
  split <;> simp_all

/-- Backward normalization also splits; it is not a reflected *forward*
carry of the original word and does not assume symmetry. -/
theorem backward_separated (p v : Nat → Nat) (L A D : Nat)
    (hp : ∀ i, p i ≤ 18) (hv : ∀ i, v i ≤ 18)
    (hpz : ∀ i, A ≤ i → p i = 0)
    (hvz : ∀ i, i < D → v i = 0) (hgap : A < D) (hDL : D ≤ L) :
    (∀ i, backCarry (fun j => p j + v j) L i =
      backCarry p L i + backCarry v L i) ∧
    (∀ i, backOutput (fun j => p j + v j) L i =
      backOutput p L i + backOutput v L i) := by
  have hrv : ∀ i, L - D ≤ i → reflect v L i = 0 := by
    intro i hi
    unfold reflect
    split
    · exact hvz _ (by omega)
    · rfl
  have hrp : ∀ i, i < L - A → reflect p L i = 0 := by
    intro i hi
    unfold reflect
    split
    · exact hpz _ (by omega)
    · rfl
  have hsep := forward_separated (reflect v L) (reflect p L) (L-D) (L-A)
    (reflect_bounded v L hv) (reflect_bounded p L hp) hrv hrp (by omega)
  have he : reflect (fun j => p j + v j) L =
      fun j => reflect v L j + reflect p L j := by
    funext i
    rw [reflect_add]
    omega
  constructor
  · intro i
    unfold backCarry
    rw [he, hsep.1]
    omega
  · intro i
    unfold backOutput
    split
    · rw [he, hsep.2]
      omega
    · omega

theorem backward_zero_prefix (q : Nat → Nat) (L D : Nat)
    (hq : ∀ i, q i ≤ 18) (hz : ∀ i, i < D → q i = 0) (hDL : D ≤ L) :
    (∀ i, i + 1 < D → backOutput q L i = 0) ∧
    (∀ i, i < D → backCarry q L i = 0) := by
  have htail : ∀ i, L-D ≤ i → reflect q L i = 0 := by
    intro i hi
    unfold reflect
    split
    · exact hz _ (by omega)
    · rfl
  constructor
  · intro i hi
    unfold backOutput
    have hil : i < L := by omega
    simp only [hil, if_true]
    exact output_zero_tail (reflect q L) (L-D) (L-1-i)
      (reflect_bounded q L hq) htail (by omega)
  · intro i hi
    exact carry_zero_tail (reflect q L) (L-D) (reflect_bounded q L hq)
      htail (L-i) (by omega)

/-- Concrete one-step splitting at a zero gap.  The boundary digit belongs
only to the anchored left component. -/
theorem phi_separated (p v : Nat → Nat) (L A D : Nat)
    (hp : ∀ i, p i ≤ 18) (hv : ∀ i, v i ≤ 18)
    (hpz : ∀ i, A ≤ i → p i = 0)
    (hvz : ∀ i, i < D → v i = 0) (hgap : A < D) (hDL : D ≤ L) :
    (backCarry (fun j => p j + v j) L 0 = backCarry p L 0) ∧
    (∀ i, phi (fun j => p j + v j) L i =
      phi p L i + bulk v L (backCarry p L 0) i) := by
  have hf := forward_separated p v A D hp hv hpz hvz hgap
  have hb := backward_separated p v L A D hp hv hpz hvz hgap hDL
  have hv0 := (backward_zero_prefix v L D hv hvz hDL).2 0 (by omega)
  have hh : backCarry (fun j => p j + v j) L 0 = backCarry p L 0 := by
    rw [hb.1, hv0, Nat.add_zero]
  refine ⟨hh, ?_⟩
  intro i
  unfold phi bulk
  rw [hh]
  by_cases hc : backCarry p L 0 = 0
  · simp only [hc, if_true, hf.2, hb.2]
    omega
  · simp only [hc, if_false]
    by_cases hi : i = 0
    · subst i
      have hrv := output_zero_prefix v D 0 hvz (by omega)
      simp only [if_true, hf.2, hrv, Nat.add_zero]
    · simp only [hi, if_false, hf.2, hb.2]
      omega

theorem backward_carry_step (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    backCarry q L i = (q i + backCarry q L (i+1)) / 10 := by
  have he := back_column_equation q L i hi
  have hb := backOutput_bounded q L i
  omega

theorem backward_digit_formula (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    backOutput q L i = (q i + backCarry q L (i+1)) % 10 := by
  have he := back_column_equation q L i hi
  have hb := backOutput_bounded q L i
  omega

theorem backward_zero_tail (q : Nat → Nat) (L A : Nat)
    (hz : ∀ i, A ≤ i → q i = 0) (hAL : A ≤ L) :
    (∀ i, A ≤ i → backCarry q L i = 0) ∧
    (∀ i, A ≤ i → backOutput q L i = 0) := by
  have hpre : ∀ i, i < L-A → reflect q L i = 0 := by
    intro i hi
    unfold reflect
    split
    · exact hz _ (by omega)
    · rfl
  constructor
  · intro i hi
    exact carry_zero_prefix (reflect q L) (L-A) hpre (L-i) (by omega)
  · intro i hi
    by_cases hil : i < L
    · unfold backOutput
      simp only [hil, if_true]
      exact output_zero_prefix (reflect q L) (L-A) (L-1-i) hpre (by omega)
    · exact backOutput_tail q L i (by omega)

/-- Padding by additional zeros cannot change a backward normalization. -/
theorem backward_padding (q : Nat → Nat) (A L : Nat)
    (hz : ∀ i, A ≤ i → q i = 0) (hAL : A ≤ L) :
    (∀ i, backCarry q L i = backCarry q A i) ∧
    (∀ i, backOutput q L i = backOutput q A i) := by
  have htL := backward_zero_tail q L A hz hAL
  have htA := backward_zero_tail q A A hz (Nat.le_refl _)
  have hc : ∀ j, j ≤ A → backCarry q L (A-j) = backCarry q A (A-j) := by
    intro j
    induction j with
    | zero =>
      intro _
      simp only [Nat.sub_zero, htL.1 A (by omega), htA.1 A (by omega)]
    | succ j ih =>
      intro hj
      have hidx : A-(j+1)+1=A-j := by omega
      rw [backward_carry_step q L (A-(j+1)) (by omega),
        backward_carry_step q A (A-(j+1)) (by omega), hidx, ih (by omega)]
  have hcall : ∀ i, backCarry q L i = backCarry q A i := by
    intro i
    by_cases hi : i ≤ A
    · have hh := hc (A-i) (by omega)
      have he : A-(A-i)=i := by omega
      simpa only [he] using hh
    · rw [htL.1 i (by omega), htA.1 i (by omega)]
  refine ⟨hcall, ?_⟩
  intro i
  by_cases hi : i < A
  · rw [backward_digit_formula q L i (by omega), backward_digit_formula q A i hi,
      hcall]
  · rw [htL.2 i (by omega), htA.2 i (by omega)]

theorem phi_padding (q : Nat → Nat) (A L : Nat)
    (hz : ∀ i, A ≤ i → q i = 0) (hAL : A ≤ L) :
    ∀ i, phi q L i = phi q A i := by
  have hh := backward_padding q A L hz hAL
  intro i
  simp only [phi, hh.1, hh.2]

theorem bulk_bounded (q : Nat → Nat) (L h i : Nat) : bulk q L h i ≤ 18 := by
  have hr := output_bounded q i
  have hu := backOutput_bounded q L i
  have hv := backOutput_bounded q L (i-1)
  unfold bulk
  split
  · omega
  · split <;> omega

/-- The front of a detached component moves left by at most one column. -/
theorem bulk_zero_prefix (q : Nat → Nat) (L D h : Nat)
    (hq : ∀ i, q i ≤ 18) (hz : ∀ i, i < D → q i = 0) (hDL : D ≤ L) :
    ∀ i, i+1 < D → bulk q L h i = 0 := by
  intro i hi
  have hr := output_zero_prefix q D i hz (by omega)
  have hu := (backward_zero_prefix q L D hq hz hDL).1 i hi
  have hv := (backward_zero_prefix q L D hq hz hDL).1 (i-1) (by omega)
  unfold bulk
  split
  · omega
  · split <;> omega

theorem bulk_ge_output (q : Nat → Nat) (L h i : Nat) :
    output q i ≤ bulk q L h i := by
  unfold bulk
  split
  · omega
  · omega

theorem value_eq_zero_iff (q : Nat → Nat) (L : Nat) :
    value q L = 0 ↔ ∀ i, i < L → q i = 0 := by
  induction L with
  | zero => simp [value]
  | succ L ih =>
    have hp : 0 < 10^L := Nat.pow_pos (by decide)
    constructor
    · intro hh
      have hh' : value q L=0 ∧ q L=0 := by
        simp only [value, Nat.add_eq_zero_iff, Nat.mul_eq_zero] at hh
        exact ⟨hh.1, hh.2.resolve_right (by omega)⟩
      intro i hi
      by_cases hil : i<L
      · exact ih.mp hh'.1 i hil
      · have he : i=L := by omega
        exact he ▸ hh'.2
    · intro hh
      simp only [value, ih.mpr (fun i hi => hh i (by omega)), hh L (by omega)]
      omega

/-- A finite nonzero input has a nonzero forward normalized digit,
including its terminal carry column. -/
theorem output_nonzero (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, q i ≤ 18) (hz : ∀ i, L ≤ i → q i = 0)
    (hn : ∃ i, 0 < q i) : ∃ i, i < L+1 ∧ 0 < output q i := by
  apply Classical.byContradiction
  intro hh
  have ho : ∀ i, i<L+1 → output q i=0 := by
    intro i hi
    have hp : ¬0<output q i := by
      intro hn
      exact hh ⟨i, hi, hn⟩
    omega
  have he := value_output q (L+1)
  have hc := carry_zero_tail q L hq hz (L+1) (by omega)
  have hov := (value_eq_zero_iff (output q) (L+1)).mpr ho
  rw [hc, hov] at he
  have hqv : value q (L+1)=0 := by omega
  obtain ⟨i, hi⟩ := hn
  have hil : i<L := by
    apply Classical.byContradiction
    intro hn
    have hh := hz i (by omega)
    omega
  have hqi := (value_eq_zero_iff q (L+1)).mp hqv i (by omega)
  omega

theorem bulk_nonzero (q : Nat → Nat) (L h : Nat)
    (hq : ∀ i, q i ≤ 18) (hz : ∀ i, L ≤ i → q i = 0)
    (hn : ∃ i, 0 < q i) : ∃ i, 0 < bulk q L h i := by
  obtain ⟨i, _, hi⟩ := output_nonzero q L hq hz hn
  have hh := bulk_ge_output q L h i
  exact ⟨i, by omega⟩

theorem iter_width_upper (s : State) (t : Nat) : (iter s t).1 ≤ s.1+t := by
  induction t with
  | zero => simp [iter]
  | succ t ih =>
    have hh := (nextLen_bounds (iter s t).2 (iter s t).1).2
    change nextLen (iter s t).2 (iter s t).1 ≤ s.1+(t+1)
    omega

theorem support_width_le_of_le (q p : Nat → Nat) (L A : Nat)
    (hq : Valid L q) (hp : Valid A p) (hle : ∀ i, p i ≤ q i) : A ≤ L := by
  have ha := hp.1
  have hpz := hp.2.2.2.2
  have he := hle (A-1)
  by_cases hh : A≤L
  · exact hh
  · have hz := hq.2.2.2.1 (A-1) (by omega)
    omega

theorem wordSum_padding (q : Nat → Nat) (A L : Nat)
    (hz : ∀ i, A ≤ i → q i=0) (hAL : A≤L) : wordSum q L = wordSum q A := by
  induction L with
  | zero =>
    have hh : A=0 := by omega
    subst A
    rfl
  | succ L ih =>
    by_cases hh : A≤L
    · simp only [wordSum, hz L hh, ih hh, Nat.add_zero]
    · have he : A=L+1 := by omega
      rw [he]

/-- Exact finite-time isolation.  The right component is updated by the
branch of the autonomous left profile and remains nonzero throughout.
The initial gap loses at most two positions per time step. -/
theorem isolated_decomposition (q p v : Nat → Nat) (L A D T : Nat)
    (hq : Valid L q) (hp : Valid A p) (heq : ∀ i, q i=p i+v i)
    (hvz : ∀ i, i<D → v i=0) (hvnon : ∃ i, 0<v i)
    (hgap : A+2*T+2≤D) :
    ∀ t, t≤T → ∃ w : Nat → Nat,
      (∀ i, (iter (L,q) t).2 i = (iter (A,p) t).2 i+w i) ∧
      (∀ i, i+t<D → w i=0) ∧ (∃ i, 0<w i) := by
  intro t
  induction t with
  | zero =>
    intro _
    exact ⟨v, heq, by simpa only [Nat.add_zero] using hvz, hvnon⟩
  | succ t ih =>
    intro ht
    obtain ⟨w, he, hwz, hwn⟩ := ih (by omega)
    let qs := iter (L,q) t
    let ps := iter (A,p) t
    have hqs : Valid qs.1 qs.2 := iter_valid (L,q) t hq
    have hps : Valid ps.1 ps.2 := iter_valid (A,p) t hp
    have hple : ∀ i, ps.2 i ≤ qs.2 i := by
      intro i
      have hh := he i
      change qs.2 i=ps.2 i+w i at hh
      omega
    have hAL := support_width_le_of_le qs.2 ps.2 qs.1 ps.1 hqs hps hple
    have hw : ∀ i, w i≤18 := by
      intro i
      have hh := he i
      have hb := hqs.2.2.1 i
      change qs.2 i=ps.2 i+w i at hh
      omega
    have hwt : ∀ i, qs.1≤i → w i=0 := by
      intro i hi
      have hh := he i
      have hz := hqs.2.2.2.1 i hi
      change qs.2 i=ps.2 i+w i at hh
      omega
    have hwpre : ∀ i, i<D-t → w i=0 := by
      intro i hi
      exact hwz i (by omega)
    have hDL : D-t≤qs.1 := by
      obtain ⟨i, hi⟩ := hwn
      have hil : i<qs.1 := by
        by_cases hh : i<qs.1
        · exact hh
        · have hz := hwt i (by omega)
          omega
      have hid : D-t≤i := by
        by_cases hh : D-t≤i
        · exact hh
        · have hz := hwpre i (by omega)
          omega
      omega
    have hwidth := iter_width_upper (A,p) t
    have hAgap : ps.1<D-t := by
      change ps.1≤A+t at hwidth
      omega
    have hsep := phi_separated ps.2 w qs.1 ps.1 (D-t)
      hps.2.2.1 hw hps.2.2.2.1 hwpre hAgap hDL
    have hpad := backward_padding ps.2 ps.1 qs.1 hps.2.2.2.1 hAL
    have hppad := phi_padding ps.2 ps.1 qs.1 hps.2.2.2.1 hAL
    let w' := bulk w qs.1 (backCarry ps.2 ps.1 0)
    refine ⟨w', ?_, ?_, ?_⟩
    · intro i
      change phi qs.2 qs.1 i = phi ps.2 ps.1 i+w' i
      have hfun : qs.2 = fun j => ps.2 j+w j := by
        funext j
        exact he j
      rw [hfun, hsep.2, hppad, hpad.1]
    · intro i hi
      exact bulk_zero_prefix w qs.1 (D-t) (backCarry ps.2 ps.1 0)
        hw hwpre hDL i (by omega)
    · exact bulk_nonzero w qs.1 (backCarry ps.2 ps.1 0) hw hwt hwn

/-- Concrete isolation supplies the strict mass decrement used by the
uniform escape induction.  All normalization and coupling premises are
proved from the stated initial finite profiles. -/
theorem isolated_mass (q p v : Nat → Nat) (L A D T : Nat)
    (hq : Valid L q) (hp : Valid A p) (heq : ∀ i, q i=p i+v i)
    (hvz : ∀ i, i<D → v i=0) (hvnon : ∃ i, 0<v i)
    (hgap : A+2*T+2≤D) :
    ∀ t, t≤T → mass (iter (A,p) t)+1 ≤ mass (iter (L,q) t) := by
  intro t ht
  obtain ⟨w, he, _, hwn⟩ := isolated_decomposition q p v L A D T
    hq hp heq hvz hvnon hgap t ht
  let qs := iter (L,q) t
  let ps := iter (A,p) t
  have hqs : Valid qs.1 qs.2 := iter_valid (L,q) t hq
  have hps : Valid ps.1 ps.2 := iter_valid (A,p) t hp
  have hple : ∀ i, ps.2 i≤qs.2 i := by
    intro i
    have hh := he i
    change qs.2 i=ps.2 i+w i at hh
    omega
  have hAL := support_width_le_of_le qs.2 ps.2 qs.1 ps.1 hqs hps hple
  have hm : wordSum qs.2 qs.1 = wordSum ps.2 ps.1 + wordSum w qs.1 := by
    rw [wordSum_congr qs.2 (fun i => ps.2 i+w i) qs.1 (fun i _ => he i),
      wordSum_add, wordSum_padding ps.2 ps.1 qs.1 hps.2.2.2.1 hAL]
  obtain ⟨i, hi⟩ := hwn
  have hil : i<qs.1 := by
    by_cases hh : i<qs.1
    · exact hh
    · have hz := hqs.2.2.2.1 i (by omega)
      have he' := he i
      change qs.2 i=ps.2 i+w i at he'
      omega
  have hmpos : 1 ≤ wordSum w qs.1 :=
    DecimalZeroGap.interval_length_le_mass w qs.1 i 1 (by omega)
      (fun j hj₁ hj₂ => by
        have hji : j=i := by omega
        simpa only [hji] using hi)
  change wordSum ps.2 ps.1+1 ≤ wordSum qs.2 qs.1
  omega

#print axioms forward_separated
#print axioms backward_separated
#print axioms phi_separated
#print axioms backward_padding
#print axioms output_nonzero
#print axioms isolated_decomposition
#print axioms isolated_mass

end DecimalProfile
