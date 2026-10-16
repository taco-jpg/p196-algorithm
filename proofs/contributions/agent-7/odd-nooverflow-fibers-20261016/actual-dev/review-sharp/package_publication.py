#!/usr/bin/env python3
"""Pin the selective publication set without deleting files or touching Git."""
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[2]
REPO = PACKAGE.parents[3]
DEV = PACKAGE / 'actual-dev'
MANIFEST = DEV / 'PUBLICATION.json'
STAGE = DEV / 'STAGE_FILES.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def record(path):
    return {'path': path.relative_to(PACKAGE).as_posix(),
            'bytes': path.stat().st_size, 'sha256': sha(path)}

def main():
    old = json.loads(MANIFEST.read_text())
    old_kept = {r['path']: r for r in old['retained_files']}
    kept, omitted = [], []
    canonical = {p.stem: p for p in (PACKAGE / 'dependencies').glob('*.lean')}
    canonical.update({p.stem: p for p in PACKAGE.glob('*.lean')})
    canonical.update({p.stem: p for p in [
        DEV / 'review-oddcenter/ReviewCenter.lean',
        DEV / 'review-canonical/ReviewCanonical.lean',
        DEV / 'review-sharp/ReviewSharp.lean',
        DEV / 'review-sharp/ReviewComplete.lean',
    ]})
    for path in sorted(DEV.rglob('*')):
        if not path.is_file() or path in {MANIFEST, STAGE}:
            continue
        item = record(path)
        if item['path'] in old_kept:
            item['kind'] = old_kept[item['path']].get('kind', 'retained_evidence')
            kept.append(item)
        elif path.suffix == '.olean':
            source = path.with_suffix('.lean')
            if not source.is_file():
                raise ValueError('Object lacks retained or pinned source: ' + str(path))
            item.update(reason='Reproducible Lean compiler output. Exact source, compiler, commands and logs are retained or pinned.',
                        source_snapshot=source.relative_to(PACKAGE).as_posix(),
                        source_sha256=sha(source))
            omitted.append(item)
        elif path.suffix == '.lean' and path.parent.name == 'source' and path.stem in canonical and path.read_bytes() == canonical[path.stem].read_bytes():
            source = canonical[path.stem]
            item.update(reason='Byte-identical build snapshot. Canonical source and exact pin are retained; the build verification records this snapshot hash.',
                        canonical_source=source.relative_to(PACKAGE).as_posix(),
                        canonical_source_sha256=sha(source))
            omitted.append(item)
        else:
            item['kind'] = {
                '.log': 'compiler_or_audit_log',
                '.py': 'reproducibility_runner',
                '.json': 'verification_or_review_record',
                '.md': 'semantic_review_or_handoff',
                '.txt': 'retained_failure_diagnostic',
            }.get(path.suffix, 'retained_source_or_evidence')
            if path.name == 'PublicAudit.lean':
                item['kind'] = 'generated_complete_axiom_audit_source'
            elif path.suffix == '.lean':
                item['kind'] = 'review_fixture_or_unique_source_snapshot'
            kept.append(item)
    stage_paths = sorted({(PACKAGE / r['path']).relative_to(REPO).as_posix() for r in kept} |
                         {MANIFEST.relative_to(REPO).as_posix(), STAGE.relative_to(REPO).as_posix()})
    STAGE.write_text(json.dumps(stage_paths, indent=2) + '\n')
    stage_rec = record(STAGE)
    stage_rec['kind'] = 'flat_repository_relative_staging_list'
    kept.append(stage_rec)
    kept.sort(key=lambda r: r['path'])
    represented = {r['path'] for r in kept + omitted}
    actual = {p.relative_to(PACKAGE).as_posix() for p in DEV.rglob('*') if p.is_file() and p != MANIFEST}
    if represented != actual or len(represented) != len(kept) + len(omitted):
        raise ValueError('Manifest coverage or uniqueness failed')
    for item in omitted:
        if 'canonical_source' in item and (PACKAGE / item['path']).read_bytes() != (PACKAGE / item['canonical_source']).read_bytes():
            raise ValueError('Omitted source differs from its canonical copy')
    result = dict(old)
    result['role'] = 'odd actual arithmetic bridge author and independent center/canonical/sharp/arbitrary-output reviewer'
    result['retained_files'] = kept
    result['omitted_reproducible_files'] = omitted
    result['publication_note'] = ('Selective evidence publication only. All original OddActual draft snapshots, failed reviewer runner and diagnostic, compiler/audit logs, generated audit sources, verification records and review fixtures are retained. Omitted files remain local and are either byte-identical pinned source copies or reproducible compiler outputs. No files were deleted; this specialist made no Git or remote writes.')
    result['staging_list'] = 'actual-dev/STAGE_FILES.json'
    result['manifest_coverage'] = {'all_actual_dev_files_except_manifest_itself_accounted_for': True,
                                   'retained_count': len(kept), 'omitted_count': len(omitted),
                                   'flat_stage_count_including_manifest': len(stage_paths)}
    additions = [
        {'attempt': 'review-canonical/attempt-001', 'status': 'FAIL_BEFORE_LEAN', 'reason': 'Reviewer repository-path startup error; original runner and diagnosis retained. No theorem compiler failure.'},
        {'attempt': 'review-canonical/attempt-002', 'status': 'PASS_FRESH_LOCAL_CLOSURE', 'reason': 'Nine project modules plus five independent canonical boundary fixtures; 122 public and 285 module-origin audits.'},
        {'attempt': 'review-sharp/attempt-001', 'status': 'PASS_FRESH_LOCAL_CLOSURE', 'reason': 'Thirteen project modules plus eleven independent fixtures; 188 public and 431 module-origin audits.'},
        {'attempt': 'review-sharp/final-001', 'status': 'PASS_FRESH_LOCAL_CLOSURE', 'reason': 'Final fifteen-module project plus eighteen independent fixtures; 214 public and 468 module-origin audits, of which 450 originate in the project.'},
    ]
    history = {a['attempt']: a for a in result['attempt_history']}
    history.update({a['attempt']: a for a in additions})
    result['attempt_history'] = list(history.values())
    result['independent_reviews'] = [
        {'target': 'OddCenter', 'report': 'actual-dev/review-oddcenter/REVIEW.md', 'status': 'PASS'},
        {'target': 'OddCanonical and OddWords', 'report': 'actual-dev/review-canonical/REVIEW.json', 'status': 'PASS'},
        {'target': 'OddSharp', 'report': 'actual-dev/review-sharp/REVIEW.json', 'status': 'PASS'},
        {'target': 'OddOutputRange and OddComplete plus full final closure', 'report': 'actual-dev/review-sharp/FINAL_REVIEW.json', 'status': 'PASS'},
    ]
    result['final_independent_execution'] = {
        'path': 'actual-dev/review-sharp/final-001/verification.json',
        'sha256': sha(DEV / 'review-sharp/final-001/verification.json'),
        'registry_sha256': sha(PACKAGE / 'PROJECT_REGISTRY.json'),
        'status': 'PASS', 'project_module_count': 15,
        'project_theorem_constants': 450, 'fixture_theorem_constants': 18,
        'all_module_theorem_constants': 468, 'explicit_public_theorems': 214,
    }
    MANIFEST.write_text(json.dumps(result, indent=2) + '\n')
    assert sha(PACKAGE / 'PROJECT_REGISTRY.json') == 'ca9d1fa657f6fc786fa14ed0df2456333280ee8a5eb1a58cadeebb902ff16926'
    print(json.dumps({'manifest_sha256': sha(MANIFEST), 'stage_list_sha256': sha(STAGE),
                      **result['manifest_coverage']}, indent=2))

if __name__ == '__main__':
    main()
