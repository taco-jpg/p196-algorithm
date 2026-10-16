"""Pin this scoped interval project and print every explicit exported theorem."""
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[4]
MODULES = ['Agent102RunDefs', 'Agent102AffineArithmetic', 'Agent102RunWord',
           'Agent102RunEndpoints', 'Agent102AffineRuns',
           'Agent102ParameterIntervalDefs', 'Agent102ParameterIntervalAlgebra',
           'Agent102ParameterIntervalCompact', 'Agent102AffineInequalityIntervals',
           'Agent102PiecewiseCounts', 'Agent102AffineRunParameterSets',
           'Agent102ParameterSetDecisions']
if '--controls' in sys.argv:
    MODULES.append('Agent102ParameterSetControls')
PROJECT = 'agent102-affine-parameter-intervals'
records, endpoints = {}, []
for module in MODULES:
    path = ROOT / 'proofs' / (module + '.lean')
    data = path.read_bytes()
    source = data.decode()
    records[module] = dict(path=str(path.relative_to(ROOT)),
        sha256=hashlib.sha256(data).hexdigest(),
        git_blob=hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest(),
        imports=re.findall(r'^import (\S+)$', source, re.M))
    stack = []
    for line in source.splitlines():
        m = re.match(r'namespace (\S+)$', line)
        if m:
            stack.append(m[1]); continue
        if re.match(r'end(?:\s+\S+)?$', line):
            if stack: stack.pop()
            continue
        m = re.match(r'(?:@\[[^\]]*\]\s*)?theorem (\S+)', line)
        if m:
            endpoints.append('.'.join(stack+[m[1]]))

names = [n for n in endpoints if re.fullmatch(r'[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*', n)]
registry = dict(schema_version=1, catalogue_complete=False,
    catalogue_blockers=['Scoped static literal affine-run parameter sets; actual decimal iteration closure, a realizable infinite safe family, and P196 are not supplied.'],
    toolchain=dict(version='4.19.0', commit='6caaee842e94',
        allowed_axioms=['propext','Classical.choice','Quot.sound']),
    projects={PROJECT: dict(scope='Exact finite interval unions for equality and palindrome parameters of actual Int.toNat-clipped affine run words; no cutoff prefix enumeration; complete quantified decisions and extensional interval certificates.',
        roots=[MODULES[-1]], modules=records)},
    claims=[dict(id='A102-EXACT-PARAMETER-INTERVALS',project=PROJECT,endpoints=names)],
    literal_audit_extra_endpoints=[n for n in endpoints if n not in names],
    registry_name_note='The unchanged verifier endpoint parser excludes ?. All explicit exports are retained in LiteralAudit, and all module-origin theorems are audited independently of spelling.',
    source_baseline='9361e8a8d13c731a4004b08957f4cd543b3ae38f')
(ROOT/'proofs/Agent102ParameterSets.registry.json').write_text(json.dumps(registry,indent=2)+'\n')
audit = 'import '+MODULES[-1]+'\n\n'+'\n'.join('#print axioms '+n for n in endpoints)+'\n'
dest = Path(__file__).resolve().parent/'audit'
dest.mkdir(exist_ok=True)
(dest/'LiteralAudit.lean').write_text(audit)
print(json.dumps({'modules':len(records),'literal_exports':len(endpoints),'registry_endpoints':len(names),'root':MODULES[-1]}))
