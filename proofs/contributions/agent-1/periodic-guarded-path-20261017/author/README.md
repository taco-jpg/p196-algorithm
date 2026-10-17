# Guarded finite quotient paths: author evidence

Author: Agent1 specialist `/root/research_status/numeric_bridge_review`.
Accepted coordination claim: `9d6dc9caa3e77b9036b348ac6d77c3f49553ba30`.
The parent owns Git integration and publication. This helper wrote only its
assigned mathematical module and this author evidence directory.

Frozen source: `proofs/Agent1PeriodicGuardedPath.lean`.
SHA256: `66b821219ee88fa711a88eabc6985b33525e3ebaa0f224430395202e2012d916`.
Git blob: `e80d35796417b6c754067c53c16193d2fbc153b1`.

## Exact interface and semantics

There are six public declarations in namespace `Agent1.Periodic`:

* `quotientPathWord B H w k i` is the complete original periodic template
  with the supplied blocks and copy count at index i.
* `quotientPathExponent B H w k0 i` is the literal natural recursion:
  start at k0, then subtract two and add both actual stripped-period counts.
* `quotient_path_guarded_step` identifies each used transition with
  `Agent8.stepWord`, using all three exact `QuotientPath` successor equations
  and the supplied exponent recurrence. The guard is required only at
  source indices strictly before N.
* `quotient_path_actual_prefix` keeps one supplied ordinary seed n fixed
  and proves positivity, original `DecimalDigits.Canonical`, and every
  in-range original column sum for all actual `Lychrel196.orbit n t`, t≤N.
  It includes N=0 without requiring any guard or recurrence at that unused
  transition. No guard is added at the final endpoint.
* `quotientPathExponent_lower_bound` proves the explicit finite budget:
  starting at 2*N+3 gives exponent at least 2*(N-i)+3 for every i≤N.
  This arithmetic theorem does not require path validity or coefficient
  bounds because the added counts are natural numbers.
* `quotient_path_finite_realizable` uses initial original `ValidPeriodic`
  and a supplied exact finite path to select one positive canonical seed
  once at copy count 2*N+3. That same seed realizes every displayed state
  through N. The seed is existential outside the finite time quantifier,
  and may depend on the path and N.

The exact elaborated public types and all six axiom prints are retained in
`audit-001/lean.log`. The source reuses `quotient_step_bounded`,
`actual_step_representation`, `periodicWord_realizable`,
`DecimalDigits.value_positive`, and `DecimalDigits.orbit_positive`.
It does not reprove generic decimal soundness or build a fresh seed at
each time. Original METHOD_AND_PROOF.md section4 line164 is attributed
for its prior instruction to choose a large enough finite starting exponent.

There is no assertion of one seed working for every horizon, no exchange of
the finite-horizon/seed quantifiers, no abstract graph-walk realization,
no construction of a full path, no affirmative interface-cycle search,
and no safety, nonpalindromicity, return, or 196 conclusion. Agent17's
uniform-seed lane and the historical affirmative-interface lane remain
outside this result.

## Actual verification

Official Lean 4.19.0, commit `6caaee842e94`, was run explicitly with
`--trust=0 -j1 -DElab.async=false`. The driver uses a 600-second timeout
and a 1500 MiB RSS stop threshold sampled every10ms, with no virtual-address
cap. No watchdog fired and no Lean failures occurred.

| Invocation | Result | Seconds | Kernel peak RSS, KiB |
| --- | --- | ---: | ---: |
| attempt-001: complete mathematical module | PASS | 0.47 | 459632 |
| audit-001: complete new-module origin audit | PASS | 1.44 | 759088 |

Every invocation retains the exact source snapshot, driver, command,
compiler identity, dependency pins, actual output, and result. This is an
author increment using21 reused dependencies, not a fresh closure build.
The literal imports are WidthPath, ZeroNumeric, and Realizability; their
static union gives22 modules including the new source. All21 dependency
source hashes, Git blobs, literal imports, working files, retained successful
fresh-build source identities, and compiler hashes were checked. Object
hashes are recorded and dependency immutability is rechecked after each run.
The ignored `dependencies/` directory is a local cache only; exact provenance
is preserved in each `source-and-dependencies.json`.

The audit enumerates every constant originating in the new module and
traverses all16 theorem constants, all5 safe definitions, and0 safe opaques.
The actual transitive logical axiom union is exactly the standard three:
`propext`, `Classical.choice`, and `Quot.sound`. No sorry, custom logical
axiom, unsafe axiom, or unsafe opaque is present. Compiler runtime constants
are explicitly inventoried separately, including the generated partial
helper `quotientPathExponent._unsafe_rec`; that helper is not a mathematical
partial definition or a logical theorem premise. Exact runtime counts and
all public exports are in `audit-001/origin-summary.json`.

`SOURCE_SCOPE.md` preserves the source-only scout (SHA256
`926b7065e6343f5d6e9160017ddefc81fde7105e1dfc488f5ec7f4f13c50bb31`).
`OWNERSHIP_SCOPE.md` preserves the complementary scout (SHA256
`e1b6c103145122ba65b9dddd448546c5988dc62b1fc590f3c6380ec8c3c80a8a`).
Final independent22-module fresh verification and publication are separate
parent/reviewer gates. There are no remaining local author proof obligations.
