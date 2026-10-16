import Agent9DecimalFactorialEscape
import Lean

open Lean Elab Command

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/- The checker pattern follows the retained interval-closure audit. Its scope
is the nine unchanged dependency modules 和 these two new proof modules. -/

#check @P196.Agent9.FactorialEscape.recurrence_factorial_bound
#check @P196.Agent9.FactorialEscape.sharpEscapeBound_factorial
#check @P196.Agent9.FactorialEscape.sharpDigitSumEscapeBound_factorial
#check @P196.Agent9.FactorialEscape.digitSum_uniform_window_factorial
#check @P196.Agent9.FactorialEscape.digitSum_uniform_window_196_factorial

#print axioms P196.Agent9.FactorialEscape.factorial
#print axioms P196.Agent9.FactorialEscape.factorial_zero
#print axioms P196.Agent9.FactorialEscape.factorial_succ
#print axioms P196.Agent9.FactorialEscape.factorial_pos
#print axioms P196.Agent9.FactorialEscape.recurrence_step_bound
#print axioms P196.Agent9.FactorialEscape.recurrence_factorial_bound_succ
#print axioms P196.Agent9.FactorialEscape.recurrence_factorial_bound
#print axioms P196.Agent9.FactorialEscape.sharpEscapeBound_factorial
#print axioms P196.Agent9.FactorialEscape.sharpDigitSumEscapeBound_factorial
#print axioms P196.Agent9.FactorialEscape.digitSum_uniform_window_factorial
#print axioms P196.Agent9.FactorialEscape.digitSum_uniform_window_196_factorial

run_cmd do
  let env ← getEnv
  let selected : List String := [
    "LychrelDigitSums", "SharedProfile", "ProfileDynamics", "ProfileIsolation",
    "UniformEscape", "SharpProfileBounds", "SharpUniformEscape", "DecimalEmbedding",
    "SharpUniformDecimal", "Agent9FactorialRecurrence", "Agent9DecimalFactorialEscape"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut visited : List String := []
  let mut theoremCount := 0
  let mut definitionCount := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        if !(visited.contains origin.toString) then
          visited := origin.toString :: visited
        match info with
        | .axiomInfo value =>
          if value.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {origin} {name}"
          else
            throwError m!"CUSTOM_AXIOM {origin} {name}"
        | .thmInfo _ =>
          theoremCount := theoremCount + 1
          let dependencies ← liftCoreM (Lean.collectAxioms name)
          let axl := dependencies.toList
          for axiomName in axl do
            if !(allowed.contains axiomName) then
              throwError m!"DISALLOWED_AXIOM {origin} {name} {axiomName}"
            if !(union.contains axiomName) then
              union := axiomName :: union
          logInfo m!"AUDIT_THEOREM {origin} {name} : {axl}"
        | .defnInfo _ | .opaqueInfo _ =>
          if info.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_DEFINITION {origin} {name}"
          else
            definitionCount := definitionCount + 1
            let dependencies ← liftCoreM (Lean.collectAxioms name)
            let axl := dependencies.toList
            for axiomName in axl do
              if !(allowed.contains axiomName) then
                throwError m!"DISALLOWED_DEFINITION_AXIOM {origin} {name} {axiomName}"
              if !(union.contains axiomName) then
                union := axiomName :: union
            logInfo m!"AUDIT_DEFINITION {origin} {name} : {axl}"
        | _ => pure ()
  for origin in selected do
    if !(visited.contains origin) then
      throwError m!"MISSING_MODULE_ORIGIN {origin}"
  logInfo m!"FULL_MODULE_AUDIT theorems={theoremCount} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={definitionCount}"
  logInfo m!"AUDITED_MODULE_ORIGINS {visited}"
