# Agent 113 — every repetition of the known p11 center driver

## Result and scope

**PAPER PROOF + COMPUTED:** in base 10, the driver

```
E = (10100110011)^k
G = (11100010000)^k
k >= 1
```

has **no compatible center cycle at any finite width**, for **any natural
center-trim schedule**. The executable invariant check uses the particular
binary schedule `V=(01000010000)^k`; the extension to other schedules uses
the separately credited equal-total trim-transport theorem.

This excludes every repetition of the known p11 driver as a route to a
neutral-band certificate. It does not exclude other decimal driver streams,
prove an unrestricted neutral-band obstruction, decide the ordinary 196
orbit, or exhibit a decimal Lychrel number. **No new Lean theorem is claimed.**

The decisive computation checks an untrusted regular-language invariant with
separately written arithmetic and direct finite-graph searches. It does not
trust the invariant generator's local equations, determinizer, minimizer,
frontier counts, or assertion that two frontiers are equal.

Attribution: the existing neutral-band work supplies the exact center model;
Agent 118 supplied the successful correlated-MDD approach and owns the
separate p12 regular-language result (#399). Agent 111 owns the independent
p11 delayed-output implementation/review; its reported whole-language return
matches this result (issue289/comment6433380470). Agent 101 owns cumulative
complete-state reachability (#357), independently reviewed in our #379.
Agent 7/107 supply padding/trim transport (#336), with formalization #391.

This PR stacks on #379 for the independent Python reference used by tests.
The generator includes unchanged main `cauto_fast.cpp` only for local segment
tables. The independent invariant checker includes neither that source nor
our finite-automata library.

## 1. Every repetition is one regular language

The two trim positions are phases 1 and 6, with zero-based indices.
Starting after phase 1 produces alternating temporal segments:

| Type | Phases | e | g | Last-phase trim |
|---|---|---|---|---|
| A | 2,3,4,5,6 | 10011 | 10001 | 00001 |
| B | 7,8,9,10,0,1 | 001110 | 000011 | 000001 |

Each letter stores its type, every phase's two exposed carry bits and retained
high digit, and the pending coefficient at its final trim. All phase relations
inside a segment are retained. A complete cut for repetition count k is an
alternating word of exactly `2*k` letters. Segment B crosses into the next
chronological unit; this wrap is included, not identified with the old unit.

Let A0,B0 denote the prescribed outer-boundary letters. The source language is
`L0=(A0 B0)^+`, excluding the empty word. Its three-state automaton has a
separate nonaccepting initial state and permits further AB units after every
accepting boundary. These outgoing transitions must remain present even when
a particular transducer run has not yet closed its cyclic coefficient.

For one segment, local arithmetic gives choices `(new_configuration,c)`,
where c is that segment's first coefficient at the current spatial layer.
The output letter's pending coefficient is the NEXT segment's c. Thus a
cyclic transducer retains `(first_c,current_c)`, emits a letter with guessed
`next_c`, advances to it, and accepts only when `current_c=first_c` at the
actual word end. Combining this with the entire input-automaton path retains
all temporal correlations, for every positive word length simultaneously.

The generator uses image states `(input_node,current_c,first_c)`. Alphabet
IDs retain stable meanings `(type,complete_configuration,pending_coefficient)`.
Minimization is performed on whole languages, not independent sets of letters.

## 2. Uniform coverage of spatial widths

The phase-length offsets for the displayed schedule are

```
delta = (0,1,0,1,1,1,1,0,0,0,0).
```

They repeat for every k. Every positive initial width is uniquely
`m0=2*q+s`, with `q>=0` and `s in {1,2}`. There are exactly q generic layers
before the midpoint tail. Write T0 for the first generic transition, which
checks a trimmed outer coefficient against 9, and T for the stationary
interior transition, which checks it against stored pending memory.
For q>=1, the exact cut language is `T^(q-1)(T0(L0))`.

The q=0 exceptions are precisely widths 1 and 2. Every other width has one
of two fixed parity tails, represented at widths 3 and 4 starting at layer 1.
Both tails have exactly two layers:

| Parity | First tail layer | Second tail layer |
|---|---|---|
| Odd | ODD where delta=0; EVEN where delta=1 | EXTRA at 1,6; otherwise inactive |
| Even | EVEN where delta=0; generic where delta=1 | EXTRA at 0,2; ODD at 1,3,4,5,6; otherwise inactive |

Odd/even midpoint rules join the two normalization carry traces. EXTRA checks
the additional central output created by overflow. Pending trim coefficients
receive their final check: for a trimmed phase, the next center half-length
equals the raw half-length minus one. No terminal memory obligation is lost.

Both segment types start the SECOND tail layer at an inactive position.
Its first coefficient is consequently NONE in each segment. The independent
checker can compose the two layers locally and check the remaining cyclic
first-layer relation by ordinary graph reachability, without building or
minimizing a tail NFA. At widths 1 and 2 only the first-layer boundary flag
changes. These facts hold uniformly in q and k.

## 3. Independently checked invariant certificate

The generated DFA I has **13,876 states and 470,714 labelled transitions**.
The independent checker treats its states, edges, and decoded alphabet as
untrusted input. It verifies syntax, semantic-symbol uniqueness and bounds,
determinism, chronological segment types, and `I subset (AB)^+`.
Initial boundary letters are independently constructed from E/G.

It then verifies the following finite obligations:

```
T0(L0) subset I
T(I) subset I
short_width_1(L0) = empty
short_width_2(L0) = empty
odd_tail(I) = empty
even_tail(I) = empty
```

For inclusion, it explores the product of the source DFA, the independent
cyclic arithmetic transducer, and the target DFA. A missing semantic output
letter or transition goes to a rejecting sink. Exploration continues there:
only an accepted source word with closed coefficient trace is a counterexample.
This checks all finite accepted word lengths, not a bounded set of repetitions.

The first two inclusions imply by induction that every generic cut language
is contained in I. The remaining four emptiness checks exclude every q>=0,
every k>=1. This proof uses a checked invariant; it does not assume that
regular-image iteration must terminate, or that its cumulative union is regular.

**COMPUTED independent checker output:**

| Obligation | Reached product states | Result |
|---|---:|---|
| Correct positive alternating word shape | 13,876 | PASS |
| First image included in I | 171 | PASS |
| Generic image included in I | 232,168 | PASS |
| Width 1 exception empty | 19 | PASS |
| Width 2 exception empty | 19 | PASS |
| Odd tail empty | 57 | PASS |
| Even tail empty | 59 | PASS |

Total: **10,173,487 charged operations**, **21,340 local arithmetic calls**,
peak **232,168 product states**, complete `VERIFIED_INVARIANT`, exit 0.
Here VERIFIED_INVARIANT is a computed checker status, not Lean verification.

## 4. Natural trims and rotations

For any closed center cycle with these E/G streams, length accounting gives
`sum(v)=sum(g)/2=2*k`. The displayed binary schedule w has the same total.
Using the credited padding covariance, choose nonnegative depths a_t with
`a_(t+1)=a_t+v_t-w_t`, taking a0 large enough to cover all partial deficits.
Equal totals imply `a_P=a0`. Padding center t by a_t neutral pairs preserves
validity, symmetry, carry/overflow streams, and the cyclic seam, while changing
its trim to w_t. An assumed arbitrary-trim cycle would therefore give one
excluded by the invariant. This is a PAPER corollary of existing transport,
not a claim that the binary-schedule executable accepts arbitrary trim inputs.
Joint rotations of the driver are covered by reindexing temporal phases.

## 5. Reproduction and independent controls

From the repository root:

```sh
c++ -O2 -std=c++17 calculation/agent-113/center_regular.cpp -o /tmp/a113_regular
c++ -O2 -std=c++17 calculation/agent-113/check_regular_invariant.cpp -o /tmp/a113_check
/tmp/a113_regular 10 10100110011 11100010000 01000010000 --depth 8 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 120
set -o pipefail
/tmp/a113_regular 10 10100110011 11100010000 01000010000 --text-depth 5 --depth 5 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 120 | /tmp/a113_check - --seconds 180 --memory-mib 4096 --states 5000000 --ops 600000000
```

The first command finds exact whole-language `L5=L6`; both short cases and
all ten earlier parity tails are empty. The last raw image has 231,344 NFA
states and 8,350,120 edges; complete run 127,361,537 charged operations,
about 199 MiB peak RSS. The second command independently verifies the smaller
set of invariant obligations above. The generated text is certificate data,
not trusted executable code; it need not be saved or added to the repository.

The following finite counts are controls, not the uniform proof:

| Generic depth | k=1 | k=2 | k=3 |
|---:|---:|---:|---:|
| 1 | 35 | 1,225 | 42,875 |
| 2 | 83 | 7,577 | 657,443 |
| 3 | 243 | 115,033 | 34,755,075 |
| 4 | 563 | 559,193 | 414,911,363 |
| 5 | 755 | 960,601 | 752,450,435 |
| 6 | 755 | 960,601 | 752,450,435 |

Unchanged explicit-frontier code reproduces k1/k2, and Agent111/118's
independently authored MDD results supply k3 controls (#380/#369).
Our independently written global chronological Python recurrence compares
**52,550 complete p11 cut tuples** with the regular automata: k1 at depths
1,2,5; k2 at 1,2; k3 at 1. Injective semantic encoding, membership of every
tuple, and equal independently counted DFA cardinality establish exact finite
set equality. A base-2 positive family adds 898 tuples and three actual-center
prefix controls. Production short/interior positive-tail tests in bases
2,4,8,26 reconstruct and independently integer-replay **22 complete edges**.

```sh
python3 calculation/agent-113/test_p11_regular.py --engine /tmp/a113_regular --depths 1 2 5
python3 calculation/agent-113/test_p11_regular.py --engine /tmp/a113_regular --base 2 --e 1010 --g 1010 --v 0001 --depths 1 2 5
python3 -O calculation/agent-113/test_p11_regular.py --engine /tmp/a113_regular --positive-tails --guards
c++ -O2 -std=c++17 calculation/agent-113/test_finite_automata.cpp -o /tmp/a113_fa_test
/tmp/a113_fa_test
```

Automata controls cover 120 random NFAs, 131,160 independently enumerated
words, 120 canonicalization comparisons, new-alphabet and rejecting-sink
cases, epsilon handling, and exact big-integer counting. ASan/UBSan pass
for this library; leak scanning is disabled because of the container's proc
restrictions. Ten production guards distinguish five malformed inputs from
five incomplete searches, including a real one-second timeout. They never
turn a cap into an exclusion. Python checks remain active under optimization.

The standalone invariant-checker regression independently accepts the full
certificate, rejects a depth-1 non-invariant, rejects **12 corruptions**, and
returns UNDECIDED for two forced resource caps. Corruptions include empty-word
acceptance, removal of the initial transitions, wrong driver/order, duplicate
symbols/edges, bad carry/pending data, out-of-range edges, truncation, and
trailing data. The full invariant also passes ASan/UBSan:

```sh
python3 calculation/agent-113/test_regular_invariant.py --engine /tmp/a113_regular --checker /tmp/a113_check --sanitize --seconds 180
python3 calculation/agent-113/test_center_local_relations.py --engine /tmp/a113_regular
```

The sanitizer option builds a temporary wrapper around the same checker.
It preserves state/operation/time guards and bypasses only the address-space
limit incompatible with ASan's virtual reservation. The arithmetic test
compares complete local relations with the independent global Python model:
1,680 generic queries, 74 terminal queries, and 2,504 successor tuples agree.
Cached two-layer terminal composition additionally agrees on 3,424 cases,
including 60 synthetic negative and four synthetic positive cut states.
Those synthetic cuts are controls, not claims of reachable center cycles.

Repository gate `python3 tools/verify.py --changed`: **PASS**, 5,217 Lean
files / 301 projects, zero changed Lean modules or endpoint audits.
The exact published tree is checked before publication. No existing checker,
other agent's source, README, RESULTS, Lean source, or registry is changed.
