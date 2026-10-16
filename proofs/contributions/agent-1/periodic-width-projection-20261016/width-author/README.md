# Width residue author increment

Frozen source: `proofs/Agent1PeriodicWidth.lean`, SHA256
`0ae4dbb296dd596f305c115b7626afc44f69d7fdc0de7d56140205e4bbff8be3`,
Git blob `3ef9f257fe773f362c60d5840efe2029e673a94a`.
Author: Agent1 specialist `/root/research_status/numeric_bridge_review`.
The parent owns integration and independent closure verification.

## Checked interface and interpretation

The module imports only `Agent1PeriodicQuotient`. Its five public declarations
are in namespace `Agent1.Periodic`:

* `widthResidue B H := (2 * B.length + H.length) % 8`.
* `widthResidue_lt B H` proves this residue is below eight.
* `periodicWord_length_mod_eight B H w k hlen` proves the complete word
  length has this residue when `w.length = 4`. It permits `k = 0`, empty
  interfaces, and arbitrary coefficients; no validity premise is needed.
* `quotient_width_mod_eight B H w hB hH hw hlen` proves the actual maximal
  quotient interface width has residue
  `(2 * B.length + H.length + rawGamma B H w) % 8`.
* `quotient_widthResidue B H w hB hH hw hlen` expresses the same update as
  `(widthResidue B H + rawGamma B H w) % 8`.

The quotient lemmas retain exactly the existing coefficient bounds
`Bounded B 18`, `Bounded H 18`, `Bounded w 18`, and period length four.
They use the original signed `quotient_width_balance`; the word-length
lemma uses the original `periodicWord_length`. They add no exponent guard,
safety premise, canonical realization, positivity premise, or new carry
definition. This local accounting does not assert a temporal period
divisible by eight, positive overflow count, cycle existence, or an
ordinary integer orbit.

The exact elaborated public types and axioms are in
`audit-003/audit.log`.

## Actual checks and retained attempts

Compiler: official Lean 4.19.0, commit `6caaee842e94`, binary SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every invocation used `--trust=0 -j1 -DElab.async=false`.
This is an **author increment**, reusing the supplied previously built
14-module Quotient dependency closure. It is not a new clean closure build.
Source SHA256, Git blob, and object SHA256 pins were checked against the
Quotient registry and working source before compilation; source and object
pins were rechecked after successful compilation and audit. Full pins are
in `attempt-002/receipt.json`.

| Attempt | Actual result |
| --- | --- |
| `attempt-001` | FAIL before elaboration: optional `--memory=1400` produced `unknown configuration option 'max_memory'`. Source unchanged. |
| `attempt-002` | PASS in 0.43 s after removing only the unsupported flag; operating-system virtual-address limit remained 1900 MiB. |
| `audit-001` | FAIL, SIGSEGV before any output under 1900 MiB virtual-address limit, importing full `Lean`. |
| `audit-002` | FAIL, SIGSEGV before any output under the same limit, importing only `Lean.Elab.BuiltinEvalCommand`. |
| `audit-003` | PASS in 1.25 s with the unchanged minimal-import audit, one core, and a 1500 MiB physical-RSS watchdog sampled every 10 ms. No virtual-address cap. |

The successful audit's kernel peak RSS was 751920 KiB; the sampled peak
was 752048 KiB. Its observed virtual address size reached 2068968 KiB,
above the previous 1900 MiB virtual-address cap. The watchdog never fired.
All failures and their actual commands, diagnostics, and source snapshots
are retained. These resource failures were not proof failures.

`audit-003` enumerates every declaration originating in the new module,
audits transitive axioms for all theorem, safe definition, and safe opaque
constants, and rejects custom safe axioms or axioms outside
`propext`, `Classical.choice`, and `Quot.sound`.
Result: **6 theorem constants, 1 safe definition, 0 safe opaque constants**;
the six include the four named theorems and two elaborator-generated proof
constants. The axiom union is exactly the standard three above. It also
records two generated unsafe implementation definitions, zero partial
definitions, zero unsafe implementation axioms, and zero unsafe opaque
constants; none is a logical proof dependency outside the audited set.

`run-attempt.py` reproduces the accepted strict compile in a new labelled
directory; `run-audit.py` reproduces the accepted module audit in a new
labelled directory. Both preserve existing attempt directories. No original
dependency source or object was modified, and no Git writes were performed
by this author helper.
