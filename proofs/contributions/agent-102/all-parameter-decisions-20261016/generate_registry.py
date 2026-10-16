"""Pin the exact Agent 102 modules and generate literal exported-theorem audits."""
from pathlib import Path
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[4]
MODULES = ['Agent102RunDefs', 'Agent102AffineArithmetic', 'Agent102RunWord',
           'Agent102RunEndpoints', 'Agent102AffineRuns',
           'Agent102AffineBoundary', 'Agent102AffineDecision',
           'Agent102RunDecision', 'Agent102AffineAllParameters', 'Agent102AllParameterControls']
PROJECT = 'agent102-all-parameter-decisions'
records = {}
endpoints = []
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

registry_names = [n for n in endpoints if re.fullmatch(r'[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*',n)]
registry = dict(schema_version=1, catalogue_complete=False,
    catalogue_blockers=['Scoped affine run comparison only; actual decimal iteration closure and P196 are not supplied.'],
    toolchain=dict(version='4.19.0', commit='6caaee842e94',
        allowed_axioms=['propext','Classical.choice','Quot.sound']),
    projects={PROJECT: dict(scope='Exact compressed literal-run equality at arbitrary parameters; sound and complete universal/existential equality and palindrome decisions from finite prefix and proven tail; concrete kernel controls.',
        roots=['Agent102AllParameterControls'], modules=records)},
    claims=[dict(id='A102-ALL-PARAMETER-DECISIONS',project=PROJECT,endpoints=registry_names)],
    literal_audit_extra_endpoints=[n for n in endpoints if n not in registry_names],
    registry_name_note='The unchanged verifier only accepts alphanumeric endpoint names. All exports, including names containing ?, remain in LiteralAudit and the exhaustive module-origin audit.',
    source_baseline='cba5dc441289bbed383972aa522a45c473879396')
(ROOT/'proofs/Agent102AllParameters.registry.json').write_text(json.dumps(registry,indent=2)+'\n')
audit = 'import Agent102AllParameterControls\n\n' + '\n'.join('#print axioms '+n for n in endpoints)+'\n'
dest=Path(__file__).resolve().parent/'audit'
dest.mkdir(exist_ok=True)
(dest/'LiteralAudit.lean').write_text(audit)
print(json.dumps({'modules':len(records),'exports':len(endpoints),'registry':'proofs/Agent102AllParameters.registry.json'}))
