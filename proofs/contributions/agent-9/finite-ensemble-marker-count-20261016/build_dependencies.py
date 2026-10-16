#!/usr/bin/env python3
"""Build only missing pinned dependencies in the private author directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

package = Path(__file__).resolve().parent
repo = package.parents[3]
build = Path('/workspace/scratch/8dcaf4a67fa4/agent9-ensemble-author/dev')
for item in json.loads((package/'dependencies.json').read_text()):
    source = repo/item['current_path']
    data = source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['module']
    staged = build/(item['module']+'.lean')
    obj = build/(item['module']+'.olean')
    if staged.exists() and staged.read_bytes() == data and obj.exists() and obj.stat().st_size > 0:
        continue
    result = subprocess.run([sys.executable, str(package/'compile_attempt.py'), item['module'], str(source)])
    if result.returncode:
        sys.exit(result.returncode)
