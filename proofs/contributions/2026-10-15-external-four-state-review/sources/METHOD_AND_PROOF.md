# Whole-word regular invariant synthesis with unrestricted overflow

## Result and exact domain

The primary four-state Boolean instance is UNSAT. Its independent LRAT
replay and independent arithmetic/encoding audit are recorded separately.
The claimed consequence is only the following bounded-state exclusion:

> No nonempty safe forward-closed language of canonical decimal folded
> words is recognized by a complete deterministic pair-reading automaton
> with at most four states and eleven independent center/end predicates.

This does not exclude arbitrary regular languages. It supplies no decimal
Lychrel witness and no termination proof for 196. Overflow and nonoverflow
are both permitted at every update; no temporal clock, starting integer,
or fixed observation partition is prescribed.

A folded word is `(p,c)`, where `p` is a finite list in `0,...,18`, and
`c` is absent or belongs to `{0,2,...,18}`. If p is nonempty its first
symbol is positive. If p is empty, c is positive. Its full symmetric
coefficient word is `p,c,reverse(p)` when c exists, and `p,reverse(p)`
otherwise. Canonical ordinary realization uses high digits `min(q,9)`,
low digits `max(q-9,0)`, and middle digit c/2. For every realization n,
the value of the full coefficient polynomial at ten is `T(n)`, where
`T(n)=n+reverse(n)`. Consequently its exact next folded word G is unique.

The automaton has a distinguished initial state 0, a complete deterministic
transition function `delta:{0,...,N-1} x {0,...,18}->{0,...,N-1}`, and
predicates `F(s,c)` for the eleven possible centers, including absence.
It accepts `(p,c)` exactly when `F(delta*(0,p),c)` holds. Only canonical
words are in its semantic domain; behavior on noncanonical words imposes
no acceptance or safety obligation. The number N counts the initial state
and any dead state. Terminal predicates are not eleven additional reading
states. Every ordinary regular language over pair symbols followed by one
center marker has such a representation, although its minimal N may exceed
four. A partial DFA with four live states and an extra dead state has five
states under this convention and is not excluded by the four-state result.
An automaton with fewer than four states can be padded with unreachable
states to give one with exactly four states, so the exact four-state
UNSAT result also excludes every smaller number under this convention.

## Safety and the finite monitor

Write B for the folded words whose *next ordinary output* is a palindrome.
The previously proved all-width classification is

`B = {all coefficients <=9} union {outer coefficient 11, all coefficients in {0,11}}`.

The second class has absent or zero center because the center is even.
The classification and its carry proof are in
`../../renewal_pass/seam_audit/METHOD_AND_PROOF.md`; that source is pinned
by the arithmetic audit. This use of B is not a test for whether the chosen
realization at time zero itself is a palindrome.

The safety monitor has four states: empty; nonempty and all symbols <=9;
nonempty with first symbol 11 and every symbol in {0,11}; neither class.
Its first pair transition excludes symbol zero. Its terminal test covers
the one-digit case and both parity choices. Boolean variables S(s,m)
contain every reachable automaton/monitor product state: the initial pair
is asserted, and every product edge is a Horn implication. Any product
terminal in B is forbidden to have its automaton end predicate true.
Thus every satisfying assignment recognizes a safe language. Conversely,
for a safe language, setting S to the actual reachable set satisfies all
these clauses. The auxiliaries are overapproximations of reachability,
not guessed single paths or locally selectable carries.

## The exact outside-in whole-word transducer

A transducer state is `(h,a,b,t,started)`. Here h is the proposed whole
overflow bit, a is the low-side incoming carry, b the high-side outgoing
carry, and t is the delayed high output digit if h=1. Initial states are
`(0,0,0,-1,false)` and `(1,0,1,1,false)`.

For each source pair q and inward high carry b' in {0,1}, retain the edge
exactly when `floor((q+b')/10)=b`. Define

`a'=floor((q+a)/10), ell=(q+a) mod 10, u=(q+b') mod 10`.

The emitted pair is `ell+u` if h=0 and `ell+t` if h=1. The next state is
`(h,a',b',u if h=1 else -1,true)`. The first q must be positive.

For an absent center, retain termination iff a=b; the output center is
absent for h=0 and 2t for h=1. For a present center c, retain termination
iff `floor((c+a)/10)=b`. For h=0 the output center is
`2*((c+a) mod 10)`. For h=1 emit one additional pair
`((c+a) mod 10)+t` and use absent output center. Empty p with absent or
zero center is rejected. These rules give 46 states, 872 ordinary edges,
and 251 terminal cases.

These are the two ends of the same ordinary decimal column addition.
Terminal matching joins the inward carries, so an accepting complete path
exists precisely for the actual overflow and actual full carry sequence.
All other local choices die at the center. Every canonical input has one
accepting path and the output is G of that input. Thus no independently
chosen local control sequence is promoted to a realizable orbit.

Closure variables R(x,s,t) contain every reachable product of this
transducer state x, input automaton state s, and output automaton state t.
Both initial transducer states are asserted with automaton states (0,0).
Each transducer edge gives

`R(x,s,t) and delta(s,q)=s' and delta(t,o)=t' => R(y,s',t')`.

Each valid terminal gives `R and F(input_state,input_center) =>
F(output_state,output_center)`, including the extra pair transition for an
odd source with overflow. Hence all accepted canonical inputs have accepted
images. Conversely, for a closed language, assigning R to exact reachable
products satisfies every terminal clause. The CNF is not imposing closure
on incomplete paths, free carry controls, or noncanonical words.

## Exact nonemptiness bound

If any accepted word has no pairs, one of the positive-center predicates
at state 0 supplies it directly. Otherwise, take an accepted canonical word
with the least number m of pairs. Its first symbol is positive. If m>N,
then the m automaton states immediately after pair positions 1,...,m
repeat. Delete the segment between two equal such states. This preserves
the first symbol, final automaton state, and center and gives a shorter
accepted canonical word, a contradiction. Therefore m<=N.

The witness encoding selects N transitions. The first reads a pair in
1,...,18; each later choice reads a pair in 0,...,18 or a padding symbol
19 that leaves the automaton state unchanged. Each witness state and
letter choice is exactly one. The final witness state has an accepted
center. A single final disjunction also permits an accepted one-digit
word. Thus this part is satisfiable exactly when the canonical language
is nonempty, not merely when an unreachable DFA state is marked accepting.
The pair-path auxiliaries remain satisfiable when the one-digit disjunct
is the witness: choose any positive first pair, pad the remaining positions,
and set every witness-end selector false. That arbitrary path need not be
accepted when the one-digit predicate already satisfies the final clause.

The language must in fact be infinite. Its integer rank Q(10) strictly
increases under G: `G(Q)(10)=T(Q(10))>Q(10)` for every positive Q(10).
A nonempty finite closed set would contain a rank-maximal member and its
strictly larger image, which is impossible. This elementary fact alone
does not exclude infinite regular languages.

## Redundant terminating-word exclusions

The primary and corroborating instances include every canonical folded
word with at most two pairs whose canonical realization is observed to
reach a palindrome within sixty positive additions. This is a complete
enumeration of a specified finite input range, with 3,706 terminating
labels among 3,969 inputs. The 263 unclassified inputs impose no negative
label. Every full ordinary-integer trajectory for a negative label is
preserved in `*.terminating.json.gz` and independently replayed.

If a language is safe and closed it cannot accept any of these words:
closure would retain its successive folded words until the predecessor
of the displayed positive-time palindrome, contradicting safety. This
argument applies to every realization because its first ordinary output
is fixed by the folded word. No conjectured Lychrel status is used.

These extra clauses can remove no genuine solution and do not change the
model's semantic scope. They are not a finite observation approximation
to closure; the full all-length safety and closure obligations remain in
the formula.

## SAT evidence, provenance, and limits

`synthesize_dfa.py` is the exact source. The primary call is
`build(4,2,symmetry=False)`, exposed as
`--states 4 --terminating-depth 2 --no-symmetry --stem dfa4_neg2`.
The resulting CNF has 2,682 variables and 263,792 clauses. The archived
primary CNF is byte-identical to a fresh regeneration. CaDiCaL reported
UNSAT in 35.37 seconds and emitted the full text LRAT proof.

The corroborating instance sets `symmetry=True` and has 263,944 clauses.
Its additional clauses order the first appearance of noninitial target
state names. They only remove equivalent state renamings; inaccessible
states may be completed by self-loops. It reported UNSAT in 5.84 seconds.
The main exclusion does not depend on this symmetry argument.

The positive-hint LRAT checker imports no solver or generator. It verifies
each added clause using explicit unit-propagation hints and requires a
verified empty clause; unsupported negative RAT hints cause rejection.
The separate semantic checker audits the arithmetic and CNF clause families.
Hashes bind the complete CNFs, proofs, and arithmetic evidence. A solver
status alone is not the claimed proof.

A five-state symmetric run started before the four-state audit completed,
with the same 180-second cap. It returned UNKNOWN at 180.00 seconds;
its full CNF, log, and incomplete proof trace are preserved. The trace is
not a refutation, and there is no five-state exclusion.
No larger-state run is implied. The remaining positive task is an actual
nonempty semantic language with universal safety and successor coverage,
possibly using at least five pair-reading states or a richer recursive
description. This result supplies no instance of that language.
