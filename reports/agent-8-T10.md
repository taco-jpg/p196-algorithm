# Agent 8 — T10.B.short-period independent red-team automaton

**Status:** COMPUTED. Independent standard-library-only Python implementation of the exact position-by-position B-cycle transfer for base 10. Independent reproduction of the previously documented p<=10 absence; not a new decimal Lychrel theorem and not a Lean theorem.

## Scoped result

**No base-10 B cycle of exact period p=1,..,10** under the neutral-band `Hyp`/`nextB` rules. The test has no bound on the length of a B state. It enumerates all binary overflow words, not just cyclic representatives, and uses no state/depth cap in any accepted negative conclusion: every work queue exhausted before configured safeguards (`cap=300000`, `depth <= 450`).

The independent transfer implementation in `calculation/agent-8/short_period.py` differs from `structure/bauto.cpp`: it is pure Python; enumerates all overflow words, including rotations; represents states as `(L,H,Y)` Python tuples; recursively traverses **time** within one column; and breadth-first explores column layers, without copying packed-state C++ code. The mathematical local transfer formulation is the same (necessarily so, for exact replication).

### Reproduce (no external dependencies)

```
python3 calculation/agent-8/short_period.py --pmax 8 --cap 300000
python3 calculation/agent-8/short_period.py --pmin 9 --pmax 10 --cap 300000
python3 calculation/agent-8/short_period.py --g 11100010000 --cap 300000
python3 calculation/agent-8/short_period.py --g 100010001000 --cap 300000
```

The first two commands respectively report:

```
SUMMARY {'EXHAUSTED': 510} total_states_by_word 493512
SUMMARY {'EXHAUSTED': 1536} total_states_by_word 32137
```

Thus all `2^(1)+...+2^(10)=2046` overflow words, totaling 525,649 (word,state)-records, return `EXHAUSTED`, with zero `ACCEPT`, `CAPPED`, or `DEPTH-CAPPED`. Most costly p<=10 instance among necklace representatives is p8 `g=01010101`, at 244,785 states, depth 88.

**Positive controls** (COMPUTED, match documented independent `bauto` results):

```
p=11 g=11100010000 status=ACCEPT depth=29 states=10861 explored_arcs=11110
  accepting interface: ((1,0,1,0,0,1,1,0,0,1,1), ..., ...)
p=12 g=100010001000 status=ACCEPT depth=53 states=99378 explored_arcs=100092
  accepting interface: ((1,0,0,1,0,1,0,1,1,0,1,0), ..., ...)
```

The accepted `L` strings are exactly the known `e=10100110011` for p11 and an allowed p12 rotation `e=100101011010`. This is a B-only acceptance, not a center match/certificate.

## Why the transfer is necessary for B-cycles (paper derivation)

Index time modulo p by t, exterior coefficient position from the least-significant end by k. Let `x_t` be the coefficient at position k, `L_t` the incoming carry for forward normalization from position k-1, `H_t` the required outgoing carry for reverse normalization through position k-1, and choose `h_t in {0,1}` as incoming reverse carry from k+1.

For base 10, correct local normalization enforces

```
floor((x_t+h_t)/10) = H_t.
d_t = (x_t+L_t) mod 10.
r_t = (x_t+h_t) mod 10.
x_{t+1} = d_t + (g_t ? Y_t : r_t).
L'_t = floor((x_t+L_t)/10),  H'_t = h_t,
Y'_t = r_t for the times t with g_t=1.
```

Here `g_t` is the known whole-block reverse overflow bit, and `Y_t` stores the previous adjacent reverse-normalized digit that the overflow shift pairs with the present forward digit. In the first exterior column, `L=0`, `H=g`, `Y=1` (the new lowest-digit 1 introduced by overflow), and the first source coefficient is nonzero. The code **overapproximates** this initial admissibility by not excluding zeros for every *other* time instant's first coefficient; this can create extra paths but cannot cause a false negative.

On exit into arbitrarily many neutral 9-coefficients, the interface must satisfy `L_t+H_t=1` for all t and `Y_t=9*L_t` at overflow times. This is the existing exact B automaton acceptance criterion, independently re-implemented. Every real closed B word trajectory with that overflow word induces a path from the initial to an accepting interface. Search stores every transfer state reached through each column, and terminates only when a complete BFS layer gives no unseen states; therefore `EXHAUSTED` means no accepting interface at **any** B width.

## Additional disjoint short-period checks (COMPUTED)

The same source and the same p11/p12 positive controls were subsequently used on the exact-period **13, 14, 15** slices, enumerating one necklace of every rotational class (rotation suffices because a B-cycle can be cyclically reindexed). No state/depth cap was reached in any run:

```
python3 calculation/agent-8/short_period.py --pmin 13 --pmax 13 --necklace --cap 300000
  SUMMARY {'EXHAUSTED': 632} total_states_by_word 4152
python3 calculation/agent-8/short_period.py --pmin 14 --pmax 15 --necklace --cap 300000
  SUMMARY {'EXHAUSTED': 3374} total_states_by_word 244843
```

The second run comprises 1,182 p14 necklaces and 2,192 p15 necklaces; p14 total states 203,926 (maximum single word 182,837, depth 55), p15 total states 40,917 (maximum single word 33,089, depth 18). These independently corroborate the previously documented negative periods 13–15, not the unresolved p16/p18 cycles.

## What is not claimed

- Periods p=11 and 12 have positive B-only controls; p=16,18 and all p>15 remain outside the completed negative scope. Their center matching remains open at arbitrary repetition.
- This independent check is NOT a proof that base 10 has no Lychrel numbers; only a bounded-period negative result for the specific one-band certificate format.
- It is neither Lean-compiled nor a replacement for `python3 tools/verify.py --changed`.
- No branch, PR, `README.md` or `RESULTS.md` edit is made due the manager-declared contribution-policy conflict in `AGENTS.md`.

## Attribution

Original transfer automaton and earlier p<=10 search: `calculation/neutral_band/structure/bauto.cpp` and `calculation/neutral_band/README.md`. Independent Python implementation and positive controls contributed here as a red-team reproduction, not priority claimed for the underlying mathematical recurrence.