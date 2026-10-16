import Lean
import Lychrel196Research

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for n in #[
      ``FoldedDecimal.even_folded_trace_sound,
      ``FoldedDecimal.odd_folded_trace_sound,
      ``FoldedDecimal.folded_emission_no_overflow,
      ``FoldedDecimal.folded_emission_overflow,
      ``FoldedDecimal.folded_delay_update,
      ``FoldedDecimal.representation_next,
      ``FoldedDecimal.valid_word_realizable] do
    let some info := env.find? n | throwError "Missing declaration {n}"
    let deps := info.getUsedConstantsAsSet.toList.filter fun dep =>
      ["FoldedDecimal.", "DecimalDigits.", "Lychrel196."].any
        (fun pfx => pfx.isPrefixOf dep.toString)
    logInfo m!"{n}: {deps}"
