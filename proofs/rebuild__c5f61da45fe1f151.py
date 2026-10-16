#!/usr/bin/env python3
"""Independent fresh source rebuild and complete explicit-declaration audit."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

WORKSPACE = Path('/workspace/scratch/63e10b24caf2')
REPO = WORKSPACE / 'p196-algorithm'
HERE = Path(__file__).resolve().parent
BUILD = WORKSPACE / 'radix-review-build'
LEAN = WORKSPACE / 'runtime-audit/lean'
DEPS = 'proofs/contributions/agent6-complementary-bulk/'
SOURCES = [DEPS + name + '.lean' for name in ['ExteriorCore', 'ExteriorCapTwo', 'ExteriorCoverage']]
SOURCES += ['proofs/contributions/agent-110/exterior-global/RadixExterior.lean']
FROZEN_RADIX = '3aa5f400f939b7888a8e503cc1489514222701078449492f375681129c8e5716'
REVIEWER = '/root/runtime_audit (Agent 110 runtime/audit reviewer; separate from author)'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_comments(text):
    """Handle these sources' nested Lean comments; reject strings or generators."""
    result, depth, pos = [], 0, 0
    while pos < len(text):
        if text.startswith('/-', pos):
            depth += 1
            result.extend('  ')
            pos += 2
        elif depth and text.startswith('-/', pos):
            depth -= 1
            result.extend('  ')
            pos += 2
        elif depth:
            result.append('\n' if text[pos] == '\n' else ' ')
            pos += 1
        elif text.startswith('--', pos):
            end = text.find('\n', pos)
            end = len(text) if end < 0 else end
            result.extend(' ' * (end - pos))
            pos = end
        else:
            assert text[pos] != '"', 'String syntax requires separate review'
            result.append(text[pos])
            pos += 1
    assert depth == 0
    return ''.join(result)


def enumerate_declarations(text):
    code = strip_comments(text)
    assert not re.search(r'\b(?:sorry|admit|sorryAx|native_decide|ofReduceBool|axiom|unsafe|implemented_by|macro|elab|syntax|run_cmd|run_meta)\b', code)
    namespace, entries = None, []
    for lineno, line in enumerate(code.splitlines(), 1):
        match = re.fullmatch(r'\s*namespace\s+([\w.]+)\s*', line)
        if match:
            assert namespace is None
            namespace = match[1]
            continue
        if re.fullmatch(r'\s*end\s+[\w.]+\s*', line):
            namespace = None
            continue
        match = re.match(r'^\s*(?:@\[[^\]]*\]\s*)?(abbrev|def|structure|theorem)\s+([\w\']+)', line)
        if match:
            assert namespace is not None
            entries.append({'kind': match[1], 'name': namespace + '.' + match[2], 'line': lineno})
    assert len(entries) == len(re.findall(r'\b(?:abbrev|def|structure|theorem)\s+[\w\']+', code))
    assert namespace is None
    return code, entries


def main():
    BUILD.mkdir(exist_ok=False)
    logs, snapshots = HERE / 'logs', HERE / 'source_snapshots'
    logs.mkdir(exist_ok=False)
    snapshots.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    report = {'status': 'RUNNING', 'reviewer': REVIEWER, 'started_utc': started,
              'independent_from_author_checker': True, 'project_object_reuse': False,
              'development_cache_reuse': False, 'build_dir_initially_absent': True,
              'build_dir': str(BUILD), 'sources': {}, 'commands': [],
              'driver_sha256': digest(Path(__file__)), 'runtime': {}}
    runtime = WORKSPACE / 'runtime-audit'
    for relative in ['lean', 'app-path-compat.c', 'app-path-compat.so',
                     'lean-4.19.0-linux/bin/lean', 'lean-4.19.0-linux/lib/lean/libleanshared.so',
                     'lean-4.19.0-linux/lib/lean/libleanshared_1.so', 'lean-4.19.0-linux/lib/lean/libInit_shared.so']:
        report['runtime'][relative] = digest(runtime / relative)
    assert report['runtime']['lean-4.19.0-linux/bin/lean'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
    env = os.environ.copy()
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT', 'LD_PRELOAD', 'LD_LIBRARY_PATH']:
        env.pop(key, None)
    env['LEAN_PATH'] = str(BUILD)
    report['environment'] = {'LEAN_PATH': str(BUILD), 'other_lean_overrides': 'unset',
                             'adapter': 'launcher uses only the hash-recorded current-process readlink adapter'}

    def save():
        (HERE / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')

    def run(name, args):
        argv = [str(LEAN), *args]
        start = time.monotonic()
        print('START', name, flush=True)
        log = logs / (name + '.log')
        with log.open('w') as handle:
            proc = subprocess.run(argv, cwd=BUILD, env=env, stdout=handle, stderr=subprocess.STDOUT, text=True)
        report['commands'].append({'name': name, 'argv': argv, 'cwd': str(BUILD),
                                   'returncode': proc.returncode, 'seconds': round(time.monotonic() - start, 3),
                                   'log': str(log.relative_to(HERE)), 'log_sha256': digest(log)})
        save()
        print('END', name, 'exit', proc.returncode, flush=True)
        assert proc.returncode == 0, name
        return log.read_text()

    try:
        version = run('version', ['--version']).strip()
        assert 'version 4.19.0' in version and 'commit 6caaee842e94' in version
        report['version'] = version
        names, available = [], {'Std'}
        for relative in SOURCES:
            src = REPO / relative
            data = src.read_bytes()
            code, entries = enumerate_declarations(data.decode())
            deps = re.findall(r'^import\s+(\w+)\s*$', code, re.M)
            assert set(deps) <= available, (src.name, deps)
            sha = hashlib.sha256(data).hexdigest()
            if src.stem == 'RadixExterior':
                assert sha == FROZEN_RADIX
                assert sum(d['kind'] == 'theorem' for d in entries) == 15
            report['sources'][src.stem] = {'path': relative, 'sha256': sha, 'imports': deps,
                                           'declarations': entries, 'forbidden_token_scan': 'PASS'}
            (BUILD / src.name).write_bytes(data)
            (snapshots / src.name).write_bytes(data)
            names.extend(d['name'] for d in entries)
            run(src.stem, ['-j1', '-DElab.async=false', '-o', src.stem + '.olean', src.name])
            assert digest(src) == sha == digest(BUILD / src.name)
            report['sources'][src.stem]['olean_sha256'] = digest(BUILD / (src.stem + '.olean'))
            available.add(src.stem)
        assert len(names) == len(set(names))
        audit = 'import RadixExterior\n' + ''.join('#print axioms ' + name + '\n' for name in names)
        (BUILD / 'ReviewerAudit.lean').write_text(audit)
        (HERE / 'ReviewerAudit.lean').write_text(audit)
        output = run('ReviewerAudit', ['-j1', '-DElab.async=false', 'ReviewerAudit.lean'])
        rows = re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]", output, re.M)
        rows = [(name, sorted(a.strip() for a in value.split(',') if a.strip())) for name, value in rows]
        rows += [(name, []) for name in re.findall(r"^'([^\n]+)' does not depend on any axioms", output, re.M)]
        counts = Counter(name for name, _ in rows)
        assert set(counts) == set(names) and set(counts.values()) == {1}
        assert all(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, axioms in rows)
        for name, record in report['sources'].items():
            assert digest(REPO / record['path']) == record['sha256'] == digest(BUILD / (name + '.lean'))
            assert digest(BUILD / (name + '.olean')) == record['olean_sha256']
        report.update(status='PASS', completed_utc=datetime.now(timezone.utc).isoformat(),
                      audited_declarations=len(names), axiom_audit=dict(sorted(rows)),
                      source_hashes_unchanged=True,
                      signed_reviewer_identity=REVIEWER)
        save()
        print('PASS', len(names), 'explicit public declarations', flush=True)
    except Exception as exc:
        report.update(status='FAILED', error=repr(exc))
        save()
        raise


if __name__ == '__main__':
    main()
