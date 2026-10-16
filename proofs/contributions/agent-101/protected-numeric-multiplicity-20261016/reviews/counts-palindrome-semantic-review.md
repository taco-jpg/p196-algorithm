# Independent review of the protected family's unique initial palindrome

## Verdict, identity, and independence

**PASS.** `Agent101ProtectedPalindrome.lean` correctly specializes the complete generic palindrome-fiber theorem to the entire protected seed union. It proves that exactly one seed is initially palindromic, identifies that seed explicitly, and includes all natural `m` and `k`, including zero.

Reviewed source: `proofs/Agent101ProtectedPalindrome.lean`.

```text
SHA-256 1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295
```

The reviewer is the Agent #101 research-inventory worker. I did not author either `Agent101ProtectedMultiplicity.lean` or `Agent101ProtectedPalindrome.lean`; both were authored by the numeric-bridge worker. **I did author the frozen `Agent101SplitEnumeration.lean` and `Agent101PalindromeFibers.lean` dependencies.** This review is independent for the two new protected-family modules. Rebuilding my own dependencies is recorded as verification, not as independent semantic review of those dependencies.

This report extends `counts-semantic-review.md`. No mathematical source was modified, and no Git writes were performed.

## The precise public result

The explicit candidate is defined from its least-significant-first digit half:

```lean
palindromeHalf m k = [7] ++ List.replicate m 7 ++ List.replicate k 9
palindromeDigits m k = palindromeHalf m k ++ (palindromeHalf m k).reverse
palindromeSeed m k = natValue (palindromeDigits m k)
```

The principal theorem is the full biconditional:

```lean
protectedSeeds_palindrome_iff (m k n : Nat) :
  (n ∈ protectedSeeds m k ∧ Lychrel196.Palindrome n) ↔
    n = palindromeSeed m k
```

This simultaneously supplies existence and uniqueness. The original `Lychrel196.Palindrome` is used throughout, so the result is about ordinary decimal reversal. `palindromeSeed_member_palindrome` separately proves that the candidate is an actual member of the complete counted union and is an actual palindrome. The member-only, palindrome-only, and uniqueness corollaries preserve that same meaning.

## Why there is exactly one eligible profile

The outer coefficient 14 and all protective coefficients 18 are even. A false index entry selects coefficient 5, which is odd; a true entry selects 14, which is even. `inputWord_even_iff` proves both directions of:

```lean
(∀ s ∈ inputWord xs k, s % 2 = 0) ↔
  xs = List.replicate xs.length true
```

In the forward proof, each actual Boolean entry contributes its selected coefficient to the complete input word. Evenness therefore excludes the false case for every entry. `all_true_eq_replicate` then identifies the entire Boolean list, including the empty list. The reverse direction checks all positions of the complete mirrored word, including its protective portion.

Combined with the exact index-length condition from `mem_protectedSeeds`, this leaves precisely the index `List.replicate m true`. No unexamined profile remains in the union: the previous counting review established that its indices range over every Boolean list of length `m`.

## Existence and the explicit value

Evenness alone is not treated as a realization proof. The source first establishes:

```lean
profileCount (inputHalf (List.replicate m true) k) none = 5 * 5 ^ m
```

and proves that this count is strictly positive for all `m` and `k`. It then applies the generic constructive endpoint `half_coefficientWord_mem_numericFiber` with both the positive-count premise and the full evenness premise. This supplies a canonical ordinary-integer realization and actual numerical palindromicity.

`half_inputWord_all_true` identifies the halved complete word exactly with `palindromeDigits m k`: 14 becomes 7, 18 becomes 9, and the full reversal is preserved under the map. The candidate is then inserted into the complete protected union using the all-true index of the correct length.

The uniqueness direction starts from an arbitrary palindromic member of the union, obtains its profile witness, applies the generic full-fiber characterization, proves that the witness must be all true, and rewrites the generic explicit half-profile value to `palindromeSeed`. It does not assume that the original member was the selected candidate, and it does not rely merely on a uniqueness theorem without an existence witness.

## Boundary and scope checks

- At `m = 0`, the empty index is also the all-true index, so the eligible profile still exists and has positive count 5.
- At `k = 0`, the protective 9 segment is empty, but the initial 7 remains in each half. The candidate is still nonempty, canonical, and positive through its established protected-seed membership.
- At `m = k = 0`, the candidate is 77, which belongs to the five width-two seeds identified in the counting review.
- At `m = 1`, `k = 0`, the candidate is 7777; at `m = 0`, `k = 1`, it is 7997. These are direct readings of the explicit digit definition, not additional test claims.

The result concerns initial palindromicity. It neither changes nor independently proves the protected family's transition or finite-horizon safety properties. Those later-iterate properties retain their separate hypotheses. In particular, the present result is valid at `k = 0` without extending a positive-`k` safety theorem to that boundary.

Together with the preceding distinctness and count theorem, this module provides the exact existing member that a subsequent initial-palindrome filter must remove. The filtering and subtraction proof belongs to the separate parent module.

## Fresh rebuild and all-export audit

`counts-palindrome-rebuild.py` first rechecked every source-snapshot and `.olean` hash from the complete 10-module fresh build recorded in `counts-verification.json`. It then copied and rebuilt the two additional frozen sources into that same isolated closure:

| Additional module | Source SHA-256 | Actual Lean exit code |
|---|---|---:|
| `Agent101PalindromeFibers` | `27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633` | 0 |
| `Agent101ProtectedPalindrome` | `1a662e360011f41d156efd9b5d62cc2acb18078486bcea6cab52b03aec18d295` | 0 |

Both were compiled with Lean 4.19.0, `-j1`, and `--trust=0`. The project import path contained only the isolated `counts-build` directory. The protected-family target compiled in approximately 0.80 seconds. Its source hash remained unchanged after verification.

`counts-palindrome-Audit.lean` checks all 15 public exports, comprising three definitions and 12 theorems. The audit returned 0. All three definitions are axiom-free; the theorem axiom union is `propext`, `Classical.choice`, and `Quot.sound`. The target source contains no `sorry`, `admit`, `axiom`, or `native_decide` token.

`counts-palindrome-verification.json` records the prior fresh-closure evidence hash, the rechecked dependencies, both exact source snapshots, actual commands and return codes, generated artifact hashes, all audited exports, and the authorship disclosure. Separate source-build logs and `counts-palindrome-axioms.log` preserve the actual Lean output.

No semantic defect, missing existence premise, or omitted zero boundary was found in this specialization.
