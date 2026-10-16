#!/usr/bin/env python3
"""Parse ReviewAudit.log (Lean messages may wrap over several lines).

Usage: parse_audit.py REVIEWAUDIT_LOG OUT_JSON
"""
import json
import re
import sys
from collections import Counter

log, out = sys.argv[1], sys.argv[2]
text = open(log, encoding='utf-8').read()
# split into messages at each "ReviewAudit.lean:L:C: severity:" header or at a bare #print line
# Messages are printed without a file header here; each starts at column 0
# with AUDIT-*, a quoted constant name, '@' or 'def'/'theorem', and may wrap.
parts = re.split(r"(?m)^(?=AUDIT-|'|@|def |theorem |[A-Za-z_][\w.]* : )", text)
thm = {}
other_count = 0
other_axioms = Counter()
summary = None
violations = []
for p in parts:
    body = re.sub(r'^ReviewAudit\.lean:\d+:\d+: (info|warning|error): ', '', p.strip())
    flat = ' '.join(body.split())
    m = re.match(r'AUDIT-THM (\S+) \[(\S+)\] axioms=\[(.*?)\]', flat)
    if m:
        axs = [a.strip() for a in m.group(3).split(',') if a.strip()]
        thm[m.group(1)] = {'module': m.group(2), 'axioms': axs}
        continue
    m = re.match(r'AUDIT-OTHER (\S+) \[(\S+)\] axioms=\[(.*?)\]', flat)
    if m:
        other_count += 1
        other_axioms[tuple(a.strip() for a in m.group(3).split(',') if a.strip())] += 1
        continue
    if flat.startswith('AUDIT-SUMMARY'):
        summary = flat
    if flat.startswith('AUDIT-VIOLATION'):
        violations.append(flat)
# explicit "#print axioms" outputs (they appear without the AUDIT prefix)
printed = {}
for m in re.finditer(r"'([^']+)' (depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", ' '.join(text.split())):
    axs = [a.strip() for a in (m.group(3) or '').split(',') if a.strip()]
    printed[m.group(1)] = axs

allowed = {'propext', 'Classical.choice', 'Quot.sound'}
named = {n: v for n, v in thm.items() if not re.search(r'\._proof_\d+$|\.eq_\d+$|\.eq_def$|\.match_\d+|\._simp_\d+|\._auxLemma', n)}
res = {
    'summary_line': summary,
    'violations': violations,
    'fourColumnKernel_theorem_constants': len(thm),
    'fourColumnKernel_named_theorems': len(named),
    'axiom_set_histogram_fourColumnKernel': {('[' + ', '.join(k) + ']'): v for k, v in
                                             Counter(tuple(v['axioms']) for v in thm.values()).most_common()},
    'other_closure_theorems_audited': other_count,
    'axiom_set_histogram_other_closure_theorems': {('[' + ', '.join(k) + ']'): v for k, v in other_axioms.most_common()},
    'all_within_allowed': all(set(v['axioms']) <= allowed for v in thm.values()) and
                          all(set(k) <= allowed for k in other_axioms),
    'explicit_print_axioms': printed,
    'named_theorems': {n: v for n, v in sorted(named.items())},
}
json.dump(res, open(out, 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('summary_line', 'fourColumnKernel_theorem_constants',
                                       'fourColumnKernel_named_theorems',
                                       'axiom_set_histogram_fourColumnKernel',
                                       'other_closure_theorems_audited',
                                       'axiom_set_histogram_other_closure_theorems',
                                       'all_within_allowed')}, indent=1))
print('explicit #print axioms entries:', len(printed))
for k in ['FourColumnKernel.Certificate.ancestry_bound', 'FourColumnKernel.Certificate.no_196',
          'FourColumnKernel.Certificate.no_196_listed_prefix', 'FourColumnKernel.Certificate.ancestry_bound_33',
          'FourColumnKernel.Certificate.no_196_33', 'FourColumnKernel.Certificate.sharp_33',
          'FourColumnKernel.Certificate.sharp_33_starts', 'FourColumnKernel.Certificate.table4_checked',
          'FourColumnKernel.Certificate.allRows', 'FourColumnKernel.Certificate.shortDescent4',
          'FourColumnKernel.actual_iterPairs_rank4']:
    print(k, printed.get(k))
