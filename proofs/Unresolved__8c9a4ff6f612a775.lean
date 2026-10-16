import ReturnCertificate

/-!
Agent #123: statement-only handoff. No proof of this proposition is supplied.
This is the missing finite witness, not a new claim of ownership or a theorem.
-/
namespace Agent123.Obligations
open Agent109 Agent109.Cert

def AdmissibleReturnWitness : Prop :=
  ∃ cert : Certificate, ∃ H M : Word,
    check cert = true ∧ decide (Admissible0 cert H M) = true

end Agent123.Obligations
