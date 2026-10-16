#!/usr/bin/env python3
"""Independent build and transitive axiom audit of the exact safety modules."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path('/workspace/scratch/4ce7c54d31f6')
REPO = ROOT / 'p196-repo'
CONTRIBUTION = REPO / 'proofs/contributions/agent-3/finite-horizon-overflow-20261016'
HERE = Path(__file__).resolve().parent
BUILD = HERE / 'fresh-build'
LEAN = ROOT / 'lean-runtime/lean-4.19.0-linux/bin/lean'
SOURCES = [
    ('PeriodObstructions', REPO/'proofs/PeriodObstructions__70ce034b31b5b218.lean',
     '83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a'),
    ('ActualWordBridge', REPO/'proofs/ActualWordBridge__7f032d27940694a8.lean',
     '3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6'),
    ('FamilyDefinitions', CONTRIBUTION/'FamilyDefinitions.lean',
     '497ffe833495c50e7df5714fd50c0a4835aaf96f71ec8d21fc43102b1468a1d4'),
    ('LychrelDigitSums', REPO/'proofs/LychrelDigitSums__0810ace083af80c5.lean',
     'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57'),
    ('DecimalSafeRuns', REPO/'proofs/DecimalSafeRuns__aaaac5a66315c5e2.lean',
     '2d0e44adfbfa2592b1eaedfb46d2dff3f62db0a2ca05171bb2a7c1a66ec03f22'),
    ('SafetyBridge', CONTRIBUTION/'SafetyBridge.lean',
     '18079ba07cccf1bcc9098320ae62f887ba080896be11bead43de6e7f26573e5e'),
    ('NormalizedSafety', CONTRIBUTION/'NormalizedSafety.lean',
     '6c344b93df1f8574dcf8ecf60c9db09d3f798c3df1b13831713af010c71652c1'),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    BUILD.mkdir(exist_ok=False)
    logs = HERE / 'logs'
    logs.mkdir(exist_ok=True)
    expected_lean = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
    assert sha256(LEAN) == expected_lean
    report = {'reviewer':'Agent #3 runtime/dependency specialist',
              'independent_of_safety_author':True,
              'claim_id':'55c0133a597cd3577fbbb864414fe4527729e554',
              'compiler':str(LEAN),'compiler_sha256':expected_lean,
              'fresh_build_directory':str(BUILD),'sources':[],'commands':[]}
    declarations = []
    for module, source, expected in SOURCES:
        assert sha256(source) == expected, (source,sha256(source),expected)
        target = BUILD/(module+'.lean')
        target.write_bytes(source.read_bytes())
        assert sha256(target) == expected
        report['sources'].append({'module':module,'source':str(source),
                                  'copy':str(target),'sha256':expected})
        if module in ['SafetyBridge','NormalizedSafety']:
            declarations.extend('P196.Agent3.OverflowHorizon.'+n for n in
                                re.findall(r'^(?:theorem|def)\s+(\S+)',target.read_text(),re.M))
    assert len(declarations)==19, declarations
    audit='import NormalizedSafety\n\n'+'\n'.join('#print axioms '+n for n in declarations)+'\n'
    (BUILD/'IndependentSafetyAxioms.lean').write_text(audit)
    (HERE/'IndependentSafetyAxioms.lean').write_text(audit)
    env=os.environ.copy()
    env['LEAN_PATH']=str(BUILD)
    for module in [m for m,_,_ in SOURCES]+['IndependentSafetyAxioms']:
        argv=[str(LEAN),'-o',module+'.olean',module+'.lean']
        start=time.monotonic()
        result=subprocess.run(argv,cwd=BUILD,env=env,text=True,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log=logs/(module+'.log')
        log.write_text(result.stdout)
        record={'argv':argv,'cwd':str(BUILD),'LEAN_PATH':str(BUILD),
                'exit_code':result.returncode,'seconds':time.monotonic()-start,
                'log':str(log)}
        report['commands'].append(record)
        (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
        print(module,'exit',result.returncode,'seconds',round(record['seconds'],3),flush=True)
        if result.returncode:
            print(result.stdout,flush=True)
            raise SystemExit(result.returncode)
        record['olean_sha256']=sha256(BUILD/(module+'.olean'))
    output=(logs/'IndependentSafetyAxioms.log').read_text()
    audited=set(re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)",output))
    assert audited==set(declarations),(audited,declarations)
    axioms=set(a.strip() for group in re.findall(r'axioms: \[([^\]]*)\]',output)
               for a in group.split(',') if a.strip())
    assert axioms<={'propext','Classical.choice','Quot.sound'},axioms
    for module in ['SafetyBridge','NormalizedSafety','IndependentSafetyAxioms']:
        output=(logs/(module+'.log')).read_text()
        assert 'sorryAx' not in output and 'Lean.ofReduceBool' not in output
        assert not re.search(r'declaration uses .*sorry',output)
    for _,source,expected in SOURCES:
        assert sha256(source)==expected,'Source changed during review: '+str(source)
    report['result']='PASS'
    report['new_declarations_audited']=declarations
    report['axiom_union']=sorted(axioms)
    report['source_hashes_stable']=True
    (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 19 safety declarations, fresh closure; axiom union',sorted(axioms))


if __name__=='__main__':
    main()
