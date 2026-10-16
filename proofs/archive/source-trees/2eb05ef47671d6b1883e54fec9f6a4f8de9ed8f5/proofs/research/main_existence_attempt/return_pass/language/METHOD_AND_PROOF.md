# Exact correlated languages and inductive kernels

No finite decimal Lychrel witness is supplied. This note specifies a positive
certificate search and proves the meaning of its completed exclusion data.

Write a canonical folded pair word as `w=(p,c)`, where `p` lists outermost
digit-pair sums, and `c` is absent for even length or an even integer in
`0,2,...,18` for odd length. A nonempty `p` starts positively. With no pairs,
the center is positive. Let `G` be the exact pair-word reverse-add map.

Every canonical word has a positive integer realization: choose high digit
`min(q,9)` and low digit `max(q-9,0)` for each opposed pair, and halve its
center. Reverse-add depends on the pair sums, independently of these splits.
Let `B` be the exact palindrome-predecessor language: either every coefficient
is at most 9, or the outer coefficient is 11 and every coefficient is 0 or 11.
In the latter case an odd center must be zero.

## The positive certificate

Fix a deterministic pair transition table `delta`, initially at state zero.
A complete word belongs to class `(delta(0,p),c)`. Its center acceptance flags
are completely unrestricted. Thus a choice of accepted classes specifies an
entire regular language of canonical finite words, at every word length.

Make a finite directed graph on all realizable classes. There is an edge
`a -> b` iff some complete canonical word `w` lies in `a` and `G(w)` lies in
`b`. Mark a class unsafe if it contains a word of `B`. The greatest safe
inductive class set is obtained by deleting unsafe classes and repeatedly
deleting a class with any edge to a deleted class.

If the remaining set is nonempty, its words form a nonempty safe closed
language `L`: `L` avoids `B` and `G(L)` is contained in `L`. A shortest
accepted word gives a finite integer `n0`; then `n1=T(n0)` and every subsequent
iterate are nonpalindromic. Thus `n1` would be a finite Lychrel witness.
This requires complete graph coverage, canonical nonemptiness, and an
independent safety/closure audit. No completed search here leaves a class.

The edge graph is constructed by the exact outside-in carry transducer,
combined with one copy of `delta` for input and another for output. Its
backward high carry is checked at the actual center. Overflow uses a delayed
high digit and can emit one extra pair at an odd input center. Both branches
and every allowed center are included. A completed finite product covers
all finite word lengths; a state cap does not.

## Why an empty-kernel proof is independently checkable

Each deleted class has one stored canonical word. At rank zero, ordinary
integer reversal/addition takes that word's realization to a palindrome. At
positive rank, the actual numerical successor belongs to a class already
deleted at a lower rank. If an inductive class language accepted the former
class, it would accept this particular word and hence the latter class.
Induction on the stored ranks therefore forbids every listed class.

The independent checker does not import the discovery program or its carry
transducer. It reconstructs a decimal integer string for each word, computes
ordinary integer reversal/addition, classifies the actual resulting pair
word, and verifies every rank edge. It separately enumerates **all** canonical
classes reachable in the saved transition table, and requires the proof to
cover exactly that set. No solver status or sampled orbit supplies a proof.

This verification suffices to exclude every nonempty safe closed language
using that fixed transition table and arbitrary terminal flags. The graph
need not be trusted to establish an exclusion once this complete arithmetic
certificate has passed. It does not exclude different transition tables,
all automata below a state count, or decimal Lychrel numbers.

## Right-context observation automata

The first family records the vector

`O_k(w) = (1_B(w), 1_B(G(w)), ..., 1_B(G^k(w)))`.

Its minimized pair states are residual functions: two prefixes are identified
only when appending every possible pair suffix and center gives the same
observation vector. The implementation starts with the exact five-state `B`
machine. To add one observation, it takes the regular preimage under `G`,
determinizes all possible high-carry paths, pairs with the current `B` state,
and Moore-minimizes the eleven terminal output values. At a canonical center,
exactly one full carry path is valid, which fixes the next observation.
This construction is exact for arbitrary word lengths; 22,000 independent
integer controls per depth additionally checked its implementation.

These states retain full right-context correlations. There is no discarded
wake, moving cut, or identity `b_next >= b+overflow`. The previous finite
suffix impossibility proof therefore does not apply. This is also neither
an additive/group/XOR score nor a language defined by allowed individual
carry tiles. The finite kernel solves every acceptance choice on the whole
order-sensitive automaton at once.

The completed depth-four obstruction has a precise information collision.
The words `((6,13), no center)` and `((5,0,5,13,17), no center)` both reach
state 125 of the saved 75,311-state pair automaton. The first is the pair word
of 1675; the second has canonical realization 5,059,984,000. The supplied
class-elimination chain switches between different words in the same class.
It is **not** an ordinary reverse-add orbit. A finer positive invariant must
break at least one class identification in that finite chain; splitting this
one pair alone is not claimed sufficient.

## Tested image ancestry and safe ancestry

Ordinary image ancestry retains the structural restriction `w in G(C)`, where
`C` is all canonical words. Projecting the input labels of the exact carry
transducer gives a 47-state output NFA, including a final state for the extra
pair emitted at an odd overflow center. Its determinization has 481 subsets
and minimizes to 449 states. Products of this image observer with `D0` and
`D1` were fully searched. Center flags remain unrestricted, so any acceptance
rule using image membership is included in their exclusions.

Image membership is about the entire pair word, not one digit realization.
The integer 5,059,984,000 itself cannot equal `T(n)`: a nine-digit input is
too small, whereas a ten-digit input has output divisible by 11. This value
has residue 5 modulo 11. Nevertheless another realization of its pair word
has genuine two-step ancestry:

`1,513,900,000 -> 1,513,993,151 -> 3,027,986,302`.

The unique predecessor pair word is `(2,10,2,6,18)`, and its unique predecessor
is `(1,5,1,3,9)`, all of even length with no center. The latter is in `B`, and
the middle integer is a palindrome. Thus ordinary ancestry does not remove
the splice, but safe two-step ancestry does. Root independently verified
uniqueness by ordinary integer enumeration over all 3,580,398 canonical
pair words of the possible input lengths; see the root inverse audit files.

Define safe ancestry by `S0=C` and `S_(r+1)=G(S_r minus B)`. A word of `Sr`
has an actual r-step generating history avoiding palindromes at every
positive-time step. The safe-image construction takes the product of the
input-language DFA and the carry transducer, projects input symbols, trims
nonaccepting NFA states, and determinizes the output language. These are
exact language operations, not a test of one realization.

The one-step safe image was completed and its `D0` kernel excluded. The
two-step safe image has a completed finite NFA; determinization results and
any subsequent kernel status are recorded separately. Excluding the one
concrete splice is not a safe inductive language, and the NFA itself is not
claimed closed or palindrome-free. The unresolved positive object remains
a nonempty safe forward-closed sublanguage with a finite accepted word.
