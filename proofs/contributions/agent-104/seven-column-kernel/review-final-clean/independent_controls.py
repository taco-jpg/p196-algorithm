#!/usr/bin/env python3
"""Independent controls around the committed Agent 104 clean-build runner.

This script does not modify any Lean, generator, or check.py source and never
imports a prebuilt local theorem object. The archive is the previously recorded
official Lean release artifact, not a newly authenticated download.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile

import zstandard

sys.dont_write_bytecode = True

ROOT = Path('/workspace/scratch/7649db1e242c')
REPO = ROOT / 'p196-agent104'
PACKAGE = REPO / 'proofs/contributions/agent-104/seven-column-kernel'
WORK = ROOT / 'build104-independent-final'
TOOLCHAIN = ROOT / 'toolchain'
PREFIX = TOOLCHAIN / 'lean-4.19.0-linux'
ARCHIVE = TOOLCHAIN / 'lean-4.19.0-linux.tar.zst'
ARCHIVE_PIN = '6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe'
COMPILER_PIN = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write(name: str, obj: object) -> None:
    (WORK / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=REPO)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def preflight(commit: str) -> dict:
    assert git('rev-parse', 'HEAD').decode().strip() == commit
    runner = PACKAGE / 'check.py'
    assert git('show', commit + ':' + str(runner.relative_to(REPO))) == runner.read_bytes()
    spec = importlib.util.spec_from_file_location('committed_runner', runner)
    checked = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(checked)
    pins = {}
    standard = set()
    source_theorems = {}
    suspicious = []

    def visit(module: str) -> None:
        if module in pins or module in standard:
            return
        path = checked.CORE if module == 'LychrelDigitSums' else PACKAGE / (module.replace('.', '/') + '.lean')
        if not path.exists():
            path = PACKAGE / 'certificate' / (module + '.lean')
        if not path.exists():
            standard.add(module)
            return
        blob = path.read_bytes()
        assert git('show', commit + ':' + str(path.relative_to(REPO))) == blob, module
        pins[module] = digest(path)
        code = checked.code_only(blob.decode())
        source_theorems[module] = len(re.findall(r'(?m)^\s*(?:private\s+|protected\s+)?theorem\s+(\S+)', code))
        for line_num, line in enumerate(code.splitlines(), 1):
            if re.search(r'\b(?:unsafe|run_cmd|run_meta|elab|macro|syntax|initialize|opaque|axiom|sorry|admit|native_decide|ofReduceBool|skipKernelTC|implemented_by|extern)\b', line):
                suspicious.append([module, line_num, line.strip()])
        for imported in checked.imports(blob.decode()):
            visit(imported)

    for module in ('Conclusion739', 'TerminalObstruction'):
        visit(module)
    assert standard == {'Std'}, standard
    assert not suspicious, suspicious
    assert not os.environ.get('LD_PRELOAD', '')
    assert not os.environ.get('LD_LIBRARY_PATH', '')
    assert digest(ARCHIVE) == ARCHIVE_PIN
    assert digest(PREFIX / 'bin/lean') == COMPILER_PIN
    archive_pins = {}
    installed_pins = {}
    with ARCHIVE.open('rb') as raw:
        with zstandard.ZstdDecompressor().stream_reader(raw) as stream:
            with tarfile.open(fileobj=stream, mode='r|') as tf:
                for entry in tf:
                    name = entry.name.removeprefix('./')
                    parts = name.split('/', 1)
                    if len(parts) != 2 or parts[0] != PREFIX.name or not entry.isfile():
                        continue
                    relative = parts[1]
                    selected = relative == 'bin/lean' or (relative.startswith('lib/lean/') and (relative.endswith('.olean') or relative.endswith('.so')))
                    if not selected:
                        continue
                    source = tf.extractfile(entry)
                    assert source is not None
                    h = hashlib.sha256()
                    for chunk in iter(lambda: source.read(1024 * 1024), b''):
                        h.update(chunk)
                    archive_pins[relative] = h.hexdigest()
                    installed_pins[relative] = digest(PREFIX / relative)
                    assert installed_pins[relative] == archive_pins[relative], relative
    assert len(archive_pins) > 1000
    write('official-archive-member-pins.json', archive_pins)
    write('independent-source-pins.json', pins)
    write('source-theorem-counts.json', source_theorems)
    support_files = [runner, TOOLCHAIN / 'lean', TOOLCHAIN / 'proc-self-compat.c', TOOLCHAIN / 'proc-self-compat.so', PREFIX / 'src/lean/Lean/Util/CollectAxioms.lean', TOOLCHAIN / 'lean-4.19.0-release.json', PACKAGE / 'environment/verification.json']
    result = {
        'status': 'PASS', 'checked_at_utc': now(), 'source_commit': commit,
        'local_module_count': len(pins), 'source_named_theorem_count': sum(source_theorems.values()),
        'source_trust_escape_scan': suspicious, 'nonlocal_direct_imports': sorted(standard),
        'official_archive': str(ARCHIVE), 'official_archive_sha256': ARCHIVE_PIN,
        'archive_origin': 'Previously recorded official leanprover/lean4 v4.19.0 Linux release; no independent network download claimed.',
        'archive_member_count_verified_against_installation': len(archive_pins),
        'archive_pins_file': 'official-archive-member-pins.json',
        'support_file_pins': {str(p): digest(p) for p in support_files},
        'inherited_LD_PRELOAD': os.environ.get('LD_PRELOAD', ''),
        'inherited_LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', ''),
        'source_snapshot_rebuild_explanation': 'Every local source is compared byte-for-byte to this Git commit before check.py copies and hashes the same source closure into a new directory. No pre-existing local .olean is supplied.',
    }
    write('independent-preflight.json', result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('commit')
    args = parser.parse_args()
    invocation = {'source_commit': args.commit, 'started_at_utc': now(), 'status': 'PREFLIGHT'}
    write('invocation.json', invocation)
    try:
        preflight(args.commit)
        command = [sys.executable, str(PACKAGE / 'check.py'), str(TOOLCHAIN / 'lean'), '--evidence', str(WORK / 'rebuild'), '--module', 'Conclusion739', '--module', 'TerminalObstruction', '--jobs', '2', '--require-committed']
        invocation.update(status='RUNNING', command=command, cwd=str(REPO), runner_sha256=digest(PACKAGE / 'check.py'))
        write('invocation.json', invocation)
        print('Independent preflight PASS; starting fresh 383-module build.', flush=True)
        with (WORK / 'runner-output.log').open('w') as out:
            completed = subprocess.run(command, cwd=REPO, stdout=out, stderr=subprocess.STDOUT)
        invocation.update(status='CHECKER_EXITED', checker_exit_code=completed.returncode, checker_finished_at_utc=now(), checker_output_sha256=digest(WORK / 'runner-output.log'))
        write('invocation.json', invocation)
        print(f'Independent checker exit: {completed.returncode}', flush=True)
        return completed.returncode
    except Exception as exc:
        invocation.update(status='FAIL', failure=repr(exc), finished_at_utc=now())
        write('invocation.json', invocation)
        raise


if __name__ == '__main__':
    raise SystemExit(main())
