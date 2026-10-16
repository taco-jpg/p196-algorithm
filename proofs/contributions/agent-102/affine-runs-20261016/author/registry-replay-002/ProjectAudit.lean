import Agent102AffineRuns
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
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
#check Agent102.Span.overlaps_iff_exists_covers
#check Agent102.Span.overlaps_of_covers
#check Agent102.word_eq_iff_length_and_overlap_digits
#check Agent102.word_eq_iff_count_sum_and_overlap_digits
#check Agent102.le_maxList_of_mem
#check Agent102.cutoff_le_lengthCutoff
#check Agent102.wordAt_nil
#check Agent102.wordAt_cons
#check Agent102.widthAffine_eval
#check Agent102.widthAffine_nonneg
#check Agent102.spanSpecsFrom_at
#check Agent102.spanSpecs_at
#check Agent102.spanSpecsFrom_nonneg
#check Agent102.spanSpecs_nonneg
#check Agent102.widthAffine_mem_endpoints
#check Agent102.lo_mem_endpoints
#check Agent102.hi_mem_endpoints
#check Agent102.endpoints_nonneg
#check Agent102.compareCutoff_le_pairCutoff
#check Agent102.left_lengthCutoff_le
#check Agent102.right_lengthCutoff_le
#check Agent102.pairCutoff_le_equalityCutoff
#check Agent102.combined_endpoints_nonneg
#check Agent102.endpoint_nat_lt_stable
#check Agent102.width_eq_stable
#check Agent102.Span.overlaps_iff_four
#check Agent102.span_overlap_stable
#check Agent102.wordAt_eq_iff_spans
#check Agent102.wordAt_eq_stable
#check Agent102.wordAt_reverse
#check Agent102.wordAt_palindrome_stable
#check Agent102.equalOnTail_spec
#check Agent102.unequalOnTail_spec
#check Agent102.equality_before_cutoff_of_tail_mismatch
#check Agent102.palindromicOnTail_spec
#check Agent102.nonpalindromicOnTail_spec
run_cmd do
  let env ← getEnv
  let selected : List String := ["Agent102RunDefs", "Agent102AffineArithmetic", "Agent102RunEndpoints", "Agent102RunWord", "Agent102AffineRuns"]
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
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
