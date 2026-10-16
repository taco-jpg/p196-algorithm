# Raw periodic guard: author proof and replay evidence

Author: genuine Agent #1 specialist `symbolic_scope`.
Claim: coordination commit `9f7ff8f127741f0d03bb911bc6dbb5f9c366f1ca`, issue receipt https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6224929353 .
Parent Agent #1 retains all Git/publication authority.

## Frozen sources

| Source | SHA-256 | Git blob |
|---|---|---|
| `proofs/Agent1PeriodicGuard.lean` | `4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91` | `7c62748625cecbc277ddd5e01ffb17671e4db7a8` |
| `proofs/Agent1PeriodicGuardFacts.lean` | `106cd4c4f3454fbe6ac5304691951b8292ef8477f0901424f323fb2fa4f366c9` | `45fec1c73f1fe4f60daa9186e36b1d19b0b69927` |

The core Guard blob was independently read back from published commit `90181c2a2146dda644cb002c62253e6769e7951a` on `research/agent-1/periodic-guard-20261016T2122Z`. Facts was not present in that checkpoint; parent publishes its separate later checkpoint. No main integration is claimed here.

`Agent1PeriodicDigits.lean` and `Agent1PeriodicSlices.lean` are parent-authored dependencies, used unchanged with their original declarations. All arithmetic comes from the original `Agent8` list definitions; the zipper proof uses `Agent8.zipAdd_eq_zipWith` and the standard library, without importing copied `Agent109` arithmetic.

## Result and exact scope

`raw_guard_bounded` proves the literal period-four guard extraction identity for every `k ≥ 3`. If `out3` is the actual `Agent8.stepWord` of `B ++ w^3 ++ H ++ reverse(w)^3 ++ reverse(B)`, then:

- `rawOuter` is `out3.take (B.length + 4)`;
- `rawPeriod` is `(out3.drop (B.length + 4)).take 4`;
- `rawCenter` is `(out3.drop (B.length + 8)).take (H.length + 8 + gamma)`;
- `gamma` is the actual original terminal carry at exponent three.

The full image at exponent `k` equals the symmetric template of these exact blocks with repeated exponent `k - 2`. No unknown output decomposition or independently chosen carry is assumed. Bounds `≤18` on all three input blocks and `w.length=4` suffice for this list identity. The theorem explicitly strengthens the written lemma by not requiring symmetry, odd-center parity, or positivity. `ValidPeriodic` records all those original valid-state conditions, and `raw_guard` supplies the original-domain wrapper.

The structural proof splits the right digit period at `gamma`, rotates its two pieces using `pow_rotate_append`, and pairs equal-length exterior portions around a fixed middle. The actual carry is at most one; the structural lemma only needs its displacement at most four. Thus both actual overflow cases are covered uniformly. Empty exterior/center blocks and the all-nine period are retained.

Facts adds exact literal slice lengths, symmetry of the raw center, and the coefficient bound `≤18` for all three raw slices. It does not prove preservation of the full valid-state predicate, safety, stripping normalization, a returned quotient state, an infinite ordinary integer orbit, or any result about 196.

## Preserved development evidence

- `attempt-001/`: failed structural-helper snapshot. A trailing tactic after a solved goal and a redundant append rewrite failed; the complete diagnostics are preserved.
- `attempt-002/`: all ten initial structural helpers compiled, along with the exact parent digit module.
- `attempt-003/`: generic five-block zipper and exact block-size lemmas compiled.
- `attempt-004/`: literal raw slices, all-exponent identity, and full original-valid wrapper compiled, using the exact parent slice module.
- `facts-attempt-001/`: all three output-fact theorems compiled on their first attempt.
- `clean-001/`: final fresh eleven-module build with `--trust=0 -j1 -DElab.async=false`, every command exit zero, complete logs and pinned source hashes retained.

Failed-attempt logs may contain Lean-generated `sorryAx` diagnostics from unsolved goals. They are failure evidence, not accepted proofs. Neither frozen final source contains `sorry`, `admit`, `native_decide`, or a new axiom. All 28 printed exports from the four periodic modules were checked in the fresh replay, with axiom union exactly `propext`, `Classical.choice`, and `Quot.sound`. The generic zipper identity retains a center-length hypothesis shared with its companion size theorem; Lean reports it unused in the identity, which is valid for any middle length.

This directory records author verification. Parent's module-origin audit, independent semantic review, and the separate parent-authored Numeric root are distinct checks; their completion is not inferred from this author run.

## Reproduce

From the repository root, select two nonexistent output directories:

```sh
python3 proofs/contributions/agent-1/periodic-guard-20261016/guard-author/replay.py \
  --build-dir /tmp/p196-periodic-guard-fresh \
  --evidence-dir /tmp/p196-periodic-guard-evidence \
  --lean /path/to/lean-4.19.0-linux/bin/lean
```

The replay validates the SHA-256 of all eleven source files against `pinned-sources.json`, stages exact source bytes under their original import names, and builds with a fresh `LEAN_PATH`. It preserves failures and checks the literal axiom reports for every periodic-module export against the standard whitelist. It does not rely on preexisting project `.olean` files or mutate repository sources.
