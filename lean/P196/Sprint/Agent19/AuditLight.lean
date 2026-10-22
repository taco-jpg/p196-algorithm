import P196.Agent315Orbit196Residues.Orbit196Mod3
import P196.Agent315Orbit196Residues.Orbit196Mod9
import P196.Agent119EightFamilies.EightFamilies
import P196.Agent119EightFamilies.TemporalResidues
import P196.Agent9DigitSumWindows.UniformDecimal
import P196.Agent9DigitSumWindows.SharpUniformDecimal
import P196.Agent9DigitSumWindows.Agent9DecimalFactorialEscape
import P196.Agent9DigitSumWindows.Agent9DigitSumIntervalCounts
import P196.Agent117RemainingCycles.Projection
import P196.Agent117RemainingCycles.Cycle112_k8
import P196.Agent117RemainingCycles.Cycle138_k7
import P196.Agent117RemainingCycles.Cycle164_k7
import P196.Agent117RemainingCycles.Cycle198_k7
import P196.Agent117RemainingCycles.Cycle248_k7
import P196.Agent117RemainingCycles.Cycle275_k8
import P196.Agent117RemainingCycles.Cycle398_k7
import P196.Agent117RemainingCycles.Cycle626_k7
import P196.Agent117RemainingCycles.Cycle710_k7
import P196.Agent117RemainingCycles.Cycle716_k7
import P196.Agent117RemainingCycles.Cycle790_k7
import P196.Agent117RemainingCycles.Cycle911_k7
import P196.Agent117RemainingCycles.Cycle936_k7
import P196.Agent117RemainingCycles.Cycle952_k7
import P196.Agent124ForwardInvariant.A124W3Summary
import P196.Agent113FiveLayer.FiveLayer
import P196.Agent113FiveLayer.FourColumnChain

/-! Agent 19 review: axiom audit of every registered endpoint of Agent315Orbit196Residues, Agent119EightFamilies, Agent9DigitSumWindows, Agent117RemainingCycles, Agent124ForwardInvariant, Agent113FiveLayer.
Run `lake env lean` on this file; each line must list only propext, Classical.choice, Quot.sound. -/


-- Agent315Orbit196Residues
#print axioms Agent315.TemporalColumn99.orbit196_mod3_ne_zero
#print axioms Agent315.TemporalColumn99.not_dvd3_orbit196
#print axioms Agent315.TemporalColumn99.orbit196_mod9_ne_zero
#print axioms Agent315.TemporalColumn99.not_dvd9_orbit196

-- Agent119EightFamilies
#print axioms Agent119.EightFamilies.famDigit_zero
#print axioms Agent119.EightFamilies.famDigit_one
#print axioms Agent119.EightFamilies.famDigit_mid
#print axioms Agent119.EightFamilies.famDigit_hi1
#print axioms Agent119.EightFamilies.famDigit_hi0
#print axioms Agent119.EightFamilies.mul_sparse_aux
#print axioms Agent119.EightFamilies.value_sparse
#print axioms Agent119.EightFamilies.fam_value
#print axioms Agent119.EightFamilies.fam_canonical
#print axioms Agent119.EightFamilies.step_mod3
#print axioms Agent119.EightFamilies.orbit196_not_dvd3
#print axioms Agent119.EightFamilies.fam_dvd3
#print axioms Agent119.EightFamilies.orbit196_three
#print axioms Agent119.EightFamilies.orbit196_dvd11
#print axioms Agent119.EightFamilies.step_ge
#print axioms Agent119.EightFamilies.orbit_mono
#print axioms Agent119.EightFamilies.orbit196_five
#print axioms Agent119.EightFamilies.fam_zero
#print axioms Agent119.EightFamilies.fam_ge
#print axioms Agent119.EightFamilies.early_or_short
#print axioms Agent119.EightFamilies.canonical196
#print axioms Agent119.EightFamilies.V_adm
#print axioms Agent119.EightFamilies.V_rep
#print axioms Agent119.EightFamilies.V_succ
#print axioms Agent119.EightFamilies.V_succ_fst
#print axioms Agent119.EightFamilies.V_succ_snd
#print axioms Agent119.EightFamilies.value_lt_pow
#print axioms Agent119.EightFamilies.V_width
#print axioms Agent119.EightFamilies.V_width3
#print axioms Agent119.EightFamilies.V_width4
#print axioms Agent119.EightFamilies.canonical_congr
#print axioms Agent119.EightFamilies.V_carry_le
#print axioms Agent119.EightFamilies.next_digits_no_overflow
#print axioms Agent119.EightFamilies.next_digits_overflow
#print axioms Agent119.EightFamilies.V_prefix_pred
#print axioms Agent119.EightFamilies.wordPrefix_two
#print axioms Agent119.EightFamilies.wordPrefix_three
#print axioms Agent119.EightFamilies.wordPrefix_four
#print axioms Agent119.EightFamilies.fam_palindrome
#print axioms Agent119.EightFamilies.last_step_overflow
#print axioms Agent119.EightFamilies.last_step_no_overflow
#print axioms Agent119.EightFamilies.pow_hundred_mod11
#print axioms Agent119.EightFamilies.pow_two_r_mod11
#print axioms Agent119.EightFamilies.value_sparse_mod11
#print axioms Agent119.EightFamilies.middle_overflow
#print axioms Agent119.EightFamilies.middle_no_overflow_one
#print axioms Agent119.EightFamilies.noOverflow_half
#print axioms Agent119.EightFamilies.segment_mem
#print axioms Agent119.EightFamilies.middle_no_overflow_even
#print axioms Agent119.EightFamilies.pred_11_0_0
#print axioms Agent119.EightFamilies.pred_1_16
#print axioms Agent119.EightFamilies.noOverflowPred_7700
#print axioms Agent119.EightFamilies.pred_3_13_9_9
#print axioms Agent119.EightFamilies.no_pred_11_0_0
#print axioms Agent119.EightFamilies.seven_chain
#print axioms Agent119.EightFamilies.reduce
#print axioms Agent119.EightFamilies.no_fam_one
#print axioms Agent119.EightFamilies.no_fam_two
#print axioms Agent119.EightFamilies.no_fam_four
#print axioms Agent119.EightFamilies.no_fam_eight
#print axioms Agent119.EightFamilies.no_fam_seven
#print axioms Agent119.EightFamilies.no_fam_mul3
#print axioms Agent119.EightFamilies.orbit196_ne_fam
#print axioms Agent119.EightFamilies.orbit196_digits_ne_fam
#print axioms Agent423.TemporalResidues.step_preserves_divisor99
#print axioms Agent423.TemporalResidues.step_preserves_dvd99
#print axioms Agent423.TemporalResidues.orbit_preserves_divisor99
#print axioms Agent423.TemporalResidues.orbit_preserves_dvd99
#print axioms Agent423.TemporalResidues.orbit_dvd99_of_dvd99_at
#print axioms Agent423.TemporalResidues.step_mod99_of_dvd11
#print axioms Agent423.TemporalResidues.orbit_mod99_pow_of_dvd11
#print axioms Agent423.TemporalResidues.orbit_six_mod99_of_dvd11
#print axioms Agent423.TemporalResidues.orbit_mod99_period_six
#print axioms Agent423.TemporalResidues.orbit196_six_mod99
#print axioms Agent423.TemporalResidues.orbit196_mod99_after_six
#print axioms Agent423.TemporalResidues.periodic_reduce
#print axioms Agent423.TemporalResidues.orbit196_mod99_table
#print axioms Agent423.TemporalResidues.phase196_injective
#print axioms Agent423.TemporalResidues.any_period_of_196_suffix_multiple_six
#print axioms Agent423.TemporalResidues.step_mod3
#print axioms Agent423.TemporalResidues.orbit_mod3_nonzero
#print axioms Agent423.TemporalResidues.orbit196_mod3_nonzero
#print axioms Agent423.TemporalResidues.orbit196_never_dvd99
#print axioms Agent423.TemporalResidues.phase_has_palindrome_representative
#print axioms Agent423.TemporalResidues.no_mod99_only_palindrome_exclusion

-- Agent9DigitSumWindows
#print axioms DecimalUniformEscape.digitSum_uniform_escape
#print axioms DecimalUniformEscape.digitSum_uniform_window
#print axioms DecimalUniformEscape.digitSum_uniform_window_196
#print axioms DecimalUniformEscape.digitSum_uniform_escape_sharp
#print axioms DecimalUniformEscape.digitSum_uniform_window_sharp
#print axioms DecimalUniformEscape.digitSum_uniform_window_196_sharp
#print axioms P196.Agent9.FactorialEscape.sharpEscapeBound_factorial
#print axioms P196.Agent9.FactorialEscape.sharpDigitSumEscapeBound_factorial
#print axioms P196.Agent9.FactorialEscape.digitSum_uniform_window_factorial
#print axioms P196.Agent9.FactorialEscape.digitSum_uniform_window_196_factorial
#print axioms P196.Agent9.IntervalCounts.digitSum_interval_count
#print axioms P196.Agent9.IntervalCounts.digitSum_interval_count_196

-- Agent117RemainingCycles
#print axioms Agent117.lowDigits_append
#print axioms Agent117.highDigits_append
#print axioms Agent117.lowDigits_length
#print axioms Agent117.highDigits_length
#print axioms Agent117.take_zipWith_append
#print axioms Agent117.forwardPrefix_append_take
#print axioms Agent117.forwardAdmitted_project
#print axioms Agent117.project_mem_prefixPredecessors
#print axioms Agent117.Cycle112_k8.entry_ok
#print axioms Agent117.Cycle112_k8.entry_end
#print axioms Agent117.Cycle112_k8.cycle_ok
#print axioms Agent117.Cycle112_k8.cycle_end
#print axioms Agent117.Cycle112_k8.cycle_pos
#print axioms Agent117.Cycle112_k8.no_checked_tree_contains_p0
#print axioms Agent117.Cycle112_k8.checkInitial_fails
#print axioms Agent117.Cycle138_k7.entry_ok
#print axioms Agent117.Cycle138_k7.entry_end
#print axioms Agent117.Cycle138_k7.cycle_ok
#print axioms Agent117.Cycle138_k7.cycle_end
#print axioms Agent117.Cycle138_k7.cycle_pos
#print axioms Agent117.Cycle138_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle138_k7.checkInitial_fails
#print axioms Agent117.Cycle164_k7.entry_ok
#print axioms Agent117.Cycle164_k7.entry_end
#print axioms Agent117.Cycle164_k7.cycle_ok
#print axioms Agent117.Cycle164_k7.cycle_end
#print axioms Agent117.Cycle164_k7.cycle_pos
#print axioms Agent117.Cycle164_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle164_k7.checkInitial_fails
#print axioms Agent117.Cycle198_k7.entry_ok
#print axioms Agent117.Cycle198_k7.entry_end
#print axioms Agent117.Cycle198_k7.cycle_ok
#print axioms Agent117.Cycle198_k7.cycle_end
#print axioms Agent117.Cycle198_k7.cycle_pos
#print axioms Agent117.Cycle198_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle198_k7.checkInitial_fails
#print axioms Agent117.Cycle248_k7.entry_ok
#print axioms Agent117.Cycle248_k7.entry_end
#print axioms Agent117.Cycle248_k7.cycle_ok
#print axioms Agent117.Cycle248_k7.cycle_end
#print axioms Agent117.Cycle248_k7.cycle_pos
#print axioms Agent117.Cycle248_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle248_k7.checkInitial_fails
#print axioms Agent117.Cycle275_k8.entry_ok
#print axioms Agent117.Cycle275_k8.entry_end
#print axioms Agent117.Cycle275_k8.cycle_ok
#print axioms Agent117.Cycle275_k8.cycle_end
#print axioms Agent117.Cycle275_k8.cycle_pos
#print axioms Agent117.Cycle275_k8.no_checked_tree_contains_p0
#print axioms Agent117.Cycle275_k8.checkInitial_fails
#print axioms Agent117.Cycle398_k7.entry_ok
#print axioms Agent117.Cycle398_k7.entry_end
#print axioms Agent117.Cycle398_k7.cycle_ok
#print axioms Agent117.Cycle398_k7.cycle_end
#print axioms Agent117.Cycle398_k7.cycle_pos
#print axioms Agent117.Cycle398_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle398_k7.checkInitial_fails
#print axioms Agent117.Cycle626_k7.entry_ok
#print axioms Agent117.Cycle626_k7.entry_end
#print axioms Agent117.Cycle626_k7.cycle_ok
#print axioms Agent117.Cycle626_k7.cycle_end
#print axioms Agent117.Cycle626_k7.cycle_pos
#print axioms Agent117.Cycle626_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle626_k7.checkInitial_fails
#print axioms Agent117.Cycle710_k7.entry_ok
#print axioms Agent117.Cycle710_k7.entry_end
#print axioms Agent117.Cycle710_k7.cycle_ok
#print axioms Agent117.Cycle710_k7.cycle_end
#print axioms Agent117.Cycle710_k7.cycle_pos
#print axioms Agent117.Cycle710_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle710_k7.checkInitial_fails
#print axioms Agent117.Cycle716_k7.entry_ok
#print axioms Agent117.Cycle716_k7.entry_end
#print axioms Agent117.Cycle716_k7.cycle_ok
#print axioms Agent117.Cycle716_k7.cycle_end
#print axioms Agent117.Cycle716_k7.cycle_pos
#print axioms Agent117.Cycle716_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle716_k7.checkInitial_fails
#print axioms Agent117.Cycle790_k7.entry_ok
#print axioms Agent117.Cycle790_k7.entry_end
#print axioms Agent117.Cycle790_k7.cycle_ok
#print axioms Agent117.Cycle790_k7.cycle_end
#print axioms Agent117.Cycle790_k7.cycle_pos
#print axioms Agent117.Cycle790_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle790_k7.checkInitial_fails
#print axioms Agent117.Cycle911_k7.entry_ok
#print axioms Agent117.Cycle911_k7.entry_end
#print axioms Agent117.Cycle911_k7.cycle_ok
#print axioms Agent117.Cycle911_k7.cycle_end
#print axioms Agent117.Cycle911_k7.cycle_pos
#print axioms Agent117.Cycle911_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle911_k7.checkInitial_fails
#print axioms Agent117.Cycle936_k7.entry_ok
#print axioms Agent117.Cycle936_k7.entry_end
#print axioms Agent117.Cycle936_k7.cycle_ok
#print axioms Agent117.Cycle936_k7.cycle_end
#print axioms Agent117.Cycle936_k7.cycle_pos
#print axioms Agent117.Cycle936_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle936_k7.checkInitial_fails
#print axioms Agent117.Cycle952_k7.entry_ok
#print axioms Agent117.Cycle952_k7.entry_end
#print axioms Agent117.Cycle952_k7.cycle_ok
#print axioms Agent117.Cycle952_k7.cycle_end
#print axioms Agent117.Cycle952_k7.cycle_pos
#print axioms Agent117.Cycle952_k7.no_checked_tree_contains_p0
#print axioms Agent117.Cycle952_k7.checkInitial_fails

-- Agent124ForwardInvariant
#print axioms Agent124.FwdW3.excluded_length
#print axioms Agent124.FwdW3.no_196_excluded

-- Agent113FiveLayer
#print axioms Agent113.FiveLayer.cert5_checked
#print axioms Agent113.FiveLayer.outer_in_layer0
#print axioms Agent113.FiveLayer.five_layer_strong
#print axioms Agent113.FiveLayer.pairAt_zero_pos
#print axioms Agent113.FiveLayer.full_to_outer
#print axioms Agent113.FiveLayer.five_layer
#print axioms Agent113.FiveLayer.width_lt_five
#print axioms Agent113.FiveLayer.no_196_full_pattern
#print axioms Agent113.FiveLayer.sharp_four
#print axioms Agent113.FourColumn.value_ge_of_lead
#print axioms Agent113.FourColumn.value_lt'
#print axioms Agent113.FourColumn.width_bounds
#print axioms Agent113.FourColumn.pow_ten_mono
#print axioms Agent113.FourColumn.width_ge_of_ge
#print axioms Agent113.FourColumn.width_le_of_lt
#print axioms Agent113.FourColumn.width_eq_of_bounds
#print axioms Agent113.FourColumn.canonical_quad
#print axioms Agent113.FourColumn.quad_box
#print axioms Agent113.FourColumn.quad_step
#print axioms Agent113.FourColumn.quad_eq_quad4
#print axioms Agent113.FourColumn.layerAtQ_beyond
#print axioms Agent113.FourColumn.rangeAll_sound
#print axioms Agent113.FourColumn.Cert4.inLayer_beyond
#print axioms Agent113.FourColumn.Cert4.step_sound
#print axioms Agent113.FourColumn.Cert4.short_sound
#print axioms Agent113.FourColumn.Cert4.depth_bound
#print axioms Agent113.FourColumn.cover19
#print axioms Agent113.FourColumn.cover18
