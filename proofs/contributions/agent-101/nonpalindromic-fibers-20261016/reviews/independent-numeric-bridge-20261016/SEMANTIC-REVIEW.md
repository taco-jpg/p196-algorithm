# Independent review: initial-palindrome and nonpalindrome numeric fibers

## Result: PASS

The fresh seven-module source closure, all 32 public source declarations,
and all 19 independent boundary theorems passed with
`--trust=0 -j1 -DElab.async=false`. A further environment-level audit passed
for all 48 compiled logical declarations in the two reviewed modules
(44 theorems and 4 definitions). Their axiom union is exactly
`propext`, `Classical.choice`, and `Quot.sound`. All source hashes remained
unchanged after both checks. No mathematical or scope defect was found.

Lean also generated 14 declarations explicitly marked unsafe for native
compiler implementation stages and specialized list-filter loops. They are
listed separately, are not public mathematical exports, and appear in no
audited logical declaration's axiom dependencies. See the audit-classifier
note below; no unsafe mathematical export is permitted by the verifier.

## Reviewer independence and frozen sources

The reviewer is Agent #101's numeric-bridge subagent. The reviewer did not
author either reviewed module: `Agent101PalindromeFibers.lean` was authored
by the research-inventory subagent; `Agent101NonpalindromicFibers.lean` was
authored by the parent agent. The reviewer **did** author the previously
checked `Agent101NumericFibers.lean` dependency. This is an independent
review of the two new mathematical modules, not a claim of independent
authorship for the entire dependency closure.

Frozen source hashes:

| Module | SHA-256 |
|---|---|
| Agent101PalindromeFibers | `27ebcd2a7b790d87e45f19e51d0d7e2ff977f297742936503b9552026e3ea633` |
| Agent101NonpalindromicFibers | `22e33259394d275175a02a90a887e3fa49af488a3931e3518fc99899a59154e5` |

Both sources are read-only throughout the review. Exact copies of the
seven-module dependency closure are rebuilt in a new temporary directory;
the build's `LEAN_PATH` contains that directory alone, so no previously
compiled project objects can satisfy a dependency.

## Semantic findings

### Ordinary decimal palindromicity

`palindrome_natValue_iff_reverse` assumes `canonicalDigits ds` and reuses
the original `DecimalDigits.palindrome_value_iff`. This is the actual
`Lychrel196.reverse10` predicate on the ordinary integer `natValue ds`.
It is not a replacement list-palindrome predicate with unproved numerical
meaning. In particular, zero low digits remain permitted, while the high
digit must be positive. The existing decimal reversal correctly discards
leading zeros after reversal.

Reflection symmetry makes `digitPairSums ds` equal to twice each original
digit. The parity and halving lemmas therefore give a necessary evenness
condition and determine the only possible palindromic source. Their proofs
range over finite lists and do not count the unconstrained tails of decimal
digit functions.

### Sufficiency and canonical leading digit

The reverse direction does not merely halve a putative profile and assume
it is a numeral. Positive `profileCount` is converted through the already
proved exact enumeration length into an actual canonical realization.
`canonical_half_pairSums` shows that halving its even mirrored sums preserves
digit bounds and a positive highest digit: a positive even outer sum is at
least two. This is precisely the condition that prevents an invalid or
zero-leading half-profile from being admitted.

The resulting `palindrome_mem_numericFiber_iff` needs no additional profile
validity premise. Positivity of the exact multiplicity and evenness of every
coefficient are the complete existence conditions. The equivalence also
specifies the unique ordinary integer as the value of the halved profile.

### Empty, singleton, and impossible profiles

For the empty profile, the all-even predicate is vacuous but the exact
multiplicity is zero, so the indicator is zero. A singleton center zero
also has zero multiplicity: zero is not counted as a positive canonical
numeral. A positive even center at most 18 has its unique one-digit source,
which is a palindrome; odd centers and centers above 18 have no source.

An outer coefficient zero has no allowed leading-positive digit split,
even when other coefficients are positive. A coefficient above 18 has no
bounded digit split. Those cases again have zero exact multiplicity and do
not produce a spurious half-profile palindrome. Conversely, internal zero
coefficients and a zero center are valid when the outer profile is positive;
the proofs preserve these cases rather than excluding all zeros.

### Indicator, finite filtering, and subtraction

`palindromePossible` is a computable test over the finite coefficient list
and exact profile count. It does not decide an unbounded existential over
ordinary integers. Its Boolean form is proved equivalent to the precise
existence conditions in the generic palindrome theorem.

Both filtered numerical lists inherit `Nodup`. The palindrome list is proved
to be either empty or the singleton containing the half-profile value.
The partition theorem is an exact sum of the two filtered lengths. Thus
subtracting `palindromeIndicator` from `profileCount` gives the exact
nonpalindrome count. The independent review additionally derives
`palindromeIndicator h c ≤ profileCount h c` directly from the partition,
so natural-number truncating subtraction cannot hide an underflow error.
It also derives the independent bound `palindromeIndicator ≤ 1`.

### Numerical membership and scope

The numerical specification of the nonpalindrome list retains the original
fixed input decimal width and the coefficient bound at most 18 required
for numerical profile recovery. It does not claim a cross-width inverse
characterization. Filtering excludes initial palindromes only; it does not
assert anything about the next or subsequent iterate. The independent
review checks the concrete example 20: it belongs to the initial
nonpalindrome fiber for half-profile `[2]`, while its next value 22 is a
palindrome.

No semantic defect was found in either frozen module. Acceptance of the
formal compilation and audit is determined by the machine-readable results
in `verification.json` and `compiled-audit-verification.json`.

## Reproducible independent checks

Run `verify.py`, then `audit_compiled.py`, using the pinned Lean 4.19.0
runtime recorded in the manifests. Every compilation uses
`--trust=0 -j1 -DElab.async=false`.

The first script rebuilds all seven original dependency modules from exact
source copies, checks independent boundary theorems, and audits all 32
public source declarations from the two reviewed modules. The second script
enumerates their actual compiled environment declarations, rejects any
custom logical axiom, and audits every safe compiled theorem, definition,
and opaque declaration, including generated logical declarations not named
in source text. It separately records Lean-flagged unsafe implementation
stages and verifies that every public mathematical source declaration is
included in the logical audit.

The independent boundary module covers empty profiles, zero singleton,
smallest and largest positive single digits, odd and oversized centers,
zero and oversized outer coefficients, valid internal/central zeros,
ordinary trailing-zero reversal, an odd outer profile with no palindrome,
the unique `[18]` palindrome, non-underflow subtraction, and the initial-only
scope counterexample. Concrete examples use kernel-checked `decide`; there
is no native evaluator proof shortcut.

Command arguments, exact source/compiler hashes, exit codes, elapsed times,
raw logs, and source-unchanged checks are retained in this folder. Runtime
copies and compiled objects remain only in the temporary build directory.

## Audit-classifier correction retained as evidence

The first environment-level audit intentionally rejected every declaration
of Lean's `axiomInfo` form. That was too broad: the compiler represents its
unsafe specialized implementation of the list-filter loop using an unsafe
implementation axiom. This caused an audit failure despite the successful
kernel check and standard-only public mathematical axiom dependencies.
The rejected audit source and raw log are retained in `attempts/`.

The corrected audit reads Lean's `ConstantInfo.isUnsafe` flag. It records
those implementation declarations separately and restricts their names to
compiler stage suffixes and the two generated filter-loop specializations.
It rejects every safe logical axiom, audits every safe logical declaration,
and requires every source-level public export to occur in that audit. This
classification does not permit an unsafe public theorem or an additional
logical axiom dependency. No reviewed mathematical source was changed.
