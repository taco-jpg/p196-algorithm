import Agent107TransducerGraph
import Agent107TransducerBoundary
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
#check Agent107.FoldedTransducer.actual_accepts
#check Agent107.FoldedTransducer.accepting_state_eq_actual
#check Agent107.FoldedTransducer.accepting_finitePath_unique
#check Agent107.FoldedTransducer.exists_unique_finitePath
#check Agent107.FoldedTransducer.actual_output_even_no_overflow
#check Agent107.FoldedTransducer.actual_output_even_overflow
#check Agent107.FoldedTransducer.actual_output_odd_no_overflow
#check Agent107.FoldedTransducer.actual_output_odd_overflow
#check Agent107.FoldedTransducer.actual_output
#check Agent107.FoldedTransducer.accepting_output
#check Agent107.FoldedTransducer.accepts_symmetrize
#check Agent107.FoldedTransducer.foldPrefix_symmetrize
#check Agent107.FoldedTransducer.pathOutput_symmetrize
#check Agent107.FoldedTransducer.reconstructed_admissible
#check Agent107.FoldedTransducer.accepting_input_realizable
#check Agent107.FoldedTransducer.canonical_accepting_step
#check Agent107.FoldedTransducer.canonical_step_path
#check Agent107.FoldedTransducer.accepting_numeric_realizable
#check Agent107.FoldedTransducer.Table.states_length
#check Agent107.FoldedTransducer.Table.edges_length
#check Agent107.FoldedTransducer.Table.terminals_length
#check Agent107.FoldedTransducer.Table.states_nodup
#check Agent107.FoldedTransducer.Table.edges_nodup
#check Agent107.FoldedTransducer.Table.terminals_nodup
#check Agent107.FoldedTransducer.Table.edge_mem_iff
#check Agent107.FoldedTransducer.Table.terminal_mem_iff
#check Agent107.FoldedTransducer.Table.states_closed
#check Agent107.FoldedTransducer.reachable_iff_mem_states
#check Agent107.FoldedTransducer.Boundary.initial_no_overflow_sentinel
#check Agent107.FoldedTransducer.Boundary.empty_input_rejected
#check Agent107.FoldedTransducer.Boundary.one_digit_accepts_iff
#check Agent107.FoldedTransducer.Boundary.odd_center_rejected
#check Agent107.FoldedTransducer.Boundary.oversized_center_rejected
#check Agent107.FoldedTransducer.Boundary.first_pair_zero_rejected
#check Agent107.FoldedTransducer.Boundary.odd_overflow_has_extra_pair
#check Agent107.FoldedTransducer.Boundary.accepted_tail_not_unique
#check Agent107.FoldedTransducer.accepting_states_mem
#check Agent107.FoldedTransducer.graphAccepts_iff_accepts
#check Agent107.FoldedTransducer.accepting_state_unique
#check Agent107.FoldedTransducer.accepting_finitePath_unique_unrestricted
#check Agent107.FoldedTransducer.indexed_edge_eq
#check Agent107.FoldedTransducer.indexed_terminal_eq
#check Agent107.FoldedTransducer.indexed_accepts
#check Agent107.FoldedTransducer.accepting_indexed_exists
#check Agent107.FoldedTransducer.indexed_output
#check Agent107.FoldedTransducer.nodup_get_injective
#check Agent107.FoldedTransducer.indexed_history_unique
#check Agent107.FoldedTransducer.admissible_unique_history
#check Agent107.FoldedTransducer.indexed_numeric_realizable
run_cmd do
  let env ← getEnv
  let selected : List String := ["Lychrel196Research", "Agent107TransducerDefs", "Agent107TransducerPath", "Agent107TransducerInput", "Agent107TransducerOutput", "Agent107TransducerNumeric", "Agent107TransducerTablesData", "Agent107TransducerTablesChecks", "Agent107TransducerTables", "Agent107TransducerReachable", "Agent107TransducerGraph", "Agent107TransducerBoundary"]
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
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
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
