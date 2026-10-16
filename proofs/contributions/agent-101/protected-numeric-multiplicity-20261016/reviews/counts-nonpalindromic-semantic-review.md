# Independent review of the exact protected nonpalindromic count

## Verdict and source identity

**PASS.** The new module removes precisely the existing initial palindrome from the complete protected seed family. Its numerical membership is complete for the specified family, its length is exactly `5 * 11 ^ m - 1`, and it explicitly proves nonemptiness for every natural `m` and `k`.

Reviewed source: `proofs/Agent101ProtectedNonpalindromic.lean`.

```text
SHA-256 93aa73770e3a57e89ad8b07eadc580ecd5c13494da8578ecbfcc41078c954df6
```

The reviewer is the research-inventory worker and did not author this target or its new generic filtering dependency. The reviewer previously authored the frozen `Agent101SplitEnumeration` and `Agent101PalindromeFibers` dependencies. This report independently reviews the new protected filtering target and its use of the generic list helpers; it does not present the reviewer's own earlier modules as independently reviewed by their author.

No mathematical source was modified, and no Git writes were performed. Both newly rebuilt source hashes remained unchanged.

## Exact filtering and membership

`protectedNonpalSeeds m k` filters `protectedSeeds m k` using the Boolean negation of the decision procedure for the original `Lychrel196.Palindrome`. `mem_protectedNonpalSeeds` proves the corresponding full biconditional:

```lean
n ∈ protectedNonpalSeeds m k ↔
  n ∈ protectedSeeds m k ∧ ¬ Lychrel196.Palindrome n
```

The final numerical membership theorem retains every member satisfying the exact ordinary-integer conditions:

```lean
n ∈ protectedNonpalSeeds m k ↔
  decimalWidth n (2 * (m + k + 1)) ∧
  ¬ Lychrel196.Palindrome n ∧
  ∃ xs : List Bool, xs.length = m ∧
    Lychrel196.step n = natValue (inputWord xs k)
```

It is obtained by composing the complete protected-family membership equivalence with the exact filter membership equivalence and reassociating the conjunctions. There is no restriction to a chosen numerical representative of a profile. Positivity and the common input width are inherited for every filtered member. Filtering also preserves the previously proved absence of repeated integers.

## Why natural subtraction is exact

The source first proves an equality of lists, not just an upper bound on the number of removed elements:

```lean
(protectedSeeds m k).filter
    (fun n => decide (Lychrel196.Palindrome n)) = [palindromeSeed m k]
```

The helper `list_eq_singleton_of_nodup_mem_iff` requires both no duplicates and the full membership equivalence `x ∈ xs ↔ x = a`. Its empty-list case is explicitly impossible because the reverse implication supplies membership of `a`. Thus the use of `protectedSeeds_palindrome_iff` supplies actual existence as well as uniqueness; an empty palindrome sublist cannot satisfy the argument.

`length_filter_partition` partitions any finite list between a Boolean predicate and its complement. Applied here, then rewritten using the singleton equality and the exact unfiltered count, it gives:

```lean
1 + (protectedNonpalSeeds m k).length = 5 * 11 ^ m
```

The stated subtraction formula follows from this equality. Natural-number truncation does not hide an impossible count, because the removed singleton has already been established and the pre-subtraction partition equality holds.

## Nonemptiness and zero boundaries

`protectedNonpalSeeds_nonempty` is an unconditional theorem for all natural `m` and `k`. It uses `0 < 11 ^ m` and the exact length formula to rule out an empty filtered list. In particular, `5 * 11 ^ m` is at least 5 and the remaining count is at least 4; no empty-family premise can make a later universal safety statement vacuous.

- At `m = 0`, the count is 4, independently of `k`.
- At `k = 0`, the protective portion is empty but all membership, length, and nonemptiness theorems still apply.
- At `m = k = 0`, the unfiltered family is the five width-two integers from the preceding review. Removing its unique palindrome 77 leaves 59, 68, 86, and 95.

These boundaries are within the formal universal quantifiers. The last description is a direct reading of the previously reviewed explicit definitions, not an additional test claim.

The bundled endpoint `protectedNonpalSeeds_exact` includes the exact length, no duplicates, an explicit existential nonempty conclusion, and positivity, width, and initial nonpalindromicity of every member. It does not itself claim any later-iterate safety. Such results retain the separate hypotheses of the protected finite-horizon construction, including positive `k` when required.

## Fresh build and public axiom audit

`counts-nonpalindromic-rebuild.py` rechecked the source-snapshot and generated `.olean` hashes of the preceding 12-module fresh closure, then compiled these two additional frozen sources into the same isolated directory:

| Module | Source SHA-256 | Lean exit code |
|---|---|---:|
| `Agent101NonpalindromicFibers` | `22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5` | 0 |
| `Agent101ProtectedNonpalindromic` | `93aa73770e3a57e89ad8b07eadc580ecd5c13494da8578ecbfcc41078c954df6` | 0 |

Both compilations used Lean 4.19.0, `-j1`, and `--trust=0`, with only the freshly source-built project closure on `LEAN_PATH`. The generic filtering module compiled in approximately 1.63 seconds and the target in approximately 0.86 seconds.

`counts-nonpalindromic-Audit.lean` explicitly checks all 10 public exports, comprising one definition and nine theorems. The audit returned 0. The definition is axiom-free; the theorem axiom union is `propext`, `Classical.choice`, and `Quot.sound`. The target source contains no `sorry`, `admit`, `axiom`, or `native_decide` token.

Commands, actual return codes, exact source snapshots, source and artifact hashes, prior closure evidence, and the authorship disclosure are retained in `counts-nonpalindromic-verification.json`, `counts-nonpalindromic-build-results.json`, the two source-build logs, and `counts-nonpalindromic-axioms.log`.

No missing existence premise, hidden empty-family case, or mismatch between the filter and the ordinary-number predicate was found.
