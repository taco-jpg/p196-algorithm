import P196.F1Semigroup.F1Cls
import P196.F1Semigroup.F1Sep1
import P196.F1Semigroup.F1Sep2
import P196.F1Semigroup.F1Sep3
import P196.F1Semigroup.F1Sep4
import P196.F1Semigroup.F1Tables
import P196.F1Semigroup.F1MinData
/-!
# Audit formalization, part 3: the minimal DFA of the base-10 F1 language has exactly 241 states

`LangB` (proved equal to the walk specification `Lang` in `F1Core.LangB_iff`) is the language of cyclic
words accepted by the first-coordinate NFA.  We prove, with kernel-checked finite certificates:

* `upper`  : there is a complete DFA with 241 states accepting `LangB`;
* `lower`  : every complete DFA (state type `Fin n`) accepting `LangB` has `n ≥ 241`;
* `acc104` : the 241-state DFA has exactly 104 accepting states.
-/
namespace F1

theorem sepOK_all : ∀ d, d < nC → sepOK d = true := by
  intro d hd
  by_cases h1 : d < 120
  · exact sepOK_1 d h1 (by omega)
  by_cases h2 : d < 170
  · exact sepOK_2 d h2 (by omega)
  by_cases h3 : d < 208
  · exact sepOK_3 d h3 (by omega)
  · exact sepOK_4 d (by unfold nC at hd; omega) (by omega)

/-! ## Pigeonhole on naturals -/

theorem inj_le : ∀ (n m : Nat) (f : Nat → Nat), (∀ c, c < m → f c < n) →
    (∀ c c', c < m → c' < m → f c = f c' → c = c') → m ≤ n := by
  intro n
  induction n with
  | zero =>
    intro m f hf _
    by_cases hm : m = 0
    · omega
    · have := hf 0 (by omega); omega
  | succ n ih =>
    intro m f hf hinj
    by_cases hex : ∃ c0, c0 < m ∧ f c0 = n
    · obtain ⟨c0, hc0, hfc0⟩ := hex
      have hm : 1 ≤ m := by omega
      let g : Nat → Nat := fun c => if c < c0 then f c else f (c + 1)
      have hg : ∀ c, c < m - 1 → g c < n := by
        intro c hc
        simp only [g]
        split
        · have h1 := hf c (by omega)
          have : f c ≠ n := by
            intro h; have := hinj c c0 (by omega) hc0 (by omega); omega
          omega
        · have h1 := hf (c + 1) (by omega)
          have : f (c + 1) ≠ n := by
            intro h; have := hinj (c + 1) c0 (by omega) hc0 (by omega); omega
          omega
      have hgi : ∀ c c', c < m - 1 → c' < m - 1 → g c = g c' → c = c' := by
        intro c c' hc hc' h
        simp only [g] at h
        split at h <;> split at h
        · exact hinj c c' (by omega) (by omega) h
        · have := hinj c (c' + 1) (by omega) (by omega) h; omega
        · have := hinj (c + 1) c' (by omega) (by omega) h; omega
        · have := hinj (c + 1) (c' + 1) (by omega) (by omega) h; omega
      have := ih (m - 1) g hg hgi
      omega
    · have : ∀ c, c < m → f c < n := by
        intro c hc
        have h1 := hf c hc
        have h2 : f c ≠ n := fun h => hex ⟨c, hc, h⟩
        omega
      have := ih m f this hinj
      omega

/-! ## Lower bound -/

theorem sep_spec (c d : Nat) (hcd : c < d) (hd : d < nC) :
    accB (irun (Rget c) (sepWord c d)) ≠ accB (irun (Rget d) (sepWord c d)) := by
  have h := sepOK_all d hd
  simp only [sepOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range,
    bne_iff_ne, ne_eq] at h
  have hc := h.2 c hcd
  have hRc : Rget c < nS := by
    have h' := sepOK_all c (by unfold nC at *; omega)
    simp only [sepOK, Bool.and_eq_true, decide_eq_true_eq] at h'
    exact h'.1
  have hRd := h.1
  rw [← accQ_eq _ (irun_spec _ _ hRc).1, ← accQ_eq _ (irun_spec _ _ hRd).1]
  exact hc

theorem rep_lt (c : Nat) (hc : c < nC) : Rget c < nS := by
  have h' := sepOK_all c hc
  simp only [sepOK, Bool.and_eq_true, decide_eq_true_eq] at h'
  exact h'.1

theorem lower (n : Nat) (D : DFA (Fin n)) (hD : ∀ w, D.accepts w = LangB w) : nC ≤ n := by
  have hu' : ∀ c, ∃ w, c < nC → irun 0 w = Rget c := by
    intro c
    by_cases hc : c < nC
    · obtain ⟨w, hw⟩ := reach_all (Rget c) (rep_lt c hc)
      exact ⟨w, fun _ => hw⟩
    · exact ⟨[], fun h => absurd h hc⟩
  let u : Nat → List Bool := fun c => Classical.choose (hu' c)
  have hu : ∀ c, c < nC → irun 0 (u c) = Rget c := fun c hc => Classical.choose_spec (hu' c) hc
  let f : Nat → Nat := fun c => (D.runFrom D.start (u c)).val
  have key : ∀ c d, c < d → d < nC → f c ≠ f d := by
    intro c d hcd hd hf
    have hc : c < nC := by omega
    have hq : D.runFrom D.start (u c) = D.runFrom D.start (u d) := Fin.ext hf
    have e1 : D.accepts (u c ++ sepWord c d) = D.accepts (u d ++ sepWord c d) := by
      simp only [DFA.accepts, DFA.runFrom, List.foldl_append] at *
      rw [hq]
    rw [hD, hD, LangB_irun, LangB_irun, irun_append, irun_append, hu c hc, hu d hd] at e1
    exact sep_spec c d hcd hd e1
  refine inj_le n nC f (fun c _ => (D.runFrom D.start (u c)).isLt) ?_
  intro c c' hc hc' h
  rcases Nat.lt_trichotomy c c' with hlt | heq | hgt
  · exact absurd h (key c c' hlt hc')
  · exact heq
  · exact absurd h.symm (key c' c hgt hc)

/-! ## Upper bound: the quotient DFA with 241 states -/

def Q : DFA (Fin 241) where
  start := ⟨clsOf 0 % 241, Nat.mod_lt _ (by decide)⟩
  step := fun q a => ⟨clsOf (Nget a (Rget q.val)) % 241, Nat.mod_lt _ (by decide)⟩
  acc := fun q => accB (Rget q.val)

theorem Q_run (w : List Bool) : ∀ i, i < nS →
    ((Q.runFrom ⟨clsOf i % 241, Nat.mod_lt _ (by decide)⟩ w).val = clsOf (irun i w)) ∧
    clsOf (irun i w) < 241 := by
  induction w with
  | nil =>
    intro i hi
    have h := clsOK_all i hi
    simp only [clsOK, Bool.and_eq_true, decide_eq_true_eq] at h
    have h1 : clsOf i < 241 := h.1.1.1.1
    exact ⟨by simp [DFA.runFrom, irun, Nat.mod_eq_of_lt h1], h1⟩
  | cons a w ih =>
    intro i hi
    have h := clsOK_all i hi
    simp only [clsOK, Bool.and_eq_true, decide_eq_true_eq] at h
    have h1 : clsOf i < 241 := h.1.1.1.1
    have hcong : clsOf (Nget a (Rget (clsOf i))) = clsOf (Nget a i) := by
      cases a
      · exact h.1.2
      · exact h.2
    have hN := (tab_step a i hi).1
    obtain ⟨ih1, ih2⟩ := ih (Nget a i) hN
    have hc' := clsOK_all (Nget a i) hN
    simp only [clsOK, Bool.and_eq_true, decide_eq_true_eq] at hc'
    have h2 : clsOf (Nget a i) < 241 := hc'.1.1.1.1
    have estep : Q.step ⟨clsOf i % 241, Nat.mod_lt _ (by decide)⟩ a
        = ⟨clsOf (Nget a i) % 241, Nat.mod_lt _ (by decide)⟩ := by
      apply Fin.ext
      simp only [Q]
      rw [Nat.mod_eq_of_lt h1, hcong]
    refine ⟨?_, ?_⟩
    · show (List.foldl Q.step (Q.step ⟨clsOf i % 241, _⟩ a) w).val = clsOf (irun (Nget a i) w)
      rw [estep]; exact ih1
    · exact ih2

theorem upper : ∀ w, Q.accepts w = LangB w := by
  intro w
  have h0 : 0 < nS := by decide
  have hr := Q_run w 0 h0
  have hcls := clsOK_all (irun 0 w) (irun_spec w 0 h0).1
  simp only [clsOK, Bool.and_eq_true, decide_eq_true_eq] at hcls
  have hq := hr.1
  have hacc : accQ (Rget (clsOf (irun 0 w))) = accQ (irun 0 w) := by simpa using hcls.1.1.2
  rw [LangB_irun]
  unfold DFA.accepts
  show accB (Rget (Q.runFrom ⟨clsOf 0 % 241, _⟩ w).val) = accB (irun 0 w)
  rw [hq]
  rw [← accQ_eq _ (irun_spec w 0 h0).1, ← accQ_eq _ hcls.1.1.1.2, hacc]

/-- Main theorem: the minimal complete DFA for the decimal F1 language of cyclic overflow words has
exactly 241 states (104 accepting), starting from the 434 reachable Boolean-relation states. -/
theorem minimal_dfa_241 :
    (∃ D : DFA (Fin 241), ∀ w, D.accepts w = LangB w) ∧
    (∀ (n : Nat) (D : DFA (Fin n)), (∀ w, D.accepts w = LangB w) → 241 ≤ n) :=
  ⟨⟨Q, upper⟩, fun n D h => lower n D h⟩

/-- and `LangB` is the walk language of the NFA specification -/
theorem minimal_dfa_241_spec :
    (∃ D : DFA (Fin 241), ∀ w, (D.accepts w = true ↔ Lang w)) ∧
    (∀ (n : Nat) (D : DFA (Fin n)), (∀ w, (D.accepts w = true ↔ Lang w)) → 241 ≤ n) := by
  refine ⟨⟨Q, fun w => by rw [upper]; exact LangB_iff w⟩, fun n D h => lower n D fun w => ?_⟩
  have := h w
  rw [← LangB_iff] at this
  cases hb : D.accepts w <;> cases hl : LangB w <;> simp_all

end F1
