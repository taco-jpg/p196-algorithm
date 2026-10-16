# Agent #111: growing power-of-ten suffix modulus

Task: `agent111-growing-tenpower-suffix-20261016`. Coordination issue #61.

## Precise mathematical proposition

At decimal width L, a subset of positive integers is allowed to depend on the exact width and on the last k(L) digits, where k(L)>=1 and 2*k(L)+4<=L for all sufficiently large L. If that subset is nonempty and forward-closed under actual ordinary decimal reverse-and-add, then it necessarily contains an ordinary positive palindrome.

The concrete uniform schedule k(L)=floor((L-4)/2) for L>=6 makes the modulus 10^k(L), which is unbounded and exponentially large as a function of the width L; it is **not** included in Agent111 PR #102's bounded-modulus theorem. This is a restricted invariant-class obstruction, not a result that any starting orbit visits a palindrome, and not an answer to P196.

The proof reuses the existing source theorem `ExactLengthResidues.saturation_of_split` (original, attributed Agent111/merged PR #40) at (M,u,q,r)=(10^k,10^k,1,1). The resulting exact-width saturation threshold is 2*k+4. An original theorem `AstraModular.large_width_compatible_state` produces a late actual orbit state with width at least any B, divisible by 11, and not divisible by 10. It therefore satisfies the exact compatible-residue premises for its own width-dependent modulus. Membership transfers via the assumed width/suffix congruence condition.

For B=6 the source bridge picks an actual orbit time in the range 30–31, but does **not** show that the orbit state equals the constructed palindrome.

## Validation

**LEAN-CHECKED, awaiting independent semantic review.** Official Lean 4.19.0 [run #38971847141](https://github.com/taco-jpg/p196-algorithm/actions/runs/38971847141) returned PASS: **12 freshly rebuilt source modules, 1,006 theorem constants audited**, transitive theorem axioms exclusively `propext`, `Classical.choice`, and `Quot.sound`. The archived original exact-length residue source and original decimal semantics were used without source changes. Source SHA256: `910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a`. The [CI manifest](verification/CI.json), [new-module compiler axiom log](verification/GrowingSuffix.log), and [full Actions artifact #12076648408](https://github.com/taco-jpg/p196-algorithm/actions/runs/38971847141/artifacts/12076648408) preserve reproducible evidence. The initial failed attempt and compiler diagnosis (`dvd_refl` unresolved, provisional `sorryAx`) are retained at [attempt-001.log](verification/attempt-001.log); that failure was fixed by commit `2dd0d9e` and a complete new build succeeded. No finite experiment was treated as proof. Independent semantic review and default-branch integration are distinct unsatisfied gates.

Original reviewed proof source: commit `c3192d5bf2962298bcb2bb209a0947f657e8a7e5`. Original archive tree at `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

## Stronger exact-half-width constructive result

**LEAN-CHECKED on official Lean 4.19.0:** [`SharpSuffix.lean`](SharpSuffix.lean) removes the four-digit pad required by the general arbitrary-modulus construction. The checked theorem `Agent111.GrowingSuffix.palindrome_with_given_suffix` constructs an ordinary positive exactly `L`-digit palindrome sharing `n % 10^k` for **any** `0 < k` with `2*k <= L` and `10 ∤ n`. It instantiates the original `two_pool_realization` with two empty inner pools, and retains the original canonical decimal semantics. This is true for arbitrary input `n` meeting those hypotheses, not only orbit values.

The resulting `variable_half_suffix_closed_set_contains_palindrome` excludes safe positive nonempty forward-closed sets whose eventual width-`L` membership depends only on the final `k(L)` decimal digits, when `2*k(L) <= L` and `k(L)>0`. The explicit `exact_half_suffix_closed_set_contains_palindrome` takes `k(L)=floor(L/2)` for every `L>=6`. This is stronger than the above original theorem's `(L-4)/2` bound. It still does not establish any palindrome hit in the orbit of 196 (or any other actual orbit).

Official [GitHub Actions run #38972428087](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972428087) **PASS**: clean 13-module closure, 1,012 theorem constants audited, axioms only `propext`, `Classical.choice`, `Quot.sound`. `GrowingSuffix.lean` SHA256 `910ddd984a85d235fc2829b87904c4f9947a306c0f1a652bf252f5128a5a040a`, `SharpSuffix.lean` SHA256 `8f26f160d90b363a4e89728bc2470bde12bac5e751c89e97dacbc9e59bfa1c1c`. The durable [verification manifest](verification/SharpCI.json) and [axiom log](verification/SharpSuffix.log) link the full [artifact](https://github.com/taco-jpg/p196-algorithm/actions/runs/38972428087/artifacts/12077712695) (SHA256 `50bb5472ecb9124e36e8370c5643075130c05b520a30c75e18f13449b39a3966`). The original compiler-generated implementation stubs are documented separately and do not enter these theorem dependencies. Independent interpretation review and accepted-build integration remain pending; the proof is source-pinned to the preserved archived original module layout, which must be reconciled with current main layout by the integration owner.
