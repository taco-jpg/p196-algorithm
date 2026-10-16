#!/usr/bin/env python3
"""Independent fresh-source verification of Agent 3's cardinality module."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
CONTRIBUTION = HERE.parents[1]
REPO = HERE.parents[5]
SOURCE_RECORDS = [
    ('PeriodObstructions', REPO / 'proofs/PeriodObstructions__70ce034b31b5b218.lean',
     '83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a'),
    ('ActualWordBridge', REPO / 'proofs/ActualWordBridge__7f032d27940694a8.lean',
     '3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6'),
    ('FamilyDefinitions', CONTRIBUTION / 'FamilyDefinitions.lean',
     '497ffe833495c50e7df5714fd50c0a4835aaf96f71ec8d21fc43102b1468a1d4'),
    ('FamilyCardinality', CONTRIBUTION / 'FamilyCardinality.lean',
     'dfded4df411694fcbe50487e7a963f45c7e0abe34e46ed828926aee9f329248d'),
]
EXPECTED_LEAN = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
ALLOWED_AXIOMS = {'propext', 'Quot.sound', 'Classical.choice'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--lean', required=True, type=Path)
    parser.add_argument('--build-dir', required=True, type=Path)
    args = parser.parse_args()
    lean = args.lean.resolve()
    build = args.build_dir.resolve()
    build.mkdir(parents=True, exist_ok=False)
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=True)
    assert sha256(lean) == EXPECTED_LEAN
    report = {
        'reviewer': 'Agent #3 runtime/dependency specialist',
        'author_independent': True,
        'claim_id': '55c0133a597cd3577fbbb864414fe4527729e554',
        'compiler': str(lean), 'compiler_sha256': EXPECTED_LEAN,
        'build_directory': str(build), 'fresh_directory': True,
        'source_records': [], 'commands': [],
    }
    for module, source, expected in SOURCE_RECORDS:
        actual = sha256(source)
        assert actual == expected, (source, actual, expected)
        target = build / (module + '.lean')
        target.write_bytes(source.read_bytes())
        assert sha256(target) == expected
        report['source_records'].append({
            'module': module, 'source': str(source),
            'build_copy': str(target), 'sha256': expected,
        })
    audit = '''import FamilyCardinality

namespace P196.Agent3.OverflowHorizon.CardinalityIndependentReview

open P196.Agent3.OverflowHorizon

theorem exact_enumeration (xs : List Bool) (m : Nat) :
    xs ∈ allBits m ↔ xs.length = m := mem_allBits_iff xs m

theorem no_unpaired_center (xs : List Bool) (k i : Nat) :
    2 * i + 1 ≠ (inputWord xs k).length := by
  rw [inputWord_length]
  omega

theorem exact_distinct_family (m k : Nat) :
    (familyWords m k).length = 2 ^ m ∧
    (familyWords m k).Nodup ∧
    ∀ w ∈ familyWords m k,
      Agent8.CanonicalPair w ∧ w.length = 2 * (m + k + 1) ∧
        w.length % 2 = 0 := familyWords_exact m k

#print axioms exact_enumeration
#print axioms no_unpaired_center
#print axioms exact_distinct_family
#print axioms P196.Agent3.OverflowHorizon.choice
#print axioms P196.Agent3.OverflowHorizon.inputHalf
#print axioms P196.Agent3.OverflowHorizon.inputWord
#print axioms P196.Agent3.OverflowHorizon.target

end P196.Agent3.OverflowHorizon.CardinalityIndependentReview
'''
    (build / 'CardinalityIndependentReview.lean').write_text(audit)
    (HERE / 'CardinalityIndependentReview.lean').write_text(audit)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(build)
    axiom_union = set()
    for module in [m for m, _, _ in SOURCE_RECORDS] + ['CardinalityIndependentReview']:
        argv = [str(lean), '-o', module + '.olean', module + '.lean']
        start = time.monotonic()
        result = subprocess.run(argv, cwd=build, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout
        (logs / (module + '.log')).write_text(output)
        command = {'argv': argv, 'cwd': str(build), 'LEAN_PATH': str(build),
                   'exit_code': result.returncode, 'seconds': time.monotonic() - start,
                   'log': str(logs / (module + '.log'))}
        report['commands'].append(command)
        (HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
        print(module, 'exit', result.returncode, 'seconds', round(command['seconds'], 3), flush=True)
        if result.returncode:
            print(output, flush=True)
            raise SystemExit(result.returncode)
        assert 'sorryAx' not in output and 'Lean.ofReduceBool' not in output
        assert not re.search(r'declaration uses .*sorry', output)
        for group in re.findall(r'axioms: \[([^\]]*)\]', output):
            axiom_union.update(a.strip() for a in group.split(',') if a.strip())
        command['olean_sha256'] = sha256(build / (module + '.olean'))
    assert axiom_union <= ALLOWED_AXIOMS, axiom_union
    source_audit = (logs / 'FamilyCardinality.log').read_text()
    cardinality_audits = re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)", source_audit)
    assert len(cardinality_audits) == 24, len(cardinality_audits)
    for _, source, expected in SOURCE_RECORDS:
        assert sha256(source) == expected, 'Source changed during independent build: ' + str(source)
    report['family_cardinality_audited_declarations'] = cardinality_audits
    report['axiom_union'] = sorted(axiom_union)
    report['sources_unchanged_after_build'] = True
    report['result'] = 'PASS'
    (HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: fresh closure, 24 cardinality declaration audits, independent center check; axioms', sorted(axiom_union))


if __name__ == '__main__':
    main()
