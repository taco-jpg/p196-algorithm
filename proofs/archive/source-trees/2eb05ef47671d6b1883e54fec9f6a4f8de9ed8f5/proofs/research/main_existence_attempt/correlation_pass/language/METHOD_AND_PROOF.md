# Correlated configurations, refinement, and exact obstructions

Let C be the canonical folded decimal pair words and G their exact
reverse-add map. Let B be the words whose next ordinary reverse-add output
is a palindrome. A positive certificate would be a nonempty regular
language L contained in C, with `L intersect B = empty` and `G(L) subset L`.
No such language is certified here.

## Complete configuration acceptance

Let N be the exact saved safe-two-ancestry NFA. For a pair prefix p, write
`Q(p)` for its entire reachable subset, including states not accepting at the
actual center. This retains correlations that terminal-flag selection loses.
The center is always part of the complete-word class.

For depth four let R4(p) be the saved minimized pair state observing
`B(w), B(G(w)), ..., B(G^4(w))` for every possible suffix and center. Define
R5, R6, ... by the exact carry-observer extension: retain the current B
observer state and every unresolved high-carry path, together with the
previous-level observer state of its emitted output pair prefix. These raw
states form finite deterministic machines. The implementation constructs
only states and transitions actually needed; it does not infer emptiness
from an unbuilt transition.

The complete class is

`K_k(p,c) = (Q(p), Rk(p), c)`.

Allow completely arbitrary acceptance choices on these classes. This
permits negative tests and arbitrary Boolean correlations on the whole NFA
configuration, not only positive conjunctions, existential paths, terminal
flags, or ancestry membership. Keeping the unminimized observer residuals
at depths above four makes this family at least as discriminating as the
corresponding minimized observation machine.

**Collision obstruction theorem.** Suppose u and v are canonical words,
`K_k(u)=K_k(v)`, and ordinary reverse-add from a realization of v first
reaches a palindrome at a finite positive time h. No safe forward-closed
union of Kk classes contains u.

Proof: acceptance of u accepts its entire class and therefore v. Forward
closure forces `G^(h-1)(v)` into the language. That word belongs to B, which
contradicts safety. This argument imposes no bound on the lengths of other
accepted words. It does not assert that u itself terminates.

If u is a trace word of 196 at time t, closure also forbids accepting any
earlier trace word. This is not an exclusion of every class, every possible
seed, or an invariant entered after the last excluded time.

## Counterexample-guided refinements

`correlated_cegar.py` keeps full Q(p) throughout. It first searches with R4,
then independently tests the same candidate words against successively finer
raw observation residuals through R10. Concrete terminating collisions force
rejection of the affected class; distinguishing residuals repair a particular
collision but do not prove closure of the remaining classes.

The first run completely enumerated all canonical pair prefixes through
five pairs. Their count is

`1 + 18*(1 + 19 + 19^2 + 19^3 + 19^4) = 2,476,099`.

The leading pair is positive, and subsequent pairs range from zero through
eighteen. The previous 8,396 path witnesses supplied additional candidate
prefixes; all new claims were reclassified using entire configurations.
The second run's six-pair range was interrupted at its stated 100-second
limit. Only actual saved collisions are proved in that range. Progress
counts do not imply an exhaustive search or any remaining-class theorem.

For the explicit D4 collision, independent enumeration through three pairs
finds no shorter representative at all, and only `(18,17,17)` at three
pairs. This proves minimum prefix length and uniqueness, not merely the
smallest terminating witness observed. Equality of D4 residuals proves that
no observation depth at most four separates the prefixes. Ordinary
arithmetic after replacing the center by zero gives differing sixth-output
palindromicity, so depth five is the first separating observation depth.

## Independent replay

`check_correlated_collisions.py` imports neither discovery code nor the carry
transducer module. It reconstructs NFA subsets from the saved adjacency
table and independently checks all centers and S2 accepting masks. It
recomputes the 196 trace with digit-by-digit integer reversal.

For observations above depth four, the checker expands complete emitted
prefixes literally along each possible high-carry history, recursively
classifies those prefixes, and compares immutable residual signatures. It
does not use discovery state ids, cached discovery transitions, or a claimed
minimized table. Each terminating witness is then replayed with ordinary
integer arithmetic, requiring no earlier palindrome than the saved first
hit. Thus the exact full-correlation collision and its arithmetic consequence
are checked separately. The decimal carry equations themselves are the
standard outside-in equations already specified in the preceding pass.

The source NFA and D4 tables are immutable audited inputs from the prior
pass. Their cryptographic hashes and the certificate hashes appear in each
replay report. The completed shorter-run enumeration cardinality is checked
independently. No exhaustive cardinality is claimed for the partial length-six
range.

## Positive conjunctions and antichains

For another possible synthesis family, allow an arbitrary positive Boolean
formula in predicates `s in Q(p)`, separately for each D0 state and center.
Any conjunction of any number of NFA residual states is permitted. This
strictly exceeds the former union-of-terminal-components model.

NFA determinized transitions preserve inclusion:

`A subset B implies delta(A,q) subset delta(B,q)`.

Within a fixed observer state, a reachable superset therefore covers the
future transitions of a smaller configuration for downward-reachability
exploration. The search keeps only undominated reachable configurations and
stores a real prefix for each. An exact completion would satisfy:

1. The initial configuration is covered.
2. Each retained configuration has an actual canonical-prefix witness.
3. Every canonical labeled successor is covered by a retained configuration
   in the successor observer state.

Induction would then prove that every reachable configuration lies below a
retained one. If, additionally, every retained complete-word class had an
exact terminating representative, monotonicity of a positive acceptance
formula would exclude the entire positive Boolean family: accepting a
smaller configuration would also accept a covered terminating superset.
Neither premise of that global exclusion is claimed here. The exploration
timed out before the coverage condition was checked to completion.

`check_antichain.py` proves the narrower statement actually supported by the
snapshot: all 65,170 entries are reachable and are pairwise incomparable
within their observer state. Strict superset checks are complete because a
superset must occur in the inverted list of every member of the smaller
configuration; choosing the shortest such list cannot omit one. Equal-size
distinct sets cannot contain each other. A later configuration might contain
several snapshot entries, so the count is not a lower bound for the final
maximal antichain or for minimized DFA size.

## Explicit closure obligation

The natural regular candidate F10 retains S2 membership and excludes any
word with a palindrome among its next eleven outputs. Its safety is
immediate. Closure requires the twelfth output to be nonpalindromic as well.
The independently checked transition `9948 -> 18447` fails exactly that
condition: both words lie in S2, and their first palindrome times are twelve
and eleven. Checking all ordinary integers below 1,000 proves that this
counterexample has minimum decimal width for this candidate.

This failed closure test prevents interpreting unexcluded target classes or
an ancestry-plus-finite-future filter as a positive invariant. The unresolved
object remains a genuinely nonempty language with a complete universal
forward-closure proof.
