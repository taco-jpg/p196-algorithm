# Full-configuration correlation pass

**No safe forward-closed language or decimal Lychrel witness was found.**
This pass retained every reachable state of the exact 6,680-state safe-two-
ancestry NFA, including nonaccepting states. It did not rerun selection of
individual terminal flags.

The principal result is a finite arithmetic obstruction certificate for
**146 complete configuration/observation classes** occurring on the first
101 words of the 196 trajectory. Every class collision was independently
replayed, including its complete NFA subset, center, safe-two membership,
ordinary integer first-palindrome time, and exact recursive observation
residual. These are class exclusions, not a proof that 196 terminates.

| Observation depth | Checked excluded trace classes | Furthest excluded trace position |
|---|---:|---:|
| 4 | 57 | 100 |
| 5 | 42 | 100 |
| 6 | 27 | 100 |
| 7 | 12 | 100 |
| 8 | 6 | 92 |
| 9 | 1 | 69 |
| 10 | 1 | 69 |

Depth four uses the previously saved minimized observer. Depths five through
ten use exact unminimized carry-observer extensions, generated lazily. The
unbuilt transitions are never treated as missing. A raw residual equality
therefore implies equality on every future pair suffix and center.

The complete shorter search enumerated all **2,476,099** canonical pair
prefixes through five pairs, in addition to the existing 8,396-word witness
corpus, and found 75 collisions at depths four through seven. The follow-up
retained a 100-second cap, completed the same five-pair range, and stopped
partway through six pairs. Its 146 saved collisions are proved; the unfinished
six-pair enumeration and global language synthesis are **UNKNOWN**. No later
full determinization or global kernel was claimed.

## Two explicit full-correlation collisions

At trace position 25, the pair prefix of 8,801,197,801,088 is

`(16,16,0,2,1,17)`, center `14`.

It has complete NFA subset `{364}` and D4 state 74, identical to
`(18,17,17)`, center `14`. The latter has canonical realization 9,997,889 and
first reaches a palindrome after ten additions. Exhaustive enumeration of
all 6,859 canonical prefixes of at most three pairs proves that this is the
**unique shortest prefix in that exact combined class**.

This collision is repaired by depth five, and five is the first possible
observation depth that repairs it: changing the center to zero makes the
first prefix reach a palindrome at addition six, while the second prefix
does not do so during its first six additions. No appended pair is needed.

At trace position 69, the pair prefix of
1,326,313,072,829,535,757,534,829,271,313,622 is

`(3,5,8,9,4,4,4,7,9,11,10,10,13,8,8,12,12)`, no center.

It has the same complete 19-state NFA subset and exact raw depth-ten residual
as `(3,6,4,6,12,12)`, no center. The latter realizes as **364,699,330,000** and
first reaches a palindrome after **13** additions. No minimality claim is
made for this second witness. The depth-ten acceptance family cannot contain
this trace class, or any earlier 196 trace word in a forward-closed language.
The certificate does not forbid entering an invariant at a later trace word.

## An actual closure test

The regular candidate

`F10 = S2 intersect {words whose first eleven reverse-add outputs are nonpalindromes}`

was tested for its closure obligation. It fails:

`9948 -> 18447`.

Both words are accepted by the exact S2 NFA. Their first palindrome times
are respectively twelve and eleven, so the input is in F10 and its image
is outside F10. All 999 positive integers below 1,000 were checked independently;
there is no failure of this form below four digits. Thus the witness has
minimum decimal width for this candidate. Missing class collisions are not
treated as a substitute for this closure test.

## Antichain search

The second method used subset inclusion between complete NFA configurations,
stratified by D0 state. Monotonicity of NFA transitions permits exact
downward-closure exploration with reachable maximal representatives. This
could cover arbitrary positive conjunctions and disjunctions of all NFA
state-presence predicates, rather than terminal-flag unions.

The 90-second run did not complete. Its saved snapshot contains **65,170**
reachable, pairwise incomparable configuration/observer pairs, with at most
43 NFA states per subset. An independent checker reconstructed every subset
and checked all possible strict containment pairs through inverted indices.
The counts by D0 state are 1, 11,143, 54,005, and 21. These are exact snapshot
counts; later reachable supersets might dominate existing entries. They do
not establish the final antichain size or a minimum automaton size.

All subprocesses for this pass stopped. Global reachable downward closure,
global acceptance-family exclusion, and positive inductive synthesis remain
UNKNOWN. `METHOD_AND_PROOF.md` states the precise theorem and limitations.

## Reproduce and audit

Run from the project root:

```sh
python3 main_existence_attempt/correlation_pass/language/check_correlated_collisions.py --certificate correlated_cegar_pairs5_result.json
python3 main_existence_attempt/correlation_pass/language/check_correlated_collisions.py
python3 main_existence_attempt/correlation_pass/language/focused_checks.py
python3 main_existence_attempt/correlation_pass/language/check_antichain.py
```

Discovery commands are recorded in the reports. Time-cap snapshots can vary
by machine; the saved certificates and their hashes are the audited objects.
No earlier research artifact was modified and no external publication was
performed by this worker.
