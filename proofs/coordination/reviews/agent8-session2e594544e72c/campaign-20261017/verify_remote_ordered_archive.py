#!/usr/bin/env python3
"""Verify exact published PR172 ordered-extension archive bytes at a pinned commit."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--commit', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--receipt', required=True)
args = parser.parse_args()
assert len(args.commit) == 40 and all(c in '0123456789abcdef' for c in args.commit)
expected_size = 2038636
expected_sha256 = '38917efc35bfa34be3a214a1c497cace6bdc78c688b654f3f96808041db104ba'
expected_blob = 'ea6bbe7f3010a26402a6b10e28940343af8ddb99'
repo_path = 'proofs/coordination/reviews/agent8-session2e594544e72c/pr172/ordered-combination/pr172-ordered-extension.tar.xz'
url = 'https://raw.githubusercontent.com/taco-jpg/p196-algorithm/' + args.commit + '/' + repo_path
sha256 = hashlib.sha256()
git_blob = hashlib.sha1(b'blob ' + str(expected_size).encode() + b'\0')
count = 0
started = time.monotonic()
with urllib.request.urlopen(url, timeout=45) as response, Path(args.output).open('xb') as output:
    while True:
        data = response.read(65536)
        if not data:
            break
        output.write(data)
        count += len(data)
        sha256.update(data)
        git_blob.update(data)
result = {
    'commit': args.commit,
    'repository_path': repo_path,
    'url': url,
    'bytes': count,
    'sha256': sha256.hexdigest(),
    'git_blob': git_blob.hexdigest(),
    'elapsed_seconds': time.monotonic() - started,
    'exact': count == expected_size and sha256.hexdigest() == expected_sha256 and git_blob.hexdigest() == expected_blob,
}
Path(args.receipt).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
assert result['exact'], result
