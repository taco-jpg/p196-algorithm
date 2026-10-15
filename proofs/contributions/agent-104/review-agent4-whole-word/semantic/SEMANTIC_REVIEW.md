# Independent semantic review of Agent 4's whole-word bridge

Source pin: `4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7`.
Reviewer: Agent 104, semantic specialist. This is independent replication and
scope review of Agent 4's result, including possible overlap with Agent 8's
period work. It asserts no new ownership, originality, or human peer review.

**Semantic finding:** no mathematical statement mismatch, circular premise,
missing positivity condition, or invalid carry-overlap restriction was found
in the six exports. Their implications have the ordinary reverse-and-add
interpretation stated below. **Independent formal acceptance remains pending**
the execution specialist's completed fresh five-module Lean chain and
transitive axiom audit. The semantic specialist ran no Lean compiler.
Historical author logs are not substituted for that gate.

The two concrete illustrations are bounded Python diagnostics at this
checkpoint. `ReviewScopeWitnesses.lean` contains complete attempted
kernel-checkable statements for them, with no `sorry` or native evaluation,
but its frozen source is **WIP until actually compiled and audited**.

## Source and dependency identity

The exact local import closure has five modules. `source-manifest.json`
records original repository paths, Git blob IDs, complete SHA-256 values,
sizes, and imports. The hashes equal the author's historical integration
manifest; no original source was edited.

| Module | SHA-256 |
|---|---|
| LychrelDigitSums | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| PrefixModel | `8ea1199dbd413869efd8e48955119361cb44c6d7cc69722d276cb1c825da37b0` |
| SaturationCertificate | `7ce611b42425dcad50527788d95b9bfa648883ed11561df3ebbb6438a1728791` |
| SaturationTheorem | `9a7f65a82d611bf24f2661de0715d0a70f69da0b5a51d3ad00725cde37f5b2eb` |
| WholeWordBridge | `483fc3084a9e9b796f9fd56e9640962839417386a30a2c803c9dd9b09ffa5b87` |

`WholeWordBridge` imports `LychrelDigitSums` and `SaturationTheorem`; the latter
imports `SaturationCertificate`, which imports `PrefixModel`. The remaining
imports are official Lean 4.19.0 `Std` and `Lean.Elab.Tactic.Omega`. Static
inspection found no executable `sorry`, `admit`, custom axiom,
`native_decide`, `Lean.ofReduceBool`, unsafe declaration, or alternate
implementation in these sources. This textual check does not replace the
execution specialist's compiled dependency audit. The author's historical
audit reports only `propext` and `Quot.sound` for all six bridge endpoints.

Applicable repository instructions were read: `proofs/PUBLICATION_POLICY.md`,
the root and proofs READMEs, and `proofs/contributions/README.md`. No applicable
`AGENTS.md` was found in this checkout or its workspace ancestry. The review
respects the separation of conditional theorem, written review, diagnostic,
and completed formal verification.

## Meaning of the exact state

In the foundation, `value d L` reads the first `L` least-significant-first
digits. `Canonical n d L` means `L>0`, each in-range digit is at most nine,
the leading digit is positive, and `value d L=n`. It therefore precludes
leading-zero padding and represents a positive integer. Values of `d`
outside the width are unconstrained but irrelevant here.

`columnSum d L i = d i + d (L-1-i)` is a mirrored **sum of two digits**, not
an input or output digit. The bridge's `prefix3 q` is `(q 0,q 1,q 2)`.
`Admissible L q` asserts positive width, `q 0>0`, coefficients at most 18,
reflection symmetry within the width, and an even coefficient at an odd
word's self-reflected center. These are realizable finite-word conditions:
the foundation's `valid_word_realizable` supplies a canonical positive integer
with those column sums. They do not assume the conclusion being reviewed.

`carry q 0=0` and `carry q (i+1)=(q i+carry q i)/10`; all in-range carries
are zero or one. The normalized digits are the remainders. With no final
carry the width stays `L`; with final carry one it becomes `L+1` and the
new leading digit is one. `nextColumns` folds these actual normalized
digits at the selected width. Thus the reflected pairing shifts by one
column in the overflow branch.

`iterPairs` starts at `(L,q)` at time zero and applies this normalization
once per successor. `Lychrel196.orbit` likewise starts at the input at time
zero and applies `n + reverse10 n` once per successor; reversal discards
numerical leading zeros in the ordinary way. The foundation's
`representation_next` and `iterPairs_representation` align these two time
indices. There is no extra hidden normalization step. Both dynamics continue
after a palindrome.

## Six-export audit

| Export | Exact content and review |
|---|---|
| `nextColumns_prefix3` | For `L>=3`, symmetric in-range `q<=18`, one application of `advance (prefix3 q) (carry q (L-3))` equals the actual next prefix paired with final carry. It needs neither positivity nor center evenness because it is an algebraic projection; these conditions enter later through admissibility. |
| `iterPairs_width_ge` | For arbitrary `q,L,n`, the defined width is at least `L`. This unconditional statement follows directly because `nextWidth` selects `L` or `L+1`; its comment's word “canonical” is an interpretation valid when admissibility/representation is subsequently supplied. |
| `actual_width_overflow_identity` | Under initial admissibility, the width at time `n` is exactly `L + sum_{i=0}^{n-1} overflowAt i`. Admissibility preservation gives the bit bound needed to identify the branch increment with the final carry. No off-by-one error was found. |
| `iterPairs_prefix_evolution` | Under initial admissibility and `L>=3`, each actual step projects using the actual inward carry at its current width minus three. Admissibility preservation and width monotonicity make every needed index valid. |
| `actual_saturated_prefix_return` | If the first three **column sums** return at time `n`, and `2*width_n=2*L+n`, then `n%8=0`. The transition, carry-bit, valid-prefix and total-overflow premises are derived from the actual whole word, not postulated as a separate approximate orbit. |
| `numeric_saturated_prefix_obstruction` | Given a canonical initial integer of width at least three, supplies canonical digits and width of the ordinary time-`P` endpoint, and proves that returned column-sum prefix plus `2*W=2*L+P` implies `P%8=0`. It uses the endpoint from `iterPairs_representation`. |

### Carry indices and overlapping widths

Let `C_j=carry q j`, `(a,b,c)=(q 0,q 1,q 2)`, and `e=C_(L-3)`.
Symmetry gives, in order,

`C_(L-2)=(c+e)/10`, `C_(L-1)=(b+C_(L-2))/10`,
`C_L=(a+C_(L-1))/10`.

The low carries are `C_1=a/10` and `C_2=(b+C_1)/10`. In the no-overflow
branch the three low digits pair with the corresponding high digits. In
the overflow branch the low digit at zero pairs with the appended one;
positions one and two pair with the old high digits from positions zero
and one. These are exactly the two branches of `advance`.

The written `prefix_growth/README.md` assumes width at least six while
describing separated ends. The bridge's stronger `L>=3` domain is sound:
it never selects the inward carry independently of the word. At `L=3`
that carry is `C_0=0`; at `L=4` it is `C_1`; at `L=5` it is `C_2`.
Shared columns are therefore read with their actual shared carries.
Reflection arithmetic is used only at indices zero through two, all less
than `L`. No separation hypothesis is secretly needed. The exhaustive
short-width controls below specifically include these overlaps.

### Width saturation and clock telescoping

The finite certificate covers every `a=1..18`, `b,c=0..18` and `e=0..1`.
For each edge with overflow `g`, it asserts

`82*g + V(next) <= 41 + V(current)`,

and asserts an increment by one modulo eight of a clock whenever equality
holds. Eighteen `decide +kernel` rows cover the entire finite domain. Their
generator is not a trusted inference rule.

On a returned prefix the potentials cancel, giving `2*O<=n` where `O`
is the total overflow count. In the bridge, width telescoping and the
separate hypothesis `2*width_n=2*L+n` give `2*O=n` exactly. There is no
natural-subtraction truncation hidden in that equation. The proof
`tight_clock_telescope` uses nonnegative slack and total equality to show
each step is tight, then sums the clock increments. Prefix return also
returns the clock, so `8` divides `n`.

Here “saturated” means equality in the half-growth bound **for a closed
prefix path**. It does not mean a width increase at every step, nor a
general half-growth bound for arbitrary nonclosed orbit segments. The
condition is aggregate over the selected segment. The theorem neither
assumes nor proves indefinite repetition of that segment.

Time zero is allowed and correctly yields `0%8=0`. A positive-time
hypothesis is unnecessary for divisibility. Initial positivity is already
in admissibility, or in the canonical representation for the numeric
endpoint. No initial or intermediate nonpalindromicity hypothesis is used.

### Existential canonical endpoint

The numeric endpoint's order is `exists e W, Canonical (...) e W AND
(prefix return -> width equality -> divisibility)`. It is not literally
a theorem quantified over every supplied endpoint representation. However,
the proof fixes `W` to the actual iterated width and obtains `e` from the
ordinary orbit representation theorem before introducing either antecedent.
It cannot choose a padded width or unrelated sequence to evade them.
Since `W>=L>=3`, the endpoint prefix reads only actual in-range digits.

Mathematically, ordinary canonical digits and their width are unique;
out-of-range tails do not change this prefix. A client wanting a Lean
statement with an arbitrary separately supplied canonical endpoint must
either use the existing existential witness or add the corresponding
representation-uniqueness corollary. That interface convenience is not
presently one of the six exports and must not be silently ascribed to it.

## Bounded diagnostics and concrete scope illustrations

`exact_diagnostics.py` uses exact Python integers, a direct decimal string
reversal, independently written carry normalization, and the displayed
`advance` equations. It has no external packages, randomness, concurrency,
or Lean invocation. The complete emitted results, counts and selected full
traces are in `exact-diagnostics.json`; stdout is retained separately.

| Diagnostic scope | Cases | Result |
|---|---:|---|
| Every admissible symmetric word of width 3,4,5,6,7,8 | 198,882 words | No discrepancy in projection, actual carry, overflow width, canonical integer realization, or literal decimal normalization. |
| Every admissible initial word of width 3,4,5,6, each through 24 steps | 10,440 starts; 250,560 steps | No discrepancy in literal numeric orbit, prefix update, width telescoping, closed-prefix bounds, or stated saturation implication. |

These are diagnostics, not a replacement for a universal proof. The loop
enumerates all admitted words within the specified finite widths; it does
not claim to enumerate every abstract three-column path or every integer
representation of a given word.

Two diagnostic illustrations were isolated:

| Initial integer | Time | Endpoint | Widths | Returned prefix | Relevant arithmetic |
|---:|---:|---:|---|---|---|
| 89870 | 8 | 179745797 | 5 to 9 | `(8,16,16)` | `2*9=2*5+8`, so positive saturated return is diagnostically nonvacuous. |
| 770 | 7 | 176176 | 3 to 6 | `(7,14,7)` | `2*6<2*3+7`, while `7%8!=0`; dropping saturation would overstate the result. |

The latter trajectory passes through the palindrome 44044 at time five,
which also illustrates the theorem's intentional convention of continuing
reverse-and-add after palindromes. The proposed Lean witness module proves
only the displayed orbit/canonical/prefix/width assertions, not that extra
palindrome observation. Until the witness module actually compiles, both
rows retain diagnostic status.

Pinned-main exact-token searches found no occurrences of `89870`,
`179745797`, or `176176`. The token `770` occurs in unrelated counts,
identifiers, and discussion of a remaining three-column prefix branch; no
matching seven-step witness statement was located. Commands, scope, counts
and interpretation are retained in `exact-prior-occurrences.json` and
`publication-selection.json`. This is a bounded repository-location check,
not a literature or novelty claim. All illustrations are offered as review
replication and scope checks, not new major theorems.

## Remaining gates and scope limits

1. Complete the fresh Lean 4.19.0 import chain and transitive audit of all six
   bridge exports. The semantic review does not itself satisfy this gate.
2. Compile and audit the frozen `ReviewScopeWitnesses.lean` before promoting
   either finite illustration to checked formal status. Preserve any failed
   attempt and revise only with coordinated source pinning.
3. Applying the result to a particular integer and time still requires its
   prefix-return and saturated-width premises. For 196 those premises are
   not supplied by this review.
4. The full complementary-quotient period-at-least-42 theorem additionally
   needs its phase, even-overflow, and modulo-nine hypotheses. This bridge
   alone does not establish those hypotheses for every ordinary orbit.
5. No persistent interface, infinite orbit avoiding palindromes, exclusion
   of all longer nonsaturated returns, or resolution of P196 follows.

Reproduction of diagnostic evidence, from this directory:

```text
python snapshot_sources.py
python exact_diagnostics.py > exact-diagnostics.log
python search_prior_witnesses.py > exact-prior-occurrences.log
```

The source snapshots are reproducible duplicates of pinned tracked files;
publication can omit them while retaining their exact source manifest.
Large raw grep results likewise repeat tracked source text and may be omitted
as operational source-location metadata. They contain no unique diagnostic
or mathematical result. The finite diagnostic script/results and authored
review/witness source must be retained.
