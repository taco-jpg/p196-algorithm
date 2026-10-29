# X07: Post-collision restoration of the complement-nine piston

Labels: **PAPER PROOF** for the zero-gap carry latch, **COMPUTED** for the specified 200-step exhaustive repairs and independent arithmetic controls. **UNDECIDED** whether any fixed base-10 orbit has infinitely many repairs. No Lean-verified claim.

## Structural format and newly discovered regeneration

Write actual, least-significant-first decimal digits as `A ++ 9^L ++ H`, with `|A|=|H|=m`, `H[i]=9-A[i]` (same direction, not reversal), `A[m-1]<=8`, and `sum(A)=8 (mod 9)`. Allow `L=0` as a valid empty central domain. The long-core piston theorem in `AgentX07ComplementPistonProof.md` proves closure for `L>=1` and nonpalindromicity. Here we establish the additional **zero-gap latch**: at `L=0`, if the low half of the pairword normalizes with outgoing carry `alpha=1`, the next integer is still `A' ++ H'` with the same complement, innermost-digit and charge conditions, and has no length overflow. The latch may persist for multiple steps. If `alpha=0`, this exact argument stops; the resulting digits are independently simulated rather than assumed to repair.

A genuine repair is an ordinary decimal reverse-and-add orbit that starts in this `L=0` family, **leaves** it at some earlier state, reaches no palindrome in between, then **returns** to the protected family with `L>=1`. Thus it creates a new central nine-run after the old run has vanished; mere survival with no digit-core regeneration is not counted.

Two exact examples (normal base-10 integers):

* `94780521` (`m=4`, low-first `A=[1,2,5,0]`) loses the invariant at step 1 and returns at step **19** to `838016291619837`: this has `m=7`, `L=1`, low-first `A'=[7,3,8,9,1,6,1]`, charge `35 ≡ 8 (mod 9)`, and a regenerated central `9`.
* `996508003491` (`m=6`, low-first `A=[1,9,4,3,0,0]`) loses the invariant at step 1 and returns at step **7** to `75454399245456`: `m=6`, `L=2`, `A'=[6,5,4,5,4,2]` with sum26 `≡ 8 (mod 9)` and a regenerated central `99`.

Neither example reaches a palindrome within 4,000 independently checked integer steps. Neither is proved never to reach one. The first restoration does **not** imply another restoration.

## Zero-gap latch: complete carry proof

At `L=0`, the low-half pair coefficients are `B_i=9+A_i-A_{m-1-i}`, and the high-half coefficients are `18-B_i`. Normalize the first half from incoming carry 0, yielding decimal digits `U` and outgoing carry `alpha`. If `alpha=1`, the high-half first carry equals 1. Since the corresponding coefficient-plus-carry sums add to 19, normalization proceeds with complementary carries and complementary decimal outputs: `H'[i]=9-U[i]` for each i, and final carry 0. Thus `A'=U`, `m'=m`, `L'=0`, and leading digit stays nonzero. Since `sum(B)=9m`, preservation of value modulo 9 during normalization gives `sum(U)≡sum(B)-alpha ≡8 (mod9)`. At the innermost coefficient, outgoing carry 1 implies `U[m-1]=A[m-1]-A[0]-1+c_prev <=8`, preserving the guard. A palindrome in this format would force `A_i+A_{m-1-i}=9` for all i, hence `2 sum(A)=9m`; this contradicts `sum(A)=8 (mod9)`. Consequently every zero-gap latch step is exactly safe. This theorem does **not** assert that `alpha=1` persists indefinitely; strict arithmetic growth with fixed digit length eventually forces `alpha=0`.

## Exhaustive finite construction and independent controls

Census is **all** `10^m` possible low-half digit words of fixed length `m` (including leading zeroes) for `m=4` and `m=6`, retaining exactly the words with `sum(A)=8 (mod9)` and `A_last<=8`: 1,000 and 100,000 starts respectively. Enumerate actual decimal digit-list orbits through step 200, stopping at any palindrome. Check the full protected format (including `L=0`) on every state. The positive repair list, all 136 witnesses, is `renewal_events.json`.

| boundary width `m` | guarded starts | repair witnesses | returned length `L=1` | returned length `L=2` | return step range |
|---|---:|---:|---:|---:|---|
| 4 | 1,000 | **26** | 26 | 0 | 17–20 |
| 6 | 100,000 | **110** | 73 | 37 | 6–9 |

Every one of the 136 witnesses passes an **independent Python big-integer** reverse-and-add replay for steps 0..200, including the no-palindrome test and every return time/central length. The C++ census records no second positive repair within this **200-step window**, not a no-go theorem. The two examples above additionally pass independent 4,000-step Python integer replays. A tempting `995599004400 -> 999999999999 -> 1999999999998` superficially creates eleven central 9s, but it **hits a palindrome at step 1**, so the scanner correctly rejects it. This is an important adversarial control.

Reproduce from the repository root:

    sh calculation/new_structures/agent-X07/renewal_run.sh

The script compiles the independent C++ digit scanner, exhaustively recomputes the complete 136-record JSON fixture, replays every witness with Python arbitrary-precision integers, and checks the two long examples. No SAT, probabilistic search, infinite-horizon conclusion, base-10 Lychrel theorem, or Lean checker is claimed. **Next construction:** combine two staggered regeneration defects, since a single repaired centre of length 1 or 2 is consumed quickly and the one-gap relay does not repeat in the checked window.
