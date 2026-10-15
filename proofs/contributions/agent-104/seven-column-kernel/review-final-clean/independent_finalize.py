#!/usr/bin/env python3
"""Recheck all independent-run records and preserve complete textual evidence."""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path('/workspace/scratch/7649db1e242c')
WORK = ROOT / 'build104-independent-final'
BUILD = WORK / 'rebuild'
REPO = ROOT / 'p196-agent104'
PACKAGE = REPO / 'proofs/contributions/agent-104/seven-column-kernel'
DEST = PACKAGE / 'review-final-clean'
PREFIX = ROOT / 'toolchain/lean-4.19.0-linux'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
EXPECTED = [
    'SevenColumnKernel.Finite739.initialCovered',
    'SevenColumnKernel.Finite739.ancestry_bound39',
    'SevenColumnKernel.Finite739.no_196_739_palindrome',
    'SevenColumn.Certificate739.allRowsFast',
    'SevenColumn.Certificate739.allRows',
    'SevenColumnKernel.TerminalObstruction.next_prefix_196_impossible',
    'SevenColumnKernel.TerminalObstruction.positive_time_no_196_pair_prefix',
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def main() -> None:
    invocation = read(WORK / 'invocation.json')
    preflight = read(WORK / 'independent-preflight.json')
    report = read(BUILD / 'verification.json')
    original_pins = read(WORK / 'independent-source-pins.json')
    archive_pins = read(WORK / 'official-archive-member-pins.json')
    assert invocation['checker_exit_code'] == 0
    assert report['status'] == 'PASS'
    assert report['source_commit'] == invocation['source_commit'] == preflight['source_commit']
    assert report['require_committed_sources']
    assert report['fresh_source_rebuild'] and report['snapshot_complete_before_build']
    assert report['parallel_build_workers'] == 2 and report['async_elaboration'] is False
    assert report['originals_unchanged_at_completion']
    assert report['selected_top_level_modules'] == ['Conclusion739', 'TerminalObstruction']
    assert set(report['sources']) == set(original_pins)
    assert len(report['sources']) == 383
    for path, expected in preflight['support_file_pins'].items():
        assert sha(Path(path)) == expected, path
    for path, expected in report['compiler']['fingerprints'].items():
        assert sha(Path(path)) == expected, path
    for name, rec in report['sources'].items():
        assert rec['sha256'] == original_pins[name], name
        assert rec['matches_source_commit'], name
        assert sha(BUILD / rec['snapshot']) == rec['sha256'], name
        assert sha(REPO / rec['original_path']) == rec['sha256'], name
        assert sha(BUILD / 'snapshot' / (name.replace('.', '/') + '.olean')) == rec['object_sha256'], name
    for rec in report['builds']:
        assert rec['exit_code'] == 0, rec['label']
        assert sha(BUILD / rec['log']) == rec['log_sha256'], rec['label']
    source_builds = [r['label'] for r in report['builds'] if r['label'] in report['sources']]
    assert len(source_builds) == len(set(source_builds)) == 383
    assert set(source_builds) == set(report['sources'])
    local_objects = 0
    official_objects = 0
    for module, rec in report['imported_object_fingerprints'].items():
        path = Path(rec['path'])
        assert sha(path) == rec['sha256'], module
        if path.is_relative_to(BUILD / 'snapshot'):
            assert module in report['sources'], module
            assert rec['sha256'] == report['sources'][module]['object_sha256'], module
            local_objects += 1
        else:
            rel = str(path.relative_to(PREFIX))
            assert archive_pins[rel] == rec['sha256'], module
            official_objects += 1
    assert local_objects == 383
    full_log = (BUILD / 'logs/AllExportedAxioms.log').read_text()
    declarations = re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$', full_log, re.MULTILINE)
    declared = {name: module for module, name in declarations}
    assert len(declared) == len(declarations)
    printed = {}
    print_count = 0
    for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", full_log):
        assert name not in printed, name
        printed[name] = sorted(a.strip() for a in axioms.split(',') if a.strip())
        print_count += 1
    for name in re.findall(r"'([^']+)' does not depend on any axioms", full_log):
        assert name not in printed, name
        printed[name] = []
        print_count += 1
    assert set(printed) == set(declared) == set(report['theorems'])
    assert print_count == report['theorem_count']
    for name, axioms in printed.items():
        assert set(axioms) <= ALLOWED, (name, axioms)
        assert report['theorems'][name] == {'module': declared[name], 'axioms': axioms}, name
    unsafe_records = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', full_log, re.MULTILINE)
    unsafe = {name for _, name in unsafe_records}
    all_dependencies = {a for axioms in printed.values() for a in axioms}
    assert not unsafe.intersection(all_dependencies)
    for name in EXPECTED:
        assert name in declared, name
    assert printed['SevenColumn.Certificate739.allRowsFast'] == []
    assert not re.search(r'(^|\n).*\berror:', full_log)
    counts = collections.Counter(declared.values())
    assert report['theorems_per_module'] == {m: counts[m] for m in report['sources']}
    independent_inventory_log = (WORK / 'inventory-only.log').read_text()
    independent_inventory_count = int(re.search(r'^INVENTORY_TOTAL_THEOREMS (\d+)$', independent_inventory_log, re.MULTILINE).group(1))
    independent_private_count = int(re.search(r'^INVENTORY_PRIVATE_NAME_THEOREMS (\d+)$', independent_inventory_log, re.MULTILINE).group(1))
    independent_module_counts = {m: int(n) for m, n in re.findall(r'^INVENTORY_MODULE (\S+) (\d+)$', independent_inventory_log, re.MULTILINE)}
    assert independent_inventory_count == len(declared)
    assert independent_module_counts == report['theorems_per_module']
    assert read(WORK / 'inventory-only.json')['exit_code'] == 0
    source_counts = read(WORK / 'source-theorem-counts.json')
    for module, count in source_counts.items():
        assert counts[module] >= count, (module, counts[module], count)
    result = {
        'status': 'PASS', 'source_commit': report['source_commit'],
        'independent_execution': True,
        'fresh_source_module_count': len(report['sources']),
        'source_bytes': sum(r['bytes'] for r in report['sources'].values()),
        'successful_source_build_count': len(source_builds),
        'audited_theorem_count': len(declared),
        'separate_inventory_only_count': independent_inventory_count,
        'separate_inventory_private_name_count': independent_private_count,
        'separate_inventory_matches_exhaustive_audit_per_module': True,
        'explicit_source_theorem_count': sum(source_counts.values()),
        'allowed_axioms': sorted(ALLOWED),
        'actual_axiom_union': sorted(all_dependencies),
        'axiom_set_counts': {';'.join(k) or '(none)': v for k,v in collections.Counter(tuple(x) for x in printed.values()).items()},
        'unsafe_implementation_axiom_count': len(unsafe_records),
        'unsafe_implementation_axioms_in_accepted_theorem_dependencies': [],
        'endpoint_axioms': {name: printed[name] for name in EXPECTED},
        'imported_local_object_count': local_objects,
        'imported_official_object_count': official_objects,
        'all_imported_standard_objects_match_pinned_official_archive': True,
        'all_sources_objects_logs_and_compiler_pins_rechecked_after_completion': True,
        'checker_exit_code': invocation['checker_exit_code'],
        'started_at_utc': invocation['started_at_utc'],
        'checker_finished_at_utc': invocation['checker_finished_at_utc'],
        'checker_report_sha256': sha(BUILD / 'verification.json'),
        'full_axiom_log_sha256': sha(BUILD / 'logs/AllExportedAxioms.log'),
        'no_196_739_palindrome_is_restricted_family_avoidance_not_P196': True,
        'ancestry_statement': 'For all natural A,P,t: 0 < A and PalindromeStarts739 P and ordinary orbit A t = P imply t <= 39. There is no digit-width bound.',
        'all_time_statement': 'For every natural t, not PalindromeStarts739 (ordinary orbit 196 t).',
        'runner_generic_numerical_flag_explanation': 'check.py deliberately retains numerical_739_instance_established_by_this_report=false because the generic runner does not interpret theorem statements. This independent report additionally checks the complete source closure and explicit endpoint statements and records the completed restricted numerical result.',
    }
    write(WORK / 'independent-verification.json', result)
    DEST.mkdir(exist_ok=True)
    assert not (DEST / 'verification.json').exists(), 'Final evidence already exists'
    for name in ['independent_controls.py', 'independent_finalize.py', 'recover_snapshot.py', 'invocation.json', 'independent-preflight.json', 'independent-verification.json', 'independent-source-pins.json', 'official-archive-member-pins.json', 'source-theorem-counts.json', 'collector-reference-verification.json', 'operational-diagnostics.json', 'runner-output.log']:
        shutil.copyfile(WORK / name, DEST / name)
    for path in sorted(WORK.glob('shim-inspection*')):
        shutil.copyfile(path, DEST / path.name)
    for pattern in ['InventoryOnly.lean', 'inventory-only.*', 'audit-progress-*.json']:
        for path in sorted(WORK.glob(pattern)):
            shutil.copyfile(path, DEST / path.name)
    for name in ['verification.json', 'source-pins.json']:
        shutil.copyfile(BUILD / name, DEST / name)
    shutil.copytree(BUILD / 'logs', DEST / 'logs')
    shutil.copyfile(BUILD / 'snapshot/AllExportedAxioms.lean', DEST / 'AllExportedAxioms.lean')
    shutil.copyfile(PACKAGE / 'check.py', DEST / 'check.py')
    shutil.copyfile(ROOT / 'toolchain/lean', DEST / 'lean-wrapper.sh')
    shutil.copyfile(ROOT / 'toolchain/proc-self-compat.c', DEST / 'proc-self-compat.c')
    shutil.copyfile(PREFIX / 'src/lean/Lean/Util/CollectAxioms.lean', DEST / 'Lean-CollectAxioms-reference.lean')
    snapshot_members = [{
        'module': module, 'original_path': rec['original_path'],
        'source_commit': report['source_commit'], 'git_blob_sha1': rec['git_blob_sha1'],
        'recovered_path': rec['snapshot'], 'bytes': rec['bytes'], 'sha256': rec['sha256'],
    } for module, rec in sorted(report['sources'].items())]
    write(DEST / 'source-snapshot-inventory.json', {
        'source_commit': report['source_commit'],
        'recovery_command': 'python recover_snapshot.py --repo /path/to/p196-algorithm --output /new/empty/snapshot',
        'members': snapshot_members,
        'excluded': 'The 383 duplicate source copies and all compiled .olean files remain outside the repository. Original sources are preserved at the exact Git commit and individually byte/hash pinned here; recover_snapshot.py recreates them using git show and verifies every SHA256. Exact local and standard object SHA256 pins are in verification.json. No substantive log is excluded.',
        'audit_source': {'path': 'AllExportedAxioms.lean', 'bytes': (DEST / 'AllExportedAxioms.lean').stat().st_size, 'sha256': sha(DEST / 'AllExportedAxioms.lean')},
    })
    readme = f'''# Independent clean whole-chain rebuild and axiom audit

**PASS.** A new independent clean reviewer executed a fresh source-only build of all {len(report['sources'])} local modules selected by `Conclusion739` and `TerminalObstruction`, then independently rechecked the complete compiled theorem inventory and all source, object, log, and compiler pins. This is an independent execution, not the earlier parent-run structural build.

Source commit: `{report['source_commit']}`. Checker exit status: **0**. Started: `{invocation['started_at_utc']}`; checker completed: `{invocation['checker_finished_at_utc']}`. Every source matched the committed bytes before being copied into the new build directory. No pre-existing local `.olean` was reused. Subsequent evidence-only Git commits did not change this pinned source selection.

## Exact accepted results

- `SevenColumnKernel.Finite739.ancestry_bound39`: for every natural `A`, `P`, and `t`, if `A > 0`, `P` is a decimal palindrome beginning with 739, and the ordinary reverse-and-add orbit from `A` reaches `P` at time `t`, then `t ≤ 39`. There is no digit-length restriction.
- `SevenColumnKernel.Finite739.no_196_739_palindrome`: at every natural time `t`, the ordinary orbit from 196 is not a palindrome beginning with 739.
- `TerminalObstruction` additionally excludes the pair-column prefix `[1,9,6]` at positive times under its stated width hypothesis. These are pair sums, not the digits of 196.

The all-time conclusion concerns the restricted 739 palindrome family. It does **not** prove P196 or decimal Lychrel existence. The accepted statements have no unsupplied finite-certificate premises.

## Exhaustive theorem and axiom checks

The compiled local closure contains **{len(declared)} theorem constants**, including private and compiler-generated theorems; the source contains {sum(source_counts.values())} explicit theorem declarations. These are coverage counts, not numbers of independent mathematical results. `AllExportedAxioms.lean` discovers the complete compiled inventory by module ownership. The complete substantive output is retained at `logs/AllExportedAxioms.log`.

A separately executed inventory-only command counted the same {independent_inventory_count} theorem constants, including {independent_private_count} names in the `_private` namespace, and its per-module counts agree exactly with the exhaustive audit. This diagnostic was authorized while the long aggregate audit was running. It introduced no theorem and did not replace any axiom check. Its source, full output, timing, and the original audit's measured CPU-progress samples are preserved.

Every discovered theorem has exactly one returned axiom report. Every transitive axiom set is contained in `propext`, `Classical.choice`, and `Quot.sound`; the actual union is exactly those three. No `sorryAx`, custom logical axiom, or native evaluation axiom occurs. `allRowsFast` has no axioms. The endpoint-specific sets and the complete per-theorem inventory are preserved in the JSON reports.

There are {len(unsafe_records)} compiler-generated unsafe implementation axiom declarations. None occurs transitively in an accepted theorem. Their existence is not silently treated as logical proof: the runner rejects safe custom axioms and allowlists the transitive dependencies of every theorem. The inspected official `Lean.Util.CollectAxioms` implementation visits the checked kernel environment, recursively follows types and values, and records all `axiomInfo` entries regardless of their unsafe flag. Its source was byte-compared to the pinned release archive. The local source scan also found no proof escape or native evaluator constructs.

## Toolchain and isolation

Official Lean **4.19.0**, release commit `6caaee842e94`. Compiler binary SHA256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Official archive SHA256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

Preflight compared 1,476 compiler, shared-library, and standard-object archive members with the installation. The final audit imported {local_objects} newly built local objects and {official_objects} standard objects; every standard object matches that archive. The existing official archive was reused and independently hashed; no independent network re-download is claimed.

The transparent wrapper preloads only the documented `/proc/<current-pid>/exe` to `/proc/self/exe` compatibility shim. Its C source, binary SHA256, exported symbols, disassembly, and read-only data inspection are preserved. It does not interpose Lean or kernel functions. No inherited `LD_PRELOAD` or `LD_LIBRARY_PATH` override was present. The runner clears external Lean import-path variables and sets `LEAN_PATH` to the fresh source/object directory.

Two build workers were authorized. Each compiler used `-j1 -DElab.async=false`. No memory limit was imposed. Every compilation command, exit code, timing, peak RSS, and substantive output is retained in `verification.json`, `runner-output.log`, and `logs/`.

## Evidence and reproduction

- `independent-verification.json`: independent post-build acceptance checks and exact endpoint interpretation.
- `verification.json`: unmodified runner report, full source/object/compiler pins, complete theorem inventory, and all command records.
- `preflight-01/`: frozen historical checkpoint explicitly labeled full rebuild IN_PROGRESS at that time.
- `independent_controls.py`, `independent_finalize.py`, and `check.py`: the controls and exact committed runner used.
- `source-snapshot-inventory.json` and `recover_snapshot.py`: exact original-source references and SHA256-verified source recovery.

The generic runner retains `numerical_739_instance_established_by_this_report=false` because it does not interpret mathematical statements. This is not a failed finite check. The independent report additionally checks the final statements and complete unconditional application, and records the restricted numerical result explicitly. The runner also records original-source stability rather than enforcing it; this independent acceptance step separately enforces every original-source hash at completion.

From the source checkpoint, with a pinned Lean executable or the documented transparent wrapper:

```bash
python proofs/contributions/agent-104/seven-column-kernel/check.py /absolute/path/to/lean --evidence /new/empty/build --module Conclusion739 --module TerminalObstruction --jobs 2 --require-committed
```

The exact successful invocation and paths are in `invocation.json`. To reconstruct the flattened source snapshot, run `python recover_snapshot.py --repo /path/to/p196-algorithm --output /new/empty/snapshot` from this evidence directory. The recovery tool reads only the pinned Git commit and verifies every source SHA256.

Duplicate fresh-build sources and all `.olean` files remain outside the repository at `/workspace/scratch/7649db1e242c/build104-independent-final/rebuild/snapshot`. They are excluded as reproducible build infrastructure. Their exact hashes, the committed original sources, all substantive logs, and the generated axiom-audit source are retained. No build error or rejected proof occurred in this independent run.
'''
    (DEST / 'README.md').write_text(readme)
    write(DEST / 'final-evidence-manifest.json', {
        'source_commit': report['source_commit'], 'status': 'PASS',
        'files': {str(p.relative_to(DEST)): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(DEST.rglob('*')) if p.is_file()},
        'manifest_excludes_itself': True,
    })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
