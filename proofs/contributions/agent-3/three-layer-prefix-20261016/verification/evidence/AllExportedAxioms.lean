import Lean
import FamilyDefinitions
import FamilyCardinality
import FiniteHorizonOverflow
import SafetyBridge
import NormalizedSafety
import FiniteHorizonTheorem
import HistoryInterfaces
import TwoLayerCertificate
import IntegerInterfaces
import ActualHistories
import HistoryFamily
import HistorySafety
import TwoHistoryTheorem
import DeadPrefix
import ActualDepth
import SharpHistoryFamily
import SharpHistoryTheorem

set_option pp.privateNames true

#print axioms P196.Agent3.OverflowHorizon.NoNeutral
#print axioms P196.Agent3.OverflowHorizon.allBits
#print axioms P196.Agent3.OverflowHorizon.allBits._sunfold
#print axioms P196.Agent3.OverflowHorizon.allBits.eq_1
#print axioms P196.Agent3.OverflowHorizon.allBits.eq_2
#print axioms P196.Agent3.OverflowHorizon.allBits.match_1
#print axioms P196.Agent3.OverflowHorizon.allBits_length
#print axioms P196.Agent3.OverflowHorizon.allBits_length._proof_1
#print axioms P196.Agent3.OverflowHorizon.allBits_nodup
#print axioms P196.Agent3.OverflowHorizon.choice
#print axioms P196.Agent3.OverflowHorizon.choice.eq_1
#print axioms P196.Agent3.OverflowHorizon.choice_injective
#print axioms P196.Agent3.OverflowHorizon.choice_le_eighteen
#print axioms P196.Agent3.OverflowHorizon.choice_map_injective
#print axioms P196.Agent3.OverflowHorizon.digitColumn
#print axioms P196.Agent3.OverflowHorizon.digitColumn.eq_1
#print axioms P196.Agent3.OverflowHorizon.digitColumn_pair
#print axioms P196.Agent3.OverflowHorizon.digitColumn_pair._proof_1
#print axioms P196.Agent3.OverflowHorizon.digitList_canonical
#print axioms P196.Agent3.OverflowHorizon.digitList_target_realization
#print axioms P196.Agent3.OverflowHorizon.digitList_target_realization._proof_1
#print axioms P196.Agent3.OverflowHorizon.digitValue
#print axioms P196.Agent3.OverflowHorizon.digitValue.eq_1
#print axioms P196.Agent3.OverflowHorizon.familyWords
#print axioms P196.Agent3.OverflowHorizon.familyWords.eq_1
#print axioms P196.Agent3.OverflowHorizon.familyWords_exact
#print axioms P196.Agent3.OverflowHorizon.familyWords_length
#print axioms P196.Agent3.OverflowHorizon.familyWords_member_properties
#print axioms P196.Agent3.OverflowHorizon.familyWords_nodup
#print axioms P196.Agent3.OverflowHorizon.finite_horizon_overflow_family
#print axioms P196.Agent3.OverflowHorizon.highWord
#print axioms P196.Agent3.OverflowHorizon.highWord.eq_1
#print axioms P196.Agent3.OverflowHorizon.inputHalf
#print axioms P196.Agent3.OverflowHorizon.inputHalf.eq_1
#print axioms P196.Agent3.OverflowHorizon.inputHalf_bounded
#print axioms P196.Agent3.OverflowHorizon.inputHalf_bounded._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputHalf_bounded._proof_2
#print axioms P196.Agent3.OverflowHorizon.inputHalf_bounded._proof_3
#print axioms P196.Agent3.OverflowHorizon.inputHalf_bounded._proof_4
#print axioms P196.Agent3.OverflowHorizon.inputHalf_length
#print axioms P196.Agent3.OverflowHorizon.inputHalf_length._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord
#print axioms P196.Agent3.OverflowHorizon.inputWord.eq_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_bounded
#print axioms P196.Agent3.OverflowHorizon.inputWord_bounded._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_bounded._proof_2
#print axioms P196.Agent3.OverflowHorizon.inputWord_canonical
#print axioms P196.Agent3.OverflowHorizon.inputWord_canonical._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_canonical_even
#print axioms P196.Agent3.OverflowHorizon.inputWord_common_next_value
#print axioms P196.Agent3.OverflowHorizon.inputWord_even_width
#print axioms P196.Agent3.OverflowHorizon.inputWord_even_width._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_final_carry
#print axioms P196.Agent3.OverflowHorizon.inputWord_final_carry._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_head
#print axioms P196.Agent3.OverflowHorizon.inputWord_injective
#print axioms P196.Agent3.OverflowHorizon.inputWord_injective._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_length
#print axioms P196.Agent3.OverflowHorizon.inputWord_length._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral._proof_2
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral._proof_3
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral._proof_4
#print axioms P196.Agent3.OverflowHorizon.inputWord_noNeutral._proof_5
#print axioms P196.Agent3.OverflowHorizon.inputWord_normalized_digits
#print axioms P196.Agent3.OverflowHorizon.inputWord_normalized_safe
#print axioms P196.Agent3.OverflowHorizon.inputWord_step
#print axioms P196.Agent3.OverflowHorizon.inputWord_step._proof_1
#print axioms P196.Agent3.OverflowHorizon.inputWord_symmetric
#print axioms P196.Agent3.OverflowHorizon.lowWord
#print axioms P196.Agent3.OverflowHorizon.lowWord.eq_1
#print axioms P196.Agent3.OverflowHorizon.mem_allBits_iff
#print axioms P196.Agent3.OverflowHorizon.mem_familyWords_iff
#print axioms P196.Agent3.OverflowHorizon.mem_familyWords_iff._proof_1
#print axioms P196.Agent3.OverflowHorizon.mem_familyWords_iff._proof_2
#print axioms P196.Agent3.OverflowHorizon.normalized_target_safe_prefix
#print axioms P196.Agent3.OverflowHorizon.normalized_target_safe_prefix._proof_1
#print axioms P196.Agent3.OverflowHorizon.normalized_target_step_value
#print axioms P196.Agent3.OverflowHorizon.overlap
#print axioms P196.Agent3.OverflowHorizon.overlap._sunfold
#print axioms P196.Agent3.OverflowHorizon.overlap.eq_1
#print axioms P196.Agent3.OverflowHorizon.overlap.eq_2
#print axioms P196.Agent3.OverflowHorizon.overlap.match_1
#print axioms P196.Agent3.OverflowHorizon.overlap_replicate
#print axioms P196.Agent3.OverflowHorizon.padded_normalization
#print axioms P196.Agent3.OverflowHorizon.padded_normalization._proof_1
#print axioms P196.Agent3.OverflowHorizon.rhoWord
#print axioms P196.Agent3.OverflowHorizon.rhoWord.eq_1
#print axioms P196.Agent3.OverflowHorizon.rho_inputWord
#print axioms P196.Agent3.OverflowHorizon.rho_inputWord._proof_1
#print axioms P196.Agent3.OverflowHorizon.stable_digit_carry
#print axioms P196.Agent3.OverflowHorizon.stable_digit_carry._proof_1
#print axioms P196.Agent3.OverflowHorizon.stepWord_noNeutral_overflow
#print axioms P196.Agent3.OverflowHorizon.stepWord_noNeutral_overflow._proof_1
#print axioms P196.Agent3.OverflowHorizon.stepWord_noNeutral_overflow._proof_2
#print axioms P196.Agent3.OverflowHorizon.target
#print axioms P196.Agent3.OverflowHorizon.target.eq_1
#print axioms P196.Agent3.OverflowHorizon.targetColumn
#print axioms P196.Agent3.OverflowHorizon.targetColumn.eq_1
#print axioms P196.Agent3.OverflowHorizon.targetColumn_bound
#print axioms P196.Agent3.OverflowHorizon.targetColumn_bound._proof_1
#print axioms P196.Agent3.OverflowHorizon.targetColumn_bound._proof_2
#print axioms P196.Agent3.OverflowHorizon.targetColumn_central
#print axioms P196.Agent3.OverflowHorizon.targetColumn_central._proof_1
#print axioms P196.Agent3.OverflowHorizon.targetColumn_central._proof_2
#print axioms P196.Agent3.OverflowHorizon.targetColumn_central._proof_3
#print axioms P196.Agent3.OverflowHorizon.targetColumn_central._proof_4
#print axioms P196.Agent3.OverflowHorizon.targetColumn_reflection
#print axioms P196.Agent3.OverflowHorizon.targetColumn_zero
#print axioms P196.Agent3.OverflowHorizon.target_admissible
#print axioms P196.Agent3.OverflowHorizon.target_admissible._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_admissible._proof_2
#print axioms P196.Agent3.OverflowHorizon.target_admissible._proof_3
#print axioms P196.Agent3.OverflowHorizon.target_hasRun18
#print axioms P196.Agent3.OverflowHorizon.target_hasRun18._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_length_for_safety
#print axioms P196.Agent3.OverflowHorizon.target_length_for_safety._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_numeric_safe_prefix
#print axioms P196.Agent3.OverflowHorizon.target_numeric_safe_prefix._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_numeric_safe_prefix._proof_2
#print axioms P196.Agent3.OverflowHorizon.target_positive_realization_safe_prefix
#print axioms P196.Agent3.OverflowHorizon.target_positive_realization_safe_prefix._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_realization_nonpalindrome
#print axioms P196.Agent3.OverflowHorizon.target_realization_nonpalindrome._proof_1
#print axioms P196.Agent3.OverflowHorizon.target_reverse_for_safety
#print axioms P196.Agent3.OverflowHorizon.zipAdd_high_low
#print axioms P196.Agent3.OverflowHorizon.zipAdd_interchange
#print axioms P196.Agent3.OverflowHorizon.zipAdd_low_high
#print axioms P196.Agent3.OverflowHorizon.zipAdd_padded_overlap
#print axioms P196.Agent3.ThreeLayer.ExactlyTwoZeroCarryLayers
#print axioms P196.Agent3.ThreeLayer.Forced
#print axioms P196.Agent3.ThreeLayer.depthBits
#print axioms P196.Agent3.ThreeLayer.depthBits.eq_1
#print axioms P196.Agent3.ThreeLayer.finite_horizon_exact_two_history_family
#print axioms P196.Agent3.ThreeLayer.forced_13_1
#print axioms P196.Agent3.ThreeLayer.forced_13_3
#print axioms P196.Agent3.ThreeLayer.forced_14_0
#print axioms P196.Agent3.ThreeLayer.forced_2_2
#print axioms P196.Agent3.ThreeLayer.forced_3_0
#print axioms P196.Agent3.ThreeLayer.forced_5_0
#print axioms P196.Agent3.ThreeLayer.forced_7_0
#print axioms P196.Agent3.ThreeLayer.forced_7_1
#print axioms P196.Agent3.ThreeLayer.forced_7_3
#print axioms P196.Agent3.ThreeLayer.historySymbol0
#print axioms P196.Agent3.ThreeLayer.historySymbol0.eq_1
#print axioms P196.Agent3.ThreeLayer.historySymbol0_actual
#print axioms P196.Agent3.ThreeLayer.historySymbol0_path
#print axioms P196.Agent3.ThreeLayer.historySymbol0_values
#print axioms P196.Agent3.ThreeLayer.historySymbol1
#print axioms P196.Agent3.ThreeLayer.historySymbol1._proof_1
#print axioms P196.Agent3.ThreeLayer.historySymbol1._proof_2
#print axioms P196.Agent3.ThreeLayer.historySymbol1.eq_1
#print axioms P196.Agent3.ThreeLayer.historySymbol1_actual
#print axioms P196.Agent3.ThreeLayer.historySymbol1_path
#print axioms P196.Agent3.ThreeLayer.historySymbol1_values
#print axioms P196.Agent3.ThreeLayer.historyTarget_depth_prefix
#print axioms P196.Agent3.ThreeLayer.historyTarget_exact_depth
#print axioms P196.Agent3.ThreeLayer.historyTarget_mirror
#print axioms P196.Agent3.ThreeLayer.historyWord0_no_zero_predecessor
#print axioms P196.Agent3.ThreeLayer.history_has_two_actual_layers
#print axioms P196.Agent3.ThreeLayer.local_zero_two_impossible
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily0_iff
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily0_iff._proof_1
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily0_iff._proof_2
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily2_iff
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily2_iff._proof_1
#print axioms P196.Agent3.ThreeLayer.mem_sharpHistoryFamily2_iff._proof_2
#print axioms P196.Agent3.ThreeLayer.no_three_actual_fibers
#print axioms P196.Agent3.ThreeLayer.no_three_actual_histories
#print axioms P196.Agent3.ThreeLayer.no_three_paths_dead_prefix
#print axioms P196.Agent3.ThreeLayer.path_nat_forced
#print axioms P196.Agent3.ThreeLayer.path_symbol_forced
#print axioms P196.Agent3.ThreeLayer.path_zero_two_impossible
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamilies_two_step
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0.eq_1
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0_length
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0_member_properties
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0_member_properties._proof_1
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily0_nodup
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2.eq_1
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2_length
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2_member_properties
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2_member_properties._proof_1
#print axioms P196.Agent3.ThreeLayer.sharpHistoryFamily2_nodup
#print axioms P196.Agent3.ThreeLayer.sharpWord0_injective
#print axioms P196.Agent3.ThreeLayer.sharpWord2_injective
#print axioms P196.Agent3.ThreeLayer.sharp_finite_horizon_family
#print axioms P196.Agent3.ThreeLayer.sharp_initial_canonical_chain
#print axioms P196.Agent3.ThreeLayer.sharp_initial_canonical_chain._proof_1
#print axioms P196.Agent3.ThreeLayer.sharp_initial_integer_exists
#print axioms P196.Agent3.ThreeLayer.sharp_initial_integer_package
#print axioms P196.Agent3.ThreeLayer.sharp_initial_integer_package._proof_1
#print axioms P196.Agent3.ThreeLayer.sharp_initial_no_zero_predecessor
#print axioms P196.Agent3.ThreeLayer.sharp_initial_no_zero_predecessor._proof_1
#print axioms P196.Agent3.ThreeLayer.sharp_initial_no_zero_predecessor._proof_2
#print axioms P196.Agent3.ThreeLayer.sharp_protected_exact_depth
#print axioms P196.Agent3.TwoHistory.IntegerRealizes
#print axioms P196.Agent3.TwoHistory.Joint
#print axioms P196.Agent3.TwoHistory.canonicalPair_lastPos
#print axioms P196.Agent3.TwoHistory.canonicalPair_normalized_digits
#print axioms P196.Agent3.TwoHistory.completedBits
#print axioms P196.Agent3.TwoHistory.completedBits._proof_1
#print axioms P196.Agent3.TwoHistory.completedBits.eq_1
#print axioms P196.Agent3.TwoHistory.completedBits_injective
#print axioms P196.Agent3.TwoHistory.completedBits_injective._proof_1
#print axioms P196.Agent3.TwoHistory.completedBits_length
#print axioms P196.Agent3.TwoHistory.correction
#print axioms P196.Agent3.TwoHistory.correction.match_1
#print axioms P196.Agent3.TwoHistory.correction_closes
#print axioms P196.Agent3.TwoHistory.correction_closes.match_1
#print axioms P196.Agent3.TwoHistory.correction_length
#print axioms P196.Agent3.TwoHistory.correction_length.match_1
#print axioms P196.Agent3.TwoHistory.digitColumn_zero_eq_headD
#print axioms P196.Agent3.TwoHistory.digitList_realizes_pair
#print axioms P196.Agent3.TwoHistory.digitValue_eq_evalL
#print axioms P196.Agent3.TwoHistory.digitValue_normalize
#print axioms P196.Agent3.TwoHistory.emit0
#print axioms P196.Agent3.TwoHistory.emit1
#print axioms P196.Agent3.TwoHistory.even_canonical_admissible
#print axioms P196.Agent3.TwoHistory.even_canonical_admissible._proof_1
#print axioms P196.Agent3.TwoHistory.even_canonical_realizable
#print axioms P196.Agent3.TwoHistory.finite_horizon_two_history_family
#print axioms P196.Agent3.TwoHistory.firstLabels
#print axioms P196.Agent3.TwoHistory.firstLabels._sunfold
#print axioms P196.Agent3.TwoHistory.firstLabels.eq_1
#print axioms P196.Agent3.TwoHistory.firstLabels.eq_2
#print axioms P196.Agent3.TwoHistory.firstLabels_length
#print axioms P196.Agent3.TwoHistory.historyBits
#print axioms P196.Agent3.TwoHistory.historyBits.eq_1
#print axioms P196.Agent3.TwoHistory.historyBits_closes
#print axioms P196.Agent3.TwoHistory.historyBits_length
#print axioms P196.Agent3.TwoHistory.historyFamilies_two_step
#print axioms P196.Agent3.TwoHistory.historyFamily0
#print axioms P196.Agent3.TwoHistory.historyFamily0.eq_1
#print axioms P196.Agent3.TwoHistory.historyFamily0_exact
#print axioms P196.Agent3.TwoHistory.historyFamily0_length
#print axioms P196.Agent3.TwoHistory.historyFamily0_member_properties
#print axioms P196.Agent3.TwoHistory.historyFamily0_nodup
#print axioms P196.Agent3.TwoHistory.historyFamily2
#print axioms P196.Agent3.TwoHistory.historyFamily2.eq_1
#print axioms P196.Agent3.TwoHistory.historyFamily2_exact
#print axioms P196.Agent3.TwoHistory.historyFamily2_length
#print axioms P196.Agent3.TwoHistory.historyFamily2_member_properties
#print axioms P196.Agent3.TwoHistory.historyFamily2_nodup
#print axioms P196.Agent3.TwoHistory.historyHalf0
#print axioms P196.Agent3.TwoHistory.historyHalf0.eq_1
#print axioms P196.Agent3.TwoHistory.historyHalf0_head
#print axioms P196.Agent3.TwoHistory.historyHalf1
#print axioms P196.Agent3.TwoHistory.historyHalf1.eq_1
#print axioms P196.Agent3.TwoHistory.historyHalf1_head
#print axioms P196.Agent3.TwoHistory.historyTarget
#print axioms P196.Agent3.TwoHistory.historyTarget._proof_2
#print axioms P196.Agent3.TwoHistory.historyTarget.eq_1
#print axioms P196.Agent3.TwoHistory.historyTarget_values
#print axioms P196.Agent3.TwoHistory.historyWord0
#print axioms P196.Agent3.TwoHistory.historyWord0.eq_1
#print axioms P196.Agent3.TwoHistory.historyWord0_canonical
#print axioms P196.Agent3.TwoHistory.historyWord0_even
#print axioms P196.Agent3.TwoHistory.historyWord0_even._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord0_final_carry
#print axioms P196.Agent3.TwoHistory.historyWord0_head
#print axioms P196.Agent3.TwoHistory.historyWord0_injective
#print axioms P196.Agent3.TwoHistory.historyWord0_length
#print axioms P196.Agent3.TwoHistory.historyWord0_length._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord0_reservoir
#print axioms P196.Agent3.TwoHistory.historyWord0_step
#print axioms P196.Agent3.TwoHistory.historyWord1
#print axioms P196.Agent3.TwoHistory.historyWord1.eq_1
#print axioms P196.Agent3.TwoHistory.historyWord1_canonical
#print axioms P196.Agent3.TwoHistory.historyWord1_even
#print axioms P196.Agent3.TwoHistory.historyWord1_even._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord1_final_carry
#print axioms P196.Agent3.TwoHistory.historyWord1_has_eighteen
#print axioms P196.Agent3.TwoHistory.historyWord1_has_eighteen._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord1_head
#print axioms P196.Agent3.TwoHistory.historyWord1_length
#print axioms P196.Agent3.TwoHistory.historyWord1_length._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord1_reservoir
#print axioms P196.Agent3.TwoHistory.historyWord1_step
#print axioms P196.Agent3.TwoHistory.historyWord2
#print axioms P196.Agent3.TwoHistory.historyWord2.eq_1
#print axioms P196.Agent3.TwoHistory.historyWord2_canonical
#print axioms P196.Agent3.TwoHistory.historyWord2_even
#print axioms P196.Agent3.TwoHistory.historyWord2_even._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord2_final_carry
#print axioms P196.Agent3.TwoHistory.historyWord2_injective
#print axioms P196.Agent3.TwoHistory.historyWord2_length
#print axioms P196.Agent3.TwoHistory.historyWord2_length._proof_3
#print axioms P196.Agent3.TwoHistory.historyWord2_step
#print axioms P196.Agent3.TwoHistory.history_integer_common_time_four
#print axioms P196.Agent3.TwoHistory.history_integer_realization_package
#print axioms P196.Agent3.TwoHistory.history_integer_safe_prefix
#print axioms P196.Agent3.TwoHistory.history_integer_safe_prefix._proof_1
#print axioms P196.Agent3.TwoHistory.history_integer_safe_prefix._proof_2
#print axioms P196.Agent3.TwoHistory.history_integer_safe_prefix._proof_3
#print axioms P196.Agent3.TwoHistory.history_orbit_three
#print axioms P196.Agent3.TwoHistory.history_path0
#print axioms P196.Agent3.TwoHistory.history_path1
#print axioms P196.Agent3.TwoHistory.history_positive_integer_exists
#print axioms P196.Agent3.TwoHistory.history_realizes_one
#print axioms P196.Agent3.TwoHistory.history_realizes_two
#print axioms P196.Agent3.TwoHistory.history_word_chain
#print axioms P196.Agent3.TwoHistory.initial_emit0
#print axioms P196.Agent3.TwoHistory.initial_emit1
#print axioms P196.Agent3.TwoHistory.initial_step
#print axioms P196.Agent3.TwoHistory.integer_nonpalindrome_of_odd_column
#print axioms P196.Agent3.TwoHistory.integer_nonpalindrome_of_odd_column._proof_1
#print axioms P196.Agent3.TwoHistory.integer_nonpalindrome_of_odd_outer
#print axioms P196.Agent3.TwoHistory.integer_realizes_next
#print axioms P196.Agent3.TwoHistory.integer_realizes_positive
#print axioms P196.Agent3.TwoHistory.integer_step_nonpalindrome_of_eighteen
#print axioms P196.Agent3.TwoHistory.integer_step_nonpalindrome_of_eighteen._proof_1
#print axioms P196.Agent3.TwoHistory.integer_step_nonpalindrome_of_eighteen._proof_2
#print axioms P196.Agent3.TwoHistory.integer_step_of_realizes
#print axioms P196.Agent3.TwoHistory.jointStep
#print axioms P196.Agent3.TwoHistory.local_eighteen
#print axioms P196.Agent3.TwoHistory.local_emit0
#print axioms P196.Agent3.TwoHistory.local_emit0.match_1
#print axioms P196.Agent3.TwoHistory.local_emit1
#print axioms P196.Agent3.TwoHistory.local_emit1.match_1
#print axioms P196.Agent3.TwoHistory.mem_historyFamily0_iff
#print axioms P196.Agent3.TwoHistory.mem_historyFamily0_iff._proof_1
#print axioms P196.Agent3.TwoHistory.mem_historyFamily0_iff._proof_2
#print axioms P196.Agent3.TwoHistory.mem_historyFamily2_iff
#print axioms P196.Agent3.TwoHistory.mem_historyFamily2_iff._proof_1
#print axioms P196.Agent3.TwoHistory.mem_historyFamily2_iff._proof_2
#print axioms P196.Agent3.TwoHistory.mirror_canonical
#print axioms P196.Agent3.TwoHistory.mirror_canonical._proof_1
#print axioms P196.Agent3.TwoHistory.mirror_canonical._proof_2
#print axioms P196.Agent3.TwoHistory.mirrored_eighteen_reservoir
#print axioms P196.Agent3.TwoHistory.mirrored_eighteen_reservoir._proof_1
#print axioms P196.Agent3.TwoHistory.normalized_integer_next
#print axioms P196.Agent3.TwoHistory.normalized_realizes_stepWord
#print axioms P196.Agent3.TwoHistory.path_actual_transition
#print axioms P196.Agent3.TwoHistory.path_eighteens
#print axioms P196.Agent3.TwoHistory.path_first_prefix
#print axioms P196.Agent3.TwoHistory.path_second_prefix
#print axioms P196.Agent3.TwoHistory.runStates
#print axioms P196.Agent3.TwoHistory.runStates._sunfold
#print axioms P196.Agent3.TwoHistory.runStates.eq_1
#print axioms P196.Agent3.TwoHistory.runStates.eq_2
#print axioms P196.Agent3.TwoHistory.runStates.match_1
#print axioms P196.Agent3.TwoHistory.runStates_append
#print axioms P196.Agent3.TwoHistory.scan_terminalCarry
#print axioms P196.Agent3.TwoHistory.secondLabels
#print axioms P196.Agent3.TwoHistory.secondLabels._sunfold
#print axioms P196.Agent3.TwoHistory.secondLabels.eq_1
#print axioms P196.Agent3.TwoHistory.secondLabels.eq_2
#print axioms P196.Agent3.TwoHistory.secondLabels_length
#print axioms P196.Agent3.TwoHistory.symbol
#print axioms P196.Agent3.TwoHistory.symbol._proof_1
#print axioms P196.Agent3.TwoHistory.symbol_false
#print axioms P196.Agent3.TwoHistory.symbol_true
#print axioms P196.Agent3.TwoHistory.symbol_val
#print axioms P196.Agent3.TwoHistory.symbol_values_bounded
#print axioms P196.Agent3.TwoHistory.symbol_values_bounded._proof_3

-- Preserve numeric components of private kernel names through `mkIdent`.
-- This diagnostic elaborates an ordinary #print axioms command for each.
open Lean Elab Command
run_cmd do
  let env ← getEnv
  let targets : List String := ["_private.ActualHistories.0.P196.Agent3.TwoHistory.runStates.match_1.eq_1",
    "_private.ActualHistories.0.P196.Agent3.TwoHistory.runStates.match_1.eq_2",
    "_private.ActualHistories.0.P196.Agent3.TwoHistory.runStates.match_1.splitter",
    "_private.FamilyCardinality.0.P196.Agent3.OverflowHorizon.allBits.match_1.eq_1",
    "_private.FamilyCardinality.0.P196.Agent3.OverflowHorizon.allBits.match_1.eq_2",
    "_private.FamilyCardinality.0.P196.Agent3.OverflowHorizon.allBits.match_1.splitter",
    "_private.FamilyCardinality.0.P196.Agent3.OverflowHorizon.nodup_map_of_injective",
    "_private.FiniteHorizonOverflow.0.P196.Agent3.OverflowHorizon.overlap.match_1.eq_1",
    "_private.FiniteHorizonOverflow.0.P196.Agent3.OverflowHorizon.overlap.match_1.eq_2",
    "_private.FiniteHorizonOverflow.0.P196.Agent3.OverflowHorizon.overlap.match_1.splitter",
    "_private.FiniteHorizonOverflow.0.P196.Agent3.OverflowHorizon.replicate_join",
    "_private.TwoLayerCertificate.0.P196.Agent3.TwoHistory.jointData",
    "_private.TwoLayerCertificate.0.P196.Agent3.TwoHistory.jointData._proof_2",
    "_private.TwoLayerCertificate.0.P196.Agent3.TwoHistory.jointData.match_1"]
  for (name, _) in env.constants.toList do
    if targets.contains name.toString then
      elabCommand (← `(command| #print axioms $(mkIdent name)))
