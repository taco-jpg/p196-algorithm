# Independent semantic review: numerical target wrapper

Reviewer: Agent105 / scope105 / session 9df76b. The reviewer did not author this module. Frozen source: `proofs/Agent105NumericDecoder9df76b.lean`, SHA-256 `9a63eb03cb04d9e7fb3294216ab770893ac227c089ddba6d864d73d949229db5`.

**Semantic result: PASS for all three theorem declarations. No change requested.** The full independent frozen-registry replay is recorded separately when performed; this source review does not substitute for it.

The executable function receives the canonical target's digit function e, target width W, and prescribed source width L. It calls the zero-carry decoder for W=L, the one-carry decoder only for W=L+1 and an additional leading target digit equal to one, and otherwise returns none. The two width branches are disjoint. Each accepted width branch gives L≤W, so the target's Canonical premise supplies exactly the in-range digit bound required by the physical scan theorem.

`decodeNumerical_eq_some_iff_payload` preserves the target's complete numerical width condition and the actual physical payload; it does not treat a stripped overflow payload as canonical. It retains exact list length and both output/carry constraints. Its none branch excludes precisely both possible WidthChoice branches.

`decodeNumerical_eq_some_iff` converts an accepted payload to an actual positive natural-number predecessor using the original realization bridge. The converse obtains the physical payload from an actual predecessor and transports every in-range coefficient to the returned finite list. The theorem asserts the exact returned profile, not only that some unrelated predecessor exists.

`decodeNumerical_isSome_iff` removes only the finite profile witness and is equivalent to existence of an actual positive canonical predecessor at the prescribed width. The target integer Y occurs through Canonical Y e W, so the numerical connection is explicit. Zero source width is rejected by the underlying positive-width guard; arbitrary larger or much smaller source widths fail WidthChoice.

The reviewed source makes no assumption that a general target is palindromic and does not impose the palindrome-only middle-digit obstruction. It has no hidden requirement that the overflow-truncated low payload be positive or canonical. Trailing zeros in the source are allowed by Canonical and by the original reverse10 semantics.

The existing six closed controls already verify the scanner's delicate arithmetic boundaries, including 5→10, the minimal source, a carries-(1,1) empty interior, and the nonpalindromic cross-width example. The wrapper adds only the fully proved width/leading-digit branch selection. No concrete uncovered risk was found requiring extra duplicate closed wrapper tests.

The accepted interface is for a prescribed source width and returns a coefficient profile. It is not itself an enumeration of every ordinary integer predecessor or an infinite-time orbit assertion. Existing source-width results confine possible positive predecessor widths to the target width and one less; callers may evaluate those two prescribed-width queries.
