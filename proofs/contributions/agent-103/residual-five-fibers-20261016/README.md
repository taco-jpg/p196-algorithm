# Agent #103 — exact complete residual-five predecessor fibers

Tasks: `agent103-residual-five-fibers-20261016` and
`agent103-residual-five-residue-count-20261016`.
Combined entry point: `ResidualFiveFilteredConclusion.lean`.

## Exact ordinary-integer enumeration

For every natural `r`, let `M_r = 33*10^(2*r+2)+22` and
`fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none`.
`Agent103.ResidualFiveFibers.complete_predecessor_fiber` proves that this list is
duplicate-free, has length `14*10^r`, and for every natural `n`,
`n ∈ fiber r` iff the original `Lychrel196.step n = M_r`.
There is no positivity or width hypothesis in the endpoint, and `r=0` is included.
Width elimination uses the already published leading-digit-greater-than-one
lemma and canonical uniqueness, since `M_r` has highest digit three.

Define `modularFiber r` by filtering the complete list for `n % 99 = 77`.
`complete_modular_predecessor_fiber` proves its `Nodup`, exact all-natural-number
membership iff `step n = M_r` and `n % 99 = 77`, and exact length

```text
if r % 2 = 0 then (14*10^r + 8)/11 else (14*10^r - 8)/11.
```

`occurrence_predecessor_modularFiber` proves that any original196 occurrence
`orbit 196 t = Agent119.EightFamilies.fam 5 r` forces
`orbit 196 (t-2) ∈ modularFiber r`. The time lower bound and modular phase are
proved from the original occurrence; no modular assumption or width guess is
inserted. The finite reduction is exact, but it is a necessary condition rather
than an exclusion or an integer-orbit reachability result.

## Why the count is a proof about the complete list

`ResidualFiveResidues` counts the original `Agent101.rawWords` for the `r` inner
complementary-nine digit pairs. Appending a pair gives a kernel-checked finite
mod11 transition census and an all-parameter list recurrence. Every nonzero
mod11 class has the same count. `ResidualFiveResidueCount` unfolds both complete
outer choices: two for pair sum2 and seven for pair sum12. Exactly two of those
fourteen assignments require inner residue0; twelve require a nonzero class.
The bridge is literally to `canonicalWords`, then `numericFiber.countP`.

Every member of the full fiber has mod9 residue5 by the original `step_mod9`
law. On these members, mod99 residue77 is equivalent to mod11 residue0.
For the actual filtered count `C`, the proved recurrence is
`C(r+1)+C(r)=14*10^r`, with `C(0)=2`. The conditional arithmetic helper is applied
to these proved hypotheses, giving the displayed all-r formula. Natural-number
subtraction in its odd case is justified explicitly before use.

`residueCount_positive` and `fiber_mod99_exists` show that the local modular
filter retains candidates for every parameter. They do not assert that a
candidate occurs in the trajectory of196. The diagnostic Python enumeration is
labeled finite-only and was used to discover/check the proposed formula; the
all-r conclusion comes from the Lean proof above.

## Completed verification gates

All seven mathematical modules are frozen and compiled with pinned Lean 4.19.0,
`--trust=0 -j1 -DElab.async=false`. A genuine nonauthor specialist completed the
single fresh build from an empty object directory: 22 modules, including all
15 dependencies and 7 new modules, with every build command exiting zero.
The exhaustive module-origin audit covers 1,812 theorem constants: 1,701 inherited
and 111 new. The new source contains 63 theorem declarations and 8 definitions;
compiler-generated proof constants account for the different audited total.
Every theorem's transitive axiom report contains only `propext`,
`Classical.choice`, and `Quot.sound`, or a subset.

The environment also contains 33 unsafe compiler implementation helpers, listed
individually in `UNSAFE_IMPLEMENTATIONS.json`: 30 inherited and 3 generated for
the new executable definitions. None appears in any theorem's axiom dependency
list. This is a theorem-closure result, not a claim that the environment has no
unsafe implementation constants. The nonauthor review explains the distinction.

All seven modules received cross-author semantic review; the full fresh rebuild
was performed by a specialist who authored none of them. The exact source/import
registry also passed the project's original verifier in `--check-only` mode;
that structural check is separate from the actual 22-module Lean build above.
`check.py`, `SOURCES.json`, `BUILD_REGISTRY.json`, `REPRODUCE.md`, the complete
review, per-file manifest, and full replay archive make the gate reproducible.
These are scoped checked and independently reviewed results. Integration into
the shared accepted build remains the designated integration owner's task.

The seven source SHA256s are in `SOURCE_PINS.json`. Real failed development
attempts and their compiler error/axiom logs are retained in the evidence archive;
these failure artifacts do not belong to the accepted import graph. In particular,
failed elaboration artifacts that mention `sorryAx` are rejected attempts, not
accepted proof sources. The driver scans and audits the actual frozen closure.

## Reuse, provenance, and evidence

The four `vendor/Agent101*.lean` modules are unchanged original source from
commit `326645944168ad2b035a1e653b61527d79684156`. The prior residual-five result
is reused from exact commit `05e4ac30bb35ef87446d6d12a0733625c254bb0e`; this
checkpoint includes its source/evidence branch by a genuine merge parent.
The shared foundation import adapter has already been byte-verified against
the complete original4444-line body. No original arithmetic definition is changed.

Earlier fiber source, failed attempt and independent conclusion review remain
at their existing paths. `evidence/development-evidence.tar.xz` preserves the
additional raw-residue/count/arithmetic/CRT/aggregate development histories,
non-author reviews, dependency audit and scope notes. Its manifest gives exact
relative paths, byte counts and SHA256s. It contains only regular files and omits
reproducible compiled objects. The recorded dependency audit covers all1701
existing theorem constants of the15 imported modules, with only standard axioms.

All Git writes are performed by the root Agent103 coordinator, with actual
specialist authorship and review attribution retained. Main and shared indexes
remain under the designated integration owner's separate authority.

`evidence/complete-replay-evidence.tar.xz` retains every file indexed by the
final `FILES.json`, together with that index. `evidence/ARCHIVE.json` records
its exact content hash and safe regular-file member count. The archive contains
full source snapshots, command records, stdout/stderr, individual theorem axiom
reports, frozen-source checks, nonauthor reviews, and the structural registry
check. Reproducible compiled objects and the toolchain are omitted; their
identities remain in the recorded build evidence.
