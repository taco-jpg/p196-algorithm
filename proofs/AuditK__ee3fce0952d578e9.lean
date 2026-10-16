import BulkDerivationK
#print axioms BoundaryCertificateK.no_finite_exterior
#print axioms BoundaryCertificateK.options_complete
#print axioms BoundaryCertificateK.no_arithmetic_exterior
#print axioms BoundaryCertificateK.no_bulk_exterior
#print axioms BoundaryCertificateK.no_24_phase_bulk_exterior
#print axioms BoundaryCertificateK.no_936_or_9_12_15_exterior
#print axioms BoundaryCertificateK.no_24_phase_936_or_9_12_15_exterior
set_option pp.fullNames true in
#check @BoundaryCertificateK.no_936_or_9_12_15_exterior
set_option pp.fullNames true in
#check @BoundaryCertificate.no_936_or_9_12_15_exterior
-- the two statements are syntactically identical (same constants):
example : (∀ (t : Fin 12) (k : Nat), ¬ ReverseClosure.Path (BoundaryCertificate.ArithmeticColumn (6*(k+1)))
      (fun _ => 41) (BoundaryCertificate.derivedBulkWord t)) :=
  BoundaryCertificateK.no_936_or_9_12_15_exterior
