# Finite nine-return phase persistence author receipt

Accepted claim `ec362fbee11009628944ee14ec6a1d1b29990e2e`.
Agent1 specialist `/root/research_status/cap4_existing_theorems`.
Worktree `/workspace/p196-agent1-nine-cycle-20261017`, foundation7f23ce83.
Root remains sole Git writer and issue61 relay.

## Frozen source and interfaces

Source: `proofs/Agent1PeriodicNinesPath.lean`.
SHA256: `72518762371d6174e300104d817b0e4cbe7a72d2f0f548ce6b6a9e1c79717866`.
Git blob identity (read-only): `8f6097c21dcad8affd4a2053ff8482e229358761`.
Direct imports: Agent1PeriodicWidthPath, Agent1PeriodicNines,
Agent1PeriodicPhase, Agent1PeriodicZeroPeriod.

`quotient_path_nines_phase B H w N hp hw0 hwN` proves
`∀ i, i≤N → w i=[9,9,9,9]`, where hp is the existing exact QuotientPath,
hw0 states the initial phase is nine and hwN states the endpoint is nine.
It includes N=0 and requires no original validity, positive N, exterior or
center return, safety, exponent, or catalog premise.

`quotient_path_nines_entry_sum B H w N hp hw0 hwN i hi` proves, for i<N,
`leftEntry (B i) + rightEntry (B i) (H i) [9,9,9,9] = 1`.
Both entries are the unchanged actual finite scans. No free bit is selected.

The private local eighteen absorption proof specializes existing
rawPeriod_eq_phaseImage at the actual bounded rawGamma. Existing
rawPeriod_nines and nines_entry_bits supply the zero/nine/eighteen
trichotomy, while rawPeriod_zero supplies zero absorption. Forward
induction confines the finite path to those three phases; backward
induction from its nine endpoint excludes the two absorbing exits. All
uses of the path's coefficient bounds are at used sources i<N. The
entry-sum companion then compares the actual nine update's first column.

This is conditional nine persistence. It does not assert arbitrary nine
states persist, construct a full tuple cycle, prove a generic nine-run
ancestry law, or supply a center obstruction. It adds no graph certificate
or imported catalog/rank/no-return dependency. The later same-seed safety
composition belongs to the separate numeric author.

## Retained attempts and final verification

- `attempt-001`: failed compile. Omega saw the terminalCarry expression and
  rawGamma as separate atoms because the inferred carry-bound type had not
  been restated at rawGamma. Exact source, command and failure log retained.
  Lean's generated sorryAx report belongs only to this rejected elaboration;
  no sorry/admit appears in source.
- `attempt-002`: the single explicit rawGamma type annotation resolves that
  definitional presentation. Strict compile and full new-module origin
  audit both PASS. This source is frozen without further changes.

Pinned Lean4.19.0 commit6caaee842e94. Compiler SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Flags: `--trust=0 -j1 -DElab.async=false`;4GiB address-space cap.
Final compile: exit0,0.4160s,451360KiB maximum child RSS.
Final audit: exit0,1.3183s,753940KiB maximum child RSS.
Final object SHA256:
`e2f3c12921db554e0af373154c850c2af7268f041cd9868f96da403c76dfaf0c`.

The full origin audit checks16 theorem constants, including private and
compiler-generated proof declarations; both public endpoints are required.
There are0 definitions,0 runtime entries and0 custom axioms. The theorem
axiom union is exactly propext, Classical.choice, Quot.sound. Any other
constant category or nonstandard axiom is rejected. Both public theorem
axiom sets are also printed in the canonical source.

This author increment reuses21 source/hash-pinned dependency objects from
the prior parent-clean ReturnCore build. It is not a fresh whole-closure
build or an independent package review; the parent performs those checks
separately. Every attempt retains its source/dependency/command metadata.
The manifest hashes all retained text/script evidence and records local
.olean files separately. No Git mutation or external message by this author.
