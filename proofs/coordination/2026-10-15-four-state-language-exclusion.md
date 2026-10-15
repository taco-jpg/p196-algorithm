# Checked four-state whole-word language exclusion; all capped evidence retained

This continuation follows the [intrinsic seam and finite-seed handoff](2026-10-15-intrinsic-seam-and-quantifiers.md)
at `e52125515490b668d14e95b0cf8d31767bcde7c4`. It pursues the unrestricted-language
workstream alongside the external clock hierarchy and all-base seam work.
During upload the shared head advanced through `eaa9c98b` to
`f33f917692794a93d71e714a17fcabbe84ae8c6e`. The [new reciprocal handoff](2026-10-15-sharp-kernel-and-renewal-audit.md)
supplies the complete kernel integration of the sharp fixed-(4,4,0) obstruction
and a fresh independent rebuild of our earlier 42-declaration raw-symmetry
module. Its exact sources, scope, compilation logs and provenance reconciliation
are preserved. This checkpoint acknowledges that supplied audit; it does not
claim a new local full rank rebuild. The 94/98 component-specific bounds retain
their separate finite-certificate and generic-formal scope.

Decimal Lychrel existence and the 196 claim remain unproved.

## Exact exclusion

There is no nonempty safe forward-closed language of canonical folded decimal
words recognized by a **complete deterministic automaton with at most four
pair-reading states and eleven arbitrary center/end predicates**. Initial and
dead states count toward four; the eleven terminal predicates are not additional
reading states. The alphabet is the 19 mirrored pair sums. Both overflow cases
are included at every update, with exact terminal carry matching. No seed,
temporal clock or fixed observation partition is assumed.

The [all-width reduction](../research/main_existence_attempt/continuation_pass/safe_language/METHOD_AND_PROOF.md)
proves exact arithmetic transduction, safety, closure and nonemptiness. The main
CNF has 2,682 variables and 263,792 clauses and uses **no state-renaming clauses**.
The independent checker reconstructed the complete clause multiset; a separate
literal-level LRAT checker verified 493,792 additions and 27,745,823 hints and
proved the empty clause. Root independently repeated both checks and reviewed
the all-width bridge. No Lean formalization of this reduction or LRAT checker
is claimed. The finite arithmetic controls validate the implementation; they
are not the all-width closure argument.

A four-state corroborating instance with renaming clauses is also independently
refuted. The five-state capped run remains **UNKNOWN** after 180 seconds. Its
incomplete proof trace is retained in full and is not called a refutation.
Larger regular languages and richer recursive descriptions remain open.

## Complete evidence and review history

All six exact CNF/proof artifacts are retained losslessly in **41 ordered gzip
parts**, each at most 6,000,000 bytes, with part, joined-archive and decoded
original SHA-256 values in the [archive manifest](../research/main_existence_attempt/continuation_pass/safe_language/evidence_parts/MANIFEST.json).
This includes the genuine incomplete five-state trace, not merely its solver
status. All source, logs, metadata, negative-label trajectories and the 263
short-word trajectories still UNKNOWN after 60 additions are retained. Those
263 inputs impose no negative label and imply no infinite safety claim.

The first root replay's proof and clause checks passed, but its final freeze
assertion noticed concurrent documentation edits. Its full log is retained.
The second frozen replay passed every check; the [review history](../research/main_existence_attempt/continuation_pass/root_review/PRIMARY_SAT_REVIEW_HISTORY.md)
and [hash-pinned receipt](../research/main_existence_attempt/continuation_pass/root_review/safe_language_review.json)
distinguish the two runs. Expanded inputs, exact copied replay inputs and
bytecode are inventoried as duplicate infrastructure, not omitted research.

## Reuse

From the published `safe_language/` directory, restore and replay in a disposable
checkout:

```sh
python3 -B restore_artifacts.py .
python3 -B check_lrat.py dfa4_neg2
python3 -B check_encoding.py dfa4_neg2
python3 -B restore_artifacts.py /tmp/safe_language_integrity --all --verify-only
```

The certificate rules out this exact bounded-state class. A proposed positive
regular invariant must escape that class, for example with at least five
complete pair-reading states, and still establish nonemptiness, universal
safety and successor coverage. The result supplies no positive instance.
