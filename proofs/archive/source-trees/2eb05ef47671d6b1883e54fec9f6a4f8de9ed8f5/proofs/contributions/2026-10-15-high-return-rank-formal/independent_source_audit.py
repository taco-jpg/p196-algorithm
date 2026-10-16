#!/usr/bin/env python3
"""Independently compare the frozen Lean source/data with the actual-bridge graph."""
import gzip
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def main():
    source=(HERE/'HighReturnRank.lean').read_text()
    sh=hashlib.sha256(source.encode()).hexdigest()
    verification=json.loads((HERE/'verification.json').read_text())
    generation=json.loads((HERE/'generation.json').read_text())
    assert sh==verification['source_sha256']==generation['source_sha256']
    assert verification['status']=='PASS' and verification['exit_code']==0
    assert verification['source_unchanged']
    assert (HERE/'compile.log').read_text()==verification['audit_output']
    packed=(HERE/'finite_data.json.gz').read_bytes()
    raw=gzip.decompress(packed)
    assert hashlib.sha256(packed).hexdigest()==generation['compressed_sha256']
    assert hashlib.sha256(raw).hexdigest()==generation['raw_sha256']
    data=json.loads(raw)
    certificate=HERE.parent/'2026-10-15-full-high-return/prefix_certificate.json.gz'
    independent=json.loads(gzip.decompress(certificate.read_bytes()))['vertices']
    assert len(independent)==len(data['rows'])==len(data['ranks'])==900
    for i,v in enumerate(independent):
        assert v['id']==i and v['rank']==data['ranks'][i]
        assert data['rows'][i]==[c['target'] for c in v['controls']]
    # Parse the actual Lean rank expression without importing the generator.
    expression=source.split('def rank (i : Nat) : Nat := ',1)[1].split('\ndef checkVertex',1)[0].strip()
    tokens=re.findall(r'\(|\)|\bif\b|\bi\b|<|\bthen\b|\belse\b|\d+',expression)
    assert ''.join(tokens)==re.sub(r'\s+','',expression)
    position=0
    def parse():
        nonlocal position
        if tokens[position].isdigit():
            n=int(tokens[position]);position+=1;return n
        assert tokens[position:position+4]==['(','if','i','<']
        position+=4
        bound=int(tokens[position]);position+=1
        assert tokens[position]=='then';position+=1
        left=parse()
        assert tokens[position]=='else';position+=1
        right=parse()
        assert tokens[position]==')';position+=1
        return bound,left,right
    tree=parse()
    assert position==len(tokens)
    def evaluate(tree,i):
        while not isinstance(tree,int):
            bound,left,right=tree
            tree=left if i<bound else right
        return tree
    assert [evaluate(tree,i) for i in range(900)]==data['ranks']
    # Complete generator replay is isolated from the frozen package.
    with tempfile.TemporaryDirectory(prefix='p196-rank-source-review-') as d:
        temp=Path(d)
        shutil.copyfile(HERE/'generate.py',temp/'generate.py')
        subprocess.run([sys.executable,str(temp/'generate.py')],check=True,capture_output=True,text=True)
        for name in ['HighReturnRank.lean','generation.json','finite_data.json.gz']:
            assert (temp/name).read_bytes()==(HERE/name).read_bytes(),name
    names=re.findall(r'^theorem\s+(\w+)',source,re.M)
    assert names==['finite_check','checked_vertex','rank_le_three','edge_decreases','no_four_edges']
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b',source)
    audit=verification['audit_output']
    assert "'HighReturnRank.finite_check' does not depend on any axioms" in audit
    for name in names[1:]:
        assert f"'HighReturnRank.{name}' depends on axioms: [propext, Quot.sound]" in audit
    assert len(audit.splitlines())==5
    result={'result':'PASS','vertices':900,'controls':1800,'accepted_edges':258,
        'all_rows_equal_independent_graph':True,'all_ranks_equal_independent_graph':True,
        'actual_lean_rank_tree_values_checked':900,'isolated_generator_byte_reproduction':True,
        'new_kernel_build_performed':False,'theorems':names,
        'scope':'Finite Lean graph certificate source/data review. Actual-orbit reduction remains a separate written proof.',
        'files':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in
                 ['HighReturnRank.lean','generate.py','generation.json','finite_data.json.gz','verification.json','compile.log']},
        'independent_graph_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest()}
    (HERE/'independent_source_audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
