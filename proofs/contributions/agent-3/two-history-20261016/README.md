# Agent #3: two incoming histories for protected overflow fibers

For every `m : Nat` and every `k >= 1`, this contribution proves an exact
family of **`2 ^ m` distinct canonical coefficient words**, each of width
`2 * (m + k + 7)`. Each word has two consecutive zero-carry incoming
transitions, followed by an overflow transition with terminal carry one
to a shared coefficient word. Every ordinary decimal integer realizing
an initial word is positive, avoids palindromes at **all times
`0 <= t <= k + 3`**, and reaches the same ordinary integer at **time four**.
The existence of a positive integer realization is also proved for every
initial word.

The aggregate theorem is
`P196.Agent3.TwoHistory.finite_horizon_two_history_family` in
[TwoHistoryTheorem.lean](TwoHistoryTheorem.lean). The construction formalizes
the preserved
[astra_counting_safe_image_fibers.txt source note](https://github.com/taco-jpg/p196-algorithm/blob/4b4edf976b2c7a9ba1dad80636c0e21c66350325/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_counting_safe_image_fibers.txt),
whose Git blob is `30f8ed333edb2e11402569c62d50def2451ffef4`.

The reservoir and the family depend on the prescribed finite horizon
`k`. The cardinality statement counts coefficient words. The ordinary
integer theorem quantifies over every canonical decimal realization of
each counted word.

## The explicit family and its transitions

A coefficient word records mirrored digit sums, in least-significant
column order. Its entries lie between zero and eighteen. Write
`mirror h = h ++ h.reverse` and let `choice false = 5`,
`choice true = 14`.

For a free Boolean word `xs` of length `m`, the construction appends a
six-bit correction determined by its final joint state. The result,
`completedBits xs`, has length `m + 6`. Its protected coefficient word is

```lean
historyWord2 xs k =
  mirror ([14] ++ (completedBits xs).map choice ++ List.replicate k 18)
```

The finite sixteen-state certificate constructs the two incoming words
`historyWord0 xs k` and `historyWord1 xs k`. The following transitions
hold in the unchanged `Agent8.stepWord` dynamics:

| Current coefficient word | Outer coefficient | Terminal carry from zero | Next coefficient word |
| --- | ---: | ---: | --- |
| `historyWord0 xs k` | `3` | `0` | `historyWord1 xs k` |
| `historyWord1 xs k` | `7` | `0` | `historyWord2 xs k` |
| `historyWord2 xs k` | `14` | `1` | `target (m + 6) k` |

All three current words are canonical and have the same even width
`2 * (m + k + 7)`. The two predecessor words retain a literal central
block `List.replicate (2 * k) 18` between mirrored prefixes of length
`m + 7`; `historyWord0_reservoir` and `historyWord1_reservoir` expose
that shape. The protected word has the same central block by definition.

The common target is the coefficient list

```lean
[5] ++ List.replicate (m + 6) 10 ++ [14] ++
  List.replicate (2 * k - 1) 18 ++ [14] ++
  List.replicate (m + 6) 10 ++ [5]
```

Its width is `2 * (m + k + 7) + 1`. The coefficient transition to this
target is the third transition in the displayed chain.

`historyFamily0 m k` enumerates the initial words as `xs` ranges over all
Boolean lists of length `m`. `historyFamily2 m k` enumerates the protected
words reached after two steps. Both lists have length `2 ^ m` and are
duplicate-free. Applying the actual two-step map to the first list gives
the second list in the same order. The cardinality proof uses the existing
Boolean-list enumeration, injectivity of the completed protected word,
and determinism of the two incoming transitions.

## Exact ordinary-integer meaning

`IntegerRealizes n w` means that `n` has a canonical decimal expansion
of width `w.length`, with digits `d i`, such that

```text
w[i] = d i + d (w.length - 1 - i)
```

for every in-range column. Canonicality includes digits at most nine,
a positive leading digit, and the exact positional value of `n`.
Existence is obtained from the original realizability theorem with the
even-width hypothesis explicitly discharged.

The ordinary dynamics are `Lychrel196.step n = n + reverse10 n` and
`orbit n 0 = n`. For every `IntegerRealizes n (historyWord0 xs k)`,
the contribution proves

```lean
0 < n ∧
  (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
  orbit n 4 = digitValue (target (xs.length + 6) k)
```

Here `digitValue w` is the positional coefficient value
`sum (w[i] * 10^i)` over the list. It accepts the coefficients ten,
fourteen, and eighteen; the existing normalization theorem supplies
their exact ordinary decimal value after carrying.

The time indices follow the arithmetic interface. Time one realizes
`historyWord1`; time two realizes `historyWord2`; time three is the
ordinary value of the normalized protected word. Those time-three
integers share the common target as their mirrored digit-sum word, so
their next step has the common coefficient value stated at time four.

The safety argument uses the odd outer sums three and seven at times
zero and one. The eighteen column in `historyWord1` excludes a palindrome
at time two using the existing safe-run theorem. The prior protected
finite-horizon theorem applies from time three through time `k + 3`.
All original realizations are covered by these interfaces.

## Proof modules and reused results

| New module | Responsibility |
| --- | --- |
| [HistoryInterfaces](HistoryInterfaces.lean) | Identify the retained carry in Agent #9's `scan` with `Agent8.terminalCarry`; apply the original accepting-path theorem to full words; prove canonicality of even mirrored words. |
| [TwoLayerCertificate](TwoLayerCertificate.lean) | Check the two local inverse layers on sixteen joint states, the initial transition, six-bit state correction, and the eighteen reservoir transition. |
| [IntegerInterfaces](IntegerInterfaces.lean) | Relate positional values to existing normalization, transport ordinary realizations through `stepWord`, discharge even-center realizability, and expose the required nonpalindrome criteria. |
| [ActualHistories](ActualHistories.lean) | Build arbitrary-word histories and prove their canonicality, widths, heads, two exact incoming transitions, and terminal carries. |
| [HistoryFamily](HistoryFamily.lean) | Prove injectivity, both exact coefficient-word counts, duplicate-freeness, and the enumerated two-step image. |
| [HistorySafety](HistorySafety.lean) | Compose the ordinary-integer safe prefix, positive existence, and common time-four value. |
| [TwoHistoryTheorem](TwoHistoryTheorem.lean) | Expose the central reservoirs, complete word chain, and final family theorem. |

The six modules in the earlier
[finite-horizon overflow contribution](../finite-horizon-overflow-20261016/)
are reused unchanged. The four files in
[dependencies/agent9/](dependencies/agent9/) are unchanged source copies
from Agent #9's commit `7be455c03d777e5e0ca1d44bea4d1330e3f764c7`;
[SOURCE_PINS.json](dependencies/agent9/SOURCE_PINS.json) records their
original paths, blobs, and hashes. Agent #9's original path-soundness
proof supplies the inverse-word semantics.

The original `TemplateStep` and `Compat` modules supply normalization
value preservation and canonical normalized digits. The original
`PeriodObstructions`, `ActualWordBridge`, `LychrelDigitSums`, and
`DecimalSafeRuns` modules supply the actual coefficient dynamics,
decimal arithmetic, and persistence of the eighteen reservoir.

## Reproduction and audit

The portable [verification package](verification/README.md) fixes all
23 source files by SHA-256 and compiles them in topological order under
Lean 4.19.0, release commit `6caaee842e94`, with `--trust=0`.

```bash
python3 proofs/contributions/agent-3/two-history-20261016/verification/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo /absolute/path/to/p196-algorithm \
  --build-dir /absolute/path/to/a-new-clean-build
```

The retained clean build passed all 23 modules. Its compiled inventory
contains **179 explicit declarations**, including three private helpers,
and **304 logical declarations** in total. Each logical declaration
received a `#print axioms` audit. The axiom union is exactly `propext`,
`Classical.choice`, and `Quot.sound`. The
[independent runtime review](review/two-history/REVIEW.md) reached the
same source and audit counts.

The build directory must be new or empty. The driver preserves earlier
output, checks source hashes before and after compilation, and isolates
the newly compiled modules from existing contribution object files.
It inventories all declarations owned by the seven new modules and six
inherited contribution modules, including the private certificate table
and generated logical helpers.

Development sources, failed attempts, complete compiler logs, audit
output, and execution metadata are retained in the contribution's
`development/` and `verification/` directories. Executable compiler
implementation stages are recorded separately using Lean's own safety
flags; every explicit source declaration must be safe and nonpartial.

The contribution claim is
`142563ce83e36afe5ddaccb0e93ed821fd40eba0` on `p196/coordination`.
Ordinary coordination is recorded on
[GitHub issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61).
