import TwoDigitMain
import Lean.Util.CollectAxioms
import Lean.Elab.Command

/-! Agent #115 independent axiom audit of agent113-two-digit-prefix-lean.
Enumerates every theorem whose defining module is one of the project modules
of the TwoDigitMain import closure and runs `Lean.collectAxioms` on each. -/

open Lean Elab Command

def agent115Modules : Array Name := #[`LychrelDigitSums, `TwoDigitProjection, `TwoDigitGrowth, `PalindromeBridge, `TwoDigitNumeric, `TwoDigitCertificate, `TwoDigitCert10, `TwoDigitCert20, `TwoDigitCert32, `TwoDigitCert40, `TwoDigitCert41, `TwoDigitCert60, `TwoDigitCert64, `TwoDigitCert65, `TwoDigitCert76, `TwoDigitCert80, `TwoDigitCert81, `TwoDigitCert82, `TwoDigitCert83, `TwoDigitMain]

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


#check @Agent113.TwoDigit.ancestry_bound_10
#check @Agent113.TwoDigit.ancestry_bound_20
#check @Agent113.TwoDigit.ancestry_bound_32
#check @Agent113.TwoDigit.ancestry_bound_40
#check @Agent113.TwoDigit.ancestry_bound_41
#check @Agent113.TwoDigit.ancestry_bound_60
#check @Agent113.TwoDigit.ancestry_bound_64
#check @Agent113.TwoDigit.ancestry_bound_65
#check @Agent113.TwoDigit.ancestry_bound_76
#check @Agent113.TwoDigit.ancestry_bound_80
#check @Agent113.TwoDigit.ancestry_bound_81
#check @Agent113.TwoDigit.ancestry_bound_82
#check @Agent113.TwoDigit.ancestry_bound_83
#check @Agent113.TwoDigit.no_196_thirteen
#check @Agent113.TwoDigit.no_196_thirteen_arith
#check @Agent113.TwoDigit.startsTwo_iff
#print Agent113.TwoDigit.PalindromeStartsTwo
#print Agent113.TwoDigit.StartsTwo
#print Lychrel196.Palindrome
#print Lychrel196.reverse10
#print DecimalDigits.Canonical
#print DecimalDigits.value
#print Agent113.TwoDigit.thirteenPrefixes
#print axioms Agent113.TwoDigit.no_196_thirteen
#print axioms Agent113.TwoDigit.no_196_thirteen_arith
#print axioms Agent113.TwoDigit.exact_depth_10
#print axioms Agent113.TwoDigit.exact_depth_20
#print axioms Agent113.TwoDigit.exact_depth_32
#print axioms Agent113.TwoDigit.exact_depth_40
#print axioms Agent113.TwoDigit.exact_depth_41
#print axioms Agent113.TwoDigit.exact_depth_60
#print axioms Agent113.TwoDigit.exact_depth_64
#print axioms Agent113.TwoDigit.exact_depth_65
#print axioms Agent113.TwoDigit.exact_depth_76
#print axioms Agent113.TwoDigit.exact_depth_80
#print axioms Agent113.TwoDigit.exact_depth_81
#print axioms Agent113.TwoDigit.exact_depth_82
#print axioms Agent113.TwoDigit.exact_depth_83
#agent115_audit "/home/claude/review113/audit_inventory.tsv"
