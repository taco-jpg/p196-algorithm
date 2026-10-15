import ReturnCertificate

/-!
Agent #112. Precise investigation targets, not proved theorems.
Source interface: Agent109.Cert at main eec3d5f3646cab50abad6e610ea19626cd249070.
No admitted proofs and no new axioms are introduced here.
-/
namespace Agent112.Admissibility
open Agent109 Agent109.Cert

def CyclicCenters : Prop :=
  ∀ cert : Certificate, Valid cert → ∀ i, i < cert.P → Mirr (cert.st i).C

def CyclicPositiveHeads : Prop :=
  ∀ cert : Certificate, Valid cert → ∀ i, i < cert.P →
    ∀ b, (cert.st i).B.head? = some b → 0 < b

def AutomaticAdmissibility : Prop :=
  ∀ cert : Certificate, check cert = true → ∃ H M, Admissible0 cert H M

end Agent112.Admissibility
