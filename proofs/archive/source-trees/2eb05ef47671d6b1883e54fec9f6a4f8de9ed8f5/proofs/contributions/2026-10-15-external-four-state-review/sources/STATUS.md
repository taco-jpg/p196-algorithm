# Four-state whole-word regular invariants excluded

**No safe forward-closed language or decimal Lychrel witness was found.**
This pass resolves one previously UNKNOWN bounded automaton case with a
checked UNSAT certificate. It does not exclude unrestricted regular
languages, recursive languages, or the existence of a decimal Lychrel number.

There is no nonempty safe forward-closed language of canonical folded
decimal words recognized by a **complete deterministic automaton with at
most four pair-reading states and eleven arbitrary center/end predicates**.
The initial and dead states count toward four. The input alphabet is the
19 mirrored digit sums 0,...,18. Both overflow possibilities are included
at every step, with terminal carry matching; no temporal clock or seed is
fixed. The all-width arithmetic and Boolean reduction are stated in
`METHOD_AND_PROOF.md`.

| Run | States | Renaming clauses | Variables | Clauses | Solver outcome | Wall time |
|---|---:|---|---:|---:|---|---:|
| Primary | 4 | None | 2,682 | 263,792 | UNSAT, independently proved | 35.37 s |
| Corroboration | 4 | First target appearance | 2,682 | 263,944 | UNSAT, independently proved | 5.84 s |
| Capped continuation | 5 | First target appearance | 3,683 | 609,596 | UNKNOWN | 180.00 s |

The main result uses the primary instance **without symmetry assumptions**.
The capped five-state trace is incomplete, has no claimed refutation, and
supplies neither exclusion nor invariant. No larger case was run.

## Independent evidence

`check_lrat.py` is a standalone positive-hint LRAT checker. It checks every
added clause by literal-level unit propagation and requires a proved empty
clause. The primary replay verified **493,792 additions and 27,745,823
hints**. The corroborating replay verified **119,357 additions and 3,992,780
hints**. No solver library or generator is imported by the checker.

`check_encoding.py` independently reconstructs the complete multiset of
every CNF clause from variable names, checks all formula families, and
derives the carry transducer from decimal column equations. It confirms
46 transducer states, 872 pair edges, and 251 terminal cases. All three
saved formulas passed this audit. Ordinary controls cover all 99,999
positive integers below 100,000 and all 3,969 canonical folded words of
width at most five. Complete arithmetic trajectories certify all 3,706
negative labels used as redundant solver constraints, totaling 17,946
additions. The other 263 short inputs remain UNKNOWN at horizon sixty and
impose no negative label.
Their full 60-step ordinary trajectories are separately retained and
replayed in `short_corpus_unknowns.json.gz`; this adds no infinite-safety
claim.

The universal result follows from the all-width transducer proof, exact
nonemptiness reduction, literal-complete CNF audit, and checked refutation.
The finite arithmetic controls audit implementations; their finite range
is not a substitute for universal closure.

## Reproduce

Large original artifacts are retained losslessly in ordered gzip parts
of at most 6,000,000 bytes under `evidence_parts/`. Its `MANIFEST.json`
records the ordered names, each part's hash, the joined archive hash,
and the decoded original byte count and hash. It distinguishes the two
complete UNSAT proofs from the five-state incomplete trace.

Restore the primary formula and proof to a temporary directory:

```sh
python3 -B restore_artifacts.py /tmp/safe_language_replay
python3 -B check_lrat.py /tmp/safe_language_replay/dfa4_neg2
```

For the encoding audit, copy the small metadata and label files beside
the restored formula, or restore into this directory:

```sh
python3 -B restore_artifacts.py .
python3 -B check_encoding.py dfa4_neg2
```

Verify every archived byte, including the incomplete run, without retaining
the expanded originals:

```sh
python3 -B restore_artifacts.py /tmp/safe_language_verify --all --verify-only
```

The exact primary generator command is:

```sh
python3 -B synthesize_dfa.py --states 4 --terminating-depth 2 --no-symmetry --stem dfa4_neg2
cadical --lrat --no-binary -t 180 dfa4_neg2.cnf dfa4_neg2.lrat
```

The source generator's no-symmetry output was byte-identical to the saved
primary CNF. The arithmetic evidence, full proof traces, solver logs,
unrestricted reduction, and UNKNOWN cap are preserved. This worker made
no remote write; the parent publisher owns publication.
