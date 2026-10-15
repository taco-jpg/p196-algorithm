# Independent source review of the four-state language exclusion

**PASS for the all-width mathematical reduction and source encoding.** The
exact reviewed checkpoint is
`fbbef30681848aff9e4ff3d34fc01b9ca2167f9d`. This review reads the complete
method, CNF generator, independent encoding checker, positive-RUP LRAT
checker, and coordination handoff. Ten small exact source/report files are
preserved in `sources/`; each Git blob identity was independently compared
with the retrieved commit tree. The reviewed source hashes also match the
external root's retained frozen replay receipt.

This is not a third replay of the 27,745,823 LRAT hints or another full
clause regeneration. The archived reports record both completed checks and
the verified empty clause. The verdict here concerns their mathematical
interpretation and source implementation; it does not claim Lean
formalization of the reduction or LRAT checker.

## Exact automaton class

The claim is correctly restricted to nonempty, safe, forward-closed
languages of canonical folded decimal coefficient words accepted by a
complete deterministic automaton with at most four pair-reading states
and eleven independent terminal predicates. Initial and dead states count
toward the four; the terminal predicates are not additional reading states.
Behavior on noncanonical words is irrelevant. A partial automaton with four
live states and an extra dead state lies outside this bound.

The pair alphabet is `0..18`, with a positive first pair whenever pairs
exist. Centers are absent or even values `0..18`; without pairs only a
positive center is valid. These conditions are exactly the positivity and
odd-center parity conditions for canonical pair-word realization. The
stated digit construction realizes every such word. Every realization has
the same first reverse-and-add value, namely evaluation of its coefficient
word at ten, so its next folded word is independent of the realization.

The primary instance has no state-renaming constraints. Therefore its
exclusion does not depend on the supplementary naming argument. Padding a
smaller complete automaton with unreachable states preserves its canonical
language and gives a four-state instance. The conclusion consequently
covers smaller state counts without changing the nonemptiness convention.

## All-width transduction

The transducer's low-side bit is the incoming carry at the next unread low
column, and its high-side bit is the outgoing carry at the next unread high
column. Selecting an inward high carry is allowed exactly when the complete
high-column division equation holds. Low carries propagate forward. Thus
these choices describe the two ends of one ordinary addition, rather than
independent temporal controls.

At an absent center, matching the two frontier carries joins the complete
carry chain. At a present center, its division equation joins them. This
gives a bijection between accepting paths and complete ordinary carry
sequences. Ordinary carrying from initial zero is unique, so only the actual
overflow guess admits an accepting complete path. Prefix guesses which
cannot be completed impose no terminal acceptance obligation.

The overflow shift is implemented correctly. Without overflow, each source
pair produces the sum of its two normalized digits. With overflow, its low
digit pairs with the preceding high digit, starting from the appended
terminal one. An even-width source then leaves a doubled delayed digit as
the output center; an odd-width source emits the additional pair joining
the normalized center and delayed high digit, with no output center.
The zero-pair case also checks: positive even centers below ten remain
one-digit outputs, while centers at least ten emit a two-digit pair. Absent
and zero centers at zero pair length are explicitly rejected.

For a canonical input, positivity of its ordinary normalized leading digit
ensures that the accepted transducer output is canonical. No noncanonical
output path is mistakenly treated as a genuine successor merely because
it is locally reachable.

## Safety and closure clauses

The four-state safety monitor exactly recognizes the two known
immediate-palindrome predecessor classes. Its empty state handles positive
one-digit centers separately. Its other states retain the all-small class,
the positive-outer-eleven/all-zero-or-eleven class, or neither. The even
center restriction correctly makes zero the only present center of the
second class. The first-pair zero exclusion and invalid empty terminals
are implemented in both the source and independent reconstruction.

Safety product variables are an inductively closed reachable-state
overapproximation. Every real prefix is forced into them by the initial
unit and Horn transition clauses, so all forbidden accepted terminals are
excluded. Conversely, for a safe automaton the exact reachable set satisfies
the auxiliaries. No path is selected independently for each word.

Closure variables similarly track the complete product of a transducer
state, input automaton state, and output automaton state. Deterministic
transition variables force every actual product edge. Terminal clauses
require accepted output exactly when the corresponding complete input is
accepted, including the extra output pair in the odd overflow branch.
The center equations are essential: closure is not imposed on arbitrary
unmatched carry guesses. Conversely, the exact product-reachable set of
a closed language satisfies these clauses. These arguments hold at every
word length; the finite controls are implementation checks, not a substitute
for that universal argument.

## Nonemptiness and certified exclusions

The shortest accepted canonical word with positive pair length has at most
`N` pairs. If it had more, two states *after* pair positions 1 through `m`
would repeat. Deleting the intervening segment preserves the positive first
pair, terminal state, and center. The proof does not use a potentially
invalid deletion through the initial state that could remove the only
positive first symbol.

The witness encoding realizes this bound. It reads a positive first pair
and then ordinary pair symbols or state-preserving padding, with exactly
one letter and state at each step. Deleting padding gives an actual shorter
canonical word. End selectors require its actual terminal state to accept
some center. A separate disjunct covers accepted positive one-digit words.
When that disjunct witnesses nonemptiness, the otherwise unused path
auxiliaries remain satisfiable: a complete automaton has an arbitrary
positive-first path and all path-end selectors may be false.

Every additional negative label has a retained positive-time palindrome
trajectory. Safety and closure forbid accepting it: closure reaches the
predecessor of that palindrome, where safety fails. Because the first
ordinary output depends only on the folded word, using one canonical
realization labels the entire folded word soundly. The 263 cases still
unknown after sixty additions add no exclusions. These clauses are redundant
consequences of the desired invariant, not an empirical replacement for
closure or an assumption of eventual termination.

## Certificate interpretation and limits

The independent encoding checker reconstructs all semantic clause families
from the saved variable-name bijection and compares clause multisets. The
generator's one-hot determinism, witness constraints, Horn products, and
negative-prefix evaluation agree with the written reduction. The primary
metadata and both archived check reports identify the same 2,682-variable,
263,792-clause CNF and its SHA-256 digest.

The LRAT checker validates each added clause by contradiction under its
negation using positive unit-propagation hints. It rejects missing/deleted
hint clauses, nonunit hints, satisfied hints, and unsupported negative RAT
hints, and requires a verified empty clause. Its handling of tautological
added clauses and deletions is sound. The recorded successful certificate
therefore supports unsatisfiability of the exact CNF; the separate all-width
argument above supplies the bounded-state language consequence.

The strictly increasing coefficient-word value under an actual update also
correctly shows that any nonempty closed language would be infinite. It does
not exclude an infinite regular language by itself. The result excludes only
the stated four-state class. The five-state capped run and the general
regular-language problem remain **UNKNOWN**; no positive invariant, Lychrel
witness, or conclusion about eventual termination of 196 is supplied.
