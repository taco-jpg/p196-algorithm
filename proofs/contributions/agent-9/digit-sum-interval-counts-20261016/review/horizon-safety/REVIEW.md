# Independent review: generic half-open interval count

**Verdict: PASS. No correction requested.**

Reviewer: the Agent #9 horizon-safety proof worker, independently of the
coverage-census author. The generic review below is supplemented by the completed numeric and
eleven-module closure review in [NUMERIC_REVIEW.md](full-closure/NUMERIC_REVIEW.md).
That addendum records an independent `--trust=0` rebuild and module-origin audit
of 1,451 theorems and 178 safe definitions. The complete review verdict is PASS.
The original generic-only report is preserved in `full-closure/prior-generic-review/`.

## Exact reviewed source

- Repository path:
  `proofs/contributions/agent-9/digit-sum-interval-counts-20261016/Agent9WindowIntervalCounts.lean`
- SHA-256:
  `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9`
- Git blob: `efe4e98e937918b505edfe99e4f6d501be8019f4`
- Independent check source SHA-256:
  `2bb48c3eff8c849a3e550a9f292feb7c24704993079f1694701415c006a23cf6`
- Independent check source Git blob:
  `5395162d474646aeb4b70fc3344261ad1c6c11ba`

The exact reviewed source and check source are retained in
`source-snapshot/`. The original theorem module was not edited. Source
hashes were checked again after the independent build and still matched.

## Statement and mathematical inspection

The main theorem has the exact hypothesis

```lean
∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t
```

with `0 < H` and an explicit `DecidablePred P`. Its conclusion is

```lean
N / H ≤ ((List.range' s N).filter (fun t => decide (P t))).length
```

for every natural start `s` and length `N`. `List.range'` has step one
here. The independent check proves that membership in this filtered list
is equivalent to `s ≤ t ∧ t < s + N ∧ P t`, and proves that the list has
no duplicates. Thus its length counts distinct qualifying times in the
requested half-open interval.

The proof is correct: adjacent interval concatenation splits at `s+N`
without including that endpoint in the left interval. Induction counts
one witness from each complete length-`H` block. The blocks are disjoint,
so a witness on a shared boundary belongs only to the next block. No
global sequence of selected witnesses is assumed. The final argument
uses `(N / H) * H ≤ N` and monotonicity when the remainder is appended.

## Endpoint and zero cases checked

| Case | Checked outcome |
|---|---|
| Empty interval `N=0` | Count is exactly zero; the lower bound is zero. |
| Start `s=0` | Permitted; a qualifying time zero is included. |
| Left endpoint | The singleton interval `[s,s+1)` counts the predicate `t=s` once. |
| Right endpoint | The predicate `t=s+N` contributes zero to `[s,s+N)`, for every `s,N`. |
| Window length `H=0` | The window hypothesis is impossible. The main theorem separately assumes positive `H`. |
| Window length `H=1` | The lower bound and the general upper bound force the count to equal `N`. |
| Short remainder `N<H` | No extra witness is asserted; `N/H=0`. |
| Periodic example `P(t) := t % 3 = 0` | Every length-three window has a witness, and the theorem gives the expected finite floor bound. |

The periodic check includes the concrete count `2` for `[0,6)` and count
`0` for `[1,3)`. The latter is a valid short remainder despite the
length-three window property, so the proof correctly avoids replacing
the floor bound by a ceiling bound.

## Independent build and axiom audit

Both the exact reviewed module and the independent check module compiled
successfully, in that order, with Lean 4.19.0. The review used a fresh
empty build directory and its own `LEAN_PATH`; it imported no author's
project `.olean` file. The only import of the reviewed source is `Std`.

The exact compiler commands, working directory, `LEAN_PATH`, source
hashes, and exit statuses are in `manifest.json`. Both exit statuses are
zero. The compiler executable SHA-256 was
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

All six declarations of the reviewed module, including `intervalCount`,
were audited. The definition uses no axioms, and the five theorems use
only `propext` and `Quot.sound`. The independent review declarations use
only permitted standard axioms; none uses `sorryAx`, `native_decide`, or
a new mathematical axiom. The full output is preserved in
`Agent9WindowIndependentReview.stdout.log`.

The result is a finite interval lower bound. The module neither states
nor needs existence of an asymptotic density limit. `SHA256SUMS` covers
all preserved review files except itself. No compiled artifact is
included in this review directory.
