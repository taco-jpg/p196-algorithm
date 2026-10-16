import Agent102AffineBoundary
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
/- 审计主体沿用仓库原验证器的来源模块枚举与公理限制；未修改原验证器。 -/
#check Agent102.word_nil
#check Agent102.word_cons
#check Agent102.word_append
#check Agent102.word_length
#check Agent102.word_reverse
#check Agent102.Span.shift_covers
#check Agent102.Span.shift_overlaps
#check Agent102.spansFrom_shift
#check Agent102.spansFrom_eq_map_spans
#check Agent102.spansFrom_append
#check Agent102.length_spansFrom
#check Agent102.length_spans
#check Agent102.mem_spansFrom_bounds
#check Agent102.exists_mem_spansFrom_covers
#check Agent102.exists_mem_spansFrom_covers_iff
#check Agent102.mem_spans_bounds
#check Agent102.exists_mem_spans_covers
#check Agent102.exists_mem_spans_covers_iff
#check Agent102.eq_of_mem_spansFrom_covers
#check Agent102.eq_of_mem_spans_covers
#check Agent102.getElem?_word_of_mem_spansFrom
#check Agent102.getElem?_word_of_covers
#check Agent102.Span.overlaps_iff_exists_covers
#check Agent102.Span.overlaps_of_covers
#check Agent102.word_eq_iff_length_and_overlap_digits
#check Agent102.word_eq_iff_count_sum_and_overlap_digits
#check Agent102.Affine.eval_zero
#check Agent102.Affine.eval_add
#check Agent102.Affine.intercept_bounds_of_cutoff
#check Agent102.Affine.eval_pos_of_slope_pos
#check Agent102.Affine.eval_neg_of_slope_neg
#check Agent102.Affine.eval_nonneg_iff
#check Agent102.Affine.eval_neg_iff
#check Agent102.Affine.eval_positivePart
#check Agent102.Affine.eval_positivePart_nonneg
#check Agent102.Affine.compareCutoff_comm
#check Agent102.Affine.eval_lt_of_slope_lt
#check Agent102.Affine.eval_le_iff
#check Agent102.Affine.eval_lt_iff
#check Agent102.Affine.eval_eq_iff
#check Agent102.Affine.eval_le_stable
#check Agent102.Affine.eval_lt_stable
#check Agent102.Affine.eval_eq_stable
#check Agent102.AffineBoundary.wordAt_moving
#check Agent102.AffineBoundary.wordAt_fixed
#check Agent102.AffineBoundary.moving_fixed_eq_iff
#check Agent102.AffineBoundary.compareCutoff_moving_fixed
#check Agent102.AffineBoundary.moving_fixed_stable_iff
#check Agent102.AffineBoundary.equality_changes_arbitrarily_late
#check Agent102.AffineBoundary.no_uniform_wordAt_cutoff
#check Agent102.AffineBoundary.run_structure_counterexample
#check Agent102.AffineBoundary.overlap_digits_without_width
#check Agent102.AffineBoundary.zero_span_cross_inequalities
#check Agent102.AffineBoundary.zero_span_realized
#check Agent102.AffineBoundary.cross_inequalities_false_negative
run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "Agent102RunWord", "Agent102AffineArithmetic", "Agent102AffineBoundary"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
