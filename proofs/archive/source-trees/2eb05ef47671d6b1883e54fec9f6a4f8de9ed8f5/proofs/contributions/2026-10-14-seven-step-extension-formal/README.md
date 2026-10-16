# An actual 440 boundary cannot return every seven steps four times

This contribution formalizes a finite obstruction to the proposed seven-step
renewal clock. For an admissible symmetric decimal pair word of width at least
six, starting with boundary `(4,4,0)`, at least one of the boundaries at times
`7,14,21,28` differs from `(4,4,0)`. More generally, consecutive seven-step
returns can occur at most three times.

The stronger intermediate result bounds this exact boundary-and-overflow
clock by **26 transitions**:

- Boundaries: `440 → 880 → (16,16,0) → (7,14,7) → (15,8,15) → (6,14,14) → (13,9,9) → 440`.
- Overflows: `0,0,1,0,1,0,1`, repeated by phase.

This is a theorem about actual whole-word evolution, not just freely chosen
Boolean controls. It rules out perpetual repetition of this particular
renewal mechanism. It does not prove palindrome occurrence, perpetual
palindrome avoidance, or the P196/Lychrel conjecture.

## Proof structure

| File | Role |
| --- | --- |
| `SixPrefix.lean` | Proves the six-coordinate transducer equals the actual next pair word. Its Boolean input is the actual carry at `L−6`. Boundary windows may overlap. |
| `RankData.lean` | Transparent candidate rank function on seven phases and three further coefficients in `0..18`. |
| `RankChecks0.lean` through `RankChecks6.lean` | Kernel `decide` checks of all `7·19³·2 = 96,026` phase/tail/control inputs, plus the initial rank bound. |
| `RankCertificate.lean` | Combines finite checks: each accepted transition strictly decreases rank, and phase-zero rank is at most 26. |
| `ActualRank.lean` | Supplies bounded coordinates and accepted-edge premises from the actual orbit, using actual carries. |
| `ClockPaths.lean` | Derives the exact intervening trace and overflow sequence from two successive seven-step return endpoints; proves the natural-number descent bound. |
| `NoFourReturns.lean` | Combines these results into `clock_length_bound`, `at_most_three_returns`, `one_of_four_returns_fails`, and `no_perpetual_returns`. |

`NoFourReturns.no_four_returns_of_canonical` derives admissibility from a
canonical decimal representation. All theorems are unconditional apart from
the stated width, admissibility or representation, and return hypotheses.
In particular, no unproved invariant of the inner coefficients is assumed.

## Finite certificate and trust boundary

The candidate ranks were extracted from
`../2026-10-14-seven-step-extension/direct_six_graph.bin.gz`. That graph has
48,013 vertices and 61,731 accepted edges. The proof does not trust its edge
list, the Python generator, a DAG assertion, or the external graph audit.
Instead, Lean evaluates `SixPrefix.step` on every finite input and checks the
required strict inequality whenever the next phase and overflow match.

`generate_rank_certificate.py` compresses repeated rank rows and emits the
transparent Lean definitions and check statements. A bad candidate rank or
bad compression would make the finite theorem fail. The phase prefixes and
overflows are connected to the previously checked seven-step return theorem
by `NoFourReturns.phasePrefix_lookup`, `phaseOverflow_lookup`, and
`returns_force_clock`.

No `native_decide`, custom axiom, `sorry`, or `admit` occurs in the new proof
sources. The checked transitive axiom dependencies are recorded individually
in `verification.json` and are restricted to Lean's standard `propext`,
`Quot.sound`, and `Classical.choice`.

## Reproduce

Use Lean 4.19.0 and Python 3:

```sh
python3 check.py --lean /path/to/lean-4.19.0/bin/lean
```

The checker copies all project dependencies into a fresh temporary directory,
rebuilds them, runs the finite checks with one Lean thread, synchronous theorem elaboration,
and one process by default, compiles the actual-orbit conclusion, and audits all 211 public
theorems in the new modules and the three seven-step prerequisite modules.
Each axiom audit also follows every imported theorem used by its proof. The expensive finite
checks may take several minutes. `--workers 2` permits two processes when sufficient memory is available.

The supplied `compile.log` and `verification.json` record one fresh build.
Its collection step used `--collect-build` to finish the endpoint proof and
axiom audit after the recorded dependency and rank phases, without repeating
the expensive finite checks. The collector checks source bytes, source and
object hashes, dependency hashes, exit codes, and logs before accepting that
build. No preexisting project object files were imported into it.

`provenance_reconciliation.json` preserves the original records and the
one-time reconciliation used for this run. Review found that the early resume
runner did not bind internal rank dependencies. The public runner and
collector were hardened and passed stale-dependency fixtures. The successful
finite checks were retained only after frozen source/object/log checks and an
independent byte-identical replay of all seven prerequisite objects through
`RankData`; the cheap phase aggregator was also replayed. Legacy records
without dependency fingerprints are rejected by the public tools. An initial
prerequisite replay under different elaboration settings produced different
object bytes; that result is preserved separately and was excluded from the
byte-identity comparison. No expensive finite chunk was repeated for this
reconciliation.

The verification environment required a local `readlink` compatibility shim:
reading `/proc/<own PID>/exe` was blocked while `/proc/self/exe` worked. The
shim only redirects that exact self-executable lookup; it does not modify
Lean's elaborator or kernel. A normal Lean installation does not need it.
