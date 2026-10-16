# Agent 5: exterior defect clock and returned-interface obstructions

This contribution studies the complementary nonneutral two-band quotient. It does not prove a Lychrel witness, global exterior divergence, or any all-time statement about the orbit of 196. The work is AI-assisted; no novelty, human-review, or external peer-review claim is made.

## Dependencies and evidence levels

The actual whole-word formulas are those in [the complementary-bulk quotient](../contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md), read at main `a71d6e79b009da691e2d97057f83e108a3fcff4f`. That written all-length theorem identifies the exterior function studied here with the true reverse-and-add dynamics when the two source gaps are at least two. All finite blocks may be empty. The same source supplies the width identity and the conditional infinite-safe cycle criterion; it does not supply a cycle.

`ExteriorClock.lean` defines the exact exterior function independently and proves its modular law for arbitrary finite bounded coefficient lists. Thirty supporting declarations compile locally with Lean 4.19.0 and in fresh [Actions run 38683072135](https://github.com/taco-jpg/p196-algorithm/actions/runs/38683072135), at source commit `db65db3646694d95fe6a8e7a0f836d66d8e6a4c8`. Embedded transitive audits use only `propext`, `Classical.choice`, and `Quot.sound`; the two finite scalar tables use no axioms. There are no admitted proofs, custom axioms, or native decision shortcuts.

**Formal boundary:** the all-length exterior congruence and exterior-path residue theorem are kernel checked for the explicitly defined function. The full ordinary-integer/template identification is a written dependency, not a newly completed Lean bridge. The final generic `closed_path_obstruction` retains explicit clock, budget, progress, closure, and even-overflow premises. Its arithmetic conclusion must not be described as an unconditional ordinary-map theorem without those bridges.

`complementary_quotient.py` is an independent reconstruction with literal ordinary-integer checks, not a transcription or invocation of the prior implementation. `audit_exterior.py` gives complete bounded exterior graph reconstruction and finite arithmetic controls. These Python computations are not claimed as Lean graph certificates.

## 1. Autonomous exterior factor

Write the original source template, least-significant column first, as

`B c^g A d^h C d^h reverse(A) c^g reverse(B)`, with `d=18-c`.

Here `c` belongs to `1..17` excluding 9. The phase update is `c'=2(c-9k)`, where `k=1` for `c>=10` and zero otherwise. Put `t=c-9k`.

Normalize `B` with input carry zero to obtain `(D,e)`, and normalize `reverse(B)` with input carry `k` to obtain `(E,gamma)`. Set `u=c+e-10k`. The next raw exterior is

- `(D ++ [u]) + (reverse(E) ++ [t])` when `gamma=0`;
- `(D ++ [u]) + ([1] ++ reverse(E))` when `gamma=1`.

The additions are coordinatewise. Both lists have length `|B|+1`. Remove the maximal suffix consisting of `c'` to get `B'`.

Every quantity in this update, including actual overflow `gamma`, depends only on `(c,B)`, not on `A,C,g,h`. This follows because every nonneutral constant band resets its outgoing carry to its own `k`. Every valid full quotient path therefore projects to this autonomous exterior path, as long as the whole-word gap hypotheses hold.

The exterior function is defined even beyond a bounded search domain. An edge escaping a chosen length cap does not imply divergence and must not be discarded as globally impossible.

## 2. Exact defect-mass congruence

Define the integer defect mass

`M(c,B) = sum(B) - c*|B|`.

The all-length identity is

`M(c',B') = 2*M(c,B) - gamma*c (mod 9)`.

Proof: normalizing a coefficient list `W` with input carry `a` gives a digit list `V` and final carry `f` with

`sum(V)+f = sum(W)+a (mod 9)`.

This follows by summing the column equations `x+incoming=digit+10*outgoing`, or by the list induction used in Lean. Apply it to the two normalizations of `B`. The sum of the raw exterior is then `2*sum(B)+(2-gamma)*c` modulo nine. Its length is `|B|+1`, and `c'=2c` modulo nine. Subtracting `c'*(|B|+1)` gives the stated mass expression. Removing each trailing `c'` reduces both the sum and `c'` times the length by exactly `c'`, so trimming preserves the mass exactly. This proves the identity for every finite `B` with coefficients in `0..18`; no bound on its length is used.

Lean endpoints: `normalize_mod9`, `rawExterior_sum_mod9`, `mass_stripSuffix`, and `exterior_mass_step_bounded`.

## 3. A residue clock for the six unit phases

For `c` in the phase cycle

`2 -> 4 -> 8 -> 16 -> 14 -> 10 -> 2`,

let `a(c)` respectively be `1,5,7,8,4,2`. These are the residues `2/c` modulo nine; division here means multiplication by a modular inverse. Define

`R(c,B) = a(c)*M(c,B) (mod 9)`.

The multiplier identities `2*a(c')=a(c)` and `a(c')*c=1` modulo nine turn the mass recurrence into

`R(c',B') + gamma = R(c,B) (mod 9)`.

Thus each overflow advances the clock by exactly one in the negative direction. Summing along a returned exterior path proves that its overflow total `G` is divisible by nine. The phase and exterior block must both return; merely observing a repeated leading coefficient is not sufficient.

The phase cycle `6 <-> 12` is deliberately excluded: these coefficients are not units modulo nine. Assigning them an inverse would be an error. Their absence from this theorem is not an exclusion of cycles in that family.

Lean endpoints: `exterior_clock_step` and `exterior_path_mod9`. The latter checks the concrete exterior recurrence and propagates the six-phase hypothesis; it does not simply assume a residue-clock edge law.

## 4. Overflow budget and positivity

For the actual positive exterior pair coefficient `p` and the carry `e` entering its reflected exterior, `1<=p<=18`, `e` is zero or one, and

`gamma=(p+e)//10`;

`p'=2p+e` without overflow, and `p'=p%10+1` with overflow.

The second formula includes the appended leading one and the uncarried least-significant digit. It also handles the threshold case `p=9,e=1`.

Use the potential

`psi(1)=0`, `psi(2)=psi(3)=psi(10)=1`,

`psi(4)..psi(9)=2`, and `psi(11)..psi(18)=3`.

Every one of the 36 possible scalar controls satisfies

`2*gamma + psi(p') <= 1 + psi(p)`,

`p+1 <= p' + 10*gamma`.

These complete tables are kernel checked by ordinary `decide`. On a closed exterior path of positive period `P`, the potentials and exterior coefficients telescope, giving

`2G <= P <= 10G`.

In particular `G>0`. Together with the residue clock, a six-phase exterior cycle has at least nine overflows and period at least eighteen. **The exterior-only conclusion is eighteen, not thirty-six.**

## 5. Stronger obstruction for a returned full interface

For a returned full quotient state `(c,B,A,C)`, let `Delta_g` and `Delta_h` be the accumulated gap changes. The source's exact width identity telescopes to

`2*(Delta_g+Delta_h)=G`.

Consequently `G` is even, independently of the signs of the two individual gains. For the six unit phases, the exterior theorem also makes it a positive multiple of nine. Therefore

`G >= 18` and `P >= 36`.

This excludes every shorter returned full interface in the six-phase family, even a cycle whose individual gap gains would fail the nonnegativity requirement for infinite repetition. It does not exclude longer cycles. It does not assert that any cycle exists, or that a returned exterior extends to a returned full interface.

The final Lean arithmetic wrapper proves the implication with all these premises visible. The width/parity premise is not silently inferred from exterior closure. The original all-gap template theorem is still the written link to ordinary reverse-and-add.

## 6. Independent finite controls

The seeded reconstruction replay uses 10,000 source states and four gap pairs `(2,2),(2,3),(3,2),(5,7)`: 40,000 literal-integer checks. Every test independently realizes the source pair word as a canonical integer, applies integer reverse-and-add, and compares its new pair word with the quotient. It also checks the width identity, trim conditions, exterior-factor equality, and nonpalindromicity of the positive output. There are 5,243 overflow source states.

All trimmed exteriors through length three, over all sixteen nonneutral phases (including transient odd phases), give 103,968 checks of the mass recurrence and scalar budget, including 38,988 six-phase clock checks.

The complete bounded graphs, not just reachable samples, have:

| Exterior cap | States | Internal edges | Escapes | Maximum steps to escape |
|---:|---:|---:|---:|---:|
| 1 | 288 | 88 | 200 | 6 |
| 2 | 5,472 | 1,600 | 3,872 | 7 |
| 3 | 103,968 | 30,328 | 73,640 | 10 |

Each graph is acyclic. Reverse traversal from every escape assigns each state an exact steps-to-escape rank, and every internal edge strictly lowers that rank. The enumeration includes every canonical trimmed block in the cap; a missing target is asserted to have larger exterior length. `audit_results.json` retains rank histograms and SHA-256 digests of canonical state/successor/rank rows. The script reconstructs all rows deterministically, so the results do not rely on an unavailable search trace.

These finite theorems allow unrestricted inner blocks `A,C`, but only bound continuous residence in the stated exterior cap. A path may leave the cap and later return. No conclusion about the whole infinite state space follows.

Other agents subsequently reported larger even-phase caps and separate certificates in issues 5, 7, and 8. Our all-sixteen-phase cap data is retained as an independent replication with its own scope, not a claim to their larger-cap results. Agent 101 separately reported zero violations of our mass congruence over 987,696 even-phase exteriors through length four; that is finite replication, not another proof of the all-length theorem.

## 7. Reproduction and fingerprints

From the repository root:

```sh
python3 proofs/agent5/audit_exterior.py
lean -o proofs/agent5/ExteriorClock.olean proofs/agent5/ExteriorClock.lean
```

Use official Lean 4.19.0. The Python script regenerates the JSON (formatting may differ from the compact stored version; compare parsed values). It needs no network, external solver, or third-party package. The Lean module imports only `Std` and prints the complete dependency audit for every theorem declaration.

Source SHA-256 values for the checked release:

- `ExteriorClock.lean`: `7158c8c7d07fab80c4212ba4c6c4b0a318ca22faee988c8d22eca45edfd439c5`.
- `complementary_quotient.py`: `27a905e4598bd528f6b99b352065bed321b09ed0a4cde9d4b0fd7f86f17dd716`.

Local Lean source compilation returned zero. The separate fresh GitHub run also returned success; successful compiler bootstrap alone is not counted as mathematical verification. The retained local log lists all thirty transitive audits.

## Remaining obligations and collaboration

No qualifying recurrent exterior or full interface has been found here. General all-width exterior acyclicity is unresolved, and it is not established that the 196 orbit stays in any of these templates. A period and width restriction is a necessary condition, not a percentage of progress toward a solution.

Agent 9 is developing all-width erasure laws; Agent 6 and subsequent agents are extending finite exterior certificates. Agent 109 has claimed the missing full-template/ordinary-integer Lean bridge. Agent 5 is investigating general-base and non-unit-phase arithmetic extensions instead of duplicating those tasks. Coordination, pins, and scope corrections are in [issue 5](https://github.com/taco-jpg/p196-algorithm/issues/5).
