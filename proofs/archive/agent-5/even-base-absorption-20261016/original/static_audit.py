#!/usr/bin/env python3
"""Static hygiene only: cannot establish Lean compilation or logical soundness."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import py_compile
import re
from verify_lean import lean_code_only, NS

HERE = Path(__file__).resolve().parent


def main() -> None:
    python_results = []
    for path in sorted(HERE.glob('*.py')):
        py_compile.compile(str(path), doraise=True)
        python_results.append(path.name)
    # Confirm comments and strings do not trigger false positives; real tokens do.
    sample = '/- sorry /- axiom -/ admit -/\n-- native_decide\ndef x := "sorry"\ntheorem ok : True := by trivial\n'
    forbidden = r'\b(?:sorry|admit|native_decide|sorryAx|axiom)\b'
    assert not re.findall(forbidden, lean_code_only(sample))
    assert re.findall(forbidden, lean_code_only('axiom missing : False')) == ['axiom']
    reports = {}
    names = []
    for filename in ('InitialValidity.lean', 'FiniteOverflow.lean'):
        path = HERE/filename
        text = path.read_text()
        cleaned = lean_code_only(text)
        bad = re.findall(forbidden, cleaned)
        assert not bad, (filename, bad)
        declarations = re.findall(r'^theorem\s+([A-Za-z0-9_]+)', cleaned, re.M)
        assert len(declarations) == len(set(declarations))
        names.extend(NS+n for n in declarations)
        reports[filename] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                              'theorem_names': declarations,
                              'excluded_source_tokens_found': bad}
    assert len(names) == len(set(names))
    (HERE/'Agent5AxiomAudit.lean').write_text(
        'import FiniteOverflow\n\n-- Prepared commands only. No axiom output was obtained in this run.\n' +
        '\n'.join('#print axioms '+name for name in names)+'\n')
    result = {'status':'STATIC_HYGIENE_PASS_NOT_LEAN_VERIFICATION',
              'python_syntax_checked':python_results, 'lean_sources': reports,
              'theorem_declarations':len(names),
              'kernel_compilations':0,'axiom_audits_executed':0,
              'notes':'Names and token scans are hygiene checks, not mathematical claims or formal acceptance.'}
    (HERE/'static_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'python_scripts':len(python_results),
                      'theorem_declarations':len(names),'kernel_compilations':0},indent=2))


if __name__ == '__main__':
    main()
