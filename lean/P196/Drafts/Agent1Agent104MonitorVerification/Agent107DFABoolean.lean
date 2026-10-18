import P196.Drafts.Agent1Agent104MonitorVerification.Agent107DFAAlphabet
import P196.Drafts.Agent1Agent104MonitorVerification.Agent107DFAChecker

/-!
# The original finite Boolean DFA arrays

`BooleanDFA` is an arbitrary truth assignment to the original `N × 19 × N`
transition array and `N × 11` final array, with the required positive state
count. `OneHot` states exactly one true successor in every transition row.
Extraction is a finite list search, not an external solver or choice oracle.
The reflection theorem checks the same existence and uniqueness condition.

The extracted machine is totalized on other natural symbols. Faithfulness
is asserted only for the original 19 pair symbols and valid optional centers;
symbol 19 used as witness padding by another Python routine is not read here.
-/

namespace Agent107.FoldedDFA.Encoding

structure BooleanDFA (N : Nat) where
  positive : 0 < N
  d : Fin N → Fin 19 → Fin N → Bool
  f : Fin N → Fin 11 → Bool

namespace BooleanDFA

def zero {N : Nat} (B : BooleanDFA N) : Fin N := ⟨0, B.positive⟩

def OneHot {N : Nat} (B : BooleanDFA N) : Prop :=
  ∀ a : Fin N, ∀ q : Fin 19, ∃ b : Fin N,
    B.d a q b = true ∧ ∀ c : Fin N, B.d a q c = true → c = b

def dest {N : Nat} (B : BooleanDFA N) (a : Fin N) (q : Fin 19) : Fin N :=
  ((List.finRange N).find? (B.d a q)).getD B.zero

def toDFA {N : Nat} (B : BooleanDFA N) : DFA N where
  positive := B.positive
  step a q := if h : q < 19 then B.dest a ⟨q, h⟩ else a
  final a c := if h : CenterValid c then B.f a ⟨centerCode c, centerCode_lt c h⟩
    else false

@[simp] theorem toDFA_start {N : Nat} (B : BooleanDFA N) :
    B.toDFA.start = B.zero := rfl

theorem toDFA_step_symbol {N : Nat} (B : BooleanDFA N)
    (a : Fin N) (q : Fin 19) :
    B.toDFA.step a q.val = B.dest a q := by
  simp only [toDFA, dif_pos q.isLt]

theorem toDFA_final_valid {N : Nat} (B : BooleanDFA N)
    (a : Fin N) (c : Option Nat) (hc : CenterValid c) :
    B.toDFA.final a c = B.f a ⟨centerCode c, centerCode_lt c hc⟩ := by
  simp only [toDFA, dif_pos hc]

@[simp] theorem toDFA_final_none {N : Nat} (B : BooleanDFA N) (a : Fin N) :
    B.toDFA.final a none = B.f a ⟨0, by decide⟩ := by
  exact B.toDFA_final_valid a none trivial

@[simp] theorem toDFA_final_some_zero {N : Nat} (B : BooleanDFA N) (a : Fin N) :
    B.toDFA.final a (some 0) = B.f a ⟨1, by decide⟩ := by
  exact B.toDFA_final_valid a (some 0) (by decide)

theorem dest_true {N : Nat} (B : BooleanDFA N) (h : B.OneHot)
    (a : Fin N) (q : Fin 19) : B.d a q (B.dest a q) = true := by
  cases hf : (List.finRange N).find? (B.d a q) with
  | none =>
    obtain ⟨b, hb, _⟩ := h a q
    have hn := (List.find?_eq_none.mp hf) b (List.mem_ofFn.mpr ⟨b, rfl⟩)
    exact False.elim (hn hb)
  | some b =>
    simpa only [dest, hf, Option.getD_some] using List.find?_some hf

theorem dest_iff {N : Nat} (B : BooleanDFA N) (h : B.OneHot)
    (a : Fin N) (q : Fin 19) (b : Fin N) :
    B.d a q b = true ↔ B.dest a q = b := by
  obtain ⟨w, _, hu⟩ := h a q
  constructor
  · intro hb
    exact (hu (B.dest a q) (B.dest_true h a q)).trans (hu b hb).symm
  · intro hb
    rw [← hb]
    exact B.dest_true h a q

/-- The original one-hot row and the extracted deterministic transition
have exactly the same successor, in both directions. -/
theorem transition_iff {N : Nat} (B : BooleanDFA N) (h : B.OneHot)
    (a : Fin N) (q : Fin 19) (b : Fin N) :
    B.d a q b = true ↔ B.toDFA.step a q.val = b := by
  rw [B.toDFA_step_symbol]
  exact B.dest_iff h a q b

theorem transition_selected {N : Nat} (B : BooleanDFA N) (h : B.OneHot)
    (a : Fin N) (q : Nat) (hq : q < 19) :
    B.d a ⟨q, hq⟩ (B.toDFA.step a q) = true := by
  exact (B.transition_iff h a ⟨q, hq⟩ _).2 rfl

end BooleanDFA

/-- An executable exactly-one check for one finite Boolean row. -/
def checkRow {N : Nat} (row : Fin N → Bool) : Bool :=
  (List.finRange N).any fun b => row b &&
    allFin (fun c => boolImplies (row c) (decide (c = b)))

theorem checkRow_iff {N : Nat} (row : Fin N → Bool) :
    checkRow row = true ↔
      ∃ b : Fin N, row b = true ∧ ∀ c : Fin N, row c = true → c = b := by
  simp only [checkRow, List.any_eq_true, Bool.and_eq_true,
    allFin_iff, boolImplies_iff, decide_eq_true_eq]
  constructor
  · rintro ⟨b, _, hb, hu⟩
    exact ⟨b, hb, hu⟩
  · rintro ⟨b, hb, hu⟩
    exact ⟨b, List.mem_ofFn.mpr ⟨b, rfl⟩, hb, hu⟩

def checkOneHot {N : Nat} (B : BooleanDFA N) : Bool :=
  allFin fun a => allFin fun q => checkRow (B.d a q)

theorem checkOneHot_iff {N : Nat} (B : BooleanDFA N) :
    checkOneHot B = true ↔ B.OneHot := by
  simp only [checkOneHot, allFin_iff, checkRow_iff, BooleanDFA.OneHot]

end Agent107.FoldedDFA.Encoding

#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.toDFA_start
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.toDFA_step_symbol
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.toDFA_final_valid
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.toDFA_final_none
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.toDFA_final_some_zero
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.dest_true
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.dest_iff
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.transition_iff
#print axioms Agent107.FoldedDFA.Encoding.BooleanDFA.transition_selected
#print axioms Agent107.FoldedDFA.Encoding.checkRow_iff
#print axioms Agent107.FoldedDFA.Encoding.checkOneHot_iff
