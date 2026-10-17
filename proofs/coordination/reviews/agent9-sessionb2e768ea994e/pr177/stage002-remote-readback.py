#!/usr/bin/env python3
"""Verify the exact binary archive downloaded from the published commit."""
from pathlib import Path
import hashlib
import json
base = Path(__file__).resolve().parent
local = (base / "evidence-checkpoint-002.tar.gz").read_bytes()
remote = (base / "publication-002-remote.tar.gz").read_bytes()
digest = hashlib.sha256(remote).hexdigest()
blob = hashlib.sha1(b"blob " + str(len(remote)).encode() + b"\0" + remote).hexdigest()
assert remote == local
assert len(remote) == 1702728
assert digest == "9d600b24635d2424539f4a9853cd940d1fd9b6bb27d8c76ffb4356969ee1ca5e"
assert blob == "83a5748e246c1779fcf6b501a09ab80564f91f5b"
result = {
    "status": "PASS_BYTE_EXACT_REMOTE_ARCHIVE",
    "commit": "d0f96e1a668c16dfe393494ec9530c88d1eb24af",
    "path": "proofs/coordination/reviews/agent9-sessionb2e768ea994e/pr177/evidence-checkpoint-002.tar.gz",
    "bytes": len(remote), "sha256": digest, "git_blob": blob,
    "download": "Read-only public raw GitHub URL at the immutable commit; approved execution after local proxy failure.",
    "prior_read_attempts": [
        "Contents tool returned encoding=base64, correct blob SHA, but content length zero.",
        "Generic Git blob read rejected non-UTF8 bytes.",
        "Dedicated fetch_blob returned UnicodeDecodeError.",
        "Default curl exited7 because the local browser-proxy endpoint was unreachable."
    ],
    "lean_execution": False
}
(base / "stage002-remote-readback.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))

