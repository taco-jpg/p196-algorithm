OUTER-PREFIX INVARIANTS WITH NO PRESCRIBED CLOCK

No Lychrel witness was found. The greatest universal safe trap is empty
at every tested width k=1,...,5. Unlike the previous maximal-clock search,
this search admits every overflow schedule and every canonical q prefix.

Let q_i=d_i+d_(L-1-i), with digits ordered from low to high and L>=2k.
Keep the outer prefix q_0,...,q_(k-1), where q_0>0 and 0<=q_i<=18.
For incoming interior carry b in {0,1}, normalize this prefix forward
from low carry0, obtaining digits l_i. Normalize it backward from b,
obtaining high-side digits u_i and final overflow h. Exact next prefixes:

  h=0: q'_i=l_i+u_i.
  h=1: q'_0=l_0+1; q'_i=l_i+u_(i-1) for 1<=i<k.

The interior supplies exactly one of these two carries. Conversely each
carry is realized by the canonical full word prefix ++ [18b] ++ reverse
prefix, because the central even coefficient 0 or18 resets the carry
to b independently of the low carry. Thus no hypothetical branch is
introduced when testing closure of a language containing all completions
of an outer prefix, with arbitrary widths L>=2k.

A prefix makes every completion avoid a palindrome on the next addition
exactly when it contains a coefficient>=10 and is not entirely in {0,11}
with outer coefficient11. The exact two palindrome-predecessor patterns
are q entirely<=9, or q_0=11 with all coefficients in {0,11}. If neither
pattern can occur in the prefix, neither can occur in a completion. If
one can occur, completing with an even central zero realizes it.

For a set S of such safe prefixes, requiring both successor prefixes to
lie in S is necessary and sufficient for universal prefix closure. A
nonempty S would give a finite decimal seed: realize any prefix in S,
then apply one ordinary reverse-and-add step. The resulting orbit would
avoid palindromes by induction, since widths never decrease.

The program computes the greatest possible S by deleting every unsafe
prefix, then every prefix with at least one deleted successor. It checks
an explicit descending rank along one successor for every deleted safe
state, and both closure obligations for every surviving state. The set
of survivors is empty in each complete finite state space:

  k   canonical prefixes   largest deletion rank
  1                   18                       1
  2                  342                       7
  3                6,498                      13
  4              123,462                      20
  5            2,345,778                      27

This excludes only languages determined by at most five outer mirrored
digit sums, closed for arbitrary interiors of length at least2k. It does
not exclude longer prefixes, interior restrictions, correlated carry
histories, variable-time constructions, or any actual Lychrel candidate.
The descending ranks are adversarial prefix escape bounds, not bounds
on when a fixed integer reaches a palindrome.

Independent ordinary-integer controls verify every prefix transition
for widths1,2,3 with both realized incoming carries (13,716 controls).
The column equations above justify the general prefix map. These are
finite computational checks and written arguments, not Lean theorems.

Reproduce:
  g++ -std=c++17 -O3 -Wall -Wextra search.cpp -o prefix-search
  ./prefix-search > results.jsonl
  python3 numeric_control.py
