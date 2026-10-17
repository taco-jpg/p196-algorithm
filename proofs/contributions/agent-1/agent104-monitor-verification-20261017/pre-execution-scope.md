# Refreshed Agent104 monitor compiler scope

This is read-only source scouting. No Lean command, source repair, Git write,
mathematical proof or new external offer was performed. The original sealed
`agent104-monitor-scout/` is unchanged. Root will record the narrow claim
before any compiler execution.

The actual author comments 6228796729 and 6228809415 were read and retained.
`07bf76c` corrected the exceptional monitor branch for m1 from true to false;
`4b86bfc` corrected the Python semantic check. The earlier67b→32e comparison
remains empty for Lean sources. `260a70f0375993f4cbb371e92844097284361916`
adds only the two explicitly unproved Prop definitions
`monitorBadWordCorrespondence` and `safetyRowsSound` to the corrected module.
Its SHA256 is c54af29492579f97972cd7750d734f641fa7a03756f4eceb28204b6ae62a22e6,
Git blob5e61a1e844d7615eb58563ba98e479d281b94d24.

The actual branch readback had advanced again to
`e67807e6d3d7a0cbd43d26257f37d1dd66e43ae6`. Root explicitly selected this
immutable head for service; do not follow later moving heads silently.
Its source is `proofs/Agent104DFABadMonitor.lean`, SHA256
`ef835d8428cc54e4e2df1ab31029d6ad30787395a7f2cc24cde292a48f57c2a4`, Git blob
`1bfa3e38a555db46cda81993ee81e1eb4d042721`. This new delta adds `allLow`,
`allExceptional`, absorbing-m3 and same-state m1/m2 run lemmas, plus the two
first-symbol branch equivalences. The exact67b→260a and260a→e678 diffs are
preserved. There is still one distinct monitor source module; its contribution
copy has the identical blob.

## Minimal closure and reproducible inputs

The module still imports only `Agent107DFABoolean` and `Lychrel196Research`.
`minimal-closure-e67807e.json` records the16-module order and every path,
import, SHA256 and Git blob. All15 inherited module blobs are unchanged from
the previously inspected67b tree and Agent107 interface97fe2e595793a021f9cc73e3139ea90a3ac5f5e7.
All16 exact import-name source copies are in `prepared-sources/`; their
SHA256 and Git blob hashes were checked. There is no missing project source.
The sole historical alias remains
`proofs/Lychrel196Research__c696e0ea3db39d92.lean`, SHA256
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
The applicable AGENTS.md blob is unchanged from the prior inspected source.

The build order is:
Lychrel196Research; Agent107TransducerDefs; Agent107TransducerPath;
Agent107TransducerInput; Agent107TransducerOutput; Agent107TransducerNumeric;
Agent107TransducerTablesData; Agent107TransducerTablesChecks;
Agent107TransducerTables; Agent107TransducerReachable; Agent107TransducerGraph;
Agent107DFA; Agent107DFAAlphabet; Agent107DFAChecker; Agent107DFABoolean;
Agent104DFABadMonitor.

The complete proposed command plan is `first-bounded-command-plan.json`:
official pinned Lean4.19.0 at
`/workspace/p196-tools/lean-4.19.0-linux/bin/lean`, explicit
`--trust=0 -j1 -DElab.async=false`, serial fresh objects in a new empty
directory, 4GiB address space,600 seconds per command,1200 seconds overall.
It begins with `-o Lychrel196Research.olean Lychrel196Research.lean` and ends
with `-o Agent104DFABadMonitor.olean Agent104DFABadMonitor.lean`.
Preserve the original first nonzero/timeout/signal and stop; mark all later
commands NOT_RUN. Author retains any repair. Conditional origin/public audits
require all16 compilation commands to pass and must match root's accepted
claim. No prospective audit outcome is asserted.

## Concrete source-only diagnostic concerns

At selected source lines140–141, the q=11 branch of `runMonitor_cons_m1`
asks `simp` to exclude a run from m2 ending at m1. The supplied lemma
`runMonitorFrom_m2_iff_allExceptional` characterizes ending at m2, so it does
not directly establish that exclusion. At line149, the q≤9 branch of
`runMonitor_cons_m2` has the corresponding m1-to-m2 exclusion gap. These
are likely unclosed-simp goals to check, not recorded compiler diagnostics;
no theorem repair is proposed or implemented by this scout.

The potential `(m == .m0)` typeclass concern is resolved by actual source
inspection: pinned Lean Prelude line1006 provides
`instance [DecidableEq α] : BEq α`. No missing BEq claim is made.
The new Prop target references match the inspected imported API names and
namespaces (`Admissible`, `BadWord`, `inputCenter`, `foldPrefix`, `OneHot`,
`DFA.accepts`). They remain unproved targets, not safety theorems.

`public-declarations.json` lists all30 explicit declarations:14 theorem
statements,15 definitions and the MonitorState inductive. Generated constants
must additionally be included by a module-origin audit after successful
compilation. The two universal Prop definitions must never be counted as
proved monitor correspondence or safety.
