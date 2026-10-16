import CoordinateThreshold
import Lean
set_option pp.universes true

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
