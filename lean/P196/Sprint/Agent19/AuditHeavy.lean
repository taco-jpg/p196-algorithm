import P196.Agent124FourDigit.A124F4Final
import P196.Agent124FourDigit.A124F5Final
import P196.Agent124Prefix620.A124Prefix620Final
import P196.Agent104Prefix739.Conclusion739
import P196.Agent124PrefixFiveSix.Agent124PrefixSummary
import P196.Agent118PrefixKernel.Conclusion217
import P196.Agent118PrefixKernel.Conclusion777
import P196.Agent118PrefixKernel.Controls218
import P196.Agent118PrefixKernel.Witnesses
import P196.Agent118PrefixKernel.Conclusion218

/-! Agent 19 review: axiom audit of every registered endpoint of Agent124FourDigit, Agent124Prefix620, Agent104Prefix739, Agent124PrefixFiveSix, Agent118PrefixKernel.
Run `lake env lean` on this file; each line must list only propext, Classical.choice, Quot.sound. -/


-- Agent124FourDigit
#print axioms Agent124.CertF4.ancestry_00
#print axioms Agent124.CertF4.no_196_00
#print axioms Agent124.CertF4.ancestry_01
#print axioms Agent124.CertF4.no_196_01
#print axioms Agent124.CertF4.ancestry_02
#print axioms Agent124.CertF4.no_196_02
#print axioms Agent124.CertF4.ancestry_03
#print axioms Agent124.CertF4.no_196_03
#print axioms Agent124.CertF4.ancestry_04
#print axioms Agent124.CertF4.no_196_04
#print axioms Agent124.CertF4.ancestry_05
#print axioms Agent124.CertF4.no_196_05
#print axioms Agent124.CertF4.ancestry_06
#print axioms Agent124.CertF4.no_196_06
#print axioms Agent124.CertF5.ancestry_00
#print axioms Agent124.CertF5.no_196_00
#print axioms Agent124.CertF5.ancestry_01
#print axioms Agent124.CertF5.no_196_01
#print axioms Agent124.CertF5.ancestry_02
#print axioms Agent124.CertF5.no_196_02
#print axioms Agent124.CertF5.ancestry_03
#print axioms Agent124.CertF5.no_196_03
#print axioms Agent124.CertF5.ancestry_04
#print axioms Agent124.CertF5.no_196_04

-- Agent124Prefix620
#print axioms Agent124.CertPrefix620.ancestry_620
#print axioms Agent124.CertPrefix620.no_196_620

-- Agent104Prefix739
#print axioms SevenColumnKernel.Finite739.initialCovered
#print axioms SevenColumnKernel.Finite739.ancestry_bound39
#print axioms SevenColumnKernel.Finite739.no_196_739_palindrome

-- Agent124PrefixFiveSix
#print axioms Agent124.PrefixSummary.classes_length
#print axioms Agent124.PrefixSummary.ancestry_all
#print axioms Agent124.PrefixSummary.no_196_all

-- Agent118PrefixKernel
#print axioms Agent118.Finite217.ancestry_bound23
#print axioms Agent118.Finite217.no_196_217_palindrome
#print axioms Agent118.Finite217.no_196_217_palindrome_unfolded
#print axioms Agent118.Finite777.ancestry_bound25
#print axioms Agent118.Finite777.no_196_777_palindrome
#print axioms Agent118.Finite777.no_196_777_palindrome_unfolded
#print axioms Agent118.Controls218.witness_orbit
#print axioms Agent118.Controls218.witness_family
#print axioms Agent118.Controls218.family_reached
#print axioms Agent118.Controls218.short_edge_image
#print axioms Agent118.Controls218.short_edge_source
#print axioms Agent118.Controls218.short_source_mem
#print axioms Agent118.Controls218.old_short_premise_fails
#print axioms Agent118.Controls218.bound33_attained
#print axioms Agent118.Controls218.bound32_fails
#print axioms Agent118.Witnesses.starts_of_digits
#print axioms Agent118.Witnesses.w218_orbit
#print axioms Agent118.Witnesses.w218_family
#print axioms Agent118.Witnesses.depth15_218
#print axioms Agent118.Witnesses.w777_orbit
#print axioms Agent118.Witnesses.w777_family
#print axioms Agent118.Witnesses.depth14_777
#print axioms Agent118.Witnesses.w217_orbit
#print axioms Agent118.Witnesses.w217_family
#print axioms Agent118.Witnesses.depth15_217
#print axioms Agent118.Finite218.ancestry_bound34
#print axioms Agent118.Finite218.no_196_218_palindrome
#print axioms Agent118.Finite218.no_196_218_palindrome_unfolded
