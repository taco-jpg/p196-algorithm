import EventualCompat
import Lean.Util.CollectAxioms
import Lean.Elab.Command

/-! Agent #115 independent axiom audit of agent112-eventual-realizability.
Enumerates every theorem whose defining module is one of the project modules
of the EventualCompat import closure and runs `Lean.collectAxioms` on each. -/

open Lean Elab Command

def agent115Modules : Array Name := #[`TemplateStep, `ReturnCertificate, `AdmissibleCenters, `SymbolicGrowth, `EventualRealization, `EventualCorrespondence, `CoefficientContraction, `LychrelDigitSums, `PeriodObstructions, `Compat, `EventualCompat]

elab "#agent115_audit " path:str : command => do
  let env ← getEnv
  let mods := env.header.moduleNames
  let proj : NameSet := agent115Modules.foldl (fun s n => s.insert n) {}
  let mut lines : Array String := #[]
  let mut union : NameSet := {}
  let mut nthm := 0
  let mut nax := 0
  let mut nunsafe := 0
  let mut ndef := 0
  for (n, ci) in env.constants.map₁.toList do
    match env.getModuleIdxFor? n with
    | some idx =>
      let m := mods[idx.toNat]!
      if proj.contains m then
        if ci.isUnsafe then
          nunsafe := nunsafe + 1
          lines := lines.push s!"UNSAFE\t{n}\t{m}"
        match ci with
        | .thmInfo _ =>
          let axs ← collectAxioms n
          nthm := nthm + 1
          for a in axs do
            union := union.insert a
          lines := lines.push s!"THM\t{n}\t{m}\t{axs.toList}"
        | .axiomInfo _ =>
          nax := nax + 1
          lines := lines.push s!"AXIOM_DECL\t{n}\t{m}"
        | .defnInfo _ => ndef := ndef + 1
        | _ => pure ()
    | none => pure ()
  IO.FS.writeFile path.getString (String.intercalate "\n" (lines.qsort (· < ·)).toList ++ "\n")
  logInfo m!"AGENT115_SUMMARY theorems={nthm} project_axiom_decls={nax} unsafe={nunsafe} defs={ndef} axiom_union={union.toList}"


#check @Agent112.Eventual.original_arbitrary_eventual_realization
#check @Agent112.Eventual.original_eventual_realization
#check @Agent112.Eventual.original_arbitrary_safe_symbolic_positive_seed
#check @Agent112.Eventual.original_safe_symbolic_positive_seed
#print axioms Agent112.Eventual.original_arbitrary_eventual_realization
#print axioms Agent112.Eventual.original_eventual_realization
#print axioms Agent112.Eventual.original_arbitrary_safe_symbolic_positive_seed
#print axioms Agent112.Eventual.original_safe_symbolic_positive_seed
#print Agent109.Word
#print Agent109.evalL
#print Agent109.pairWord
#print Agent8.orbit
#agent115_audit "/home/claude/review112/audit_inventory.tsv"
