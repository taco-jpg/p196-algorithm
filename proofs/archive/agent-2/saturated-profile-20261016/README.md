# Agent #2 saturated-profile evidence archive

The six binary parts concatenate to one XZ-compressed USTAR archive. They retain 75 regular-file members, including the exact contents of all 27 original handoff files plus both clean-build evidence sets. Repackaging preserves each original file's bytes, not the original ZIP container encoding. `CONTENTS.json` records each other member's byte count 和 SHA-256; `TRANSPORT_AND_PRESERVATION.json` records original ZIP provenance 和 explicit infrastructure exclusions.

Reconstructed archive: 61,880 bytes. SHA-256:
`bc98d9936f5299bc6707ab3ff4f749a28818b2c0dc8bcad49303fa831c72384b`.
Uncompressed USTAR stream: 901,120 bytes. Part identities are recorded at the canonical path `proofs/Agent2SaturatedProfile.verification.json`.

Run from the repository root, using fresh temporary destinations:

```sh
cat proofs/archive/agent-2/saturated-profile-20261016/evidence.tar.xz.00[1-6] > /tmp/agent2-evidence.tar.xz
printf '%s  %s\n' bc98d9936f5299bc6707ab3ff4f749a28818b2c0dc8bcad49303fa831c72384b /tmp/agent2-evidence.tar.xz | sha256sum -c -
mkdir /tmp/agent2-evidence
tar -xJf /tmp/agent2-evidence.tar.xz -C /tmp/agent2-evidence
```

The complete archive was reconstructed from its parts, decompressed, 和 compared member-by-member against the packaged inputs before publication. Each uploaded part's Git blob was compared with the local object hash. Historical SOURCE_PRESENT/BUILD_BLOCKED records are deliberately preserved; the later successful build reports supersede their verification status, not their historical contents. No runtime installation or compiled proof cache is included.
