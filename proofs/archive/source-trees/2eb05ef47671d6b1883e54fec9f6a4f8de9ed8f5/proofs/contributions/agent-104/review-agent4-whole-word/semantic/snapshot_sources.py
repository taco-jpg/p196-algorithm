#!/usr/bin/env python3
"""Read-only immutable Git export for the Agent 104 semantic review."""
import hashlib
import json
import pathlib
import re
import subprocess

PIN = '4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7'
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
PATHS = [
    'proofs/research/continuation/LychrelDigitSums.lean',
    'proofs/agent4/prefix_growth/PrefixModel.lean',
    'proofs/agent4/prefix_growth/SaturationCertificate.lean',
    'proofs/agent4/prefix_growth/SaturationTheorem.lean',
    'proofs/agent4/prefix_growth/integration/WholeWordBridge.lean',
]

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

def main():
    assert git('rev-parse', PIN).decode().strip() == PIN
    records = []
    for source in PATHS:
        data = git('show', f'{PIN}:{source}')
        target = HERE / 'source-snapshot' / pathlib.Path(source).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append({
            'source': source,
            'snapshot': str(target.relative_to(HERE)),
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': git('rev-parse', f'{PIN}:{source}').decode().strip(),
            'imports': re.findall(r'^import ([^\n]+)', data.decode(), flags=re.M),
        })
    result = {'source_commit': PIN, 'sources': records,
              'non_repository_dependencies': ['Lean 4.19.0 standard library: Std and Lean.Elab.Tactic.Omega'],
              'evidence_label': 'source identity only; no compilation performed by semantic reviewer'}
    (HERE / 'source-manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
