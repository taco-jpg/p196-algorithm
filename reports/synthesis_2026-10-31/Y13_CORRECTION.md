# Y13 repunit interval correction

Consolidated from the 2026-10-31 synthesis audits, with a fresh independent arithmetic check during publication.

**Status: COMPUTED counterexample + PAPER PROOF algebraic correction. Decimal existence remains UNDECIDED.**

## Failure in the broad interval lemma

The current [Y13 result](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/results/AgentY13FirstExitRepunitRigidity.md) 和 [reproducer docstring](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/new_structures/agent-Y13/first_exit_rigidity.py) assert the following implication for `M_j=10^j-1`, `g=gcd(h,k)`:

```text
1 <= h < k, 10^h <= q < 2*10^h, M_k divides M_h*q
=> q=M_k/M_g => M_h*q=M_k => palindrome.
```

The last equality drops the factor `M_h/M_g`.

```text
h=2, k=3, g=1, q=111
100 <= 111 < 200
M_h*q = 99*111 = 10989 = 999*11
reverse10(10989) = 98901
```

Every premise of the broad interval statement holds, while the asserted equality 和 palindrome conclusion fail. The correct identity:

```text
M_h * (M_k/M_g) = M_k * (M_h/M_g).
```

## Precise consequence

- The valid divisibility step `M_k/M_g | q` survives.
- The guarded subclaim `0<q<10^h` excludes larger repunit factors because `M_k/M_g>10^h`; the counterexample leaves that subclaim intact.
- The interval forces `q=M_k/M_g`, but the resulting multiplier generally exceeds 1.
- **The example has `q mod 9 = 3`. It does 不 refute the narrower X07 assertion restricted to actual first exits of charge-2 quotients.** The displayed broad argument nevertheless fails to prove that assertion. A separate valid restricted proof remains necessary.
- The existing 1,234 finite controls cannot repair the universal algebraic step.

The complement-piston row in [GAP_MAP](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/docs/GAP_MAP.md) repeats the first-exit-palindrome consequence. Treat that consequence as unsupported by the cited Y13 proof pending repair; preserve the independently valid guarded piston identities.

## Fresh exact reproduction

The following Python check ran successfully during publication; a separate JavaScript BigInt check agreed.

```python
from math import gcd
h, k, q = 2, 3, 111
Mh, Mk, Mg = 10**h-1, 10**k-1, 10**gcd(h,k)-1
assert 10**h <= q < 2*10**h
assert (Mh*q) % Mk == 0
assert Mh*q == 10989 != Mk
assert str(Mh*q) != str(Mh*q)[::-1]
assert Mh*(Mk//Mg) == Mk*(Mh//Mg)
```

Repair locations: the result note, the proof docstring, 和 the dependent GAP_MAP row. Preserve the distinction between a false broad lemma 和 the still-unresolved restricted first-exit assertion.

The publication adds documentation 和 small Python controls. No Lean source changed; no Lean build, `verify.py`, lean4checker replay, or new allowed-axiom audit was performed.
