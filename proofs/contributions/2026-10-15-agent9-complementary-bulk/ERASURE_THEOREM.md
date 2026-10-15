# Exact exterior erasure in the complementary-band quotient

Agent 9; AI-assisted research. No novelty, human independent review, or solution of P196 is claimed. This contribution proves all-length local exterior identities. It does not prove that every exterior escapes, exclude every quotient cycle, or supply a finite Lychrel witness.

## Source and actual-map interface

The starting source is `../2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`, read at main `a71d6e79b009da691e2d97057f83e108a3fcff4f`, blob `f48a0ec61e7ff0419bb9121a792e79505810db50`. Its equations (3), (6), (7), and (10) define the exact whole-word complementary-band quotient. We use those equations, not freely selected carries. Their complete ordinary-integer bridge remains the existing written theorem; the new self-contained Lean source formalizes the exterior formulas and the erasure laws below, rather than re-formalizing that entire bridge.

Coefficients are in `0,...,18`; words are least-significant-first. For a nonneutral phase `c` in `{1,...,17}\{9}`, put

```
k = 1[c >= 10],     t = c - 9*k,     c' = 2*t,     E_t = {t,t+9}.
```

Thus `1 <= t <= 8`. Let `B` be the finite exterior. Normalize `B` with incoming carry zero, obtaining digits `D` and final carry `alpha`. Normalize `reverse(B)` with incoming carry `k`, obtaining digits `R` and final carry `gamma`. The actual quotient exterior is autonomous: neither `A`, `C`, nor either gap enters these normalizations. The raw exterior is

```
gamma = 0:   B_r = (D, t-k+alpha) + (reverse(R), t),
gamma = 1:   B_r = (D, t-k+alpha) + (1, reverse(R)).
```

Here `+` is coordinatewise addition and juxtaposition is concatenation. Both raw words have length `|B|+1`. Let `u_B` be the length of the maximal suffix of `B_r` consisting of `c'`. Removing that suffix gives the next exterior `B'`.

A source exterior is trimmed when it is empty or its last coefficient differs from `c`. The original quotient produces trimmed targets.

## The exact erasure theorem

**Overflow.** If `gamma=1`, then

```
u_B = length of the maximal suffix of B over E_t,
|B'| = |B|+1-u_B >= 1.
```

No trimmedness assumption is needed for this case. In particular, arbitrarily long erasure is possible, but the raw exterior is never erased completely.

**No overflow.** If `gamma=0` and `B` is trimmed, then

```
u_B = 1[alpha=k],
|B'| = |B| + 1[alpha!=k].
```

Thus a no-overflow step cannot shorten a trimmed exterior. The Lean theorem proves this algebraic identity for the displayed no-overflow raw formula even without a final-carry premise; selecting this formula for the actual quotient requires `gamma=0`.

**Complete binary collapse.** If `gamma=1` and every coefficient of `B` belongs to `E_t`, then the stronger word identity is

```
B_r = (t) (2*t)^|B|,        B' = (t).
```

The alphabet has two letters, but its words need not alternate. For example, `c=1, B=(10,10,10)` and `c=1, B=(10,1,10)` both collapse to `(1)` at next phase `2`. When `B` is empty, overflow forces `k=1`, and the same identity gives the singleton `(t)`.

## All-length proof

For a coefficient `x` and incoming carry `e`, write

```
carry(x,e) = (x+e)//10,       digit(x,e) = (x+e)%10.
```

Every carry used below is a bit. A coefficient `t+9*z`, with `z` a bit, resets either incoming carry to `z`; its digit is `t-z+e`.

Read the exterior from the bulk outward, so `xs=reverse(B)`. The forward carry from the remaining exterior into its first coefficient `x` is some bit `a`; the reflected normalization enters from the bulk with carry `k`. The last raw overflow coefficient, now the first coefficient in this reversed view, is

```
digit(t+9*k, carry(x,a)) + digit(x,k).
```

The exact local criterion is

```
digit(t+9*k, carry(x,a)) + digit(x,k) = 2*t
    iff x=t or x=t+9.                         (1)
```

For `x<=8`, both carries out of `x` vanish, and the left side is `t+x`; equality forces `x=t`. For `x>=10`, both carries are one, and the left side is `t+x-9`; equality forces `x=t+9`. For `x=9`, the left side is `t+9+a-10*k`. Equality would require `t=9+a` if `k=0`, or `t=a-1` if `k=1`; both contradict `1<=t<=8`.

Whenever `x=t+9*z`, (1) strips one output coefficient, resets the reflected carry to `z`, and leaves precisely the same raw problem on the remaining list. Induction therefore peels exactly the maximal suffix over `E_t`. If a nonalphabet coefficient is reached, (1) prevents another strip. If the entire list is exhausted, the carried total overflow hypothesis forces the remaining bit to be one. The last raw coefficient is then `digit(t+9,0)+1=t`, not `2*t`. This proves the overflow theorem and, when every letter is in the alphabet, the displayed complete-collapse word identity.

For no overflow, the last raw coefficient is `digit(t+9*k,alpha)+t=2*t-k+alpha`, so it equals `2*t` precisely when `alpha=k`. If that equality fails, nothing strips. If it holds and `B` is nonempty, let `x` be its last source coefficient and `a` the incoming forward carry. Then `carry(x,a)=k`. The next paired raw coefficient satisfies

```
digit(x,a)+digit(x,k)=2*t
    iff x=t+9*k and a=k.                      (2)
```

To verify (2), the condition `carry(x,a)=k` also implies `carry(x,k)=k`: split `x<=8`, `x=9`, and `x>=10`. The equality becomes `2*x+a-19*k=2*t`; with `a,k` bits, parity forces `a=k`, then `x=t+9*k`. Trimmedness excludes this source coefficient. Thus exactly one column strips. An empty `B` has no second column, so the same count holds.

## Consequences for cycle searches

Once an actual trimmed exterior is nonempty it remains nonempty: no-overflow length is nondecreasing, and overflow length is at least one. Every overflow creates a nonempty exterior. A nontrivial returned quotient cycle must contain an overflow: without overflow the positive actual outer coefficient changes from `a` to `2*a+e`, with `e` a bit, and strictly increases. Therefore no returned cycle can contain an empty exterior state. This uses the original actual-map bridge and is a written corollary, not an additional audited Lean declaration.

For any returned exterior cycle, let `r_s` be the length of the `E_{t_s}` suffix before an overflow. Summing the exact length changes gives the necessary budget

```
sum_{overflow steps s} (r_s-1)
    = number of no-overflow steps with alpha_s != k_s.       (3)
```

The sum is an integer sum; a zero-length erasable suffix contributes `-1`. A shrinking step must be an overflow with `r_s>=2`. Equation (3) is only a necessary cycle condition. It does not establish escape, forbid all cycles, or imply either gap gain is nonnegative. The separate original two-gap cycle criterion still requires both total gap gains and all within-cycle gap guards.

## Essential hypotheses and failed simplifications

For `c=1, B=(1,1)`, there is no overflow and the raw exterior is `(2,2,2)`. All three letters strip. The source is untrimmed, so this disproves a no-overflow one-column bound without trimmedness. Its source `E_t` suffix has length two, not three, so the same example disproves the overflow suffix formula with its overflow hypothesis removed.

The initial exploratory description of long collapses as alternating tails was unnecessarily restrictive: every word over the two-letter alphabet is allowed, subject to actual overflow. We retain the exact alphabet criterion, not an alternation assumption.

The first Lean draft at commit `20d4919f099311d1c5782e38b53e6c34f4b01672` failed because three bare `omega` calls lacked explicit division-case facts. CI run `38682431393` failed and its resulting `sorryAx`-dependent declarations were not accepted. Supplying the carry equations and separating low/neutral/high coefficients repaired those proofs. No mathematical premise was weakened to obtain compilation.

## Verification and reproduction

`ExteriorErasure.lean` has 28 supporting theorem declarations, not 28 independent major results. The exact committed source has SHA-256

```
1de006bcb67eefc0feba31332ed7790813b291aa31de2c8f45de70caf6a970a2
```

It passed GitHub Actions run `38683728944` at commit `9a8c30c0e097f3ef0cfc5c614be957f153e4b827`, then a separate local rebuild of the exact source downloaded from that run. Both use Lean 4.19.0, release commit `6caaee842e94`. `verify.py` requires every declared theorem to have a printed dependency audit and rejects any dependency outside `propext`, `Classical.choice`, and `Quot.sound`. Some declarations use no axioms. There is no `sorry`, `native_decide`, or custom axiom in the accepted source. The complete compiler output has SHA-256 `d8cb44b6b9300939e62fc1312b0aeeddb81b17ae7c9473690b97fde1b079048a`.

```
python verify.py --lean /path/to/lean-4.19.0/bin/lean
python audit_erasure.py
```

The exhaustive finite test checks 2,085,136 canonical exteriors of length at most four over all sixteen phases, including both trimmed and untrimmed sources. It checks 65,520 binary full-collapse words through length twelve, and 10,000 seeded random full quotient instances through the independent ordinary-integer operation `n+int(str(n)[::-1])`. Results and the hypothesis counterexample are in `erasure_audit.json`. Histogram rows with no overflow and more than one stripped column concern untrimmed controls, not counterexamples to the theorem. A separate initial small-interface test checked 267,520 literal-integer instances; its reproducible source and record are added separately.

The finite controls validate implementations and edge cases. The all-length conclusions come from the proofs and their stated interfaces. No numerical percentage toward solving P196 is assigned.
