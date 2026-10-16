#!/usr/bin/env python3
"""Agent #1: positive and failure-injection checks for byte coverage, not proofs."""
import argparse,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
if args.output.exists():raise ValueError('Never overwrite prior test evidence')
ROOT=Path(__file__).resolve().parents[4]; P=ROOT/'proofs'; manifest=P/'MANIFEST.sha256'; original=manifest.read_bytes(); records=[]
def run(label,expected):
 p=subprocess.run(['python3','-B',str(P/'verify_release.py')],cwd=ROOT,capture_output=True,text=True)
 if (p.returncode==0)!=expected:raise RuntimeError(label+': unexpected result '+p.stdout+p.stderr)
 records.append({'case':label,'expected_success':expected,'exit_code':p.returncode,'log':p.stdout+p.stderr})
try:
 run('complete-git-index',True)
 lines=original.decode().splitlines(keepends=True)
 manifest.write_text(''.join(lines[1:]));run('missing-manifest-row',False)
 manifest.write_text(''.join(lines)+lines[0]);run('duplicate-manifest-row',False)
 manifest.write_text('0'*64+'  ../../unrelated\n'+original.decode());run('unsafe-path',False)
 manifest.write_bytes(original)
 source=P/'contributions/2026-10-15-agent3-complementary-bulk/OuterOrbit.lean';data=source.read_bytes()
 try:
  source.write_bytes(data+b'\n-- failure injection\n');run('altered-mathematical-source-bytes',False)
 finally:source.write_bytes(data)
 hide=P/'CONSOLIDATION.md';data=hide.read_bytes()
 try:
  hide.unlink();run('missing-tracked-file',False)
 finally:hide.write_bytes(data)
 dummy=P/'agent1-unlisted-negative-control.txt'
 if dummy.exists() or subprocess.check_output(['git','ls-files','--',str(dummy.relative_to(ROOT))],cwd=ROOT):raise ValueError('Negative-control path already exists')
 try:
  dummy.write_text('Temporary failure-injection file.\n');subprocess.run(['git','add','--',str(dummy.relative_to(ROOT))],cwd=ROOT,check=True);run('new-tracked-file-omitted-from-manifest',False)
 finally:
  subprocess.run(['git','rm','--cached','-f','--',str(dummy.relative_to(ROOT))],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
  dummy.unlink(missing_ok=True)
 run('restored-index-after-negative-controls',True)
finally:manifest.write_bytes(original)
# Hard links preserve source bytes without duplicating the entire exported tree.
# This positive control does not modify exported bytes or the source worktree.
with tempfile.TemporaryDirectory(prefix='agent1-export-',dir=ROOT.parent) as directory:
 dest=Path(directory)/'proofs';shutil.copytree(P,dest,copy_function=os.link,ignore=shutil.ignore_patterns('__pycache__'))
 p=subprocess.run(['python3','-B',str(dest/'verify_release.py')],cwd=directory,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('Export verification failed: '+p.stdout+p.stderr)
 result=json.loads(p.stdout);assert result['coverage_source'].startswith('export-tree-')
 records.append({'case':'complete-export-without-git','expected_success':True,'exit_code':p.returncode,'log':p.stdout+p.stderr})
output=args.output;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps({'agent':'Agent #1','scope':'Byte coverage and identity; not mathematical proof','manifest_sha256':hashlib.sha256(original).hexdigest(),'results':records,'status':'PASS'},indent=2)+'\n')
print('PASS',len(records),'positive/negative controls; output',output)
