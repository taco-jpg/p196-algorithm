import Conclusion218
import Lean
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
run_cmd do
  let env ← getEnv
  let selected : List String := ["PrefixCertificate", "Rank218Data00", "Rank218Data01", "Rank218Data02", "Rank218Data03", "Rank218Data04", "Rank218Data05", "Rank218Data06", "Rank218Data07", "Rank218Data08", "Rank218Data09", "Rank218Data10", "Rank218Data11", "Rank218Data12", "Rank218Data13", "Rank218Data14", "Rank218Data15", "Rank218", "LychrelDigitSums", "PrefixInverse", "ActualPrefix", "ShortBoundary", "LongRowsBase", "PalindromeBridge", "ActualAncestry", "PrefixAncestry", "FastInverse", "FastRowsBase", "RowBoolean", "PrefixChecksBase", "Rows218_000", "Rows218_001", "Rows218_002", "Rows218_003", "Rows218_004", "Rows218_005", "Rows218_006", "Rows218_007", "Rows218_008", "Rows218_009", "Rows218_010", "Rows218_011", "Rows218_012", "Rows218_013", "Rows218_014", "Rows218_015", "Rows218_016", "Rows218_017", "Rows218_018", "Rows218_019", "Rows218_020", "Rows218_021", "Rows218_022", "Rows218_023", "Rows218_024", "Rows218_025", "Rows218_026", "Rows218_027", "Rows218_028", "Rows218_029", "Rows218_030", "Rows218_031", "Rows218_032", "Rows218_033", "Rows218_034", "Rows218_035", "Rows218_036", "Rows218_037", "Rows218_038", "Rows218_039", "Rows218_040", "Rows218_041", "Rows218_042", "Rows218_043", "Rows218_044", "Rows218_045", "Rows218_046", "Rows218_047", "Rows218_048", "Rows218_049", "Rows218_050", "Rows218_051", "Rows218_052", "Rows218_053", "Rows218_054", "Rows218_055", "Rows218_056", "Rows218_057", "Rows218_058", "Rows218_059", "Rows218_060", "Rows218_061", "Rows218_062", "Rows218_063", "Rows218_064", "Rows218_065", "Rows218_066", "Rows218_067", "Rows218_068", "Rows218_069", "Rows218_070", "Rows218_071", "Rows218_072", "Rows218_073", "Rows218_074", "Rows218_075", "Rows218_076", "Rows218_077", "Rows218_078", "Rows218_079", "Rows218_080", "Rows218_081", "Rows218_082", "Rows218_083", "Rows218_084", "Rows218_085", "Rows218_086", "Rows218_087", "Rows218_088", "Rows218_089", "Rows218_090", "Rows218_091", "Rows218_092", "Rows218_093", "Rows218_094", "Rows218_095", "Rows218_096", "Rows218_097", "Rows218_098", "Rows218_099", "Rows218_100", "Rows218_101", "Rows218_102", "Rows218_103", "Rows218_104", "AllRows218", "Initial218_00", "Initial218_01", "Initial218_02", "Initial218_03", "Initial218_04", "Initial218_05", "Initial218_06", "Initial218_07", "Initial218_08", "Initial218_09", "Initial218", "Short218_00", "Short218_01", "Short218_02", "Short218_03", "Short218_04", "Short218_05", "Short218_06", "Short218_07", "Short218_08", "Short218_09", "Short218_10", "Short218_11", "Short218_12", "Short218_13", "Short218_14", "Short218_15", "Short218_16", "Short218_17", "Short218", "Conclusion218"]
  for mod in env.allImportedModuleNames do
    logInfo m!"AUDIT_IMPORT {mod}"
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then
            logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else
            throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          logInfo m!"AUDIT_THEOREM {mod} {name}"
          elabCommand (← `(command| #print axioms $(mkIdent name)))
        | _ => pure ()
