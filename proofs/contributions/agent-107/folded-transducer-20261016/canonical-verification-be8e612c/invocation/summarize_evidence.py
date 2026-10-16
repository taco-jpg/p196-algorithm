#!/usr/bin/env python3
"""Read-only checks of original canonical results; write separate invocation summaries."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent.parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

report = json.loads((OUT / 'verification.json').read_text())
project = report['projects']['agent107-folded-transducer']
receipt = json.loads((OUT / 'invocation/invocation.json').read_text())
logpath = OUT / 'agent107-folded-transducer/logs/ProjectAudit.log'
log = logpath.read_text()
rows = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]', log, re.M)
normalized = [(mod, name, sorted(a.strip() for a in axs.split(',') if a.strip())) for mod, name, axs in rows]
assert report['status'] == project['status'] == 'PASS'
assert receipt['exit_code'] == 0 and receipt['worktree_unchanged']
assert len(rows) == len({name for _, name, _ in rows}) == project['theorem_count']
assert all(a in {'propext', 'Classical.choice', 'Quot.sound'} for _, _, axs in normalized for a in axs)
assert all(command['exit_code'] == 0 for command in project['commands'])
assert all('--trust=0' not in command['argv'] for command in project['commands'])
original_files = json.loads((OUT / 'FILES.json').read_text())
for relative, record in original_files.items():
    path = OUT / relative
    assert sha(path) == record['sha256'] and path.stat().st_size == record['bytes'], relative
assert sha(OUT / 'FILES.json') == receipt['canonical_FILES_sha256']
origins = dict(sorted(Counter(mod for mod, _, _ in rows).items()))
unsafe = project['unsafe_implementation_axioms']
sets = Counter(tuple(axs) for _, _, axs in normalized)
summary = {
    'caller': 'Agent #107',
    'original_verifier_report_agent': report['agent'],
    'status': report['status'],
    'source_commit': report['source_commit'],
    'source_tree_clean': report['source_tree_clean'],
    'worktree_unchanged_after': receipt['worktree_unchanged'],
    'repository_wide_pass': report['repository_wide_pass'],
    'lean_command_count': len(project['commands']),
    'all_lean_exit_codes': [command['exit_code'] for command in project['commands']],
    'source_module_count': len(project['sources']),
    'registered_endpoint_count': len(project['endpoints']),
    'full_origin_theorem_count': len(rows),
    'foundation_theorem_count': origins['Lychrel196Research'],
    'agent107_theorem_count': sum(n for m, n in origins.items() if m != 'Lychrel196Research'),
    'module_origin_counts': origins,
    'normalized_axiom_union': sorted({a for _, _, axs in normalized for a in axs}),
    'axiom_set_counts': [{'axioms': list(axs), 'theorems': n} for axs, n in sorted(sets.items())],
    'unsafe_implementation_axiom_count': len(unsafe),
    'unsafe_implementation_axiom_origin_counts': dict(sorted(Counter(mod for mod, name in unsafe).items())),
    'unsafe_implementation_axioms': unsafe,
    'unsafe_note': 'The unmodified verifier reports axiomInfo with isUnsafe as implementation placeholders; all theorem dependency sets contain only the three allowed logical axioms.',
    'canonical_explicit_trust_zero': False,
    'trust_note': receipt['trust_option'],
    'original_FILES_entries': len(original_files),
    'original_FILES_all_hashes_verified': True,
    'original_FILES_preserved_sha256': sha(OUT / 'FILES.json'),
    'verification_json_sha256': sha(OUT / 'verification.json'),
    'audit_log_sha256': sha(logpath),
    'started_at_utc': receipt['started_at_utc'],
    'finished_at_utc': receipt['finished_at_utc'],
    'elapsed_seconds': receipt['elapsed_seconds'],
}
(OUT / 'invocation/summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
lines = [
    '# Agent #107：原 canonical verifier 独立运行结果',
    '',
    '**结果：PASS，exit 0。** 从已发布提交 `be8e612ca0694d5d9d8473c784ab1956f93405b6` 的干净隔离工作树实际执行原未改 verifier；12 个注册模块全部从源码重编，随后总模块来源公理审计成功。13 个 Lean 命令全部 exit 0。',
    '',
    f"UTC 开始 `{receipt['started_at_utc']}`，结束 `{receipt['finished_at_utc']}`；实测耗时 `{receipt['elapsed_seconds']}` 秒。运行前后 HEAD 相同、工作树状态为空。原 verifier SHA256 为 `{receipt['source_sha256']['proofs/verify_project__214bf7673efe116b.py']}`；注册表 SHA256 为 `{receipt['source_sha256']['proofs/Agent107Transducer.registry.json']}`。实际命令见同目录 `invocation.json` 的 argv。",
    '',
    '调用者是 Agent #107；原 `verification.json` 的 `agent: Agent #1` 是原脚本作者字段，完整保留。此为显式选择项目的 scoped gate，原报告 `repository_wide_pass` 为 false，不能外推为整个仓库全部项目通过。',
    '',
    '本次原脚本 Lean 命令未显式设置 `--trust=0`，没有修改脚本以改变该行为。此前作者及独立检查已分别显式使用 `--trust=0`；两类证据分开保留。本记录不把本次原脚本命令称为显式 trust-zero 检查。',
    '',
    '## 完整模块来源审计',
    '',
    f'总计 **{len(rows)} 条定理**，其中基础模块 **{origins["Lychrel196Research"]} 条**、Agent107 模块 **{summary["agent107_theorem_count"]} 条**。审计含各模块辅助定理，按实际 `env.getModuleIdxFor?` 来源筛选，不只检查列出的公共端点。',
    '',
    '| 模块 | 定理数 |',
    '|---|---:|',
]
lines += [f'| `{mod}` | {n} |' for mod, n in origins.items()]
lines += ['', '所有定理依赖的公理并集恰为 `Classical.choice`、`Quot.sound`、`propext`；无自定义或其他禁止公理依赖。按照完整跨行日志归一化后：', '', '| 公理集合 | 定理数 |', '|---|---:|']
lines += [f'| {", ".join(f"`{a}`" for a in axs) if axs else "无"} | {n} |' for axs, n in sorted(sets.items())]
lines += [
    '',
    f'原脚本同时报告 **{len(unsafe)} 个 unsafe implementation 占位**：基础模块 13 个、Defs 2 个、TablesData 3 个。这是原脚本对 `axiomInfo.isUnsafe` 的分类；所有已审计定理的公理依赖仍仅包含上述三个允许项。没有将这些实现占位隐去或计作新的数学假设。精确名称如下：',
    '',
]
lines += [f'- `{mod}`：`{name}`' for mod, name in unsafe]
lines += [
    '',
    '## 证据完整性',
    '',
    f'原 `FILES.json` 的 {len(original_files)} 项逐文件 SHA256 和字节数均已复核匹配；原清单自身 SHA256 为 `{sha(OUT / "FILES.json")}`，与运行结束时记录一致。原 `verification.json`、全部日志、构建源码快照、自动生成的 `ProjectAudit.lean` 均未修改。',
    '',
    '本 invocation 子目录在原 verifier 退出后另行加入，保留调用者收据、原 verifier/registry 字节快照、外围日志和本汇总；`INVOCATION_FILES.json` 覆盖补充后的全部非 `.olean` 文件。原 `FILES.json` 原字节不变。',
    '',
    '运行前曾发现该隔离工作树尚未物化（13,991 条删除状态、verifier/registry 缺失）。当时 verifier 未启动，也没有 Lean 数学失败。主代理随后完成 checkout 物化；本次运行入口独立确认干净状态和源码与 HEAD 的字节一致性。诊断单独记录于 `setup-diagnostic.json`，未伪装成编译失败或原始即时快照。',
    '',
]
(OUT / 'invocation/SUMMARY.zh-CN.md').write_text('\n'.join(lines))
files = {str(p.relative_to(OUT)): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file() and p.suffix != '.olean' and p.name != 'INVOCATION_FILES.json'}
(OUT / 'INVOCATION_FILES.json').write_text(json.dumps(files, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'theorem_count': len(rows), 'unsafe_implementation_axioms': len(unsafe), 'original_FILES_entries_verified': len(original_files), 'supplemental_inventory_entries': len(files), 'summary_json_sha256': sha(OUT / 'invocation/summary.json'), 'supplemental_inventory_sha256': sha(OUT / 'INVOCATION_FILES.json')}, ensure_ascii=False))
