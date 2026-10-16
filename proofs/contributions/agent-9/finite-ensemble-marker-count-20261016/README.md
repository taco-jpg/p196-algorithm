# Exact finite ensemble marker count

The complete ordinary-integer count in equation (3) of the preserved finite-horizon density note is now Lean-checked, together with its direct finite positive-hit upper bound. The fresh author gate passed on 2026-10-16 with official Lean 4.19.0, `--trust=0`, all 100 literal export reports, 和 an exhaustive audit of every theorem 和 safe definition from the selected compiled module origins. The mathematical files are frozen at the hashes in `AUTHOR_FREEZE.json`. Independent review evidence is recorded separately under `review/horizon-safety/`.

## Exact source 和 scope

This formalizes the existing written argument at:

- Original commit: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Original path: `proofs/contributions/2026-10-14-finite-horizon-density/README.md`.
- Git blob: `6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c`.
- SHA256: `dc9ee090a96d434f5ef6ab5874b32c70bb2e18d8e520d20e7996f2d03e8af2dd`.
- Written statement: “Exact finite counting bound,” equation (3), with the accompanying counting proof.

The original bytes are retained in `source/README.original.md`. The source already proves the counting statement on paper 和 explicitly distinguishes it from its then-existing Lean deterministic marker theorem. This contribution supplies the missing finite formalization; it makes no novelty claim.

For natural `L > 0` 和 `r > 0`, define

\[
J=\left\lfloor\frac{\max(\lfloor L/2\rfloor-1,0)}r\right\rfloor,
\qquad a_j=1+jr.
\]

The `j`th marker means that the digits at every position `a_j+i` 和 `L-1-(a_j+i)`, for `i<r`, are all nine. Digits are numbered from the least significant digit. In the final numeric predicate each digit is literally `n / 10^i % 10`.

`unmarkedSeeds L r` is a complete duplicate-free list of precisely the integers in `[10^(L-1),10^L)` with none of these `J` markers. Its exact length is

\[
9\,10^{L-1-2rJ}(10^{2r}-1)^J.
\]

The theorem `mem_unmarkedSeeds` is a full membership iff using the ordinary decimal interval 和 the intrinsic quotient/remainder marker predicate. It does not leave a restriction to one digit-splitting profile or to a constructed subfamily. `unmarkedSeeds_nodup` proves each integer occurs once.

## The finite early-hit consequence

For every natural `R`, let `r = FiniteHorizonBlocks.blockLength R`. This is the original sufficient run length for the positive horizon `H=R+1`:

\[
r=\min\{1+2R,\ 1+\lfloor(7R+4)/4\rfloor\}.
\]

`positiveHits L R` filters the complete canonical interval by an explicit finite Boolean test. The test ranges over `k=0,...,R` 和 checks the actual ordinary reverse-add orbit at time `k+1`. `mem_positiveHits` proves that its members are exactly the width-`L` integers with a palindrome at some `1≤t≤R+1`.

`positiveHits_subset_unmarkedSeeds` invokes the unchanged `FiniteHorizonBlocks.mirroredNines_safe_prefix`. Consequently `positiveHits_count_le` bounds the length of that complete early-hit list by the displayed exact marker-complement count. An initially palindromic seed is allowed throughout. This is an upper bound on early hits; the exact equality counts the marker complement.

The analytic limits, growing logarithmic horizons, initial-palindrome intersection formulas (4)/(5), time-zero refinements, fixed infinite survivors, 和 claims about 196 are outside this contribution.

## Proof structure 和 interfaces

All new mathematical names are in `P196.Agent9.Ensemble`. `exports.json` records every literal definition/theorem export.

| Module | Main contribution |
| --- | --- |
| `Agent9FiniteProducts` | Complete fixed-length finite word products; duplicate freedom; repeated block concatenation; full positional membership using `drop (j*r)` followed by `take r`. |
| `Agent9MarkerWords` | All 100 inner pair choices 和 90 canonical outer choices; removal of exactly the one all-nine block; complete fixed-length pair wrapping, injectivity, boundedness, low-position reads, 和 reflected-position reads. |
| `Agent9MarkerEnumeration` | Complete canonical digit-list membership iff, exact width, absence of precisely the selected markers, duplicate freedom, 和 the product count. |
| `Agent9NumericMarkerCount` | Quotient/remainder digit bridge; all-width geometry; one-digit boundary; complete intrinsic ordinary-integer membership; numeric duplicate freedom; equation (3). |
| `Agent9FiniteHorizonCount` | Exact canonical interval enumeration; positive-time hit semantics; direct use of the original deterministic marker theorem; the finite natural-number upper count. |

For widths at least two, the proof decomposes a canonical digit list into one outer pair, `J` complete selected blocks of `r` pairs each, a free suffix of pairs, 和 the optional center. Writing

\[
q=\lfloor L/2\rfloor-1-Jr,\qquad e=L\bmod2,
\]

the intermediate count is

\[
90(10^{2r}-1)^J100^q10^e.
\]

The proved width 和 exponent identities turn this into the source expression. Fixed-length decomposition 和 wrapping injectivity establish a bijection with all canonical words satisfying the marker condition.

### Boundary checks in the theorem statements

- `L=1` is represented by exactly the nine single digits `1,...,9`.
- `J=0` yields every canonical width-`L` seed, as required by the vacuous marker condition.
- The leading digit lies in `1,...,9`; the trailing digit may be zero.
- Even 和 odd widths are included. `selected_position_geometry` places each low position strictly below `L/2` 和 each reflected position strictly above `(L-1)/2`, away from both endpoints 和 any odd center.
- `selected_digits_le` proves `2*r*J ≤ L-1`, so the free-digit exponent has its intended ordinary meaning.
- One complete `r`-pair block has `10^(2*r)-1` allowed fillings. Individual pairs inside an allowed block may equal `(9,9)`.
- The public completeness theorem assumes precisely `L>0` 和 `r>0`; no zero-width claim is made.

## Reuse 和 import provenance

`dependencies.json` pins all 11 unchanged source files by original path, source commit, Git blob, SHA256, 和 current local path. The existing Agent101 finite product/numeral helpers 和 the original FiniteHorizonBlocks dynamics are reused.

The original numeral source families have duplicate foundation names. The preserved consolidation compatibility source `Lychrel196Research__c6542b77be5d4aca.lean`, blob `72a4f16d2160c3ebcee1d729fa1f5c717739b57e`, contains only its provenance comment 和 `import LychrelDigitSums`. Using those exact bytes gives one common unchanged foundation for Agent101NumericFibers 和 FiniteHorizonBlocks. The author rebuild validates that route from source. The adapter contributes zero declarations, which the audit explicitly records while still requiring its compiled import.

`source/CENSUS-REUSE.md` records the scoped coverage/ownership review 和 the reused interfaces. This contribution leaves the existing fixed-profile fibers, protected-profile families, running-maximum work, cylinder-image work, 和 separately claimed digit-sum collapse unchanged.

## Verification receipt

The full author build in `verification/full-001/` ran from 22:17:43 to 22:19:42 UTC on 2026-10-16. It used a fresh private directory 和 copied no compiled objects. Its exact command for each module included `--trust=0 -j1 -DElab.async=false`.

| Gate | Result |
| --- | --- |
| Official compiler | Lean 4.19.0, commit `6caaee842e94`, Release |
| Rebuilt source closure | 11 unchanged dependencies, five new mathematical modules, one full audit module |
| Literal export axiom reports | 100/100 present 和 accepted |
| Exhaustive theorem-constant audit | 1,505 theorem constants |
| Exhaustive safe-definition audit | 239 safe definitions |
| Compiled mathematical origins | 15 with declarations, plus the explicit empty compatibility import |
| Allowed axiom union | `propext`, `Classical.choice`, `Quot.sound` |

Every substantive compiler attempt is retained under `development/`, including six failed attempts, their exact source snapshots, stdout/stderr, commands, timestamps, hashes, 和 exit codes. No failed attempt is substituted for the final checked source. The completed development compiler objects were hashed before being emptied to recover scratch space; that cleanup is recorded in `development/completed-objects-reclaimed.json`. The fresh final build uses a different directory.

Narrow direct ordinary-integer controls independently evaluated 1,999,008 seed/case visits across the exact parameter rows in `controls_parameters.json`. These cover zero markers, one-digit width, both parity widths, nonzero-leading/zero-trailing semantics, two selected blocks, 和 a complete block of two pairs. At `L=6,r=2`, the exact count is `899910`; the explicitly incorrect per-pair exclusion formula gives `882090`. For the `r=1` cases, the controls also check the direct one-positive-step upper count. The source, parameters, complete rows, raw stdout/stderr, 和 status/hashes are retained in `controls.py` 和 `verification/finite-controls*`. These controls supplement the unbounded-parameter Lean proof.

### Reproduction

From the repository root, with fresh output directories:

```bash
python proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --repo-root /absolute/path/to/repository \
  --build-dir /absolute/path/to/new-private-build \
  --report-dir /absolute/path/to/new-report-directory
```

The verifier checks every dependency hash 和 every frozen new-source hash, retains the complete command/log/source receipt, requires all 100 literal axiom reports, 和 checks the exhaustive module-origin summaries. The exact original full-gate command is also recorded in `AUTHOR_RESULT.json`.

The finite controls run with Python 3 和 its standard library:

```bash
python proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/controls.py
```

The parent owns publication 和 Git operations. The root-created checkpoint carriers 和 independent review files are excluded from the author's final manifest so that their separate evidence can be added without changing the frozen author packet.
