import Agent104DFABadMonitor
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["Lychrel196Research", "Agent107TransducerDefs", "Agent107TransducerPath", "Agent107TransducerInput", "Agent107TransducerOutput", "Agent107TransducerNumeric", "Agent107TransducerTablesData", "Agent107TransducerTablesChecks", "Agent107TransducerTables", "Agent107TransducerReachable", "Agent107TransducerGraph", "Agent107DFA", "Agent107DFAAlphabet", "Agent107DFAChecker", "Agent107DFABoolean", "Agent104DFABadMonitor"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut defs := 0
  let mut union : List Name := []
  let mut defUnion : List Name := []
  let mut seen : List String := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          if !(seen.contains mod.toString) then seen := mod.toString :: seen
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | .defnInfo v =>
          if v.safety != .safe then
            logInfo m!"NONSAFE_DEFINITION {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_DEFINITION_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_DEFINITION {mod} {name} : {axl}"
        | .opaqueInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_OPAQUE {mod} {name}"
          else
            defs := defs + 1
            let axs ← liftCoreM (Lean.collectAxioms name)
            let axl := axs.toList
            for ax in axl do
              if !(defUnion.contains ax) then defUnion := ax :: defUnion
            if axl.any (fun ax => !(allowed.contains ax)) then
              throwError m!"DISALLOWED_OPAQUE_AXIOMS {mod} {name} : {axl}"
            logInfo m!"AUDIT_SAFE_OPAQUE {mod} {name} : {axl}"
        | _ => pure ()
  for mod in selected do
    if !(seen.contains mod) then throwError m!"MODULE_NOT_AUDITED {mod}"
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
  logInfo m!"FULL_DEFINITION_AUDIT definitions={defs} union={defUnion}"

#check Agent104.DFASafety.MonitorState
#print axioms Agent104.DFASafety.MonitorState

#check Agent104.DFASafety.monitorStep
#print axioms Agent104.DFASafety.monitorStep

#check Agent104.DFASafety.pairAllowed
#print axioms Agent104.DFASafety.pairAllowed

#check Agent104.DFASafety.terminalApplicable
#print axioms Agent104.DFASafety.terminalApplicable

#check Agent104.DFASafety.badTerminal
#print axioms Agent104.DFASafety.badTerminal

#check Agent104.DFASafety.centerCode
#print axioms Agent104.DFASafety.centerCode

#check Agent104.DFASafety.centerCode_none
#print axioms Agent104.DFASafety.centerCode_none

#check Agent104.DFASafety.centerCode_some_zero
#print axioms Agent104.DFASafety.centerCode_some_zero

#check Agent104.DFASafety.monitorStep_m0
#print axioms Agent104.DFASafety.monitorStep_m0

#check Agent104.DFASafety.monitorStep_m1
#print axioms Agent104.DFASafety.monitorStep_m1

#check Agent104.DFASafety.monitorStep_m2
#print axioms Agent104.DFASafety.monitorStep_m2

#check Agent104.DFASafety.monitorStep_m3
#print axioms Agent104.DFASafety.monitorStep_m3

#check Agent104.DFASafety.runMonitorFrom
#print axioms Agent104.DFASafety.runMonitorFrom

#check Agent104.DFASafety.runMonitor
#print axioms Agent104.DFASafety.runMonitor

#check Agent104.DFASafety.allLow
#print axioms Agent104.DFASafety.allLow

#check Agent104.DFASafety.allExceptional
#print axioms Agent104.DFASafety.allExceptional

#check Agent104.DFASafety.runMonitorFrom_nil
#print axioms Agent104.DFASafety.runMonitorFrom_nil

#check Agent104.DFASafety.runMonitorFrom_cons
#print axioms Agent104.DFASafety.runMonitorFrom_cons

#check Agent104.DFASafety.runMonitorFrom_append
#print axioms Agent104.DFASafety.runMonitorFrom_append

#check Agent104.DFASafety.runMonitorFrom_m3
#print axioms Agent104.DFASafety.runMonitorFrom_m3

#check Agent104.DFASafety.runMonitorFrom_m1_iff_allLow
#print axioms Agent104.DFASafety.runMonitorFrom_m1_iff_allLow

#check Agent104.DFASafety.runMonitorFrom_m2_iff_allExceptional
#print axioms Agent104.DFASafety.runMonitorFrom_m2_iff_allExceptional

#check Agent104.DFASafety.runMonitor_cons_m1
#print axioms Agent104.DFASafety.runMonitor_cons_m1

#check Agent104.DFASafety.runMonitor_cons_m2
#print axioms Agent104.DFASafety.runMonitor_cons_m2

#check Agent104.DFASafety.monitorStates
#print axioms Agent104.DFASafety.monitorStates

#check Agent104.DFASafety.pairSymbols
#print axioms Agent104.DFASafety.pairSymbols

#check Agent104.DFASafety.centerSymbols
#print axioms Agent104.DFASafety.centerSymbols

#check Agent104.DFASafety.checkSafetyRows
#print axioms Agent104.DFASafety.checkSafetyRows

#check Agent104.DFASafety.monitorBadWordCorrespondence
#print axioms Agent104.DFASafety.monitorBadWordCorrespondence

#check Agent104.DFASafety.safetyRowsSound
#print axioms Agent104.DFASafety.safetyRowsSound
