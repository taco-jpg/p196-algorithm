import BoundaryCertificateK
import ArithmeticBridge

/-! Agent #109 kernel-only replay of `ArithmeticBridge.lean`: identical proofs with
`decide +kernel` in place of the compiler-evaluated decision procedure, over the literal
tables of `BoundaryDataK.lean`. Definitions that do not mention those tables are reused
from the original module. -/

namespace BoundaryCertificateK
open Sofic BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem candidates_complete_checked :
    ∀ (l : Fin 88) (q : Fin 19) (a b e : Fin 2),
      let x := candidate l q a b e
      permitted l x = true → opts.toList.contains x = true := by
  decide +kernel

theorem permitted_bounds {l : Nat} {x : Opt} (h : permitted l x = true) :
    l < 88 ∧ x.q < 19 ∧ x.a < 2 ∧ x.b < 2 ∧ x.e < 2 ∧
    x = candidate l x.q x.a x.b x.e := by
  have hh := h
  simp only [permitted, Bool.and_eq_true, decide_eq_true_eq,
    Bool.or_eq_true, Bool.not_eq_true, beq_iff_eq] at hh
  refine ⟨by omega, by omega, by omega, by omega, by omega, ?_⟩
  cases x with
  | mk q a b c e r =>
    simp only [candidate, Opt.mk.injEq]
    simp only [Opt.q, Opt.a, Opt.b, Opt.c, Opt.e, Opt.r] at hh
    exact ⟨trivial, trivial, trivial, hh.2, trivial, by omega⟩

theorem options_complete {l : Nat} {x : Opt} (h : permitted l x = true) :
    ∃ i : Fin 164, opts[i.val]! = x := by
  obtain ⟨hl, hq, ha, hb, he, hx⟩ := permitted_bounds h
  have hc := candidates_complete_checked ⟨l, hl⟩ ⟨x.q, hq⟩
    ⟨x.a, ha⟩ ⟨x.b, hb⟩ ⟨x.e, he⟩
  rw [← hx] at hc
  have hmem : x ∈ opts.toList := by simpa using hc h
  obtain ⟨i, hi, heq⟩ := List.mem_iff_getElem.mp hmem
  have hsize : opts.toList.length = 164 := by decide
  refine ⟨⟨i, by omega⟩, ?_⟩
  have hi' : i < opts.size := by simpa using hi
  simpa [getElem!_pos, hi'] using heq

noncomputable def optionIndex (x : Opt) : Fin 164 := by
  classical
  exact if h : ∃ i : Fin 164, opts[i.val]! = x then Classical.choose h else ⟨0, by decide⟩

theorem optionIndex_correct {l : Nat} {x : Opt} (h : permitted l x = true) :
    opts[(optionIndex x).val]! = x := by
  have hx := options_complete h
  simp only [optionIndex, dif_pos hx]
  exact Classical.choose_spec hx

theorem fiber_complete {l : Nat} {x : Opt} (h : permitted l x = true) :
    (optionIndex x).val ∈ fiber l := by
  have hl := (permitted_bounds h).1
  have hall := List.all_eq_true.mp fibers_arithmetic_checked l (List.mem_range.mpr hl)
  have hpairs := (Bool.and_eq_true_iff.mp hall).2
  have hpair := List.all_eq_true.mp hpairs (optionIndex x).val
    (List.mem_range.mpr (optionIndex x).isLt)
  have heq : (fiber l).contains (optionIndex x).val = permitted l opts[(optionIndex x).val]! := by
    simpa using hpair
  rw [optionIndex_correct h, h] at heq
  simpa using heq

theorem arithmetic_column_to_table {n : Nat} {old new : Word}
    (hn : 0 < n) (h : ArithmeticColumn n old new) :
    Column fiber output n old new := by
  obtain ⟨hold, hnew, x, hxper, hx⟩ := h
  refine ⟨hold, hnew, (fun i => (optionIndex (x i)).val), ?_, ?_⟩
  · intro i
    exact congrArg (fun y => (optionIndex y).val) (hxper i)
  · intro i hi
    refine ⟨fiber_complete (hx i hi).1, ?_⟩
    have hnext : opts[(optionIndex (x (i+1))).val]! = x (i+1) := by
      by_cases hh : i+1 < n
      · exact optionIndex_correct (hx (i+1) hh).1
      · have heq : i+1 = n := by omega
        rw [heq, show x n = x 0 from by simpa using hxper 0]
        exact optionIndex_correct (hx 0 hn).1
    change outputOf opts[(optionIndex (x i)).val]! opts[(optionIndex (x (i+1))).val]! = _
    rw [optionIndex_correct (hx i hi).1, hnext]
    exact (hx i hi).2

theorem arithmetic_path_to_table {n : Nat} (hn : 0 < n) {u v : Word}
    (h : ReverseClosure.Path (ArithmeticColumn n) u v) :
    ReverseClosure.Path (Column fiber output n) u v := by
  induction h with
  | refl => exact .refl _
  | snoc _ edge ih => exact .snoc ih (arithmetic_column_to_table hn edge)

/-- Unconditional, all-width exclusion for the displayed decimal inverse
equations. This does not assert a theorem about arbitrary decimal orbits. -/

theorem no_arithmetic_exterior {n : Nat} {target : Word}
    (ht : Accepts graph0K n target) :
    ¬ ReverseClosure.Path (ArithmeticColumn n) (fun _ => 41) target := by
  intro h
  exact no_finite_exterior ht (arithmetic_path_to_table ht.1 h)

end BoundaryCertificateK
