# Agent #103 — complete residual-five fibers with positive first hit two

Task: `agent103-residual-five-firsthit-two-20261016`.
Remote ownership was established at coordination commit
`a594eb7693d25e925642d15ae14bea763db500f3` before any new proof development.
Entry point: `ResidualFiveFirstHitConclusion.lean`.

## Exact statements

Use the unchanged original decimal reverse-and-add operation `Lychrel196.step`
and its `orbit`. The prior complete fiber is

```lean
fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none
modularFiber r = (fiber r).filter (fun n => decide (n % 99 = 77))
```

For every natural parameter `r` and every member `n` of the full fiber:

- `orbit n 1 = 33 * 10^(2*r+2) + 22`, which is not a palindrome.
- `orbit n 2 = Agent119.EightFamilies.fam 5 r`, which is a palindrome.
- `Palindrome n` holds exactly when `r = 0` and `n = 1661`.
- The original positive-first-hit defining conjunction holds at time two:
  `0 < 2`, a palindrome at time two, and no palindrome at any strictly positive
  time below two. No new or weakened first-hit predicate is introduced.

For each member of the exact modulo-99 filtered fiber, the stronger temporal
equality is proved for every natural `i`:

```lean
orbit n i % 99 = orbit 196 (7 + i) % 99
```

`complete_modular_first_hit_fiber` combines these facts with the previously
proved duplicate freedom, full natural-number membership iff, and exact length

```lean
if r % 2 = 0 then (14 * 10^r + 8) / 11 else (14 * 10^r - 8) / 11
```

`compatible_first_hit_exists` discharges existence for every parameter by the
proved positive count of the actual list. It gives a positive integer with the
full residue trace and positive first hit two; for `r > 0` its initial value is
also nonpalindromic. These are local ordinary-integer constructions. Residue
equality does not identify integer trajectories or establish 196 reachability.

## Proof ingredients and provenance

`ResidualFiveHitDynamics` compares the mirrored digits of the canonical middle
integer with the original family digit function. Its unequal endpoint digits
give the nonpalindrome at time one.

`ResidualFiveInitialPalindromes` specializes the unchanged Agent101 complete
numeric-fiber palindrome criterion. A positive parameter places odd coefficient
9 in the profile; at parameter zero, halving `[2,12,12,2]` has original numeric
value 1661. The exceptional member is proved to exist.

`ResidualFivePhaseCompatibility` applies Agent423's original modulo-99 power
law on the divisible-by-11 class. The exact starting phase is the original
196 phase table at time seven. It does not reimplement a general temporal law.

The previous 22-module fiber/count package is inherited from exact evidence
commit `018a49231cd3226506699282f0f173745e6b9f8d`, together with its additive
audit-scope clarification at `b235d662ce481cf43f8db1335c18f5993953af9d`.
Its mathematical sources are unchanged. The only additional original
dependency is unchanged `Agent101PalindromeFibers.lean` from
`71691d50497edc83247b3571af276bb0ee438491`, blob
`2ea26d6f8cd0d2a3ef7d3f887cb9e10fd66b5953`. Its source and provenance are retained.

## Completed independent verification

All four new modules are frozen and author-compiled with the official
Lean 4.19.0 executable, commit `6caaee842e94`, using
`--trust=0 -j1 -DElab.async=false`. All 20 new source theorem declarations have
successful explicit `#print axioms` reports within the project's standard
`propext`, `Classical.choice`, `Quot.sound` allowlist. There are no new definitions.
The 14 original public theorem declarations in Agent101's added dependency also
compiled and were queried. A separate genuine nonauthor specialist then performed
one complete fresh build of the frozen source commit
`1908a7e91d4c45c9ce455235f40d4b627af7e4d9`. All **27 modules** compiled successfully:
23 dependencies and 4 new modules. The full audit queried **1881 theorem constants**,
including private and generated helpers: 1834 inherited constants and 47 from
the new modules. Every actual transitive axiom list is a subset of the three
foundational axioms above. All 1812 theorem names, origins and individual axiom
lists from the preceding package are preserved in this audit.

The safety census has two separately defined scopes. There are 33 inherited
unsafe `axiomInfo` implementation entries. The additional complete
`defnInfo`/`opaqueInfo` inventory has 1157 inherited entries: 216 safe definitions,
917 unsafe definitions, 24 partial definitions, and no opaque definitions.
The 33-entry ledger is not the total number of unsafe constants in every
`ConstantInfo` category. None of the recorded unsafe or partial names occurs
in any audited theorem's axiom list. The four new modules introduce no
definition or opaque constants. See [SAFETY_CENSUS.md](SAFETY_CENSUS.md).

The current gate is **INDEPENDENTLY-REVIEWED for this contribution closure**.
The frozen mathematical sources have not changed since their tested commit.
The single-root source/import registry check also passed; this structural check
is separately identified from the actual full Lean build. The contribution
does not assert a repository-wide acceptance or its own main integration.

The portable [check.py](check.py), exact [SOURCES.json](SOURCES.json),
[BUILD_REGISTRY.json](BUILD_REGISTRY.json), and [REPRODUCE.md](REPRODUCE.md)
permit a new clean run. The complete source, commands, outputs, failed attempts,
source snapshots and named reviews are retained in
`evidence/complete-replay-evidence.tar.xz`: **203 regular files**, comprising
202 indexed files plus `FILES.json`, **189180 bytes**, SHA-256
`b8fdab43cb48d3d507e52143e90e634d65ce7c7c1080f58c34f08881c42a6fef`.
All archived bytes were verified after decompression; compiler objects are
reproducible and excluded. The earlier development archive remains unchanged.

Real proof development is retained in `evidence/development-evidence.tar.xz`.
The first phase proof attempt failed because a simplifier rewrite recurred;
its source and genuine error/`sorryAx` report remain clearly rejected evidence.
The final explicit modular-arithmetic proof compiled successfully and is the
only phase source in the accepted import graph. No failed attempt is imported.

Authors: the genuine `/root/scope_scan` specialist wrote dynamics;
`/root/source_audit` wrote the initial-palindrome specialization; root wrote
the phase specialization and aggregate. `/root/runtime` authored none of these
four proof modules and performed the independent full build and semantic review.
Named cross-author reviews cover the phase module and the other three modules,
with authorship boundaries recorded in the final review. Root is the sole Git
writer; the designated external integration owner retains main authority.
