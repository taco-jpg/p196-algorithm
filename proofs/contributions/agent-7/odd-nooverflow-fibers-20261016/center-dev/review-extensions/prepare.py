"""Restore excluded byte-identical dependency copies before a fresh review build."""
from pathlib import Path
import hashlib
import json
import shutil

root = Path(__file__).resolve().parent
contribution = root.parent.parent
pins = json.loads((root / "source-sha256.json").read_text())
for mod in ["InverseFibers", "PathCounts", "WordBridge", "OddCenter", "OddCounts"]:
    original = (contribution / "dependencies" if mod in
                {"InverseFibers", "PathCounts", "WordBridge"} else contribution) / (mod + ".lean")
    target = root / "source" / (mod + ".lean")
    assert hashlib.sha256(original.read_bytes()).hexdigest() == pins[mod]["sha256"], mod
    if not target.exists():
        shutil.copyfile(original, target)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == pins[mod]["sha256"], mod
print("Five pinned dependency copies are present and byte-identical.")
