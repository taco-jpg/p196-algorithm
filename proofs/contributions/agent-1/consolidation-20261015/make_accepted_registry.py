#!/usr/bin/env python3
"""Generate the exact independently reviewed 38-module registry, never infer acceptance.

The complete path/hash/import mapping must match the frozen independent review
identity. Newly changed source or a larger later catalogue is rejected. This
first registry deliberately does not claim complete repository-wide coverage.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'proofs'))
from verify_project import code_only

EXPECTED_MAP = '59f7f540d107a7d35b27c4a00cc0e5075ec6fc8a5bf6a8114eeb34855e75e931'
BASE = 'b6f827418576027b1cff89746ee8077217963fce'
GROUPS = [
 ('proofs/contributions/2026-10-15-agent3-complementary-bulk', ['OuterCharge','OuterOrbit']),
 ('proofs/contributions/2026-10-15-agent9-alternating-scalar-boundary', ['AlternatingScalarBoundary']),
 ('proofs/contributions/2026-10-14-base-uniqueness-formal', ['SignedDigitUniqueness']),
 ('proofs/contributions/2026-10-15-base-reflection-formal', ['BaseReflection','ResetNormalization','PhysicalWidth','SeamSafety']),
 ('proofs/contributions/2026-10-15-base-reverse-add-formal', ['ReverseAdd']),
 ('proofs/contributions/agent-11/base-high-threshold', ['HighBaseNormalization','HighBasePairs','HighBaseThreshold','HighBaseNumeric','HighBaseFirstHit']),
 ('proofs/research/continuation', ['LychrelDigitSums']),
 ('proofs/research', ['Lychrel196Research']),
 ('proofs/contributions/2026-10-15-carry-observability', ['PrefixCarryBound','ActualCarryObservability','DifferenceObservability']),
 ('proofs/contributions/agent-113/two-digit-prefix', ['TwoDigitProjection','TwoDigitGrowth','TwoDigitNumeric','TwoDigitCertificate','TwoDigitMain'] + ['TwoDigitCert'+s for s in ['10','20','32','40','41','60','64','65','76','80','81','82','83']]),
 ('proofs/contributions/agent-104/seven-column-kernel', ['PalindromeBridge'])]


def main() -> None:
    import re
    modules = {}
    for folder, names in GROUPS:
        for name in names:
            if name in modules: raise ValueError('Duplicate registered module')
            path = folder+'/'+name+'.lean'; data = (ROOT/path).read_bytes()
            imports = [d for line in re.findall(r'^\s*import\s+([^\n]+)', code_only(data.decode()), re.M) for d in line.split()]
            if name == 'Lychrel196Research': imports = ['LychrelDigitSums']
            modules[name] = {'path':path, 'sha256':hashlib.sha256(data).hexdigest(),
                'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest(), 'imports':imports}
    actual = hashlib.sha256(json.dumps(modules,sort_keys=True).encode()).hexdigest()
    if actual != EXPECTED_MAP:
        raise ValueError('Reviewed source/import map changed; new review required: '+actual)
    for name, rec in modules.items():
        origin = BASE
        if name == 'OuterOrbit': origin = '34c32e5455e8828161b89051cdd3bfe41176da07'
        elif name == 'AlternatingScalarBoundary': origin = 'c74581b4f146e1b540e4ef3713468c02b54728e6'
        elif name.startswith('HighBase'): origin = 'eefa6fee230d996065d9077b8ae2246af67d6e30'
        elif name in ['PrefixCarryBound','ActualCarryObservability','DifferenceObservability']: origin = '0b14bd101430e16ab06a5a9c706f0eda0a83767e'
        elif name.startswith('TwoDigit'): origin = '10eea4e977f864d605c97880f2347ba5f49d14bb'
        rec['historical_source_commit'] = origin
    modules['Lychrel196Research']['adapter'] = {
        'kind':'verified_embedded_foundation',
        'original_source_sha256':'f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c',
        'container_module':'LychrelDigitSums',
        'container_source_sha256':'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57',
        'original_excluded_line':'import Std','embedded_start_line_1_based':11,'embedded_line_count':4444}
    claims = [
      ('agent113-thirteen-prefix','TwoDigitMain','Agent113.TwoDigit',
       ['no_196_thirteen_arith','startsTwo_iff']+['exact_depth_'+s for s in ['10','20','32','40','41','60','64','65','76','80','81','82','83']],
       'Thirteen restricted palindrome-prefix ancestry bounds and exact sharpness; no unrestricted Lychrel theorem.'),
      ('agent3-five-step-charge','OuterOrbit','P196.Agent3.Charge',
       ['charge_zero_from_five','returned_outer_charge_zero','five_step_bound_sharp'],
       'Charge vanishes by five steps of the explicit outer list map; ordinary-integer semiconjugacy remains separate.'),
      ('agent9-alternating-spatial-boundary','AlternatingScalarBoundary','Agent9.AlternatingScalarBoundary',
       ['no_six_boundary','no_twelve_boundary'],
       'No finite spatial cut path from the root trace to either specified constant trace; actual exterior bridge remains separate.'),
      ('agent11-high-base-first-hit','HighBaseFirstHit','Agent11HighBase',
       ['numeric_two_step_threshold','numeric_interval_first_hit','binary_threshold_counterexample'],
       'Ordinary integer reverse-add in every integer base at least3, under exact high-pair-sum and canonical-digit hypotheses; first positive hit1 or2.'),
      ('agent10-nine-carry-reconstruction','DifferenceObservability','DifferenceObservability',
       ['nine_carry_words_determine_pair_sums','nine_carry_words_determine_next_integer'],
       'Identical complete carry words at times0..8 and equal initial width determine pair sums and the next integer, not the initial integer.')]
    registry = {'schema_version':1,'agent':'Agent #1','generation_owner':'agent1-batch2-exact-map-v1',
      'title':'Explicit accepted module registry: consolidation-reviewed core',
      'reviewed_source_map_sha256':EXPECTED_MAP,
      'toolchain':{'release':'4.19.0','commit_prefix':'6caaee842e94','allowed_axioms':['propext','Classical.choice','Quot.sound'],'compiler_arguments':['-j1','-DElab.async=false']},
      'catalogue_complete':False,
      'catalogue_blockers':[
       {'id':'PREEXISTING_ACCEPTED_SCOPE_CENSUS','status':'OPEN','description':'Pre-existing accepted scopes advertised in REPRODUCE.md and coordination handoffs remain accepted under their original records, but are not all represented by this first combined registry. A scoped PASS is not repository-wide verification.'},
       {'id':'BASELINE_BYTE_COVERAGE','status':'OPEN','description':'Initial main b6f8274 has 478 tracked proof files absent from its legacy manifest, including132 Lean files. Regeneration and complete tracked-file coverage verification remain required.'}],
      'projects':{'consolidation-core':{'modules':modules,
       'roots':['OuterOrbit','AlternatingScalarBoundary','HighBaseFirstHit','DifferenceObservability','TwoDigitMain'],
       'scope':'Previously accepted thirteen-prefix closure together with four independently reviewed branch-only packages; disjoint abstract-model and actual-arithmetic conclusions remain distinct.',
       'review_path':'contributions/agent-1/consolidation-20261015/reviews/batch2.md','historical_originals_unchanged':True}},
      'claims':[{'id':i,'project':'consolidation-core','module':m,'scope':scope,'endpoints':[ns+'.'+e for e in ends]} for i,m,ns,ends,scope in claims],
      'retained_not_accepted':[{'path':'contributions/agent-113/five-layer/FourColumnProjection.lean','status':'INTEGRATED_EVIDENCE_ONLY','reason':'WIP five-layer development preserved by PR47; absent from the independently verified thirteen-prefix closure. No five-layer obstruction acceptance.'}]}
    path = ROOT/'proofs/ACCEPTED_BUILD.json'
    if path.exists():
        old = json.loads(path.read_text())
        if old.get('catalogue_complete') or set(old.get('projects',{})) != {'consolidation-core'}:
            raise ValueError('Refusing to overwrite an expanded or completed catalogue')
        if old.get('reviewed_source_map_sha256',EXPECTED_MAP) != EXPECTED_MAP:
            raise ValueError('Refusing to overwrite a differently reviewed source map')
    path.write_text(json.dumps(registry,indent=2)+'\n')
    print('Wrote exact reviewed registry:',len(modules),'modules;',len(claims),'claim groups; global catalogue INCOMPLETE')


if __name__ == '__main__':
    main()
