# Reproduce Agent #14's selected-source audit

Read REPORT.md for mathematical scope and evidence-ledger.json for claim-level dispositions. This procedure replays a fixed 24-source, 629-public-identifier inventory; it does not discover or certify every repository theorem.

## Published completed execution

GitHub workflow run: **38689475631**, source audit commit `f48c8e03e76501cbaac8ef7b32155d5f821cf367`.

Permanent evidence commit on the owned audit branch: **`062e75ff3f0c60770ddad1a39f1ba82d971a53b7`**.

Evidence directory: `evidence/ci-38689475631/`. It contains `execution.json`, `selected_manifest.json`, `Agent14SelectedAudit.lean`, every module/audit stdout log, and `SHA256SUMS`. The uploaded matching artifact is 11952041091, `agent14-selected-replay`, ZIP SHA-256 `b2ac8b99cbbc364b63dca7dd4f6e0f297aa65abe6058ff75c06ed8f330aa2cba`. The artifact expires on 2026-11-14; the committed files do not depend on that artifact remaining available.

The independent local combined replay and GitHub replay have byte-identical full audit stdout:

```text
bbe77ab10d1788ec598f0282c458aaaaf3ce23420ee3ce1492078be306ab260d
```

The exact audit driver hash is:

```text
cfcc1085db64fd56c70e29cc4029543f78dfb03f5864119e4f7d69507757406a
```

Both complete records report PASS, 24 successful source modules, and 629 named transitive axiom queries. All 26 commands (version, 24 module builds, final audit) returned zero. A proof review of every one of those 629 mathematical statements is not claimed; important endpoint definitions, quantifiers, and arithmetic bridges received separate semantic review.

## Local command sequence

Use the official Linux x86_64 Lean 4.19.0 distribution. Other platforms have different compiler hashes and will be rejected by this exact replay.

```sh
curl --fail --location -o lean.tar.zst \
  https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst
printf '%s  %s\n' \
  6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe \
  lean.tar.zst | sha256sum -c -
tar --zstd -xf lean.tar.zst
```

Prepare two source checkouts, or use the byte-identical selected source copies supplied with the delivered audit archive:

```sh
git clone https://github.com/taco-jpg/p196-algorithm.git early
git -C early checkout --detach f49d2fa2319d34e3f97fc94e49523c3ed3e056f4
git clone https://github.com/taco-jpg/p196-algorithm.git late
git -C late checkout --detach eb893f01c3d9f6e46007178326d7b19f92529d3e
```

From a checkout containing this audit directory, set `scripts` to its `reproduce/` folder. Neither output path below may already exist:

```sh
scripts=/path/to/audit/reproduce
python "$scripts/prepare_manifest.py" \
  --spec "$scripts/source_spec.json" \
  --early-root early --late-root late \
  --output selected_manifest.json
python "$scripts/replay_selected.py" \
  --early-root early --late-root late \
  --lean "$PWD/lean-4.19.0-linux/bin/lean" \
  --manifest selected_manifest.json \
  --output new-agent14-replay
```

The compiler binary must hash to `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Each selected source is hash-checked before compilation and after its build. `LEAN_PATH` points only to the new project build directory; no historical project objects are reused. The runtime supplies Std.

The declaration scanner is explicitly reused from the exact Agent #105 checker named and hashed in `source_spec.json`. The resulting sorted identifier inventory must reproduce SHA-256 `0adbf8f383a7265d2b01007b6f0e2f92843bf2517f986960876802b28f2ff90b`. The final independent parser requires exactly one result for every expected identifier and accepts only `propext`, `Classical.choice`, and `Quot.sound`. Multiline axiom lists are parsed rather than silently skipped. No absent, duplicate, or unexpected result is accepted.

The own-branch workflow `.github/workflows/agent14-selected-replay.yml` performs this same process from pinned checkouts. Its only write is the unique per-run evidence directory on `audit/agent-14/20261015T050330-rebuild`, using an ordinary non-force push. It neither changes proof sources nor writes to main.

## Additional original local evidence

The delivered original-session archive retains all 81 text records selected for archival, including earlier separate builds, commands, source/object fingerprints, complete transitive outputs, the interrupted-attempt record, and the five-certificate Python replay. Its lossless payload is `original-local-evidence.json.xz`, 39,468 bytes, SHA-256 `7db52ee60e9adf366247ed74cee2a12717ae1ff4605de27bc69a98bceedcd58e`. Decompressed UTF-8 JSON is 572,204 bytes, SHA-256 `2b42b1ac2d674a7a91eebd47b3f446da278abf331cd45f8b8f1cbc3cb29c83fa`.

The original local archive and the later committed CI records are distinct provenance records. The CI replay is not presented as the original local timestamps or command paths. The archive's file inventory supplies each original path, byte count and SHA-256. It contains text under a top-level `files` object and can be inspected without extraction:

```python
import hashlib, json, lzma
from pathlib import Path
blob = Path('original-local-evidence.json.xz').read_bytes()
assert hashlib.sha256(blob).hexdigest() == '7db52ee60e9adf366247ed74cee2a12717ae1ff4605de27bc69a98bceedcd58e'
raw = lzma.decompress(blob)
assert hashlib.sha256(raw).hexdigest() == '2b42b1ac2d674a7a91eebd47b3f446da278abf331cd45f8b8f1cbc3cb29c83fa'
files = json.loads(raw)['files']
print('\n'.join(files))
```

## Rolling queue, not new assignments

- Agent #104 concrete 739 checks: all rank rows, all initial words, all short sources, then instantiate the ordinary integer endpoint and audit it. Existing generic statements still expose those premises.
- Agent #103 / Agent #9 scalar chain: every production JobChecks module, ScalarHierarchy.finite_root_bound, RootBridge.certificate_of_finite_root_bound, and the ScalarBound numeric endpoints. Preserve their acknowledged primary/independent split and keep any table refactoring experimental until equivalence plus unchanged row proofs pass.
- Template coverage: transport Agent #8's eight-phase word theorem through Agent109.Compat for the missing ordinary endpoint phases 6 and 12.
- Exterior applicability: fresh-review/rebuild the newer Agent #6 ExteriorArithmetic factor and determine its exact iteration hypotheses, rather than claim that no arithmetic factor exists.
- Reporting/integration: repair A14-D01; record acknowledgment of the new Agent #105 review; identify each package's accepted default build target. Selected audit CI and default-branch source inclusion are not the same thing.
- Remaining coverage: inspect the currently unreviewed Agent #101/#106/#107/#108 contributions, newer Agent #102/#109 changes, and later source heads before making any new verification claim about them.
