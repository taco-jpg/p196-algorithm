# Noncommutative carry-history attempt

This attempt does **not** prove decimal Lychrel existence. It gives an exact
obstruction to a proposed one-row noncommutative group-score certificate.

## Certificate sought

Let an arbitrary group element label each of the 872 edges and 251 terminal
tiles of the exact reverse-and-add folded transducer. For a valid pair-sum
word q, let S(q) be the ordered product of the labels along its unique history
q -> T(q), including the terminal label. We tried to require:

1. S(q)=e whenever T(q) is palindrome-producing;
2. S(T(q))=S(q) for every q;
3. S(q) is nonidentity for at least one finite q.

The third condition together with the first two would give a finite decimal
Lychrel witness after a finite number of initial steps. No such score exists
within this ansatz, for **any group**, finite or infinite.

We also tried the more general update S(T(q))=h^{-1}S(q)h with a fixed element
h in an arbitrary group. This also forces every complete score to be e.
Consequently changing from S3 to A5, or any other finite group, cannot help
this particular certificate.

## Exact all-length relations

The safety graph has 48 useful states, 464 edges, and 138 terminals. Write
p_u for the prefix product in safety state u. Its equations are:

    p_initial=e,
    p_v=p_u*g_k,
    p_u*g_terminal=e.

For the two-history product graph, write

    d_u=(prefix_current)^{-1}*prefix_next.

There are 1,258 useful states, 24,041 edges, and 3,521 terminals. Its equations
are:

    d_initial=e,
    d_v=g_current^{-1}*d_u*g_next,
    g_current_terminal^{-1}*d_u*next_terminal_product=e.

The next terminal product includes the extra next-history edge when the
first terminal emits an extra pair. This is retained in both implementations.

These state potentials are necessary as well as sufficient. For example,
fix any accepted suffix of a useful two-history state and denote its current
and next products by A and B. Equality of the complete scores gives

    prefix_current*A=prefix_next*B,
    d=A*B^{-1}.

Thus d is independent of the prefix reaching that state. The safety argument
is identical with the required complete product e. Reachability and
coaccessibility ensure a usable prefix and suffix exist for every retained
state. There is no maximum word length in these relations.

For conjugated update, replace each current-history tile g by h^{-1}gh in
the equations, and define d=(h^{-1}prefix_current*h)^{-1}prefix_next.

## Gauge fixing preserves every complete score

Choose a_u in the group for each of the 46 underlying FST states, with
a_0=a_1=e at the two possible start states. Transform an edge u->v and
terminal from u by:

    g_edge' = a_u^{-1}*g_edge*a_v,
    g_terminal' = a_u^{-1}*g_terminal.

All complete products are unchanged. A spanning forest from the two starts
has 44 edges; recursively choosing a_v=g_edge^{-1}a_u sets those 44 labels
to e. Therefore these identity constraints are without loss of generality.
Safety potentials transform by p'=p*a_x. Ordinary closure potentials
transform by d'=a_x^{-1}*d*a_y. For conjugated update the transformation is
d'=(h^{-1}a_x*h)^{-1}*d*a_y. Every defining equation is preserved.

More explicitly, put phi(z)=h^{-1}zh. For a closure edge the defining
relator R=phi(g_current)^{-1}d_u*g_next*d_v^{-1} transforms to
phi(a_current_destination)^{-1}R*phi(a_current_destination).
For a closure terminal its relator is unchanged, including when its next
product has both an extra edge and a terminal. The checker independently
verifies these identities by reducing words in distinct free generators;
it does not assume the untwisted argument applies.

## Exact elimination results

The gauge-fixed conservation presentation has 2,429 generators and 28,214
relations. Elementary free-group reduction and substitution eliminate all
2,429 generators, leaving no relations or generators.

The conjugacy presentation adds generator h. It eliminates the same 2,429
other generators and leaves h free, with no remaining relations. Every one
of the 1,123 gauge-fixed tile labels is e in both presentations, so every
complete history score is e before or after gauge fixing.

Every elimination in both certificates actually uses a **unit relator**
after earlier identity substitutions and cyclic conjugation reduction. Thus
the result uses only group cancellation, not commutativity, finite-group
enumeration, numerical optimization, an SMT status, or a general-purpose
group word-problem solver.

`check_certificate.py` independently replays each stored relation from the
original equations using only previously certified substitutions. It checks
the single occurrence of the eliminated generator, the exact solved word,
absence of circular definitions, identity of all original relations, and
identity of every tile. It also compares the abelianized group relations
against the already established additive safety/closure matrices, allowing
for the opposite safety-potential sign convention and duplicate initial
equalities. Both replay runs pass.

The seed196 and seed18887 products both reduce to e. More importantly,
**all** complete products do, so this is not a seed-specific obstruction.

## Automorphism update consequence

If an arbitrary automorphism phi of a group were used in place of conjugation,
embed that group into its semidirect product with the infinite cyclic group,
choosing the stable element h so that h^{-1}gh=phi(g). The same tile labels
would then satisfy the conjugacy equations. Their scores must be identity
in the larger group and hence in the original group. Thus every group
automorphism update is excluded too. The direct computation itself needs
only the fixed-conjugation equations stated above.

This does not exclude an arbitrary nonlinear update of the score, a
conditional score, a score retaining additional spatial or temporal memory,
or an invariant not expressed by one ordered product of these fixed tiles.
It does not establish that 196, 18887, or any other candidate reaches a
palindrome.

## Reproduction

    python main_existence_attempt/group_invariant/presentation.py
    python main_existence_attempt/group_invariant/check_certificate.py
    python main_existence_attempt/group_invariant/conjugacy.py
    python main_existence_attempt/group_invariant/check_certificate.py --conjugacy

Both searches and both checks each ran in less than one second in this
workspace. The JSON files contain the complete exact replay certificates
and SHA-256 hashes. No Lychrel witness was found.
