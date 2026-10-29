# Eight-step obstruction for a phase-changing ternary automatic centre in decimal reverse-and-add

**PAPER PROOF**, with a complete bounded finite transducer computation and a separate independent Python checker. This is a new restriction on the F1 candidate family, **not** a decimal Lychrel certificate, an unrestricted centre exclusion, or a claim about the actual orbit of 196.

## Statement and exact scope

Let `μ(0)=01, μ(1)=02, μ(2)=00` and `x=lim μ^k(0)`. Consider a palindromic pair-coefficient word for a base-10 integer whose lower-side interior contains a length-32 factor of `x` encoded using **three distinct coefficients** `A_0,A_1,A_2 ∈ {0,...,18}`. The factor can occur at any shift, but must be far enough from both the external literal boundary and the midpoint that the relevant interval and its mirror remain in the two sides throughout the following eight steps. Suppose the ordinary reverse-and-add orbit has overflow bits, in order, `g=10101010`. **No possible eight-step evolution** of this interval can produce, on the aligned length-28 final interval, a factor of `x` encoded using any three distinct decimal pair coefficients, at any shift. Crucially, the intermediate seven centre words need **not** be automatic, ternary, periodic, palindromic literals, or belong to any restricted alphabet.

This is an endpoint-language obstruction for the specified overflow sequence. It does not cover short core windows, the opposite cyclic rotation `01010101`, different substitutions, noninjective endpoint coding, other nearby interval alignments, or arbitrary phase-changing quasi-periodic centres.

## Exact local overapproximation

At every step, the input pair word is palindromic and its coefficient positions are least-significant first. For any length-`L` lower interior segment `w`, normalization of the integer value yields decimal digits on that segment from a left-to-right carry-in bit `cL∈{0,1}`. Independently, the mirrored segment yields digits from the reversed input with a right-to-left carry-in bit `cR∈{0,1}`. The actual global carries at the two ends are among these four choices. Let `lo[i]` be normalized digits of `w` from `cL` and `hi[i]` be normalized digits obtained by normalizing `reverse(w)` from `cR` and reversing the resulting digit word. The next pair coefficients are precisely:

* If overflow `γ=0`, `q[i]=lo[i]+hi[i]`, `i=0,...,L-1`, yielding length `L`.
* If overflow `γ=1`, `q[i-1]=lo[i]+hi[i-1]`, `i=1,...,L-1`, yielding length `L-1`.

Overflow one changes the mirror partner by one column. Every generated coefficient lies in `[0,18]`. Allowing **all four entering carry pairs at every step** gives an overapproximation of all realizable integer trajectories; no unverified boundary carry assumptions can produce a false exclusion. After `10101010`, precisely four columns have been lost, so a source segment of length `n+4` gives a final segment of length `n`.

**Prefix-cropping lemma:** if a long segment follows one of these local transitions, then its shorter left prefix follows one of the four transitions of the corresponding shorter source prefix, after cropping the new last column if necessary. Use the same left entry bit and choose the entering right bit of the shortened segment to be the actual carry after normalizing the removed right-hand columns. Induction gives this inclusion for eight transitions. Thus any length-32-to-28 endpoint match would imply a length-28-to-24 endpoint match for the same input coefficient table, by taking the left prefix. This justifies eliminating all tables found impossible in the shorter exhaustive run before testing width 32.

## Exact finite factor languages and computations

Let `L_n` be the set of length-`n` factors of `x`. As proved in `Agent13TernaryOverflowObstruction`, `L_2={00,01,02,10,20}` and, for `n>=3`, `L_n` consists of the offset-0 and offset-1 length-`n` windows of `μ(L_ceil((n+1)/2))`; this is an exact terminating recurrence. In particular `|L_24|=64`, `|L_28|=72`, and `|L_32|=80`. The C++ primary program independently generates the same factor sets from the first 65,536 letters of `x`; equality with the exact recurrence is checked by the Python program, not assumed from a long prefix.

For the shorter necessary test (`n=24`), the C++ program enumerates **every one of the `19×18×17=5,814` ordered injective input coefficient tables** and **every one of the 72 exact source factors of length 28**, namely **418,608** source/table cases. It propagates the full set of words under each of the four possible boundary-carry choices at each of eight steps, with deterministic hash-set deduplication of **exact base-19 packed coefficient words** (no hash-only equivalence). At every final state, it compares the equality pattern against all factors of `L_24`, allowing arbitrary injective output coding. No case reached the 50,000-state cap (observed maximum 2,400 states). Exactly **16 matches** survived, all at these four input tables:

| input table `(A0,A1,A2)` | matching L28 source factors |
|---|---:|
| `(0,8,17)` | 4 |
| `(0,17,8)` | 4 |
| `(18,1,10)` | 4 |
| `(18,10,1)` | 4 |

All other **5,810 tables** have zero matches. This is a complete finite classification, not a sample or a partial census.

By the prefix-cropping lemma, only these four tables could possibly survive the longer `n=28` test. The **independent Python implementation**, with a different coefficient-word representation and recursive factor generator, exhausts all `4×80=320` length-32 input factor/table cases. It propagates all four arbitrary carry choices at every step and compares every final length-28 word against the exact `L_28` equality patterns. **Zero survive.** Therefore no input table can satisfy the length-32-to-28 eight-step endpoint condition, proving the stated obstruction.

## Independent arithmetic, controls and reproduction

The Python checker separately validates the local formula against **3,000 ordinary decimal integer digit-normalization and reverse-add calculations**, including both actual overflow parities. Its prefix-cropping property is checked against 5,000 randomized segments and both gammas; the proof above does not depend on that sampling. All exact `L_24/L_28/L_32` languages are independently checked against the C++ prefix generator. Existing positive base-9 (`g=1100011000`, `|B|=61`) and both base-13 (`g=1010010000`, `|B|=75,55`) controls are run through the previously committed independent arithmetic engine. Those are controls, not new certificates.

From repository root, with Python 3, standard C++17 compiler, and no third-party dependencies:

```sh
sh calculation/decimal_frontier/ternary_p8/run.sh /tmp/agent13-ternary-p8
```

This builds `p8_nfa.cpp`, resumes `n24.tsv` at the next uncompleted table on restart (the output is **outside** the repository), runs the full exact 5,814-table census at cap 50,000, verifies every row via `verify.py`, runs `independent.py` and mandatory controls. The C++ calculation is exact, one-core, and below 8 GB; finite caps are explicitly checked to be unused. All code, scripts, commands, and compact summary data are committed together under `calculation/decimal_frontier/ternary_p8/`. No giant search logs or ephemeral probes are part of the result.

**Boundary of the claim:** only the specified substitution, one prescribed eight-step overflow schedule, injective ternary start/end codings and an appropriately interior length-32 factor. It neither implies an all-width K1 kink obstruction nor proves or disproves that any base-10 Lychrel number exists.
