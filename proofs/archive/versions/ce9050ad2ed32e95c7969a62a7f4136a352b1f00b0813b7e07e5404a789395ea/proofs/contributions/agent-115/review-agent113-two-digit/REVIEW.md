# Agent #115 independent review of `agent113-two-digit-prefix-lean`

Task `agent115-review-agent113-two-digit` (claimed on `p196/coordination` at
`fcbe3bc`). Review = replication; **no new theorem**. Package owner: Agent #113
(PR #47).

**Verdict: PASS** for the stated scope.

## Pins

- Reviewed source: `10eea4e977f864d605c97880f2347ba5f49d14bb`
  (`research/agent-113/s20261015`; Lean proof source `4a584d1` per the task
  record, `10eea4e` adds evidence only). Package
  `proofs/contributions/agent-113/two-digit-prefix/`.
- Closure: 20 modules — base `LychrelDigitSums.lean` (SHA-256 `ca5f4652…dc0b57`),
  Agent #104's `PalindromeBridge.lean` (byte-identical to current main), and the 18
  `TwoDigit*.lean` modules. Hashes recorded by Agent #115 in `build/SCOPE113.json`.
- Official Lean 4.19.0 `6caaee842e94`, `bin/lean` SHA-256 `92c3d35b…e023`.

## 1. Fresh build — PASS

Independent driver `build/agent115_build_scope113.py` (Agent #113's `build.sh`
was not used): empty directory, every module compiled from source with
`-DElab.async=false`, one process at a time, forbidden-token scan outside
comments. All 20 modules exit 0; the largest certificate module (`TwoDigitCert65`)
took 62 s and every module stayed under 0.5 GB except the base (2.3 GB).
Report: `build/build_report.json`; logs: `build/logs/`.

## 2. Axiom audit — PASS

`audit/Agent115Audit113.lean` enumerates every theorem whose defining module is
one of the 20 closure modules and runs `Lean.collectAxioms`: 2,852 theorems
(1,063 in `Agent113.*` namespaces), transitive union exactly
`{propext, Classical.choice, Quot.sound}` (`audit/axiom_inventory.tsv`). The 13
axiom-kind constants found are compiler-generated specializations in the base
module (`…_spec_N`, `…_elambda_1`); none occurs in any theorem's axioms.
`no_196_thirteen`, `no_196_thirteen_arith` and all 13 `exact_depth_*` use the
three standard axioms.

## 3. Statement fidelity — PASS

- `ancestry_bound_ab : ∀ A P t, 0 < A → PalindromeStartsTwo a b P →
  Lychrel196.orbit A t = P → t ≤ h` for the 13 pairs, with
  `(10:1, 20:2, 32:2, 40:3, 41:3, 60:3, 64:3, 76:3, 80:4, 81:4, 82:4, 83:4, 65:6)`;
  these are exactly the bounds of `p196_thirteen_prefix_theorem.md` §1, where
  `H(P)` allows intermediate palindromes and starts at any positive `A`.
- `PalindromeStartsTwo a b P = Palindrome P ∧ StartsTwo a b P`;
  `StartsTwo` asks for a canonical decimal representation (`Canonical`: digits
  ≤ 9, nonzero leading digit, value `P`) of width `W ≥ 2` whose two leading digits
  are `a, b`. `startsTwo_iff` gives the arithmetic reading
  `1 ≤ a ≤ 9 ∧ b ≤ 9 ∧ ∃ k, P / 10^k = 10a + b`. `Palindrome n` is
  `reverse10 n = n`. No width bound or interior-digit restriction is present.
- `no_196_thirteen : ∀ t, ∀ ab ∈ thirteenPrefixes, ¬ PalindromeStartsTwo ab.1 ab.2
  (orbit 196 t)`, with `thirteenPrefixes` the 13 listed pairs, and
  `no_196_thirteen_arith : Palindrome (orbit 196 t) → orbit 196 t / 10^k ∉
  [10,20,32,40,41,60,64,65,76,80,81,82,83]` for every `k`.
- `exact_depth_*` pair each bound with an explicit positive start reaching a
  first palindrome of that prefix at exactly that time (kernel `decide`), so the
  13 bounds are attained.
- Prefix 10 has leading digit 1; the package handles its last step with its
  own `descending_last_step`, which is covered by the compiled proof.

This excludes 13 two-digit palindrome families from the orbit of 196 at every
time. It does not prove that 196 is a Lychrel number and says nothing about
other prefixes.

## Not checked

No novelty assessment; no rerun of Agent #113's Python/C dynamic-programming
diagnostics (they are not part of the proof).
