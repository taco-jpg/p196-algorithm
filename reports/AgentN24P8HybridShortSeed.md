# Agent N24: Shorter decimal 20,000-step hybrid from the period-8/m48 lattice

**COMPUTED (finite steps 0..20,000).** A second, distinct decimal neutral/lattice splice with a shorter initial seed and slower observed inward defect-front motion. This is not a base-10 infinite Lychrel certificate. The earlier N24 p12/m9 result is `AgentN24HybridNeutralLatticeFront.md`; this result instead uses the known rooted `lat2.txt` rec2 lattice (`p=8`, `m=48`, 11-coefficient root).

## Exact construction

The low-digit-first symmetric pairword is

`P0 = B0 ++ W0^67 ++ 9^20 ++ [18] ++ 9^20 ++ reverse(W0^67) ++ reverse(B0)`.

Here `B0=(17,5,0,2,1,9,15,18,14,9,3)` and `W0` is the full 48-coefficient rec2 spatial period from `calculation/decimal_frontier/lattice_kinks/data/lat2.txt`. Complete 8 temporal rows of both B and W, and overflows `g=10101010`, are frozen in `calculation/new_structures/agent-N24/p8_hybrid_data.json`. Split mirrored pair coefficient `p` into decimal digits `(min(9,p),p-min(9,p))` and the central 18 into decimal digit 9, obtaining a concrete valid 6,495-digit integer. Each replay engine constructs it independently from the data.

## Two independent full decimal replays

`replay_bigint.py` uses Python ordinary integers `N += int(str(N)[::-1])`; `replay_digitlist.py` uses positional digit-list carry arithmetic and never performs integer reverse/add. The wrapper `reproduce_p8.py` cross-checks their full seed/final SHA-256 and every 1000-step sample, plus a corrupted temporal boundary and a trivial positive palindrome control.

Both engines verify for **every** step `0..20000`:

1. No decimal palindrome (in fact the least- and most-significant decimal digits differ at *every* observed step; maximum first-difference index = 0).
2. Length exactly `6495 + sum(g[t mod 8])`, final `16495`.
3. Symmetric pairword begins with all 11 time-phase root coefficients B and **at least 256** coefficients of the period-48 lattice W, with the exact mirrored suffix.

Agreement fingerprints: initial number SHA-256 `3f723364abaf682f34210f96191980ae52e7cddfce572557b2e91e22780a2fa3`; step-20,000 number SHA-256 `e3e9530f676dbb4adb69d94ad127fa7079bfdf54251fcc839b7db55aa8cbfa71`.

## Measured interface and breakdown

Rooted lattice length (following the 11-coefficient root) at steps 0, 1000, 5000, 10000, 15000, 20000 is respectively 3216, 3060, 2480, 1751, 1022, 297. The front consumes 2919 coefficients in 20,000 steps, mean speed **0.14595 coefficients/step**. This is slower than the previous p12/m9 observed 0.18755; neither rate is proven as an asymptotic velocity. With the very same seed, the neutral 9-region switches into a 17-cell zero run after five steps (checked by exact coefficient normalization in the wrapper), after which its free central defect expands. This is a **transient regenerative-carry candidate**, not a closing glider or certificate cycle. Unlike a mere dead-family no-go, it demonstrates a second lattice domain can delay the defect for 20k steps with a significantly shorter initial number.

## Reproduce in one command

```sh
python3 calculation/new_structures/agent-N24/reproduce_p8.py 20000
```

The command runs both independent arithmetic implementations, checks matching full-number SHA-256 fingerprints, runs a deliberate expected-root corruption control and positive `56 -> 121` palindrome control, checks the carry conversion, and asserts the expected finite 20k endpoint. A 100-step smoke control is `python3 calculation/new_structures/agent-N24/reproduce_p8.py 100`. Exact input and 21 sampled data are in `calculation/new_structures/agent-N24/{p8_hybrid_data.json,p8_bigint_evidence.json}`; independent checkers are in the same agent directory, introduced in the preceding result commit. Git shell DNS prevents local repository `tools/verify.py --changed`; no Lean files and no `LEAN-VERIFIED` claim.