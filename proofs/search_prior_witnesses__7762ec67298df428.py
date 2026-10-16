#!/usr/bin/env python3
"""Retain exact-token prior occurrence search at the immutable review pin."""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
PIN = '4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7'

def main():
    results = []
    for number in (89870, 179745797, 770, 176176):
        args = ['git', '-C', str(REPO), 'grep', '-n', '-w', str(number), PIN, '--', 'proofs']
        p = subprocess.run(args, capture_output=True, text=True)
        assert p.returncode in (0, 1), p.stderr
        name = f'exact-prior-occurrence-{number}.txt'
        (HERE/name).write_text(p.stdout)
        results.append({'command': args, 'returncode': p.returncode,
                        'lines': len(p.stdout.splitlines()), 'output': name})
    out = {'source_commit': PIN, 'scope': 'tracked proofs text at pinned main; not a literature search',
           'searches': results}
    (HERE/'exact-prior-occurrences.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
