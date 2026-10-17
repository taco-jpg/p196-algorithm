import ActualCarrySupport

set_option pp.all true
set_option pp.proofs true
set_option pp.deepTerms true
set_option pp.maxSteps 1000000
set_option maxRecDepth 100000
set_option maxHeartbeats 0

#print P196.Agent15.SpectralSupport.outgoing
#print axioms P196.Agent15.SpectralSupport.outgoing
#print P196.Agent15.SpectralSupport.actualCharge
#print axioms P196.Agent15.SpectralSupport.actualCharge
#print P196.Agent15.SpectralSupport.outgoing_length
#print axioms P196.Agent15.SpectralSupport.outgoing_length
#print P196.Agent15.SpectralSupport.outgoing_getElem
#print axioms P196.Agent15.SpectralSupport.outgoing_getElem
#print P196.Agent15.SpectralSupport.outgoing_getElem?
#print axioms P196.Agent15.SpectralSupport.outgoing_getElem?
#print P196.Agent15.SpectralSupport.outgoing_last
#print axioms P196.Agent15.SpectralSupport.outgoing_last
#print P196.Agent15.SpectralSupport.outgoing_binary
#print axioms P196.Agent15.SpectralSupport.outgoing_binary
#print P196.Agent15.SpectralSupport.outgoing_reverse_iff
#print axioms P196.Agent15.SpectralSupport.outgoing_reverse_iff
#print P196.Agent15.SpectralSupport.actualCharge_zero_iff
#print axioms P196.Agent15.SpectralSupport.actualCharge_zero_iff
#print P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine
#print axioms P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine
#print P196.Agent15.SpectralSupport.actualCharge_nonzero_iff_nine_asymmetry
#print axioms P196.Agent15.SpectralSupport.actualCharge_nonzero_iff_nine_asymmetry
#print P196.Agent15.SpectralSupport.actualCharge_zero_of_no_nine
#print axioms P196.Agent15.SpectralSupport.actualCharge_zero_of_no_nine
#print P196.Agent15.SpectralSupport.canonical_actualCharge_zero_iff
#print axioms P196.Agent15.SpectralSupport.canonical_actualCharge_zero_iff
#print P196.Agent15.SpectralSupport.canonical_outgoing_reflected_eq_of_nonnine
#print axioms P196.Agent15.SpectralSupport.canonical_outgoing_reflected_eq_of_nonnine
#print P196.Agent15.SpectralSupport.canonical_actualCharge_nonzero_iff_nine_asymmetry
#print axioms P196.Agent15.SpectralSupport.canonical_actualCharge_nonzero_iff_nine_asymmetry
#print P196.Agent15.SpectralSupport.canonical_actualCharge_zero_of_no_nine
#print axioms P196.Agent15.SpectralSupport.canonical_actualCharge_zero_of_no_nine
#print P196.Agent15.SpectralSupport.actualCharge_width_zero
#print axioms P196.Agent15.SpectralSupport.actualCharge_width_zero
#print P196.Agent15.SpectralSupport.actualCharge_width_one
#print axioms P196.Agent15.SpectralSupport.actualCharge_width_one
#print P196.Agent15.SpectralSupport.Controls.nine_zero_charge
#print axioms P196.Agent15.SpectralSupport.Controls.nine_zero_charge
#print P196.Agent15.SpectralSupport.Controls.even_overflow_zero_charge
#print axioms P196.Agent15.SpectralSupport.Controls.even_overflow_zero_charge
#print P196.Agent15.SpectralSupport.Controls.odd_free_center
#print axioms P196.Agent15.SpectralSupport.Controls.odd_free_center
#print P196.Agent15.SpectralSupport.Controls.odd_nine_asymmetry
#print axioms P196.Agent15.SpectralSupport.Controls.odd_nine_asymmetry
#print DecimalDigits.carry
#print axioms DecimalDigits.carry
#print DecimalDigits.carry_bounded
#print axioms DecimalDigits.carry_bounded
#print DecimalDigits.columnSum
#print axioms DecimalDigits.columnSum
#print DecimalDigits.columnSum_bounded
#print axioms DecimalDigits.columnSum_bounded
#print DecimalDigits.columnSum_symmetric
#print axioms DecimalDigits.columnSum_symmetric
#print DecimalDigits.Canonical
#print axioms DecimalDigits.Canonical
#print RawSymmetryObstruction.nonnine_binary_div
#print axioms RawSymmetryObstruction.nonnine_binary_div
#print P196.Agent15.SpectralCarry.Binary
#print axioms P196.Agent15.SpectralCarry.Binary
#print P196.Agent15.SpectralCarry.carryCharge
#print axioms P196.Agent15.SpectralCarry.carryCharge
#print P196.Agent15.SpectralCarry.carryCharge_zero_iff
#print axioms P196.Agent15.SpectralCarry.carryCharge_zero_iff
#print P196.Agent15.SpectralCarry.carryCharge_eq_odd_source_sum
#print axioms P196.Agent15.SpectralCarry.carryCharge_eq_odd_source_sum
#print P196.Agent15.SpectralCarry.carryCharge_eq_even_source_sum
#print axioms P196.Agent15.SpectralCarry.carryCharge_eq_even_source_sum
#print P196.Agent15.SpectralCarry.evenCharge.eq_1
#print axioms P196.Agent15.SpectralCarry.evenCharge.eq_1
#print P196.Agent15.SpectralCarry.oddCharge.eq_1
#print axioms P196.Agent15.SpectralCarry.oddCharge.eq_1
#print P196.Agent15.SpectralSupport.actualCharge.eq_1
#print axioms P196.Agent15.SpectralSupport.actualCharge.eq_1
#print P196.Agent15.SpectralSupport.outgoing.eq_1
#print axioms P196.Agent15.SpectralSupport.outgoing.eq_1
#print P196.Agent15.SpectralSupport.outgoing_binary._proof_3
#print axioms P196.Agent15.SpectralSupport.outgoing_binary._proof_3
#print P196.Agent15.SpectralSupport.outgoing_binary._proof_4
#print axioms P196.Agent15.SpectralSupport.outgoing_binary._proof_4
#print P196.Agent15.SpectralSupport.outgoing_last._proof_1
#print axioms P196.Agent15.SpectralSupport.outgoing_last._proof_1
#print P196.Agent15.SpectralSupport.outgoing_last._proof_2
#print axioms P196.Agent15.SpectralSupport.outgoing_last._proof_2
#print P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_10
#print axioms P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_10
#print P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_8
#print axioms P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_8
#print P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_9
#print axioms P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine._proof_9
#print P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_5
#print axioms P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_5
#print P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_6
#print axioms P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_6
#print P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_7
#print axioms P196.Agent15.SpectralSupport.outgoing_reverse_iff._proof_7
