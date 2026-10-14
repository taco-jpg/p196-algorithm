# Conditional carry-history score attempt

No decimal Lychrel witness was found. Two genuinely conditional formulations
were built, both with exact finite encodings that cover every word length.

## 1. Parity of full carry-history tiles: exactly excluded

Assign a bit to each of the 872 edges and 251 terminal tiles of the exact
46-state folded decimal reverse-and-add transducer. Let S(q) be the XOR of
the labels along the unique history q -> T(q). Accept precisely S(q)=1.
Require only:

    T(q) bad  => S(q)=0,
    S(q)=1   => S(T(q))=1,
    S(q)=1 for at least one finite canonical q.

The second line is an implication, not equality. It permits (S(q),S(T(q)))
=(0,1), so the previous unconditional conservation obstruction does not
answer this formulation.

This is also not the previously excluded 2- or 3-state DFA over raw q
symbols. Its parity bit reads full carry-history tiles and is combined with
the 46-state transducer, including guessed high carries and overflow memory.
It is not the one-tile allowed grammar: two occurrences of a bit-1 tile can
cancel, and order is retained in the underlying carry transducer.

Safety is expressed exactly by GF(2) prefix potentials on the 48-state
safety graph. A spanning-forest gauge sets 44 edge bits to zero without
changing any complete score. Gaussian elimination, with exact GF(2) checks,
reduces 1,171 tile/potential variables using 648 rows of rank 645. It fixes
597 tiles to zero and leaves 526 independent tile bits.

Closure uses four reachable-prefix flags per state of the 1,258-state
two-history composition. For prefix parities (a,b), a pair of tiles (i,j)
updates to (a XOR bit_i,b XOR bit_j). Each terminal forbids only completed
parities (1,0). If the first terminal emits an extra pair, the second
history consumes both its extra edge and its terminal; both bits are used.

Nonemptiness is exact: under the forest gauge, all complete scores vanish
iff every tile bit vanishes. Indeed every FST state has a zero-score forest
prefix and at least one valid terminal. If all complete scores vanish, its
terminal labels vanish; inserting any single edge before such a terminal
then forces that edge label to vanish. Thus the disjunction of the 526
remaining tile bits is equivalent to an actual finite accepted history.

The final CNF has 5,683 Boolean variables and 213,475 clauses. CaDiCaL
returned UNSAT after about 0.07 solver seconds. This status was **not**
taken on trust: `check_lrat.py` independently checked all 7,795 LRAT
additions, using 18,119 positive unit-propagation hints, through the empty
clause. It rejects unsupported negative RAT hints. Deletion requests are
ignored, which is sound because previously proved clauses remain true.

Hence no finite nonempty conditional XOR-parity invariant of this specified
carry-history form exists. This is an obstruction to an ansatz, not a
termination theorem for any decimal integer.

CNF SHA-256:
`da720bbb2202c14d961c777a594005132cd450ed8c8b610ae297539191c0fb4d`

LRAT SHA-256:
`b205af87cccefed26420399b7ab4b68f6012a09d9652aa115917d8f6e5298042`

## 2. Full two-state transformation monoid: unresolved

Each tile now carries any function {0,1}->{0,1}: identity, flip, reset-0,
or reset-1. Start in state 0, compose these functions along the complete
history, and accept terminal result 1. The same conditional safety and
closure rules apply. This strictly adds noninvertible behavior and is not
an arbitrary-group product.

The monoid gauge does **not** set tree maps to identity. If a_u and a_v are
permutations of the two control labels, transform a tile u->v by

    delta'_edge = a_v o delta_edge o a_u^{-1},
    delta'_terminal = delta_terminal o a_u^{-1}.

Initial permutations are identities. For each forest edge choose the child
permutation to make delta'_edge(0)=0. The value delta'_edge(1) remains free,
so both the identity and reset-0 map remain possible on a tree edge. This
normalization preserves all complete acceptance results and makes every
(FST state,control 0) reachable by an actual forest prefix.

Exact finite nonemptiness is encoded as follows. Either a terminal accepts
control 0 directly, or an accepted path has a last transition from control
0 to control 1. Its remaining edges all preserve control 1 until an
accepting terminal. A simple such suffix has at most 46 FST vertices.
Six-bit ranks enforce acyclic predecessor witnesses for this suffix,
starting at an actual tile with delta(0)=1 and ending at a terminal with
delta(1)=1. There is no arbitrary maximum integer size in this argument.

The full encoding has 13,365 variables and 449,130 clauses. CaDiCaL reached
the deliberately bounded 45-second limit and returned UNKNOWN. No SAT
candidate, UNSAT claim, or mathematical exclusion is reported. The large
incomplete proof trace was discarded; the encoding, log, and result remain.

A subsequently authorized **single 600-second discovery run** used exactly
the same CNF, without producing a proof trace. It also returned UNKNOWN at
its 600-second wall-clock limit (600.11 seconds including the driver). No
SAT assignment was produced, so no finite candidate was extracted. This
does not exclude the two-state monoid class. The original 45-second log and
result are preserved as `monoid_45s.log` and `monoid_45s_result.json`; the new
files are `monoid_600s.log` and `monoid_600s_result.json`.

The unchanged monoid CNF SHA-256 is
`fb4f0a042167ebe54a319c41b6cae1a44a79f113e0f365c16ff8c81fb9a52aaf`.
`continue_monoid.py` records SAT, if ever obtained, only as
`candidate_pending_root_audit`, even after its independent clause/product
checks and canonical decimal realization. An UNSAT discovery result would
remain `unsat_proof_pending` until an independently checked proof exists.

For any future SAT result, `monoid.py` independently computes the complete
safety and closure reachable products from the actual tile functions and
BFS-extracts a finite accepted canonical word, including its terminal. It
does not treat the solver's auxiliary reachability or rank variables as a
certificate of correctness.

## Reproduce

    python main_existence_attempt/conditional_score/parity.py 60 any
    python main_existence_attempt/conditional_score/check_lrat.py any
    python main_existence_attempt/conditional_score/monoid.py 45

The arbitrary-group conservation result does not settle the monoid model.
The parity result does not exclude larger finite scores, more control
states, noninvertible score updates, or additional carry-history rows.
