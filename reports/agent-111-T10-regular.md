# Agent 111 — independent all-repetition p11 center verification

**PAPER PROOF + COMPUTED. No new Lean theorem.**

## Result, attribution, and dependencies

Independently corroborates Agent113's primary p11 regular-language result:
in base10, for every positive integer k, the streams
`e=(10100110011)^k`, `g=(11100010000)^k` admit **no closed center itinerary
at any finite width**, with any natural trim schedule. This includes common
cyclic rotations of those streams. It does not exclude other exterior
streams, every decimal certificate, or decimal Lychrel numbers.

Agent113 claimed the primary p11 application in issue289 comment6433210400;
our independent scope is comment6433215987. Their preliminary canonical
return (comment6433329526) has the same13,876 states/470,714 edges.
Agent118 retains primary regular-language design/p12 application attribution.
This independently authored delayed-output construction differs from their
required-coefficient recurrence. No other agent's automaton source was used
to implement it. Our earlier p11/k3 MDD result is PR380.

This PR is stacked directly on PR344, which supplies `long_center.py` and
`center_controls.py`. It does not depend on PR380's MDD implementation.
All new implementation/test files are under `calculation/agent-111/`.
Local arithmetic reuses the original `cauto_fast.cpp`; independence concerns
the regular-language representation, image construction, and its review.
The whole-integer oracle independently checks the arithmetic bridge.
Original source SHA256:
`eb2e6b18b09fdfcae0a5b6b818d23291123ed6a76b59fb6e531589e7f6d00fff`.
Guarded temporary-header SHA256:
`01077a522265dbaa2e6428b352b2497ffea8bcc163cce903fcf69c1e32582bfc`.

## Typed finite words represent every repetition (PAPER PROOF)

Use the binary trim unit `v=01000010000`, whose sum is2. The ordered unit
segments are A:phases2..6 and B:phases7..10,0,1. A symbol contains the segment
type and its complete existing local state `(configuration,z)`; its numeric
encoding is `(uint64(type)<<32)|local_id`. A persistent local arithmetic
instance gives every symbol the same meaning throughout the computation.
Occurrences of a type share transition definitions, not chosen states.

The initial language is the positive powers `(A_start B_start)^k`, k>=1.
For each spatial layer j, let F_j^(k) be the original complete frontier for
the repeated temporal period11k. The regular language L_j is exactly their
typed union. In particular, the slice of L_j at word length2k is F_j^(k).
No primitive center response or bound on k is assumed.

For an input symbol x_i of type t_i, the original local table supplies rows
`(y_i,c_i)`. The output symbol at position i is
`encode(t_i,y_i,c_(i+1 mod n))`. Our NFA delays that output by one position.
After selecting the first input edge and row, its pending state is
`(old_DFA_state,previous_type,previous_y,first_c)`. At each next input edge
and local row `(y,c)`, emit `encode(previous_type,previous_y,c)` and retain
the new pending y. If the old state accepts, also emit
`encode(previous_type,previous_y,first_c)` to a terminal-only accepting node.
The pending state retains its outgoing continuations at accepting prefixes.

Every nonempty accepted input path and selection of local rows produces
exactly its cyclic image path. Conversely, each accepted output path records
such an input path and rows, including its closing coefficient. This proves
exact image equality for all finite word lengths. It covers one-symbol
words, inactive signed c=-1, and words that traverse accepting prefixes.
The general API computes image(L minus {empty word}); an accepting old start
is preserved so nonempty paths revisiting it are not lost.

Determinization uses exact NFA subsets. Canonicalization first removes
unreachable/nonproductive states, treating missing edges as the same implicit
rejecting sink. Moore refinement begins with acceptance and only splits old
classes by their full sorted `(label,target_class)` vectors. A stable class
count is therefore a stable equivalence relation. Sorted-label BFS numbers
the quotient canonically. Equality compares every acceptance bit and edge,
not counts, hashes, bounded prefixes, or independent coordinate projections.

## Uniform width reduction and arbitrary trims (PAPER PROOF)

The unit width offset is `d=(0,1,0,1,1,1,1,0,0,0,0)`. Because both unit
totals balance, this same offset repeats for every k; width thresholds do
not grow with k. At starting width w, the first terminal layer is
`j0=floor((w-1)/2)` and the total layer count is `j0+2`.
All preceding layers after layer0 use one stationary generic relation.
The two terminal signatures depend only on parity, apart from the special
first-layer boundary at widths1/2. For w>=3, increasing width by2 shifts their
layer indices by1 without changing the local signatures.

The exact generic language equality L5=L6 consequently determines every
later frontier uniformly in k. F0 is excluded from recurrence detection
because it has a special boundary signature. All widths1..22 and eventual
parity representatives23/24 are checked by their complete tail languages.
All are empty. This covers every positive width and every positive k;
the conservative `mlo=23` follows the existing unit-P all-width threshold.

Every accepted center itinerary is symmetric, since each incoming center
map is symmetric; empty centers violate the complementary carry condition.
Thus the nonempty symmetric domain covers all accepted closed centers.

For an arbitrary natural trim schedule r on11k phases, width closure forces
sum r=2k=sum v^k. The credited neutral-padding covariance/transport theorem
(Agents7/107/110, PRs315/336/338) chooses integer padding heights h satisfying
`h_(t+1)-h_t=r_t-v_t`; equality of totals makes this cyclic. Adding a common
constant makes every h nonnegative. Padding then preserves the prescribed
e/g streams and transports the itinerary to v^k. Its width is finite for
each finite k; no uniform bound on padding is needed because all widths
have already been excluded. This is reuse of their theorem, not a new
padding result or a formal Lean verification in this PR.

## Exact computation

```bash
python3 calculation/agent-111/regular_center.py build /tmp/agent111_regular
python3 -O calculation/agent-111/regular_p11.py /tmp/agent111_regular
```

The runner uses30s wall,6GiB address space,500,000 automaton states,
12,000,000 edges and150,000,000 charged work operations per image.
Both target runs completed within these limits. Exact finite-k counts are useful
controls; they are not the reason the all-k conclusion follows.

| Layer | Minimal DFA states | Edges | k=1 | k=2 | k=3 |
|---|---:|---:|---:|---:|---:|
|1|37|255|35|1225|42875|
|2|121|1114|83|7577|657443|
|3|1021|19452|243|115033|34755075|
|4|3907|112820|563|559193|414911363|
|5|13876|470714|755|960601|752450435|
|6|13876|470714|755|960601|752450435|

```text
REGULAR_PERIOD jstar=5 period=1 equality=full_canonical_DFA
DONE v=01000010000 status=none quantifier=all_positive_repetitions
jstar=5 period=1 mlo=23 classes=2 feasible_classes=0 images=40 tails=24
STATUS=NO_CENTER_FOR_ANY_POSITIVE_REPETITION_OR_FINITE_WIDTH_OF_THIS_DRIVER
```

The last generic image has403,342 NFA states/10,976,027 edges,29,512 subset states/
952,516 edges, and39,848,404 charged operations. The first target run took
3.704s/364MiB peak RSS; an independent rerun took3.350s/364MiB. No cap fired.
The24 tails count width invocations, including equivalent signatures and
early empty languages; they are not24 distinct signature classes.

## Independent controls

```bash
c++ -O2 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-111/regular_selftest.cpp -o /tmp/a111_regular_test
/tmp/a111_regular_test
python3 -O calculation/agent-111/regular_audit.py
python3 -O calculation/agent-111/regular_controls.py \
  --binary /tmp/agent111_regular
```

The C++ oracle was written from the public API before its author read the
implementation. It uses direct Cartesian choices on complete finite words
and independently specified expected regular languages. The Python audit
separately compares delayed-output and required-coefficient transducers.
Equivalence explores the entire finite product DFA with implicit dead sinks;
there is no word-length cutoff for those language checks.

| Check | Completed scope |
|---|---|
|C++ finite oracle|1000 seeded cases;2003 finite images;61,112 raw choices;32,592 output words;1003 changed relations|
|C++ exact language oracle|247 unbounded-length image comparisons;2978 equivalences;82,325 explored product states;4374 distinguished state pairs|
|Canonicalization/NFA controls|241 canonical cases;242 NFA cases;5 invalid-input and4 cap controls|
|Independent Python transduction|67 exact regular-language comparisons;67 partial-DFA canonical checks;1177 bounded explicit outputs;357 complete predecessor paths;4 empty-word controls|
|Phase mapping|4052 mappings: every nonempty trim word of periods1..9, repetitions1/2/3/5|
|Whole-integer return graphs|664 patterns;2660 widths;102,132 center states;456 return edges;14 positive/2646 negative widths;zero discrepancies|

The247 unbounded-length checks include finite/empty languages; this count
does not assert247 infinite languages. Explicit infinite-language controls
include identity, relabeling, typed cyclic shift, accepting-prefix loops,
and closure behavior. Full uint64 symbols and nonproductive dead cycles
are included in canonicalization controls.

For each fixed-width whole-integer case, enumerate every symmetric center
and compute its partial one-unit return function by direct integer
normalization. Kahn peeling leaves exactly its cyclic states, hence decides
existence for every positive repetition count at that width. Every retained
edge is replayed. This corpus has14 cycles/14 cyclic states and56 replayed
temporal edges; all its cycles have repetition1. We do not mislabel it as
an empirical subharmonic-positive corpus.

Complete finite-frontier sets also agree with the separately authored
`regular_frontier_explicit.cpp`, which uses only the original explicit Fast
engine. Comparisons decode full type/configuration/signed-z tuples, removing
dependence on local numeric IDs. The18 comparisons cover p11 k1 layers1..6,
k2 layers1..3, and source-base2 repetitions1/2/3 at layers1..3:
153,545 complete words in total, largest frontier115,033. This is full set
equality, not merely agreement of the counts in the table.

```bash
python3 -O calculation/agent-111/regular_frontier_controls.py \
  --binary /tmp/agent111_regular
c++ -O1 -g -std=c++17 -fsanitize=address,undefined \
  -fno-omit-frame-pointer -fno-pie -no-pie \
  calculation/agent-111/regular_selftest.cpp -o /tmp/a111_regular_test_san
ASAN_OPTIONS=detect_leaks=0 /tmp/a111_regular_test_san
python3 calculation/agent-111/regular_center.py build \
  /tmp/agent111_regular_san --sanitize
python3 -O calculation/agent-111/regular_adapter_smoke.py \
  --binary /tmp/agent111_regular --sanitizer-binary /tmp/agent111_regular_san
```

ASan/UBSan passes the same complete synthetic corpus. Production smoke
controls reconstruct source-base2 K1, twice-repeated K2, asymmetric K2
clustered trims `11000000`, and source-base26 K1. Each binary independently
replays24 integer edges (48 total); every returned response uses one supplied
unit, so no concrete subharmonic witness is claimed. Both binaries also pass
8 direct rejections,9 state/edge/work cap paths across finite/generic/all-width
modes,1 generic-horizon case, and7 Python-wrapper rejections. Incomplete
outcomes are checked for absence of both positive and negative decisions.
Only leak detection is disabled for the sandbox's inspection restriction;
address and undefined-behavior checks stay enabled.

## Witnesses, limits, and scope discipline

Every production positive, even without `-w`, chooses a finite accepted word,
recomputes every layer for the actual width, and recovers full accepting
predecessor paths. Position i requires a local row `(y_i,z_(i-1 mod n))`.
DP merges prefixes only at equal `(position,old_DFA_state)`; no marginal
combination replaces a path. For unit anchor a, phase t of word repetition r
maps to `(rP+t+P*[t<a]) mod(kP)`, preserving the wrapped segment chronology.
All actual kP center transitions, including final closure, are replayed
before `FEASIBLE ... replay=ok` is emitted. Reconstruction limits remain
unresolved outcomes, not negative decisions.

The adapter accepts guarded units P<=48 and at least one binary trim;
zero-trim inputs are explicitly unsupported. A legacy fixed-period fallback
would lose the all-k quantifier and is therefore forbidden here. Canonical
state/edge/work limits, OS memory/CPU/wall limits, failure to find a generic
period, and unsupported inputs all remain UNDECIDED. Finite-k count overflow
only saturates display and never affects equality or acceptance.

Agent116's known base20 source-width27 positive was also tried as an optional
stress control. Even a16,000,000-edge budget capped after two completed
images (4.152s,2GiB address budget). It is explicitly UNDECIDED for this
representation, not a failed certificate or an absence result. The source
is PR356 commit `b7a718b78d67cf54d362232ba1b8f90fbec23af8`.

## Repository verification

`python3 tools/verify.py --changed` passed against fetched main
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:5217 Lean files/301 projects,
zero new or changed Lean modules, zero endpoints audited, and
`ALL CHECKS PASSED (changed files only, against origin/main)`.
This is the repository compliance gate, not kernel verification of the
computed exclusion. Publication uses the exact checked file contents;
the shared README/RESULTS, Lean registry, and other agents' files are unchanged.
