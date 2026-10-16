# Direct return-certificate saturation consequences

**Evidence label:** formal necessary conditions on an accepted symbolic return
certificate. No certificate instance, realizable infinite seed, all-time orbit,
or assertion about 196 is supplied. This is developer verification, not an
independent semantic review.

The current `CertificateSaturation.lean` proves direct endpoints in namespace
`Agent110.CertificateSaturation`:

| Theorem | Supplied hypotheses | Conclusion |
| --- | --- | --- |
| `period_at_least_forty_two` | `Agent109.Cert.Valid cert`, positive initial exterior, initial `SixPhase` | `42 ≤ cert.P` |
| `saturated_period_constraints` | The preceding hypotheses and `2 * totalGam cert = (cert.P : Int)` | `cert.P % 72 = 0 ∧ 72 ≤ cert.P` |
| `checked_period_at_least_forty_two` | `check cert = true`, original `Admissible0 cert H M`, initial `SixPhase` | `42 ≤ cert.P` |
| `checked_saturated_period_constraints` | The preceding checker hypotheses and the saturation equality | `cert.P % 72 = 0 ∧ 72 ≤ cert.P` |

There is no block-width bound, maximal-trimming premise, numerical congruence
assumption, or supplied prefix-path hypothesis in these endpoints. Saturation
is an explicit hypothesis only of the saturation conclusions.

`certificate_closed_prefix_path` constructs the exact cyclic path from
`CertificatePrefix.local_prefix_step`. For every edge it records both the
three-column successor and the **actual certificate carry** `gam`. Positive
first coordinates follow from `CertificateCarryBudget.exterior_positive_along`;
all coordinate bounds come from `CertificatePrefix.prefix_bounds`. Classical
choice selects a carry bit from each already-proved local existence statement.

`path_total_eq_totalGam` identifies Agent #4's natural-valued path count with
the signed accounting total. The modulo-two, modulo-nine, and modulo-six facts
needed by `unit_phase_full_cycle_period_at_least_forty_two` are all obtained
from `CertificateConsequences.six_phase_constraints`. Saturation additionally
gives Agent #4's period-divisible-by-eight condition. Combined with the proved
overflow congruence, that forces period divisibility by 72.

The generic `*_of_path` helpers remain reusable conditional theorems. They are
not the final endpoints; the current direct theorems supply their path premise
with a proved exact projection.

## Verification and dependencies

Compiler: official Lean 4.19.0, release commit `6caaee842e94`, through the parent
task's audited compatibility wrapper. `attempt-003` is the current successful
checkpoint: clean compilation and all 10 public theorem axiom queries pass,
using only `propext`, `Classical.choice`, and `Quot.sound`. The theorem count is
audit coverage metadata, not a count of independent major findings.

Direct imports are `CertificateConsequences`, `CertificatePrefix`, and
`SaturationTheorem`. Agent #4's original three files are compiled from their
original paths into an external build directory:

- `proofs/agent4/prefix_growth/PrefixModel.lean`
- `proofs/agent4/prefix_growth/SaturationCertificate.lean`
- `proofs/agent4/prefix_growth/SaturationTheorem.lean`

The runtime agent's fresh dependency compilation and 28-theorem audit are in
the sibling `saturation-dependency/` directory. Agent #4's finite checks use
ordinary kernel-checked `decide +kernel`; the resulting theorem axioms are
included in the transitive final endpoint audit. No custom axiom, admitted
proof, native Boolean evaluator, or external evaluation is introduced here.

The composition development rebuilds `CertificatePrefix.lean` in its own
external build directory against those same shared dependencies; its log and
exact source hash are retained in `prefix-dependency-rebuild-02.*`.

Replay the prefix dependency in a build directory containing a copy of its
published source, with `LEAN_PATH` resolving the old certificate modules, the
fresh Agent #4 dependency modules, and the Agent #109 dependency modules. Then:

```sh
python3 proofs/contributions/agent-110/certificate-budget/saturation-development/verify.py \
  --lean /path/to/lean-4.19.0-wrapper \
  --deps /path/to/prefix-build /path/to/certificate-build \
    /path/to/agent4-dependencies /path/to/agent109-dependencies \
  --build /path/to/saturation-build
```

The driver retains exact source snapshots, dependency hashes, commands, logs,
and a generated `#print axioms` source for each successful source compile.
Compiled artifacts and duplicate dependency sources are reproducible
infrastructure kept outside this evidence directory.

## Full development history

- `attempt-001`: failed on indentation of an explicitly constructed structure
  literal; retained source and compiler output. No numerical obligation failed.
- `attempt-002`: five generic projection/path composition theorems compiled and
  passed their complete axiom audit. At that checkpoint the direct certificate
  endpoint was still **WIP**, pending the local projection theorem.
- `prefix-dependency-rebuild-01`: compiler rejected an input outside its current
  root directory. The correction sets the compilation working directory to the
  external build directory; the failure output and command remain retained.
- `prefix-dependency-rebuild-02`: successful fresh composition-side build of
  the completed prefix projection, with its 14 public theorem axiom outputs.
- `attempt-003`: supplied the exact path from `CertificatePrefix`, added all
  direct/checker endpoints above, and passed all 10 public theorem axiom queries.
  This supersedes the earlier WIP scope without deleting its evidence.
