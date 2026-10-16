#!/usr/bin/env python3
"""Generate the exact tested PR58 repair from immutable Git blobs; never apply it."""
from pathlib import Path
import argparse, difflib, hashlib, subprocess

BASE_HEAD = 'b1cee0df38a410cce8462db56266860a4e7ec0be'
PATCH_SHA256 = 'f1f4412b92109462ab17c9944e6970f95878fe606b7ddb9247510db9b0a5ecdd'
BASE = 'proofs/contributions/agent-17/m99-a07-uniform-finite-seed/'
WORKFLOW = '.github/workflows/agent17-m99-a07-check.yml'
BLOBS = {
    WORKFLOW: '53345f7d23a3e58b8199b3121105a2a4f1f661ef',
    BASE+'README.md': '33709e0d2710621015e8957b4387f1eb040a450c',
    BASE+'UniformFiniteSeed.lean': 'af9a9ae132fd36df0bb0f40d6fe1b6c3bef2ce3c',
}
HELPER = '854d44271674d10575d02cd67d142c19cc3151ee'
ADAPTER = 'b329f9a549b82c463a549496ca5d96ba5af964ac'

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--cache', type=Path, help='Optional directory of <git-blob-sha>.txt files')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    def read(sha: str) -> str:
        data = (args.cache/(sha+'.txt')).read_bytes() if args.cache else subprocess.check_output(
            ['git', '-C', str(args.repo), 'cat-file', 'blob', sha])
        actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual != sha:
            raise ValueError('Git blob identity mismatch: '+sha)
        return data.decode('utf-8')
    old = {name: read(sha) for name, sha in BLOBS.items()}
    new = dict(old)
    new['proofs/Agent423/FiniteEnsemble.lean'] = read(HELPER)
    new[BASE+'UniformFiniteSeed.lean'] = read(ADAPTER)
    new[WORKFLOW] = old[WORKFLOW].replace(
        '      - proofs/contributions/agent-17/m99-a07-uniform-finite-seed/**',
        '      - proofs/contributions/agent-17/m99-a07-uniform-finite-seed/**\n      - proofs/Agent423/FiniteEnsemble.lean').replace(
        '          /tmp/lean-4.19.0-linux/bin/lean -i . -o /tmp/UniformFiniteSeed.olean',
        '          export LEAN_PATH=.\n          /tmp/lean-4.19.0-linux/bin/lean -o Agent423/FiniteEnsemble.olean Agent423/FiniteEnsemble.lean\n          /tmp/lean-4.19.0-linux/bin/lean -o /tmp/UniformFiniteSeed.olean')
    new[BASE+'README.md'] = old[BASE+'README.md'].replace(
        'Status: WIP pending pinned Lean 4.19.0 build.',
        'Status: written finite-ensemble result repaired by Agent #423; local Lean 4.19.0 build and all exported axiom queries pass. Independent review and main integration remain separate gates.').replace(
        '## Mathematical result',
        '## Interface repair\n\nThe former Std-only source referenced unavailable Fintype/Finset interfaces and failed elaboration. The repaired declaration takes an explicit fixed finite enumeration `enum : List alpha` plus `complete : forall x, x in enum`. This changes the Lean API, not the mathematical finite-universe hypothesis. The underlying implementation is Agent423.FiniteEnsemble. No Mathlib migration or extra all-time-safety premise is introduced. Original source and failure evidence remain pinned at PR58 head b1cee0df38a410cce8462db56266860a4e7ec0be.\n\nThe workflow uses LEAN_PATH for imports. The removed `-i .` option requests an ilean output file in this compiler; it does not specify an import directory.\n\n## Mathematical result')
    patch = ''
    for name, text in new.items():
        before = old.get(name, '')
        if before == text:
            continue
        patch += f'diff --git a/{name} b/{name}\n'
        if name not in old:
            patch += 'new file mode 100644\n'
        patch += ''.join(difflib.unified_diff(before.splitlines(True), text.splitlines(True),
            fromfile='a/'+name if name in old else '/dev/null', tofile='b/'+name))
    encoded = patch.encode('utf-8')
    actual = hashlib.sha256(encoded).hexdigest()
    if actual != PATCH_SHA256:
        raise ValueError('Generated patch differs from the checked candidate: '+actual)
    args.output.write_bytes(encoded)
    print('Generated', len(encoded), 'bytes; SHA256', actual, '; base', BASE_HEAD)

if __name__ == '__main__':
    main()
