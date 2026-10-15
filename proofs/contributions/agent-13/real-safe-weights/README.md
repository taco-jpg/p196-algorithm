# Exact real safe incoming-weight obstruction

Agent #13 formalizes section 3 of `FINITE_SEED_OBSTRUCTIONS.md` at source snapshot `c2b6977e43a79caa5ff3bb88801f3ba896986f38`. This is independent formalization of the existing written mathematics, not a claim of original discovery. The decimal complementary-family dependency is in `../safe-predecessor-family/`.

## Mathematical coverage

`Agent13SafeWeights.mem_safeFiber_iff` proves that the finite encoding contains exactly every actual safe predecessor, using the unchanged `Lychrel196.step`. The full incoming operator is not defined to be the displayed family sum. Positivity and order reversal are assumed only on the safe set; values outside it are unrestricted.

For every real-valued weight satisfying those premises and every integer parameter `m>=2`, `incoming_weight_ratio` gives the exact lower bound `9*10^(m-2)` at `y_m=10^(2*m)+99*10^(m-1)-1`. `no_uniform_multiplier` proves that every finite real multiplier fails somewhere on the safe set, including negative proposed multipliers. `not_exists_uniform_bound` states the equivalent negated-existence form. `incoming_weight_sqrt_lower` proves the source's strict lower bound `(9/100)*sqrt(10/11)*sqrt(y_m)` on that same ratio.

There are 15 new theorem declarations, supported by the 36 previously checked family declarations. These are declaration counts, not 51 independent research discoveries. The three original weight conclusions have exact coverage. No theorem about indefinite survival, a Lychrel witness, or 196 is added.

## Verification status

The two new modules compiled locally, and all 15 transitive axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. A separate empty-directory rebuild then compiled the unchanged decimal source, all three family modules, both real-weight modules, and a combined 51-theorem axiom audit, each with exit status 0. This is `LEAN_CHECKED`, not independent-agent review or default-branch integration. The CI workflow in this contribution repeats that audit in a separate GitHub runner; its actual run result must be checked rather than inferred from this README.

Mathlib is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b`, with the same existing Lean 4.19.0 compiler (`6caaee842e94`). Its dependency manifest is checked byte-for-byte. Development used the official compiled-library cache; all 7,265 transferred source hashes were verified. The clean contribution build is not described as a complete Mathlib source rebuild. The original Std-only family checker still needs no Mathlib and is unchanged.

## Reproduction

Prepare a clean Mathlib checkout at the exact commit above with its pinned dependencies and the official cache for the four imports listed in `.github/workflows/agent13-real-weights.yml`. Do not migrate the toolchain or run an unpinned dependency update. Then run:

```sh
python3 proofs/contributions/agent-13/real-safe-weights/check.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --mathlib /absolute/path/to/pinned/mathlib \
  --out /new/audit/directory
```

The checker validates library pins, rejects modified previously checked family sources, rebuilds into a fresh temporary directory, and audits every exported theorem. For the Git-metadata-free development artifact, also supply `--library-audit /path/to/library-audit`; its exact source-index digest is checked. Do not invoke Lake inside that transferred Git-free tree: use the explicit-path checker or a normal Git checkout.

Independent semantic review and integration remain pending. This result excludes the specified nonincreasing-weight method; it does not exclude arbitrary other weight constructions or settle the research problem.
