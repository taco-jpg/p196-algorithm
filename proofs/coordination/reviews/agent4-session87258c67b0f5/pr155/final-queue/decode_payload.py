#!/usr/bin/env python3
"""Decode one exact base64 publication payload without overwriting any file."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import resource

LIMIT = 1024 * 1024 * 1024
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
resource.setrlimit(resource.RLIMIT_AS, (min(LIMIT, hard) if hard != resource.RLIM_INFINITY else LIMIT, hard))
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("payload")
p.add_argument("metadata")
p.add_argument("destination")
args = p.parse_args()
metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
encoded = Path(args.payload).read_bytes()
if encoded.endswith(b"\n"):
    encoded = encoded[:-1]
body = base64.b64decode(encoded, validate=True)
expected = metadata["archive"]
actual_git = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
actual_sha = hashlib.sha256(body).hexdigest()
if len(body) != expected["bytes"] or actual_sha != expected["sha256"] or actual_git != expected["git_blob"]:
    raise ValueError("Decoded payload does not match the exact archive identity")
with Path(args.destination).open("xb") as output:
    output.write(body)
print(json.dumps({"status": "PASS", "bytes": len(body), "sha256": actual_sha, "git_blob": actual_git, "destination": args.destination}, indent=2))
