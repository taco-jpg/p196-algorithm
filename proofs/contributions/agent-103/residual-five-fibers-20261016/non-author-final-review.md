# Non-author final review: residual-five predecessor fibers

Reviewer: **Agent #103 /root/runtime**, a separate real subagent of the same service account. The reviewer authored the reproduction tooling, independently read the frozen mathematical sources, and did not author or edit these seven mathematical modules.

**Result: PASS for the scoped contribution.** All seven source modules passed semantic review. One complete rebuild restored every dependency from its pinned Git commit and original path, verified both Git blob and SHA-256 identities, and compiled all 22 project modules in a previously nonexistent directory. No old project `.olean` was copied into that build.

The original `Lychrel196.step`, `Lychrel196.orbit`, original Agent101 digit-list evaluation, and complete ordinary-integer `numericFiber` are preserved. This result is a complete local predecessor classification and a necessary finite reduction for any hypothetical original-196 residual-five occurrence. It does not prove an occurrence on that orbit or global avoidance of the residual family or palindromes.

## Actual kernel evidence

The official release is Lean **4.19.0**, commit **6caaee842e94**. Every module compilation and the complete environment audit used:

```text
--trust=0 -j1 -DElab.async=false
```

The single full run started at **2026-10-16T21:53:21Z** and finished at **2026-10-16T21:56:02Z**. All 22 module commands and the final audit exited **0**. The seven new-module compile logs contain no warnings or errors. Source, compiler and runtime hashes remained unchanged.

The audit discovers every theorem by its actual compiled module origin, including private declarations and generated proof helpers, and issues a literal `#print axioms` for each one. It audited **1,812 theorem constants: 1,701 inherited dependency constants and 111 constants from the new modules**. The inherited theorem names, module origins and individual axiom lists exactly match the preceding 15-module dependency audit.

The seven new source files contain **63 written theorem declarations and 8 definitions**. The larger compiled count includes Lean-generated proof helpers and is not a count of distinct mathematical discoveries.

| New module | Written theorem declarations | Compiled theorem constants |
|---|---:|---:|
| `ResidualFiveFibers` | 11 | 17 |
| `ResidualFiveFiberConclusion` | 7 | 20 |
| `ResidualFiveResidues` | 20 | 26 |
| `ResidualFiveResidueCount` | 16 | 23 |
| `ResidualFiveResidueBridge` | 3 | 6 |
| `ResidualFiveCountArithmetic` | 3 | 13 |
| `ResidualFiveFilteredConclusion` | 3 | 6 |

Every audited theorem's transitive axioms are contained in `{propext, Classical.choice, Quot.sound}`. All 11 declared registry endpoints were found in the actual full audit with the expected module origins and allowed axioms.

### Unsafe implementation ledger

The environment also contains **33 declarations flagged `isUnsafe`**, all retained individually in `UNSAFE_IMPLEMENTATIONS.json` and in the raw audit log. **30 are inherited from dependencies; 3 are new compiler implementation helpers**:

- `List.countP.go._at.Agent103.ResidualFiveResidues.rawCount._spec_1`
- `List.countP.go._at.Agent103.ResidualFiveResidueCount.residueCount._spec_1`
- `List.filterTR.loop._at.Agent103.ResidualFiveFibers.modularFiber._spec_1`

These implementation entries are not suppressed or described as absent. None occurs in any of the 1,812 actual theorem axiom lists. The audit rejects non-unsafe custom axiom declarations and retains the unsafe implementation ledger separately from the proof-dependency results.

## Source identity and foundation compatibility

`SOURCES.json` fixes 15 dependency modules and 7 new modules. The original sources are read from commits `913441a936a437e5f4b82d03d7e7fae32da877af`, `6fae6e659e5c08c59666588c71a4ed06760de85e`, `326645944168ad2b035a1e653b61527d79684156`, and the first contribution's final evidence commit `05e4ac30bb35ef87446d6d12a0733625c254bb0e`. The seven new files are individually frozen by SHA-256 and their Git blob identities.

The sole compatibility source is the exact import-only `Lychrel196Research` forwarder, `import LychrelDigitSums` followed by a newline. Its SHA-256 is `13dd9effbef33d3d10138baed5cb3a6f964691ba895cc5d453f2553f0ac81011`.

The checker verifies that the original foundation body after `import Std` is uniquely contained byte-for-byte in pinned `LychrelDigitSums`: **177,451 bytes, 4,444 lines**, beginning at byte offset **329**, line **11**. The preflight independently read Agent101's original foundation blob and verified it is the same original foundation. This adapter forwards the existing definitions; it adds no replacement definitions or mathematical assumptions.

## Semantic review

1. **Complete ordinary predecessor list.** The profile `[2,12] ++ replicate r 9`, with no center digit, is normalized through the original carry/value interfaces to `33*10^(2*r+2)+22`. The outer sum-2 pair has 2 canonical choices, the next sum-12 pair has 7 choices, and each inner sum-9 pair has 10 choices. Original numeric-value injectivity yields an actual list of `14*10^r` distinct ordinary integers.
2. **All widths are covered.** The target's highest digit is 3. The existing generic no-overflow theorem rules out an added high column without assuming the target is a palindrome. An arbitrary predecessor is first proved nonzero, represented canonically, and then proved to have width `2*r+4`. The final membership equivalence has no width premise.
3. **The raw residue count is concrete.** `rawNine` is original `rawWords`, and `rawCount` counts original `natValue` residues on that complete list. A single even-length wrap negates the old residue modulo 11. The ten ordered sum-9 pairs therefore reach every class except the negative old class, exactly once. The all-parameter list recurrence and nonzero-class uniformity retain that sign and the original multiplicities.
4. **All fourteen outside assignments are counted.** Double wrapping cancels the two inner sign changes. The complete 2-by-7 outside list contains two zero residue targets and twelve nonzero targets. It gives the actual ordinary-integer count `2*rawCount r 0 + 12*rawCount r 1`. At `r=0`, the compatible integers are 1661 and 2750; trailing-zero inputs and the palindromic local predecessor are not omitted.
5. **The modulo-99 bridge applies on the actual fiber.** Its members have residue 5 modulo 9, derived from the unchanged reverse-add modulo-9 law. On those members, residue 77 modulo 99 is equivalent to residue 0 modulo 11. The bridge uses `List.countP_congr` on the same list.
6. **The displayed closed form has no remaining recurrence hypothesis.** The actual filtered count satisfies `C(0)=2` and `C(r+1)+C(r)=14*10^r`. These facts discharge the conditional arithmetic module's assumptions. Thus the original filter length is `(14*10^r+8)/11` for even `r` and `(14*10^r-8)/11` for odd `r`. The odd subtraction is justified before natural-number division. Filtered `Nodup` makes this a distinct-integer cardinality.
7. **The original-196 condition remains conditional.** A hypothetical occurrence at time `t` yields membership of `orbit 196 (t-2)` in that same complete filtered list. Earlier orbit bounds justify the natural-number time subtractions; the existing temporal table selects residue 77 at the correct predecessor phase. Positive local count for every `r` does not assert that any listed integer is 196-reachable.

Detailed module-specific reviews and the independent fourteen-assignment census are in `reviews/`. Separate peer review/build manifests are indexed in `non-author-final-review.json`; those peer module builds are distinguished from this complete fresh closure build.

## Published-path compatibility

The additive `BUILD_REGISTRY.json` uses the single root `ResidualFiveFilteredConclusion`. Its actual import graph reaches all **22** registered modules with no unused entries. The four current foundation paths were checked against the pinned `SOURCE_MAP`; the existing first contribution and vendored Agent101 sources retain exact source hashes.

The current project verifier was run separately with `--check-only`, using the exact published paths in a private staging checkout. It exited **0**, status `SOURCE_AND_IMPORT_CHECK_ONLY`. That check validates source identities and the import graph; it is not the mathematical build. No second complete Lean rebuild was performed.

`REPRODUCE.md` gives both commands. `verification-clean-001/verification.json` records complete per-command arguments, environment, exit codes, source/object hashes and all theorem results. The raw audit and all non-object build artifacts are indexed by `FILES.json`.
