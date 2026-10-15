import BroaderBound
import Lean.Util.CollectAxioms
import Lean.Elab.Command

/-! Agent #115 independent axiom audit (written independently of Agent #103's
AllAxioms files). Enumerates every theorem constant whose defining module is one of the 50 modules of the BroaderBound import
closure, computes `Lean.collectAxioms` for each, records any `axiom` declared in
a project module, and writes one tab-separated line per constant. -/

open Lean Elab Command

def agent115Modules : Array Name := #[`LychrelDigitSums, `ScalarClock, `ActualScalar, `PrefixExtension, `ScalarOrbit, `BroaderClock, `ActualPrefixLift, `ScalarRoot, `BoundedPrefixLift, `FiniteGraph, `RankRows, `BJobCatalog, `BJobData0, `BroaderRoot, `BJobData1, `BJobData2, `BJobData3, `BJobData4, `BJobData5, `BJobData6, `BJobData7, `BJobData8, `BJobData9, `BJobData10, `BJobData11, `BJobData12, `BJobData13, `BJobData14, `CondensationBound, `ComponentHierarchy, `ActualJobFamily, `BroaderHierarchyData, `RangeChecks, `BJobChecks0, `BJobChecks1, `BJobChecks2, `BJobChecks3, `BJobChecks4, `BJobChecks5, `BJobChecks6, `BJobChecks7, `BJobChecks8, `BJobChecks9, `BJobChecks10, `BJobChecks11, `BJobChecks12, `BJobChecks13, `BJobChecks14, `BroaderHierarchy, `BroaderBound]

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

#print axioms BroaderBound.returns_le_90_plus_warmup
#print axioms BroaderBound.returns_le_94
#print axioms BroaderBound.wide_returns_le_90
#print axioms BroaderBound.no_95_returns
#print axioms BroaderClock.return_forces_clock
#print axioms BroaderClock.returns_clock_segment
#print axioms BroaderClock.returnOK_root
#print axioms BroaderRoot.root2_realization
#print axioms BroaderRoot.returnIn_root
#print axioms BroaderRoot.actual_broader_root_path
#print axioms BroaderHierarchy.finite_root_bound
#check @BroaderBound.returns_le_90_plus_warmup
#check @BroaderBound.returns_le_94
#check @BroaderBound.wide_returns_le_90
#check @BroaderBound.no_95_returns
#check @BroaderClock.return_forces_clock
#check @BroaderHierarchy.finite_root_bound
#print ScalarOrbit.warmup
#print BroaderClock.pairAt
#print FoldedDecimal.Admissible
#print OverflowCarryNormalization.iterPairs

#agent115_audit "/home/claude/review/audit/axiom_inventory_stage2.tsv"
