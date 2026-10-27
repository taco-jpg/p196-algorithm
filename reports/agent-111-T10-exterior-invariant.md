# Agent 111 — external exterior invariant verification

**PAPER PROOF + COMPUTED tool validation. No new Lean theorem.**

## Result and scope

An independently authored verifier checks an untrusted regular-language
invariant against the actual exterior carry equations. It supports both
forward and backward certificates, every positive repetition of a supplied
finite e/g unit, arbitrary finite B widths, and arbitrary natural trims.
It derives its arithmetic internally and uses direct finite-product
reachability; no generator minimizer, determinizer, or arithmetic is trusted.

**No invariant excluding the repeated decimal P24 target is supplied or
accepted in this result.** Its exact FIRST language is independently
corroborated, and several deliberately insufficient candidate languages are
correctly rejected. A rejected candidate, cap, or terminal intersection is
not a mathematical absence result or a reconstructed B cycle.

Scope was claimed in issue289 comment6433490122 and extended to backward
verification in6433608250. Agent106 retains the primary single-phase P24
language search,116 the independent block engine,113 the backward search,
and109/115 the bounded/all-lap and two-lap applications. Agent103's warning
about inverse coefficient-port direction and Agent113's external center
invariant audit are credited. This tool does not duplicate those searches.

The positional transfer is prior `bauto` work; common-width neutral padding
is credited to Agents7/107/109 and its Agent114 formalization in PR400.
Agents115/106 discovered the forced P24 head word used as a control.
Agent105's true base6 two-lap example is credited separately below.
The production verifier imports none of those generators. The arithmetic
control alone compares with the unchanged Python neutral-band mirror and
reads its source fixtures through the parser already present on main.
This is a main-based PR with no earlier Agent111 implementation dependency.

## Exact arithmetic contract (PAPER PROOF)

A phase-t cut symbol is `(t,L,H,Y)`: low incoming carry L, reverse outgoing
carry H, and the previous reverse digit Y at overflow phases (zero otherwise).
Encode it as `t*(4*b)+L*(2*b)+H*b+Y`. Carries are bits and `0<=Y<b`.

For a current coefficient `0<=x<=2*b-2`, choose `h in {0,1}` and require
`floor((x+h)/b)=H`. Put `L'=floor((x+L)/b)` and `R=(x+h) mod b`. Then

```text
x_next = (x+L) mod b + (Y if g_t=1 else R)
output = (t,L',h,R if g_t=1 else 0)
row    = (incoming coefficient x, output symbol, outgoing coefficient x_next)
```

Rows chosen along a complete temporal word must satisfy
`out_i=in_(i+1 mod length)`. The root unit is `(t,0,g_t,g_t)`;
the terminal unit is `(t,e_t,1-e_t,(b-1)*e_t if g_t=1 else 0)`.
Both boundary languages are exact **positive** powers of their unit words.

FIRST uses `x>=1` at every phase. At the root, an overflow gives
`x_next=(x mod b)+1>0`; a nonoverflow gives `x_next=2*x+h`.
A zero in a closed head sequence therefore propagates backward and forces
all heads and all overflow bits to zero. The production scope requires
sum(g)>0, so FIRST loses no physical cycle in that scope.

For a finite closed exterior itinerary whose streams are a positive
repetition of the supplied unit, choose a common width
`N>=max(1,max_t |B_t|)` and append neutral coefficients. Credited covariance
preserves e/g; the width ledger makes the new trims exactly `u_t=g_t`.
This includes original empty-B phases, which become positive-width words.
Thus every such closed itinerary gives a path from FIRST through zero
or more generic spatial images to the prescribed terminal word language.
FIRST is applied only once; later generic returns to the numeric root are
not incorrectly subjected to the special first-column restriction.

## Why either certificate suffices (PAPER PROOF)

Let T be the complete cyclic row image, and Q the terminal unit word.
For a forward candidate I the obligations are

```text
FIRST subset I;       T(I) subset I;       I intersect Q^+ = empty.
```

Induction on finite spatial width puts every reachable cut in I, contradicting
terminal separation. For a backward candidate K the exact dual is

```text
Q^+ subset K;        Pre(K) subset K;     FIRST intersect K = empty.
```

Trace any successful finite path backward from its terminal into K, obtaining
a contradiction at its first physical column. Both arguments cover all
finite widths and every positive unit repetition without a period-descent
assumption. Candidate languages may overapproximate phase order: closure
is then checked over that entire larger language, a stronger obligation.
An accepted empty word in a candidate is harmless; cyclic images exclude it.

Inverse rows transpose only old/new symbols:
`a:(x,b,x_next)` becomes `b:(x,a,x_next)`. The temporal coefficient ports and
word order stay unchanged. Reversing those ports is a different relation.

## Direct product checking

For cyclic image inclusion, search states
`(input_DFA_state,output_DFA_state,first_coefficient,current_coefficient)`.
A missing output transition goes to a rejecting sink. Each step consumes
one actual input edge and a compatible row, updating both DFA states and
the coefficient. A counterexample ends at an accepted input word, a closed
coefficient seam, and a rejected output word. Image disjointness changes
only the output acceptance condition. Complete graph exhaustion proves the
obligation over all word lengths. Accepting input prefixes keep their
outgoing transitions; closure is required at the chosen complete word end.

The general core also checks ordinary DFA/NFA inclusion and intersection,
including epsilon edges, by exact products. Its shortest-word search handles
zero-cost epsilon edges. Production candidate files are deterministic and
have no epsilon transitions. Every reported image failure is replayed
against its full input/output languages and all selected row seams before
printing; independent Python arithmetic then replays the test failures.

## Schema, use, and status contract

```text
P196_EXTERIOR_INVARIANT 1
base B
period P
e BINARY_E
g BINARY_G
states N
start Q
accept K ACCEPTING_STATE_INDICES
transitions M
FROM INTEGER_SYMBOL TO
... exactly M transition rows ...
end
```

The parser rejects duplicate deterministic labels, invalid states/symbols,
nonbinary/mismatched streams, trailing/truncated input, and zero overflow.
Supported bases are2..62. There is no B-only overflow-parity requirement.
No row table or cached proof result is accepted from the candidate.

```bash
python3 calculation/agent-111/exterior_invariant.py build /tmp/a111_check
/tmp/a111_check candidate.txt -states-cap 1000000 \
  -edges-cap 10000000 -work-cap 100000000
/tmp/a111_check candidate.txt -backward -states-cap 1000000 \
  -edges-cap 10000000 -work-cap 100000000
```

For resource-bounded execution use `exterior_invariant.run(binary,path,
timeout=30,memory_mb=4096,backward=False)`; caps are configurable keyword
arguments. The wrapper imposes address-space, CPU and wall limits.

| Exit | Meaning |
|---:|---|
|0|VALID_INVARIANT: all three stated-direction obligations proved|
|1|REJECTED_INVARIANT: a specific language obligation failed|
|2|INVALID_OR_UNSUPPORTED input|
|3|UNDECIDED resource interruption|
|4|internal verifier error|
|124|wrapper wall timeout, UNDECIDED|

Only exit0 with all three completed obligations validates an invariant.
A terminal overlap or backward FIRST overlap need not be reachable from both
ends; it is explicitly not called an actual B witness.

## Independent P24 FIRST corroboration

For the priority `e=010100110100101011001011`,
`g=110001001000110001001000`, the scalar head graph has432 vertices and352
unique arcs. Exact SCC analysis leaves24 cyclic vertices, one per phase:
`(9,10,1,2,5,11,2,5,10,1,2,4)^2`. This agrees with115/106's prior result.
Every closed temporal path therefore repeats that head word. The reverse
carry choices at phases1/5/8/13/17/20 are independently free, giving64 blocks
per unit and the full language `(union64 blockwords)^+`, with mixed blocks.
Its direct DFA has25 states/31 edges.

```bash
python3 -O calculation/agent-111/exterior_first_language.py --selftest
python3 calculation/agent-111/exterior_first_language.py \
  --output /tmp/a111_first.txt
/tmp/a111_check /tmp/a111_first.txt
```

The last call deliberately exits1: FIRST inclusion proves with236 product
states/296 edges; GENERIC closure fails with a shortest24-symbol witness
(289 states/375 edges searched). Thus this exact frontier is not an invariant.
The selftest compares130 head graphs with independent positive-return
reachability,110 exact fixtures/222 complete finite word sets/4430 words.
Twenty multiple-head cases are explicitly unsupported by this fixture
constructor, not discarded. P24 full FIRST sets match at k1=64 and k2=4096;
the uniform conclusion comes from the finite head graph, not those counts.

## Export interoperability

`exterior_invariant_import.py` reads Agent106's proposed single-phase JSON
(`start,finals,transitions`) or Agent116's proposed block JSON
(`dfa.start,dfa.states[{final,edges}]`). Exact base/e/g must be present or
supplied explicitly; conflicting metadata rejects. The output is always
labelled an untrusted candidate, regardless of the generator's claims.

```bash
python3 calculation/agent-111/exterior_invariant_import.py export.json \
  --schema single-phase --output /tmp/candidate.txt
python3 -O calculation/agent-111/exterior_invariant_import.py --selftest
```

For `--schema overflow-block`, symbols are `(startphase<<32)|cfg`,
`cfg=Lmask|(Hmask<<ell)|(Y<<(2*ell))`. Decode each into ell phase symbols.
Each old state's outgoing codewords become an exact prefix trie; intermediate
nodes reject. A separate audit enumerates the entire local codeword-to-target
relation, proving the same path language even through arbitrarily many cycles.
No determinization/minimization is used. Current block import requires an
overflow at phase0 and local packing within32 bits; unsupported encodings
reject. Controls cover11,600 complete block codec cases,224 cyclic-DFA edge
expansions, and two rejected expansion corruptions. These are schema controls;
no unpublished generator checkpoint is represented as independently replayed.

## Computed validation

```bash
c++ -O2 -std=c++17 -Wall -Wextra -pedantic \
  calculation/agent-111/exterior_invariant_selftest.cpp -o /tmp/a111_ext_test
/tmp/a111_ext_test
c++ -O1 -g -std=c++17 -fsanitize=address,undefined \
  -fno-omit-frame-pointer -fno-pie -no-pie \
  calculation/agent-111/exterior_invariant_selftest.cpp -o /tmp/a111_ext_test_san
ASAN_OPTIONS=detect_leaks=0 /tmp/a111_ext_test_san
python3 -O calculation/agent-111/exterior_invariant_arithmetic.py
python3 calculation/agent-111/exterior_invariant.py \
  build /tmp/a111_check_san --sanitize
python3 -O calculation/agent-111/exterior_invariant_controls.py \
  --binary /tmp/a111_check --sanitizer-binary /tmp/a111_check_san
```

| Independent check | Completed scope |
|---|---|
|Abstract exact products|6426 cyclic calls,3210 cyclic intersections;256 ordinary inclusions/253 intersections;74,437 product states|
|Abstract counterexamples|3494 shortest witnesses,190 epsilon;4862 independently replayed rows|
|Finite row oracle|1603 images;111,001 raw choices;19,412 closed choices;12,079 output words|
|Infinite/adversarial controls|22 exact infinite-language cases;3 FIRST languages;8 corruptions;802 changed relations;7 dual obligations;2 transpose controls|
|Arithmetic tables|704 complete forward tables:5456 generic/5104 positive rows;704 inverse tables/10,560 rows;1148 complete cyclic preimage comparisons|
|Whole-integer arithmetic|31,168 mirror comparisons;93,504 padding identities;36,085 all-trim/common-width identities|
|Physical/source boundaries|310 FIRST/root cases;8 source cycles/56 edges/328 cut tiles;20 zero-width distinctions|
|Production, each binary|10 fixtures;8 rejected-candidate witnesses/100 integer row replays;11 malformed inputs;6 real resource interruptions|

Both optimized and ASan/UBSan abstract/production runs pass. Only leak
detection is disabled because this sandbox prevents its process inspection.
The abstract suite is separately authored from the public API; finite tests
enumerate complete row products, while infinite tests use exact independently
specified languages. A three-edge coefficient cycle detects the critical
incorrect port reversal; a two-edge test alone would not distinguish it.

Two small control invariants validate (forward empty, backward nonempty Q+,
base10/e0/g1). P24 candidates deliberately fail each forward/backward
obligation. A base2/g1 FIRST response closes only after two unit copies and
is retained, directly checking whole-word rather than per-unit closure.

Agent105's base6 fixture has driver e=g=01 and four distinct B phases
`[4,7,7,8,3]`, `[9,3,4,5,8]`, `[4,7,7,10,2,2]`, `[9,3,4,9]`, with trims
`[0,0,2,0]`. Independent integer replay checks all4 edges; padding to width6
checks7 complete cut words and24 cyclic tiles, ending in Q^2. This retains a
physical multi-lap control. Agent105 retains its discovery and one-lap
impossibility analysis; no center or full cycleOK certificate is inferred.

## Repository gate

`python3 tools/verify.py --changed` passes against fetched main
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`:5217 Lean files/301 projects,
zero changed Lean modules/zero endpoints, `ALL CHECKS PASSED`.
This is repository compliance, not kernel verification of this checker.
Only new Agent111 code/report files are published; no README/RESULTS or
other agents' files change. Every publication must match the checked tree.
