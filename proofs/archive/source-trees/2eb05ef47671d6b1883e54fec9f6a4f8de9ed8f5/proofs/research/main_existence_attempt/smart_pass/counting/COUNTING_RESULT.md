# A complete finite obstruction to short uniform killing blocks

No finite decimal Lychrel seed or all-time first-hit estimate is proved here.
No asymptotic fiber contraction is proved. The positive existence goal remains
open in this branch.

The completed result is stronger than an unchecked prefix experiment: all
65,536 binary choices in an explicit 16-column block extend to genuine finite
50-digit words with three safe, no-overflow incoming iterates. Thus the
constant-rho certificate's 9-column killing bound cannot be extended directly
to arbitrary varying rho values. In fact, every uniform killing bound of
length at most 16 fails for this inverse-prefix automaton.

## Exact finite theorem

Let G be the canonical symmetric pair-sum map. Put

    P = (11, 2, 1, 1, 8, 2),
    R = (2, 8, 5, 6, 5, 4, 3, 5, 6, 4, 5, 3, 4, 6, 4, 4).

For each b in {0,1}^16 there is a three-symbol correction C_b such that the
symmetric word with half-word

    half(q3) = P, (R_i + 9*b_i for i=1,...,16), C_b

has width 50 and admits three canonical positive predecessors

    G(q0)=q1, G(q1)=q2, G(q2)=q3,

all with no overflow. Each of q0,q1,q2,q3 contains the central coefficient
18, and all four are palindrome-avoiding pair-sum states. The q0 are distinct.
A canonical decimal realization of q0 has outer digit sum 1, so it is itself
nonpalindromic. Its first four reverse-and-add outputs are also nonpalindromic.

This is a finite family and a finite avoidance claim. The corrections C_b
can differ with b. In particular the theorem does NOT assert that all 65,536
q3 have one common G-image, and it does not establish full asymptotic rate 2
inside any single restricted overflow fiber.

## Exact inverse machine

For one no-overflow inverse layer, a state (a,b) records the low entering
carry and high outgoing carry. Given target coefficient s, each inverse
edge is obtained by choosing x in {0,...,18} and b' in {0,1} and checking

    a' = floor((x+a)/10),
    b  = floor((x+b')/10),
    s  = ((x+a) mod 10) + ((x+b') mod 10).

The new state is (a',b'), and x is the predecessor coefficient. Compose
three such layers. There are 4^3=64 joint carry states.

For s outside {0,9,18}, a single layer has at most one edge, and its emitted
coefficient is never 9. A second inverse layer is therefore deterministic
as well: targets 0 and 18 can delete an edge, but cannot branch. Consequently
all paths produced from one state share their first two carry states, and
uncertainty is confined to a subset of the four third-layer carry states.
There are at most 16*(2^4-1)=240 nonempty determinized states.

Independent arithmetic enumeration finds every one of these 240 states
reachable from a canonical positive outer prefix using coefficients in
{1,...,8,10,...,17}. The saved table contains all 240*16=3,840 deterministic
transitions, and the independent checker reconstructs every transition
from the equations above.

After reading P from the three zero boundary states, with positivity
imposed on all three emitted outer coefficients, the possible carry states
are exactly

    ((0,1), (1,1), c),  c in {00,01,10,11}.

This is group 7, represented by the 64-bit mask 4026531840. P is a shortest
positive outer prefix reaching this subset under the specified alphabet.

Read R from outside to inside. At position i, take either coefficient R_i
or R_i+9. The distinct nonempty inverse subsets after all choices at each
successive depth have sizes

    1, 2, 4, 6, 9, 12, 17, 25, 36, 58, 79, 109, 142, 169, 192, 211, 228.

The empty subset never occurs. These complete collections are saved in
independent_witness_audit.json; this verifies all 2^16 binary choices
without confusing a count of inverse paths with a count of different words.

Each of the 228 final subsets reaches the all-one joint carry state by
reading at most two further coefficients. The finite completion table
records such a correction for every subset. Pad each correction with 18s
to total length three. The last 18 emits coefficient 18 in all three
inverse layers and preserves the all-one state. Reflect the half-words.
All center carries then match, every ancestor word is canonical, and the
central 18 is present at every history level. This proves the finite theorem.

The complete palindrome-predecessor criterion already proved in this
project says that an output is palindromic exactly when all pair-sum
coefficients are at most 9, or when the outer coefficient is 11 and all
coefficients are in {0,11}. The central 18 excludes both cases.

## Solver result and independent validation

The search uses the dual of the collection game. Let D be its 240 nonempty
states, let delta be the deterministic transition, and define

    S_empty = D,
    S_(y w) = {v in D : delta(v,y) and delta(v,y+9) both belong to S_w}.

A missing transition is outside every S. Induction gives: v belongs to
S_w if and only if every binary lift of the rho-word w has a nonempty
inverse subset from v. Only 240 Boolean viability flags per position are
needed in the SAT formula. The final query asks whether any of the 16
maximal four-element subsets survives; smaller subsets are dominated.

Exact SAT models were obtained at every length 1 through 16. Their words
are saved in rho_horizon_sat.json, and independent_witness_audit.py replays
all sixteen models from the arithmetic equations. The length-17 query
returned UNKNOWN after 60.000349 seconds, with reason 'canceled'. The exact
query is preserved in rho_horizon_17_unknown.smt2. UNKNOWN is not UNSAT.

The independent checker also explicitly constructs and verifies all
65,536 reflected width-50 families, including all three no-overflow
transitions, and checks three literal decimal integer samples using ordinary
addition and reversal. The checker imports none of the prior inverse-map
implementations and does not call a SAT solver.

Run the completed finite certificate with

    python main_existence_attempt/smart_pass/counting/independent_witness_audit.py

The local transition table is reconstructed independently and compared
with compact_transitions.txt. The JSON file stores all relevant inverse
collections, the completion table, sample seeds and literal orbits.

To replay the bounded solver search, install `z3-solver` in the active Python
environment and run

    python main_existence_attempt/smart_pass/counting/rho_horizon_sat.py --max-depth 17 --timeout 60000

A solver run may return a different valid model or take different time.
The already saved length-16 certificate remains independent of that search.

## Completed and incomplete enumeration scopes

The separate dual antichain calculation completed exactly through length 7.
The maximum-antichain sizes, including depth zero, are

    1, 6, 36, 288, 2086, 10520, 38148, 122824.

The maximum numbers of viable DFA states in one such set are

    240, 235, 229, 217, 196, 180, 156, 132.

The exact final antichain and the per-level summaries are preserved in
 dual_antichain_checkpoint.pkl.gz. Its SHA-256 and precise scope are in
exploration_status.json. At depth 8, 891,073 distinct raw successor sets
were obtained, but maximality reduction was interrupted. No depth-8
antichain result is claimed.

The earlier forward collection BFS stopped at 500,001 states after
processing 161,802. The compact DFS stopped at 5,000,001 states while its
first maximal root was unfinished. Neither capped computation establishes
termination, a cycle, or a contraction. Their uncompleted in-memory state
sets were not preserved; the reproducible programs and cap metadata are.

No process from this branch is left running. Nothing in these results
controls all first-hit times for one fixed finite seed ensemble. The new
finite obstruction is not a bridge from finite avoidance to a finite
Lychrel witness.
