# Semantic acceptance after independent hosted execution

**Accepted, within the exact scope below.** This addendum closes the execution
gate recorded in the unchanged initial eight-file semantic checkpoint. It
accepts the fifteen original `Agent13SafeWeights` exports and the fifteen
explicit statement applications in `Agent104.RealWeightsExactTypes`. The
applications verify the stated types; they are not fifteen additional
mathematical results. No semantic gap or unsupplied actual-map bridge was
found. This does not prove P196 or decimal Lychrel existence.

The original source remains commit
`122367d4935f0b4cd9e0bee19e4121ec66b3164b`. A new independent hosted run,
[38700059129](https://github.com/taco-jpg/p196-algorithm/actions/runs/38700059129),
attempt 1, executed review commit
`39d9f3eb196aae5071b5c48e8a5166dad388ce9d`. It rebuilt the six original
core/family/weight modules and the exact-type harness from an initially
object-free project. The harness is the unchanged fixture first published at
`ab6768ef000358b5f81c6807db674dc7515819c9`. This is distinct from the author's
earlier CI. The semantic reviewer executed no Lean process; this acceptance
combines the prior source review with independent inspection of the new
executor's actual logs, types, source/object pins, and artifact bytes.

For the ordinary decimal map `T(n) = n + reverse10(n)`, `Safe n` means
`0 < n`, `n` is not palindromic, and `T(n)` is not palindromic. The accepted
incoming operator sums over the **complete** set of safe `n` with `T(n)=y`.
The finite range is exact because every such predecessor satisfies `n ≤ y`;
it is not a truncation or an assertion that the constructed family exhausts
the fiber.

For every real-valued weight `w` that is strictly positive on `Safe` and
nonincreasing between safe arguments, and every natural `m ≥ 2`, set
`y_m = 10^(2*m) + 99*10^(m-1) - 1`. The accepted statements give

```text
incoming(w,y_m) / w(y_m) ≥ 9*10^(m-2),
incoming(w,y_m) / w(y_m) > (9/100)*sqrt(10/11)*sqrt(y_m).
```

The actual family theorem supplies `Safe y_m`; strict positivity of the
denominator then follows from the stated weight hypothesis. Neither is an
unproved caller-supplied bridge. The multiplier statement quantifies over
**every real `C`**, including negative values, and gives a safe `y` with
`C*w(y) < incoming(w,y)`. Thus no single real multiplier bounds this incoming
sum at all safe targets under these hypotheses. There is no restriction on
weight values outside `Safe` and no summability premise. The square-root
coefficient uses exact real division and square roots; the whole natural
target expression is coerced to the reals. The width assumption is retained.

The exact accepted export set is below. Each original name is prefixed by
`Agent13SafeWeights.`; its compiled application has the same base name with
suffix `_type`, prefixed by `Agent104.RealWeightsExactTypes.`. Complete
source headers remain in `statements.json` and `ExactTypes.lean`; actual
elaborated and raw expression types are in the retained audit log.

| Original export | Accepted content |
| --- | --- |
| `predecessor_le` | Actual predecessors are at most the target. |
| `mem_safeFiber_iff` | Exact membership in the full safe predecessor fiber. |
| `full_safe_fiber_finite` | Finiteness of that unrestricted predecessor set. |
| `incoming_nonneg` | Nonnegative incoming sum at every target. |
| `family_sum_le_incoming` | Every injective safe predecessor family gives a lower partial sum. |
| `finite_family_weight_lower` | At a safe target, an `N`-element family gives `N*w(y) ≤ incoming(w,y)`. |
| `incoming_weight_lower` | Exact family-size multiplication bound for every `m ≥ 2`. |
| `incoming_weight_ratio` | The corresponding ratio bound with justified positive divisor. |
| `no_uniform_multiplier` | A strict counterexample for each real multiplier. |
| `not_exists_uniform_bound` | Negation of a uniform real bound on all safe targets. |
| `target_size_bound_nat` | Strict integral target-size bound. |
| `target_size_bound_real` | Its exact real-coercion form. |
| `family_size_scaled_power` | Exact real scaling identity for the family count. |
| `sqrt_scale_lt_family_size` | Strict square-root comparison with that count. |
| `incoming_weight_sqrt_lower` | Strict square-root lower bound for the incoming ratio. |

The semantic reviewer independently reparsed the raw audit rather than
accepting only a green CI status. Its 1,144 unique compiled theorem records
match the report exactly: 1,129 from the six original modules and 15 from
the harness. Every record has one matching transitive axiom report, all
within `propext`, `Classical.choice`, and `Quot.sound`. The thirteen generated
unsafe implementation axiom declarations occur in none of those theorem
dependencies. Both type-output formats contain exactly the fifteen required
exports, and all fifteen named applications occur in the compiled theorem
inventory. Inspection of the expression types confirms `Real` weights and
multipliers, the actual `Lychrel196.step` and `Safe`, exact natural casts,
real division, and `Real.sqrt`. All nineteen recorded commands exited zero.
These counts describe audit coverage, not the number of mathematical claims.

The original six source snapshots were checked against their Git objects,
and all seven fresh local object files were rehashed from the downloaded
artifact. Both complete artifact inventories, their exact file sets, every
command-log hash, and the original eight semantic-file hashes passed. The
reviewer also independently checked the ZIP size, SHA256, and all 56 ZIP
members against the extraction. Artifact `11955822178` is 5,786,209 bytes;
its ZIP SHA256 is
`b7e69c40b55ac87bb7580b33df2524b1327995d8e1b9057ace339c3a80985556`.

The runtime was official Lean 4.19.0, release commit `6caaee842e94`, with
the compiler/archive pins retained in the report. Mathlib was pinned to
`c44e0c8ee63ca166450922a373c7409c5d26b00b` and all eight package revisions
to its exact manifest. **The official compiled Mathlib/dependency cache was
reused; Mathlib was not rebuilt from source.** Actual import records contain
1,332 cached Mathlib/package objects, 1,303 official Lean objects, and the
seven fresh local objects. The pinned checker requires actual `findOLean`
paths, matching pre/post object hashes, matching official archive members,
and committed source bytes for every imported cached module. The reviewer
inspected that enforcement and its successful raw records. The external
objects are absent from the downloaded artifact; no second local rehash or
source rebuild of those external libraries is claimed.

Durable raw evidence is under `../execution/hosted-38700059129-1/`.
`independent-audit/verification.json` has SHA256
`3e5c6d7032fac10636b7f243b3c4408faf56ced1f7bab479178e90f4c85a1e80`;
`independent-audit/logs/AllCompiledAxioms.log` has SHA256
`5eab3f59feaea787aa7545d6e58677ed0253aec5058f425d73fc6935de088741`.
The review checked all 42 retained artifact files byte-for-byte against the
original extraction and the full 67-file execution publication manifest.
The fourteen declared exclusions are seven duplicate source copies and
seven compiled objects; exact recovery mappings and hashes remain in
`../execution/artifact-selection.json`. These packaging exclusions do not
change the original execution or the object-byte checks performed here.

The initial rational-weight computations, negative-outside-`Safe` examples,
zero-weight discussion, and finite width checks remain diagnostics or prose.
They are **not additional accepted Lean fixture theorems**. No conclusion
about unrestricted nonmonotone weights, other weighting methods, or infinite
orbit survival is added. Agent13 retains ownership of the original results.
`acceptance.json` records the exact accepted names, raw evidence hashes,
publication checks, and the unchanged initial checkpoint.
