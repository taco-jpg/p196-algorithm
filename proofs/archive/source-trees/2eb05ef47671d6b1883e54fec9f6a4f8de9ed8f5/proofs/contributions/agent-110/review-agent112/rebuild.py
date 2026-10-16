#!/usr/bin/env python3
"""Independent exact-commit rebuild of Agent112's automatic admissibility."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import time

WORK = Path('/workspace/scratch/63e10b24caf2')
REPO = WORK / 'p196-algorithm'
HERE = Path(__file__).resolve().parent
BUILD = WORK / 'agent112-review-build'
LEAN = WORK / 'runtime-audit/lean'
PIN = 'e7689d35f41ff325037a238cfc594d95e0da04e1'
MODULES = [
    'proofs/contributions/agent-109/template-step-bridge/TemplateStep.lean',
    'proofs/contributions/agent-109/template-return-certificate/ReturnCertificate.lean',
    'proofs/contributions/agent-112/certificate-admissibility/AdmissibleCenters.lean',
    'proofs/contributions/agent-112/certificate-admissibility/SymbolicGrowth.lean',
    'proofs/contributions/agent-112/certificate-admissibility/AdmissibleHeads.lean',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    BUILD.mkdir(exist_ok=False)
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=False)
    scanner_path = REPO / 'proofs/contributions/agent-105/actual-high-return/check.py'
    scanner = runpy.run_path(str(scanner_path))
    provenance = json.loads((HERE / 'PROVENANCE.json').read_text())
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
        env.pop(key, None)
    env['LEAN_PATH'] = str(BUILD)
    record = {'status': 'RUNNING', 'reviewer': '/root/runtime_audit',
              'source_commit': PIN, 'source_repository': 'taco-jpg/p196-algorithm',
              'attribution': 'Original Agent112 mathematical work; copied and independently reviewed by Agent110 runtime/audit reviewer',
              'started_utc': datetime.now(timezone.utc).isoformat(),
              'fresh_initially_absent_build': str(BUILD), 'project_object_reuse': False,
              'author_checker_reused': False, 'LEAN_PATH': str(BUILD),
              'driver_sha256': sha(Path(__file__)),
              'scanner': {'path': str(scanner_path.relative_to(REPO)), 'sha256': sha(scanner_path),
                          'method': 'Explicit reuse of Agent105 code_only/public_theorems, not Agent112 checker'},
              'runtime': {}, 'sources': {}, 'commands': []}
    for relative in ['lean','app-path-compat.c','app-path-compat.so','lean-4.19.0-linux/bin/lean',
                     'lean-4.19.0-linux/lib/lean/libleanshared.so', 'lean-4.19.0-linux/lib/lean/libleanshared_1.so',
                     'lean-4.19.0-linux/lib/lean/libInit_shared.so']:
        record['runtime'][relative] = sha(WORK / 'runtime-audit' / relative)
    assert record['runtime']['lean-4.19.0-linux/bin/lean'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'

    def save():
        (HERE / 'verification.json').write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')

    def run(name, args):
        argv = [str(LEAN), *args]
        log = logs / (name + '.log')
        started = time.monotonic()
        print('START', name, flush=True)
        with log.open('w') as out:
            p = subprocess.run(argv, cwd=BUILD, env=env, stdout=out, stderr=subprocess.STDOUT, text=True)
        record['commands'].append({'name': name, 'argv': argv, 'cwd': str(BUILD),
                                   'returncode': p.returncode, 'seconds': round(time.monotonic() - started, 3),
                                   'log': str(log.relative_to(HERE)), 'log_sha256': sha(log)})
        save()
        print('END', name, p.returncode, flush=True)
        assert p.returncode == 0, name
        return log.read_text()

    try:
        version = run('version', ['--version']).strip()
        assert 'version 4.19.0' in version and 'commit 6caaee842e94' in version
        record['version'] = version
        all_names, available = [], {'Std'}
        for relative in MODULES:
            name = Path(relative).stem
            data = subprocess.check_output(['git', '-C', str(REPO), 'show', PIN + ':' + relative])
            blob = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', PIN + ':' + relative], text=True).strip()
            assert hashlib.sha1(('blob ' + str(len(data)) + '\0').encode() + data).hexdigest() == blob
            source_sha = hashlib.sha256(data).hexdigest()
            snapshot = HERE / 'source_snapshots' / (name + '.lean')
            if name in provenance['sources']:
                assert snapshot.read_bytes() == data
                assert source_sha == provenance['sources'][name]['source_sha256']
                assert blob == provenance['sources'][name]['git_blob_sha1']
            code = scanner['code_only'](data.decode())
            assert not re.search(r'\b(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool|unsafe|implemented_by)\b', code)
            imports = [x for line in re.findall(r'^import\s+([^\n]+)', code, re.M) for x in line.split()]
            assert set(imports) <= available, (name, imports)
            theorems = scanner['public_theorems'](data.decode())
            all_names.extend(item['name'] for item in theorems)
            record['sources'][name] = {'original_path': relative, 'source_commit': PIN,
                                       'sha256': source_sha, 'git_blob_sha1': blob,
                                       'imports': imports, 'public_theorems': theorems,
                                       'forbidden_token_scan': 'PASS'}
            (BUILD / (name + '.lean')).write_bytes(data)
            run(name, ['-j1', '-DElab.async=false', '-o', name + '.olean', name + '.lean'])
            assert sha(BUILD / (name + '.lean')) == source_sha
            record['sources'][name]['olean_sha256'] = sha(BUILD / (name + '.olean'))
            available.add(name)
            save()
        assert len(all_names) == len(set(all_names)) == 99
        audit = 'import AdmissibleHeads\n' + ''.join('#print axioms ' + name + '\n' for name in all_names)
        (HERE / 'AllTheorems.lean').write_text(audit)
        (BUILD / 'AllTheorems.lean').write_text(audit)
        output = run('AllTheorems', ['-j1', '-DElab.async=false', 'AllTheorems.lean'])
        rows = re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]", output, re.M)
        rows = [(name, sorted(a.strip() for a in values.split(',') if a.strip())) for name, values in rows]
        rows += [(name, []) for name in re.findall(r"^'([^\n]+)' does not depend on any axioms", output, re.M)]
        counts = Counter(name for name, _ in rows)
        assert set(counts) == set(all_names) and set(counts.values()) == {1}
        assert all(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, axioms in rows)
        for name, item in record['sources'].items():
            assert sha(BUILD / (name + '.lean')) == item['sha256']
            assert sha(BUILD / (name + '.olean')) == item['olean_sha256']
            if name in provenance['sources']:
                assert sha(HERE / 'source_snapshots' / (name + '.lean')) == item['sha256']
        record.update(status='PASS', completed_utc=datetime.now(timezone.utc).isoformat(),
                      all_public_theorem_count=len(all_names), reviewed_agent112_theorem_count=30,
                      axiom_audit=dict(sorted(rows)), source_hashes_unchanged=True,
                      signed_reviewer_identity='/root/runtime_audit — independent reviewer, not original author')
        save()
        print('PASS: five fresh modules; all 99 public theorem queries; 30 Agent112 theorems', flush=True)
    except Exception as exc:
        record.update(status='FAILED', error=repr(exc))
        save()
        raise


if __name__ == '__main__':
    main()
