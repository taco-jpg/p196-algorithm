# Agent #112: eventual realization of arbitrary finite coefficient words

Status: **LEAN-CHECKED; independent review pending.** All 11 project source modules and the aggregate audit compiled from a new empty build directory under official Lean4.19.0. All28 new declarations received transitive axiom audits. No default-branch integration is claimed.

## Main theorem, in original semantics

`Agent112.Eventual.original_arbitrary_eventual_realization` states:

```lean
(w : Agent109.Word) -> 0 < Agent109.evalL w ->
Exists (fun t => Exists (fun n =>
  1 <= t /\ 0 < n /\
  forall k, Agent109.pairWord (Lychrel196.orbit n k) = Agent8.orbit w (t + k)))
```

Here `Word` is a **finite list of natural coefficients**, `Agent8.orbit` iterates the unchanged `pair (normalize w 0)` operation, and `pairWord n` is the digitwise pair sum of the canonical decimal digits of an ordinary integer. The conclusion concerns the *entire future orbit*, not a single matching state.

The initial word need not be symmetric, have positive endpoints, be a canonical decimal representation, or satisfy a fixed coefficient bound. Only finiteness, natural coefficients and positive radix value are assumed. In particular, this theorem does not identify the resulting integer with the input word's initial value or with196.

For the bounded0..18 special case, `original_eventual_realization` additionally supplies the explicit bound `1 <= t <= 2 * 10^w.length`. This bound is deliberately coarse and is not a performance claim. The no-coefficient-bound theorem does not assert that same transient bound.

## Proof mechanism

`EventualRealization.lean` first establishes finite overflow for bounded words. The word's positive radix value strictly grows under the actual symbolic step. If no overflow occurred before the bound, the width would remain fixed, contradicting the proved value bound `evalL w + 2 <= 2 * 10^length w`.

`EventualCorrespondence.lean` shows that the overflow yields canonical decimal digits. The exact integer/pair-word bridge and the iterate-addition identity then identify every subsequent state with an ordinary integer orbit. No prior realizability premise is used.

`CoefficientContraction.lean` removes the initial coefficient restriction. If all coefficients are at most B, one step bounds them by `2 * max 9 (B / 9)`, which is strictly less than B whenever B>18. Strong induction on B proves eventual entry into0..18, after which the first theorem applies. This contraction does not require positivity; positivity is needed for the later overflow argument.

`EventualCompat.lean` states both bounded and arbitrary-coefficient endpoints with the repository's original Agent8 and Lychrel196 constants, via the unchanged Agent109 compatibility proofs.

## Conditional safety transfer and limits

`original_arbitrary_safe_symbolic_positive_seed` assumes, in addition to positive initial value, that **every normalized word along the finite-word trajectory is non-palindromic**. It then proves existence of a strictly positive ordinary decimal Lychrel seed. The tested objects are normalized words, not the mirrored pair words themselves.

**That full infinite-safety assumption is not proved or instantiated here.** No safe symbolic witness, accepted return certificate, exhibited infinite-safe integer, or conclusion about196 is supplied. Infinite symbolic input words are outside the type and scope of the theorem. The remaining construction problem is to provide a finite positive word and a complete proof of its infinite normalized-word safety, or a concrete accepted return certificate, not to assume such a witness exists.

## Reproduce and audit

Mathematical source commit: `c4e6624f5c432aea4378d3ae8f1c8a865497d988`.
Baseline: `eec3d5f3646cab50abad6e610ea19626cd249070`.
The source closure is pinned by SHA256 in `SCOPE.json`.

```sh
LEAN=/path/to/lean-4.19.0-linux/bin/lean bash proofs/contributions/agent-112/eventual-realizability/build.sh .
```

The builder creates a new directory, verifies every source hash, compiles all11 modules plus AuditAll, preserves commands/exit statuses/full logs, and rejects unexpected transitive axioms. All exported theorem dependencies are restricted to `propext`, `Classical.choice`, `Quot.sound` or subsets. No admitted proof, custom mathematical axiom or compiler-evaluation oracle occurs in the accepted chain.

The author clean-build receipt and complete28-declaration audit are in `evidence/`. The dependency sources from the earlier automatic-admissibility task were independently reviewed by Agent110 at `1a20086a0bb73e030d18b9a4ec974d7a3ff3e04a`; that review does **not** cover these new four modules. This closure does not import the unreviewed earlier `AdmissibleCompat` wrapper.

## Coordination

Claim: `06fa057a09c77f8311fb67075089a782294be952`; strengthening claim update: `cb384d2eb3899fb42b28d0b382c74c2e0554c226` on p196/coordination.
Branch: `research/agent-112/eventual-s20261015T1630`, isolated from frozen PR41 sources. Only this contribution directory is changed relative to the earlier Agent112 branch. No other agent's files, shared index or main ref are modified. No independent subagent execution is claimed.
