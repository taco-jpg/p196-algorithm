# Fixed actual-width ordinary predecessor bounds — Agent #101 / numeric_bridge

Accepted source: `proofs/Agent101WidthFiberBounds.lean`, SHA256
`db563069a3a2e618bfced9746fbb4b7092e68634ee4de2bd632332ed71982185`.

## Complete semantic coverage

`mem_numericFiber_of_same_width_step` takes one canonical finite digit-list
representative, its exact coefficientWord reconstruction, and an arbitrary
ordinary natural number at the same actual decimalWidth with the same original
Lychrel196.step output. It proves membership in the already complete numericFiber
using original canonical-to-list and same-width pair-sum equivalence.
It neither assumes a decoder nor assumes that an arbitrary target already has
one specified profile. The representative supplies the profile explicitly.

`fixed_width_profile_length_le` sends every member of an arbitrary Nodup list
through that membership result and compares its length to the exact profileCount.
No completeness assumption on the input list is needed: the theorem applies
to every finite subfamily and hence in particular to the complete fiber.

The three consumer endpoints are:

- `fixed_width_preimages_outer_bound Y L n s d hc hL hs ho ns hns hm`:
  a canonical representative `n,d,L`, `2 <= L`, `step n = Y`, and exact
  `columnSum d L 0 = s` yield
  `ns.length <= pairCount true s * 10^(L/2-1)` for any Nodup list whose
  members have actual width L and step output Y. The representative need
  not belong to ns; the empty-list case is included.
- `fixed_width_preimages_bound Y L ns hL hns hm`:
  the same bound uniformly replaces the outer factor by nine. In a nonempty
  list, one actual member supplies the representative; the empty list is
  handled directly.
- `one_digit_preimages_bound Y ns hns hm`:
  a Nodup same-target width-one list has length at most one. Its half is
  empty and `profileCount_single_le` handles the positive single center.

`profileCount_cons_outer_le` is the arithmetic helper preserving the exact
outer factor while bounding the center by one and the remaining pair product
by a power of ten. No cross-width reasoning is included here; root combines
these endpoints with Agent105's separately attributed constraints.

## Attribution and dependency choice

The private finite-list subset cardinality helper specializes the same erase
proof already published as
`P196.Agent2.OverflowFibers.nodup_subset_length_le`, source
`Agent2OverflowBound.lean`, Git blob
`7a8ec5eb70cf418ef23f0a55654b88031797bfb4`. The private Nat specialization
avoids importing its unrelated Agent8 stepWord chain and is not claimed as new
mathematics. The accepted file documents the exact provenance inline.

All original Agent101 enumeration, numeric interpretation and count declarations
are imported unchanged. The only direct import is Agent101ProfileExtraction.

## Evidence

`attempt-002` passes actual Lean 4.19.0 `--trust=0 -j1 -DElab.async=false`,
with six public axiom prints. `attempt-001` is retained: `subst outer` chose
the alternate equality to the actual column sum rather than to the requested s;
the corrected proof explicitly rewrites the desired equality in its profile
hypothesis. Rejected attempt recovery axioms are not accepted evidence.

`ModuleAudit.lean` and `module-audit/` audit both new module origins, covering
all 26 theorem constants, including private/generated proofs. The 13 public
exports and all 26 transitive reports use only propext, Classical.choice,
Quot.sound. No new axiom, unsafe definition, or opaque declaration is present.
`INCREMENTAL-VERIFICATION.json` records exact source and reused olean hashes.

This package is LEAN-CHECKED incrementally by its author, not independently
reviewed here and not a fresh dependency rebuild. All compiler objects reside
in scratch `agent101-runtime/profile-width-dev`, outside contribution sources.
