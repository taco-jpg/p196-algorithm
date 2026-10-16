"""Root replay of the primary nonsymmetric proof and independent encoding audit."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'safe_language'
OUT = HERE / 'primary_sat'
OUT.mkdir(exist_ok=True)

def module(name):
    spec = importlib.util.spec_from_file_location(name, SOURCE / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

stem = 'dfa4_neg2'
paths = [SOURCE / n for n in ['synthesize_dfa.py','check_encoding.py','check_lrat.py','METHOD_AND_PROOF.md','STATUS.md',stem+'.cnf',stem+'.lrat']]
before = {p.name: sha(p) for p in paths}
(HERE / 'primary_sat_frozen_sources.json').write_text(json.dumps(before,indent=2)+'\n')
assert before[stem+'.cnf'] == '072ae39e17bc277de1a90cd1fa93f752546f276762e3ec79585e04899f1319e7'
assert before[stem+'.lrat'] == '9f86cc7c5e0aa8bb1788553171f355d369adef609464805b8e32a7d21dc0447b'
proof = module('check_lrat').check(SOURCE / (stem+'.cnf'), SOURCE / (stem+'.lrat'))
print(json.dumps(proof), flush=True)
(OUT / 'root_lrat_check.json').write_text(json.dumps(proof,indent=2)+'\n')
for ext in ['.cnf','.json','.variables.json.gz','.terminating.json.gz']:
    shutil.copyfile(SOURCE / (stem+ext), OUT / (stem+ext))
module('check_encoding').main(OUT / stem)
assert before == {p.name: sha(p) for p in paths}
(HERE / 'safe_language_review.json').write_text(json.dumps({
    'status':'PASS',
    'primary_proof_replayed':True,
    'primary_encoding_audit_reexecuted':True,
    'all_width_mathematical_reduction_read_and_reviewed':True,
    'source_sha256':before,
    'scope':'At most four complete deterministic pair-reading states, eleven center/end predicates, canonical folded words; no fixed seed or overflow clock.',
    'five_state_result':'UNKNOWN',
    'general_regular_case':'UNKNOWN',
    'decimal_existence_proved':False,
},indent=2)+'\n')
