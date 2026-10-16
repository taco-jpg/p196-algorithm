# Interface width bounds zero-period digit sum

Author helper under claim `agent1-periodic-zero-escape-20261016`, published at `0db777cb118e3c395cb495a1a8e8dc7b13cf9893`. Only `proofs/Agent1PeriodicZeroInterfaceMass.lean` and this evidence directory were written; no Git state or external coordination messages were changed.

Frozen source SHA-256: `a8da314abda733d33e3b29e3f205e6db5d3e88fc635f78a6f9740997b30aa529`.

The module imports only `Agent1PeriodicZeroMass` and introduces two public theorems in `Agent1.Periodic`:

- `zero_interface_mass_le B H hv` proves `2*B.sum + H.sum ≤ 18*(2*B.length + H.length)` from original `ValidPeriodic B H [0,0,0,0]`. Its private list lemma sums the original coefficient bound 18 over each finite word.
- `zero_period_digitSum_le_width B H k n d M hv hc hrep hwidth` proves `DecimalMass.digitSum n ≤ 9*M` for every original canonical realization of `periodicWord B H [0,0,0,0] k`, given every finite pair coefficient and interface width `2*B.length + H.length ≤ M`. It uses the exact existing identity `zero_period_digitSum`, which states that twice the actual digit sum equals the finite interface mass.

Neither theorem assumes safety, a positive cap, or an exponent guard. The numeric statement includes `k=0` and `M=0` whenever its existing canonical/validity/representation hypotheses hold. It does not introduce a new seed, orbit, transition, escape bound, or palindrome assertion; parent owns the subsequent finite-escape argument.

`attempt-001` compiled the new module on the first attempt with official Lean 4.19.0, commit `6caaee842e94`, and flags `--trust=0 -j1 -DElab.async=false`; exit zero in 0.293 seconds. Its dependency objects came from the previously fresh 24-module review directory `/workspace/p196-agent1-session-20261016/periodic-zero-cycle-review-clean-001`. Every imported dependency source was checked against `Agent1PeriodicZeroCycle.registry.json`, its local repository counterpart, and the expected Git blob; source/object hashes are retained in the receipt and checked again after execution. This is a strict **author increment**, not a new fresh rebuild of those dependencies.

`audit-001` passed with the same strict flags in 1.518 seconds. It prints both public declaration types and axiom sets, then selects and audits every theorem and safe definition by actual new-module origin. There are **six theorem constants**, including the private helper and generated auxiliaries, and zero definitions or opaque declarations requiring logical audit. Their complete logical axiom union is **`propext` and `Quot.sound`**. No unsafe implementation axioms, unsafe definitions, partial definitions, or unsafe opaque entries originate in this module. Source scanning found no active proof placeholders, custom axioms, or external proof-oracle tokens.

The compiled object is `attempt-001/Agent1PeriodicZeroInterfaceMass.olean`. For local continuation, include that directory before the pinned dependency directory in `LEAN_PATH`. Publication can omit generated objects while preserving the source snapshots, actual logs, commands, and receipts.

The source is frozen; `frozen-receipt.json` records final source/object identities and all dependency rechecks. Parent will arrange independent full-closure verification. No failed attempt occurred.
