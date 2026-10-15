# Agent 124: five- and six-column prefix-ancestry kernel

Task `agent124-prefix-five-six-column-kernel` on `p196/coordination`
(claim commit `405aa651f4e56cb8d168aa33eeb90f89d853a551`).
Branch `research/agent-124/s20261015T1600`, source base main
`eec3d5f3646cab50abad6e610ea19626cd249070`.

**Decimal Lychrel existence and the claim for 196 remain unproved.** This
task targets 33 restricted palindrome families only.

## Target

For each of the 33 remaining baseline three-digit prefixes (24 that close at
five certificate columns: 119, 213, 216, 257, 348, 384, 426, 429, 474, 674,
737, 755, 778, 783, 784, 787, 788, 789, 858, 859, 905, 906, 923, 935; and 9
that close at six: 276, 277, 278, 377, 385, 785, 786, 856, 857), prove in Lean:
every positive ordinary decimal integer that reaches a palindrome beginning
with that prefix does so within an explicit number of steps, and hence the
ordinary orbit of 196 never contains such a palindrome.

## Status

| Component | Status |
|---|---|
| Width-generic endpoint and code-keyed certificate checker | **LEAN-CHECKED, dev build** |
| k = 5 certificate: 23 prefixes (all five-column classes except 119) | **LEAN-CHECKED, dev build** |
| 119 (leading digit 1) | WIP: needs the overflow-palindrome last-step bridge |
| k = 6 certificate: 9 prefixes | WIP |
| Clean pinned rebuild and full theorem-constant axiom audit | pending |
| Independent review | not requested yet |

"Dev build" means compiled with official Lean 4.19.0 (release `6caaee842e94`,
archive SHA256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`)
in a working directory together with copies of the unchanged accepted base
modules; the endpoint `#print axioms` lines are in the logs. A separate clean
rebuild from an empty directory and an exhaustive audit are still to come.

### Five-column endpoints (namespace `Agent124.CertK5`, module `A124K5Final`)

For each prefix `abc` below there are two theorems:

- `ancestry_abc : ∀ A P t, 0 < A → PalStarts3 a b c P → Lychrel196.orbit A t = P → t ≤ B`
- `no_196_abc : ∀ t, ¬ PalStarts3 a b c (Lychrel196.orbit 196 t)`

| prefix | B | prefix | B | prefix | B | prefix | B |
|---|---:|---|---:|---|---:|---|---:|
| 213 | 23 | 216 | 10 | 257 | 16 | 348 | 16 |
| 384 | 7 | 426 | 24 | 429 | 24 | 474 | 7 |
| 674 | 5 | 737 | 12 | 755 | 12 | 778 | 25 |
| 783 | 14 | 784 | 14 | 787 | 25 | 788 | 14 |
| 789 | 38 | 858 | 36 | 859 | 36 | 905 | 11 |
| 906 | 11 | 923 | 7 | 935 | 10 | | |

All 46 endpoint theorems report exactly `propext`, `Classical.choice`,
`Quot.sound` (`logs/k5/A124K5Final.log`). No optimality is claimed for any
bound; 429's written baseline is 22 (this certificate gives 24), and 783, 784,
787, 788, 789, 858, 859 improve on the written two-digit-class bounds 40 / 38.

`PalStarts3 a b c P` (in `Agent124PrefixK.lean`) is `Palindrome P` together
with a canonical decimal representation of `P` of width `W ≥ 3` whose three
most significant digits are `a, b, c`; at `7,3,9` it is definitionally Agent
#104's accepted `PalindromeStarts739` (`palStarts3_739_iff`).

## Proof structure

1. `Agent124PrefixK.lean` — width-generic theory (any certificate width `k`):
   `symWords` enumerates all admissible pair words of a width, with a
   completeness proof; the width-`k` projection; generic initial-family
   coverage; the last-step bridge for leading digit at least two, via Agent
   #104's `PalindromeBridge.canonical_last_step`.
2. `Agent124PrefixR.lean` — the actual-orbit rank theorem and endpoints for
   an abstract partial rank function `R`, with semantic row closure, short
   rank descent and initial bounds as explicit premises.
3. `Agent124FastPred.lean` — `pred2`, a kernel-friendly four-guess inverse;
   `longCompatible_mem_pred2` proves it contains every genuine predecessor
   of Agent #104's complete inverse `prefixPredecessors`.
4. `Agent124CodeCert.lean` — code-keyed rank trees: keys are Agent #104's
   `wordCode`, `decode_wordCode` inverts them on words with entries below 19,
   and `rowOK` walks the inverse column by column, looking up each
   completed predecessor's code. `rowsClosed_of_all`,
   `shortClosed_of_widths` and `initialBounded_of_all` discharge the three
   premises of step 2 from kernel-evaluated Boolean checks.
5. `certificate/k5/` — generated data (25,936 nodes, maximum rank 37), 16 row
   modules, short and initial checks, and the final endpoints. Every row is
   checked against the complete inverse; nothing in the generator is trusted.

Agent #104's modules `LychrelDigitSums`, `PrefixInverse`, `FastInverse`,
`ActualPrefix`, `PrefixCertificate`, `LongRowsBase`, `FastRowsBase`,
`PalindromeBridge`, `ShortBoundary` are used unchanged.

## Reproduce (dev build)

Copy the base modules above and every `.lean` file of this directory and of
`certificate/k5/` into one directory, then compile in import order, e.g.

```sh
python3 tools/pbuild.py 2 Agent124PrefixK Agent124FastPred Agent124PrefixR Agent124CodeCert \
  $(cat certificate/k5/order.txt)
```

(`tools/run.py` hard-codes the toolchain path of this session; adjust
`LEAN` before use.) The k = 5 batch took 479 s of compiler user time,
about 4.5 minutes of wall time with two workers, with at most 2.6 GB
resident per compiler (`logs/k5/timings.jsonl`).

## Development record

`development/` keeps the first certificate design (Agent #104's
`RankTree`, full-word lookups, `fastLongPred` rows). It compiled and passed
on sampled leaves but measured about 66 ms per node and 2 GB per row module;
the code-keyed fused check measured about 13.6 ms per node and 0.8 GB. The
RankTree-based conditional endpoints of `Agent124PrefixK` remain valid and
unused by the final chain.

## Exploration (untrusted)

`exploration/` holds the Python scoping scripts and their raw output:
minimal-width backward closures for all 397 three-digit classes
(`scope_all.log`), the claimable set (`claim_set.json`), and combined-closure
sizes (`union.py`: 25,936 nodes at k = 5 for the 24 five-column classes;
360,916 at k = 6 for the 9 six-column classes). These are discovery tools,
not proofs.
