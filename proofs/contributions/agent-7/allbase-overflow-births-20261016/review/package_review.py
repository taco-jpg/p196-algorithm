#!/usr/bin/env python3
"""Package checked review/canonical evidence without source, registry or Git edits."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[3]
REVIEW = PACKAGE / 'review'
VERIFY = PACKAGE / 'verification'
PROJECT = 'agent7-allbase-overflow-births'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return str(path.relative_to(REPO))


def write_json(path, data):
    with path.open('x') as stream:
        stream.write(json.dumps(data, indent=2) + '\n')


def evidence(path):
    return {'path': rel(path), 'sha256': sha(path), 'bytes': path.stat().st_size}


def main():
    stamp = datetime.now(timezone.utc).isoformat()
    registry_path = PACKAGE / 'PROJECT_REGISTRY.json'
    assert sha(registry_path) == '138fc4ac68beb8188812db092aae722476475dbb9644eb2e03d586fa5d6e733e'
    registry = json.loads(registry_path.read_text())
    modules = registry['projects'][PROJECT]['modules']
    assert len(modules) == 13
    final_path = REVIEW / 'final-003/verification.json'
    final = json.loads(final_path.read_text())
    assert sha(final_path) == 'eb4f8873b5001970d7a8140cb4a9b7c57661143e435010e9401ad49de8537101'
    assert final['status'] == 'PASS' and final['project_module_origin_theorem_count'] == 338
    canonical_folder = VERIFY / 'canonical-001'
    canonical_path = canonical_folder / 'verification.json'
    canonical = json.loads(canonical_path.read_text())
    assert sha(canonical_path) == '0d892b22478ed833adc75ee3da1e46b9a8420b7ba5fe0a12c9792e220a3db664'
    assert canonical['status'] == 'PASS' and canonical['source_tree_clean']
    assert canonical['agent'] == 'Agent #1' and canonical['registry_sha256'] == sha(registry_path)
    project = canonical['projects'][PROJECT]
    assert project['theorem_count'] == 338 and len(project['endpoints']) == 33
    for module, record in modules.items():
        assert sha(REPO / record['path']) == record['sha256']
        assert project['sources'][module]['sha256'] == record['sha256']
        assert final['source_records'][module]['sha256'] == record['sha256']
    for command in project['commands']:
        assert command['exit_code'] == 0
        assert sha(canonical_folder / command['log']) == command['log_sha256']
        assert '--trust=0' not in command['argv']
    files = json.loads((canonical_folder / 'FILES.json').read_text())
    for name, record in files.items():
        path = canonical_folder / name
        assert sha(path) == record['sha256'] and path.stat().st_size == record['bytes']
    gap_path = REVIEW / 'canonical-gap-source.json'
    assert sha(gap_path) == '004b0483eedae90777247fe10479794d26cd9b3f84f718524bf8d9559fb7914e'
    gap = json.loads(gap_path.read_text())
    assert not gap['issues'] and not gap['independent_execution_performed']
    observed = set()
    audit_text = (REVIEW / 'final-003/logs/PublicAudit.log').read_text()
    for raw in re.findall(r'^AUDIT_THEOREM \S+ \S+: \[([^\]]*)\]', audit_text, re.M):
        observed.update(re.split(r'\s*,\s*', raw.strip()) if raw.strip() else [])
    assert observed == {'propext', 'Classical.choice', 'Quot.sound'}

    equivalence = {
        'local_verified_commit': '96c618e812f3675c460d259ca76d3ce1b7073bd3',
        'published_source_commit': '4512ecb58abd9ff464d8d3b1c70b6abeb85472d0',
        'identical_full_tree': '3d952a0a1deef7aec912a93d8654b33734e4b847',
        'published_source_url': 'https://github.com/taco-jpg/p196-algorithm/commit/4512ecb58abd9ff464d8d3b1c70b6abeb85472d0',
        'draft_pr': 'https://github.com/taco-jpg/p196-algorithm/pull/127',
        'remote_evidence_attribution': 'Parent /root reported successful publication and independent readback of the identical full tree in its direct task message. This packet preparer did not perform another remote lookup or any Git mutation.',
        'locally_rechecked_evidence': 'The preserved canonical report records the local commit and source_tree_clean=true; all 13 current sources match both canonical and independent-review source SHA256 records and the frozen registry.',
    }
    assert canonical['source_commit'] == equivalence['local_verified_commit']
    actors = {
        'AdjacentBirths': '/root/odd_counts', 'ActualOverflowBirths': '/root/odd_counts',
        'OverflowDigits': '/root/gap_inventory', 'OverflowEndpoints': '/root/gap_inventory',
        'CanonicalOverflowBirths': '/root',
        'independent_execution_and_review_harness': '/root/runtime',
        'canonical_source_cross_review': '/root/gap_inventory',
        'affiliation': 'All are participants in the same Agent 7 collaboration. Cross-author review/execution is independent within that team; no external unaffiliated review is claimed.',
    }
    receipt = {
        'status': 'EXECUTION RECEIPT FOR PRESERVED CANONICAL PASS', 'prepared_at': stamp,
        'actual_executor': 'Agent #7 /root', 'prepared_by': 'Agent #7 /root/runtime',
        'executor_attribution': 'Parent directly reported performing the canonical run; preparer inspected the unchanged report, all command exit codes, source pins, complete FILES inventory and log hashes.',
        'historical_report_agent_label': canonical['agent'],
        'historical_label_explanation': 'The unchanged retained verifier hardcodes Agent #1. Its report is preserved byte-for-byte; the label is not relabeled as the current executor.',
        'report': evidence(canonical_path), 'files_inventory': evidence(canonical_folder / 'FILES.json'),
        'reference_verifier': evidence(REPO / 'proofs/verify_project__214bf7673efe116b.py'),
        'registry': evidence(registry_path),
        'compiler': canonical['compiler'], 'source_equivalence': equivalence,
        'project': PROJECT, 'modules': 13, 'new_public_endpoints': 33,
        'module_origin_theorems': 338, 'observed_theorem_axioms': sorted(observed),
        'compiler_generated_unsafe_implementation_constants': project['unsafe_implementation_axioms'],
        'actual_recorded_compiler_flags': ['-j1', '-DElab.async=false'],
        'trust_flag_note': 'The original canonical command records contain no explicit --trust flag. The separate independent review rebuilt every frozen project source with explicit --trust=0; these two execution descriptions are kept distinct.',
        'recorded_commands': project['commands'],
        'independent_review_report': evidence(final_path),
        'source_only_canonical_cross_review': evidence(gap_path),
        'affiliation': actors['affiliation'],
        'scope': 'Scoped finite one-step all-base overflow theorem; repository_wide_pass remains false.',
    }
    write_json(VERIFY / 'AGENT7_EXECUTION_RECEIPT.json', receipt)

    findings = [
        {'area': 'Original semantics', 'result': 'PASS', 'detail': 'actualDigits, incoming, terminal, ordinaryTags, pairs and eval are the unchanged original APIs. Arbitrary Bool tags are erased by actual ordinary carrying. The new arithmetic expression is proved equal to these actual digits before it is used.'},
        {'area': 'All bases and coefficient bounds', 'result': 'PASS', 'detail': 'The local and actual birth classification uses every integer base b>=2 and old coefficients in [0,2*b-2]. Inherited b>=3 rigidity/safety statements remain restricted and are not used to extend the new result to base two.'},
        {'area': 'Actual carry coupling', 'result': 'PASS', 'detail': 'The two exterior prefix carries determine u=(a+l)/b and v=(z+h)/b. These are the genuine c_i and c_(L-i), not guessed independently. Both equations and the original incoming_bit bounds are supplied in the actual iff proofs.'},
        {'area': 'Shift and valid indices', 'result': 'PASS', 'detail': 'Computed terminal one gives output length L+1. Reflection is L-i, whose old symmetric coefficient is q_(i-1). The strict interior inequalities prove all getElem/getD accesses valid; outside-list default zeros cannot become births.'},
        {'area': 'Complete zero/max rows', 'result': 'PASS', 'detail': 'Each literal actual zero/max statement is an iff with the complete four oriented rows and the required carry conditions. The inherited row is the corresponding old homogeneous adjacent extreme pair. The neutral-neighbor result is necessary; neutrality alone does not suffice.'},
        {'area': 'Endpoint domains', 'result': 'PASS', 'detail': 'Both actual endpoints equal 1+q0%b and are positive for b>=2 without source bounds or symmetry. Bounded coefficients make each endpoint maximal iff b=2 and q0=1. For b>=3 the remainder upper bound rules out the maximum without coefficient bounds.'},
        {'area': 'Canonical quantifier coverage', 'result': 'PASS', 'detail': 'The wrapper quantifies over all finite DigitBounds/PositiveLast input words and tagged xs with literal xs.map fst=pairs digits and original terminal one. Bounds and symmetry are derived. hqs implies xs.length=digits.length; therefore indices 0, 0<i<L and L cover the entire actual output. Width one retains both output endpoints.'},
        {'area': 'Numerical reverse-add transport', 'result': 'PASS', 'detail': 'The wrapper directly applies unchanged ReverseAdd.reverse_add_normalization to obtain valid output digits, PositiveLast, exact width and eval b output=eval b digits+reversedValue b digits. It introduces no alternate integer representation or orbit map.'},
        {'area': 'Proof audit', 'result': 'PASS', 'detail': 'All 13 frozen project modules independently compiled from exact source with --trust=0 in final-001. After reviewer-only corrections, final-003 audits all 142 public roots and 349 module-origin theorem constants, including 338 project and 11 review constants. Only the three permitted foundational axioms occur in theorem dependencies.'},
        {'area': 'Scope limits', 'result': 'PASS', 'detail': 'The result is one finite reverse-add step. No run population, ancestry, lifetime, infinite avoidance or 196 conclusion follows. The existing binary 110 example is retained solely as a control.'},
    ]
    final_review = {
        'status': 'PASS', 'reviewed_at': stamp, 'reviewer': 'Agent #7 /root/runtime',
        'actors_and_affiliation': actors, 'registry': evidence(registry_path),
        'frozen_source_sha256': {m: r['sha256'] for m, r in modules.items()},
        'source_equivalence': equivalence, 'findings': findings, 'issues': [],
        'independent_execution': {
            'fresh_project_compilation': evidence(REVIEW / 'final-001/verification.json'),
            'final_report': evidence(final_path), 'project_modules': 13,
            'project_public_roots': 133, 'review_public_roots': 9,
            'combined_public_roots': 142, 'project_module_origin_constants': 338,
            'review_module_origin_constants': 11, 'combined_module_origin_constants': 349,
            'observed_theorem_axioms': sorted(observed), 'explicit_trust_flag': '--trust=0',
            'reuse_description': 'final-003 validates and copies the exact 13 objects freshly compiled with exit zero in final-001. It compiles only the corrected review fixture and then executes the complete audit; no failed fixture object is imported.',
            'unsafe_implementation_constants': final['unsafe_implementation_axioms'],
        },
        'retained_review_attempts': [
            {'attempt': 'review/final-001', 'status': 'FAIL in reviewer fixture only', 'detail': 'All 13 project modules exited zero. Two fixture membership eliminations failed because an empty-list branch remained; snapshot and log are retained.'},
            {'attempt': 'review/final-002', 'status': 'FAIL in reviewer audit command only', 'detail': 'All nine corrected fixture roots compiled. The audit command used unsupported display-only pp.width; its error, full axiom output and source are retained.'},
            {'attempt': 'review/final-003', 'status': 'PASS', 'detail': 'The unsupported display option was removed; corrected fixture and complete audit exited zero. No research source or registry changed.'},
        ],
        'uncompiled_initial_fixture_draft': {'path': rel(REVIEW / 'drafts/BoundaryContracts-001.lean'), 'interpretation': 'Preserved pre-execution draft with redundant dsimp calls, not a checked result.'},
        'canonical_execution': evidence(canonical_path),
        'canonical_executor_receipt': evidence(VERIFY / 'AGENT7_EXECUTION_RECEIPT.json'),
        'canonical_source_cross_review': evidence(gap_path),
        'inherited_dependency_review': evidence(REVIEW / 'DEPENDENCY_REVIEW.json'),
        'finite_discovery': {**evidence(REVIEW / 'finite-001/verification.json'),
                             'scope': '554788 coupled tuples in 41 bases; 10508 symmetric coefficient words in bases 2..7 and widths 1..6; 5236 overflow words and 22498 interior positions.',
                             'interpretation': 'Finite discovery/control evidence, not a universal proof.'},
        'publication': 'Selective manifests retain every substantive review source, draft, failure, audit source, log and report. Byte-identical copied project sources and compiler objects are omitted with exact hashes and reproduction reasons.',
    }
    write_json(REVIEW / 'FINAL_REVIEW.json', final_review)

    comment = '''## COMMENT — Agent 7 cross-author review

I reviewed this contribution as `/root/runtime` within the same Agent 7 collaboration. I did not author the five new research modules: `/root/odd_counts` wrote the arithmetic and actual classification; `/root/gap_inventory` wrote the digit bridge and endpoints; `/root` wrote the canonical wrapper. I prepared the independent review harness, boundary contracts and scoped registry. This is a cross-author team review; the affiliation is explicit.

**PASS for the claimed finite, one-step scope.** The actual pair uses the correct overflow reflection `L-i` and both recursively computed quotient carries. The two literal iff statements retain all four zero/maximum rows and their carry conditions. Endpoint positivity, the exact binary maximum exception, the width-one case, and the original canonical numeric reverse-add equality are covered. The literal coefficient projection derives source symmetry/bounds and fixes source/output lengths, so every valid output position is covered by the two endpoints or the strict interior quantifier. I found no material domain or converse gap. Neutrality is a necessary condition; no lifetime, population or 196 conclusion is claimed.

**Execution:** all 13 exact frozen project modules compiled from source with official Lean 4.19.0 and explicit `--trust=0` in `review/final-001`. The only failures were in my review code: two finite-membership fixture proofs, followed by an unsupported display-only audit option. Both failed attempts and their source/logs remain retained. `review/final-003` pins and reuses those same successfully compiled project objects, checks nine corrected boundary contracts, and completes the full audit: **142 public roots and 349 module-origin theorem constants**, comprising **338 project constants and 11 review constants**. Theorem dependencies are limited to `propext`, `Classical.choice`, and `Quot.sound`; the four compiler-generated unsafe implementation constants are recorded separately and are absent from theorem dependencies. Final report SHA256: `eb4f8873b5001970d7a8140cb4a9b7c57661143e435010e9401ad49de8537101`.

The parent's unchanged canonical verifier also passed on clean local commit `96c618e812f3675c460d259ca76d3ce1b7073bd3`, auditing 13 modules, 338 module-origin theorems and 33 new endpoints. Its original report `0d892b22478ed833adc75ee3da1e46b9a8420b7ba5fe0a12c9792e220a3db664` preserves the historical Agent #1 label and its original flags; `verification/AGENT7_EXECUTION_RECEIPT.json` identifies the actual Agent 7 parent executor. Parent publication/readback establishes equivalent remote source `4512ecb58abd9ff464d8d3b1c70b6abeb85472d0`, with identical full tree `3d952a0a1deef7aec912a93d8654b33734e4b847`.

The frozen registry is `138fc4ac68beb8188812db092aae722476475dbb9644eb2e03d586fa5d6e733e`. The separate canonical source review by `/root/gap_inventory` is retained at `review/canonical-gap-source.json`, SHA256 `004b0483eedae90777247fe10479794d26cd9b3f84f718524bf8d9559fb7914e`. Full findings, attribution, preserved failures and staging inventories are in `review/FINAL_REVIEW.json` and the publication manifests.
'''
    with (REVIEW / 'REVIEW_COMMENT.md').open('x') as stream:
        stream.write(comment)

    def classify(folder):
        retained, omitted = [], []
        metadata = {'PUBLICATION.json', 'STAGE_FILES.json', 'FINAL_STAGE_FILES.json'}
        for path in sorted(folder.rglob('*')):
            if not path.is_file() or (path.parent == folder and path.name in metadata):
                continue
            if path.suffix == '.olean':
                source_path = path.with_suffix('.lean')
                omitted.append({**evidence(path), 'kind': 'compiled_object',
                                'source_sha256': sha(source_path) if source_path.exists() else None,
                                'compiler_sha256': final['lean_sha256'],
                                'reason': 'Reproducible compiler object, not source proof evidence. Exact object identity is retained; all substantive source/log/report evidence is published.'})
            elif path.suffix == '.lean' and path.stem in modules and 'source' in path.parts:
                canonical_source = REPO / modules[path.stem]['path']
                assert sha(path) == sha(canonical_source) == modules[path.stem]['sha256']
                omitted.append({**evidence(path), 'kind': 'byte_identical_project_source_copy',
                                'retained_source': rel(canonical_source),
                                'retained_source_sha256': sha(canonical_source),
                                'reason': 'Exact frozen source already retained at the registry path; this build-directory copy adds no distinct source version.'})
            else:
                retained.append(path)
        return retained, omitted

    review_retained, review_omitted = classify(REVIEW)
    verify_retained, verify_omitted = classify(VERIFY)
    review_stage = sorted({rel(p) for p in review_retained} |
                          {rel(registry_path), rel(REVIEW / 'PUBLICATION.json'),
                           rel(REVIEW / 'STAGE_FILES.json'), rel(REVIEW / 'FINAL_STAGE_FILES.json')})
    verify_stage = sorted({rel(p) for p in verify_retained} |
                          {rel(VERIFY / 'PUBLICATION.json'), rel(VERIFY / 'STAGE_FILES.json')})
    combined = sorted(set(review_stage) | set(verify_stage))
    write_json(REVIEW / 'STAGE_FILES.json', review_stage)
    write_json(VERIFY / 'STAGE_FILES.json', verify_stage)
    write_json(REVIEW / 'FINAL_STAGE_FILES.json', combined)
    review_extra = [registry_path, REVIEW / 'STAGE_FILES.json', REVIEW / 'FINAL_STAGE_FILES.json']
    write_json(REVIEW / 'PUBLICATION.json', {
        'status': 'FROZEN REVIEW PUBLICATION PACKET', 'prepared_at': stamp,
        'prepared_by': 'Agent #7 /root/runtime', 'source_edits': False, 'git_or_remote_mutations': False,
        'retained_files': [evidence(p) for p in sorted(review_retained + review_extra)],
        'omitted_files': review_omitted,
        'metadata_self_record': 'This manifest is staged but does not include its own digest, avoiding self-reference.',
        'failure_policy': 'Every failed review report, original diagnostic log, unique failed source and original runner draft is retained. Failed attempts are not relabeled as PASS.',
        'repeated_fixture_snapshots': 'Per-attempt reviewer fixture/audit source snapshots are intentionally retained, including byte-identical fixed fixture inputs.',
        'cross_author_receipt': evidence(gap_path),
    })
    write_json(VERIFY / 'PUBLICATION.json', {
        'status': 'FROZEN CANONICAL EXECUTION PUBLICATION PACKET', 'prepared_at': stamp,
        'prepared_by': 'Agent #7 /root/runtime', 'actual_executor': 'Agent #7 /root',
        'retained_files': [evidence(p) for p in sorted(verify_retained + [VERIFY / 'STAGE_FILES.json'])],
        'omitted_files': verify_omitted, 'original_report_preserved': evidence(canonical_path),
        'metadata_self_record': 'This manifest is staged but does not include its own digest, avoiding self-reference.',
        'source_equivalence': equivalence,
    })
    assert len(combined) == len(set(combined))
    assert all((REPO / name).is_file() for name in combined)
    assert not any(name.endswith('.olean') for name in combined)
    for folder in (REVIEW, VERIFY):
        publication = json.loads((folder / 'PUBLICATION.json').read_text())
        for record in publication['retained_files']:
            assert sha(REPO / record['path']) == record['sha256']
    assert sha(registry_path) == canonical['registry_sha256']
    print(json.dumps({
        'review_stage_paths': len(review_stage), 'canonical_stage_paths': len(verify_stage),
        'combined_stage_paths': len(combined), 'review_omissions': len(review_omitted),
        'canonical_omissions': len(verify_omitted),
        'final_stage': evidence(REVIEW / 'FINAL_STAGE_FILES.json'),
        'final_review': evidence(REVIEW / 'FINAL_REVIEW.json'),
        'execution_receipt': evidence(VERIFY / 'AGENT7_EXECUTION_RECEIPT.json'),
        'review_manifest': evidence(REVIEW / 'PUBLICATION.json'),
        'canonical_manifest': evidence(VERIFY / 'PUBLICATION.json'),
    }, indent=2))


if __name__ == '__main__':
    main()
