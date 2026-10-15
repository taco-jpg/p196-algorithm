# Agent #13 — retained proof evidence

The two binary parts preserve one lossless XZ-compressed tar archive of the actual local baseline, development failures, clean builds, commands, exit statuses, source hashes, and all transitive axiom reports. No runtime binaries or compiled project objects are included. Failed proof sources remain evidence, not accepted build targets.

```sh
cd proofs/contributions/agent-13/audit
cat proof-evidence-01.xz.part00 proof-evidence-01.xz.part01 > proof-evidence-01.tar.xz
echo '58d47b910f1791c81cd4185c4c1191aa2febd47038cc0ee9b708da9c0bda3453  proof-evidence-01.tar.xz' | sha256sum -c -
mkdir extracted
tar -xJf proof-evidence-01.tar.xz -C extracted
```

The reconstructed archive is 18,400 bytes. Its internal `MANIFEST.json` records every other member's exact path, size and SHA-256. Stored Git blob IDs are `f07d1d6aa5463afe2a48d6b6e86be37716ea69dc` and `e3c9b97d30d0fd8d1cbc7f90412b7cc3b9419db3` in concatenation order.

`audit/clean-family/` contains the full Std-only 36-theorem clean build. `audit/clean-weights/` contains the full 51-theorem fresh contribution build, unchanged decimal core included. `audit/ci-family/` is the independently hosted GitHub runner's 36-theorem evidence at `4f09ed9b9b2d86037c1f37bc78802dbfa7929686`. Every accepted result's transitive axiom report contains only `propext`, `Classical.choice`, and `Quot.sound`. Independent semantic review has not yet occurred.

The initial core attempt hit a container execution boundary before completion; it is preserved separately from the later successful baseline. Failed local Family/TargetSafety/Counting proof attempts are retained under `development/` and never imported by accepted checkers. A Git-metadata-free Lake probe attempted to reclone a dependency; that directory was restored from the exact artifact and all 7,265 library source hashes were reverified. This infrastructure event is not a theorem failure. The real dependency uses the official compiled Mathlib cache, not a claimed complete source rebuild of Mathlib.

The internal inventory is an immutable checkpoint. Its historical reference to `checkpoint-01.tar.xz` names the larger local archive from which this proof-evidence archive was losslessly selected. The current public inventory instead points here. The omitted exploratory 133-row FINDINGS index is not a semantic census; original table rows remain in the pinned source and the discovery workflow is retained.

## Later verified CI checkpoint

The real-weight workflow at `f4d2f159c955ade70e74fe06bda77ec6e8a7aa13` completed successfully: run `38688269514`, artifact `11949934665` (`agent13-real-safe-weight-kernel-audit`). Its downloaded ZIP SHA-256 is `77509b53b12bafcf5e9448db6f09cab38909ecd0b2bef45bc774b22d68801ebf`. All seven source/audit compilation steps exited 0, with all 51 theorem reports present. The ZIP also contains exact contribution sources. This later CI artifact is not silently included in the earlier archive. The committed workflow reproduces it when ephemeral artifact retention ends.
