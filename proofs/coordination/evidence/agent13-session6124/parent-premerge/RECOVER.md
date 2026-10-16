# Recover the parent premerge evidence checkpoint

The adjacent `parent-integration-evidence-premerge.ARCHIVE_RECEIPT.json` identifies the compressed byte count and SHA-256, pins the full manifest, and records byte-for-byte verification of every archive member. Check that identity before extraction.

Create a new output directory:

```sh
mkdir recovered-parent-premerge
tar -xJf parent-integration-evidence-premerge.tar.xz -C recovered-parent-premerge
```

The extracted root is `recovered-parent-premerge/parent-package`. The `scratch/` and `memory/` groups preserve the input structure; original absolute paths appear in `INPUT_SNAPSHOT_MANIFEST.json`. Historical execution paths inside original logs remain untouched.

Run this standard-library check from the recovered package root to verify its file identities:

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json
root = Path.cwd()
manifest = json.loads((root / 'MANIFEST.json').read_text())
for record in manifest['files']:
    data = (root / record['package_path']).read_bytes()
    assert len(data) == record['bytes'], record['package_path']
    assert hashlib.sha256(data).hexdigest() == record['sha256'], record['package_path']
print('Every manifest-listed file matches its recorded bytes and SHA-256.')
PY
```

The manifest omits itself to avoid a circular hash; the outer receipt pins its own identity. `PRESERVATION_CHECKS.json` identifies the lossless restoration of the complete initial report. Earlier failures remain failures in the original records. This checkpoint makes no claim that a merge or additional Lean audit occurred.
