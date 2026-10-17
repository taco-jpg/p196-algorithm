python3 - proofs/REPRODUCE.md <<'PY'
import hashlib
import json
import os
import sys
from pathlib import Path

mapping = json.loads(Path("proofs/SOURCE_MAP.json").read_text(encoding="utf-8"))
original = sys.argv[1]
entry = mapping["paths"][original]
selected = entry.get("current") or entry["preserved"]
path = Path(selected)
data = os.fsencode(os.readlink(path)) if entry["mode"] == "120000" else path.read_bytes()
actual = hashlib.sha256(data).hexdigest()
print("baseline:", mapping["base"])
print("original:", original)
print("selected:", selected)
print("sha256:", actual)
if actual != entry["sha256"]:
    raise SystemExit("Selected bytes do not match the historical source map")
print("source hash: MATCH")
PY
