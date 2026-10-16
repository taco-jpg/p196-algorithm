## Result

For every target decimal width D >= 2, the number of distinct positive ordinary reverse-add predecessors is at most `9 * 10^(D/2 - 1)`, and an explicitly defined complete predecessor list attains the bound at every width. The one-digit sharp bound is 1, attained by target 2. Nat division/subtraction and all short-width cases are explicit.

`Agent101.Maximum.all_width_inverse_maximum` states both the universal upper bound for every Nodup finite predecessor sublist and a full all-natural-number membership iff for an attaining list. `one_digit_inverse_maximum` supplies the remaining target width. This quantifies ordinary `Lychrel196.step` integers, including both possible input widths.

## Source and dependencies

Four new modules export 36 theorems and five definitions. Complete mathematical source: `0fcbe9973659f178e9c834c68d45f660241d6fbd`; tree `15556f672ab08a0198d3bd334aa034741572c1e6`. Original Agent105 cross-width modules are reused unchanged from5923015f. Bounds directly imports Agent2's original public nodup-subset cardinality theorem; original dependency bytes and provenance are retained. The existing numeric fibers and Boolean filter partition are reused from PR85/PR114. This PR is stacked on PR114 pending designated integration.

The new profile extraction is existential finite-list reconstruction. Agent105/session9df76b separately owns computational projections and executable arbitrary-target predecessor enumeration; that scope is not taken over here.

## Verification status

All four final sources have completed actual author Lean4.19.0 `--trust=0` compilation and their public axiom checks. Only `propext`, `Classical.choice`, and `Quot.sound` occur. A genuine nonauthor has independently read all four sources and found no semantic gap; source-only receipts explicitly do not claim independent execution. The 17-module source-pinned full fresh rebuild and exhaustive module-origin audit are the remaining gate. This PR stays draft until that gate and final evidence publication finish.

Successful and failed development attempts are retained. The earlier private copy of an existing cardinality helper was replaced with direct original reuse; superseded attempts remain outside the accepted closure. No sorry/admit, new axioms, native_decide, or altered reverse-add semantics are accepted.

This supplies an inverse branching bound. It does not classify all maximizers, prove an infinite palindrome-free orbit, or resolve196. Agent11 owns serialized main integration; Agent101 holds no main-write slot.