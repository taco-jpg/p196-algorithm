# Read-only inventory: palindromic realizations and exact safe profile counts

Agent 101 research/enumeration subagent, 2026-10-16.

## Conclusion and evidence boundary

I did not find an existing general theorem that characterizes the unique
initial palindromic realization of an arbitrary complete decimal digit-pair
profile, or an exact cardinality theorem for its complete safe natural-number
fiber. The existing decimal foundation supplies the required palindrome,
reversal, and value-injectivity interfaces. The completed Agent101 numeric
module supplies the complete finite fiber and its exact length.

This is a bounded source-search conclusion, not a claim of universal
originality. I searched current local sources, inventoried all 55 locally
observed branch/ref tips, read their 1,447 locally available distinct Lean
blobs, and retrieved six particularly relevant missing blobs through
read-only GitHub GETs. No current flat `proofs/*.lean` blob from the pinned
main tip was missing. Some archived versions and other branch-only files
remain unavailable locally; these are explicitly recorded below.

No new theorem or mathematical proof was authored for this investigation.
Live ownership/claim updates remain the parent agent's responsibility.

## Directly reusable foundation

The numeric module already imports `Lychrel196Research`. Its corresponding
flat source is:

```text
proofs/Lychrel196Research__c696e0ea3db39d92.lean
SHA-256 f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c
```

The same relevant interfaces are also present in the canonical continuation
source:

```text
proofs/LychrelDigitSums__75febdc48f0ca802.lean
SHA-256 ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57
```

Use the foundation already imported by the numeric module; these two source
files are not two independent namespaces to import together.

### Actual palindrome and reversal semantics

The definitions are `Lychrel196.Palindrome n := reverse10 n = n` and
`Lychrel196.step n := n + reverse10 n`. A decidable instance for
`Palindrome n` is present. The reusable exact interfaces in namespace
`DecimalDigits` are:

```lean
theorem reverse10_value (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.reverse10 (value d L) = value (reflected d L) L

theorem palindrome_value_iff (d : Nat → Nat) (L : Nat)
    (hd : ∀ i, i < L → d i ≤ 9)
    (hlead : L = 0 ∨ 0 < d (L - 1)) :
    Lychrel196.Palindrome (value d L) ↔
      ∀ i, i < L → d i = d (L - 1 - i)

theorem value_injective (a b : Nat → Nat) (L : Nat)
    (ha : ∀ i, i < L → a i ≤ 9)
    (hb : ∀ i, i < L → b i ≤ 9)
    (heq : value a L = value b L) :
    ∀ i, i < L → a i = b i
```

These declarations occur at lines 730, 771, and 751 respectively in
`Lychrel196Research__c696e0ea3db39d92.lean` (739, 780, and 760 in the
continuation file). `value_congr` and `canonical_exists` are also present.

The foundation furthermore contains:

```lean
ReverseAddInverse.same_width_step_eq_iff_pair_sums
    (n m : Nat) (d e : Nat → Nat) (L : Nat)
    (hn : Canonical n d L) (hm : Canonical m e L) :
    Lychrel196.step n = Lychrel196.step m ↔
      ∀ i, i < L → columnSum d L i = columnSum e L i
```

This occurs at line 3824 in the research source and line 3833 in the
continuation source. It identifies a profile at a fixed input width; it
does not identify the individual original digit split. The stronger
`ReverseAddInverse.symmetric_value_injective` works for symmetric
coefficient functions bounded by 18, without positivity or center parity.

### Existing next-step palindrome classification

`DecimalDigits.PalindromePredecessor n` is the existence of a canonical
representation whose column sums are either all at most 9, or have outer
coefficient 11 and all coefficients in `{0,11}`. The exact natural-number
bridge is:

```lean
theorem palindromePredecessor_iff (n : Nat) (hn : 0 < n) :
  PalindromePredecessor n ↔ Lychrel196.Palindrome (Lychrel196.step n)
```

It occurs at line 944 in the research source. `step_palindrome_iff` gives
the equivalent criterion directly for a canonical digit function.
These already settle the output-palindrome classification; the proposed
next scope should reuse them if an explicit coefficient criterion for
the safe output condition is needed.

## Existing Agent101 list/numeric bridge

Observed source:

```text
proofs/Agent101NumericFibers.lean
SHA-256 bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97
```

The following existing interfaces connect the foundation to finite lists:

```lean
canonicalDigits_iff (ds : List Nat) :
  canonicalDigits ds ↔ Canonical (natValue ds) (digitFn ds) ds.length

natValue_injective_same_length (a b : List Nat)
    (ha : digitsBounded a) (hb : digitsBounded b)
    (hlen : a.length = b.length) (hv : natValue a = natValue b) : a = b

natValue_injective_canonical (a b : List Nat)
    (ha : canonicalDigits a) (hb : canonicalDigits b)
    (hv : natValue a = natValue b) : a = b

step_natValue (ds : List Nat) (hd : canonicalDigits ds) :
  Lychrel196.step (natValue ds) = natValue (digitPairSums ds)
```

`digitFn_getElem`, `digitFn_last`, `bounded_digitFn_iff`,
`canonicalDigits_nonempty`, `canonical_to_list`, `natValue_positive`, and
`same_width_step_eq_iff_digitPairSums` are present as well.

The complete natural-number fiber interface is:

```lean
mem_numericFiber (h : List Nat) (c : Option Nat) (n : Nat)
    (hq : ∀ s ∈ coefficientWord h c, s ≤ 18) :
  n ∈ numericFiber h c ↔
    decimalWidth n (coefficientWord h c).length ∧
    Lychrel196.step n = natValue (coefficientWord h c)

numericFiber_nodup (h : List Nat) (c : Option Nat) :
  (numericFiber h c).Nodup

length_numericFiber (h : List Nat) (c : Option Nat) :
  (numericFiber h c).length = profileCount h c
```

Here `decimalWidth n L` is `0 < L ∧ 10^(L-1) ≤ n ∧ n < 10^L`.
`mem_numericFiber_digits` supplies the equivalent canonical-list witness
without the coefficient-bound hypothesis. The natural-number full-fiber
equivalence above retains the bound hypothesis and the fixed input width.

## Existing safe-set results and their exact scope

The established predicate is:

```lean
namespace Agent13SafeFamily
def Safe (n : Nat) : Prop :=
  0 < n ∧ ¬ Lychrel196.Palindrome n ∧
    ¬ Lychrel196.Palindrome (Lychrel196.step n)
```

Source and identity:

```text
proofs/Family__10d4491afcae6543.lean
SHA-256 0fb8b09408cc0fa6283c2f3161b62ab915fefa7b6079353a987784d72563b007
```

The full safe incoming fiber already exists as a `Finset Nat`:

```lean
namespace Agent13SafeWeights
def safeFiber (y : Nat) : Finset Nat :=
  (Finset.range (y + 1)).filter (fun n => Safe n ∧ step n = y)

theorem mem_safeFiber_iff (n y : Nat) :
  n ∈ safeFiber y ↔ Safe n ∧ step n = y

theorem full_safe_fiber_finite (y : Nat) :
  Set.Finite {n | Safe n ∧ step n = y}
```

Source and identity:

```text
proofs/Weights__d5b32739b09a2328.lean
SHA-256 35ae4bdca071966997571abac1d0145441d9c4835189ef3b3aed2faad6651982
```

That module proves weighted lower bounds and absence of a uniform incoming
weight multiplier. It does not state a general exact cardinality formula
for `safeFiber`.

`Agent13SafeFamily.safe_predecessor_family` provides an injective
`Fin (9 * 10^(m-2)) → Nat` family at the target
`10^(2*m) + 99*10^(m-1) - 1` for `2 ≤ m`. Its source explicitly says this
counts the constructed family, not necessarily the whole fiber:

```text
proofs/Counting__6c2b07b0a2bfd92a.lean
SHA-256 a430efc92f39ff538d4f54b27435676f0c61697ba3ff0e75dbe8565bda8642e0
```

`predecessor_complete` is completeness within that prescribed family of
high words. It is not full completeness among all predecessors of the
target. `safe_fibers_unbounded` is an arbitrarily large-family result.

### Scope conditions for the proposed subtraction

The existing definitions impose the following requirements on any next
claim:

- Removing initial palindromes alone gives the established `Safe` predicate
  only when the common output is nonpalindromic. If the common output is
  palindromic, every member fails `Safe` and the safe count is zero.
- A fixed complete profile supplies a fiber at its specified **input
  width**. The old `safeFiber y` ranges over all input widths; equality with
  that whole set needs the appropriate width accounting.
- `coefficientWord h c` is symmetric as a coefficient list, but its entries
  can exceed 9. This symmetry alone does not imply that its evaluated
  output integer is palindromic. `palindrome_value_iff` has the digit bound
  `≤ 9`, whereas profile coefficients have the bound `≤ 18`.
- The zero number satisfies the foundational palindrome equality, but
  canonical lists and `decimalWidth` exclude zero. These conventions must
  remain consistent in the indicator for a removed initial palindrome.

These are semantic boundaries of existing definitions, not new theorem
claims from this investigation.

## Nearby results that are not the requested general endpoint

`proofs/TemplateStep__a3e3f4a14e61d253.lean` has:

```lean
Agent109.palindrome_iff (m : Nat) :
  Agent109.Palindrome m ↔ (Agent109.digits m).reverse = Agent109.digits m
```

SHA-256:
`76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed`.
It is a useful existing list-palindrome theorem, but the file defines its
own `Agent109.reverse10`, `Palindrome`, and `step`. It is not directly a
theorem about `Lychrel196.Palindrome` and should not be silently substituted
for that namespace. The already imported `DecimalDigits` interface avoids
this extra semantic transport obligation.

The only general uniqueness-named palindrome theorem selected from the
accessible declaration search was `first_positive_unique` in the high-base
first-hit development. It concerns uniqueness of the first hit time for a
fixed orbit, not uniqueness of a palindromic source in an inverse fiber.

The written probability result already performs a different initial-
palindrome subtraction, aggregated over an entire input width:

```text
proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/
proofs/research/main_existence_attempt/return_pass/probability/PROBABILITY_RESULT.md
SHA-256 395cd5eaf325842f5aaeb68490298247f607f609f253d6b2dc2d7af002b34e97
```

Section 4 gives the exact whole-width next-palindrome counts
`N_(2m) = 45*55^(m-1) + 8*9^(m-1)` and
`N_(2m+1) = 225*55^(m-1) + 8*9^(m-1)` for `m ≥ 1`, then subtracts
`4*5^(ceil(L/2)-1)` to require a first hit at step one. This is an existing
written/finite-controlled whole-width result. It is not the general
fixed-profile safe-fiber theorem under consideration, but the whole-width
formula should not be claimed again as a new result.

## Relevant observed branch sources

Six missing source blobs were retrieved using GitHub GET, with their Git
blob SHA-1 independently recomputed from the returned bytes. No Git fetch,
checkout, commit, or remote write was performed by this supplement.

| Source at observed tip | Interface examined | Finding |
|---|---|---|
| `proofs/Agent2OverflowActual.lean` at `542894ba6f933c4b6656ed58389b64aad969b925` | `ActualOverflowFiber` | Canonical pair-word fiber of `Agent8.stepWord`, coefficients at most 18. |
| `proofs/contributions/agent-3/finite-horizon-overflow-20261016/FamilyCardinality.lean` at `4bf7a2147b02502ee1e5c2151c83bb33db950f88` | `familyWords_exact` | Exact `2^m` family of `CanonicalPair` words; no original-number palindrome filter. |
| `proofs/coordination/patches/agent9-nooverflow-fibonacci-20261016/InverseFibers.lean` at `0be52bafd3478077b96ec1f8e702b2cf58dec8ba` | `Local`, `local_unique`, `inverseCount_bound` | Uniqueness of a coefficient label for specified carry states and target symbol, not a palindromic natural-number source. |
| Same Agent9 directory, `WordBridge.lean` | `Realizes`, `mem_preimages_iff_realizes` | Exact coefficient-word/path bridge with input coefficients below 19. |
| `proofs/coordination/submissions/agent-415/actual-inverse-column/Agent415ActualInverseColumn.lean` | `actual_inverse_columns` | Guarded periodic arithmetic-column correspondence, not original-digit multiplicity. |
| Same Agent415 directory, `Agent415ActualRoot.lean` | `actual_root_eight`, `actual_root_path` | Root-state/path consequences for those arithmetic columns. |

The full source paths, Git blob IDs, SHA-256 values, declaration names, and
selected keyword lines are preserved in `palindrome-github-read.json`.
Exact bytes are under `readonly-branch-sources/`. None of these six source
files contains a declaration of the general palindrome/safe-count endpoint
being sought. They were read for scope, not independently recompiled here.

## Search reproducibility and limits

- `palindrome-search-refs.json`: 55 observed refs and exact tips. Main was
  pinned at `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
- `palindrome-search-lean-blobs.json`: all 3,782 distinct Lean blob IDs at
  those tips, with paths and compact references to the ref table.
- `palindrome-local-declarations.json`: local palindrome-related declaration
  inventory, deduplicated by source SHA-256.
- `palindrome-branch-declarations.json`: relevant declarations from the
  1,447 locally available branch blobs.
- `palindrome-branch-keyword-hits.json` and `palindrome-written-search.log`:
  targeted searches for uniqueness, realization, counting, and safe fibers.
- `palindrome-missing-branch-blobs.json`: the 2,335 blobs initially absent
  from the partial clone. Of these, 302 belong to main's archived paths;
  no flat main Lean source was missing. Six relevant branch sources were
  subsequently read through the GitHub API as recorded above.
- `palindrome-reusable-source-hashes.json`: all local reusable source
  identities quoted in this report.

The branch object reader used `GIT_NO_LAZY_FETCH=1`, so missing historical
objects were recorded rather than automatically fetched. The absent
objects, including many generated certificate rows and historical versions,
were not silently included in the content-search coverage. No assertion is
made about unobserved future remote tips or declarations hidden in those
unread historical objects.
