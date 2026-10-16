import CertificateControls
import Lean
set_option pp.universes true

#check Agent109.Word
#check Agent109.zipAdd
#check Agent109.pair
#check Agent109.normalize
#check Agent109.stepWord
#check Agent109.template
#check Agent109.zipAdd_eq_zipWith
#check Agent109.zipAdd_append
#check Agent109.zipAdd_length
#check Agent109.zipAdd_comm
#check Agent109.zipAdd_reverse
#check Agent109.zipAdd_replicate
#check Agent109.norm
#check Agent109.carryWord
#check Agent109.normalize_eq_norm
#check Agent109.norm_length
#check Agent109.norm_append
#check Agent109.Bounded
#check Agent109.norm_carry_le
#check Agent109.norm_digit_lt
#check Agent109.kOf
#check Agent109.tOf
#check Agent109.Phase
#check Agent109.norm_band_tail
#check Agent109.norm_band
#check Agent109.complement_k
#check Agent109.complement_t
#check Agent109.complement_phase
#check Agent109.next_phase
#check Agent109.next_complement
#check Agent109.Data
#check Agent109.data
#check Agent109.u0
#check Agent109.u1
#check Agent109.u2
#check Agent109.u3
#check Agent109.digitWord
#check Agent109.bounded_reverse
#check Agent109.norm_template
#check Agent109.normalize_template
#check Agent109.gamma_le
#check Agent109.pair_split
#check Agent109.Br
#check Agent109.Ar
#check Agent109.Cr
#check Agent109.stepWord_template
#check Agent109.reverseAux
#check Agent109.reverseFuel
#check Agent109.reverse10
#check Agent109.Palindrome
#check Agent109.step
#check Agent109.orbitWord
#check Agent109.orbit
#check Agent109.evalL
#check Agent109.digitsFuel
#check Agent109.digits
#check Agent109.pairWord
#check Agent109.digitsFuel_stable
#check Agent109.digits_zero
#check Agent109.digits_pos
#check Agent109.evalL_digits
#check Agent109.evalL_append
#check Agent109.evalL_zipAdd
#check Agent109.reverseFuel_digits
#check Agent109.reverse10_eq
#check Agent109.step_eq_evalL_pair
#check Agent109.Canon
#check Agent109.evalL_pos_of_canon
#check Agent109.digits_evalL
#check Agent109.evalL_norm
#check Agent109.LastPos
#check Agent109.canon_normalize
#check Agent109.bounded_pair_digits
#check Agent109.canon_digits
#check Agent109.canon_last_pos
#check Agent109.pair_last
#check Agent109.lastPos_pairWord
#check Agent109.pairWord_step
#check Agent109.pairWord_orbit
#check Agent109.orbit_succ_value
#check Agent109.actual_template_step
#check Agent109.canon_iff
#check Agent109.evalL_lt
#check Agent109.evalL_ge
#check Agent109.palindrome_iff
#check Agent109.step_palindrome_iff
#check Agent109.actual_template_palindrome_iff
#check Agent109.Cert.append_inj_left'
#check Agent109.Cert.shape_reverse
#check Agent109.Cert.shape_palindrome_iff
#check Agent109.Cert.StepPal
#check Agent109.Cert.step_palindrome_template
#check Agent109.Cert.template_trim
#check Agent109.Cert.State
#check Agent109.Cert.Link
#check Agent109.Cert.Certificate
#check Agent109.Cert.gam
#check Agent109.Cert.LocalOK
#check Agent109.Cert.Certificate.P
#check Agent109.Cert.Certificate.st
#check Agent109.Cert.Certificate.lk
#check Agent109.Cert.Valid
#check Agent109.Cert.check
#check Agent109.Cert.check_sound
#check Agent109.Cert.Inv
#check Agent109.Cert.inv_not_palindrome
#check Agent109.Cert.inv_step
#check Agent109.Cert.certificate_sound
#check Agent109.Cert.Mirr
#check Agent109.Cert.realize
#check Agent109.Cert.mirr_wrap
#check Agent109.Cert.template_mirr
#check Agent109.Cert.template_lastPos
#check Agent109.Cert.template_bounded
#check Agent109.Cert.template_realized
#check Agent109.Cert.Admissible0
#check Agent109.Cert.mirr_of_split
#check Agent109.Cert.certificate_existence
#check P196.Agent7.Finite.Outer
#check P196.Agent7.Finite.normalize
#check P196.Agent7.Finite.bulkPhase
#check P196.Agent7.Finite.stripSuffix
#check P196.Agent7.Finite.outerNext
#check P196.Agent7.Finite.decodeWord
#check P196.Agent7.Finite.encoded
#check P196.Agent7.Finite.validOuter
#check P196.Agent7.Finite.staysSmall
#check P196.Agent7.Finite.cap2_exits_by_seven
#check P196.Agent7.Finite.sharpStart
#check P196.Agent7.Finite.cap2_sharp_six
#check P196.Agent7.Finite.cap2_sharp_seven
#check P196.Agent7.Finite.decode_complete
#check P196.Agent7.Finite.cap2_unencoded
#check P196.Agent7.Finite.outerIterate
#check P196.Agent7.Finite.exit_witness_of_false
#check P196.Agent7.Finite.cap2_exit_witness
#check Agent109.Outer.normalize7_eq
#check Agent109.Outer.kOf_eq
#check Agent109.Outer.outerNext_eq
#check Agent109.Outer.stripSuffix_spec
#check Agent109.Outer.norm_digits_le
#check Agent109.Outer.zipAdd_le
#check Agent109.Outer.k_le
#check Agent109.Outer.t_le
#check Agent109.Outer.u_le
#check Agent109.Outer.succ_bounded
#check Agent109.Outer.bounded_strip
#check Agent109.Outer.actual_step_outer
#check Agent109.Outer.outerIter
#check Agent109.Outer.outerIterate_eq
#check Agent109.Outer.actual_outer_orbit
#check Agent109.Outer.actual_cap2_exit
#check Agent116.CertificateExterior.Realizes
#check Agent116.CertificateExterior.realizes_next
#check Agent116.CertificateExterior.realizes_all
#check Agent116.CertificateExterior.admissible_realizes_zero
#check Agent116.CertificateExterior.realized_head_positive
#check Agent116.CertificateExterior.admissible_heads_positive
#check Agent116.Exterior.stripSuffix_idempotent
#check Agent116.Exterior.stripSuffix_append_replicate
#check Agent116.Exterior.stripSuffix_length_le
#check Agent116.Exterior.stripSuffix_last
#check Agent116.Exterior.stripSuffix_head_pos
#check Agent116.Exterior.stripSuffix_bounded
#check Agent116.Exterior.Br_append_phase
#check Agent116.Exterior.Br_append_replicate
#check Agent116.Exterior.outerNext_append_replicate
#check Agent116.Exterior.outerNext_stripSuffix_eq
#check Agent116.Exterior.outerNext_of_partial_trim
#check Agent116.CertificateExterior.stateOuter
#check Agent116.CertificateExterior.local_outer_step
#check Agent116.CertificateExterior.certificate_outer_orbit
#check Agent116.CertificateExterior.certificate_phase_index
#check Agent116.CertificateExterior.stateOuter_valid
#check Agent116.CertificateExterior.EscapeAt
#check Agent116.CertificateExterior.valid_exceeds_cap
#check Agent116.CertificateExterior.accepted_admissible_exceeds_cap
#check Agent116.CertificateExterior.escapeAt_two
#check Agent116.CertificateExterior.accepted_admissible_exceeds_two
#check Agent110.Accounting.width
#check Agent110.Accounting.dg
#check Agent110.Accounting.dh
#check Agent110.Accounting.sumPrefix
#check Agent110.Accounting.totalGam
#check Agent110.Accounting.totalG
#check Agent110.Accounting.totalH
#check Agent110.Accounting.totalJ
#check Agent110.Accounting.totalJ1
#check Agent110.Accounting.totalJ2
#check Agent110.Accounting.totalK
#check Agent110.Accounting.sumPrefix_congr
#check Agent110.Accounting.sumPrefix_add
#check Agent110.Accounting.sumPrefix_sub
#check Agent110.Accounting.sumPrefix_two_mul
#check Agent110.Accounting.sumPrefix_one
#check Agent110.Accounting.sumPrefix_two
#check Agent110.Accounting.sumPrefix_le
#check Agent110.Accounting.sumPrefix_difference
#check Agent110.Accounting.sumPrefix_cyclic_difference
#check Agent110.Accounting.Br_length
#check Agent110.Accounting.Ar_length
#check Agent110.Accounting.Cr_length
#check Agent110.Accounting.local_width_balance
#check Agent110.Accounting.local_outer_lower
#check Agent110.Accounting.local_inner_lower
#check Agent110.Accounting.local_B_length_difference
#check Agent110.Accounting.local_A_length_difference
#check Agent110.Accounting.local_C_length_difference
#check Agent110.Accounting.totalJ_eq_period
#check Agent110.Accounting.totalJ1_add_totalJ2
#check Agent110.Accounting.two_totalK
#check Agent110.Accounting.totalG_eq_trim_counts
#check Agent110.Accounting.totalH_eq_trim_counts
#check Agent110.Accounting.totalG_eq_totalJ1
#check Agent110.Accounting.totalH_eq_totalK_sub_totalJ1
#check Agent110.Accounting.totalGam_eq_twice_gains
#check Agent110.Accounting.totalG_nonneg
#check Agent110.Accounting.totalH_nonneg
#check Agent110.Accounting.totalGam_even
#check Agent110.Accounting.checked_accounting
#check Agent115.ExteriorFactorization.lowValue
#check Agent115.ExteriorFactorization.zValue
#check Agent115.ExteriorFactorization.highValue
#check Agent115.ExteriorFactorization.rhoNum
#check Agent115.ExteriorFactorization.nonneutralPhase
#check Agent115.ExteriorFactorization.Target
#check Agent115.ExteriorFactorization.digitsOf
#check Agent115.ExteriorFactorization.digitsOf_length
#check Agent115.ExteriorFactorization.normalize_eq
#check Agent115.ExteriorFactorization.normalize_length
#check Agent115.ExteriorFactorization.lowValue_append
#check Agent115.ExteriorFactorization.highValue_append_single
#check Agent115.ExteriorFactorization.foldl_high
#check Agent115.ExteriorFactorization.lowValue_reverse
#check Agent115.ExteriorFactorization.normalize_carry_le
#check Agent115.ExteriorFactorization.normalize_append_single
#check Agent115.ExteriorFactorization.fromScans
#check Agent115.ExteriorFactorization.outerNext_eq_fromScans
#check Agent115.ExteriorFactorization.stripSuffix_append_single
#check Agent115.ExteriorFactorization.zipWith_append_single
#check Agent115.ExteriorFactorization.strip_zip_append
#check Agent115.ExteriorFactorization.phase_facts
#check Agent115.ExteriorFactorization.outerNext_append_band
#check Agent115.ExteriorFactorization.outerNext_append_replicate
#check Agent115.ExteriorFactorization.outerNext_of_values
#check Agent115.ExteriorFactorization.zValue_append_band
#check Agent115.ExteriorFactorization.zValue_append_replicate
#check Agent115.ExteriorFactorization.rhoNum_append_band
#check Agent115.ExteriorFactorization.rhoNum_append_replicate
#check Agent115.ExteriorFactorization.lowValue_of_zValue
#check Agent115.ExteriorFactorization.entries_le_of_valid
#check Agent115.ExteriorFactorization.factorization_le
#check Agent115.ExteriorFactorization.target
#check Agent115.ExteriorFactorization.factorization_general
#check Agent115.ExteriorFactorization.highValue_cons
#check Agent115.ExteriorFactorization.highValue_lt
#check Agent115.ExteriorFactorization.eq_of_values
#check Agent115.ExteriorFactorization.canonical_eq_le
#check Agent115.ExteriorFactorization.last_ne_of_valid
#check Agent115.ExteriorFactorization.observation_injective
#check Agent115.ExteriorFactorization.revN
#check Agent115.ExteriorFactorization.rawSucc
#check Agent115.ExteriorFactorization.outerNext_eq_strip
#check Agent115.ExteriorFactorization.lowValue_digitsOf
#check Agent115.ExteriorFactorization.lowValue_zipWith
#check Agent115.ExteriorFactorization.length_zipWith_eq
#check Agent115.ExteriorFactorization.highValue_zipWith
#check Agent115.ExteriorFactorization.lowValue_append_single
#check Agent115.ExteriorFactorization.highValue_reverse
#check Agent115.ExteriorFactorization.rawSucc_values
#check Agent115.ExteriorFactorization.takeWhile_eq_mem
#check Agent115.ExteriorFactorization.stripSuffix_spec
#check Agent115.ExteriorFactorization.rawSucc_length
#check Agent115.ExteriorFactorization.successor_observation
#check Agent6.ExteriorCoordinates.betaNum
#check Agent6.ExteriorCoordinates.betaNum_eq
#check Agent6.ExteriorCoordinates.highContribution
#check Agent6.ExteriorCoordinates.betaNum_outerNext_raw
#check Agent6.ExteriorCoordinates.betaNum_outerNext
#check Agent6.ExteriorCoordinates.phaseCarry
#check Agent6.ExteriorCoordinates.phaseDigit
#check Agent6.ExteriorCoordinates.overflow
#check Agent6.ExteriorCoordinates.phaseCarry_le_one
#check Agent6.ExteriorCoordinates.phaseCarry_eq_div_nine
#check Agent6.ExteriorCoordinates.phaseDigit_identity
#check Agent6.ExteriorCoordinates.phaseDigit_le_eight
#check Agent6.ExteriorCoordinates.phaseDigit_pos
#check Agent6.ExteriorCoordinates.overflow_eq_highValue
#check Agent6.ExteriorCoordinates.overflow_eq_rho_quotient
#check Agent6.ExteriorCoordinates.overflow_le_one
#check Agent6.ExteriorCoordinates.overflow_eq_zero_iff
#check Agent6.ExteriorCoordinates.overflow_eq_one_iff
#check Agent6.ExteriorCoordinates.rhoNum_lt_twice_denominator
#check Agent6.ExteriorCoordinates.empty_word_coordinates
#check Agent6.ExteriorCoordinates.empty_word_quotient_iff
#check Agent6.ExteriorCoordinates.quotient_identity_forall_iff
#check Agent6.ExteriorCoordinates.excluded_phase_controls
#check Agent6.ExteriorCoordinates.unbounded_coefficient_control
#check Agent6.ExteriorCoordinates.revN_lt_power
#check Agent6.ExteriorCoordinates.highContribution_emod_ten_of_overflow_ne_zero
#check Agent6.ExteriorCoordinates.highContribution_ne_zero_of_pos
#check Agent6.ExteriorCoordinates.highContribution_ne_zero_of_nonneutral
#check Agent6.ExteriorCoordinates.zero_phase_empty_control
#check Agent6.ExteriorCoordinates.zero_overflow_negative_control
#check Agent6.ExteriorCoordinates.zero_overflow_positive_control
#check Agent6.ExteriorCoordinates.one_overflow_negative_control
#check Agent6.ExteriorCoordinates.one_overflow_positive_control
#check Agent6.ExteriorCoordinates.both_signs_at_zero_overflow
#check Agent6.ExteriorCoordinates.both_signs_at_one_overflow
#check Agent6.ExteriorCoordinates.outerIter
#check Agent6.ExteriorCoordinates.orbitSum
#check Agent6.ExteriorCoordinates.contributionSum
#check Agent6.ExteriorCoordinates.outerIter_zero
#check Agent6.ExteriorCoordinates.outerIter_succ
#check Agent6.ExteriorCoordinates.orbitSum_zero
#check Agent6.ExteriorCoordinates.orbitSum_succ
#check Agent6.ExteriorCoordinates.contributionSum_zero
#check Agent6.ExteriorCoordinates.contributionSum_succ
#check Agent6.ExteriorCoordinates.orbitSum_telescope
#check Agent6.ExteriorCoordinates.betaNum_outerIter
#check Agent6.ExteriorCoordinates.contributionSum_eq_betaNum_sub
#check Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_beta_return
#check Agent6.ExteriorCoordinates.closed_orbit_contributionSum_eq_zero
#check Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_padding_return
#check Agent6.ExteriorCoordinates.outerIter_eq_chain
#check Agent6.ExteriorCoordinates.contributionSum_eq_chain_betaNum_sub
#check Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonneg
#check Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonpos
#check Agent6.ExteriorCoordinates.orbitSum_zero_both_signs
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_initial_ne_zero
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_pos
#check Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_nonneutral
#check Agent6.ExteriorCoordinates.overflowBit
#check Agent6.ExteriorCoordinates.carryScale
#check Agent6.ExteriorCoordinates.weightedReverse
#check Agent6.ExteriorCoordinates.weightedPhase
#check Agent6.ExteriorCoordinates.overflowCount
#check Agent6.ExteriorCoordinates.overflowBit_le_one
#check Agent6.ExteriorCoordinates.carryScale_eq
#check Agent6.ExteriorCoordinates.overflowCount_zero
#check Agent6.ExteriorCoordinates.overflowCount_succ
#check Agent6.ExteriorCoordinates.overflowCount_le
#check Agent6.ExteriorCoordinates.highContribution_eq_weighted
#check Agent6.ExteriorCoordinates.contributionSum_eq_weighted
#check Agent6.ExteriorCoordinates.closed_orbit_weighted_balance
#check Agent6.CertificateCoordinates.rowOuter
#check Agent6.CertificateCoordinates.rowContribution
#check Agent6.CertificateCoordinates.rowContributionSum
#check Agent6.CertificateCoordinates.rowOuter_orbit
#check Agent6.CertificateCoordinates.rowOuter_orbit_of_lt
#check Agent6.CertificateCoordinates.rowOuter_closed
#check Agent6.CertificateCoordinates.rowSum_eq_orbitSum
#check Agent6.CertificateCoordinates.rowContributionSum_eq_contributionSum
#check Agent6.CertificateCoordinates.valid_row_contribution_sum_eq_zero
#check Agent6.CertificateCoordinates.checked_row_contribution_sum_eq_zero
#check Agent6.CertificateCoordinates.valid_row_both_signs
#check Agent6.CertificateCoordinates.checked_row_both_signs
#check Agent6.CertificateCoordinates.checked_coordinate_conditions
#check Agent6.CertificateCoordinates.checked_row_weighted_balance
#check Agent6.CertificateFilter.coordinateFilter
#check Agent6.CertificateFilter.coordinateFilter_eq_true_iff
#check Agent6.CertificateFilter.checked_coordinateFilter
#check Agent6.CertificateFilter.check_eq_false_of_coordinateFilter_eq_false
#check Agent6.CertificateFilter.period_pos_of_coordinateFilter
#check Agent6.CertificateFilter.coordinateFilter_eq_false_of_period_zero
#check Agent6.CertificateFilter.filteredCheck
#check Agent6.CertificateFilter.filteredCheck_eq_check
#check Agent6.CertificateControls.controlLink
#check Agent6.CertificateControls.cancellationCandidate
#check Agent6.CertificateControls.cancellationCandidate_period
#check Agent6.CertificateControls.cancellationCandidate_link_count
#check Agent6.CertificateControls.cancellationCandidate_rows
#check Agent6.CertificateControls.cancellationCandidate_contributions
#check Agent6.CertificateControls.cancellationCandidate_sum_zero
#check Agent6.CertificateControls.cancellationCandidate_filter_passes
#check Agent6.CertificateControls.cancellationCandidate_first_phase_failure
#check Agent6.CertificateControls.cancellationCandidate_check_false
#check Agent6.CertificateControls.cancellationCandidate_filteredCheck_false
#check Agent6.CertificateControls.coordinateFilter_not_sufficient
#check Agent6.CertificateControls.emptyCandidate
#check Agent6.CertificateControls.emptyCandidate_boundary
#check Agent6.CertificateControls.zeroPhaseCandidate
#check Agent6.CertificateControls.zeroPhaseCandidate_boundary
#print axioms Agent109.Word
#print axioms Agent109.zipAdd
#print axioms Agent109.pair
#print axioms Agent109.normalize
#print axioms Agent109.stepWord
#print axioms Agent109.template
#print axioms Agent109.zipAdd_eq_zipWith
#print axioms Agent109.zipAdd_append
#print axioms Agent109.zipAdd_length
#print axioms Agent109.zipAdd_comm
#print axioms Agent109.zipAdd_reverse
#print axioms Agent109.zipAdd_replicate
#print axioms Agent109.norm
#print axioms Agent109.carryWord
#print axioms Agent109.normalize_eq_norm
#print axioms Agent109.norm_length
#print axioms Agent109.norm_append
#print axioms Agent109.Bounded
#print axioms Agent109.norm_carry_le
#print axioms Agent109.norm_digit_lt
#print axioms Agent109.kOf
#print axioms Agent109.tOf
#print axioms Agent109.Phase
#print axioms Agent109.norm_band_tail
#print axioms Agent109.norm_band
#print axioms Agent109.complement_k
#print axioms Agent109.complement_t
#print axioms Agent109.complement_phase
#print axioms Agent109.next_phase
#print axioms Agent109.next_complement
#print axioms Agent109.Data
#print axioms Agent109.data
#print axioms Agent109.u0
#print axioms Agent109.u1
#print axioms Agent109.u2
#print axioms Agent109.u3
#print axioms Agent109.digitWord
#print axioms Agent109.bounded_reverse
#print axioms Agent109.norm_template
#print axioms Agent109.normalize_template
#print axioms Agent109.gamma_le
#print axioms Agent109.pair_split
#print axioms Agent109.Br
#print axioms Agent109.Ar
#print axioms Agent109.Cr
#print axioms Agent109.stepWord_template
#print axioms Agent109.reverseAux
#print axioms Agent109.reverseFuel
#print axioms Agent109.reverse10
#print axioms Agent109.Palindrome
#print axioms Agent109.step
#print axioms Agent109.orbitWord
#print axioms Agent109.orbit
#print axioms Agent109.evalL
#print axioms Agent109.digitsFuel
#print axioms Agent109.digits
#print axioms Agent109.pairWord
#print axioms Agent109.digitsFuel_stable
#print axioms Agent109.digits_zero
#print axioms Agent109.digits_pos
#print axioms Agent109.evalL_digits
#print axioms Agent109.evalL_append
#print axioms Agent109.evalL_zipAdd
#print axioms Agent109.reverseFuel_digits
#print axioms Agent109.reverse10_eq
#print axioms Agent109.step_eq_evalL_pair
#print axioms Agent109.Canon
#print axioms Agent109.evalL_pos_of_canon
#print axioms Agent109.digits_evalL
#print axioms Agent109.evalL_norm
#print axioms Agent109.LastPos
#print axioms Agent109.canon_normalize
#print axioms Agent109.bounded_pair_digits
#print axioms Agent109.canon_digits
#print axioms Agent109.canon_last_pos
#print axioms Agent109.pair_last
#print axioms Agent109.lastPos_pairWord
#print axioms Agent109.pairWord_step
#print axioms Agent109.pairWord_orbit
#print axioms Agent109.orbit_succ_value
#print axioms Agent109.actual_template_step
#print axioms Agent109.canon_iff
#print axioms Agent109.evalL_lt
#print axioms Agent109.evalL_ge
#print axioms Agent109.palindrome_iff
#print axioms Agent109.step_palindrome_iff
#print axioms Agent109.actual_template_palindrome_iff
#print axioms Agent109.Cert.append_inj_left'
#print axioms Agent109.Cert.shape_reverse
#print axioms Agent109.Cert.shape_palindrome_iff
#print axioms Agent109.Cert.StepPal
#print axioms Agent109.Cert.step_palindrome_template
#print axioms Agent109.Cert.template_trim
#print axioms Agent109.Cert.State
#print axioms Agent109.Cert.Link
#print axioms Agent109.Cert.Certificate
#print axioms Agent109.Cert.gam
#print axioms Agent109.Cert.LocalOK
#print axioms Agent109.Cert.Certificate.P
#print axioms Agent109.Cert.Certificate.st
#print axioms Agent109.Cert.Certificate.lk
#print axioms Agent109.Cert.Valid
#print axioms Agent109.Cert.check
#print axioms Agent109.Cert.check_sound
#print axioms Agent109.Cert.Inv
#print axioms Agent109.Cert.inv_not_palindrome
#print axioms Agent109.Cert.inv_step
#print axioms Agent109.Cert.certificate_sound
#print axioms Agent109.Cert.Mirr
#print axioms Agent109.Cert.realize
#print axioms Agent109.Cert.mirr_wrap
#print axioms Agent109.Cert.template_mirr
#print axioms Agent109.Cert.template_lastPos
#print axioms Agent109.Cert.template_bounded
#print axioms Agent109.Cert.template_realized
#print axioms Agent109.Cert.Admissible0
#print axioms Agent109.Cert.mirr_of_split
#print axioms Agent109.Cert.certificate_existence
#print axioms P196.Agent7.Finite.Outer
#print axioms P196.Agent7.Finite.normalize
#print axioms P196.Agent7.Finite.bulkPhase
#print axioms P196.Agent7.Finite.stripSuffix
#print axioms P196.Agent7.Finite.outerNext
#print axioms P196.Agent7.Finite.decodeWord
#print axioms P196.Agent7.Finite.encoded
#print axioms P196.Agent7.Finite.validOuter
#print axioms P196.Agent7.Finite.staysSmall
#print axioms P196.Agent7.Finite.cap2_exits_by_seven
#print axioms P196.Agent7.Finite.sharpStart
#print axioms P196.Agent7.Finite.cap2_sharp_six
#print axioms P196.Agent7.Finite.cap2_sharp_seven
#print axioms P196.Agent7.Finite.decode_complete
#print axioms P196.Agent7.Finite.cap2_unencoded
#print axioms P196.Agent7.Finite.outerIterate
#print axioms P196.Agent7.Finite.exit_witness_of_false
#print axioms P196.Agent7.Finite.cap2_exit_witness
#print axioms Agent109.Outer.normalize7_eq
#print axioms Agent109.Outer.kOf_eq
#print axioms Agent109.Outer.outerNext_eq
#print axioms Agent109.Outer.stripSuffix_spec
#print axioms Agent109.Outer.norm_digits_le
#print axioms Agent109.Outer.zipAdd_le
#print axioms Agent109.Outer.k_le
#print axioms Agent109.Outer.t_le
#print axioms Agent109.Outer.u_le
#print axioms Agent109.Outer.succ_bounded
#print axioms Agent109.Outer.bounded_strip
#print axioms Agent109.Outer.actual_step_outer
#print axioms Agent109.Outer.outerIter
#print axioms Agent109.Outer.outerIterate_eq
#print axioms Agent109.Outer.actual_outer_orbit
#print axioms Agent109.Outer.actual_cap2_exit
#print axioms Agent116.CertificateExterior.Realizes
#print axioms Agent116.CertificateExterior.realizes_next
#print axioms Agent116.CertificateExterior.realizes_all
#print axioms Agent116.CertificateExterior.admissible_realizes_zero
#print axioms Agent116.CertificateExterior.realized_head_positive
#print axioms Agent116.CertificateExterior.admissible_heads_positive
#print axioms Agent116.Exterior.stripSuffix_idempotent
#print axioms Agent116.Exterior.stripSuffix_append_replicate
#print axioms Agent116.Exterior.stripSuffix_length_le
#print axioms Agent116.Exterior.stripSuffix_last
#print axioms Agent116.Exterior.stripSuffix_head_pos
#print axioms Agent116.Exterior.stripSuffix_bounded
#print axioms Agent116.Exterior.Br_append_phase
#print axioms Agent116.Exterior.Br_append_replicate
#print axioms Agent116.Exterior.outerNext_append_replicate
#print axioms Agent116.Exterior.outerNext_stripSuffix_eq
#print axioms Agent116.Exterior.outerNext_of_partial_trim
#print axioms Agent116.CertificateExterior.stateOuter
#print axioms Agent116.CertificateExterior.local_outer_step
#print axioms Agent116.CertificateExterior.certificate_outer_orbit
#print axioms Agent116.CertificateExterior.certificate_phase_index
#print axioms Agent116.CertificateExterior.stateOuter_valid
#print axioms Agent116.CertificateExterior.EscapeAt
#print axioms Agent116.CertificateExterior.valid_exceeds_cap
#print axioms Agent116.CertificateExterior.accepted_admissible_exceeds_cap
#print axioms Agent116.CertificateExterior.escapeAt_two
#print axioms Agent116.CertificateExterior.accepted_admissible_exceeds_two
#print axioms Agent110.Accounting.width
#print axioms Agent110.Accounting.dg
#print axioms Agent110.Accounting.dh
#print axioms Agent110.Accounting.sumPrefix
#print axioms Agent110.Accounting.totalGam
#print axioms Agent110.Accounting.totalG
#print axioms Agent110.Accounting.totalH
#print axioms Agent110.Accounting.totalJ
#print axioms Agent110.Accounting.totalJ1
#print axioms Agent110.Accounting.totalJ2
#print axioms Agent110.Accounting.totalK
#print axioms Agent110.Accounting.sumPrefix_congr
#print axioms Agent110.Accounting.sumPrefix_add
#print axioms Agent110.Accounting.sumPrefix_sub
#print axioms Agent110.Accounting.sumPrefix_two_mul
#print axioms Agent110.Accounting.sumPrefix_one
#print axioms Agent110.Accounting.sumPrefix_two
#print axioms Agent110.Accounting.sumPrefix_le
#print axioms Agent110.Accounting.sumPrefix_difference
#print axioms Agent110.Accounting.sumPrefix_cyclic_difference
#print axioms Agent110.Accounting.Br_length
#print axioms Agent110.Accounting.Ar_length
#print axioms Agent110.Accounting.Cr_length
#print axioms Agent110.Accounting.local_width_balance
#print axioms Agent110.Accounting.local_outer_lower
#print axioms Agent110.Accounting.local_inner_lower
#print axioms Agent110.Accounting.local_B_length_difference
#print axioms Agent110.Accounting.local_A_length_difference
#print axioms Agent110.Accounting.local_C_length_difference
#print axioms Agent110.Accounting.totalJ_eq_period
#print axioms Agent110.Accounting.totalJ1_add_totalJ2
#print axioms Agent110.Accounting.two_totalK
#print axioms Agent110.Accounting.totalG_eq_trim_counts
#print axioms Agent110.Accounting.totalH_eq_trim_counts
#print axioms Agent110.Accounting.totalG_eq_totalJ1
#print axioms Agent110.Accounting.totalH_eq_totalK_sub_totalJ1
#print axioms Agent110.Accounting.totalGam_eq_twice_gains
#print axioms Agent110.Accounting.totalG_nonneg
#print axioms Agent110.Accounting.totalH_nonneg
#print axioms Agent110.Accounting.totalGam_even
#print axioms Agent110.Accounting.checked_accounting
#print axioms Agent115.ExteriorFactorization.lowValue
#print axioms Agent115.ExteriorFactorization.zValue
#print axioms Agent115.ExteriorFactorization.highValue
#print axioms Agent115.ExteriorFactorization.rhoNum
#print axioms Agent115.ExteriorFactorization.nonneutralPhase
#print axioms Agent115.ExteriorFactorization.Target
#print axioms Agent115.ExteriorFactorization.digitsOf
#print axioms Agent115.ExteriorFactorization.digitsOf_length
#print axioms Agent115.ExteriorFactorization.normalize_eq
#print axioms Agent115.ExteriorFactorization.normalize_length
#print axioms Agent115.ExteriorFactorization.lowValue_append
#print axioms Agent115.ExteriorFactorization.highValue_append_single
#print axioms Agent115.ExteriorFactorization.foldl_high
#print axioms Agent115.ExteriorFactorization.lowValue_reverse
#print axioms Agent115.ExteriorFactorization.normalize_carry_le
#print axioms Agent115.ExteriorFactorization.normalize_append_single
#print axioms Agent115.ExteriorFactorization.fromScans
#print axioms Agent115.ExteriorFactorization.outerNext_eq_fromScans
#print axioms Agent115.ExteriorFactorization.stripSuffix_append_single
#print axioms Agent115.ExteriorFactorization.zipWith_append_single
#print axioms Agent115.ExteriorFactorization.strip_zip_append
#print axioms Agent115.ExteriorFactorization.phase_facts
#print axioms Agent115.ExteriorFactorization.outerNext_append_band
#print axioms Agent115.ExteriorFactorization.outerNext_append_replicate
#print axioms Agent115.ExteriorFactorization.outerNext_of_values
#print axioms Agent115.ExteriorFactorization.zValue_append_band
#print axioms Agent115.ExteriorFactorization.zValue_append_replicate
#print axioms Agent115.ExteriorFactorization.rhoNum_append_band
#print axioms Agent115.ExteriorFactorization.rhoNum_append_replicate
#print axioms Agent115.ExteriorFactorization.lowValue_of_zValue
#print axioms Agent115.ExteriorFactorization.entries_le_of_valid
#print axioms Agent115.ExteriorFactorization.factorization_le
#print axioms Agent115.ExteriorFactorization.target
#print axioms Agent115.ExteriorFactorization.factorization_general
#print axioms Agent115.ExteriorFactorization.highValue_cons
#print axioms Agent115.ExteriorFactorization.highValue_lt
#print axioms Agent115.ExteriorFactorization.eq_of_values
#print axioms Agent115.ExteriorFactorization.canonical_eq_le
#print axioms Agent115.ExteriorFactorization.last_ne_of_valid
#print axioms Agent115.ExteriorFactorization.observation_injective
#print axioms Agent115.ExteriorFactorization.revN
#print axioms Agent115.ExteriorFactorization.rawSucc
#print axioms Agent115.ExteriorFactorization.outerNext_eq_strip
#print axioms Agent115.ExteriorFactorization.lowValue_digitsOf
#print axioms Agent115.ExteriorFactorization.lowValue_zipWith
#print axioms Agent115.ExteriorFactorization.length_zipWith_eq
#print axioms Agent115.ExteriorFactorization.highValue_zipWith
#print axioms Agent115.ExteriorFactorization.lowValue_append_single
#print axioms Agent115.ExteriorFactorization.highValue_reverse
#print axioms Agent115.ExteriorFactorization.rawSucc_values
#print axioms Agent115.ExteriorFactorization.takeWhile_eq_mem
#print axioms Agent115.ExteriorFactorization.stripSuffix_spec
#print axioms Agent115.ExteriorFactorization.rawSucc_length
#print axioms Agent115.ExteriorFactorization.successor_observation
#print axioms Agent6.ExteriorCoordinates.betaNum
#print axioms Agent6.ExteriorCoordinates.betaNum_eq
#print axioms Agent6.ExteriorCoordinates.highContribution
#print axioms Agent6.ExteriorCoordinates.betaNum_outerNext_raw
#print axioms Agent6.ExteriorCoordinates.betaNum_outerNext
#print axioms Agent6.ExteriorCoordinates.phaseCarry
#print axioms Agent6.ExteriorCoordinates.phaseDigit
#print axioms Agent6.ExteriorCoordinates.overflow
#print axioms Agent6.ExteriorCoordinates.phaseCarry_le_one
#print axioms Agent6.ExteriorCoordinates.phaseCarry_eq_div_nine
#print axioms Agent6.ExteriorCoordinates.phaseDigit_identity
#print axioms Agent6.ExteriorCoordinates.phaseDigit_le_eight
#print axioms Agent6.ExteriorCoordinates.phaseDigit_pos
#print axioms Agent6.ExteriorCoordinates.overflow_eq_highValue
#print axioms Agent6.ExteriorCoordinates.overflow_eq_rho_quotient
#print axioms Agent6.ExteriorCoordinates.overflow_le_one
#print axioms Agent6.ExteriorCoordinates.overflow_eq_zero_iff
#print axioms Agent6.ExteriorCoordinates.overflow_eq_one_iff
#print axioms Agent6.ExteriorCoordinates.rhoNum_lt_twice_denominator
#print axioms Agent6.ExteriorCoordinates.empty_word_coordinates
#print axioms Agent6.ExteriorCoordinates.empty_word_quotient_iff
#print axioms Agent6.ExteriorCoordinates.quotient_identity_forall_iff
#print axioms Agent6.ExteriorCoordinates.excluded_phase_controls
#print axioms Agent6.ExteriorCoordinates.unbounded_coefficient_control
#print axioms Agent6.ExteriorCoordinates.revN_lt_power
#print axioms Agent6.ExteriorCoordinates.highContribution_emod_ten_of_overflow_ne_zero
#print axioms Agent6.ExteriorCoordinates.highContribution_ne_zero_of_pos
#print axioms Agent6.ExteriorCoordinates.highContribution_ne_zero_of_nonneutral
#print axioms Agent6.ExteriorCoordinates.zero_phase_empty_control
#print axioms Agent6.ExteriorCoordinates.zero_overflow_negative_control
#print axioms Agent6.ExteriorCoordinates.zero_overflow_positive_control
#print axioms Agent6.ExteriorCoordinates.one_overflow_negative_control
#print axioms Agent6.ExteriorCoordinates.one_overflow_positive_control
#print axioms Agent6.ExteriorCoordinates.both_signs_at_zero_overflow
#print axioms Agent6.ExteriorCoordinates.both_signs_at_one_overflow
#print axioms Agent6.ExteriorCoordinates.outerIter
#print axioms Agent6.ExteriorCoordinates.orbitSum
#print axioms Agent6.ExteriorCoordinates.contributionSum
#print axioms Agent6.ExteriorCoordinates.outerIter_zero
#print axioms Agent6.ExteriorCoordinates.outerIter_succ
#print axioms Agent6.ExteriorCoordinates.orbitSum_zero
#print axioms Agent6.ExteriorCoordinates.orbitSum_succ
#print axioms Agent6.ExteriorCoordinates.contributionSum_zero
#print axioms Agent6.ExteriorCoordinates.contributionSum_succ
#print axioms Agent6.ExteriorCoordinates.orbitSum_telescope
#print axioms Agent6.ExteriorCoordinates.betaNum_outerIter
#print axioms Agent6.ExteriorCoordinates.contributionSum_eq_betaNum_sub
#print axioms Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_beta_return
#print axioms Agent6.ExteriorCoordinates.closed_orbit_contributionSum_eq_zero
#print axioms Agent6.ExteriorCoordinates.contributionSum_eq_zero_of_padding_return
#print axioms Agent6.ExteriorCoordinates.outerIter_eq_chain
#print axioms Agent6.ExteriorCoordinates.contributionSum_eq_chain_betaNum_sub
#print axioms Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonneg
#print axioms Agent6.ExteriorCoordinates.orbitSum_eq_zero_of_nonpos
#print axioms Agent6.ExteriorCoordinates.orbitSum_zero_both_signs
#print axioms Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_initial_ne_zero
#print axioms Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_pos
#print axioms Agent6.ExteriorCoordinates.closed_orbit_both_signs_of_nonneutral
#print axioms Agent6.ExteriorCoordinates.overflowBit
#print axioms Agent6.ExteriorCoordinates.carryScale
#print axioms Agent6.ExteriorCoordinates.weightedReverse
#print axioms Agent6.ExteriorCoordinates.weightedPhase
#print axioms Agent6.ExteriorCoordinates.overflowCount
#print axioms Agent6.ExteriorCoordinates.overflowBit_le_one
#print axioms Agent6.ExteriorCoordinates.carryScale_eq
#print axioms Agent6.ExteriorCoordinates.overflowCount_zero
#print axioms Agent6.ExteriorCoordinates.overflowCount_succ
#print axioms Agent6.ExteriorCoordinates.overflowCount_le
#print axioms Agent6.ExteriorCoordinates.highContribution_eq_weighted
#print axioms Agent6.ExteriorCoordinates.contributionSum_eq_weighted
#print axioms Agent6.ExteriorCoordinates.closed_orbit_weighted_balance
#print axioms Agent6.CertificateCoordinates.rowOuter
#print axioms Agent6.CertificateCoordinates.rowContribution
#print axioms Agent6.CertificateCoordinates.rowContributionSum
#print axioms Agent6.CertificateCoordinates.rowOuter_orbit
#print axioms Agent6.CertificateCoordinates.rowOuter_orbit_of_lt
#print axioms Agent6.CertificateCoordinates.rowOuter_closed
#print axioms Agent6.CertificateCoordinates.rowSum_eq_orbitSum
#print axioms Agent6.CertificateCoordinates.rowContributionSum_eq_contributionSum
#print axioms Agent6.CertificateCoordinates.valid_row_contribution_sum_eq_zero
#print axioms Agent6.CertificateCoordinates.checked_row_contribution_sum_eq_zero
#print axioms Agent6.CertificateCoordinates.valid_row_both_signs
#print axioms Agent6.CertificateCoordinates.checked_row_both_signs
#print axioms Agent6.CertificateCoordinates.checked_coordinate_conditions
#print axioms Agent6.CertificateCoordinates.checked_row_weighted_balance
#print axioms Agent6.CertificateFilter.coordinateFilter
#print axioms Agent6.CertificateFilter.coordinateFilter_eq_true_iff
#print axioms Agent6.CertificateFilter.checked_coordinateFilter
#print axioms Agent6.CertificateFilter.check_eq_false_of_coordinateFilter_eq_false
#print axioms Agent6.CertificateFilter.period_pos_of_coordinateFilter
#print axioms Agent6.CertificateFilter.coordinateFilter_eq_false_of_period_zero
#print axioms Agent6.CertificateFilter.filteredCheck
#print axioms Agent6.CertificateFilter.filteredCheck_eq_check
#print axioms Agent6.CertificateControls.controlLink
#print axioms Agent6.CertificateControls.cancellationCandidate
#print axioms Agent6.CertificateControls.cancellationCandidate_period
#print axioms Agent6.CertificateControls.cancellationCandidate_link_count
#print axioms Agent6.CertificateControls.cancellationCandidate_rows
#print axioms Agent6.CertificateControls.cancellationCandidate_contributions
#print axioms Agent6.CertificateControls.cancellationCandidate_sum_zero
#print axioms Agent6.CertificateControls.cancellationCandidate_filter_passes
#print axioms Agent6.CertificateControls.cancellationCandidate_first_phase_failure
#print axioms Agent6.CertificateControls.cancellationCandidate_check_false
#print axioms Agent6.CertificateControls.cancellationCandidate_filteredCheck_false
#print axioms Agent6.CertificateControls.coordinateFilter_not_sufficient
#print axioms Agent6.CertificateControls.emptyCandidate
#print axioms Agent6.CertificateControls.emptyCandidate_boundary
#print axioms Agent6.CertificateControls.zeroPhaseCandidate
#print axioms Agent6.CertificateControls.zeroPhaseCandidate_boundary
