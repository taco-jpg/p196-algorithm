import P196.SevenCarryMaximalWidth.CandidateData

/-!
Literal finite-index decomposition for the width-seven certificates.
The standard eliminator Fin.cases splits a bounded universal goal before
the supplied leaf tactic runs. No whole enumeration is sent to one decision.
The existing certify_fin16 helper is reused where its bound applies.
-/

namespace SevenCarryMaximalWidth.Candidates

private def finitePointCases (body : Lean.TSyntax `Lean.Parser.Tactic.tacticSeq) :
    Nat → Lean.MacroM (Lean.TSyntax `tactic)
  | 0 => `(tactic| (intro i; exact Fin.elim0 i))
  | n + 1 => do
      let rest ← finitePointCases body n
      `(tactic| (
          refine Fin.cases ?_ ?_
          · $body:tacticSeq
          · $rest:tactic))

syntax "seven_width_fin " num " => " tacticSeq : tactic

macro_rules
  | `(tactic| seven_width_fin $n:num => $body:tacticSeq) =>
      finitePointCases body n.getNat

end SevenCarryMaximalWidth.Candidates
