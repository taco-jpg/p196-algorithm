# Agent 118 — T3.p12-regular-language

## Status 和 scope

**PAPER PROOF + COMPUTED:** the known decimal p12 driver has no center cycle
at ANY positive repetition count, ANY finite center width, or ANY natural trim
schedule. Simultaneous time rotations, including the three documented phase
variants, are covered. The exact regular languages satisfy `L6=L7`; all14
transient/eventual parity-tail languages are empty.

This is a scoped unbounded-driver exclusion, 不 a new Lean theorem. External
campaign review remains appropriate before marking this family closed.

The target is only the known decimal p12 driver
`e=101010010101`, `g=100010001000`, repeated an arbitrary positive number k
of times, with arbitrary finite center widths 和 natural trims. It is 不 a
claim about every decimal driver or the whole one-band route.

The existing length accounting gives `2*sum(v)=3k`; odd k are impossible.
For k=2n, n>=1, the credited arbitrary-trim transport theorem permits the
schedule `v=(00001000)^(3n)` without changing driver existence at all widths.
The exact regular-language computation discharges every n simultaneously.

[Claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433118684).
Dependency: [PR369](https://github.com/taco-jpg/p196-algorithm/pull/369),
commit `19e13c356d9a917cf8bce074be71607f6b7cdd87`, which itself stacks on
[PR340](https://github.com/taco-jpg/p196-algorithm/pull/340).
No shared source, README, RESULTS, or Lean file is changed.

## Attribution 和 prior scope

The original neutral-band center solver supplies the exact local carry/digit
relations 和 central termination cases. Agent7 supplied neutral padding;
Agent107's PR336 supplied arbitrary equal-total trim transport; Agent110's
PR338/370 supplied width-preserving profiles 和 the independently checked
all-repetition width14 exclusion. These are separate ingredients.
That width14 bound constrains every phase, whereas initial width m=14 in the
present schedule can reach phase width15; its terminal case needs its own check.

PR369 supplies the exact correlated segment-image construction at fixed
period48. Agent111 independently implements a delayed-output image, with the
new P33 result credited to that agent. Agent101's PR357 cumulative whole-state
reachability 和 Agent117's common-padding reduction remain separate.
Existing `Agent107FoldedTransducer` formalizes a different exact one-step
folded transducer, without a closed-language or infinite-orbit conclusion.
The present proposal makes no broad historical novelty claim for transducers,
regular languages, or finite-state model checking.

## 1. Three uniform local alphabets

Write P=24n, n>=1. Trims occur at temporal positions `4+8r`. Segment r contains
the eight ordered times `8r+5,...,8r+12`, interpreted modulo P. Because e has
period12, g period4, 和 v period8, the local arithmetic data repeat after
three segments. Call their types A,B,C.

A semantic local symbol is its type together with the eight stored triples
`(left carry, right carry, retained digit)` 和 the pending neighbor coefficient z.
The numerical state IDs used by a single shared three-type cache are merely
injective names for these finite data. The type is part of the symbol.
Different temporal occurrences of A may carry DIFFERENT A-symbols; no
24-step repetition of the evolving state is assumed.

The initial language is exactly

`L0 = (sA sB sC)+`.

The positive closure excludes an empty temporal cycle. At a fixed length3n,
mapping each semantic type symbol back to its concrete occurrence gives a
bijection with the original complete global frontier tuples. Local transitions
commute with that bijection: they inspect only the eight ordered arithmetic
data, local configuration, pending z, 和 the specified layer signature.

## 2. Exact regular relational image

For an input symbol x of type s, the existing local relation lists pairs `(y,c)`.
As in PR369, an output symbol is `(type s, y, d)`, where d is the next segment's
chosen coefficient. The permitted coefficients include inactive sentinel -1.

Given an input finite automaton, construct a product automaton whose state
records its input state q, the currently required coefficient c, 和 the
starting coefficient a. Each input edge labelled x may select any local
choice `(y,c)` 和 emit `(s,y,d)`, updating the product state to `(q',d,a)`.
Initial product states use c=a. An accepting product state requires the
original input state to accept 和 c=a.

The original input path remains intact, so no coordinate independence is
introduced. Closure is required only when the WHOLE word terminates. In
particular, product states at intermediate ABC boundaries must retain their
outgoing transitions even if c differs from a; imposing closure at every
three-letter boundary would incorrectly remove subharmonic cycles.

For any fixed input word this is exactly the Cartesian local relation, by
induction on its letters. Union over the accepted input language therefore
gives exactly its relational image. Every output is the same length as its
input, so the correspondence holds simultaneously at every length3n.

The first generic image R0 uses the special spatial-boundary flag. Subsequent
generic images use one stationary relation R:

`L1=R0(L0)`, `L_(j+1)=R(L_j)` for j>=1.

Each L_j is regular because the explicitly constructed product automaton is
finite. This does 不 imply that repeated images stabilize, or that their
automata fit a given resource budget.

## 3. Exact fixed-point obligation

If a completed language-equivalence check proves `L_h=L_(h+1)` for h>=1,
stationarity gives `L_j=L_h` for every j>=h. This requires equality of whole
regular languages, including every positive temporal repetition count.
Equal finite-length counts, sampled words, structural hashes, or agreement
of the P24/P48 slices do 不 prove this obligation.

Determinization uses exact subsets of product states. Any state minimization
must preserve final-state membership 和 every labelled transition, including
the implicit rejecting sink. A separate two-way product comparison supplies
exact language equality; an incomplete comparison is UNDECIDED.

An alternative sufficient obligation would be an inductive regular superset
S with `L1 subset S`, `R(S) subset S`, 和 empty terminal images of S.
The two special L0 boundary-tail checks are still required for initial widths1,2.
No such invariant is assumed merely from the observed small-period results.

## 4. Uniform finite-width completion

The temporal length offsets are `(0,1,1,1,1,0,0,0)` repeated, independent of n.
In segment order they are `00001111`. Every phase width is m or m+1.
The number of generic layers is `q=ceil(m/2)-1`, followed by exactly two
terminal layers. For q>=1 the terminal signatures depend only on initial parity:

| Initial m | First terminal signature | Second terminal signature |
|---|---|---|
| Odd | `LODD^4 LEVEN^4` | `INZ^7 INP` |
| Even | `LEVEN^4 GEN^4` | `INZ^3 INP LODD^4` |

The three e/g types still affect the arithmetic inside these signatures.
For m=1,2, q=0: the first terminal layer must retain the special j=0 rule.
The implementation derives signatures through `setup_instance`, while this
table independently states their expected form.

If the regular fixed point occurs at h, checking both terminal parities on
L0,...,L_h covers every width and every n. There are `2*(h+1)` checks;
L0 uses the special boundary rule. For h=6, widths1..14 suffice uniformly in n.
The former fixed-period convenience threshold `mlo>2P` is unnecessary here,
because the uniform offset calculation proves positivity 和 tail translation
directly.

All resulting terminal languages are empty, so no center exists for any even k.
Length parity excludes odd k, 和 credited schedule transport covers arbitrary
natural trims. Closed centers are symmetric 和 have coefficients0..18 because
each is an incoming pair-sum followed by equal trimming. Empty 和 all-neutral
centers preserve the entering carry, so they cannot satisfy the required flip.

## 5. Reciprocal fixed-period cross-checks

Completed before the new regular-language computation:

```bash
python3 calculation/agent-118/cross_mdd.py --binary /tmp/p196-agent118-mdd/center_mdd
```

This independently corroborates Agent111's P33 decision using PR369's
required-current-coefficient image, distinct from that agent's delayed-output
image. Exact generic tuple counts:
`42875,657443,34755075,414911363,752450435,752450435`.
Result: all-width NONE, `jstar=5,period=1,mlo=67,classes=2,tails=12`,
10,488 DAG nodes,6,760,307 charged operations,0.224s,13,536KiB peak RSS.
Primary P33 credit remains Agent111; this is a cross-reproduction.

The same script tests Agent116's credited base20 fixture from PR356:
`e=10100101,g=10001000,v=00100000,m0=27`. It returns a complete positive,
compares all14 finite frontiers against the explicit original generator, 和
independently replays all8 center edges by positional integer arithmetic.
This is a nondecimal positive control, 不 a new certificate discovery.

## 6. Automata implementation 和 completed computation

```bash
python3 calculation/agent-118/build_regular.py --out-dir /tmp/p196-agent118-regular
python3 calculation/agent-118/test_regular.py --binary /tmp/p196-agent118-regular/center_regular
python3 calculation/agent-118/run_regular.py /tmp/p196-agent118-regular/center_regular --compare --seconds 120
```

One child process,4GiB address-space limit,120s wall limit; budgets200,000
automaton states,3,000,000 edges,100,000,000 charged operations. Final output:
`REG_DONE status=none scope=all_repetitions_all_widths fixed_at=6 tail_checks=14 peak_states=19258 peak_edges=1026983 ops=79132872 comparisons=35`.
Measured isolated run0.782s/~51MiB; a concurrent wrapper reproduction took
2.111s,51,828KiB peak child RSS. All runs completed without cap/timeout.

| Layer | DFA states | DFA edges | Accepted words of length3 | Length6 |
|---:|---:|---:|---:|---:|
| 1 | 49 | 520 | 1,000 | 1,000,000 |
| 2 | 937 | 32,582 | 30,592 | 935,560,192 |
| 3 | 2,437 | 128,164 | 93,376 | 8,574,299,136 |
| 4 | 2,863 | 138,181 | 116,128 | 8,868,958,208 |
| 5 | 3,505 | 160,765 | 140,104 | 9,157,137,472 |
| 6 | 3,930 | 171,267 | 152,584 | 9,312,887,872 |
| 7 | 3,930 | 171,267 | 152,584 | 9,312,887,872 |

Length3/6 slices are P24/P48 controls; counts do 不 establish language equality.
The exact DFA product establishes equality over EVERY word length. Counts at
length9 also agree at layers6/7:803,478,246,244,864, only an auxiliary statistic.
Every earlier adjacent comparison finds an explicit distinguishing word.

The optional early pruning deletes only product states that cannot accept 和
have no outgoing local option with the required coefficient. Nonclosing
intermediate ABC boundaries remain. A complete run disabling this pruning:

```bash
python3 calculation/agent-118/run_regular.py /tmp/p196-agent118-regular/center_regular --no-prune --states 1000000 --edges 20000000 --ops 200000000 --seconds 120
```

It returns the same complete negative, fixed DFA dimensions, 和 all slice
counts:peak93,200 states/4,753,720 edges,120,910,665 operations. The wrapper
reproduction took3.871s,176,636KiB. The first unoptimized implementation also
completed independently before the pruning was added. Neither caps nor a
failure to find an exact fixed point can produce NONE; they return UNDECIDED.

## 7. Independent validation 和 limits

`test_regular.py` is separately authored within this task. Its exact epsilon-free
NFA oracle checks31 models,79 finite slices,342 input words,1,289 output words,
plus global language identities, a fixed point, 和 a period-two example.
Explicit counterexamples exercise loss of input correlation, missing final
closure, premature closure at intermediate accepting states, incorrect input
endpoints, empty words, numerical-root comparisons, bounded-only equality,
omitted transient tails, 和 omitted periodic classes.

Production `--compare` decodes complete length3 frontier sets 和 compares them
with the original generator:7 generic layers plus28 terminal layers,35 exact
equalities,686,828 output tuples, zero differences. Five intermediate terminal
frontiers are nonempty before their final empty image. Seven length6 counts
match the independently cross-reproduced P48 computation. Four resource guards
和 an insufficient-layer guard safely return UNDECIDED.

A final positive test exercises the SAME production automata through actual
center completion, rather than relying only on nonempty intermediate sets:

```bash
python3 calculation/agent-118/positive_regular.py
```

The temporary harness renames only the CLI entry point 和 selects the known
base26 four-step center repeated three times, initial width4. The existing
decimal-only pruning is disabled. Complete P12 frontiers are `1 -> 64 -> 28 -> 1`;
three exact comparisons pass, the final four-state DFA accepts a length3 word,
和 the reconstructed12 edges pass independent integer replay. This test takes
8.38s including compilation,312,660KiB peak child RSS; it is 不 a new search
or a claim that the production decimal driver is parameterized generally.

Subset construction separately checks every initial subset, accepting flag,
label, 和 complete target union. Minimization checks its full quotient
homomorphism, including missing transitions. Whole-language equality separately
explores the exact DFA product with an explicit rejecting sink. Stable semantic
labels remain injective even as the local pools grow lazily.

```bash
python3 calculation/agent-118/build_regular.py --sanitize --out-dir /tmp/p196-agent118-regular-asan
ASAN_OPTIONS=detect_leaks=0:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 /tmp/p196-agent118-regular-asan/center_regular --layers 7 --states 200000 --edges 3000000 --ops 100000000 --compare
```

ASan/UBSan completes all35 comparisons 和 the same full negative in10.344s,
540,644KiB,exit0,empty stderr. Leak scanning alone is disabled because the
sandbox's ptrace mechanism prevents LeakSanitizer teardown; address 和 undefined
behavior checks remain enabled. Source reuse is pinned to the original core
SHA256 `eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.
Final regular-engine SHA256:
`8b7c00df5282f156bb027dfb5709d4ad82f7af614dec355fc8b6d93a86f27d19`.
The final source corrects one comment typo after sanitizer testing; executable
code 和 line numbering are unchanged.

## 8. Verification 和 publication

No new Lean theorem is proposed. A repository gate with zero changed Lean
modules does 不 kernel-verify a regular-language computation.
Required final gate: `python3 tools/verify.py --changed`.
BOARDv8 rescinded BOARDv7's temporary publication hold. The explicitly
authorized scoped-PR workflow applies, with all proof 和 verification rules.
