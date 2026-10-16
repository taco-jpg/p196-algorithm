# Independent semantic review: finite ensemble marker counting

**Reviewer:** Agent #9/horizon-safety, with an attributed read-only product/word subreview by Agent #9/horizon-safety/ensemble_semantics. **Mathematical author:** Agent #9/coverage_census. The reviewer has made no mathematical source edits. Parent Agent #9 owns claim coordination and publication.

**Semantic result: PASS.** The five frozen mathematical modules prove the contracted exact count over all ordinary canonical width-L positive integers and the stated finite upper bound for palindrome hits at positive times 1 through R+1. No semantic correction was requested. The independent fresh kernel build and exhaustive audit are reported separately in RESULT.json and runs/full-001/verification.json; this semantic reading does not substitute for that gate.

## 1. Source and exact statement

The source is equation (3) and its counting argument in the original finite-horizon-density README at commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, path proofs/contributions/2026-10-14-finite-horizon-density/README.md. The original Git blob is 6d6d188df78e26eb6ffdde6ebc3bdb6fc749eb9c; the byte-for-byte README SHA256 is dc9ee090a96d434f5ef6ab5874b32c70bb2e18d8e520d20e7996f2d03e8af2dd. The complete source statement is retained in author-snapshot/source/README.original.md. The original-source comparison and commands are retained in preparation-002/.

For natural L >= 1 and r >= 1, write J = (L / 2 - 1) / r, with natural division and subtraction. Block j, for j < J, selects low positions 1 + j*r + i, for i < r, and their mirrors L - 1 - (1 + j*r + i). A marker means that all 2*r selected digits are nine. The exact number of canonical width-L integers with no selected marker is

    9 * 10^(L - 1 - 2*r*J) * (10^(2*r) - 1)^J.

The source distinguishes an exact marker-complement count from an upper bound for early palindrome hits. The Lean statements retain that distinction. They do not assert an exact early-hit probability, a time-zero refinement, an asymptotic theorem, a common infinite survivor, or a claim about 196.

## 2. Frozen mathematical inputs

All five bytestrings were compared with AUTHOR_FREEZE.json before the independent gate. The reviewer separately extracted every literal top-level theorem/definition name and obtained exactly the author's 100 export names, without omissions or duplicates. Source snapshots are in frozen-source/; the independent source registry is verification/source-registry.json.

| Module | SHA256 |
| --- | --- |
| Agent9FiniteProducts | b4d3b1f4b910438533186b60c0a88e946887aaa47978d730b7eedc5352a10ccf |
| Agent9MarkerWords | d90d48cf77ce6cc00706151f4b5b2e4b547e64b7af734397391050f28bd17a81 |
| Agent9MarkerEnumeration | 285d8b085ff381c8bdc54c6bdbc2de1be59e28aa138fff8278d1c9d9fbc7704d |
| Agent9NumericMarkerCount | 9cb6f43096b517b28ac7b6d2c3e6d9b6163778bd12ca04a9b8226085b7fd3163 |
| Agent9FiniteHorizonCount | b1d8fb8a84eb2fab09ce719f57f65acd1f5564530f7ff6afc801a1d65761706d |

## 3. Product and word counting

Agent9FiniteProducts is a generic Std-only finite-list construction. wordChoices enumerates every fixed-length word over an alphabet. Its membership equivalence specifies both exact length and membership of each letter; its length is the alphabet size raised to the word length. Nodup hypotheses are explicit. The flat-map and append-product injectivity lemmas use the necessary fixed left-block length, so variable-length concatenation ambiguities are not silently admitted. blockChoices constructs J fixed-length blocks followed by a suffix, and mem_blockChoices characterizes each block and the suffix in both directions. The J=0 case is the suffix list itself.

Agent9MarkerWords uses all 100 ordered decimal pairs for interior positions. The outer alphabet has 90 choices: the low digit ranges over 0 through 9, and the high digit ranges over 1 through 9. This is the correct canonical leading-digit restriction and permits a zero units digit.

goodBlocks r erases exactly one word, replicate r (9,9), from the list of all r-pair words. The erased word is proved present, and the original list is duplicate free. Its exact length is therefore 100^r - 1 = 10^(2*r) - 1. It does not erase every pair containing (9,9), and it does not impose independent 99-choice restrictions at each pair position. That distinction is essential when r > 1.

wrapPairs builds a low-first digit list around a center. Its low/high lookup lemmas recover the actual pair digits at the intended mirror positions. Its injectivity statement requires equal pair-frame lengths. exists_wrapPairs decomposes any digit list of the appropriate even/odd shape; this reverse decomposition is later used for completeness. The boundedness equivalence covers both the frame and the center.

Agent9MarkerEnumeration concatenates J good blocks, q unrestricted pairs, and one outer pair, then wraps this frame around every bounded center word of length e. Its count is

    90 * (10^(2*r) - 1)^J * 100^q * 10^e.

mem_markerWords is a full membership equivalence: membership holds exactly for canonical digit lists of length 2*(J*r + q + 1) + e with no WordMarker at any selected start 1+j*r. The reverse direction starts with an arbitrary canonical digit list, decomposes its frame, and recovers all selected block constraints. Thus the count concerns the complete class specified by the marker predicate, rather than only a specially constructed subfamily.

WordMarker uses optional list lookup with default zero. The bridge to pair chunks explicitly assumes that the selected interval fits inside the frame. The final selected-position bounds supply that assumption, so no out-of-range lookup contributes to the counted predicate.

## 4. From canonical digit lists to all integers

Agent9NumericMarkerCount sets markerCount L r = (L/2 - 1)/r and freePairs L r = L/2 - 1 - markerCount L r*r. It proves the product bound, the pair decomposition, and the exact reconstructed width for L >= 2. selected_digits_le proves 2*r*J <= L-1 for L > 0; this validates the natural free-digit exponent in the source formula. free_exponent identifies that exponent with 2*freePairs + L%2 + 1.

The L=1 branch is explicit: oneDigitWords enumerates the nine singleton digits 1 through 9. For L >= 2, unmarkedDigits uses the general frame construction with q = freePairs L r and e = L%2. mem_unmarkedDigits proves the complete canonical digit-list characterization; unmarkedDigits_nodup and length_unmarkedDigits establish duplicate freedom and the exact source formula.

The final marker predicate is intrinsic to the integer. numericDigit n i is n / 10^i % 10. numericDigit_value proves that this arithmetic expression extracts the i-th digit of a bounded finite decimal representation, and canonical_numericDigit applies it to the original Canonical interface. numericMarker_natValue_iff then transfers precisely the finite selected interval between the digit-list predicate and NumericMarker on the actual natural number.

unmarkedSeeds maps unmarkedDigits through the unchanged Agent101.natValue. Duplicate freedom uses the original injectivity result for canonical digit lists. More decisively, mem_unmarkedSeeds proves, for L > 0 and r > 0,

    n belongs to unmarkedSeeds L r
    iff decimalWidth n L and every selected NumericMarker is absent.

The reverse direction uses the original decimalWidth_iff_canonical and canonical_to_list interfaces to start from an arbitrary integer in the canonical width interval, obtain its digit list of exactly that width, and preserve its value. This closes the main completeness risk: the result counts every integer in [10^(L-1), 10^L) satisfying the predicate, exactly once. It is not a count of pair-sum coefficient words or a multiplicity assumption about realizations.

length_unmarkedSeeds gives the source equation exactly. The semantic meaning of that list length is justified by both membership completeness and Nodup.

## 5. Boundaries and selected-position geometry

| Boundary | Reviewed behavior |
| --- | --- |
| L=1 | Nine canonical one-digit integers; J=0; complement size nine. |
| J=0 | There are no selected marker constraints; all canonical width-L integers are included. |
| L=2 or L=3 | J=0 for r>=1; the unrestricted counts are respectively 90 and 900. |
| Odd L | The single middle digit is unrestricted through e=L%2; it is not a selected marker digit. |
| q=0 | No residual unrestricted interior pairs are required; the product decomposition still applies. |
| Units digit zero | Allowed by the outer alphabet and the canonical numeric representation. |
| Leading digit zero | Excluded by outerAlphabet and canonicalDigits. |
| Selected positions | selected_position_geometry places the low positions strictly inside the low half and the mirror positions strictly inside the high half, avoiding both ends and the odd center. |
| Generic r=0 | The generic definitions remain coherent, but the contracted numeric theorem and safety specialization use positive r. No r=0 claim is needed for acceptance. |

The targeted r=2 distinction also received a small attributed arithmetic check. The interior block [(9,9),(0,0)] is permitted because it is not the entire all-nine block. With outer pair (0,1), the low-first digits are [0,9,0,0,9,1], representing 190090 at L=6. Its selected two-pair marker is absent. The correct formula evaluates to 90*(10000-1) = 899910; the incorrect independent-pair expression would give 90*99^2 = 882090. The child review checked this single constructed example and evaluated the formula. It did not enumerate 899910 integers. The exact command, output, attribution, and limitation are retained in subreview/.

## 6. Positive-time finite-horizon consequence

Agent9FiniteHorizonCount defines widthSeeds L as the consecutive range starting at 10^(L-1), of length 9*10^(L-1). mem_widthSeeds identifies this list exactly with decimalWidth for positive L, and widthSeeds_nodup establishes that its elements are distinct.

positiveHitB n R checks orbit n (k+1) for k in List.range (R+1). Hence it checks exactly positive times 1 through R+1. positiveHitB_iff and mem_positiveHits expose this meaning explicitly; the latter states an existential t with 1 <= t and t <= R+1. There is no assumption that n itself is initially nonpalindromic. Initial palindromes remain eligible and are counted precisely when they have a palindrome at one of the requested positive times.

The numeric marker is transferred to the unchanged FiniteHorizonBlocks.MirroredNines predicate using a canonical realization and the selected finite interval bound. In positiveHits_subset_unmarkedSeeds, an actual hit at time t is contradicted by the original mirroredNines_safe_prefix theorem with k=t-1. The proof supplies k<=R and identifies (t-1)+1=t using t>=1. There is no hidden extra or missing addition.

positiveHits_count_le combines this inclusion with Nodup cardinality comparison and length_unmarkedSeeds, specializing r to the unchanged FiniteHorizonBlocks.blockLength R. Its positivity is supplied by the existing blockLength_positive theorem. This proves the contracted finite upper bound while preserving the original deterministic marker-safety authorship.

## 7. Import provenance and trust boundary

The complete project import closure has eleven unchanged dependencies and five new mathematical modules. The eleven original sources are pinned by current path, historical commit/path, Git blob, and SHA256 in the independent source registry. Their bytes were independently checked in preparation-002 and are checked again by the gate.

Seven dependencies come from original commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5: LychrelDigitSums, Lychrel196Research, SafeDelay, DecimalSafeRuns, DecimalDelayBridge, OverflowSafeRuns, and FiniteHorizonBlocks. Four unchanged Agent101 sources come from source main f44c06c4851b26523bcec920d93a52b93fd2a0a6: Agent101DigitPairs, Agent101MultiplicityBounds, Agent101SplitEnumeration, and Agent101NumericFibers. The Agent101 numeric enumeration/canonical interfaces and the original marker-safety theorem retain their original authorship.

The specific Lychrel196Research source is the original retained import-only adapter, blob 72a4f16d2160c3ebcee1d729fa1f5c717739b57e, SHA256 5c8859684f186a7121d0d3cbf82f2ad5ac9398ccb73c4dd6a9d2256be128a11b. It imports LychrelDigitSums and declares nothing. This makes the Agent101 and marker-safety imports share the same foundation without copying or replacing mathematical definitions. It is the sole legitimate zero-declaration project origin and must still be compiled in the fresh closure.

The independent verifier is copied and narrowly adapted from the reviewer's earlier recorded verification driver. Its exact hash and original driver attribution are recorded in verification/frozen-preparation.json and RESULT.json. It checks source identities and exact import closure, rejects forbidden proof tokens after stripping comments/strings, rebuilds all selected project modules with official Lean 4.19.0 at --trust=0, prints every literal public export's type and axioms, and collects transitive axioms for every theorem and every safe definition/opaque declaration by compiled module origin. The only permitted mathematical axioms are propext, Classical.choice, and Quot.sound. Unsafe compiler implementation constants are reported separately. The standard Lean runtime is hashed, rather than rebuilt from its own source, and the gate is scoped to this selected project closure rather than the entire repository.

## 8. Evidence history and scope

preparation-001 preserves an actual failed read-only lookup of the published generic checkpoint before its commit object was present in the local repository. Parent subsequently fetched the checkpoint. preparation-002 verifies the now-present checkpoint and all historical source bytes. This was an availability failure; it was not a compiler failure or a mathematical defect. The reviewer performed no Git mutation, source correction, or compensating proof edit.

The read-only child review covered Agent9FiniteProducts, Agent9MarkerWords, and Agent9MarkerEnumeration and found no defect. The reviewer independently read all five frozen modules, the exact original README, the retained numeric adapter and canonical interfaces, and the original finite marker-safety interface. Parent's additional reading of the final numeric/safety layer is separately attributed in the collaboration record and is not counted as another compiler audit. The author's own full gate and finite controls are separate supporting evidence, not the independent result reported here.

Acceptance is for the exact finite count and its direct finite positive-hit upper bound under the stated hypotheses. No further theorem, optional expansion of finite controls, or duplicate full compiler run is required by a remaining semantic risk.
