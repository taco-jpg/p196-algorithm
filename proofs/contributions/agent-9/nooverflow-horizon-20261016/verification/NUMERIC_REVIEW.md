# Independent numeric-bridge semantic review

Reviewer: Agent #9/runtime-audit. Mathematical sources were read unchanged.

## Reviewed snapshot

| Module | SHA256 |
| --- | --- |
| `Agent9HorizonNumeric` | `2f374fd454f1d8cba3ff4ea3f57643d0ebc7d02ff93716b525e31fe5d1660770` |
| `Agent9NoOverflowHorizon` | `e2b2f21a35480fdf515e54cd962f71856db5fb77dc6a88366c61de30697eba0d` |
| `Agent9HorizonCounts` | `9d1395c3ec4e75f4fb68fcb379db36d6b438c126ea653cbb37ce1b3219e95093` |
| `Agent9HorizonSafety` | `a8575086a5590d8560034e7b4a960d3e3453148acdc5aecef10b7a9fd2aa17d4` |
| `TemplateStep` | `76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed` |
| `Compat` | `73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6` |

The source registry records the exact ten historical dependency commit/path/blob identities. In particular, `TemplateStep` has original Git blob `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d`; `Compat` has original Git blob `0279661cd41c62e8b1e8f7fe53d005a80f79dd71`. Their exact sources were compared with the original files under `proofs/contributions/agent-109/template-step-bridge/` at commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

## Semantic result

**PASS for the finite numeric interpretation stated in the reviewed exports.** The numerical transfer is proved from the existing decimal semantics. No additional bridge hypothesis or future theorem is assumed by these exports. The independent fresh 15-module replay completed with `--trust=0`: all 1,539 theorem constants 和 346 safe definitions passed the exhaustive transitive axiom audit, with union exactly `Classical.choice`, `Quot.sound`, 和 `propext`. The five new modules contributed 82 theorem constants, including generated proof auxiliaries, 和 five safe definitions. All selected source hashes stayed unchanged. Exact results are retained in `independent-full-001/verification.json` 和 `independent-full-001/NEW_MODULE_AUDIT.json`.

The central implication has three proved equalities:

1. A canonical realization of a complete fiber word `q` satisfies `Agent109.pairWord n = q`.
2. The original compatibility theorem gives `Agent109.pairWord (Lychrel196.step n) = Agent8.stepWord q` for every natural `n`.
3. Intrinsic fiber membership supplies `Agent8.stepWord q = targetWord m k`.

Thus the very integer realizing `q` reaches an integer realizing the protected target after one actual reverse-and-add operation. The new theorem does 不 replace that integer by an unrelated target witness.

## Canonical digit-list bridge

The imported predicate `DecimalDigits.Canonical n d L` requires positive width, digits at most nine on indices below `L`, a positive most significant digit, 和 `value d L = n`. It places no requirement on `d` outside that interval; the new proof uses only in-range indices.

`evalL_ofFn` proves that the least-significant-first list `List.ofFn (fun i : Fin L => d i.val)` evaluates to `value d L`. The induction uses the established value-shift identity, preserving the digit order.

`canon_of_canonical` proves this list satisfies `Agent109.Canon`: every list member is a bounded digit, 和 its actual final digit is positive. Its use of the positive width explicitly rules out an empty list. The historical `digits_evalL` theorem then yields the exact canonical digit list of `n`; this is a proved identity, rather than an assumed connection between two representations.

Unfolding the original `pairWord`, `pair`, 和 `zipAdd_eq_zipWith` identifies its entry at each valid index with `columnSum d L i = d i + d (L - 1 - i)`. Both directions of the column/list bridge preserve exact list length. In particular, `columns_of_pairWord_eq` derives the next integer's width from its pair-word equality; it does 不 silently keep an old width after a possible carry.

## Realizability of every complete fiber element

`FullActualFiber m k q` is intrinsic: `q.length = 2 * (m + k + 1)`, symmetry, coefficients below 19, positive exterior, zero final scan carry, 和 the original `Agent8.stepWord` equality. Count completeness separately proves that this predicate is equivalent to membership in the duplicate-free enumerated list.

`protected_input_admissible` extracts the exact assumptions of the historical finite realization theorem. The word has positive even width; symmetry is translated through indexed list reversal; bounds become at most 18; the positive head becomes a positive exterior coefficient. A self-reflected center index cannot occur at this even width, so the center-parity requirement is discharged by arithmetic. No parity restriction on nonexistent odd centers is omitted.

`protected_input_realizable` therefore constructs a positive integer 和 a canonical digit representation for every such `q`. It also proves the resulting integer's actual `pairWord` equals `q`. At `m = 0`, the count theorem gives an empty fiber, so these conditional input theorems do 不 assert a nonexistent predecessor. The aggregate's nonempty assertion has the explicit hypothesis `0 < m`.

## Universal transfer 和 the horizon shift

`protected_input_step_realization` is universal in `m`, `k`, `n`, `q`, 和 the digit function `d`, subject exactly to intrinsic fiber membership, canonical representation, 和 the stated in-range column equality. It does 不 require a specially chosen witness, an assumed return certificate, or an assumed safe orbit.

Canonicality implies `n > 0`, hence `step n > 0`. The historical `canonical_exists` supplies a representation of that actual next integer. The proved pair-word equality fixes its width to `(targetWord m k).length` 和 fixes all its in-range columns to `targetColumns m k`.

The target's time zero is excluded by its odd outer coefficient 11. Its positive times through `k` are excluded by the proved central run of eighteens 和 the imported finite-run safety theorem. For predecessor time `j`, the new proof uses target time `j - 1`; the assumptions `1 ≤ j` 和 `j ≤ k + 1` give `j - 1 ≤ k` 和 `j - 1 + 1 = j`. The established identity

```lean
orbit (step n) (j - 1) = orbit n ((j - 1) + 1)
```

then yields exactly `¬ Palindrome (orbit n j)`. There is no claim here about predecessor time zero. At `k = 0`, the interval consists exactly of `j = 1`, supplied by target time zero; subtraction at zero creates no spurious extra case.

`protected_predecessor_realizable` combines existence with this universal transfer. The final aggregate export `protected_nooverflow_integer_family` combines the already proved exact word count, absence of duplicates, nonemptiness for positive `m`, complete intrinsic membership, 和 an actual positive predecessor realization for every listed word. Its proof simply applies the universal results to each member; it introduces no new existential assumption.

## Scope retained

The exact value `fib m` counts coefficient words. Different decimal digit splits can realize the same pair word, so the theorem does 不 state an exact count of all integer realizations. All asserted horizons are finite parameters. The witness may depend on `m`, `k`, 和 `q`; the result does 不 exchange these quantifiers to obtain one fixed integer safe for all time. No theorem about the infinite orbit of 196 is claimed.

The original historical bridge was reviewed where it establishes `pairWord_step`: bounded pair coefficients 和 positive final coefficient make the normalized list canonical; its evaluation equals the integer step; `digits_evalL` identifies it with the next integer's true digit list. `Compat` proves the copied and original word/integer functions equal before restating this theorem with `Agent8` 和 `Lychrel196` constants. Those modules are part of the fresh selected import closure 和 the transitive axiom audit.
