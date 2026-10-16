#!/usr/bin/env python3
"""Outer invocation receipt for the unmodified published project verifier."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import time

WORKTREE = Path('/workspace/scratch/94808c4aecb2/agent107-canonical-be8e612c')
EXPECTED_HEAD = 'be8e612ca0694d5d9d8473c784ab1956f93405b6'
LEAN = '/workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean'
OUTPUT = Path('/workspace/scratch/94808c4aecb2/p196-agent107/proofs/contributions/agent-107/folded-transducer-20261016/canonical-verification-be8e612c')
RECEIPTS = Path('/workspace/scratch/94808c4aecb2/agent107-runtime/canonical-be8e612c-invocation')
VERIFIER = Path('proofs/verify_project__214bf7673efe116b.py')
REGISTRY = Path('proofs/Agent107Transducer.registry.json')
ARGV = ['python3', str(VERIFIER), '--lean', LEAN, '--registry', str(REGISTRY), '--project', 'agent107-folded-transducer', '--output', str(OUTPUT)]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=WORKTREE)

def main():
    RECEIPTS.mkdir(parents=True, exist_ok=False)
    (RECEIPTS / 'setup-diagnostic.json').write_text(json.dumps({
        'recorded_at_utc': utc(),
        'stage': 'read-only setup before any canonical verifier invocation',
        'prior_observation': {'head': EXPECTED_HEAD, 'git_status_porcelain_line_count': 13991, 'first_status_lines': ['D  .github/workflows/agent1-consolidation-core.yml', 'D  .github/workflows/agent1-consolidation-delta.yml', 'D  .github/workflows/agent1-consolidation-index.yml', 'D  .github/workflows/agent1-consolidation-snapshot.yml', 'D  .github/workflows/agent1-english-inventory.yml', 'D  .github/workflows/agent1-english-publish.yml'], 'verifier_exists': False, 'registry_exists': False},
        'effect': 'Verifier was not started; no Lean or mathematical proof failure occurred at this setup stage.',
        'root_reported_remediation': 'Root executed git read-tree -mu HEAD to materialize the detached sparse worktree.',
        'note': 'Prior observations are recorded after root remediation; the exact prior observation timestamp was not separately retained. This wrapper independently checks the current clean worktree before invocation.'
    }, ensure_ascii=False, indent=2) + '\n')
    head = git('rev-parse', 'HEAD').decode().strip()
    status = git('status', '--porcelain=v1')
    (RECEIPTS / 'git-status-before.txt').write_bytes(status)
    assert head == EXPECTED_HEAD, (head, EXPECTED_HEAD)
    assert not status, 'Worktree must be clean before the canonical run'
    assert not OUTPUT.exists(), 'Canonical output path must be new'
    source_hashes = {}
    for path in [VERIFIER, REGISTRY]:
        data = (WORKTREE / path).read_bytes()
        assert data == git('show', f'HEAD:{path}'), f'Published bytes differ: {path}'
        source_hashes[str(path)] = sha(data)
        (RECEIPTS / path.name).write_bytes(data)
    receipt = {
        'caller': 'Agent #107',
        'role': 'lean_runtime independent verifier invocation',
        'original_report_agent_field_policy': 'Preserve original verifier field Agent #1 without modification',
        'head_before': head,
        'git_status_before': status.decode(),
        'cwd': str(WORKTREE),
        'argv': ARGV,
        'source_sha256': source_hashes,
        'started_at_utc': utc(),
        'status': 'RUNNING',
        'trust_option': 'The original unmodified canonical verifier does not pass --trust=0; earlier independent checks explicitly passed --trust=0.',
    }
    def save():
        (RECEIPTS / 'invocation.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    save()
    start = time.monotonic()
    with (RECEIPTS / 'verifier.stdout.log').open('wb') as out, (RECEIPTS / 'verifier.stderr.log').open('wb') as err:
        proc = subprocess.Popen(ARGV, cwd=WORKTREE, stdout=out, stderr=err)
        receipt['verifier_pid'] = proc.pid
        save()
        print(json.dumps({'event': 'CANONICAL_VERIFIER_STARTED', 'pid': proc.pid, 'cwd': str(WORKTREE), 'argv': ARGV, 'receipt': str(RECEIPTS / 'invocation.json'), 'started_at_utc': receipt['started_at_utc']}, ensure_ascii=False), flush=True)
        rc = proc.wait()
    receipt.update({'exit_code': rc, 'finished_at_utc': utc(), 'elapsed_seconds': round(time.monotonic()-start, 6), 'status': 'COMPLETED'})
    after = git('status', '--porcelain=v1')
    (RECEIPTS / 'git-status-after.txt').write_bytes(after)
    receipt['head_after'] = git('rev-parse', 'HEAD').decode().strip()
    receipt['git_status_after'] = after.decode()
    receipt['worktree_unchanged'] = not after and receipt['head_after'] == EXPECTED_HEAD
    save()
    if OUTPUT.exists():
        original_files = OUTPUT / 'FILES.json'
        receipt['canonical_FILES_sha256'] = sha(original_files.read_bytes()) if original_files.is_file() else None
        save()
        target = OUTPUT / 'invocation'
        shutil.copytree(RECEIPTS, target)
        shutil.copyfile(__file__, target / Path(__file__).name)
        (target / 'README.md').write_text('# 原 canonical verifier 的外围调用收据\n\n调用者为 Agent #107；原脚本报告中的 Agent #1 是上游作者字段，未作修改。\n\n本次从发布提交 be8e612ca0694d5d9d8473c784ab1956f93405b6 对应的干净工作树，原样运行原 verifier。其 Lean 命令不显式传入 `--trust=0`；此前作者与独立检查已另行显式使用 `--trust=0`。\n\n`FILES.json` 是原 verifier 自行产生的原始清单，保持原字节；本 invocation 子目录在原脚本退出后复制进入，另由 `INVOCATION_FILES.json` 记录全目录（排除 `.olean` 和清单自身）。原 verification.json、源码与日志均未改动。\n\n实际 argv、时间、exit、HEAD、工作树状态及原 verifier/registry SHA256 见 invocation.json。\n')
        files = {str(p.relative_to(OUTPUT)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in sorted(OUTPUT.rglob('*')) if p.is_file() and p.suffix != '.olean' and p.name != 'INVOCATION_FILES.json'}
        (OUTPUT / 'INVOCATION_FILES.json').write_text(json.dumps(files, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)
    return rc

if __name__ == '__main__':
    sys.exit(main())
