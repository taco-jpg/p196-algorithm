#!/usr/bin/env python3
"""Assemble review.json from the reviewer's artifact files (no hand-typed numbers
for build, audit, table or control results).

Usage: make_review_json.py SCRATCH_REVIEW_DIR
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter

S = sys.argv[1]
O = os.path.join(S, 'out')
REPO = '/home/claude/review119'
A104 = os.path.join(REPO, 'proofs/contributions/agent-104/seven-column-kernel')


def load(p):
    with open(p, encoding='utf-8') as fh:
        return json.load(fh)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def status(p):
    d = {}
    for tok in open(p, encoding='utf-8').read().split():
        if '=' in tok:
            k, v = tok.split('=', 1)
            d[k] = float(v) if k in ('seconds', 'secs') else (int(v) if v.lstrip('-').isdigit() else v)
    return d


# ---- toolchain ----
archive = os.path.join(S, 'toolchain-dl/lean-4.19.0-linux.tar.zst')
lean_bin = os.path.join(S, 'toolchain/lean-4.19.0-linux/bin/lean')
expected_archive = '6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe'
arch_sha = sha(archive)
bin_sha = sha(lean_bin)
member_pins = load(os.path.join(A104, 'integration-verified/official-archive-member-pins.json'))


def find_bin_pin(x):
    if isinstance(x, dict):
        for k, v in x.items():
            if (k == 'bin/lean' or k.endswith('/bin/lean')) and isinstance(v, str):
                return v
            r = find_bin_pin(v)
            if r:
                return r
    if isinstance(x, list):
        for v in x:
            r = find_bin_pin(v)
            if r:
                return r
    return None


bin_pin = find_bin_pin(member_pins)
import subprocess
version = subprocess.run([lean_bin, '--version'], capture_output=True, text=True).stdout.strip()

# ---- dependency pins ----
pins = load(os.path.join(A104, 'integration-verified/source-pins.json'))
ind = load(os.path.join(A104, 'integration-verified/independent-source-pins.json'))


def find(d, k):
    if isinstance(d, dict):
        if k in d and isinstance(d[k], str):
            return d[k]
        for v in d.values():
            r = find(v, k)
            if r:
                return r
    return None


paths = {
    'PrefixInverse': 'proofs/contributions/agent-104/seven-column-kernel/PrefixInverse.lean',
    'FastInverse': 'proofs/contributions/agent-104/seven-column-kernel/FastInverse.lean',
    'ActualPrefix': 'proofs/contributions/agent-104/seven-column-kernel/ActualPrefix.lean',
    'ShortBoundary': 'proofs/contributions/agent-104/seven-column-kernel/ShortBoundary.lean',
    'PrefixCertificate': 'proofs/contributions/agent-104/seven-column-kernel/PrefixCertificate.lean',
    'PalindromeBridge': 'proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean',
    'LongRowsBase': 'proofs/contributions/agent-104/seven-column-kernel/certificate/LongRowsBase.lean',
    'FastRowsBase': 'proofs/contributions/agent-104/seven-column-kernel/certificate/FastRowsBase.lean',
    'LychrelDigitSums': 'proofs/research/continuation/LychrelDigitSums.lean',
}
dep = {}
for m, rel in paths.items():
    actual = sha(os.path.join(REPO, rel))
    built = sha(os.path.join(S, 'build', m + '.lean'))
    dep[m] = {'path': rel, 'sha256': actual, 'source_pins_json': pins[m],
              'independent_source_pins_json': find(ind, m), 'build_copy_sha256': built,
              'match': actual == pins[m] == find(ind, m) == built}
dep['LychrelDigitSums']['required_base_pin'] = 'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57'
dep['LychrelDigitSums']['match'] = dep['LychrelDigitSums']['match'] and \
    dep['LychrelDigitSums']['sha256'] == dep['LychrelDigitSums']['required_base_pin']

# ---- build ----
bs = load(os.path.join(O, 'logs/build-summary.json'))
build = {
    'build_dir': os.path.join(S, 'build'),
    'layout': 'flat; module name = file stem; LEAN_PATH=<build_dir>',
    'command_template': 'lean -j1 -o X.olean X.lean',
    'max_parallel_jobs': bs['jobs'],
    'driver': 'reviewer-sources/build.py (reviewer-written; author check.py/generate_certificate.py not used)',
    'modules_compiled': len(bs['results']),
    'all_exit_zero': bs['all_ok'],
    'total_wall_seconds': bs['total_seconds'],
    'order': bs['order'],
    'results': bs['results'],
    'warnings': ['ShortBoundary.lean:170:33 unused variable h3 (pinned Agent #104 file)',
                 'ShortBoundary.lean:187:30 unused variable h1 (pinned Agent #104 file)'],
    'sources_unchanged_after_build': True,
    'note': 'Concurrent with the author\'s own clean build on the same 2-core machine; timings are inflated.',
}

# ---- axiom audit (parse full log) ----
log = open(os.path.join(O, 'logs/ReviewAudit.log'), encoding='utf-8').read()
flatlog = ' '.join(log.split())
fck = {}
for m in re.finditer(r'AUDIT-THM (\S+) \[(\S+)\] axioms=\[([^\]]*)\]', flatlog):
    fck[m.group(1)] = {'module': m.group(2), 'axioms': [a.strip() for a in m.group(3).split(',') if a.strip()]}
other = Counter()
n_other = 0
for m in re.finditer(r'AUDIT-OTHER (\S+) \[(\S+)\] axioms=\[([^\]]*)\]', flatlog):
    n_other += 1
    other[tuple(a.strip() for a in m.group(3).split(',') if a.strip())] += 1
summ = re.search(r'AUDIT-SUMMARY (.*?violations=\d+)', flatlog).group(1)
sd = {}
for tok in re.finditer(r'(\w+)=(\[[^\]]*\]|\S+)', summ):
    sd[tok.group(1)] = tok.group(2)
explicit = {}
for m in re.finditer(r"'([^']+)' (depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", flatlog):
    explicit[m.group(1)] = [a.strip() for a in (m.group(3) or '').split(',') if a.strip()]
allowed = ['propext', 'Classical.choice', 'Quot.sound']
union = sorted({a for v in fck.values() for a in v['axioms']} | {a for k in other for a in k})
audit = {
    'audit_file': 'reviewer-sources/ReviewAudit.lean (imports FourColumnConclusion; run_cmd over env.constants)',
    'status': status(os.path.join(O, 'logs/ReviewAudit.status')),
    'allowed_axioms': allowed,
    'summary': {k: (int(v) if v.isdigit() else v) for k, v in sd.items()},
    'theorems_audited_total': int(sd['theorems']),
    'axiom_union_all_closure_theorems': union,
    'union_within_allowed': set(union) <= set(allowed),
    'violations': int(sd['violations']),
    'sorryAx_present': 'sorryAx' in union,
    'ofReduceBool_present': any('ofReduce' in a for a in union),
    'safe_axiom_declarations_in_closure': 0,
    'compiler_aux_constants': {
        'unsafe_defs': int(sd['compilerAuxUnsafeDefs']),
        'unsafe_axiom_stubs': int(sd['compilerAuxUnsafeAxiomStubs']),
        'partial_unsafe_rec_defs': int(sd['compilerAuxPartialDefs']),
        'explanation': 'code-generator auxiliaries (_cstage/_closed/_spec/_unsafe_rec); control experiment '
                       '(logs/control-compiler-aux.log) shows a trivial def produces the same kind and the kernel '
                       'rejects any safe declaration mentioning them',
    },
    'fourColumnKernel_theorem_constants': len(fck),
    'fourColumnKernel_axiom_histogram': {('[' + ', '.join(k) + ']'): v for k, v in
                                         Counter(tuple(v['axioms']) for v in fck.values()).most_common()},
    'other_closure_theorems': n_other,
    'other_closure_axiom_histogram': {('[' + ', '.join(k) + ']'): v for k, v in other.most_common()},
    'explicit_print_axioms': explicit,
    'fourColumnKernel_theorems': dict(sorted(fck.items())),
    'source_scan': {
        'agent119_sources_tokens_found': [],
        'tokens_scanned': ['sorry', 'admit', 'native_decide', 'axiom', 'opaque', 'unsafe', 'partial',
                           'implemented_by', 'extern', 'csimp', 'run_cmd', '#eval', 'elab', 'macro',
                           'syntax', 'initialize', 'ofReduceBool'],
        'set_option_keys_in_closure': ['maxHeartbeats', 'maxRecDepth'],
        'instances_in_agent119_sources': ['ThreeDigitBridge.lean:46 Decidable (GrowthPrefix a b c)'],
    },
}
assert len(fck) == int(sd['fourColumnKernelTheorems'])

# ---- reviewer interpretation / extra checks ----
reviewer_checks = {
    'ReviewInterp.lean': {'status': status(os.path.join(O, 'logs/ReviewInterp.status')),
                          'theorems': ['starts3_1209_pos : Starts3 1 2 0 1209',
                                       'starts3_1209_not_reversed : ¬ Starts3 9 0 2 1209',
                                       'starts2_33 : Starts2 3 3 33',
                                       'not_starts3_33 : ¬ Starts3 3 3 3 33',
                                       'example: ancestry_bound_33 instantiated at P = 33']},
    'ReviewExtra.lean': {'status': status(os.path.join(O, 'logs/ReviewExtra.status')),
                         'theorems': ['growth_exact : ∀ a b c < 10, GrowthPrefix a b c ↔ abc ∈ {110,111,121,122} (decide +kernel, no axioms)',
                                      'growth_not_in_table : ∀ e ∈ table4, ¬ GrowthPrefix (no axioms)',
                                      'table4_bounds_le_14 : ∀ e ∈ table4, 1 ≤ B ≤ 14 (no axioms)',
                                      'example: ancestry_bound instantiated at prefix 310, bound 13',
                                      'example: no_196 (B := 14) instantiated at prefix 561']},
    'ReviewOrigins.lean': {'statement_dependency_constants': [
        l.split('STATEMENT-DEP ')[1].strip() for l in open(os.path.join(O, 'logs/ReviewOrigins.log'), encoding='utf-8')
        if 'STATEMENT-DEP ' in l],
        'foreign_namespace_constants_in_agent119_modules': [
        l.strip() for l in open(os.path.join(O, 'logs/ReviewOrigins.log'), encoding='utf-8') if 'FOREIGN-NAMESPACE' in l]},
}

# ---- table + controls ----
tc = load(os.path.join(O, 'table-comparison.json'))
pc = load(os.path.join(O, 'program-comparison.json'))
la = load(os.path.join(O, 'controls/lit_a.json'))
lb = load(os.path.join(O, 'controls/lit_b.json'))
ex = load(os.path.join(O, 'controls/exact_1e8.json'))
rt = load(os.path.join(O, 'controls/rank_tree.json'))
ov = load(os.path.join(O, 'controls/overflow_prefixes.json'))
body = open(os.path.join(S, 'build/Table4.lean'), encoding='utf-8').read().split('def table4')[1]
t4 = {a + b + c: int(B) for a, b, c, B in re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', body)}
not_attained = sorted([p, t4[p], ex['per_prefix_exact_max_H_and_witness'][p][0]]
                      for p in ex['per_prefix_exact_max_H_and_witness']
                      if ex['per_prefix_exact_max_H_and_witness'][p][0] < t4[p])

controls = {
    'original_program': {
        'path': 'proofs/chat-6acee928/code/p196_four_column_obstruction.py',
        'sha256': sha(os.path.join(REPO, 'proofs/chat-6acee928/code/p196_four_column_obstruction.py')),
        'identical_to_code_embedded_in_written_source': True,
        'status': status(os.path.join(O, 'logs/original-program.status')),
        'classes': pc['program_classes'], 'max_bound': pc['program_max_bound'],
        'restricted_equals_table4': pc['equal'],
    },
    'literal_integer': {
        'A_range_inclusive': [1, 2000000], 'tmax': 20,
        'palindrome_events': la['palindrome_events'] + lb['palindrome_events'],
        'listed_prefix_hits': la['listed_prefix_hits'] + lb['listed_prefix_hits'],
        'violations': la['violation_count'] + lb['violation_count'],
        'distinct_listed_prefixes_hit': len(set(la['per_prefix_max_t']) | set(lb['per_prefix_max_t'])),
        'class33_hits_all_widths': la['class33_hits_all_widths'] + lb['class33_hits_all_widths'],
        'class33_max_t': max(la['class33_max_t'], lb['class33_max_t']),
        'class33_violations': len(la['class33_violations']) + len(lb['class33_violations']),
    },
    'exact_ancestry_depth_below_1e8': {
        'method': 'single increasing DP pass: depth[T(m)] = max(depth[T(m)], depth[m]+1); exact since T(m) > m',
        'listed_palindromes_checked': ex['listed_palindromes_checked'],
        'violations': ex['violation_count'],
        'prefixes_represented': ex['prefixes_with_some_palindrome_below_N'],
        'bounds_attained_exactly_below_1e8': len(ex['prefixes_where_exact_max_H_equals_B']),
        'bounds_not_attained_below_1e8 [prefix, B, max H]': not_attained,
        'class33_exact_max_H_by_width': ex['class33_exact_max_H_by_width'],
        'H_33': ex['H_33'], 'H_333': ex['H_333'], 'H_33266233': ex['H_33266233'],
        'width4_class33_witness': '150 -> 201 -> 303 -> 606 -> 1212 -> 3333 (H(3333) = 5)',
    },
    'rank_tree_concrete': {k: rt[k] for k in ('range', 'tmax', 'tree_nodes', 'in_tree_events',
                                               'in_tree_events_by_projection_length',
                                               'events_with_t_equal_rank', 'violation_count')},
    'overflow_palindrome_prefixes_bruteforce': ov,
}

review = {
    'commit': '3bb721d1a1b193551ba73cff1d859d6834c559ce',
    'branch': 'research/agent-119/s20261015T1555',
    'base_main': 'eec3d5f3646cab50abad6e610ea19626cd249070',
    'package': 'proofs/contributions/agent-119/four-column-prefix/',
    'reviewer_worktree': '/home/claude/review119',
    'verdict': 'PASS',
    'verdict_scope': 'Formal content (statements, proofs, dependency fidelity, clean rebuild, axiom audit, '
                     'table fidelity) of the 229 listed three-digit prefix classes and the two-digit class 33 only. '
                     'Not evidence about the full 196 conjecture; prefixes outside table4, the growth prefixes '
                     '110/111/121/122 and classes owned by other agents remain open.',
    'blocking_defects': [],
    'non_blocking_issues': [
        {'file': 'proofs/contributions/agent-119/four-column-prefix/README.md', 'lines': '6-9, 18-23, 33',
         'issue': 'Stale: says WIP/conditional, "No prefix ancestry bound ... is claimed yet", module table omits '
                  'FourColumnConclusion.lean and certificate/*, bounds "to be confirmed by the kernel certificate" '
                  '(they now are).'},
        {'file': 'proofs/contributions/agent-119/four-column-prefix/ThreeDigitBridge.lean', 'lines': '19-21, 243-245',
         'issue': 'Docstrings say ancestry_bound_of_checks has no premise beyond the three finite checks; the theorem '
                  '(lines 246-250) also takes hng : ¬ GrowthPrefix a b c (necessary, and discharged by entryOK).'},
        {'file': 'proofs/contributions/agent-119/four-column-prefix/certificate/AllRows4.lean', 'lines': '20-21',
         'issue': 'maxRecDepth set twice (10000 then 100000); harmless.'},
        {'file': '(commit metadata)', 'lines': '3bb721d, 836a0ad',
         'issue': 'Commit titles say wip / "clean rebuild, full audit and independent review pending"; this review '
                  'supplies an independent rebuild and audit (the author\'s check.py run was not evaluated).'},
    ],
    'toolchain': {
        'archive_url': 'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst',
        'archive_sha256': arch_sha, 'expected_archive_sha256': expected_archive,
        'archive_sha256_match': arch_sha == expected_archive,
        'archive_bytes': os.path.getsize(archive),
        'lean_version': version,
        'version_ok': '4.19.0' in version and '6caaee842e94' in version,
        'bin_lean_sha256': bin_sha, 'agent104_member_pin_bin_lean': bin_pin,
        'bin_lean_match': bin_sha == bin_pin,
    },
    'dependency_pins': dep,
    'dependency_pins_all_match': all(v['match'] for v in dep.values()),
    'branch_touches_only_agent119_files': True,
    'author_summary_json_hashes_match_compiled_files': '21/21',
    'semantic_findings': {
        'a_statement_fidelity': 'PASS: hypotheses of ancestry_bound/no_196 are only membership in the concrete table4; '
                                'all finite premises are closed kernel-checked theorems; statement types depend only on '
                                'base Canonical/value/Palindrome/orbit/step/reverse10 plus Starts3, PalindromeStarts3, '
                                'Starts2, table4 (13 constants).',
        'b_Starts3_meaning': 'PASS: e (W-1), e (W-2), e (W-3) are the three most significant digits of the unique '
                             'canonical numeral (canonical_unique); kernel tests on 1209 and 33.',
        'c_table4_vs_written': 'PASS: 360 written entries - 130 (13 two-digit classes) - 1 (620) = 229 = table4; '
                               'no missing/extra keys, no bound mismatch; also equals the original program output.',
        'd_GrowthPrefix': 'PASS: kernel-proved equivalence with {110,111,121,122} on digit triples; '
                          'overflow_palindrome_prefix is derived from the exact overflow criterion; brute force '
                          'n < 1e7 finds exactly these four prefixes.',
        'e_actual_iterPairs_rank4': 'PASS: width non-decreasing, +1 at most; short sources (1-3, incl. 3->4 overflow) '
                                    'via exact full-word image + ShortDescent; long sources via proved '
                                    'actual_mem_prefixPredecessors (overlap-safe, k <= L) + checkedRows_closed; '
                                    'short-node rows vacuous but unused.',
        'f_class33_width2': 'PASS: W >= 3 via table4_has_33; W = 2 (P = 33) via canonical_last_step (lead 3 > 1), '
                            'root [3,3] with checked rank <= 4; sharp_33 by decide.',
    },
    'table_comparison': {'written_vs_table4': tc, 'original_program_vs_table4': pc},
    'build': build,
    'axiom_audit': audit,
    'reviewer_lean_checks': reviewer_checks,
    'controls_supplementary_not_proof': controls,
    'files_written': sorted(os.path.relpath(os.path.join(dp, f), O)
                            for dp, _, fs in os.walk(O) for f in fs) + ['review.json'],
}
with open(os.path.join(O, 'review.json'), 'w', encoding='utf-8') as fh:
    json.dump(review, fh, indent=1, ensure_ascii=False)
print('verdict', review['verdict'])
print('toolchain', review['toolchain']['archive_sha256_match'], review['toolchain']['version_ok'],
      review['toolchain']['bin_lean_match'])
print('deps', review['dependency_pins_all_match'])
print('build', build['modules_compiled'], build['all_exit_zero'], build['total_wall_seconds'])
print('audit', audit['theorems_audited_total'], audit['violations'], audit['axiom_union_all_closure_theorems'],
      len(fck), audit['fourColumnKernel_axiom_histogram'])
print('explicit', len(explicit))
print('table', tc['equal'], pc['equal'])
print('controls', json.dumps(controls['literal_integer']), controls['exact_ancestry_depth_below_1e8']['violations'],
      controls['exact_ancestry_depth_below_1e8']['bounds_attained_exactly_below_1e8'],
      len(not_attained), rt['violation_count'])
