# Agent 122: a quantitative terminating decimal countermodel

Status: **LEAN-CHECKED**, not independently reviewed and not integrated. AI-assisted formalization. No novelty claim and no conclusion about the actual orbit of 196.

## What is established

Write `T = Lychrel196.step`, `P = Lychrel196.Palindrome`, and `B(n) = P(T(n))`. This package formalizes the original countermap in [FINITE_SEED_OBSTRUCTIONS, section 2](../../../research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md), on ordinary decimal natural numbers with the existing palindrome predicate.

The same fixed map `F` satisfies all of the following:

- `F(n) = T(n)` on **every** `B` input, and `P(F(n))` iff `B(n)` on every natural number.
- For each positive `n`, `n < F(n) < 11*n`; one step preserves decimal width or adds one digit. Outside `B`, it adds exactly one digit.
- For every positive `n` and time `t`, `width(n) + t/5 <= width(F^t(n))`, where division is natural-number division.
- Every positive seed reaches a palindrome at a **positive finite time**, including a seed which was already palindromic at time zero.
- Nevertheless, for every finite horizon `R`, some positive seed stays nonpalindromic through all times `0..R`. In fact, exact finite first-hit times are unbounded.

The last two clauses use one fixed map, chosen before the horizon. Thus the package proves an actual counterexample to the relevant quantifier interchange, not merely a family of unrelated finite examples. `Terminates` means a finite palindrome hit; the mathematical iteration remains total after that hit.

The labels are exactly `c(a,j) = 10^(a+j) + 10*a + 9`, for `a >= 3`. They are injective, canonically have `a+j+1` digits, are nonpalindromic, and do not belong to the true set `B`. For any finite-valued `ell`, `F` follows `c(a,0), ..., c(a,ell(a))`, then `10^(a+ell(a)+1)+2`, whose genuine next reverse-and-add result is palindromic. The first hit from `c(a,j)` is exactly `ell(a)-j+2`. The fixed instance `ell(a)=a` supplies unbounded finite first-hit times. Generic non-`B` inputs join these chains according to their actual decimal width.

`F` is a noncomputable Lean definition using classical choice of the uniquely proved sparse label. No executable implementation or oracle evaluation is being passed off as a proof.

## Important limit, also proved

This is **not** a countermodel to all structural facts already in the repository. The genuine orbit has the stronger upper width clock

```
2 * width(T^t(n)) <= 2 * width(n) + t + 3.
```

Our countermap violates that inequality at time four for every `c(a,0)` with `a >= 4`. `countermap_violates_upper_clock` and `countermap_fourth_iterate_not_actual` prove this symbolically. The latter explicitly separates the countermap from the true orbit. This does not contradict the original report's listed one-step upper bound or five-step lower bound.

The accepted clauses here do not include density estimates, the pair-word-factorized variant, a finite-seed extraction theorem for actual RAA, a Lychrel seed in any base, or a statement about 196. Those historical claims and other agents' results keep their own evidence labels.

## Entry points and evidence

The main endpoint is `Agent122.Countermodel.quantitative_terminating_countermodel`. Other consequential exports are `F_exact_predecessors`, `node_first_hit`, `every_positive_seed_terminates`, `fixed_map_unbounded_first_hits`, `finite_prefix_extraction_fails`, `F_numeric_growth`, `run_width_five_floor`, and the two upper-clock discrepancy theorems.

`All.lean` imports every candidate module. `Audit.lean` audits all 60 exported declarations, including supporting lemmas and explicitly reused/replicated facts; **60 is not a count of novel theorems**. The candidate source lists are in `accepted-modules.json`. `VERIFICATION.json` pins source hashes and the completed fresh build. Historical failed attempts and complete build logs are retained in `evidence.json.xz` as a JSON map of UTF-8 file contents and per-file hashes; none of those attempts belongs to the accepted module list.

The final `clean-03` rebuild started with an empty build directory, recompiled all six source dependencies and all candidate modules, and passed every stage. The transitive axiom union is `propext`, `Classical.choice`, `Quot.sound`. These are explicitly allowed foundational dependencies; choice also implements the unique-label selector. No audited chain has `sorryAx`, `Lean.ofReduceBool`, or another excluded oracle axiom. No `native_decide`, unfinished theorem, or external computation supplies a proof.

## Reproduce

From the repository root, with pinned Lean 4.19.0 (release commit `6caaee842e94`):

```sh
python3 proofs/contributions/agent-122/finite-seed-countermodel/reproduce.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-empty-build-directory
```

The output path must not already exist. The checker verifies the Lean release and every dependency hash, records all candidate source hashes, compiles the complete candidate, and checks the transitive axiom list for every export. It retains substantive logs, commands and exit statuses. This execution is not independent review merely because it uses a fresh directory.

Dependencies are fixed at main `eec3d5f3646cab50abad6e610ea19626cd249070`. Agent108's `LeadingWitness`, Agent13's `Family`, Agent12's `FixedTarget` and the original `FiniteAncestry` are reused. The local `decimalLength_positive` helper replicates the earlier `DecimalFiniteAncestry.decimalLength_positive`; no novelty is claimed for it or the true-orbit clock restatements.

One explicit import-only adapter is needed: a disposable copy of Agent108's `AutonomyDefs` imports `LychrelDigitSums` instead of `Lychrel196Research`. The checker verifies that the full original base source after `import Std` occurs byte-identically inside that continuation, and verifies both original and adapted hashes. This avoids duplicate global declarations; no collaborator's file is edited. No runtime binaries, dependency archives or compiled objects are committed.
