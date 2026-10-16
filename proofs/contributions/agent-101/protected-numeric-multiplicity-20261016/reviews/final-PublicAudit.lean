import Agent101ProtectedFamily
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0

#check Agent101.Protected.protectedSeeds
#print axioms Agent101.Protected.protectedSeeds
#check Agent101.Protected.coefficientWord_inputHalf
#print axioms Agent101.Protected.coefficientWord_inputHalf
#check Agent101.Protected.coefficientWord_inputHalf_bounded
#print axioms Agent101.Protected.coefficientWord_inputHalf_bounded
#check Agent101.Protected.mem_inputFiber
#print axioms Agent101.Protected.mem_inputFiber
#check Agent101.Protected.mem_protectedSeeds
#print axioms Agent101.Protected.mem_protectedSeeds
#check Agent101.Protected.mem_protectedSeeds_numeric
#print axioms Agent101.Protected.mem_protectedSeeds_numeric
#check Agent101.Protected.mem_protectedSeeds_width
#print axioms Agent101.Protected.mem_protectedSeeds_width
#check Agent101.Protected.mem_protectedSeeds_positive
#print axioms Agent101.Protected.mem_protectedSeeds_positive
#check Agent101.Protected.inputFiber_index_unique
#print axioms Agent101.Protected.inputFiber_index_unique
#check Agent101.Protected.inputFibers_disjoint
#print axioms Agent101.Protected.inputFibers_disjoint
#check Agent101.Protected.protectedSeeds_nodup
#print axioms Agent101.Protected.protectedSeeds_nodup
#check Agent101.Protected.natProduct_append
#print axioms Agent101.Protected.natProduct_append
#check Agent101.Protected.length_inputFiber
#print axioms Agent101.Protected.length_inputFiber
#check Agent101.Protected.length_inputFiber_cons
#print axioms Agent101.Protected.length_inputFiber_cons
#check Agent101.Protected.length_flatMap_scale
#print axioms Agent101.Protected.length_flatMap_scale
#check Agent101.Protected.length_protectedSeeds_cons_choice
#print axioms Agent101.Protected.length_protectedSeeds_cons_choice
#check Agent101.Protected.length_protectedSeeds
#print axioms Agent101.Protected.length_protectedSeeds
#check Agent101.Protected.protectedSeeds_exact
#print axioms Agent101.Protected.protectedSeeds_exact
#check Agent101.natValue_eq_digitValue
#print axioms Agent101.natValue_eq_digitValue
#check Agent101.natValue_normalize
#print axioms Agent101.natValue_normalize
#check Agent101.natValue_normalize_zero
#print axioms Agent101.natValue_normalize_zero
#check Agent101.step_eq_normalized_pair_value
#print axioms Agent101.step_eq_normalized_pair_value
#check Agent101.numericFiber_first_step
#print axioms Agent101.numericFiber_first_step
#check Agent101.Protected.digitValue_eq_natValue
#print axioms Agent101.Protected.digitValue_eq_natValue
#check Agent101.Protected.inputFiber_first_value
#print axioms Agent101.Protected.inputFiber_first_value
#check Agent101.Protected.inputFiber_second_value
#print axioms Agent101.Protected.inputFiber_second_value
#check Agent101.Protected.inputFiber_safe_positive_times
#print axioms Agent101.Protected.inputFiber_safe_positive_times
#check Agent101.Protected.protectedSeeds_first_value
#print axioms Agent101.Protected.protectedSeeds_first_value
#check Agent101.Protected.protectedSeeds_second_value
#print axioms Agent101.Protected.protectedSeeds_second_value
#check Agent101.Protected.protectedSeeds_common_second_value
#print axioms Agent101.Protected.protectedSeeds_common_second_value
#check Agent101.Protected.protectedSeeds_safe_positive_times
#print axioms Agent101.Protected.protectedSeeds_safe_positive_times
#check Agent101.Protected.protectedSeeds_safe_all_times_of_nonpalindrome
#print axioms Agent101.Protected.protectedSeeds_safe_all_times_of_nonpalindrome
#check Agent101.Protected.protectedSeeds_exact_safe_positive_times
#print axioms Agent101.Protected.protectedSeeds_exact_safe_positive_times
#check Agent101.palindrome_natValue_iff_reverse
#print axioms Agent101.palindrome_natValue_iff_reverse
#check Agent101.digitPairSums_of_reverse_eq
#print axioms Agent101.digitPairSums_of_reverse_eq
#check Agent101.even_digitPairSums_of_reverse_eq
#print axioms Agent101.even_digitPairSums_of_reverse_eq
#check Agent101.half_digitPairSums_of_reverse_eq
#print axioms Agent101.half_digitPairSums_of_reverse_eq
#check Agent101.digitFn_half_map
#print axioms Agent101.digitFn_half_map
#check Agent101.digitPairSums_bounded
#print axioms Agent101.digitPairSums_bounded
#check Agent101.canonical_half_pairSums
#print axioms Agent101.canonical_half_pairSums
#check Agent101.digitPairSums_half_of_reverse_even
#print axioms Agent101.digitPairSums_half_of_reverse_even
#check Agent101.canonical_half_coefficientWord
#print axioms Agent101.canonical_half_coefficientWord
#check Agent101.half_coefficientWord_mem_numericFiber
#print axioms Agent101.half_coefficientWord_mem_numericFiber
#check Agent101.palindrome_mem_numericFiber_iff
#print axioms Agent101.palindrome_mem_numericFiber_iff
#check Agent101.palindrome_numericFiber_exists_iff
#print axioms Agent101.palindrome_numericFiber_exists_iff
#check Agent101.palindrome_numericFiber_eq_half
#print axioms Agent101.palindrome_numericFiber_eq_half
#check Agent101.palindrome_numericFiber_unique
#print axioms Agent101.palindrome_numericFiber_unique
#check Agent101.palindromeNumericFiber
#print axioms Agent101.palindromeNumericFiber
#check Agent101.nonpalindromicNumericFiber
#print axioms Agent101.nonpalindromicNumericFiber
#check Agent101.mem_palindromeNumericFiber
#print axioms Agent101.mem_palindromeNumericFiber
#check Agent101.mem_nonpalindromicNumericFiber
#print axioms Agent101.mem_nonpalindromicNumericFiber
#check Agent101.palindromeNumericFiber_nodup
#print axioms Agent101.palindromeNumericFiber_nodup
#check Agent101.nonpalindromicNumericFiber_nodup
#print axioms Agent101.nonpalindromicNumericFiber_nodup
#check Agent101.length_filter_partition
#print axioms Agent101.length_filter_partition
#check Agent101.numericFiber_length_partition
#print axioms Agent101.numericFiber_length_partition
#check Agent101.mem_nonpalindromicNumericFiber_numeric
#print axioms Agent101.mem_nonpalindromicNumericFiber_numeric
#check Agent101.palindromePossible
#print axioms Agent101.palindromePossible
#check Agent101.palindromePossible_iff
#print axioms Agent101.palindromePossible_iff
#check Agent101.palindromeIndicator
#print axioms Agent101.palindromeIndicator
#check Agent101.list_eq_singleton_of_nodup_mem_iff
#print axioms Agent101.list_eq_singleton_of_nodup_mem_iff
#check Agent101.list_eq_nil_of_forall_not_mem
#print axioms Agent101.list_eq_nil_of_forall_not_mem
#check Agent101.palindromeNumericFiber_eq
#print axioms Agent101.palindromeNumericFiber_eq
#check Agent101.length_palindromeNumericFiber
#print axioms Agent101.length_palindromeNumericFiber
#check Agent101.length_nonpalindromicNumericFiber
#print axioms Agent101.length_nonpalindromicNumericFiber
#check Agent101.nonpalindromicNumericFiber_exact
#print axioms Agent101.nonpalindromicNumericFiber_exact
#check Agent101.Protected.palindromeHalf
#print axioms Agent101.Protected.palindromeHalf
#check Agent101.Protected.palindromeDigits
#print axioms Agent101.Protected.palindromeDigits
#check Agent101.Protected.palindromeSeed
#print axioms Agent101.Protected.palindromeSeed
#check Agent101.Protected.all_true_eq_replicate
#print axioms Agent101.Protected.all_true_eq_replicate
#check Agent101.Protected.inputWord_all_true_even
#print axioms Agent101.Protected.inputWord_all_true_even
#check Agent101.Protected.inputWord_even_iff
#print axioms Agent101.Protected.inputWord_even_iff
#check Agent101.Protected.coefficientWord_inputHalf_even_iff
#print axioms Agent101.Protected.coefficientWord_inputHalf_even_iff
#check Agent101.Protected.half_inputWord_all_true
#print axioms Agent101.Protected.half_inputWord_all_true
#check Agent101.Protected.profileCount_inputHalf_all_true
#print axioms Agent101.Protected.profileCount_inputHalf_all_true
#check Agent101.Protected.profileCount_inputHalf_all_true_positive
#print axioms Agent101.Protected.profileCount_inputHalf_all_true_positive
#check Agent101.Protected.palindromeSeed_member_palindrome
#print axioms Agent101.Protected.palindromeSeed_member_palindrome
#check Agent101.Protected.protectedSeeds_palindrome_iff
#print axioms Agent101.Protected.protectedSeeds_palindrome_iff
#check Agent101.Protected.palindromeSeed_mem
#print axioms Agent101.Protected.palindromeSeed_mem
#check Agent101.Protected.palindromeSeed_palindrome
#print axioms Agent101.Protected.palindromeSeed_palindrome
#check Agent101.Protected.protectedSeeds_palindrome_unique
#print axioms Agent101.Protected.protectedSeeds_palindrome_unique
#check Agent101.Protected.protectedNonpalSeeds
#print axioms Agent101.Protected.protectedNonpalSeeds
#check Agent101.Protected.mem_protectedNonpalSeeds
#print axioms Agent101.Protected.mem_protectedNonpalSeeds
#check Agent101.Protected.protectedNonpalSeeds_nodup
#print axioms Agent101.Protected.protectedNonpalSeeds_nodup
#check Agent101.Protected.protectedSeeds_palindrome_filter
#print axioms Agent101.Protected.protectedSeeds_palindrome_filter
#check Agent101.Protected.length_protectedNonpalSeeds
#print axioms Agent101.Protected.length_protectedNonpalSeeds
#check Agent101.Protected.mem_protectedNonpalSeeds_positive
#print axioms Agent101.Protected.mem_protectedNonpalSeeds_positive
#check Agent101.Protected.mem_protectedNonpalSeeds_width
#print axioms Agent101.Protected.mem_protectedNonpalSeeds_width
#check Agent101.Protected.mem_protectedNonpalSeeds_numeric
#print axioms Agent101.Protected.mem_protectedNonpalSeeds_numeric
#check Agent101.Protected.protectedNonpalSeeds_nonempty
#print axioms Agent101.Protected.protectedNonpalSeeds_nonempty
#check Agent101.Protected.protectedNonpalSeeds_exact
#print axioms Agent101.Protected.protectedNonpalSeeds_exact
#check Agent101.Protected.protectedNonpalSeeds_second_value
#print axioms Agent101.Protected.protectedNonpalSeeds_second_value
#check Agent101.Protected.protectedNonpalSeeds_common_second_value
#print axioms Agent101.Protected.protectedNonpalSeeds_common_second_value
#check Agent101.Protected.protectedNonpalSeeds_safe
#print axioms Agent101.Protected.protectedNonpalSeeds_safe
#check Agent101.Protected.protectedNonpalFamily_exact
#print axioms Agent101.Protected.protectedNonpalFamily_exact

run_cmd do
  let env ← getEnv
  let publicNames : List String := ["Agent101.Protected.protectedSeeds", "Agent101.Protected.coefficientWord_inputHalf", "Agent101.Protected.coefficientWord_inputHalf_bounded", "Agent101.Protected.mem_inputFiber", "Agent101.Protected.mem_protectedSeeds", "Agent101.Protected.mem_protectedSeeds_numeric", "Agent101.Protected.mem_protectedSeeds_width", "Agent101.Protected.mem_protectedSeeds_positive", "Agent101.Protected.inputFiber_index_unique", "Agent101.Protected.inputFibers_disjoint", "Agent101.Protected.protectedSeeds_nodup", "Agent101.Protected.natProduct_append", "Agent101.Protected.length_inputFiber", "Agent101.Protected.length_inputFiber_cons", "Agent101.Protected.length_flatMap_scale", "Agent101.Protected.length_protectedSeeds_cons_choice", "Agent101.Protected.length_protectedSeeds", "Agent101.Protected.protectedSeeds_exact", "Agent101.natValue_eq_digitValue", "Agent101.natValue_normalize", "Agent101.natValue_normalize_zero", "Agent101.step_eq_normalized_pair_value", "Agent101.numericFiber_first_step", "Agent101.Protected.digitValue_eq_natValue", "Agent101.Protected.inputFiber_first_value", "Agent101.Protected.inputFiber_second_value", "Agent101.Protected.inputFiber_safe_positive_times", "Agent101.Protected.protectedSeeds_first_value", "Agent101.Protected.protectedSeeds_second_value", "Agent101.Protected.protectedSeeds_common_second_value", "Agent101.Protected.protectedSeeds_safe_positive_times", "Agent101.Protected.protectedSeeds_safe_all_times_of_nonpalindrome", "Agent101.Protected.protectedSeeds_exact_safe_positive_times", "Agent101.palindrome_natValue_iff_reverse", "Agent101.digitPairSums_of_reverse_eq", "Agent101.even_digitPairSums_of_reverse_eq", "Agent101.half_digitPairSums_of_reverse_eq", "Agent101.digitFn_half_map", "Agent101.digitPairSums_bounded", "Agent101.canonical_half_pairSums", "Agent101.digitPairSums_half_of_reverse_even", "Agent101.canonical_half_coefficientWord", "Agent101.half_coefficientWord_mem_numericFiber", "Agent101.palindrome_mem_numericFiber_iff", "Agent101.palindrome_numericFiber_exists_iff", "Agent101.palindrome_numericFiber_eq_half", "Agent101.palindrome_numericFiber_unique", "Agent101.palindromeNumericFiber", "Agent101.nonpalindromicNumericFiber", "Agent101.mem_palindromeNumericFiber", "Agent101.mem_nonpalindromicNumericFiber", "Agent101.palindromeNumericFiber_nodup", "Agent101.nonpalindromicNumericFiber_nodup", "Agent101.length_filter_partition", "Agent101.numericFiber_length_partition", "Agent101.mem_nonpalindromicNumericFiber_numeric", "Agent101.palindromePossible", "Agent101.palindromePossible_iff", "Agent101.palindromeIndicator", "Agent101.list_eq_singleton_of_nodup_mem_iff", "Agent101.list_eq_nil_of_forall_not_mem", "Agent101.palindromeNumericFiber_eq", "Agent101.length_palindromeNumericFiber", "Agent101.length_nonpalindromicNumericFiber", "Agent101.nonpalindromicNumericFiber_exact", "Agent101.Protected.palindromeHalf", "Agent101.Protected.palindromeDigits", "Agent101.Protected.palindromeSeed", "Agent101.Protected.all_true_eq_replicate", "Agent101.Protected.inputWord_all_true_even", "Agent101.Protected.inputWord_even_iff", "Agent101.Protected.coefficientWord_inputHalf_even_iff", "Agent101.Protected.half_inputWord_all_true", "Agent101.Protected.profileCount_inputHalf_all_true", "Agent101.Protected.profileCount_inputHalf_all_true_positive", "Agent101.Protected.palindromeSeed_member_palindrome", "Agent101.Protected.protectedSeeds_palindrome_iff", "Agent101.Protected.palindromeSeed_mem", "Agent101.Protected.palindromeSeed_palindrome", "Agent101.Protected.protectedSeeds_palindrome_unique", "Agent101.Protected.protectedNonpalSeeds", "Agent101.Protected.mem_protectedNonpalSeeds", "Agent101.Protected.protectedNonpalSeeds_nodup", "Agent101.Protected.protectedSeeds_palindrome_filter", "Agent101.Protected.length_protectedNonpalSeeds", "Agent101.Protected.mem_protectedNonpalSeeds_positive", "Agent101.Protected.mem_protectedNonpalSeeds_width", "Agent101.Protected.mem_protectedNonpalSeeds_numeric", "Agent101.Protected.protectedNonpalSeeds_nonempty", "Agent101.Protected.protectedNonpalSeeds_exact", "Agent101.Protected.protectedNonpalSeeds_second_value", "Agent101.Protected.protectedNonpalSeeds_common_second_value", "Agent101.Protected.protectedNonpalSeeds_safe", "Agent101.Protected.protectedNonpalFamily_exact"]
  let mut seen := 0
  for (name, info) in env.constants.toList do
    if publicNames.contains name.toString then
      if info.isUnsafe then throwError m!"UNSAFE_PUBLIC_DECLARATION {name}"
      match info with
      | .axiomInfo _ => throwError m!"PUBLIC_CUSTOM_AXIOM {name}"
      | _ => pure ()
      seen := seen + 1
      logInfo m!"PUBLIC_SAFE {name}"
  if seen != publicNames.length then throwError m!"PUBLIC_CENSUS_MISMATCH {seen}"
  logInfo m!"PUBLIC_COUNT {seen}"
