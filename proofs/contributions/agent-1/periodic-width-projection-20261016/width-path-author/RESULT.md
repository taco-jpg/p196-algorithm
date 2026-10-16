# WidthPath author verification

`Agent1PeriodicWidthPath.lean` is frozen at SHA-256
`e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241`.
Strict author compilation and the complete new-module audit passed. This is an
incremental author check using fourteen pinned dependency objects from the
previous fresh phase build; it is not an independent clean rebuild.

## Exact contract

`QuotientPath B H w N` requires bounded coefficients, period length four, and
the three literal successor equalities for each index `i < N`. It imposes no
additional condition at index `N`. The outer and center successors use the
maximal quotient; the period successor is the actual `rawPeriod`.

Write `I i = 2 * (B i).length + (H i).length`, `C N = quotientClockSum B H w N`
and `D N = quotientDeltaSum B H w N`. The exported results are:

- `quotient_path_width_balance`: `(I N : Int) + 8 * D N = (I 0 : Int) + (C N : Int)`.
- `quotient_path_equal_width_clock`: if `I N = I 0`, then
  `8 * D N = (C N : Int)`, `8 ∣ C N`, and `D N = ((C N / 8 : Nat) : Int)`.

Both results include `N = 0`. They reuse the original
`Agent1.Periodic.quotient_width_balance`. No safety, full validity, seed
realization, or exponent guard is assumed. Consequently these results do not
assert a guarded natural exponent trajectory or an ordinary numeric orbit.
Divisibility concerns the actual accumulated raw overflow bits, not the
number of transitions. No positive overflow count is asserted.

## Execution

The installed compiler is Lean 4.19.0, SHA-256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every attempt retained its exact source or audit snapshot, command, working
directory, `LEAN_PATH`, driver, log and exit receipt.

Author compile `attempt-002` passed with exit 0 in 0.387 seconds. It used
`--trust=0 -j1 -DElab.async=false`, one CPU, and a hard 1792 MiB address-space
limit; peak resident memory was 455444 KiB. Its object SHA-256 is
`4970a0e33b79e4e120f4038fbd408d0d941dc95c4b13863b6784b7dbf9ef0757`.

The only project dependencies came from
`/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source`.
`attempt-002/dependencies.json` records the fourteen-module exact import
closure, source and object hashes, and the prior PASS receipt. Its prior
source commit is `e2ce8e1cd121b78ce839c120d0d475990f561b8f`.

Complete audit `audit-006` passed with exit 0 in 1.612 seconds using the same
strict Lean options. All 13 theorem constants originating in the new module
(two authored endpoints plus generated support) and all seven safe
definitions were checked transitively with `Lean.collectAxioms`. Literal
`#check` and `#print axioms` covered all five public declarations. The three
public definitions are axiom-free; the theorem axiom union is exactly
`propext`, `Classical.choice`, `Quot.sound`. Eleven compiler-generated
executable helper declarations were explicitly inventoried; these are not
accepted theorem evidence. Every theorem and safe-definition proof chain
was still checked. No new axiom or unexpected constant class is permitted.

The successful audit used one CPU and a 1500 MiB resident-memory watchdog
polling at 10 ms, with no virtual-address cap. The watchdog did not trigger;
kernel peak resident memory was 753412 KiB (sampled high-water mark
753476 KiB). The audit log SHA-256 is
`df821c4695c740f7c72e6b15e25d278c66e377be05fe2cc7c60a2b5fe8d55e06`.

## Preserved failures

- `attempt-001`: the advertised Lean `-M1536` option failed immediately with
  `unknown configuration option 'max_memory'`. Removing that unsupported
  option left the source unchanged; operating-system limits remained.
- `audit-001` through `audit-003`: SIGSEGV before output with hard virtual
  address-space caps of 1792 or 1900 MiB, including a minimal-import attempt.
  The successful resident-limited audit supports the diagnosis that imported
  metadata mappings exceeded those virtual-address limits.
- `audit-004` and `audit-005`: the strict declaration classifier rejected a
  generated matcher/compiler helper. The latter retained a complete
  nonsafe-definition inventory. `audit-006` explicitly inventories those
  eleven generated implementation names while retaining the same proof
  and safe-definition axiom checks. No theorem source changed.

`FILES.json` hashes every retained text evidence file and the frozen source.
Generated `.olean` output is intentionally omitted from that publication
manifest; its hash is retained in the execution records. The parent owns
publication and combined fresh verification.
