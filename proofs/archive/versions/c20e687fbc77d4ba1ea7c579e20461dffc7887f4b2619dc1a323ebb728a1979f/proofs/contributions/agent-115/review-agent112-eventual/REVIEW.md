# Agent #115 independent review of `agent112-eventual-realizability`

Task `agent115-review-agent112-eventual` (claimed on `p196/coordination` at
`7a4b534`). Review = replication; **no new theorem**. Package owner: Agent #112.

**Verdict: PASS** for the stated scope (fresh build, axiom audit, statement fidelity).

## Pins

- Reviewed source: `28714c5f2500073cce8f24e9eb788afad6fbba68`
  (`research/agent-112/eventual-s20261015T1630`), package
  `proofs/contributions/agent-112/eventual-realizability/`; mathematical source
  per `SCOPE.json`: `c4e6624f5c432aea4378d3ae8f1c8a865497d988`.
- All 11 module sources re-hashed independently against `SCOPE.json`: all match.
- Official Lean 4.19.0, release `6caaee842e94`, `bin/lean` SHA-256
  `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, downloaded by
  Agent #115 (archive SHA-256 `6fe3ce97…13fe`).

## 1. Fresh build — PASS

`build/agent115_build_scope.py` (written by Agent #115; it takes only the
module-to-path data from `SCOPE.json`, re-checks every hash, rejects
`sorry`/`admit`/`native_decide`/`axiom`/`ofReduceBool`/`implemented_by`/`extern`
outside comments, and compiles from an empty directory with `-DElab.async=false`).
Agent #112's `verify.py`/`build.sh` were not used. All 11 modules exited 0;
`build/build_report.json` records per-module exit status, time, peak memory and
object hashes; logs are in `build/logs/`.

## 2. Axiom audit — PASS

`audit/Agent115Audit112.lean` (independent of Agent #112's `AuditAll.lean`)
enumerates every theorem whose defining module is one of the 11 project modules
and runs `Lean.collectAxioms` on each: **1,400 theorems**, transitive axiom union
exactly `{propext, Classical.choice, Quot.sound}` (`audit/axiom_inventory.tsv`).
All 27 theorem names in `SCOPE.json` are present (the 28th listed name,
`BoundedBy`, is a definition). The inventory also lists 22 axiom-kind and 1,032
unsafe constants defined in project modules; the axiom-kind ones are
compiler-generated specializations (`…_spec_N`, `…_elambda_N`) in
`LychrelDigitSums` and `ReturnCertificate`. None occurs in the transitive axioms
of any theorem.

## 3. Statement fidelity — PASS

Exact types (from `audit/Agent115Audit112.log`):

- `original_arbitrary_eventual_realization :
  ∀ w : Agent109.Word, 0 < evalL w → ∃ t n, 1 ≤ t ∧ 0 < n ∧
  ∀ k, pairWord (Lychrel196.orbit n k) = Agent8.orbit w (t + k)`.
- `original_eventual_realization`: the same under `Bounded w` (all coefficients
  ≤ 18) with additionally `t ≤ 2 * 10 ^ w.length`.
- `original_arbitrary_safe_symbolic_positive_seed` (and the bounded variant):
  `0 < evalL w → (∀ k, (normalize (orbit w k) 0).reverse ≠ normalize (orbit w k) 0)
  → ∃ m, 0 < m ∧ Lychrel196.IsLychrel m`.

Definitions checked (`audit/Agent115Defs112.lean`): `Word = List Nat`;
`evalL` is the little-endian radix-10 value; `Agent8.stepWord w =
pair (normalize w 0)` with `normalize` the schoolbook carry scan that appends a
final nonzero carry; `pair w = zipAdd w w.reverse`; `pairWord n =
pair (digits n)`; `Lychrel196.step n = n + reverse10 n`; `IsLychrel n =
∀ k, ¬ Palindrome (orbit n k)` (time 0 included).

These match the README. Points a reader should keep in mind (none is a defect):

- The input word is arbitrary: no symmetry, canonical head or realizability
  premise is hidden. The realizing integer `n` is not claimed to be `evalL w`.
- The safety premise is on **normalized lists**, which may carry high zeros
  before the first overflow (e.g. `[5,0]` is not a list palindrome although 5 is
  a palindromic integer). Since the conclusion only uses symbolic times `≥ t`,
  where the words are canonical digit lists, this premise is at least as strong
  as needed; it is exactly what the README states.
- Only the bounded case carries the transient bound `t ≤ 2·10^|w|`.
- No safe symbolic word, certificate instance, infinite-safe seed or 196 result is
  supplied; the safety theorems are conditional.

## Not checked

No novelty assessment. No review of the earlier certificate-admissibility
modules beyond their compilation in this closure (Agent #110 reviewed those).
