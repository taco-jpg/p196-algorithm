# Three zero-carry layers: a four-column obstruction

Agent #3, protected task `agent3-three-layer-dead-prefix-20261016`.
The claim was published at `3fbf616030a09c373b62b285827ff4851ada2052`,
after the exact scope was proposed on [issue 61](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225498922).

## Target and current status

The target is to rule out three successive original Agent #9 `Path`
witnesses into any target half beginning `[14,14,14,5]`, regardless of
its remaining symbol tail. The application uses the already checked
two-history construction with the first three free bits fixed to
`[true,true,false]`.

At the first author checkpoint, `SharpHistoryFamily.lean` has passed
Lean 4.19.0 compilation with `--trust=0` and all 16 explicit declaration
axiom reports. It proves exact duplicate-free enumerations of `2^m`
initial and protected coefficient words, width `2*(m+k+10)`, and the
inherited ordinary-integer safety bound through time `k+3` when `k>0`.
Every initial word has a positive canonical ordinary realization, and
every such realization has common time-four value
`digitValue (target (m+9) k)`.

`DeadPrefix.lean` has now also passed `--trust=0` compilation and all 15
explicit declaration audits. Its main endpoint
`P196.Agent3.ThreeLayer.no_three_paths_dead_prefix` excludes all three
original path witnesses for every remaining tail. Its only reported
transitive axiom is `propext`. The first predecessor prefix is forced to
`[7,7,7,2]`, the second to `[3,13,13,0]`; the third layer reaches carry
state two before target coefficient zero, where no local transition exists.

The actual-fiber transport, final aggregate, and complete independent
verification are being completed separately. This checkpoint does not
mark those pending endpoints as established.

## Original semantics and provenance

The prior two-history package is reused unchanged at
`89287c9d3eb7dd801c2b1a59eff03140d47d24ec` (reviewed PR 91).
Its four Agent #9 dependency copies are unchanged from
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`.
`ActualFiber` retains its equal half-width, coefficient bound below
nineteen, zero computed terminal carry, and actual `Agent8.stepWord`
equality. The original `actual_realizes` and `realizes_path` provide the
arithmetic converse.

The historical third-layer observation is in the separate checkpoint,
generator, and saved result table under snapshot
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. The exact identities are in
`ownership/source_identity.json` and the original claim record. The
two-layer safe-image note is not the source of the third-layer table.

The intended sharpness concerns this exact bounded, equal-width,
all-zero-carry predecessor domain. Neither mixed-overflow histories nor
an unrestricted ancestry bound are included. Counts refer to coefficient
words. The family varies with the prescribed finite horizon.

## Evidence

`development/family/` preserves the first successful source snapshot,
actual command, source and runtime hashes, compiler log, and all explicit
axiom reports. Its author check reuses the pinned 23-module dependency
cache and is labeled accordingly. The axiom union is contained in
`propext`, `Classical.choice`, and `Quot.sound`.

`development/dead-prefix/` preserves both actual attempts, the successful
source and all axiom reports. The initial attempt required unfolding the
new `Forced` abbreviation before Lean could synthesize its finite
decider; the original arithmetic and path predicates were unchanged.

`ownership/` preserves the exact published claim and the two independent
read-only scope checks. `development/resources/` records removal of
reproducible compiler objects and a byte-identical duplicate download;
all mathematical source and substantive verification evidence remain
retained. No main integration slot is held by Agent #3.
