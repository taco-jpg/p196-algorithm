# Agent #4 — complementary-bulk verification checkpoint

This is AI-assisted research. No claim of a solution of P196, external novelty, independent human review, or an actual persistent complementary-band cycle is made.

## Accepted finite-domain result

The complete trimmed canonical state domain

    I = 2*len(B) + 2*len(A) + len(C) <= 6

contains **637,632 states** over all eight periodic even phases. Its induced functional graph has **15,260 internal edges**, **622,372 exits**, and **no directed cycle**. Every state leaves this domain within at most **five transitions**; the bound is attained.

An exit says only that the next interface has I>6. It does not establish eventual escape, exclude a later return through larger states, bound an actual orbit's lifetime, or prove that 196 avoids palindromes.

`search.py` produces a positive integer rank for every vertex. `replay.py` independently computes all 637,632 transitions using an ordinary integer realization, decimal string reversal, integer addition, and geometric extraction of the next interfaces. It does not call `quotient.step` or traverse the producer's graph. It verifies rank=1 on every exit and rank(source)=rank(target)+1 on every internal edge. The replay shares only the state type and enumeration with the producer; enumeration cardinality is independently checked by the formula below.

The exact two-gap, all-length interpretation depends on the written identity in `../../contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, initially inspected at main `a71d6e79b009da691e2d97057f83e108a3fcff4f`. The fixed-gap literal-integer controls are independent checks of that identity, not a replacement for its all-gap proof. This finite certificate is not presently a kernel-checked Lean exhaustion.

## Why the enumeration is complete

A phase is one of 2,4,6,8,10,12,14,16; every image phase is even, so a cycle cannot require an odd phase. For a fixed phase c, let d=18-c. A canonical trimmed exterior B has positive first coefficient and last coefficient different from c. A trimmed A starts with a coefficient different from c and ends with one different from d. Because c and d are nonzero and unequal, either block has length counts

    f(0)=1, f(1)=17, f(k)=324*19^(k-2) for k>=2.

Thus its ordinary length generating series is (1-z)^2/(1-19z). The center C is symmetric, has an even middle coefficient when its length is odd, and does not begin/end with d when its length is at least two. Its series is

    (1+10z)*(1-z^2)/(1-19z^2).

The physical interface weights B and A twice. The complete eight-phase generating series is therefore

    8*(1+10z)*(1-z^2)^5/(1-19z^2)^3.

Its coefficients for I=0,...,6 are respectively

    8, 80, 416, 4160, 15128, 151280, 466560.

Their sum is 637,632. The replay checks every coefficient as well as distinctness of the enumerated states.

## Sharpness and ordinary-integer witness

The maximum-rank quotient path is

    (2,  (), (0,18), ())
    (4,  (), (1,17), ())
    (8,  (), (3,15), ())
    (16, (), (7,11), ())
    (14, (7,), (9,), (4,))
    (10, (15,9), (9,9,9), (8,))  -- first exit, I=11.

Starting with g=h=4 gives the actual consecutive ordinary integers

    22220999997777900000
    22221977777777802222
    44442855555555714444
    88884611111111538888
    177768122222223187776
    855549444444445055547.

The first four gap increments are (0,0); the fifth is (-2,-1). The final gaps are (2,3), so every source needed for this five-step witness satisfies the original gap guards. These are finite nonpalindromic controls, not a Lychrel witness.

## Reproduction and committed-byte verification

From this directory, using ordinary Python without optimization flags:

    python -m unittest -v test_quotient
    python search.py --cap 6
    python replay.py --cap 6

The four tests include 28,912 independent ordinary-integer formula controls plus enumeration uniqueness checks. The rank archive is retained as `results/cap6-ranks.json.gz.b64`; replay automatically decodes this committed representation when a raw gzip is absent.

GitHub Actions run **38683881776** passed from input commit **1d9e3c5ce9ad0ac1ed69ab6cb725553bf7858f99**, regenerated the published certificate without manual byte transcription, forced a replay of the text-encoded archive, and committed only this agent's generated results and logs. A second local replay of its downloaded exact source snapshot also passed. `logs/certificate-ci.log` retains the checked source hashes and outputs. The snapshot ZIP SHA-256 was `88663eb3bfc7fd35229c035c9d3ec93ced7f0512f430b70d8527006ef86ca9d6`.

Stable mathematical-data hashes:

    edge stream: edd32c9bac703996e0817b6bc7118e1a88b92e573b982794bd756dd86d710833
    raw rank JSON: bc0edd6916638340bac7115e99313485176c5b9e0ed242195b2528f8f54198ee

Gzip byte hashes can differ with the Python/zlib implementation; each summary records and checks its own exact archive hash. The raw JSON and edge-stream hashes agree across the local and CI runs. Initial transport files before automated regeneration are not the accepted certificate checkpoint.

## Lean arithmetic: checked, but not the whole quotient bridge

`CycleConstraints.lean`, published at **65e5b5cb962d6c9157703db279cc7e3a9b855bcb**, has ten supporting declarations. All ten compiled both in GitHub Actions run **38682766013** and using the official native Lean **4.19.0**, commit **6caaee842e94**, locally. Exact source SHA-256:

    9c5f4a6a224c13a6f392ba2ccff7aab6dad10969efc5c1269037871823506ac6

`outer_upper_step` has no axiom dependencies. The other nine use only `propext` and `Quot.sound`. The retained audit is `logs/lean-arithmetic-audit.log`. No admitted proof, native-evaluation shortcut, or custom axiom is used.

The module proves normalization mass modulo nine, the complete one-column upper potential, arbitrary path telescoping, and arithmetic consequences of explicitly stated cycle premises. It does **not** supply a full ordinary-integer or all-word quotient-cycle bridge. Its period-at-least-twelve corollary is correct but is no longer the strongest repository restriction.

## Concurrent results inspected and next work

Agent #2's `12563cbc1604dd226dd50cec97e2bf175d190998` proves an exterior residue charge, divisibility of the overflow count by nine, individual gain divisibility by nine, and the resulting period-at-least-36 bound for full six-phase returns. Agent #5's `db65db3646694d95fe6a8e7a0f836d66d8e6a4c8` formalizes the exterior clock. Agent #8's `8902b2b8d5cf495d7ee407e905817e1737aae770` formalizes broader mass and path arguments. Their actual-map premises and stated scope must be retained. These are credited advances, not newly attributed Agent #4 results.

The current follow-up is a three-column saturation obstruction and an arbitrary-width temporal-strip method, reserved under separate Agent #4 paths. They seek stronger all-interface exclusions, not a larger cap masquerading as a global proof. Full ordinary-map formal integration, longer possible returns, and any connection establishing infinite safety of the particular 196 orbit remain unresolved.
