#!/usr/bin/env python3
"""Agent123 exact-byte publication transport; this does not rerun Lean."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import tempfile
import zlib

BRANCH = 'research/agent-123/s20261015T164520Z-publication'
SOURCE = 'eec3d5f3646cab50abad6e610ea19626cd249070'
BASE = '2c2551165c13d23b11d44122fc7a504d51053e59'
CLAIM = 'a49e2409923da5ba4948b986168cf6cc8700b157'
PREFIX = 'proofs/contributions/agent-123/template-certificate-replication'
PAYLOAD_HASH = 'dfa754a775b2edab1dfb77b0a236e88b2abeabe39dbda1073c1c7259c3182a1e'
RAW = {
    'horizon-controls.json.gz': 'fe739b25c2d937aed384e2ed46d5f23eed9075549ff2ce4ea268ee71de39f064',
    'integer-controls.csv.gz': 'dcc394cefce5d3b3c09b0f820fac76300bfd7dad825460a5cd92a1c48add096a',
}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def put_exact(path: Path, data: bytes) -> None:
    check(not path.is_symlink(), f'Symlink refused: {path}')
    if path.exists():
        check(path.read_bytes() == data, f'Existing bytes differ: {path}')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(['git', '-C', str(root), *args])

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--local-test', action='store_true')
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if not args.local_test:
        check(os.environ.get('GITHUB_REF_NAME') == BRANCH, 'Wrong publication branch')
    payload = b''.join((root / '.github/agent123-publication' / f'metadata.part{i:02d}').read_bytes() for i in range(5))
    check(sha(payload) == PAYLOAD_HASH, 'Payload SHA-256 mismatch')
    texts = json.loads(lzma.decompress(payload))
    check(isinstance(texts, dict) and len(texts) == 64, 'Expected exactly 64 original text files')
    dest = root / PREFIX
    for name, content in texts.items():
        path = PurePosixPath(name)
        check(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe path')
        check(isinstance(content, str), 'Expected UTF-8 string')
        put_exact(dest / name, content.encode('utf-8'))
    pub = dest / 'publication'
    pub.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='agent123-raw-replay-') as temporary:
        output = Path(temporary) / 'new-controls'
        command = [sys.executable, '-B', str(dest / 'controls.py'), str(args.source_root.resolve()), str(output)]
        run = subprocess.run(command, capture_output=True)
        (pub / 'raw-replay.log').write_bytes(run.stdout + b'\nSTDERR:\n' + run.stderr)
        check(run.returncode == 0, f'Controls exited {run.returncode}')
        raw_report = json.loads((output / 'controls-result.json').read_text())
        check(raw_report['status'] == 'PASS', 'Control report not PASS')
        for name, expected in RAW.items():
            data = (output / name).read_bytes()
            check(sha(data) == expected, f'Original compressed bytes not recovered: {name}')
            put_exact(dest / 'controls' / name, data)
        (pub / 'raw-replay-result.json').write_bytes((output / 'controls-result.json').read_bytes())
    original_names = sorted([*texts.keys(), *('controls/' + name for name in RAW)])
    check(len(original_names) == 66 and len(set(original_names)) == 66, 'Original file inventory mismatch')
    for row in texts['SHA256SUMS'].splitlines():
        expected, name = row.split('  ', 1)
        check(name in original_names, 'Unknown original manifest path')
        check(sha((dest / name).read_bytes()) == expected, f'Manifest mismatch: {name}')
    check(len(texts['SHA256SUMS'].splitlines()) == 65, 'Original manifest row count mismatch')
    originals = []
    for name in original_names:
        data = (dest / name).read_bytes()
        originals.append({'path': name, 'bytes': len(data), 'sha256': sha(data), 'git_blob': blob(data)})
    pins = json.loads(texts['module-pins.json'])
    dependencies = []
    for name, pin in pins.items():
        entry = {'module': name, 'path': pin['path'], 'expected_sha256': pin['sha256']}
        if not args.local_test:
            historical = git(root, 'show', f"{SOURCE}:{pin['path']}")
            check(sha(historical) == pin['sha256'] and blob(historical) == pin['git_blob'], f'Historical dependency mismatch: {name}')
            entry['historical_pin_matches'] = True
            current = (root / pin['path']).read_bytes()
            entry['publication_base_pin_matches'] = sha(current) == pin['sha256'] and blob(current) == pin['git_blob']
        else:
            entry['historical_pin_matches'] = 'NOT_RUN_LOCAL_TRANSPORT_TEST'
        dependencies.append(entry)
    delivery = (root / '.github/agent123-publication/DELIVERY.json').read_bytes()
    check(sha(delivery) == '236234aeab437c191f4a177a2b4e91508e17263c1acf308be4b0a47da45410a3', 'Original delivery metadata mismatch')
    put_exact(pub / 'ORIGINAL_DELIVERY.json', delivery)
    report = {
        'agent': 123, 'status': 'PASS', 'scope': 'Exact-byte publication and finite control replay; not a new Lean build',
        'local_transport_test': args.local_test,
        'time_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'branch': BRANCH, 'publication_base': BASE, 'claim_commit': CLAIM,
        'historical_source_commit': SOURCE,
        'historical_local_commit': '504860c408d071f30e0ff25d92cff43c89335324',
        'transport_commit': os.environ.get('GITHUB_SHA'),
        'workflow_run': os.environ.get('GITHUB_RUN_ID'),
        'original_zip_sha256': '9161d7be1540035c74f6a78e4d9b224edf86e6e8209d7774cba1eab120088518',
        'payload_sha256': PAYLOAD_HASH,
        'original_file_count': len(originals), 'original_bytes': sum(x['bytes'] for x in originals),
        'original_files': originals, 'dependencies': dependencies,
        'python': platform.python_version(), 'zlib': zlib.ZLIB_RUNTIME_VERSION,
        'raw_replay_exit_status': run.returncode,
        'lean_rebuilt_in_publication_session': False, 'integrated': False,
        'exclusions': ['Runtime installations and compiled artifacts were never part of the source bundle.',
                       'Temporary metadata payload chunks duplicate the restored original text and are transport infrastructure.',
                       'Original ZIP and addition patch are delivery wrappers; every original package file and DELIVERY metadata is preserved.'],
    }
    (pub / 'byte-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (dest / 'PUBLICATION.md').write_text('''# Agent #123：复现证据发布补记

本文件是当前发布记录；`README.md`、`LOCAL_STATUS.json`、`provenance.json` 和
`publication/ORIGINAL_DELIVERY.json` 保留此前离线会话的原始状态，未改写其字节。
它们当时的“未发布”不再描述此发布提交；此前研究也没有被追溯冒称为远端认领。

## 当前交付范围

66 个原始贡献文件完整恢复，逐文件 SHA-256 与原始包一致。64 个文本文件经无损压缩
传输后恢复；两个原始压缩数据文件由原始 `controls.py` 在固定来源、随机种子和
Python 3.13.5 环境重放，再严格核对原始压缩字节哈希，只有匹配才允许提交。
这不是以重放说明替代原始数据；两个完整 `.gz` 文件本身均在本提交中。
所有历史失败、修正、源码和公理日志均保留。机器可读核对表见
`publication/byte-verification.json`，本次重放记录与历史记录分开保存。

已发布协调认领：`a49e2409923da5ba4948b986168cf6cc8700b157`。
贡献分支：`research/agent-123/s20261015T164520Z-publication`。
本发布基于 `2c2551165c13d23b11d44122fc7a504d51053e59`；历史审计的源码版本是
`eec3d5f3646cab50abad6e610ea19626cd249070`。不修改其它 Agent 的贡献、主分支或共享索引。
另一个 `agent123-seam-mask-realizability` 任务与本包不相同，不受本发布影响。

## 证据等级

此前独立复现的两次源码构建、十个模块及 1,450 个定理常量的传递公理审计按原样保留；
本次发布只重新执行有限整数控制和字节验证，不宣称新做了一遍 Lean 构建或独立审稿。
原有数学结果归作者所有；本包是复现及范围回归检查。自身回归证明尚未获得另一位
审稿人的独立复核。本贡献尚未集成，需通过 PR 交给集成负责人。

条件证书结论仍保留实际接受证书和初态可实现性假设；本包没有证书实例、无限避回文
种子或 196 的全时证明。有限安全结论的时间从 1 开始，不能偷偷包含时间 0。

## 复现

原始 `README.md` 中的 Lean 和有限控制命令保持有效。可以在本目录执行
`sha256sum -c SHA256SUMS` 检查 65 个有清单记录的原始文件；清单自身的哈希及全部
66 个原始文件的 Git blob 标识列在 `publication/byte-verification.json`。
不把原包中历史绝对路径当作当前文件系统路径。运行复现脚本时使用新的输出目录。
''', encoding='utf-8')
    new_files = [dest / 'PUBLICATION.md', *sorted(f for f in pub.rglob('*') if f.is_file())]
    manifest = [{'path': str(f.relative_to(dest)), 'bytes': f.stat().st_size, 'sha256': sha(f.read_bytes())} for f in new_files]
    (pub / 'PUBLICATION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'original_files': 66, 'original_bytes': report['original_bytes'],
                      'raw_hashes_match': True, 'historical_dependency_pins_checked': not args.local_test}))

if __name__ == '__main__':
    main()
